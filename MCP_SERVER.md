# MCP server

`mcp_server.py` exposes the register as **typed query tools** over the [Model Context
Protocol](https://modelcontextprotocol.io), so an agent can query the cross-jurisdictional
differential layer directly instead of fetching and parsing `dataset.json`. The server reads the
committed `dataset.json` and makes **no network calls**; it only filters and reshapes published
records (no data is synthesised at query time).

## Install

```bash
uvx cbsr-mcp
```

That is the whole thing. The dataset ships inside the wheel, so there is nothing to clone, no path
to configure, and no network call at run time — the server reads the same `dataset.json` that carries
the DOI.

## Register with an MCP client

`claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`):

```json
{
  "mcpServers": {
    "cbsr": {
      "command": "uvx",
      "args": ["cbsr-mcp"]
    }
  }
}
```

Restart the client. The 33 tools below appear.

## Run from a source checkout

If you are working on the register itself rather than consuming it, the original zero-install path
still works verbatim — no packaging step, no `PYTHONPATH`:

```bash
pip install "mcp[cli]"
python mcp_server.py          # stdio transport — what MCP clients speak
mcp dev mcp_server.py         # interactive, via the MCP Inspector
```

`mcp_server.py` is a launcher; the server itself is `src/cbsr_mcp/server.py`. Both paths execute the
same code and read the same dataset: installed, it resolves the copy bundled in the wheel; from a
checkout, the `dataset.json` that `build.py` compiles. A pinned version of the tools always answers
from the pinned version of the register — that is the point.

## Tools

