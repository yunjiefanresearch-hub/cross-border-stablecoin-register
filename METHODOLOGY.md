# Methodology

This register is an expert artifact, not a scrape. Its value is the judgment in the data —
how sources are weighed and how ambiguity is resolved — made transparent and reproducible.

## Source hierarchy
1. **Primary** — statute, regulation, central-bank/regulator resolution or circular, official gazette.
   Every record's `source.primary` cites a primary instrument with a pinpoint.
2. **Regulator guidance** — supervisory guidelines, FAQs, consultation papers (as `secondary`).
3. **Secondary analysis** — law-firm client alerts, academic analysis. Used only to locate or
   interpret primary sources, never as the sole basis for a classification.

## Verification rule
A record is **verified** only when (a) it contains no `<VERIFY …>` markers and (b) a human has
checked every `source.primary` and `pinpoint` against the instrument itself. AI tools are **not**
used to generate or fill citations — a single fabricated source is fatal to a reference of this kind.
The build pipeline flags any record still containing `<VERIFY` as a **draft** and excludes it from
verified coverage counts.

## Status values
- `in_force` — effective and binding now.
- `transitional` — in force but under a transitional/grace regime.
- `proposed` — published draft / bill not yet enacted.
- `consultation` — open consultation, text may change.

## Confidence
`high | medium | low` — the maintainer's confidence in the classification given source clarity and
settledness of the regime. Moving targets (e.g. pending bills, open rulemakings) carry `medium`/`low`.

## Two evidence axes — `claim_class` and `evidence_tier`
A record makes a claim of a particular **kind**, sourced to a particular **strength**. These are
tracked as two independent fields so neither is mistaken for the other.

- **`claim_class`** (the *kind* of claim) — `tier1_legal` is a **proposition of law**: what a binding
  instrument requires, permits, or prohibits, citable to the instrument. `tier2_operational` is a
  **market/operational fact**: what is live, who is registered, what launched, what rails or liquidity
  exist — read as-of-dated. The split is the Corridor Atlas §7 distinction between primary-source legal
  constraints (Tier 1) and market-reported operability (Tier 2). It is assigned per-record (the
  `implementation_status` dimension is operational; the other fourteen are legal), so an operational
  claim that ever appears inside a legal dimension can be marked `tier2_operational` explicitly.
- **`evidence_tier`** (the *provenance strength*) — `resolution_text` = confirmed against the official
  text; `mixed` = core point confirmed, some operational detail pending; `firm_summary` =
  practitioner-corroborated, pending the official-text check.

The two are **orthogonal**: a confirmed product launch is `tier2_operational` + `resolution_text`
(well-sourced, but not law); a draft statute is `tier1_legal` + `firm_summary` with `status: proposed`
(a legal claim, not yet binding, not yet checked against the enacted text). Confidence is a *third*,
separate axis (corroboration strength), not a substitute for either.

### Earned evidence tiers and the verification pass (v0.9.1)
`evidence_tier` is **earned, not asserted**. The build enforces necessary conditions per tier:
`resolution_text` ⟹ `source.url` + `pinpoint` + `last_reviewed`; `mixed` ⟹ `url` + `pinpoint`;
`firm_summary` ⟹ `pinpoint`. These are necessary, not sufficient — the tier remains a human judgment,
but it can no longer be *claimed* without the corroborating provenance, so a promotion only lands if the
evidence is actually present. The optional `verification` block records *how* a cell was confirmed
(`method` = `official_text` | `practitioner_corroboration`, `against` = instrument/url/pinpoint,
`verified_on`), giving promotions an audit trail; `method=official_text` is consistent only with
`resolution_text`/`mixed`.

The verification itself — confirming each unverified cell against the official statutory text — is
**external work that is never fabricated**. The register ships the harness that scopes and guards it:
the earned-tier gate, the optional `verification` block, and a per-cell **worklist**
(`analysis/verification_worklist.json`) listing, for each of the 47 unverified `tier1_legal` cells, the
instrument + pinpoint and exactly what is missing. The honest invariant: the constraint substrate stays
dark for a corridor until the relevant cells are verified, so the worklist *is* the substrate's growth
path and the discharge of the standing liability.

