#!/usr/bin/env python3
"""
Gate: every published identifier must point at the repository that actually publishes it.

Through v0.10.1 the three schema `$id`s, CITATION.cff, mcp.json and the generated landing
page all pointed at `stablecoin-rail-register` -- a slug the repository no longer used. The
README carried a paragraph explaining that the slug was "retained deliberately" because
"renaming the repo would break inbound references and the schema identifier". The repo had
already been renamed. So the schema identifiers of a register whose entire value proposition
is verifiable provenance were themselves stale, and the note defending them was defending a
decision that had been reversed.

Nothing caught it, because nothing was looking. This looks.

Checked here:
  1. no LIVE artefact carries the retired slug (CHANGELOG.md and BUILD_NOTE_*.md are exempt:
     they are dated records of what was true when written, and must not be rewritten)
  2. all three schema $ids share the one canonical base URL
  3. the package version, the dataset version and mcp.json agree

    python tools/check_identifiers.py
"""
from __future__ import annotations

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

CANONICAL_SLUG = "cross-border-stablecoin-register"
RETIRED_SLUGS = ("stablecoin-rail-register",)
PAGES_BASE = f"https://yunjiefanresearch-hub.github.io/{CANONICAL_SLUG}"

# History is evidence. It is never rewritten to match the present.
HISTORICAL = {"CHANGELOG.md"}
HISTORICAL_GLOBS = ("BUILD_NOTE_*.md", "UPGRADE_*.md")

SKIP_DIRS = {".git", "dist", "build", "__pycache__", ".venv", "node_modules", "papers", "pdf"}
TEXT_SUFFIXES = {".json", ".md", ".py", ".cff", ".html", ".yaml", ".yml", ".toml"}


def _is_historical(path: pathlib.Path) -> bool:
    if path.name in HISTORICAL:
        return True
    return any(path.match(g) for g in HISTORICAL_GLOBS)


def check_no_retired_slug() -> list[str]:
    problems: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if _is_historical(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for slug in RETIRED_SLUGS:
            # Only URLs matter. Prose that *narrates* the rename is legitimate.
            for m in re.finditer(rf"https?://[^\s\"'<>)]*{re.escape(slug)}[^\s\"'<>)]*", text):
                line = text[: m.start()].count("\n") + 1
                problems.append(
                    f"{path.relative_to(ROOT)}:{line} live URL still uses the retired slug "
                    f"'{slug}' -> {m.group(0)}"
                )
    return problems


def check_schema_ids() -> list[str]:
    problems: list[str] = []
    schemas = sorted(ROOT.glob("*.schema.json")) + sorted((ROOT / "tools").glob("*.schema.json"))
    if not schemas:
        return ["no *.schema.json found"]
    for path in schemas:
        data = json.loads(path.read_text(encoding="utf-8"))
        sid = data.get("$id")
        if not sid:
            problems.append(f"{path.relative_to(ROOT)} has no $id")
            continue
        rel = path.relative_to(ROOT).as_posix()
        expected = f"{PAGES_BASE}/{rel}"
        if sid != expected:
            problems.append(
                f"{path.relative_to(ROOT)} $id is not canonical\n"
                f"      found:    {sid}\n"
                f"      expected: {expected}"
            )
    return problems


def check_versions() -> list[str]:
    problems: list[str] = []
    dataset_v = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8")).get("version")
    manifest_v = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8")).get("version")

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M)
    package_v = m.group(1) if m else None

    init = (ROOT / "src" / "cbsr_mcp" / "__init__.py").read_text(encoding="utf-8")
    m = re.search(r'__version__\s*=\s*"([^"]+)"', init)
    init_v = m.group(1) if m else None

    # The wheel bundles dataset.json, so the package version IS the register version.
    # PEP 440 post-releases (0.10.1.post1) are allowed: they let a server-only fix ship
    # without falsely implying the DATA changed. The base version must still match.
    def base(v: str | None) -> str | None:
        if v is None:
            return None
        return re.split(r"\.(?:post|dev|rc|a|b)\d*", v, maxsplit=1)[0]

    versions = {
        "dataset.json": dataset_v,
        "mcp.json": manifest_v,
        "pyproject.toml": package_v,
        "src/cbsr_mcp/__init__.py": init_v,
    }
    distinct = {base(v) for v in versions.values()}
    if len(distinct) != 1 or None in distinct:
        problems.append(
            "version drift -- the packaged server ships the dataset, so their versions cannot differ:\n"
            + "\n".join(f"      {k:<28} {v}" for k, v in versions.items())
        )
    return problems


def main() -> int:
    checks = (
        ("no retired slug in any live URL", check_no_retired_slug),
        ("schema $ids are canonical", check_schema_ids),
        ("package/dataset versions agree", check_versions),
    )

    failed = 0
    for name, fn in checks:
        problems = fn()
        if problems:
            failed += 1
            print(f"FAIL  {name}")
            for p in problems:
                print(f"    - {p}")
        else:
            print(f"OK    {name}")

    if failed:
        print(f"\n{failed} identifier check(s) failed.")
        return 1
    print("\nAll identifier checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
