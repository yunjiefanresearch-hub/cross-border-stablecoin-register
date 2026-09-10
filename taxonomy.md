# Controlled vocabulary

## Jurisdictions
`HK` Hong Kong · `TW` Taiwan · `BR` Brazil · `US` United States ·
`EU` European Union · `UK` United Kingdom · `SG` Singapore · `CN` mainland China ·
`CH` Switzerland · `AE` United Arab Emirates · `JP` Japan · `KR` South Korea

**Coverage reorientation (v0.4.0 — twelve-jurisdiction expansion).** The maintainer's revised
written substrate — the **Compliance Matrix v0.9.6** and **Cross-Border Stablecoin Architecture
v3 (Twelve Jurisdictions)** — now covers **twelve** jurisdictions in verified depth. The
register's focus set is aligned to that substrate:
- **Anchor:** US (CLARITY §404 / GENIUS Act — the doctrinal anchor).
- **Focus (verified substrate exists):** HK, EU, UK, SG, CN, BR, **CH, AE, TW, JP, KR**.
  - **CH / AE / JP / KR** added in v0.4.0 from Compliance Matrix v0.9.6 (Switzerland — bank-guarantee
    regime with permitted-but-guaranteed yield; the UAE — federal/free-zone split with an onshore
    monetary-sovereignty *channel restriction*; Japan — Electronic Payment Instruments with a closed
    issuer trichotomy and a channelled inbound route for foreign tokens; South Korea — pre-regime,
    VAUPA in force with a pending Digital Asset Basic Act).
  - **TW** promoted from a parked window to a full jurisdiction: the AML-registration layer (amended
    Money Laundering Control Act + VASP Registration Regulations, in force 30 Nov 2024) is operative;
    the draft **Virtual Asset Service Act** issuance provisions are carried as `status: proposed`,
    `draft_provision`-tagged records.
- **Parked (no written substrate yet):** none — the focus set now equals the substrate.

**Draft-law convention.** For jurisdictions whose issuance regime is a bill (TW, KR), only the
in-force layer (AML registration / user-protection) carries `status: in_force`; draft issuance,
reserve, capital, yield, redemption, monetary-sovereignty, and distribution provisions carry
`status: proposed` and the `draft_provision` tag, with `evidence_tier: firm_summary` pending the
primary-source pass. The build still renders these as ✅ in `COVERAGE.md` (a sourced record with no
`<VERIFY` marker), so the draft nuance lives in the `status` / `evidence_tier` / `tags` fields.

## instrument_type (normalized) ↔ instrument_label_local (verbatim)
- `fiat_referenced_stablecoin` — HK "specified stablecoin" / FRS; general FRS
- `payment_stablecoin` — US "payment stablecoin" (GENIUS Act / CLARITY)
- `e_money_token` / `asset_referenced_token` — EU MiCA EMT / ART
- `tokenized_mmf` — 1940-Act registered tokenised money market fund (routing target)
- `tokenized_security` — tokenised security under local securities law
- `other`
The dual field is the built-in concordance: one normalized type, each regime's own label.

## dimensions (15) — aligned to the eight-constraint framework

The register's dimension set is the union of (a) the ten Compliance-Matrix dimensions and
(b) the eight constraints of *Cross-Border Stablecoin Architecture* (§2.1–§2.8). The
`constraint_ref` field on each record links back to the constraint vocabulary.

| Dimension | Constraint | Notes |
|---|---|---|
| `regulatory_authority` | — | authority + statutory basis |
| `issuer_pathway` | C1 Issuer Eligibility | |
| `reserve_backing` | C2 (reserve half) | **split** from former `reserve_capital` |
| `capital_requirements` | C2 (capital half) | **split** from former `reserve_capital` |
| **`permitted_activity_yield`** | **C3 Yield Prohibition** | **spine 1** — the bona-fide-activity / yield line |
| **`securities_classification`** | **C4 Securities Classification** | **spine 2 (new)** — Reves/Howey; routing-into-funds line |
| `bank_nonbank_routing` | C5 Bank/Non-Bank & Routing | **new** — who may route; layer separation |
| `redemption` | — | |
| `custody` | C2 (custody facet) | |
| `aml_kyc` | — | |
| `cross_border_data` | C6 Cross-Border Payment & Data | |
| `monetary_sovereignty` | **C7 Monetary Sovereignty / Reserve-Currency Asymmetry** | **new** — non-domestic-currency usage caps |
| `disclosure_reporting` | C8 Disclosure, Reporting, Supervisory Coordination | **new** — attestation/audit/reporting |
| `distribution` | — | |
| `implementation_status` | — | maturity stage / timeline |