### The lawyer-citable subset, and why it is enforcedThe subset a lawyer or supervisor can cite as **current binding law** is the intersection
`claim_class == tier1_legal` AND `status == in_force` AND `evidence_tier == resolution_text`. To keep
that subset honest, the build enforces a locator rule: a `tier1_legal` record at `resolution_text` or
`mixed` *asserts* confirmation against the official text, so it **must** carry a `source.url` (and, at
`resolution_text`, a `pinpoint`) — otherwise the build fails. The subset is therefore never just a
filter over self-reported tags; every member points to the official instrument. It is published as
`citable_subset` in `dataset.json`, exposed by the `citable_law()` MCP tool, and shown by the "citable
law only" toggle on the site. The same discipline extends to the computed layer: `compose()` may rest
only on `tier1_legal` records, so a derived feasibility verdict is never founded on a market fact.

This is consistent with the citation firewall below — `claim_class` records *what kind* of thing a
source establishes; it never licenses generating or inferring a citation.

### Claim purity: operational illustration lives in `operational_notes`, not in the legal fields
A `tier1_legal` record's load-bearing fields (`requirement_summary`, `requirement_structured`,
`source.primary`, `pinpoint`) carry **only the proposition of law**. An operational illustration that
contextualises the claim — a product launch, a registration, the working example of a channel — goes in
the optional **`operational_notes`** field (`{ note, as_of?, source? }`), which is Tier-2 by definition,
read as-of-dated, and **omitted from the citable projection** (`citable_subset` / `citable_law`). The
build enforces the boundary (`check_citable_purity`): a citable record's `source.primary` and `pinpoint`
may not contain a product/market event or a named commercial counterparty, so the instrument a lawyer is
shown always resolves to the legal text alone. This keeps one cell as one record (no artificial
splitting) while ensuring the *citable view* of that record is purely legal; it is also the natural seed
of the per-clause constraint substrate (v0.9.0), where each C-dimension predicate will carry its own
tier and the citable projection will emit only the `tier1_legal` predicates.

## Coverage states (rendered in COVERAGE.md)
- ✅ **verified** — at least one verified record for that (jurisdiction × dimension) cell.
- ✍️ **draft** — a record exists but still contains `<VERIFY` markers.
- ⬜ **planned vX.Y** — scheduled in `roadmap.yaml`, not yet drafted.

## Time model — dated and contingent changes in law (v0.8.0)
Corridor feasibility is dated, because regimes commence on dates. The **event calendar**
(`analysis/event_calendar.json`) records the **changes in law** that move a jurisdiction's compose()
signal, and `compose(origin, destination, as_of)` applies the ones effective by a date before running
the Atlas algorithm. The model rests on three disciplines:

1. **Only changes in law are events.** Every event carries `claim_class: tier1_legal` and is backed by
   `tier1_legal` records; the build rejects an event backed by a `tier2_operational` record. A product
   launch is not an event — it is a market fact, recorded in a record's `operational_notes`. This is
   the v0.7 two-axis split inherited into the time dimension: a date-aware verdict must distinguish a
   change in *law* from a change in the *market*, and the engine is structurally prevented from
   advancing feasibility on a market event.
2. **Firm dates and contingent dates are different things.** A `scheduled` event has an
   `effective_date` (with `precision` — `day`, or `year` where only the operative year is known, as for
   the UK systemic regime) and is applied when `as_of >= effective_date`. A `contingent` event — a bill
   not yet enacted — has **no** date and is **never** applied by date; it is surfaced only as a
   hypothetical "if enacted" branch. The build rejects a contingent event that carries a date. This
   keeps a guessed enactment date from silently flipping a verdict.
