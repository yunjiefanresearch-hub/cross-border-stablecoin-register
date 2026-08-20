#!/usr/bin/env python3
"""Check or refresh direct CBSR constraints against PyPI.

This script never edits pyproject.toml. It selects the newest stable release that
still satisfies the compatibility window already reviewed there. A changed pin is
only a proposal until the complete Linux matrix and Windows clean-room job pass.
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
import json
import pathlib
import re
import urllib.request

from packaging.requirements import Requirement
from packaging.version import InvalidVersion, Version

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
FILES = (ROOT / "constraints" / "runtime.txt", ROOT / "constraints" / "dev.txt")


def _requirements() -> dict[str, Requirement]:
    project = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]
    specs = list(project.get("dependencies", []))
    for group in (project.get("optional-dependencies") or {}).values():
        specs.extend(group)
    return {Requirement(spec).name.lower(): Requirement(spec) for spec in specs}


def _latest(name: str, requirement: Requirement) -> str:
    url = f"https://pypi.org/pypi/{name}/json"
    with urllib.request.urlopen(url, timeout=30) as response:
        releases = json.load(response)["releases"]
    candidates: list[Version] = []
    for raw, files in releases.items():
        try:
            version = Version(raw)
        except InvalidVersion:
            continue
        if version.is_prerelease:
            continue
        # A version-level JSON entry may remain visible after every file for
        # that version has been yanked. Never propose such a release.
        if not files or all(file_info.get("yanked", False) for file_info in files):
            continue
        if version in requirement.specifier:
            candidates.append(version)
    if not candidates:
        raise RuntimeError(f"no stable PyPI release satisfies {requirement}")
    return str(max(candidates))


def _pins(path: pathlib.Path) -> dict[str, tuple[str, int, list[str]]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    found = {}
    pattern = re.compile(r"^([A-Za-z0-9_.-]+)==([^;\s]+)(.*)$")
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            found[match.group(1).lower()] = (match.group(2), index, lines)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()

    supported = _requirements()
    changes: list[tuple[pathlib.Path, str, str, str]] = []
    for path in FILES:
        for name, (current, _index, _lines) in _pins(path).items():
            requirement = supported.get(name)
            if requirement is None:
                continue  # pip/setuptools/wheel are verifier bootstrap tools.
            latest = _latest(name, requirement)
            if latest != current:
                changes.append((path, name, current, latest))

    if not changes:
        print("constraints are current within the reviewed compatibility windows")
        return 0

    for path, name, current, latest in changes:
        print(f"{path.relative_to(ROOT)}: {name} {current} -> {latest}")
    if args.check:
        print("refresh available; run with --write, then require the full CI matrix")
        return 1

    by_file: dict[pathlib.Path, dict[str, str]] = {}
    for path, name, _current, latest in changes:
        by_file.setdefault(path, {})[name] = latest
    for path, replacements in by_file.items():
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            match = re.match(r"^([A-Za-z0-9_.-]+)==([^;\s]+)(.*)$", line)
            if match and match.group(1).lower() in replacements:
                lines[index] = f"{match.group(1)}=={replacements[match.group(1).lower()]}{match.group(3)}"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("constraints updated; this is an unverified proposal until the full matrix passes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
