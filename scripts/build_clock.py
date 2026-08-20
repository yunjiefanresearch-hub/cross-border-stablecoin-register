"""One deterministic clock for generated release artifacts."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from datetime import date
import os

BUILD_DATE = os.environ.get("CBSR_BUILD_DATE", "2026-08-20")
try:
    date.fromisoformat(BUILD_DATE)
except ValueError as exc:
    raise SystemExit("CBSR_BUILD_DATE must be an ISO date (YYYY-MM-DD)") from exc
BUILD_TIMESTAMP = BUILD_DATE + "T00:00:00Z"
