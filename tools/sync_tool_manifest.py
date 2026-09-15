#!/usr/bin/env python3
"""Regenerate mcp.json tool metadata from the runtime registry."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from cbsr_mcp.tools import architecture, register, research, agentic  # noqa: E402,F401
from cbsr_mcp.tools.registry import metadata  # noqa: E402


def main() -> int:
    path = ROOT / "mcp.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["tools"] = metadata()
    document["runtime"]["requires"] = "mcp>=1.29,<1.30"
    document["provenance"]["tool_metadata_source"] = "src/cbsr_mcp/tools/registry.py"
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote mcp.json from registry ({len(document['tools'])} tools)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
