"""
Cross-Border Stablecoin Register (CBSR) — MCP server package.

The register itself is the artefact; this package is only the typed query surface
over it. `server.py` reads the committed dataset.json that ships inside the wheel
and makes no network calls.
"""

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

__version__ = "0.10.1"  # MUST equal the register version in dataset.json — see tools/check_identifiers.py

__all__ = ["__version__"]