| Tool | Purpose |
|---|---|
| `about()` | Register metadata: version, record count, DOI, license, verification rule |
| `list_jurisdictions()` | Jurisdictions covered + record counts |
| `list_dimensions()` | The 15 dimensions, descriptions, spine flag, record counts |
| `get_record(record_id)` | Full record (all fields incl. `requirement_structured`, `interpretation_note`) |
| `query(jurisdiction?, dimension?, status?, confidence?, constraint_ref?)` | Typed filter, AND-combined; returns provenance-bearing summaries |
| `compare_dimension(dimension)` | All jurisdictions on one dimension — the core differential view |
| `jurisdiction_profile(jurisdiction)` | All records for one jurisdiction, ordered by the framework |
| `search(keyword)` | Keyword search across summary, source, authority, tags |
| `get_corridor(corridor_id?)` | Corridor model(s): what clears / breaks at each boundary |
| `coverage()` | Jurisdiction × dimension grid: where data exists vs. is planned |
| `citable_law(jurisdiction?, dimension?)` | **Lawyer-citable subset.** Only records that are a proposition of law (`claim_class=tier1_legal`), in force (`status=in_force`), AND confirmed against the official text (`evidence_tier=resolution_text`); each row returns the binding instrument, pinpoint, and official URL. Optional jurisdiction/dimension filters. The "show me only what I could cite" view |
| `compatibility(jurisdiction?, other?, category?)` | **Analysis layer.** The §5.14 pairwise compatibility matrix (66 pairs); filter by jurisdiction, a specific pair, or category (I / I/II / II / III) |
| `interaction_sets()` | **Analysis layer.** The six constraint-interaction sets (§2.9, A–F): constraint pair, mechanism, worked example |
| `architectural_patterns()` | **Analysis layer.** The PRC three-pattern typology (§3.3), the three-layer routing architecture (§4/§6), the §4.4 five-factor test, the six design principles |
| `open_questions()` | **Analysis layer.** The four open regulatory questions (§7) with conditional-status flags |
| `compose_corridor(origin, destination, as_of?)` | **Computed layer.** COMPUTES a directed corridor's feasibility from the signal table + Atlas algorithm (not a lookup); returns class, rule fired, interaction sets, and the computed-vs-authored comparison. Pass `as_of` (ISO date) to evaluate as of that date — every scheduled change in law effective by then is applied first (returns the as-of class, the base class, and whether it changed) |
| `explain_feasibility(origin, destination)` | **Computed layer.** Explains WHY a corridor falls in its class: rule fired, each side's justifying node-record basis, and computed-vs-authored agreement |
| `corridor_timeline(origin, destination)` | **Time engine.** The dated future of a directed edge: today's class, the scheduled transitions that change it (with effective dates), and contingent "if enacted" branches. Answers "Category T today, Category I after the regime is operative" |
| `event_calendar(jurisdiction?)` | **Time engine.** The dated/contingent `tier1_legal` changes in law that move a jurisdiction's compose() signal (scheduled / contingent / in_force), with event provenance. A market launch is never an event |
| `constraint_substrate(jurisdiction?, constraint?)` | **Constraint substrate.** Each `(jurisdiction × constraint C1–C8)` as a structured pole citing the `tier1_legal` record it is transcribed from, plus coverage. Poles exist only where a record backs them |
| `compose_via_substrate(origin, destination)` | **Constraint substrate.** DERIVES a corridor's class by composing two jurisdictions' C1–C8 poles through the interaction-set rules (not the inbound-gate shortcut); returns per-set verdicts and the cross-check vs the signal compose(), or `indeterminate` with the missing poles |
| `verification_report()` | **Verification queue.** Records bucketed by `evidence_tier`, the largest backlog (legacy `unset`), and records lacking a `source.url` |
| `verification_worklist(jurisdiction?)` | **Verification harness.** Per-cell gap analysis for the primary-source pass: for each unverified cell, the instrument + pinpoint and exactly what is missing to reach each tier. `evidence_tier` is enforced by the build (earned, not asserted). Verification is external work, never fabricated — this scopes it |
| `verification_ledger(jurisdiction?)` | **Verification audit trail.** Per cell, the cited instrument's binding status, whether an official URL is attached, and the tier the pass applied — citability is capped by binding status, not by whether the text was located |
| `events_by_kind(kind?)` | **Trigger typology (§3).** The event calendar grouped by `trigger_kind` — by the *kind of certainty* a trigger carries, not by date. Separates the one kind that moves a dated horizon (fully-scheduled) from dated-but-inert changes (intra-regime-gating, dated-empty-effect) and undated contingent branches; carries the legend + horizon rule |
| `convergence(side?)` | **Yield-line convergence (§4.5).** The cross-jurisdiction view of the holder-yield-prohibited / activity-rewards-permitted boundary, reshaped from the per-jurisdiction `permitted_activity_yield` records (asserts no new facts). Tiers jurisdictions by role — citable two-sided `anchor` (US), `sibling`, `counter_example` (CH), `holder_prohibition_in_force`, `draft_would_align`, backlog — under the register's citable-purity discipline |
| `reconciliation(only_divergences?)` | **Computed-vs-authored audit.** For every undirected pair, the class the engine derives vs the class a human authored, with agree/disagree and, where they differ, the named cause (`findings_by_cause`). A divergence is a finding (a regime-in-transition side), not a defect |
| `records(claim_class?, evidence_tier?, status?, binding_status?, jurisdiction?, dimension?, citable_only?)` | **Evidence-axis browser.** Filter along the axes that decide citability and get, per record, whether it is lawyer-citable and — if not — exactly which axis blocks it (the "why not citable" x-ray). The complement to `query()` |
| `stakeholder_database()` | **The Atlas §8 actor catalogue.** Each persona (issuer, distributor, regulator, treasury, holder, …) with its lens, the C1–C8 constraints that bear on it, and the corridor archetypes (RC/SC/TC/DC) it engages. Pair with `profile_for()` |
| `profile_for(stakeholder, origin, destination)` | **Project a directed corridor onto a persona.** The persona's lens, the corridor's derived class, a per-constraint reading of the origin/destination poles that persona cares about (each citing its backing record), engaged archetypes and inbound mechanism. Introduces no new facts — every line is read from an existing record, so the profile is bounded by the verification status of the cells it reads |
| `corridor_skeleton(origin, destination)` | **The record for any directed edge.** The hand-authored RICH corridor if one exists, otherwise the COMPUTED SKELETON (derived class, inbound mechanism test + administrator, baseline archetypes, directed interaction sets, provenance). Skeletons assert nothing new: empirical fields are left explicitly unset rather than guessed |
| `edge_coverage()` | **How much of the edge layer actually carries a record.** Separates the hand-authored RICH corridors from the COMPUTED SKELETONS and the still-indeterminate edges — the honest denominator behind "132 directed corridors" |
| `forward_view(jurisdiction?)` | **The supervisor's forward view (Atlas §4.4).** The trigger register re-sorted *by jurisdiction* rather than by trigger: which pending developments will reclassify the corridors into and out of this jurisdiction, own-trigger vs counterpart-driven, and ranked counterpart exposure. Asserts no new facts |

**A suite of typed tools.** Every returned record summary carries `source.primary`, `pinpoint`, `claim_class`,
`evidence_tier`, `confidence`, dates and `version_added` — the two evidence axes (`claim_class` = kind
of claim; `evidence_tier` = provenance strength) let an agent separate *binding law* from
*well-sourced market fact*. The lawyer-citable subset (`tier1_legal` + `in_force` + `resolution_text`)
is available via `citable_law()` and as `citable_subset` in `dataset.json`. Per the methodology, some
records are transcribed from the maintainer's Compliance Matrix and are pending final primary-source
verification (`source.url` empty); treat `confidence` and `interpretation_note` accordingly.