3. **Temporal change vs structural difference.** When a scheduled event fires, the engine recomputes
   the undirected agreement. A finding that *resolves* at that horizon was a regime-in-transition
   artifact; a finding that *persists* is structural (a genuine Atlas-vs-§5.14 modelling difference).
   The worked example: US→UK is Category T today and Category I once the UK systemic regime is operative
   (2027), and the transition caveat on UK pairs clears — but the `EU-UK`/`UK-US` pairs remain findings
   afterward because the Atlas scores live-live as `I/II` while §5.14 authored them as cleanly bridgeable
   `I`. The engine reports the resolution and the residual separately rather than claiming the findings
   "go away."

## Constraint substrate — deriving feasibility from constraints (v0.9.0)
The substrate is the deepest expression of the composition thesis: rather than reading a hand-curated
inbound gate, it gives each `(jurisdiction × constraint C1–C8)` a structured **pole** and derives a
corridor's feasibility by composing two jurisdictions' poles **through the six interaction-set rules**
(§2.9). It rests on three disciplines, each inherited and sharpened from the layers below:

1. **Provenance, one level deeper.** Every pole cites the `tier1_legal` record(s) it is transcribed
   from; the build rejects a pole backed by a `tier2_operational` (market) record. Pole *assignment* is
   currently authored (transcribed from the records) — the same status as the signal table — and
   verifying each assignment against the primary text is part of the verification backlog.
2. **It never guesses.** A pole exists only where a record backs it; where a load-bearing pole is unset,
   `compose_via_substrate` returns **`indeterminate`** and names the missing poles. After the v0.9.2
   cell sweep and the v0.9.9 Taiwan enactment the substrate covers **80/96 cells** and derives **9/9**
   authored corridors and **115/132**
   directed edges — the seventeen indeterminate ones are the non-prohibited origins *into the UK and
   Taiwan*, whose inbound gates are in transition (the time engine, not the substrate, owns that). Coverage is still an
   honest readout, not a façade: the sixteen unset poles are the genuinely-unsettled cells (KR
   pre-regime; TW and UK regime-in-transition, C7 unset; CN C5, BR C4), and the verification pass stays *load-bearing* — populating a cell
   widens the substrate's structure, but only verifying it against the official text makes it citable.
3. **Cross-checked, not asserted.** Where the substrate yields a *definite* class it must equal the
   signal-table `compose()`; a disagreement fails the build and must be reconciled (the same
   computed-vs-authored discipline applied between the two engines). As of v0.9.91 the cross-check is
   exercised across **all 132 directed edges** (115 definite, every one agreeing) — not just the
   {HK, CN, JP} triangle. Worked derivations: HK→JP = II through Japan's *channelled* C7, JP→HK = I
   through Hong Kong's *open* C7, US→EU = I (EU's capped pole), EU→US = II (the US comparability
   channel) — the rules composing constraints correctly on real poles, not looked-up values.


## The `binding_status` cap on citability (v0.9.5)

The evidence model carries a third axis, `binding_status`, orthogonal to `evidence_tier` (provenance
strength) and `claim_class` (legal vs operational): the binding status of the *instrument* a cell rests
on. It encodes the central finding of the external verification pass — that **locating the official text
is not sufficient to make a cell citable as current law; the instrument must be enacted and in force.**
The build enforces that `resolution_text` requires `binding_status = in_force_enacted`, so a
made-but-not-commenced instrument (the UK FSMA 2026 SI, operative 2027-10-25), a finalized-but-
unlegislated policy (the MAS SCS framework), a pending bill or NPRM (the US CLARITY Act, the OCC/FDIC
NPRMs), or a prohibition (the PRC notices) cannot be cited as current law no matter how well its text is
read. Promotions are recorded in a `verification_ledger` audit trail, against which the build cross-checks
every record to prevent drift. This makes the citable subset an enacted-law-only set by construction, and
makes *why* a cell is or isn't citable explicit and queryable.

## Versioning
Semantic versioning. Each tagged release is archived to Zenodo for a citable DOI. The changelog
records what regulatory facts changed between versions (the register doubles as a regulatory-diff log).
