# Build Note — v0.8.0: The time / event engine

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** make corridor feasibility *dated* —
feature #1 of the three-feature plan — by adding an event calendar of changes in law and a date-aware
`compose(origin, destination, as_of)`, while inheriting the v0.7 evidence discipline into the time
dimension.

## 1. Why this, and why now

The three candidate "beyond-the-PDF" features were: (#1) a time/event engine, (#2) the two-axis
evidence model, and (#3) the constraint substrate with a real `compose()`. The deepest is #3. But #3's
prerequisites — an evidence split that separates a proposition of law from a market fact, and a
provenance gate so the computed layer rests only on law — are exactly what v0.6.0–v0.7.1 delivered. So
#1 is the now-unblocked, highest-applicability, lowest-shallowness-risk next step: it answers the
question users actually ask ("blocked today, Category I after the regime is operative"), and it inherits
the tier split for free. #3 remains the deeper, later thesis (v0.9.0).

## 2. The clock: an event calendar of changes in law

`analysis/event_calendar.json` records the **changes in law** that move a jurisdiction's compose()
signal. Each event is `{ id, jurisdiction, title, status, effective_date?, precision?, trigger?,
claim_class, effect:[{field,from,to}], basis, date_basis, records }`, with three statuses:

- **`scheduled`** — has an `effective_date` (and `precision`: `day`, or `year` where only the operative
  year is known). Applied when `as_of >= effective_date`.
- **`contingent`** — a bill with no firm date. **Never applied by date**; surfaced only as a
  hypothetical "if enacted" branch.
- **`in_force`** — already effective at the base date.

Four events ship: the **UK systemic + conduct regime** (scheduled, modelled 2027-01-01, precision
`year`) — the headline; the **Taiwan VAS Act** and **Korea DABA** (contingent — bills, no firm date);
and **Japan's Act 66/2025** full enforcement (in force, `effect: []` — included precisely to show the
calendar distinguishes a change in *law* from a change in *feasibility class*; Japan is already live).

## 3. The discipline this version is really about

The point of doing #2 before #1 was that a date-aware verdict must not advance on a market event. The
calendar enforces this:

- **Every event is `claim_class: tier1_legal`**, and **every backing record in `records` must be
  `tier1_legal`** — checked by `check_event_provenance()` (in `scripts/compose.py`) and re-enforced in
  `build.py`. A market launch (a `tier2_operational` fact) can never be an event; it lives in a record's
  `operational_notes` (the v0.7.1 field). *Negative test:* pointing an event at
  `jp-epi-implementation_status-001` (tier2_operational) fails the build.
- **A contingent event may not carry a date.** *Negative test:* giving `tw-vas-act-enacted` an
  `effective_date` fails the build. This keeps a guessed enactment date from silently flipping a verdict.

Note a deliberate modelling choice: the UK event's backing record is `uk-frs-regulatory_authority-001`
(tier1_legal, the SI 2026/102 framework), **not** the tier2_operational implementation-status record —
the forward-looking commencement is carried by the event's `date_basis` with `precision: year`, not by
pretending an in-force record already asserts the 2027 systemic regime.

## 4. Date-aware compose, and an honest headline

`signals_as_of(date)` deep-copies the signal table and applies every scheduled/in-force event ≤ date;
`compose_directed` and the undirected reduction are now parametrised on a signal set.
`edge_timeline(o, d)` returns today's class, the dated transitions that change it, and contingent "if
enacted" branches. `computed_timeline.json` records per-corridor timelines, **illustration edges** (the
authored nine corridors don't touch the UK, where the transition is), and the agreement over time.

The headline result is stated the way the project states things — with the part that *doesn't* move
called out:

- **Directed `US→UK`: Category T today → Category I as of 2027-01-01**, when the systemic regime is
  operative. Clean, and exactly the "blocked/T today → Category I later" demonstration.
- **Transition-caveated undirected pairs: 8 today → 0 at the 2027 horizon** — the regime-in-transition
  caveat (`I/II*`) clears.
- **But `EU-UK` and `UK-US` remain findings after 2027.** Their residual is *structural*, not temporal:
  the Atlas scores live-live as `I/II` (dual-authorization-or-partnership) while Architecture §5.14
  authored them as cleanly bridgeable `I`. The exact-match agreement therefore stays **64/66** across
  the horizon. The engine separates the regime-in-transition artifact (resolves by date) from the
  modelling difference (does not) instead of reporting a tidy "findings resolved."

This is a stronger result than "the UK findings go away": it localises which part of a disagreement is
a calendar artifact and which part is a real divergence between the two source documents.

## 5. Surfaces: MCP (18 → 20) and the site

- **MCP**: `compose_corridor(origin, destination, as_of?)` gains an optional `as_of` (returns the as-of
  class, the base class, and `changed_from_base`); new `event_calendar(jurisdiction?)` and
  `corridor_timeline(origin, destination)`. Verified via the mock: `compose_corridor('US','UK',
  as_of='2027-06-01')` returns I (base T, changed True); `corridor_timeline('US','UK')` shows the
  2027-01-01 T→I transition; `corridor_timeline('US','TW')` shows pre_regime today with a contingent
  "II if enacted" branch.
- **Site**: a new "Feasibility over time" section renders the headline, per-edge timelines (today →
  dated transition; contingent "if enacted"), and the event calendar — all from the embedded
  `analysis.computed_timeline` / `analysis.event_calendar`.

## 6. The liability this does not touch (restated)

The time engine is orthogonal to the standing liability: **47 `tier1_legal` cells remain `unset`**
(transcribed, not yet confirmed against the official text), and every compose() agreement — at any date
— rests on the hand-curated signal table and those cells. Dating the verdicts does not verify them.
Only the primary-source verification pass retires that liability; it is bundled into v0.9.0.

## 7. Validation

- Full pipeline green at v0.8.0: **117 records, 9 corridors, 66 pairs**; computed (non-temporal) layer
  unchanged (**9/9**, **64/66**); signal provenance clean; pre-regime `{KR, TW}` consistent; citable
  subset **21**.
- Time layer: **4 events, event-provenance clean**; `US→UK` base T / as-of-2027 I; transition-caveated
  pairs **8 → 0**.
- Negative tests pass (all fail the build as intended, all restored): citable-URL strip;
  signal-provenance flip; citable-purity re-bundle; **event backed by a tier2_operational record**;
  **contingent event carrying a date**.
- Static site regenerated at v0.8.0; timeline section renders; app JS passes `node --check`. Fresh
  extract reproduces all metrics. The local `jsonschema` shim remains outside the package.
