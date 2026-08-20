#!/usr/bin/env python3
"""Validate PDF metadata, text contract and minimum institutional layout."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import pathlib

from pypdf import PdfReader

from tools.whitepaper import TITLE

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.pdf"


def main() -> int:
    if not PDF.is_file() or PDF.stat().st_size < 40_000:
        raise SystemExit("whitepaper PDF missing or unexpectedly small")
    reader = PdfReader(str(PDF))
    if len(reader.pages) < 24:
        raise SystemExit(f"whitepaper PDF unexpectedly short: {len(reader.pages)} pages")
    if str((reader.metadata or {}).get("/Title") or "") != TITLE:
        raise SystemExit("whitepaper PDF title metadata mismatch")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    required = [
        "1. Executive summary", "12. Know-your-agent considerations",
        "21. Pilot cases", "27. Primary-source bibliography", "28. Reproducibility appendix",
        "enterprise US-to-EU stablecoin payment", "tokenized green-asset",
        "not legal advice", "external peer review and independent legal review not completed",
    ]
    missing = [token for token in required if token.lower() not in text.lower()]
    if missing:
        raise SystemExit("whitepaper PDF text contract missing: " + ", ".join(missing))
    print(f"whitepaper PDF valid: {len(reader.pages)} pages, metadata and 28-section text contract present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
