# CBSR: regression report (2026-07-15)

Method: `mcp` is not installable here (network disabled), so FastMCP's *shell* was stubbed
and the **real `cbsr_mcp/server.py` was imported** against the **real `dataset.json`**.
Everything below is measured, not assumed. Where I could not measure, it says so.

---

## P0: the MCP layer contradicts the site on the flagship claim

`compose_corridor` returns **II** for all 8 inbound-US corridors. The site, the og-card, and
`computed_corridors_directed` all say **T (Regime-in-transition)**.

    EU->US | directed='Regime-in-transition→II' | MCP compose='II' | timeline.today='II' sched=0
    UK->US | directed='Regime-in-transition→II' | MCP compose='II' | timeline.today='II' sched=1
    SG->US | HK->US | BR->US | CH->US | AE->US | JP->US   ... all identical

`compose_corridor(EU,US, as_of="2027-02-01")` also returns **II**: unchanged from base.

### Root cause (two defects, both in source, not in the build artifact)

**1. `analysis/computed_compatibility.json` + `analysis/computed_corridor_states.json`**

    "US": { "regime_status": "live", "inbound_gate": "comparability" }

`_compose_directed` reads this and yields II directly. But `analysis/signal_table.json` says:

    binding_status : made_not_commenced
    date_kind      : outer_cap
    note           : "the s.18 gate is NOT 'available but unused', it is NOT YET AVAILABLE.
                      Coding it as an in-force Category II gate let a market observation
                      ('none granted to date') do a proposition of law's work."

The signal_table records the correction. The signals the compose engine reads never received it.

**2. `analysis/event_calendar.json` has no `us-genius-act-effective` event.**

    US events: 1
      us-clarity-act-enacted | status: contingent | eff: None | has effect: True
    us-genius-act-effective present: False

`corridor_timeline` filters on `status in (scheduled,in_force)` AND `effective_date` AND
`effect`. With no such US event, it reports `scheduled_transitions: []`,
`next_scheduled_change: null`: even though `computed_forward_view.jurisdictions.US
.own_pending_events[0]` = `us-genius-act-effective`, effective 2027-01-18, `moves_class: true`.

### The UK is the working template

| | UK (correct) | US (defective) |
|---|---|---|
| signals | `regime_status: "transition"`, `inbound_gate: "transition"` | `"live"`, `"comparability"` |
| event | `uk-systemic-regime-operative`, scheduled, 2027-10-25, effect present | **absent** |
| result | T today → I on 2027-10-25 ✓ | II today, never moves ✗ |

### Impact
- `uvx cbsr-mcp` → agents receive the classification the register itself calls the error.
- The pitch's core claim ("a corridor reads one way today and another once a pending regime
  commences") is **false at the MCP layer for exactly the 8 corridors you lead with**.
- Site says T, MCP says II, on the flagship corridor.

### Proposed fix: NOT APPLIED (author's call)

    // computed_compatibility.json + computed_corridor_states.json
    "US": { "regime_status": "transition", "inbound_gate": "transition", ... }

    // event_calendar.json  events[] +=
    { "id": "us-genius-act-effective", "jurisdiction": "US", "status": "scheduled",
      "effective_date": "2027-01-18", "precision": "outer_cap",
      "title": "US GENIUS Act §18 comparability gate commences (outer cap <=2027-01-18)",
      "effect": [ {"field":"regime_status","from":"transition","to":"live"},
                  {"field":"inbound_gate","from":"transition","to":"comparability"} ] }

Then re-run `build.py` and the CI invariants.

Not applied because: it is a proposition about law (is the US regime "transition" or "live"?),
not a typo; it changes the computed layer I undertook not to touch; and it needs a rebuild plus
`run_invariants.py` / reconciliation to pass, with possible cascade into
`computed_corridors_directed`, `forward_view`, and `signal_table`.

**Consequence for the memo template:** "Class today" must NOT come from `compose_corridor`
until this is fixed: it returns the preview class. Use `computed_corridors_directed`.

---

## 1. Does it all run?

| Item | Result |
|---|---|
| `tools/make_og_card.py` | ✅ ran, correct card, both repos |
| `metrics/pull_public_stats.py` | ✅ runs; network off → `ok:false` + exit 0, no crash |
| `.github/workflows/metrics-snapshot.yml` | ✅ valid YAML; 4 steps; `permissions: contents: write` |
| landing + mapper `index.html` | ✅ parse OK; inline JS passes `node --check` |
| `cbsr_obs.py` | ✅ wrapped 7/7 tools; telemetry fired on a real call |
| `hosted-mcp/serve_http.py` | ⚠️ **not runnable here**: `mcp` absent, network off |
| Dockerfile assumption | ✅ `pyproject` `force-include` maps `dataset.json` → `cbsr_mcp/data/` |

## 2. Are the settings accurate?

| Setting | Verified |
|---|---|
| PyPI package `cbsr-mcp` | ✅ matches `pyproject.name` → pypistats URL correct |
| Zenodo `20730358` | ✅ matches `CITATION.cff` DOI |
| Version `0.10.1` | ✅ `__init__.py` == `dataset.json` |
| `as_of_base` = 2026-06-30 | ⚠️ ~2 weeks stale (content, from your pipeline) |

## 3. Can the MCP be tracked?

**Yes: via the hosted HTTP path only. Confirmed by measurement:**

    PASS  imported real cbsr_mcp.server
    PASS  33 tools registered
    PASS  instrument() wrapped 7 tool(s)
    PASS  compose_corridor(EU,US) executed against the real dataset
    PASS  telemetry: {"t":1784085271.97,"tool":"compose_corridor",
                      "args":{"origin":"EU","destination":"US"}}
    PASS  @logged decorator path emits correctly

