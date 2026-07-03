# Connect the register to Claude (or any MCP client)

This register ships two ways to consume it programmatically:

1. a **queryable MCP server** (`mcp_server.py`) that exposes the register as typed tools, and
2. a **zero-setup static JSON API** under [`/api/`](../api/index.json) if you just want to fetch and filter.

Both read the same compiled `dataset.json` and assert no new facts. The manifest at
[`mcp.json`](../mcp.json) is a copy-pasteable descriptor of the server (its command, its tools, and the
guardrails it operates under); its tool list is generated from `mcp_server.py`, so it never drifts from
the code.

If you only want the data and not a live tool surface, skip to [Zero-setup: the static API](#zero-setup-the-static-api).

---

## What you get

The server turns "a repository" into "a queryable data service." Instead of cloning the repo and parsing
YAML, an agent can ask the register directly — and every answer carries the same provenance a human sees
(`source.primary`, `pinpoint`, `claim_class`, `evidence_tier`, `confidence`, `version_added`). The full
tool list is in [`MCP_SERVER.md`](../MCP_SERVER.md); a few worth knowing on day one:

- `citable_law(jurisdiction?, dimension?)` — the lawyer-citable subset: only `tier1_legal` + `in_force` +
  `resolution_text` cells, each with an official URL and pinpoint.
- `records(claim_class?, evidence_tier?, status?, binding_status?, jurisdiction?, dimension?, citable_only?)`
  — the evidence-axis browser: for every record, whether it is citable and, if not, exactly which axis
  blocks it (the "why not citable" x-ray).
- `compose_corridor(origin, destination, as_of?)` — computes a directed corridor's feasibility class from
  the signal table and the Atlas algorithm; pass `as_of` to apply every scheduled change in law effective
  by that date first.
- `corridor_timeline(origin, destination)` — today's class, the scheduled transitions that change it, and
  any contingent "if enacted" branches (never folded into the dated line).
- `events_by_kind(kind?)` — the event calendar grouped by `trigger_kind`: which changes actually move a
  dated horizon (fully-scheduled) versus which are dated-but-inert or undated-contingent.
- `convergence(side?)` — the cross-jurisdiction yield-line view (holder-yield-prohibited /
  activity-rewards-permitted), tiered by role under the register's citable-purity discipline.
- `reconciliation(only_divergences?)` — the class the engine computes vs the class a human authored, with
  the named cause of any divergence.

### Guardrails the server operates under

- **Offline.** It reads the committed `dataset.json`; it never touches the network.
- **No synthesis.** Tools filter and reshape published records; no facts are generated.
- **Conditioning, not forecasting.** The date-aware and what-if tools apply only the register's own
  scheduled / contingent changes in law — no probabilities, no predictions.
- **Citable by construction.** The citable views return only human-verified, in-force propositions of law
  with an official source and pinpoint.

---

## Prerequisites

- Python 3.10+ available to whatever will launch the server.
- The `mcp` package on that interpreter:

  ```bash
  pip install "mcp[cli]"
  ```

  If you use a virtual environment, install it there and point the client at that environment's
  interpreter (below).

Clone or download the register so `mcp_server.py` and `dataset.json` sit together:

```bash
git clone https://github.com/yunjiefanresearch-hub/stablecoin-rail-register.git
cd stablecoin-rail-register
```

---

## Connect to Claude Desktop

The quickest path is to let the MCP CLI write the config for you:

```bash
mcp install mcp_server.py --name "Cross-Border Stablecoin Register"
```

Or add it manually to `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`):

```json
{
  "mcpServers": {
    "cross-border-stablecoin-register": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/stablecoin-rail-register/mcp_server.py"]
    }
  }
}
```

Use an **absolute path** to `mcp_server.py`. If you installed `mcp` into a venv, set `"command"` to that
venv's Python (e.g. `/path/.venv/bin/python`). Restart Claude Desktop after editing the config, then look
for the register under the tools/🔌 menu.

## Connect to Claude Code (and other project-config clients)

Clients that read a project-level `.mcp.json` can use the `mcpServers` block from
[`mcp.json`](../mcp.json). From the repo root:

```bash
claude mcp add cross-border-stablecoin-register -- python "$(pwd)/mcp_server.py"
```

or copy the `mcpServers` stanza into your client's config, replacing `mcp_server.py` with its absolute
path. The rest of `mcp.json` (description, tool inventory, guardrails) is metadata a client can surface but
does not need to run the server.

## Test it without a client

The MCP Inspector runs the server and lets you call tools by hand:

```bash
mcp dev mcp_server.py
```

Then try, for example, `citable_law` with `jurisdiction = "CH"`, or `events_by_kind` with no argument to
see which scheduled event actually moves a corridor.

---

## Zero-setup: the static API

If you don't want to run a server at all, the same views are published as plain JSON under
[`/api/`](../api/index.json) — no backend, no database, servable straight from GitHub Pages. Start at the
manifest and follow the endpoints:

```bash
curl -s https://<your-pages-host>/api/index.json          # manifest of all endpoints
curl -s https://<your-pages-host>/api/citable.json         # the 46-cell lawyer-citable subset
curl -s https://<your-pages-host>/api/events/by_kind.json  # events grouped by trigger_kind
curl -s https://<your-pages-host>/api/corridors/US-UK.json # one corridor: timeline + what-if
```

Every file carries a provenance envelope (register, version, generated timestamp, endpoint, and the
guardrail it honours). The API adds no facts the MCP server or `dataset.json` doesn't already carry — it is
purely a projection for callers who prefer static fetches to a live tool surface.

---

## Troubleshooting

- **The client shows no tools / the server won't start.** Confirm `pip install "mcp[cli]"` ran against the
  *same* interpreter the client launches, and that the path in the config is absolute. Restart the client
  after any config change.
- **`dataset.json not found`.** The server reads `dataset.json` from its own directory. Keep
  `mcp_server.py` next to `dataset.json` (as in the repo), or run `python build.py` first to (re)compile it.
- **A computed/convergence tool returns `not present`.** Those views come from the `analysis/` layer folded
  into `dataset.json` by the build. Run `python build.py` to refresh the dataset, then restart the server.
