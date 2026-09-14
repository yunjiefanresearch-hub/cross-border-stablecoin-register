#!/usr/bin/env python3
# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
"""Generate and verify multi-platform, wheel-only SHA-256 requirement locks.

The human-reviewed ``constraints/{runtime,dev,quality}.txt`` files remain the
pin source.  This tool resolves no versions.  It retrieves official release
metadata from ``https://pypi.org/pypi/.../json``, retains only non-yanked wheels
compatible with the supported target matrix, verifies dependency closure for
every target (including conditional and requested-extra dependencies), and
emits pip ``--require-hashes`` inputs plus an auditable provenance manifest.

Supported targets: Linux x86_64 CPython 3.10-3.13 and Windows amd64 CPython
3.12.  Source distributions are deliberately excluded: callers must also use
``--only-binary=:all:`` so build isolation cannot introduce unlocked inputs.
"""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse
import concurrent.futures
import dataclasses
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict, deque
from typing import Callable, Iterable

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.tags import Tag
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib


ROOT = pathlib.Path(__file__).resolve().parent.parent
CONSTRAINTS = ROOT / "constraints"
PYPROJECT = ROOT / "pyproject.toml"
PYPI_BASE = "https://pypi.org/pypi"
OFFICIAL_FILE_HOST = "files.pythonhosted.org"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
BOOTSTRAP_NAMES = frozenset({"pip", "setuptools", "wheel"})
PROVENANCE_SCHEMA = "cbsr/pypi-wheel-hash-provenance/v2"
PIN_SOURCES = ("pyproject.toml", "constraints/runtime.txt", "constraints/dev.txt", "constraints/quality.txt")


class LockError(RuntimeError):
    """The reviewed pin graph cannot produce the promised secure lock."""


@dataclasses.dataclass(frozen=True)
class Target:
    key: str
    python_version: str
    sys_platform: str
    platform_system: str
    os_name: str
    platform_machine: str
    glibc_max: str | None = None

    @property
    def environment(self) -> dict[str, str]:
        return {
            "implementation_name": "cpython",
            "implementation_version": self.python_version + ".0",
            "os_name": self.os_name,
            "platform_machine": self.platform_machine,
            "platform_python_implementation": "CPython",
            "platform_release": "",
            "platform_system": self.platform_system,
            "platform_version": "",
            "python_full_version": self.python_version + ".0",
            "python_version": self.python_version,
            "sys_platform": self.sys_platform,
            "extra": "",
        }


TARGETS = (
    # GitHub's pinned Ubuntu 24.04 runner carries glibc 2.39.  Treat that as a
    # hard upper compatibility bound so a future manylinux_2_40 wheel cannot be
    # admitted merely because its filename says x86_64.
    Target("linux-cp310-x86_64", "3.10", "linux", "Linux", "posix", "x86_64", "2.39"),
    Target("linux-cp311-x86_64", "3.11", "linux", "Linux", "posix", "x86_64", "2.39"),
    Target("linux-cp312-x86_64", "3.12", "linux", "Linux", "posix", "x86_64", "2.39"),
    Target("linux-cp313-x86_64", "3.13", "linux", "Linux", "posix", "x86_64", "2.39"),
    Target("windows-cp312-amd64", "3.12", "win32", "Windows", "nt", "AMD64"),
)


@dataclasses.dataclass(frozen=True)
class Pin:
    requirement: Requirement
    source: str
    line_number: int

    @property
    def name(self) -> str:
        return canonicalize_name(self.requirement.name)

    @property
    def version(self) -> str:
        specs = list(self.requirement.specifier)
        if len(specs) != 1 or specs[0].operator != "==" or specs[0].version.endswith(".*"):
            raise LockError(
                f"{self.source}:{self.line_number}: expected one exact == pin: {self.requirement}"
            )
        return specs[0].version

    def active(self, target: Target, extra: str = "") -> bool:
        if self.requirement.marker is None:
            return True
        env = target.environment
        env["extra"] = extra
        return self.requirement.marker.evaluate(env)


@dataclasses.dataclass(frozen=True)
class Wheel:
    filename: str
    sha256: str
    url: str
    requires_python: str | None
    tags: frozenset[Tag]


