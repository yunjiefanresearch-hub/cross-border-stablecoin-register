#!/usr/bin/env python3
"""Thin MCP composition root for the Cross-Border Stablecoin Register.

Tool logic lives behind explicit core/data/domain/tools/serialization/api boundaries.
This module only creates FastMCP, imports the tool packs and binds the central registry.
"""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "The 'mcp' package is required. Install the reviewed graph before starting CBSR."
    ) from exc

# Import order is explicit only for deterministic manifest ordering. Registration metadata
# itself is owned by tools.registry, never by a hard-coded count in this file.
from .tools import architecture as _architecture  # noqa: F401,E402
from .tools import register as _register  # noqa: F401,E402
from .tools import research as _research  # noqa: F401,E402
from .tools import agentic as _agentic  # noqa: F401,E402
from .core.catalog import DIMENSIONS  # noqa: E402
from .data.repository import CORRIDORS, DATA, RECORDS  # noqa: E402
from .tools.registry import bind, metadata  # noqa: E402

# Public compatibility aliases retained from the pre-v0.11 composition root.
# The repository module remains the single owner; these names do not copy data.

mcp = FastMCP("cross-border-stablecoin-register")
bind(mcp)


def tool_metadata() -> list[dict[str, str]]:
    """Return registry-derived tool metadata for diagnostics and manifest generation."""
    return metadata()


def main() -> None:
    """Run the stdio MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