**Two spines.** The original register had one spine (`permitted_activity_yield`). The written
corpus makes clear there is a *second* spine, `securities_classification`: two stand-alone
papers (*When Wallets Become Brokers*; *Reves' Fourth Factor and Stablecoin Routing*) turn on
it, and §4 of the Architecture paper composes C3×C4 directly. It is promoted to spine status.

## status
`in_force` · `transitional` · `proposed` · `consultation`

## confidence
`high` · `medium` · `low`

## claim_class (v0.7.0) — the *kind* of claim
`tier1_legal` · `tier2_operational`

The epistemic kind of a record's load-bearing claim, **orthogonal** to `evidence_tier` (how
well-sourced) and `status` (in force vs draft).

- **`tier1_legal`** — a **proposition of law**: what a binding instrument (statute, regulation,
  official guidance) requires, permits, or prohibits. A fact a lawyer could cite to the instrument.
  All fourteen dimensions other than `implementation_status` state propositions of law.
- **`tier2_operational`** — a **market/operational fact**: what is actually live, who is registered,
  what products launched, what banking rails or liquidity exist. Read as-of-dated. The
  `implementation_status` dimension is operational by construction.

The split follows the **Corridor Atlas §7** distinction between primary-source legal constraints
(Tier 1) and market-reported operability (Tier 2), which the Atlas warns must not be read at the same
confidence. The field is **per-record**, not derived from the dimension, so a future operational claim
inside a nominally-legal dimension (e.g. a `monetary_sovereignty` record whose load-bearing fact is a
market datum) can be tagged `tier2_operational` explicitly. Corridors do not carry `claim_class`.

**Structural citable candidates** satisfy `claim_class == tier1_legal`, `status == in_force`,
and `evidence_tier == resolution_text`. They are retained as the legacy `citable_subset`
in `dataset.json`. **Decision-ready citable law** additionally requires
`source_disposition == official`, `freshness.review_status == current`, and
`review_stage == reconciled`, with a source URL and pinpoint. This stricter
`decision_ready_citable_subset` is what `citable_law()` and the "citable law only"
toggle expose. Current means current at the dated snapshot. The 2026-08-20 snapshot
has 46 structural candidates and 0 decision-ready records out of 152 total records.

## evidence_tier — provenance strength
`resolution_text` · `mixed` · `firm_summary` (legacy records: unset)

How well-sourced the record is, independent of `claim_class`. `resolution_text` = confirmed against the
official statutory/regulatory text; `mixed` = core point confirmed, some operational detail pending;
`firm_summary` = practitioner/law-firm-corroborated, pending the official-text check. A `tier1_legal`
record at `resolution_text`/`mixed` must carry a `source.url` (and `resolution_text` a `pinpoint`) — a
build-enforced rule, so the citable subset cannot drift from "confirmed against the source."

## operational_notes (v0.7.1) — Tier-2 illustration attached to a record
Optional array of `{ note, as_of?, source? }`. The home for a market/operational fact (a launch, a
registration, a working example) that contextualises a `tier1_legal` claim without belonging in its
load-bearing legal fields. It is Tier-2 by definition, read as-of-dated, **excluded from the citable
projection** (`citable_subset` / `citable_law`), and rendered on the site as a "Tier-2 · not citable as
law" block. The build (`check_citable_purity`) forbids the same operational material — product/market
events, named commercial counterparties — from appearing in a citable record's `source.primary` or
`pinpoint`, so the instrument shown to a lawyer resolves to the legal text alone.

## interpretive_flag
Carries the Matrix's `[⚠ interpretive question]` construct as structured data:
`{ tension, resolution_channel }`. These are research instruments, not legal advice.

## analysis layer (v0.5.0)
The analysis layer encodes the Architecture working paper's payload as queryable data (under
`analysis` in `dataset.json`; standalone files in `analysis/`; schema `analysis.schema.json`).

**Compatibility categories** (the §5.14 pairwise outcome for a jurisdiction pair):
`I` dual-authorization compatible · `I/II` hybrid (dual authorization *or* partnership) ·
`II` partnership distribution required · `III` composition problem unresolved.

**Category-III axes** (why a pair is unresolved):
`prohibition` (PRC — issuance prohibited; §3.3 patterns apply) ·
`pre_regime` (TW / KR — not prohibited, not yet authorizable; resolves on enactment) ·
`prohibition+pre_regime` (PRC × TW) ·
`counterparty_conditional` (the Brazil câmbio leg — permitted only via a licensed VASP with an
FX-authorised counterparty or within the per-operation cap).