def _read_pins(path: pathlib.Path) -> tuple[list[Pin], list[str]]:
    pins: list[Pin] = []
    includes: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-c ", "--constraint ")):
            includes.append(line.split(maxsplit=1)[1])
            continue
        if line.startswith("-"):
            raise LockError(f"{path.name}:{number}: unsupported directive {line}")
        requirement = Requirement(line)
        if requirement.url is not None:
            raise LockError(f"{path.name}:{number}: direct URL dependencies are forbidden")
        pins.append(Pin(requirement, path.name, number))
    return pins, includes


def load_pin_sets(root: pathlib.Path = ROOT) -> dict[str, list[Pin]]:
    directory = root / "constraints"
    runtime, runtime_includes = _read_pins(directory / "runtime.txt")
    dev_only, dev_includes = _read_pins(directory / "dev.txt")
    quality, quality_includes = _read_pins(directory / "quality.txt")
    if runtime_includes:
        raise LockError("runtime.txt must not include another constraint file")
    if dev_includes != ["runtime.txt"]:
        raise LockError("dev.txt must contain exactly '-c runtime.txt'")
    if quality_includes:
        raise LockError("quality.txt must not include another constraint file")
    combined = runtime + dev_only
    bootstrap = [pin for pin in combined if pin.name in BOOTSTRAP_NAMES]
    if {pin.name for pin in bootstrap} != BOOTSTRAP_NAMES:
        raise LockError("dev constraints must pin pip, setuptools, and wheel for bootstrap")
    return {
        "runtime": runtime,
        "dev-only": dev_only,
        "dev": combined,
        "quality": quality,
        "bootstrap": bootstrap,
    }


