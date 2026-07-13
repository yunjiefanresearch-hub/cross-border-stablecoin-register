#!/usr/bin/env python3
"""
Cross-Border Stablecoin Register — MCP server (launcher).

The server now lives in `src/cbsr_mcp/server.py` so it can be installed as a
package and wired into an MCP client in one line, with nothing to clone:

    {"mcpServers": {"cbsr": {"command": "uvx", "args": ["cbsr-mcp"]}}}

This launcher is kept so the original zero-install path still works verbatim from
a plain source checkout — no packaging step, no PYTHONPATH:

    pip install "mcp[cli]"
    python mcp_server.py

Both paths execute the same code and read the same dataset.json.
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

import pathlib
import sys

_SRC = pathlib.Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from cbsr_mcp.server import main  # noqa: E402

if __name__ == "__main__":
    main()
