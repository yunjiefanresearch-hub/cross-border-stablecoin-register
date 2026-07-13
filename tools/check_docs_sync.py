#!/usr/bin/env python3
"""
Gate: the MCP tool surface must be identical in all three places that publish it.

Three artefacts each claim to describe the same set of tools:

    src/cbsr_mcp/server.py   the @mcp.tool() functions actually registered  -- the truth
    mcp.json                 the hand-maintained client manifest
    MCP_SERVER.md            the hand-written table a reader/registry sees

Through v0.10.1 they disagreed: the server registered 33 tools, MCP_SERVER.md documented
28. Five tools (stakeholder_database, profile_for, edge_coverage, corridor_skeleton,
forward_view) existed and worked, and no reader could discover them. That drift was silent
because nothing checked it. This checks it.

The register's own discipline is that a claim must be checkable against its source. The
documentation of the register is a claim about the register. It gets the same treatment.

    python tools/check_docs_sync.py
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

import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

SERVER = ROOT / "src" / "cbsr_mcp" / "server.py"
MANIFEST = ROOT / "mcp.json"
DOC = ROOT / "MCP_SERVER.md"


def tools_registered_in_server() -> set[str]:
    """The tools the server actually exposes: every function under an @mcp.tool() decorator."""
    tree = ast.parse(SERVER.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            target = dec.func if isinstance(dec, ast.Call) else dec
            if isinstance(target, ast.Attribute) and target.attr == "tool":
                found.add(node.name)
    return found


def tools_in_manifest() -> set[str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {t["name"] for t in data.get("tools", [])}


def tools_in_doc() -> set[str]:
    """Every table row of the form:  | `tool_name(...)` | ... |"""
    rows = re.findall(r"^\| `([a-z_][a-z0-9_]*)\(", DOC.read_text(encoding="utf-8"), re.M)
    return set(rows)


def main() -> int:
    server = tools_registered_in_server()
    manifest = tools_in_manifest()
    doc = tools_in_doc()

    if not server:
        print("FAIL  no @mcp.tool() functions found in", SERVER)
        return 1

    failures: list[str] = []

    for label, claimed in (("mcp.json", manifest), ("MCP_SERVER.md", doc)):
        undocumented = server - claimed
        phantom = claimed - server
        if undocumented:
            failures.append(
                f"{label} is missing {len(undocumented)} tool(s) the server registers: "
                + ", ".join(sorted(undocumented))
            )
        if phantom:
            failures.append(
                f"{label} documents {len(phantom)} tool(s) the server does NOT register: "
                + ", ".join(sorted(phantom))
            )

    if failures:
        print("FAIL  MCP tool surface has drifted.\n")
        for f in failures:
            print("  -", f)
        print(
            "\n  The server is the source of truth. Update mcp.json / MCP_SERVER.md to match it —\n"
            "  a tool nobody can discover is a tool that does not exist."
        )
        return 1

    print(f"OK    MCP tool surface consistent across all three sources ({len(server)} tools)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