**Interaction sets** (§2.9 — the constraint pairs that jointly bind): `A` C1×C6 · `B` C3×C4 ·
`C` C5×C1 · `D` C2×C7 · `E` C4×C6 · `F` C8×(C1–C7).

## corridor layer (directed edges)
A corridor is a directed origin→destination edge (the inbound gate binds, so the edge is read at
the destination). **Archetypes:** `RC` Regulatory · `SC` Stablecoin Settlement · `TC`
Tokenized-Asset · `DC` Digital-Financial. **Feasibility class** composes the destination inbound
gate with any origin drag: Category I / II / III, plus `blocked` (✕, destination prohibition),
`pre_regime` (○) and `regime_in_transition` (T). An **origin-override** flag marks an origin that
imposes an export/egress restriction (e.g. the MAS DTSP perimeter for Singapore-origin edges).
Source: Cross-Border Digital-Finance Corridor Atlas v0.2.3.

A corridor exists in two tiers. An **authored rich record** carries the full Atlas model
(`inbound_mechanism`, `administrator`, `archetypes`, `infrastructure_overlap`, prose); there are 9. A
**computed skeleton** (`analysis.computed_corridor_skeletons`) is emitted for every *other* derivable
directed edge and carries only the structurally-derivable fields — feasibility class (from the substrate),
inbound-mechanism `test` + `administrator` (re-projected from the destination's C1/C7 record), a baseline
archetype set, and the directed interaction sets — with provenance, cross-checked against the signal
`compose()`. Empirical fields (`infrastructure_overlap`, bespoke detail) are left unset as a per-edge
enrichment backlog. Edges into a destination whose inbound gate is in transition (the UK) have neither
tier and remain `indeterminate` — the time engine owns them.

## stakeholder layer (Atlas §8 projection)
A **stakeholder** is an actor persona that reads only a slice of C1–C8: `issuer`, `distributor`
(wallet/PSP), `reserve_custodian`, `home_regulator`, `host_regulator`, `corporate_treasury`,
`token_holder`. Each declares a *lens*, the constraints it reads on the origin and on the destination,
and the corridor archetypes (RC/SC/TC/DC) it engages. The projection `profile_for(stakeholder, edge)`
re-reads the already-derived corridor class and the relevant substrate poles through that lens — it adds
no new facts, cites the backing record for every line, and is preview (bounded by the verification status
of the cells it reads). Ships under `analysis.stakeholder_database` (the catalogue) and
`analysis.computed_stakeholder_profiles` (worked projections). Source: Corridor Atlas v0.2.3 §8.

## computed layer (v0.6.0)
The computed layer (`analysis/computed_compatibility.json`, embedded at `analysis.computed`) is the
output of `compose()` — feasibility *derived* from rules, then diffed against the authored values.

**Per-jurisdiction signals** (the inputs to compose, each annotated with the justifying node record):
`regime_status` ∈ {live, transition, pre_regime, prohibition}; `inbound_gate` ∈ {open, open_capped,
comparability, channel, usage_channel, fx_counterparty, transition, pre_regime, prohibition};
`exportable_token` (bool — an origin without one drags the edge to Category III); `egress_override`
(bool — origin imposes an export restriction, e.g. CN, SG).

**Feasibility classes** (the directed output vocabulary, six values): `I` dual authorization available ·
`II` comparability / recognition / channel determination required · `III` composition unresolved ·
`T` regime adopted but not operative · `blocked` (✕) destination prohibition · `pre_regime` (○).

**compose rule** (Corridor Atlas §3.2): origin drag first (no exportable token ⇒ III), else the
destination-determined class from the inbound-gate type. The undirected §5.14 category is a reduction
of the two directed classes.

**Cross-layer integrity:** a corridor's `compatibility_category` must equal its §5.14 row; differing
`interaction_sets` require a declared `divergence` object (`against_pair`, `pair_interaction_sets`,
`edge_interaction_sets`, `reason`). A computed-vs-authored disagreement is a **finding** (with a named
cause, e.g. `uk_regime_in_transition`), not a silent contradiction.

## time engine (v0.8.0)
The time engine makes corridor feasibility **dated**. Two artifacts, both embedded in `dataset.json`:

**`analysis/event_calendar.json`** — dated/contingent **changes in law** that move a jurisdiction's
compose() signal. Each event: `{ id, jurisdiction, title, status, effective_date?, precision?,
trigger?, claim_class, effect: [{field, from, to}], basis, date_basis, records }`.
- `status` ∈ {`scheduled` (has an `effective_date`; applied by `compose(as_of >= date)`; `precision`
  may be `day`/`year` where only the operative year is known), `contingent` (a bill with no firm date —
  never applied by date, only surfaced as an "if enacted" branch), `in_force` (already effective)}.
- `claim_class` of every event **must be `tier1_legal`**, and every id in `records` must resolve to a
  `tier1_legal` record — enforced by the build. A market launch is never an event (it lives in a
  record's `operational_notes`). This is the v0.7 two-axis discipline inherited into the time dimension.

**`analysis/computed_timeline.json`** (`analysis.computed_timeline`) — the date-aware output:
`signals_as_of(date)` applies the scheduled/in-force events ≤ date, then re-runs compose(). Records
per-edge timelines (today's class → dated transitions → contingent "if enacted" branches), the
undirected agreement over time, and the count of transition-caveated (`I/II*`) pairs at each horizon.
A residual finding that persists past a scheduled horizon is **structural** (an Atlas-vs-§5.14
modelling difference), not temporal — the engine distinguishes the two.

## constraint substrate (v0.9.0)
The deepest layer (`analysis/constraint_substrate.json`, embedded at `analysis.constraint_substrate`):
each `(jurisdiction × constraint C1–C8)` cell is a structured **pole** from a controlled vocabulary,
with `derived_from` citing the `tier1_legal` record(s) it is transcribed from.

**Pole vocabularies** — C1 issuer eligibility {open, licence_gated, closed_set, host_currency_first,
no_pathway, prohibition}; C2 reserve/capital {prescribed_hqla, prescribed_flex, informational}; C3
yield {permitted, prohibited_issuer, prohibited_incl_agents, silent}; C4 securities {payment_instrument,
contested_routing, security}; C5 bank/non-bank {bank_only, bank_and_nonbank, layered_separation};
C6 cross-border/data {open, transfer_gated, localized, restrictive}; C7 monetary sovereignty {open,
usage_capped, channelled, prohibition}; C8 disclosure {coordinated, constrained}. Attributes:
`exportable_token` (C1), `blocks_supervisory_sharing` (C6), `supervisory_sharing` (C8).

**Derivation** (`compose_via_substrate`, `analysis.computed_substrate`): origin drag (C1
`exportable_token`); destination inbound from C7×C1 (Set D / Set C — prohibition→blocked,
channelled→II, usage_capped/open→I); the Set A overlay (C1×C6 — origin data-sovereignty blocking
supervisory sharing escalates to III). Returns **`indeterminate`** where a load-bearing pole is unset.
Every pole must cite `tier1_legal` records (provenance-enforced); a definite substrate class must equal
the signal-table `compose()` (cross-check-enforced). Coverage is bounded by the verification backlog.

## verification harness (v0.9.1)
**`evidence_tier` (earned).** Enforced necessary conditions: `resolution_text` ⟹ source.url + pinpoint
+ last_reviewed; `mixed` ⟹ url + pinpoint; `firm_summary` ⟹ pinpoint. The tier is a human judgment but
cannot be claimed without the provenance.

**`verification` block** (optional record field): `{verified_by, verified_on, method
(official_text|practitioner_corroboration), against {instrument, url, pinpoint}, excerpt?}` — the audit
trail of how a cell was confirmed; `method=official_text` is consistent only with resolution_text/mixed.

**Verification worklist** (`analysis/verification_worklist.json`, `analysis.verification_worklist`):
per-cell gap analysis for the (external) primary-source pass — for each unverified record, the
instrument + pinpoint and what is missing to reach each tier. Headline counts by jurisdiction and
constraint. Exposed by the MCP tool `verification_worklist`. Verification is never fabricated; this
artifact scopes it.

## `binding_status` (v0.9.5) — the citability cap

A third evidence axis, orthogonal to `evidence_tier` and `claim_class`: the binding status of the
instrument a cell rests on.

- **`in_force_enacted`** — enacted statute/regulation, in force now (the *only* status eligible for `resolution_text`).
- **`made_not_commenced`** — made/passed but not yet commenced (e.g. UK SI 2026/102, operative 2027-10-25). Real law, not yet operative.
- **`finalized_policy_pending`** — a finalized regulator policy awaiting implementing legislation (e.g. the MAS SCS framework). Not enacted law.
- **`pending_proposal`** — a pending bill, NPRM, or consultation (e.g. the US CLARITY Act, the OCC/FDIC NPRMs, pending BCB rules). Not law.
- **`prohibition`** — the cell rests on a prohibition/absence-of-regime, so there is no positive permitted-activity rule to confirm (the PRC cells). Cannot be `resolution_text` as a positive proposition.
- **`no_regime`** — no operative regime addresses the cell.

The build forbids `resolution_text` on any status other than `in_force_enacted`, so locating the official
text does not by itself make a cell citable as current law.