**Caveats, stated plainly:**
- The stub mirrors my model of FastMCP's internals (`_tool_manager._tools` → `.fn`). It is not
  the real SDK. **Use the `@logged` decorator: that path is pure Python and cannot depend on
  SDK internals.** `instrument()` is convenience; against a differing SDK it no-ops by design.
- The two `[VERIFY]` marks in `serve_http.py` (transport string, `mcp.settings`) remain
  unverified for the same reason.
- Local `uvx cbsr-mcp` is stdio + zero network **by design** → usage is permanently
  unobservable. Only the hosted endpoint yields telemetry. That conclusion is unchanged.

---

# RESOLVED: `corridor_directed()` added (2026-07-15)

The P0 above is fixed **additively**. The proposed "6-line" signal fix was tried first and
**rejected by your own build gate** (`build.py` exit 1: substrate/skeleton cross-check disagreed
on all 8 inbound-US edges): see FIX-EXPERIMENT.md. That fix would have required re-authoring
hand-maintained legal source. This one does not.

## What changed: 3 files, no data

| File | Change |
|---|---|
| `src/cbsr_mcp/server.py` | + `COMPUTED_CORRIDORS_DIRECTED` global; + `@mcp.tool() corridor_directed(origin, destination)`; + `authoritative_reading: "corridor_directed"` in the `compose_corridor` and `corridor_timeline` payloads |
| `mcp.json` | + tool entry at index 15 (33 → 34) |
| `MCP_SERVER.md` | + table row |
| `dataset.json` | **UNCHANGED** |

## Verified

    corridor_directed(EU,US):
      class_code        : T
      feasibility_class : Regime-in-transition (destination regime enacted, not yet operative;
                          resolves to Category II on the earlier of 2027-01-18 or 120 days after final rules)
      as_of_timeline    : today_class=T, scheduled=[us-genius-act-effective @ 2027-01-18,
                          date_kind=outer_cap, status=scheduled_with_cap, resolves_to=II]
      class_basis       : binding_status=made_not_commenced

    all 8 inbound-US:  EU/UK/SG/HK/BR/CH/AE/JP -> US   today=T  ->  II @ 2027-01-18 (outer_cap)

    compose_corridor(EU,US) -> computed_class=II, authoritative_reading="corridor_directed"

| Gate | Baseline | After |
|---|---|---|
| invariants | 57/57 | **57/57** |
| negative tests | 10/10 bite | **10/10 bite** |
| `check_identifiers.py` | pass | **pass** |
| `check_docs_sync.py` | 33 tools | **34 tools** |
| dataset diff (ex-timestamps) |: | **0 paths** |

Zero data movement is the point: the directed layer already contained `class_code: "T"` and the
`us-genius-act-effective` entry in `as_of_timeline`. The register had computed the right answer
all along; the agent-facing surface simply could not see it. This exposes it and asserts nothing.

## Still yours
Whether to migrate the World A layer (compose signals / substrate poles / authored corridor
YAMLs) so `compose_corridor` itself becomes timing-aware. That is a legal re-authoring, and the
gate will hold you to doing it completely. Not urgent now: agents have a correct reading, and
the preview points at it.

---

# `us-genius-act-effective` added to the event calendar (2026-07-15)

**Question asked: does the event pass the gate on its own, with signals untouched? Answer: YES: with one snapshot-count bump.**

## Change: 2 source files, no signal touched

| File | Change |
|---|---|
| `analysis/event_calendar.json` | + `us-genius-act-effective` (scheduled, 2027-01-18, `precision: outer_cap`, `trigger_kind: scheduled-with-cap`); + `scheduled-with-cap` in `trigger_kind_legend` |
| `run_invariants.py` | T1 snapshot count `8` → `9` (label + assertion) |

The `effect` names a **binding_status**, not a compose signal field: the same pattern
`us-clarity-act-enacted` already uses. So it records the change in law and moves no class.
`scripts/compose.py` SIGNALS is **untouched**.

    effect: [{"field": "binding_status (us-pss §18 comparability gate)",
              "from": "made_not_commenced", "to": "in_force_enacted"}]

## Gates

| Gate | Result |
|---|---|
| `build.py` | **accepted** (no validation failure; 9 events in dataset) |
| invariants | 56/57 → **57/57** after the T1 bump. T1 was the ONLY failure |
| negative tests | **10/10 bite** |
| identifiers / docs_sync | **pass / 34 tools** |

T1 is a hardcoded snapshot (`len(events) == 8`), not a design principle. Bumping it is the
established practice: the calendar's own note records doing exactly this at v0.9.6 (2 events
added) and v0.10.0 (8th event added).

## What it bought: and what it did not

    event_calendar()             -> us-genius-act-effective now present
    corridor_timeline(EU,US)     -> scheduled_transitions: [{date: 2027-01-18,
                                     precision: outer_cap, event_id: us-genius-act-effective,
                                     class_before: II, class_after: II, changed: False}]
                                    next_scheduled_change: None      <-- still
    corridor_directed(EU,US)     -> today = T  ->  II @ 2027-01-18 (outer_cap)

**The date is now on the calendar. The divergence is not fixed.** Under World A the class does
not move (the gate was always coded `comparability`), so `changed: False` and
`next_scheduled_change` stays `None`.

**Note the honest tension:** this moves `corridor_timeline` from *silence* about 2027-01-18 to an
explicit `class_before: II, class_after: II, changed: False`: i.e. from "doesn't mention it" to
"mentions it and says it doesn't matter." Under World A that is correct. Under World B it is
wrong. It is defensible **only** because `corridor_timeline`'s payload now carries
`authoritative_reading: "corridor_directed"` plus a note explaining the preview's limit. Merge
these two changes together or not at all.
