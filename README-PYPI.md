# CBSR — Cross-Border Stablecoin Register (MCP server)

mcp-name: io.github.yunjiefanresearch-hub/cbsr

Typed MCP tools over an open, versioned register of how twelve jurisdictions regulate
stablecoins — clause by clause, across fifteen dimensions, with a directed corridor layer
and a computed feasibility engine.

    python -m pip install --constraint constraints/runtime.txt .

Claude Desktop / any MCP client:

```json
{ "mcpServers": { "cbsr": { "command": "C:/path/.venv/Scripts/python.exe", "args": ["C:/path/mcp_server.py"] } } }
```

**Jurisdictions** — US · EU · UK · HK · SG · CN · JP · KR · TW · CH · AE · BR

**What it is.** 152 records, each carrying its own source URL, pinpoint citation, claim class,
evidence tier and binding status. A corridor is *directed*: the same border can be permissive
one way and restricted the other, so all 132 directed corridors across the twelve jurisdictions
are modelled separately.

**What it will not do.** The server reads the committed `dataset.json` that ships inside this
wheel. It makes no network calls, and it synthesises nothing — every tool filters and reshapes
published records. `citable_law()` returns only the subset that is a proposition of law
(`tier1_legal`), in force, confirmed against official resolution text, with an official source,
current evidence at the snapshot date, and independently reconciled review. At the
2026-08-20 snapshot there are 152 records, 46 structural candidates, and **0 decision-ready
citable records**. `records()` exposes the axes blocking each record. The snapshot date is
not a claim of real-time legal currentness.

**Data:** CC-BY-4.0 · **Code:** Apache-2.0
**Repository:** https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register
