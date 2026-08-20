#!/usr/bin/env python3
"""Validate repository-relative Markdown links without requiring network access."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import pathlib
import re
from urllib.parse import unquote, urlsplit

ROOT = pathlib.Path(__file__).resolve().parent.parent
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKIP_DIRS = {".git", ".venv", "dist", "build", "site", "__pycache__", ".pytest_cache"}


def _target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1:value.index(">")]
    return value.split(maxsplit=1)[0]


def main() -> int:
    failures: list[str] = []
    checked = 0
    for document in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in document.relative_to(ROOT).parts):
            continue
        text = document.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            raw = _target(match.group(1))
            if not raw or raw.startswith(("#", "mailto:", "data:", "javascript:")):
                continue
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc:
                continue
            decoded = unquote(parsed.path)
            if not decoded or any(token in decoded for token in ("{", "}", "*")):
                continue
            candidate = (ROOT / decoded.lstrip("/")) if decoded.startswith("/") else (document.parent / decoded)
            checked += 1
            if not candidate.resolve().exists():
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{document.relative_to(ROOT)}:{line}: {raw}")
    if failures:
        raise SystemExit("broken internal Markdown links:\n  - " + "\n  - ".join(failures))
    print(f"internal Markdown links valid: {checked} local targets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