def _fetch_pypi(name: str, version: str) -> dict:
    quoted_name = urllib.parse.quote(name, safe="")
    quoted_version = urllib.parse.quote(version, safe="")
    url = f"{PYPI_BASE}/{quoted_name}/{quoted_version}/json"
    request = urllib.request.Request(url, headers={"User-Agent": "cbsr-hash-lock/1"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                if response.geturl() != url:
                    raise LockError(f"unexpected PyPI metadata redirect: {response.geturl()}")
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if attempt == 2 or (exc.code != 429 and exc.code < 500):
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(attempt + 1)
    raise LockError(f"unreachable metadata retry state for {name}=={version}")


def _metadata_wheels(name: str, version: str, payload: dict) -> tuple[dict, list[Wheel]]:
    info = payload.get("info") or {}
    if canonicalize_name(info.get("name") or "") != canonicalize_name(name):
        raise LockError(f"PyPI metadata name mismatch for {name}=={version}")
    if Version(str(info.get("version"))) != Version(version):
        raise LockError(f"PyPI metadata version mismatch for {name}=={version}")

    wheels: list[Wheel] = []
    for item in payload.get("urls") or []:
        if item.get("packagetype") != "bdist_wheel" or item.get("yanked", False):
            continue
        filename = item.get("filename") or ""
        digest = ((item.get("digests") or {}).get("sha256") or "").lower()
        url = item.get("url") or ""
        parsed_url = urllib.parse.urlparse(url)
        if (parsed_url.scheme != "https" or parsed_url.netloc != OFFICIAL_FILE_HOST
                or parsed_url.query or parsed_url.fragment):
            raise LockError(f"non-official wheel URL for {name}=={version}: {url}")
        if not SHA256_RE.fullmatch(digest):
            raise LockError(f"invalid official SHA-256 for {filename}")
        try:
            parsed_name, parsed_version, _build, tags = parse_wheel_filename(filename)
        except Exception as exc:
            raise LockError(f"invalid wheel filename in PyPI metadata: {filename}: {exc}") from exc
        if canonicalize_name(parsed_name) != canonicalize_name(name) or parsed_version != Version(version):
            raise LockError(f"wheel identity mismatch: {filename} vs {name}=={version}")
        wheels.append(
            Wheel(
                filename=filename,
                sha256=digest,
                url=url,
                requires_python=item.get("requires_python"),
                tags=frozenset(tags),
            )
        )
    if not wheels:
        raise LockError(f"{name}=={version} has no non-yanked wheels on PyPI")
    return info, wheels


def _interpreter_compatible(tag: Tag, target: Target) -> bool:
    major, minor = (int(value) for value in target.python_version.split("."))
    interpreter = tag.interpreter
    if interpreter == "py3":
        return major == 3 and tag.abi == "none"
    if interpreter.startswith("py") and interpreter[2:].isdigit():
        digits = interpreter[2:]
        # Generic Python tags are ABI-independent. py310-none is also usable
        # by a newer Python 3 interpreter (packaging.tags.compatible_tags).
        return tag.abi == "none" and (
            digits == str(major)
            or (len(digits) > 1 and int(digits[0]) == major and int(digits[1:]) <= minor)
        )
    if not interpreter.startswith("cp") or not interpreter[2:].isdigit():
        return False
    digits = interpreter[2:]
    tag_major = int(digits[0])
    tag_minor = int(digits[1:])
    if tag.abi == "abi3":
        return tag_major == major == 3 and (major, minor) >= (tag_major, tag_minor)
    expected_abi = f"cp{major}{minor}"
    return (major, minor) == (tag_major, tag_minor) and tag.abi in {expected_abi, "none"}


def _platform_compatible(platform_tag: str, target: Target) -> bool:
    if platform_tag == "any":
        return True
    if target.sys_platform == "win32":
        return platform_tag == "win_amd64"
    legacy_floor = {"manylinux1_x86_64", "manylinux2010_x86_64", "manylinux2014_x86_64"}
    if platform_tag in legacy_floor:
        return True
    match = re.fullmatch(r"manylinux_(\d+)_(\d+)_x86_64", platform_tag)
    if not match or not target.glibc_max:
        return False
    wheel_glibc = (int(match.group(1)), int(match.group(2)))
    target_glibc = tuple(int(value) for value in target.glibc_max.split("."))
    return (2, 5) <= wheel_glibc <= target_glibc and wheel_glibc[0] == 2


def wheel_supports(wheel: Wheel, target: Target) -> bool:
    if wheel.requires_python:
        try:
            if Version(target.python_version + ".0") not in SpecifierSet(wheel.requires_python):
                return False
        except Exception as exc:
            raise LockError(
                f"invalid Requires-Python for {wheel.filename}: {wheel.requires_python}"
            ) from exc
    return any(
        _interpreter_compatible(tag, target) and _platform_compatible(tag.platform, target)
        for tag in wheel.tags
    )


def _active_pin_map(pins: Iterable[Pin], target: Target) -> dict[str, Pin]:
    active: dict[str, Pin] = {}
    for pin in pins:
        if not pin.active(target):
            continue
        previous = active.get(pin.name)
        if previous and previous.version != pin.version:
            raise LockError(
                f"{target.key}: overlapping pins for {pin.name}: "
                f"{previous.version} and {pin.version}"
            )
        active[pin.name] = pin
    return active


def _requirement_applies(requirement: Requirement, target: Target, extras: set[str]) -> bool:
    if requirement.marker is None:
        return True
    candidates = extras or {""}
    for extra in candidates | {""}:
        env = target.environment
        env["extra"] = extra
        if requirement.marker.evaluate(env):
            return True
    return False


def validate_dependency_closure(
    pins: list[Pin], metadata: dict[tuple[str, str], dict], targets: Iterable[Target] = TARGETS,
    roots: Iterable[Requirement] = (), project_extras: frozenset[str] = frozenset(),
) -> None:
    """Fail when any active Requires-Dist is absent or outside its exact pin."""
    roots = tuple(roots)
    for target in targets:
        active = _active_pin_map(pins, target)
        extras_by_name: dict[str, set[str]] = defaultdict(set)
        for name, pin in active.items():
            extras_by_name[name].update(pin.requirement.extras)
        for requirement in roots:
            _reject_direct_url(requirement, "project")
            if _requirement_applies(requirement, target, set(project_extras)):
                extras_by_name[canonicalize_name(requirement.name)].update(requirement.extras)
        queue = deque(active)
        processed: dict[str, frozenset[str]] = {}
        while queue:
            name = queue.popleft()
            pin = active[name]
            extras = extras_by_name[name]
            frozen_extras = frozenset(extras)
            if processed.get(name) == frozen_extras:
                continue
            processed[name] = frozen_extras
            info = metadata[(pin.name, pin.version)]
            for raw in info.get("requires_dist") or []:
                dependency = Requirement(raw)
                _reject_direct_url(dependency, f"{pin.name}=={pin.version} Requires-Dist")
                if not _requirement_applies(dependency, target, extras):
                    continue
                dep_name = canonicalize_name(dependency.name)
                dep_pin = active.get(dep_name)
                if dep_pin is None:
                    raise LockError(
                        f"{target.key}: {pin.name}=={pin.version} requires {dependency}, "
                        f"but {dep_name} has no active exact pin"
                    )
                if dependency.specifier and Version(dep_pin.version) not in dependency.specifier:
                    raise LockError(
                        f"{target.key}: {pin.name} requires {dependency}; "
                        f"lock selects {dep_name}=={dep_pin.version}"
                    )
                requested = set(dependency.extras)
                if not requested.issubset(extras_by_name[dep_name]):
                    extras_by_name[dep_name].update(requested)
                    queue.append(dep_name)


def _project_roots(root: pathlib.Path, include_dev: bool) -> list[Requirement]:
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    specs = list(project.get("dependencies") or [])
    if include_dev:
        specs.extend((project.get("optional-dependencies") or {}).get("dev") or [])
    return [Requirement(spec) for spec in specs]


def _reject_direct_url(requirement: Requirement, source: str) -> None:
    if requirement.url is not None:
        raise LockError(f"{source}: direct URL dependencies are forbidden: {requirement.name}")


def validate_project_roots(
    root: pathlib.Path, pins: list[Pin], include_dev: bool, targets: Iterable[Target] = TARGETS
) -> None:
    requirements = _project_roots(root, include_dev)
    for target in targets:
        active = _active_pin_map(pins, target)
        for requirement in requirements:
            _reject_direct_url(requirement, "project")
            if not _requirement_applies(requirement, target, {"dev"} if include_dev else set()):
                continue
            name = canonicalize_name(requirement.name)
            pin = active.get(name)
            if pin is None:
                raise LockError(f"{target.key}: project requirement {requirement} is not pinned")
            if requirement.specifier and Version(pin.version) not in requirement.specifier:
                raise LockError(
                    f"{target.key}: project requires {requirement}; lock selects {pin.version}"
                )


def _lock_targets(pin: Pin) -> tuple[Target, ...]:
    return tuple(target for target in TARGETS if pin.active(target))


def _selected_wheels(pin: Pin, wheels: list[Wheel]) -> list[Wheel]:
    targets = _lock_targets(pin)
    if not targets:
        raise LockError(f"{pin.requirement}: marker matches none of the supported targets")
    missing = [
        target.key for target in targets if not any(wheel_supports(wheel, target) for wheel in wheels)
    ]
    if missing:
        raise LockError(
            f"{pin.name}=={pin.version} has no compatible non-yanked wheel for: "
            + ", ".join(missing)
        )
    return sorted(
        {
            wheel.filename: wheel
            for wheel in wheels
            if any(wheel_supports(wheel, target) for target in targets)
        }.values(),
        key=lambda wheel: wheel.filename,
    )


def _render_requirement(pin: Pin, wheels: list[Wheel]) -> str:
    extras = f"[{','.join(sorted(pin.requirement.extras))}]" if pin.requirement.extras else ""
    requirement = f"{pin.requirement.name}{extras}=={pin.version}"
    if pin.requirement.marker is not None:
        requirement += f"; {pin.requirement.marker}"
    hashes = sorted({wheel.sha256 for wheel in wheels})
    continuation = " " + chr(92) + "\n    "
    return requirement + continuation + continuation.join(
        f"--hash=sha256:{digest}" for digest in hashes
    )


def render_lock(title: str, pins: list[Pin], selected: dict[tuple[str, str, str], list[Wheel]]) -> str:
    lines = [
        f"# GENERATED {title} — DO NOT EDIT BY HAND.",
        "# Source pins: constraints/runtime.txt, dev.txt, and/or quality.txt.",
        "# Hash source: official https://pypi.org JSON release metadata.",
        "# Target matrix: Linux x86_64 CPython 3.10-3.13; Windows amd64 CPython 3.12.",
        "--require-hashes",
        "--only-binary=:all:",
        "",
    ]
    if title == "development lock":
        lines.extend(["-r runtime-hashes.txt", ""])
    for pin in pins:
        key = (pin.name, pin.version, str(pin.requirement.marker or ""))
        lines.extend([_render_requirement(pin, selected[key]), ""])
    return "\n".join(lines).rstrip() + "\n"


def _bootstrap_closure(
    pins: list[Pin], metadata: dict[tuple[str, str], dict]
) -> set[str]:
    """Return bootstrap roots plus their target-specific dependency closure."""
    wanted = set(BOOTSTRAP_NAMES)
    for target in TARGETS:
        active = _active_pin_map(pins, target)
        queue = deque(BOOTSTRAP_NAMES)
        extras_by_name: dict[str, set[str]] = defaultdict(set)
        processed: dict[str, frozenset[str]] = {}
        while queue:
            name = queue.popleft()
            pin = active.get(name)
            if pin is None:
                raise LockError(f"bootstrap {name} is not pinned on {target.key}")
            extras_by_name[name].update(pin.requirement.extras)
            extras = frozenset(extras_by_name[name])
            if processed.get(name) == extras:
                continue
            processed[name] = extras
            for raw in metadata[(pin.name, pin.version)].get("requires_dist") or []:
                requirement = Requirement(raw)
                _reject_direct_url(requirement, f"bootstrap {pin.name}")
                if not _requirement_applies(requirement, target, set(extras)):
                    continue
                dep_name = canonicalize_name(requirement.name)
                dep_pin = active.get(dep_name)
                if dep_pin is None or Version(dep_pin.version) not in requirement.specifier:
                    raise LockError(f"bootstrap {pin.name} requires unpinned/incompatible {requirement} on {target.key}")
                wanted.add(dep_name)
                extras_by_name[dep_name].update(requirement.extras)
                queue.append(dep_name)
    return wanted


def _source_hashes(root: pathlib.Path) -> dict[str, str]:
    # Text normalization makes the same Git tree work on CRLF Windows checkouts.
    return {name: hashlib.sha256((root / name).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            for name in PIN_SOURCES}


def offline_fetcher(root: pathlib.Path = ROOT) -> Callable[[str, str], dict]:
    """Replay reviewed metadata, never contact the network during --check.

    This verifies committed-source/metadata/lock consistency, not authenticity
    against a live service. A coordinated malicious rewrite needs code review.
    """
    try:
        provenance = json.loads((root / "constraints/hash-provenance.json").read_text(encoding="utf-8"))
        if provenance.get("schema") != PROVENANCE_SCHEMA:
            raise LockError("unsupported provenance schema; regenerate with --write")
        if provenance.get("sources") != _source_hashes(root):
            raise LockError("pin/project source drift; regenerate from official PyPI with --write")
        releases = provenance["releases"]
        if not isinstance(releases, dict):
            raise LockError("provenance releases must be a mapping")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise LockError(f"cannot read committed hash provenance: {exc}") from exc

    def replay(name: str, version: str) -> dict:
        try:
            release = releases[f"{name}=={version}"]
            if release["metadata"] != f"{PYPI_BASE}/{name}/{version}/json":
                raise LockError(f"non-official metadata endpoint for {name}=={version}")
            return {"info": release["info"], "urls": [
                {"packagetype": "bdist_wheel", "yanked": False, "filename": filename,
                 "digests": {"sha256": item["sha256"]}, "url": item["url"],
                 "requires_python": item["requires_python"]}
                for filename, item in release["wheels"].items()
            ]}
        except (KeyError, TypeError, AttributeError) as exc:
            raise LockError(f"invalid/missing committed release {name}=={version}: {exc}") from exc

    return replay


def build_outputs(
    root: pathlib.Path = ROOT,
    fetcher: Callable[[str, str], dict] = _fetch_pypi,
) -> dict[pathlib.Path, str]:
    pin_sets = load_pin_sets(root)
    unique = sorted({(pin.name, pin.version) for pins in pin_sets.values() for pin in pins})
    payloads: dict[tuple[str, str], dict] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(fetcher, name, version): (name, version) for name, version in unique}
        for future in concurrent.futures.as_completed(futures):
            key = futures[future]
            try:
                payloads[key] = future.result()
            except Exception as exc:
                raise LockError(f"failed to retrieve official PyPI metadata for {key[0]}=={key[1]}: {exc}") from exc

    metadata: dict[tuple[str, str], dict] = {}
    wheels_by_release: dict[tuple[str, str], list[Wheel]] = {}
    for (name, version), payload in payloads.items():
        info, wheels = _metadata_wheels(name, version, payload)
        metadata[(name, version)] = info
        wheels_by_release[(name, version)] = wheels

    validate_project_roots(root, pin_sets["runtime"], include_dev=False)
    validate_project_roots(root, pin_sets["dev"], include_dev=True)
    validate_dependency_closure(pin_sets["runtime"], metadata, roots=_project_roots(root, False))
    validate_dependency_closure(pin_sets["dev"], metadata, roots=_project_roots(root, True),
                                project_extras=frozenset({"dev"}))
    validate_dependency_closure(pin_sets["quality"], metadata)

    selected: dict[tuple[str, str, str], list[Wheel]] = {}
    provenance_releases = {}
    for pins in pin_sets.values():
        for pin in pins:
            marker = str(pin.requirement.marker or "")
            key = (pin.name, pin.version, marker)
            if key not in selected:
                selected[key] = _selected_wheels(pin, wheels_by_release[(pin.name, pin.version)])
            release_key = f"{pin.name}=={pin.version}"
            release = provenance_releases.setdefault(
                release_key,
                {
                    "metadata": f"{PYPI_BASE}/{pin.name}/{pin.version}/json",
                    "info": {"name": pin.name, "version": pin.version,
                             "requires_dist": sorted(metadata[(pin.name, pin.version)].get("requires_dist") or [])},
                    "wheels": {},
                },
            )
            for wheel in selected[key]:
                release["wheels"][wheel.filename] = {
                    "sha256": wheel.sha256,
                    "url": wheel.url,
                    "requires_python": wheel.requires_python,
                }

    bootstrap_names = _bootstrap_closure(pin_sets["dev"], metadata)
    bootstrap_pins = [pin for pin in pin_sets["dev"] if pin.name in bootstrap_names]
    outputs = {
        root / "constraints" / "runtime-hashes.txt": render_lock(
            "runtime lock", pin_sets["runtime"], selected
        ),
        root / "constraints" / "dev-hashes.txt": render_lock(
            "development lock", pin_sets["dev-only"], selected
        ),
        root / "constraints" / "quality-hashes.txt": render_lock(
            "quality lock", pin_sets["quality"], selected
        ),
        root / "constraints" / "bootstrap-hashes.txt": render_lock(
            "bootstrap lock", bootstrap_pins, selected
        ),
    }
    provenance = {
        "schema": PROVENANCE_SCHEMA,
        "hash_algorithm": "sha256",
        "metadata_authority": "https://pypi.org",
        "file_authority": "https://files.pythonhosted.org",
        "source_distributions_allowed": False,
        "targets": [dataclasses.asdict(target) for target in TARGETS],
        "sources": _source_hashes(root),
        "locks": {path.name: hashlib.sha256(rendered.encode("utf-8")).hexdigest()
                  for path, rendered in outputs.items()},
        "releases": dict(sorted(provenance_releases.items())),
    }
    outputs[root / "constraints" / "hash-provenance.json"] = (
        json.dumps(provenance, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    )
    return outputs


def _sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="regenerate committed hash locks")
    mode.add_argument("--check", action="store_true", help="verify committed locks and source closure offline")
    mode.add_argument("--check-online", action="store_true", help="compare committed locks to current official PyPI metadata")
    args = parser.parse_args()
    try:
        outputs = build_outputs(fetcher=offline_fetcher() if args.check else _fetch_pypi)
    except (LockError, OSError, ValueError, TypeError, KeyError) as exc:
        print(f"HASH LOCK ERROR: {exc}", file=sys.stderr)
        return 2

    if args.check or args.check_online:
        drift = []
        for path, rendered in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != rendered:
                drift.append(path.relative_to(ROOT).as_posix())
        if drift:
            print("HASH LOCK DRIFT: " + ", ".join(drift), file=sys.stderr)
            print("Run: python tools/hash_constraints.py --write", file=sys.stderr)
            return 3
        print(f"hash locks OK: {len(outputs) - 1} locks, {len(TARGETS)} targets")
        return 0

    for path, rendered in outputs.items():
        path.write_text(rendered, encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(ROOT)} sha256={_sha256(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
