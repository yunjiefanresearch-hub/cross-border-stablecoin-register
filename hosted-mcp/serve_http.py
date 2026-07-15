#!/usr/bin/env python3
"""
CBSR hosted MCP: the INSTRUMENT (runbook §3).

Runs the SAME FastMCP app as the published wheel, but over HTTP, on a server YOU
control: so every tools/call is in your logs (honestly: it's a network service).
The local `uvx cbsr-mcp` (stdio) stays untouched, pure, and offline.

Serve the CURRENT dataset: install the register from a source checkout whose
dataset.json you keep fresh (see Dockerfile), rather than the frozen PyPI wheel.

Two version-dependent spots are marked [VERIFY]: confirm against your installed
`mcp` version. Everything else is final.
"""
from __future__ import annotations
import os, sys

from cbsr_mcp.server import mcp   # reuse the exact FastMCP instance + all tools

# corridor-demand telemetry (best-effort; no-ops cleanly if internals differ)
try:
    import cbsr_obs
    cbsr_obs.instrument(mcp)
except Exception as e:
    print(f"[serve_http] obs disabled: {e}", file=sys.stderr)

HOST = os.environ.get("CBSR_HTTP_HOST", "0.0.0.0")
PORT = int(os.environ.get("CBSR_HTTP_PORT", "8000"))

# FastMCP reads host/port from settings and/or FASTMCP_* env vars depending on version.
os.environ.setdefault("FASTMCP_HOST", HOST)
os.environ.setdefault("FASTMCP_PORT", str(PORT))
for attr, val in (("host", HOST), ("port", PORT)):
    try:
        setattr(mcp.settings, attr, val)   # [VERIFY] attribute exists in recent FastMCP
    except Exception:
        pass

def run() -> None:
    # [VERIFY] Streamable HTTP is the current remote transport; older mcp used "sse".
    last_err = None
    for transport in ("streamable-http", "sse"):
        try:
            print(f"[serve_http] starting on {HOST}:{PORT} via {transport}", file=sys.stderr)
            mcp.run(transport=transport)
            return
        except Exception as e:
            last_err = e
            print(f"[serve_http] transport '{transport}' failed: {e}", file=sys.stderr)
    raise SystemExit(f"No supported HTTP transport for this mcp version: {last_err}")

if __name__ == "__main__":
    run()
