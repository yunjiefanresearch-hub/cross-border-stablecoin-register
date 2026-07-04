# Changelog

All notable changes to the **Cross-Border Stablecoin Register** are recorded here. The register
doubles as a regulatory-diff log: each version states what changed. Format follows
[Keep a Changelog](https://keepachangelog.com/); versioning is [SemVer](https://semver.org/).
Each tagged release is archived to Zenodo for a citable DOI; the **concept DOI
[10.5281/zenodo.20730358](https://doi.org/10.5281/zenodo.20730358)** always resolves to the latest
version, while each release below carries its own version DOI.

## [0.9.9] — 2026-06-30

> **Time dimension made real, and the record caught up to the dateline.** v0.9.9 does three things.
> It backfills the MiCA transitional expiry into the register's own event calendar as a structured
> intra-regime-gating event (so the flagship §3.10 claim is register-backed, not matrix-only). It surfaces
> the already-computed time engine as interactive corridor/console pages, a static JSON API, and new MCP
> tools. And, on the 30 June 2026 dateline, it records Taiwan's third-reading enactment: the register cell
> that read "a bill" the morning of the snapshot is moved to enacted-but-not-commenced, exactly the case the
> method exists to absorb. No claim is asserted beyond its verified backing.

### Fixed (post-release consistency patch)
- **Constraint substrate now reflects Taiwan's enactment.** The v0.9.9 dateline update moved Taiwan's
  records and the signal table to enacted-not-commenced, but the Taiwan C1 constraint-substrate pole was
  left at `no_pathway` (pre-regime). Re-running `scripts/substrate.py` and `scripts/build_edge_skeletons.py`
  therefore produced a definite `pre_regime` class for the nine inbound edges into Taiwan that disagreed
  with the signal `compose()` (which reads Category T, regime-in-transition), and `build.py` failed on that
  cross-check. Taiwan's C1 pole is now `licence_gated` with `exportable_token:false` (the
  enacted-not-commenced signature: a legislated approval-gated pathway exists, but no token is exportable
  until licences issue), mirroring the UK regime-in-transition treatment. `compose_via_substrate` now
  returns `indeterminate` inbound (the time engine owns the commencement) and Category III outbound via the
  origin drag, matching the signal compose. The stale `computed_substrate.json`,
  `computed_corridor_skeletons.json`, and `verification_worklist.json` (which still described Taiwan as a
  draft bill) are regenerated. Edge-layer coverage moves 124/132 to 115/132 (the nine Taiwan inbound edges
  join the eight UK ones as regime-in-transition indeterminate); invariant **A3** and the METHODOLOGY
  substrate paragraph are updated to match.
- **CI now regenerates every pure derivative before `build.py`.** `scripts/substrate.py`,
  `scripts/build_edge_skeletons.py`, `scripts/stakeholders.py`, and `scripts/build_worklist.py` are added to
  the CI regeneration block ahead of `build.py`, so the reproducibility gate (a `git diff` on `dataset.json`,
  `analysis/`, and `api/`) also covers them and a stale substrate, skeleton, or worklist can no longer be
  committed. This closes the drift class that let the Taiwan substrate lag: these four generators ship
  artifacts but were not previously re-run in CI.
- **Result:** the full documented pipeline (all generators, then `build.py`, `run_invariants.py`,
  `run_negative_tests.py`, `check_readme_counts.py`) is green and reproducible from a clean checkout;
  47/47 invariants hold and 9/9 negative tests bite.

### Fixed / Added (post-release consistency patch, round 2)
- **Stale cross-jurisdiction reference corrected (KR).** `kr-frs-regulatory_authority-001.yaml` still read
  "Analytically paired with Taiwan as pre-regime", which contradicts §3.4 after Taiwan's 30 Jun 2026
  enactment. It now reads that Taiwan transitioned to enacted-not-commenced on 2026-06-30 and South Korea
  is the sole remaining pre-regime origin, holding the both-directions pending position alone. This drift
  form (a hand-written note describing ANOTHER jurisdiction's state) sits outside the CI reproducibility
  gate and outside B1/B3 (which only check a cell's own binding-status wording).
- **New gate X1 closes that drift form.** A lint fails the invariant suite if any record's prose calls
  another jurisdiction pre-regime while that jurisdiction's signal is not pre_regime; a matching negative
  test (`xref-pre-regime`) proves it bites. Invariants 47 -> 49 (with F1 below); negative tests 9 -> 10.
- **Japan foreign-stablecoin recognition is now a first-class event.** The same-date Cabinet Office
  Ordinance (effective 1 Jun 2026) recognising equivalent foreign trust-type stablecoins was folded into
  the Act No. 66 event's prose; it is now its own event `jp-foreign-stablecoin-recognition` with a new
  `inbound-recognition` trigger kind (a dated, in-force change that opens an inbound recognition channel
  handled by conditioning, asserting no new class), backed by the JP C7 channelled-admission record. This
  is the second same-day change §3.6 separates and the dated recognition instance §5.3 uses. Event count
  7 -> 8; invariant T1 updated.
- **New per-jurisdiction supervisor forward view (Atlas §4.4).** `scripts/build_forward_view.py` emits
  `analysis/computed_forward_view.json`, re-sorting the trigger register BY JURISDICTION: each
  jurisdiction's own pending events (flagged class-moving vs accessibility-only), the inbound and outbound
  edges that reclassify under the pending set (split into own-trigger-driven vs counterpart-driven and
  attributed to the trigger causing each), the counterpart jurisdictions ranked by exposure, and a
  supervisor_reading. It asserts no new facts (re-projects `computed_corridor_states.json` +
  `event_calendar.json`). Surfaced as `api/forward.json` and a `forward` block on each
  `api/jurisdictions/{X}.json`, and as MCP tool `forward_view(jurisdiction)` (bundled into `dataset.json`
  so the tool can read it). New invariant **F1** checks it is well-formed (12 jurisdictions; the EU's own
  pending change is accessibility-only with no own-driven class movement; KR's own trigger is the
  both-directions one; provenance asserts no new facts). Added to CI ahead of `build_api.py`. MCP tools
  32 -> 33.
- **The two derivative-paper PDFs re-exported to v0.9.9.** `pdf/Cross-Border_Stablecoin_Feasibility_Over_Time_v0.1.0.pdf`
  and `pdf/Citable_by_Construction_Methodology_v0.1.0.pdf` still referenced CBSR v0.9.8 while their `.md`
  sources are v0.9.9. PDF rendering is a binary generator outside the `git diff` reproducibility gate, so
  it lagged a version. Both are re-exported from the current `.md` (pandoc + xelatex, 25 and 14 pages as
  before) and now reference CBSR v0.9.9 with no stale v0.9.8. (Note: `pdf/DISCLOSURE.pdf` also shows
  v0.9.8, but that is a stale SOURCE — `DISCLOSURE.md` itself reads v0.9.8 — so it is a content edit, not
  a re-export, and is left to the maintainer.)
- **Result:** full pipeline green and reproducible in a single CI pass (exit 0 on the `git diff` gate);
  49/49 invariants hold and 10/10 negative tests bite.

### Polish (post-release, round 3 — textual/alignment only, no behaviour change)
- **`horizon_rule` and the MCP `events_by_kind` note now enumerate `inbound-recognition`** alongside
  `dated-empty-effect` and `intra-regime-gating` as the dated-but-horizon-inert kinds. The principle was
  already correct (only `fully-scheduled` moves a horizon); the enumeration just omitted the new kind.
- **The Japan recognition event is now dual-backed.** `jp-foreign-stablecoin-recognition` cited only the
  C7 channelled-admission cell (`jp-epi-monetary_sovereignty-001`, the most on-point: it is the
  recognition-and-registration channel §86 scores as Category II). It now also cites the C1 issuer/EPIESP
  cell (`jp-epi-issuer_pathway-001`), since a recognised foreign token reaches Japan only through a
  registered EPIESP; both are tier1_legal + in_force, so the backing is stronger and the event-provenance
  gate still holds.
- **Companion paper aligned to the register's 10-kind legend (§3).** The register's `inbound-recognition`
  was a kind the paper's typology named only in passing; the Feasibility paper's §3.11 table now names both
  Japan same-day kinds (`Dated-empty-effect`, `Inbound recognition`) rather than the uninformative "In
  force", the §3.11 intro count is corrected (ten -> eleven entries, matching the 11 rows), and the §3
  typology paragraph names `dated-empty-effect` and `inbound-recognition` as kinds. The Feasibility PDF is
  re-exported (25 pages, CBSR v0.9.9). (The `Six kinds recur` phrasing in §3 counts the primary recurring
  trigger kinds and is left as authored; the register now names 10 kinds in total.)
- **Result:** unchanged behaviour; 49/49 invariants, 10/10 negative tests, single-pass reproducibility
  exit 0.



### Added — trigger typology and the MiCA event (Phase 1 backflow)
- **Event calendar** (`analysis/event_calendar.json`): every event now carries a `trigger_kind` implementing
  the flagship §3 typology, defined in a new `trigger_kind_legend`. Added the 7th event, the EU MiCA
  Article 143(3) transitional expiry, as a structured `intra-regime-gating` item with the staggered national
  schedule and the second-order EMT-custody development, with an explicitly empty feasibility effect
  (mirroring the JP control case), so it moves no compose() horizon.
- **EU EMT cell** (`eu-emt-regulatory_authority-001.yaml`): the transitional-expiry prose is corrected from
  the old uniform "ends 1 July 2026" framing to the staggered national schedule (1 July 2026 is the outer
  cap; the deadline binding a corridor is the earliest among the Member States it touches). The citable
  proposition (MiCA Titles III/IV + the EBA/ESMA/NCA architecture) is unchanged; binding_status, evidence_tier,
  url, and verification are untouched, so the ledger does not drift.
- **Open questions** (`analysis/open_questions.json`): each carries a `trigger_kind` aligned with the §3 typology.
- **Convergence product** (`analysis/computed_convergence.json`, folded into `dataset.json`): the §4.5 yield-line,
  asserted at citable depth only for the US anchor, with SG as a sibling and CH as the documented counter-example.

### Added — surfacing (Phase 2)
- **Interactive pages**: `corridors.html` (time-slider corridor explorer with what-if trigger toggles and the
  convergence view) and `console.html` (records browser with the "why not citable" x-ray, the citable-law table
  with CSV export, computed-vs-authored reconciliation, the integrity gate, and the worklist), both inheriting
  the site's design tokens.
- **Static JSON API** (`api/`): per-jurisdiction, per-corridor, per-date views plus events/convergence/
  reconciliation/corridor-states and an index manifest, each with a provenance envelope; no backend.
- **MCP tools**: `events_by_kind`, `convergence`, `reconciliation`, and a three-axis `records`, plus a generated
  `mcp.json` manifest and `docs/CONNECT_MCP.md`.

### Changed — Taiwan recorded as enacted-but-not-commenced (30 June 2026 dateline)
- **TW issuer cell** (`tw-frs-issuer_pathway-001.yaml`): `status` proposed → transitional, `binding_status`
  pending_proposal → made_not_commenced, on the Virtual Asset Service Act's third-reading enactment. The
  native-language (Chinese) verification and the 初審 first-review reference are preserved; evidence_tier stays
  firm_summary (made_not_commenced provisions carry no operative resolution_text), and source.url is unchanged,
  so the cell stays non-citable and the ledger does not drift.
- **Time engine** (`scripts/compose.py`): Taiwan's base signal moves pre_regime → transition, so inbound edges
  are held at Category T and resolve to a channelled Category II on commencement, while origin edges stay
  Category III (enactment creates no exportable token). The origin-drag axis label gains an
  `enacted_not_commenced` case. South Korea is now the one remaining pre-regime origin; the pre_regime
  cross-check is {KR}. The TW commencement event drops its exportable_token effect accordingly.
- **Verification ledger** (`analysis/verification_ledger.json`): the TW issuer entry is synced to
  made_not_commenced / status_after transitional, url and applied_tier unchanged.

### Fixed — accuracy and version consistency
- **Version pointers**: the two working papers, `README.md`, `PACKAGE.md`, and the
  `apply_verification.py` ledger stamp now cite CBSR **v0.9.9** (the papers had lagged at v0.9.8, which
  predated the MiCA event they describe). Companion-work versions (Matrix v0.9.7, Architecture v0.2.8, Atlas
  v0.2.5) and all DOIs are unchanged.
- **Japan reserve relaxation** (`analysis/event_calendar.json`): Act No. 66 of 2025 effective date corrected
  13 Jun 2026 → **1 Jun 2026** (promulgated 13 Jun 2025; in force 1 Jun 2026), with the date_basis rewritten to
  the in-force framing and the same-day equivalence-recognition pathway noted as handled by conditioning.
- **Settlement substrate attribution** (`analysis/compatibility.json`, `analysis/open_questions.json`): per the
  flagship §5.2 correction, Project Ensemble is attributed to the HKMA (not BIS) and Project Agorá to the BIS;
  the generic "BIS wholesale-settlement" label is dropped.

### Hardening
- **New invariant T2b** (`run_invariants.py`): asserts every event's `trigger_kind` is defined in the
  `trigger_kind_legend`, locking the now load-bearing typology to its own legend (suite was 40 -> 41 checks; v0.9.9 completeness pass took it to 43, and the §4 sensitivity + §5.2 settlement layers to 45, and the round-4 coherence refinements (B2/B3) to 47).
- Em-dashes removed from the newly-authored data-field prose in `event_calendar.json` and the EU EMT
  `requirement_summary` (the shared "MiCA — Regulation (EU) 2023/1114" instrument identifier is left intact).
- The previously-flagged cosmetic V1/V2 label mismatch in `run_invariants.py` is resolved.

### Fixed — v0.9.9 completeness pass (propagating the class, not just the instance)
- **All Virtual Asset Service Act cells now share the enacted-not-commenced state** (`tw-frs-*`): the nine
  auxiliary VAS-Act dimension cells (reserve_backing, redemption, capital_requirements, distribution,
  permitted_activity_yield, securities_classification, bank_nonbank_routing, disclosure_reporting,
  monetary_sovereignty) move `proposed → transitional` / `pending_proposal → made_not_commenced`, matching
  `issuer_pathway`. Their prose moves from "DRAFT / NOT operative law" to "enacted at third reading 30 Jun
  2026, awaiting FSC subsidiary legislation, not yet commenced", and `source.primary` from "Draft Virtual
  Asset Service Act" to the enacted instrument. They remain non-citable (firm_summary, no resolution_text),
  so the citable subset stays 46, and none are in the ledger, so there is no drift. Unlike the UK, whose
  delegated cells rest on a *separate* still-in-consultation FCA instrument (correctly pending_proposal),
  these cells cite the *same* now-enacted Act, so they must move with it.
- **Base date advanced 2026-06-27 → 2026-06-30** (`analysis/event_calendar.json` `as_of_base`,
  `scripts/build_corridor_states.py` `BASE_DATE`, `scripts/compose.py`): the records encode the 30 June
  enacted state, so the compose base date must be 30 June for temporal coherence (otherwise compose reports
  Taiwan enacted three days early), and this aligns the base with the dateline stated in PACKAGE, both papers,
  and this changelog. Downstream: the JP event (1 Jun) stays in the baseline, MiCA (1 Jul) and UK (2027)
  stay future; the transition caveat is 8 at base → 0 at the 2027-10-25 horizon.
- **CITATION.cff** version `0.9.8 → 0.9.9` and date-released `2026-06-27 → 2026-06-30` — the
  machine-authoritative version (Zenodo/citation tools) that the earlier pointer bump missed.

### Hardening — the gates that make the above stick (round 3)
- **New invariant V3** (`run_invariants.py`): every version-declaring metadata file (CITATION.cff, README,
  PACKAGE, ledger) must agree with `EXPECT_VERSION`. This is the gate that bites on the CITATION.cff drift
  class — version pointers are now enforced, not merely kept in sync by hand.
- **New invariant B1** (`run_invariants.py`): no cell whose binding_status says its instrument is enacted
  (in_force_enacted / made_not_commenced) may describe that instrument, in its requirement_summary, as still
  un-enacted ("not operative law", "would take effect only on enactment", "draft provisions only", "status
  proposed", …). This bites on the "label says enacted, body says draft/bill" contradiction — the Taiwan
  class — so a green build can no longer hide it. It is a coherence gate, not the mere legend-enumeration
  T2b performs.
- **Two new negative tests** (`run_negative_tests.py`): `version-consistency` (rolls CITATION.cff back to
  0.9.8 and asserts V3 rejects it) and `binding-prose-coherence` (gives an enacted cell un-enacted prose and
  asserts B1 rejects it), added via an `invariants_fail` checker that rebuilds and then runs the invariant
  suite. The battery is now 7 build-gate tests + 2 invariant-gate tests = 9/9 biting; the invariant suite is
  47/47.

### Added — the two load-bearing analytical layers the papers call for (round 3)
- **Corridor-sensitivity layer** (`analysis/computed_sensitivity.json`, `scripts/build_sensitivity.py`):
  the §4 "load-bearing forward map" ordering, given machine support. For each pending trigger it counts the
  directed edges reclassified, split into fan-in and fan-out, derived edge-by-edge from the corridor states
  (no new facts). It reproduces the paper's headline — South Korea highest (a both-directions trigger, 20
  edges = 9 in + 11 out), the United Kingdom (8) and Taiwan (9) next, Mainland China insensitive — and it
  records the one place the mechanical count and the paper's ordering diverge (Taiwan's inbound fan of 9 is
  one larger than the United Kingdom's 8, yet the paper ranks the United Kingdom ahead on timing certainty
  and resolution class) as an explicit disagreement-as-finding, keeping both the paper rank and the mechanical
  fan rank. Exposed at `api/sensitivity.json`; gated by invariant **Sen1**.
- **Settlement-substrate bloc layer** (`analysis/computed_settlement.json`, `scripts/build_settlement.py`):
  the §5.2 correction built out from a removed false attribution into the checkable structural claim the paper
  asks for. It records the three experiments with their true operators — Project Agorá (BIS-led, G7-aligned,
  dollar-routing), Project Ensemble (HKMA-led, the bridge), and mBridge (no longer BIS since the 31 Oct 2024
  withdrawal, now PRC-and-Gulf-operated, digital-yuan-dominated) — assigns each of the twelve jurisdictions to
  its bloc-internal substrate, and computes the per-edge `infrastructure_overlap` over all 66 corridors
  (same-bloc / cross-bloc / Ensemble-bridge / off-experiments). Per §5.1/§5.4 it is emitted as
  `claim_class=tier2_operational` — softer, operational-enrichment evidence, explicitly not a proposition of
  law, and no feasibility-class conclusion in §§3-4 depends on it. Exposed at `api/settlement.json`; gated by
  invariant **Set1**, which also enforces the Tier-2 discipline so the §5.2 reading can never be mistaken for
  tier1_legal.

### Hardening — round-4 coherence and labelling refinements (make the gates airtight)
- **Settlement bloc label corrected** (`scripts/build_settlement.py`): the Agorá bloc is relabelled from
  "G7-aligned" to **"Agorá-participant (dollar-routing)"**. The membership was already right
  ({US, EU, UK, JP, KR, CH}), but Korea, Switzerland (and Agorá's Mexico) are not G7, so the "G7-aligned"
  shorthand was looser than the data; the accurate label is the set of Agorá participants on the
  dollar-routing rail, with the G7 anchor noted as approximate ("G7-anchored but not G7-only").
- **V3 now covers the two working papers** (`run_invariants.py`): the *original* version drift was
  papers-vs-metadata, so V3 now also checks the `Register (CBSR, vX.Y.Z)` string each paper cites — closing
  that class rather than only the CITATION/README/PACKAGE/ledger pointers.
- **B1 is no longer a lone blacklist** (`run_invariants.py`): its phrase list is expanded (conservatively —
  "if enacted" and "not yet in force" are deliberately excluded, since a CH cell references a future bill and
  a made_not_commenced provision is correctly "not yet in force"), and it gains two companions so coherence is
  enforced in both directions rather than by an ever-growing list of forbidden strings:
  - **B2** (positive companion): every `made_not_commenced` cell must AFFIRMATIVELY signal the
    enacted-but-not-commenced status somewhere in its text — a check a novel un-enacted phrasing cannot evade.
  - **B3** (symmetric, pending direction): every `pending_proposal` cell must signal its pending / not-yet-in-
    force nature, so a pending cell cannot read as already in force (the mirror of the Taiwan class). The UK's
    delegated cells pass it because they name the draft SI / consultation their pending status rests on — the
    round-3 finding that the UK mirror is not defective is thereby encoded as a live gate.
- **CN listed as the insensitive prohibition pole** (`scripts/build_sensitivity.py`): Mainland China has no
  pending positive trigger, so it never appeared as a what-if branch; but §4 discusses it explicitly as THE
  insensitive pole, so it is now listed with `edges_reclassified=0` and `reason="prohibition"` (Sen1 enforces
  its presence). The insensitive set now matches the paper rather than silently omitting the prohibition pole.

The invariant suite is now 47/47 (B2, B3 added; V3 and Sen1 widened); the negative-test battery stays 9/9.

### Added — continuous integration (restored)
- **`.github/workflows/build.yml`** was missing (the README and this changelog referenced it, but the file
  itself had been lost), so the cloud-side check was gone even though every gate still ran locally. It is
  restored and updated to the current living-artifact model: on every push and pull request it installs the
  pinned dependencies, regenerates the **computed** layer from source in dependency order
  (`compose → build → corridor_states → sensitivity → settlement → api → pages → site`), then runs
  `run_invariants.py`, `run_negative_tests.py`, and `check_readme_counts.py`, and finally asserts the derived
  artifacts are reproducible (`git diff --exit-code -I '"generated"'`, which ignores build timestamps so it is
  not date-flaky). It deliberately does **not** run `scripts/build_analysis.py` or `scripts/build_corridors.py`
  — those regenerate the hand-maintained analysis matrix and corridor edges and would revert them. This
  affects neither the DOI nor the data; it re-adds the automatic enforcement that an invalid record, a corridor
  that contradicts the matrix, or a stale derived artifact cannot be merged.

## [0.9.8] — 2026-06-29

> **Source-layer follow-through.** v0.9.7 verified the original-language regimes and updated the record
> cells. But the hand-authored higher-level source layers (the §5.14 compatibility matrix, the §3.3
> architecture typology, the constraint substrate, and the corridor edges) still carried the pre-42号
> framing of China and a few stale placeholders. v0.9.8 propagates the same verified facts up into those
> layers, so the matrix, the architecture, and the corridors no longer lag the records. No fact changes;
> this is consistency and currency.

### Changed — China 42号 now reflected across the source layers
- **§5.14 compatibility matrix** (`build_analysis.py`): the Category-III PRC prohibition axis now cites
  银发〔2026〕42号 (in force 6 Feb 2026, repealing the 2021 Notice; written overseas RMB-pegged-stablecoin
  issuance ban and extraterritorial-issuance ban) rather than describing the prohibition generically.
- **§3.3 architecture typology** (`build_analysis.py`): the PRC boundary description previously read "not by
  any single explicit prohibition". It now records that, as of Feb 2026, the boundary is anchored by an
  explicit written prohibition (42号), while distinguishing what remains genuinely emergent (the
  Direct-Subsidiary-via-Hong-Kong pathway, constrained by the data-sharing pattern rather than a categorical
  exclusion under the Stablecoins Ordinance).
- **Constraint substrate** (`analysis/constraint_substrate.json`): the CN C1 note no longer asserts the 2021
  "PBOC framework in force"; it cites 42号 as the operative prohibition and notes the 2021 Notice was
  repealed and the banned act broadened.
- **HK→CN blocked corridor** (`build_corridors.py`): the blocked-destination inbound mechanism now cites
  42号 (the written issuance prohibition) alongside the PIPL/DSL/CAC/SAFE data and capital rules.
- **Open question §7.2** (`build_analysis.py`): the PRC-boundary question is reframed around the Feb-2026
  written tightening (42号 marked RESOLVED as the tightening event), with the three relaxation paths kept as
  the still-open branch.

### Changed — corridor traceability
- **HK→BR corridor** (`hk-br-usd-stablecoin-settlement.yaml`): four `record_refs` that were empty
  placeholders ("forthcoming" / "GAP / target …") are now wired to the BR and HK records that exist after
  v0.9.7 (`br-vasp-cross_border_data-001`, `br-vasp-issuer_pathway-001`, `br-vasp-custody-001`,
  `br-vasp-reserve_backing-001`, `br-vasp-disclosure_reporting-001`, `hk-frs-securities_classification-001`).

### Added — invariants
- Six source-layer invariants (`run_invariants.py` D1–D6) assert that the matrix, the architecture, the
  substrate note, the HK→CN corridor, the HK→BR record_refs, and open question §7.2 all carry the 42号
  reality. The suite is now **39 invariants** (was 33); `run_negative_tests.py` remains 6 gates.

## [0.9.7] — 2026-06-28

> **Native-language official-text verification (CN Chinese, KR Korean, TW Chinese, BR Portuguese).** This
> closes the residual that v0.9.5 and v0.9.6 had explicitly flagged: the original-language jurisdictions
> needed a line-read against official text before their in-force cells could be cited. An external pass did
> that spadework; v0.9.7 applies it with the same discipline (resolution_text only where
> `binding_status==in_force_enacted` AND the proposition is confirmed against the official text of the cited
> instrument; prohibitions stay prohibition). Each material claim was re-verified against current primary
> sources before encoding.

### Added / Changed — Brazil (in-force regime confirmed; citable subset 36 → 46)
- The BCB regime (Lei 14.478/2022 + Res BCB 519/520/521, in force 2 Feb 2026; Res Conjunta CMN/BCB 14/2025 +
  Res BCB 517/2025 for capital; Res 521 FX reporting from 4 May 2026) is confirmed against the official
  Portuguese text. **10 BR cells promoted to `resolution_text`** against the official BCB normativo URLs with
  article-level pinpoints (e.g. Res 520 Art. 2 III: reserve = fiduciary currency + public debt of the same
  governments; Art. 4 modalities; Art. 20 routing).
- **BR C3 yield** (`br-vasp-permitted_activity_yield-001`): `binding_status` corrected `pending_proposal` →
  `in_force_enacted`. Res 520 (in force) prohibits credit offering and public fundraising except via share
  issuance and restricts client-asset use to staking / qualified-investor transactions. Held at
  `firm_summary` with an explicit note that the specific stablecoin yield **pass-through** question remains
  unsettled pending further BCB rulemaking.

### Fixed — China (material currency correction; substance unchanged)
- The cited 2021 Notice (银发〔2021〕237号) was **repealed** by 《关于进一步防范和处置虚拟货币等相关风险的通知》
  (银发〔2026〕42号), eight ministries, in force 6 Feb 2026 ("银发〔2021〕237号同时废止"). The operative-instrument
  citation across the CN cells now reads 42号.
- **CN C7** (`cn-prc-monetary_sovereignty-001`): the RMB-pegged-stablecoin prohibition is now **written,
  in-force law**, not "PBOC October 2025 verbal guidance". The cell carries the explicit clause (未经许可，
  境内外任何主体不得在境外发行挂钩人民币的稳定币) plus the extraterritorial issuance ban and RWA rules. The
  distribution and authority cells were reworded off the old "verbal guidance" framing. CN remains the
  prohibition pole: this is a provenance + currency correction, not a re-classification.

### Changed — Korea / Taiwan (procedural accuracy)
- **KR** (`kr-frs-implementation_status-001`): softened the over-precise "off the subcommittee (12 May 2026)"
  wording (sources show the DABA + three stablecoin bills remained in the 정무위 subcommittee in late Apr
  2026); added the won-stablecoin **51% issuer-eligibility dispute** (BoK favouring a bank-majority
  consortium) and the June-elections / committee-reconstitution delay. Stays `pending_proposal`.
- **TW**: recorded the native-language confirmation that the VAS Act passed the Finance Committee
  article-by-article first review (初審) on 3 Jun 2026 and went to the plenary (not yet third reading), and
  that it is procedurally **more advanced than KR's DABA**. The `kr-daba-enacted` and `tw-vas-act-enacted`
  contingent events now note their differing stages. TW stays `pending_proposal`.

### Engineering
- `apply_verification.py` is now fully idempotent on the `verification` block: a disposition that no longer
  asserts a verdict drops any stale block (its `against.url` would otherwise diverge from the new source).
  Caught by the verification-consistency gate; covered by a new negative test.
- **Cross-platform UTF-8 (Windows fix).** Every `Path.read_text()` / `Path.write_text()` across the build
  scripts now passes `encoding="utf-8"` explicitly, and each script reconfigures stdout/stderr to UTF-8
  (guarded). Previously `python build.py` on a non-UTF-8 console (e.g. Windows GBK/cp1252) raised
  `UnicodeDecodeError` on the first non-ASCII read, forcing a `python -X utf8 build.py` workaround. The full
  pipeline, build, and site now run end to end under a strict pure-ASCII locale, with the CJK/Portuguese
  text preserved. `python build.py` works without `-X utf8`.
- **Reproducible test scripts shipped.** The invariant suite and the negative-test battery were previously
  prose claims ("N invariants pass"). They now ship as two runnable scripts: `run_invariants.py` (33 read-only
  assertions; prints `33/33 invariants hold`) and `run_negative_tests.py` (proves the six validation gates
  bite by breaking each on a throwaway copy of the register; prints `6/6 gates bit`). This replaces the
  earlier ambiguous "11 / 18 invariants" wording with a single concrete, re-runnable count of 33.

## [0.9.6] — 2026-06-28

> **Verification follow-through: the time engine now holds the two closest-to-flipping events.** The
> v0.9.5 pass surfaced two regimes on the verge of changing the citability of their cells. v0.9.6 wires
> them into the event calendar as contingent "if enacted" branches, so that when each is enacted the
> dependent cells' `binding_status` flips automatically. This is what the time engine was built for.

### Added — time-engine forward events (4 → 6)
- **`us-clarity-act-enacted`** (contingent): the US **CLARITY Act** (H.R. 3633), reported to the Senate
  on 1 Jun 2026 and placed on the Senate Legislative Calendar as **Calendar No. 423**. Its effect, when
  enacted, flips `us-pss-bank_nonbank_routing-001` from `pending_proposal` to `in_force_enacted` and turns
  on the CLARITY Sec. 404 intermediary-yield and market-structure overlays carried as pending on the US
  yield, securities, and issuer cells. No fixed date (2026 passage is roughly even, and the practical
  window runs to the August recess), so it is contingent and moves no `compose(as_of)` horizon yet.
- **`sg-scs-legislation-enacted`** (contingent): Singapore's **SCS implementing legislation** (the MAS
  framework was finalised 15 Aug 2023; MAS announced at the Nov 2025 FinTech Festival that it was ready to
  draft; the framework is expected to take effect mid-2026). Its effect, when enacted, flips the eight
  `sg-scs-*` requirement cells from `finalized_policy_pending`/`transitional` to
  `in_force_enacted`/`in_force`.

### Fixed
- **EU C7 instrument label.** The `requirement_summary` and `source.primary` for
  `eu-emt-monetary_sovereignty-001` previously read bare "Article 23" while the v0.9.5 pinpoint was
  correctly **Art. 58(3)**. All three fields now read Art. 58(3) (which applies the Art. 23
  means-of-exchange thresholds mutatis mutandis to non-EU-currency EMTs), so the cell is internally
  consistent and matches the SIGNALS basis and corridor records.

### Changed
- **US C3 yield cell** (`us-pss-permitted_activity_yield-001`): recorded the live **Senate Banking
  Committee CLARITY substitute** development (advanced 15-9 on 14 May 2026; on Calendar No. 423 from 1 Jun
  2026). The Tillis-Alsobrooks compromise prohibits service providers from offering yield for merely
  holding a stablecoin balance but allows stablecoin rewards and activity-linked incentives. This is the
  intermediary-layer (Sec. 404) extension of the GENIUS issuer-level prohibition and supports the cell's
  standing position on user-initiated, activity-linked routing. Verified against current primary sources;
  noted as not-yet-law and cross-referenced to the new contingent event.

## [0.9.5] — 2026-06-28

> **The external verification pass landed — with discipline.** An external primary-source review (web
> retrieval against official instruments) was applied to the original-seven-jurisdiction cells via a
> `verification_ledger` audit trail. Its central finding became a new architectural axis: **citability is
> capped by the binding status of the cited instrument**, independent of whether the official text was
> located. A blanket promotion to `resolution_text` would have been wrong.

### Added
- **`binding_status` axis** (schema): a third evidence axis, orthogonal to `evidence_tier` (how
  well-sourced) and `claim_class` (legal vs operational) — the binding status of the instrument a cell
  rests on: `in_force_enacted` / `made_not_commenced` / `finalized_policy_pending` / `pending_proposal` /
  `prohibition` / `no_regime`. Set on **all 152 records** (explicit dispositions for the verified
  clusters; a status-based fallback elsewhere).
- **`analysis/verification_ledger.json`** — the audit trail of the external pass: per cell, the
  instrument, binding status, official URL, pinpoint, verdict, and the tier the disposition applied.
  Generated by `scripts/apply_verification.py`.
- **Build gate `check_binding_status`** — `resolution_text` requires `binding_status=in_force_enacted`;
  any made/policy/pending/prohibition cell is forbidden from `resolution_text`. This keeps the citable
  subset honest *even after* the text is located (UK SI 2026/102 is read, but not yet in force).
- **Build gate `check_verification_ledger`** — cross-checks every record against the committed ledger
  (binding_status, applied tier, official URL); a later hand-edit that drifts from the ledger fails the build.
- **MCP tool `verification_ledger(jurisdiction?)`** (27 → 28 tools); `binding_status` added to record summaries and `about()`.

### Changed — verification landed (citable subset 21 → 36)
- **EU (MiCA, in force):** `permitted_activity_yield` (Art. 50), `monetary_sovereignty` and
  `regulatory_authority` → **`resolution_text`** with the official EUR-Lex URL. `reserve_backing` held at
  `firm_summary` (the deposit-% is in the Level-2 RTS, not line-verified this pass).
- **US (GENIUS enacted; NPRM/CLARITY pending):** `permitted_activity_yield` (Sec. 4(a)(11)),
  `securities_classification` (the GENIUS carve-out), `reserve_backing` (the statutory 1:1, Sec. 4(a)(1))
  and `issuer_pathway` (the GENIUS part) → **`resolution_text`** (status corrected `proposed → in_force`),
  with the CLARITY/NPRM overlays flagged out of the citable proposition. `capital_requirements` and
  `bank_nonbank_routing` held at `firm_summary`/`pending_proposal` (OCC/FDIC NPRM and the CLARITY bill).
- **HK (Cap. 656, in force):** eight statutory cells (yield Sch. 2 s.15, 100% reserve + trust, par
  redemption, HK$25m capital, monetary sovereignty, issuer pathway, authority, distribution) → **`resolution_text`**
  with the official e-Legislation URL; HKMA-Guideline detail flagged as guidance.
- **SG (split):** the PS Act 2019 baseline (`aml_kyc`, `regulatory_authority`) recorded as
  `in_force_enacted`; the **SCS-specific cells** (reserve, redemption, yield, label scope, capital,
  distribution, monetary sovereignty) corrected to `status: transitional` + `binding_status:
  finalized_policy_pending` — finalized MAS policy, not enacted statute. `issuer_pathway` deliberately
  *not* downgraded to `proposed` (SG is a live regime, not pre-regime).

### Fixed
- **UK time-engine date (material):** the systemic-regime commencement event corrected from the modelled
  year **2027-01-01** to the gazetted day **2027-10-25** (SI 2026/102 full commencement), `precision: day`.
  Every date-aware UK verdict shifts ~10 months; `US→UK` now flips `T → I` at 2027-10-25.
- **EU C7 pinpoint:** the non-EU-currency EMT means-of-exchange cap re-pinned from bare **Art. 23** to
  **Art. 58(3)** (which applies Art. 23 *mutatis mutandis*), reconciling the cell with the SIGNALS basis
  and the corridor records.
- **UK records:** `issuer_pathway`/`regulatory_authority` status corrected `in_force → transitional`
  (the SI is made but not commenced).

## [0.9.4] — 2026-06-27

> **The edge layer, densified.** v0.9.2 made 124/132 directed edges *derivable*, but only **9** carried a
> rich corridor record — the rest were a bare class. v0.9.4 emits a **computed skeleton** for every other
> derivable edge: the structurally-derivable fields (feasibility class, inbound-mechanism test +
> administrator, baseline archetypes, directed interaction sets) with provenance, cross-checked against
> the signal `compose()`. The edge layer now has a record for **124/132** edges (9 rich + 115 skeletons).
> No new facts: the empirical fields (`infrastructure_overlap`, bespoke detail, curated archetypes, prose)
> are left explicitly unset as a per-edge enrichment backlog — the 9 hand-authored records remain the
> enriched gold tier.

### Added — computed corridor skeletons (edge-layer densification)
- **`scripts/build_edge_skeletons.py`** → **`analysis/computed_corridor_skeletons.json`** (schema
  `cbsr-analysis/computed_corridor_skeletons`): for each derivable directed edge without a hand-authored
  rich record, a skeleton carrying the derived **feasibility class** (from the substrate), the **inbound
  mechanism** `test` + `administrator` (re-projected from the destination's C1/C7 record), a **baseline
  archetype** set (full `[RC,SC,TC,DC]` for feasible, reduced `[RC,DC]` for blocked — matching the
  hand-authored HK→CN), the **directed interaction sets**, an origin-drag flag, and **provenance**.
- **115 skeletons**, so the edge layer now has a record for **124/132** edges. The 8 still without one are
  the non-origin-dragged edges *into the UK* (inbound gate in transition — the time engine's domain).
- **No new facts, doubly gated.** Every skeleton's class is **cross-checked** against the signal
  `compose()` (build fails on divergence), and every skeleton cites its backing **`tier1_legal`** records
  (build fails on a non-tier1/missing citation). Both gates verified with negative tests.

### Changed
- **MCP: 25 → 27 tools** — `edge_coverage` (rich vs skeleton vs indeterminate counts) and
  `corridor_skeleton(origin, destination)` (returns the rich record if one exists, else the skeleton).
  Site substrate panel gains an "edges with a record" coverage card. Version 0.9.3 → 0.9.4.
- Records/substrate/worklist/stakeholder figures unchanged (152; 80/96; 57; 63 profiles; citable 21) —
  this release densifies the edge layer with derived, provenance-backed skeletons, not new claims.

### Still open (v0.9.x → v1.0)
- The (external) **verification pass** on the 57 unverified cells — still the gate to `resolution_text`
  and to citable (rather than preview) corridors, skeletons, and profiles.
- **Enrichment** of the 115 skeletons into rich records: the empirical `infrastructure_overlap` (which
  multilateral settlement projects — Agora / mBridge / Ensemble — touch each corridor), bespoke inbound
  detail, and curated archetypes. This is per-edge factual work, distinct from the now-complete derived
  skeleton layer.

## [0.9.3] — 2026-06-27

> **Two things: the build now reproduces offline, and the Atlas §8 stakeholder projection ships.**
> A reviewer flagged that `build.py` hard-imported `jsonschema` while the validator shim lives outside
> the package by design — so an offline third party (no network, package not installed) couldn't
> reproduce the green build without hand-rolling a validator. Fixed: validation now **degrades
> gracefully** to a built-in, dependency-free structural validator (a faithful subset of Draft 2020-12)
> when `jsonschema` is absent, and the build prints which backend ran. Separately, the highest-leverage
> feature short of the verification pass — the **stakeholder projection** `profile_for(stakeholder, edge)`
> (Atlas §8) — is now built, with the §8 **Stakeholder Database** it reads from. It adds no new legal
> facts: it re-projects the already-derived corridor class and substrate poles through a persona's lens,
> cites the backing record for every line, and stays preview.

### Fixed — offline reproducibility of the build
- `build.py` now does `try: from jsonschema import Draft202012Validator except ImportError:` and falls
  back to a built-in `_FallbackValidator` covering exactly the keywords this repo's schemas use
  (`type`, `required`, `enum`, `const`, `properties`, `additionalProperties`, `items`, `allOf`,
  `if/then/else`). A fresh offline extract builds green; a CI box with `jsonschema` installed still gets
  full Draft 2020-12. The build line **`schema validation backend: …`** says which one ran. Verified the
  fallback still catches a bad enum and an unexpected field. `requirements.txt` keeps `jsonschema` as the
  declared dependency for the full-validation path.

### Added — Atlas §8 stakeholder projection
- **`analysis/stakeholder_database.json`** (schema `cbsr-analysis/stakeholder_database`): seven actor
  personas — issuer, distributor/wallet, reserve custodian, home regulator, host regulator, corporate
  treasury, institutional holder — each mapped to its lens, the C1–C8 constraints it reads (per side),
  and the corridor archetypes (RC/SC/TC/DC) it engages.
- **`scripts/stakeholders.py`** — `profile_for(stakeholder, origin, dest)` re-projects the derived
  corridor class + the origin/dest poles + the edge's inbound mechanism through a persona's lens, with a
  per-constraint reading (each line citing its backing record), the engaged archetypes, and a
  verification caveat. Emits **`analysis/computed_stakeholder_profiles.json`** — **63 worked profiles**
  (the 9 authored corridors × 7 personas).
- **No new facts, and provenance-gated.** Every projected line is read from an existing record; every
  profile cites its backing `tier1_legal` records; the build **fails** if any profile cites a missing or
  non-`tier1_legal` record. Profiles are preview and inherit the verification status of the cells they
  read — `profile_for` reports how many of the cited cells are not yet verified to `resolution_text`.
- **MCP: 23 → 25 tools** — `stakeholder_database` and `profile_for`. Site gains a **stakeholder-lens
  panel**: pick a corridor, see all seven personas' projections side by side.

### Changed
- Version 0.9.2 → 0.9.3. Record/substrate/worklist figures unchanged (152 records; substrate 80/96; 9/9
  authored corridors; 124/132 edges; worklist 57; citable 21) — this release adds a projection layer and
  a reproducibility fix, not new claims.

### Still open (v0.9.x)
- The (external) **verification pass** on the 57 unverified cells — still the only thing that promotes
  them to `resolution_text` and confirms the pole assignments (and, transitively, makes the stakeholder
  profiles citable rather than preview). Authoring the full **132-edge corridor records** (the edge layer
  is "computed-complete but rich-record-sparse": 124/132 classes derivable, but only 9 carry the full
  Atlas model — `inbound_mechanism`, `administrator`, `archetypes`, `infrastructure_overlap`).

## [0.9.2] — 2026-06-27

> **The substrate, lit up.** v0.9.0 shipped the constraint substrate but it could only derive **1 of 9**
> authored corridors, because most `(jurisdiction × constraint)` cells had no record and most poles were
> unset. v0.9.2 authors the **35 missing constraint cells** across all twelve jurisdictions and the
> corresponding poles, taking substrate coverage from **22/96 → 80/96** and corridor derivability from
> **1/9 → 9/9** (and **124/132** directed edges) — every definite result still cross-checked against the
> signal-table `compose()`. No verification was fabricated: the new cells are tiered `firm_summary` where
> the regime is established and `unset` (entering the verification worklist) where it is pre-regime or a
> prohibition. 152 records; citable subset unchanged at 21.

### Added — 35 constraint-cell records (full C1–C8 coverage for all 12 jurisdictions)
- Authored the holes in the cell matrix as faithful propositions of law from the corpus: the high-value
  **C1** (US, EU issuer eligibility — both were unrecorded) and **C7** (US, UK, SG monetary
  sovereignty), plus the long tail of **C4** (securities classification, 8), **C5** (bank/non-bank
  routing, 11), **C8** (disclosure/supervisory, 7), and a few **C3/C6**. Every `(jurisdiction ×
  constraint)` cell — all 96 — now has a backing record.
- **Tiering is honest, not inflated:** 25 cells are `firm_summary` (established regime, instrument +
  pinpoint, pending the official-text check) and 10 are `unset` (CN prohibition cells; TW/KR pre-regime
  cells), which raises the verification worklist from **47 → 57** `tier1_legal` cells. Nothing was
  promoted to `resolution_text`; the citable subset stays 21.

### Added — 58 substrate poles (coverage 22/96 → 80/96)
- Authored poles for the new and existing cells, each citing its `tier1_legal` record: **C1 for all
  12**, **C7 for the nine** non-transition/non-pre-regime jurisdictions, **C6 for all 12** (Set A
  input), and C2/C3/C4/C5/C8 for the established regimes. The 16 still-unset poles are the genuinely
  unsettled ones — **TW/KR pre-regime, UK C7 in transition, CN C5, BR C4** — where the substrate
  correctly returns `indeterminate` rather than guessing.

### Result — derivability, all still cross-checked
- **Authored corridors derivable: 1/9 → 9/9.** **Directed edges derivable: 124/132** (the eight
  indeterminate are the non-prohibited origins *into the UK*, whose inbound gate is in transition — the
  time engine's domain, not the substrate's). Newly-unblocked cross-region derivations include
  **US→EU = I**, **EU→US = II**, **US→JP = II**, **EU→HK = I**, **AE→EU = I** — all derived through the
  interaction-set rules and all matching the signal `compose()`.
- The build's **cross-check is now exercised across all 132 directed edges** (124 definite, all agree);
  substrate provenance remains clean (every pole rests on a `tier1_legal` record). All prior negative
  tests still pass.

### Changed
- 117 → 152 records; 108 → 143 `tier1_legal`. Site substrate panel shows the new coverage and the
  cross-region derivations. Version 0.9.1 → 0.9.2.

### Still open (v0.9.x)
- The (external) **verification pass** on the now-**57** unverified cells — still the only thing that
  promotes them to `resolution_text` and that confirms the authored **pole assignments** against the
  official text. The authored cells widen the substrate's *structure*; verifying them is what makes it
  *citable*. Authoring the full **132-edge corridor records** (distinct from the 124 derivable edges) remains.

## [0.9.1] — 2026-06-27

> **The verification pass, made real and honest.** v0.9.0's substrate is bounded by a backlog stated
> since v0.7: **47 `tier1_legal` cells are unverified** (`evidence_tier` unset), and every
> `compose()`/substrate result rests on them. The actual verification — confirming each claim against
> the official statutory text — is external work that requires primary sources and must never be
> fabricated. So v0.9.1 ships the **harness** that makes that pass safe, enforced, and scoped, not fake
> verifications: an earned-tier gate, a per-cell worklist, and an auditable verification block. No cell
> was invented; counts are unchanged (117 records, citable 21, substrate 22/96).

### Added — `evidence_tier` is now EARNED, not asserted
- New build gate `check_evidence_tier_requirements`: a record may only claim a tier it has the evidence
  for — `resolution_text` ⟹ `source.url` + `pinpoint` + `last_reviewed`; `mixed` ⟹ `url` + `pinpoint`;
  `firm_summary` ⟹ `pinpoint`. Necessary (not sufficient) conditions — the tier stays a human judgment,
  but can no longer be claimed without the corroborating provenance. All 117 existing records pass.
  *Negative tests:* claiming `resolution_text` without a `url` fails; a `verification.method` that
  contradicts the tier fails. Both restored.

### Added — the verification worklist (`analysis/verification_worklist.json`)
- `scripts/build_worklist.py` turns "47 unset" into a precise, per-cell, machine-readable checklist:
  for each unverified record, the instrument + pinpoint and exactly what is missing to reach each tier.
  Headline: **47 tier1_legal cells unverified, all lacking a `source.url`**, concentrated in
  **HK 10 · SG 10 · UK 10 · CN 8 · US 5 · EU 4** (JP/AE/CH/BR/TW/KR are already fully tiered — which is
  why JP is the substrate's most-derivable node), with **C2** (reserve/capital) the largest constraint
  bucket. Exposed by the new MCP tool `verification_worklist(jurisdiction?)`.

### Added — the `verification` block (schema) + a worked example
- New optional record field `verification` `{verified_by, verified_on, method (official_text |
  practitioner_corroboration), against {instrument, url, pinpoint}, excerpt?}` — the audit trail of HOW
  a cell was confirmed, enabling a safe, traceable promotion. Demonstrated by formalizing the
  provenance of an already-confirmed cell (`jp-epi-monetary_sovereignty-001`, the JP C7 pole behind the
  substrate's HK→JP = II derivation) — using the source already in the record, not new evidence.

### Changed
- MCP tools 22 → 23 (`verification_worklist`); the site's substrate section gains a **"Verification
  frontier"** line (the backlog as the inverse of substrate coverage). Version 0.9.0 → 0.9.1.

### Still open — the verification pass itself (genuinely external)
- Confirming the 47 cells against the official text (fetching each `source.url`, checking the pinpoint)
  is the work the harness now scopes and guards. It lifts substrate coverage past 22/96 and retires the
  liability — and it requires primary-source access, so it is not, and should not be, faked here.

## [0.9.0] — 2026-06-27

> **The composition problem gets a substrate.** v0.6–v0.8 computed corridor feasibility from a
> hand-curated per-jurisdiction *inbound gate* and dated it. v0.9.0 adds the deeper engine the thesis
> always pointed at: each jurisdiction's stance on the eight constraints (C1–C8) as a structured
> **pole**, and a `compose_via_substrate()` that derives a corridor's class by composing two
> jurisdictions' poles **through the six interaction-set rules** (§2.9), not by reading a single gate.
> This is feature #3 — built as a real, enforced, *additive* layer, deliberately **not** bundled with
> the full 132-edge expansion or the verification pass (those remain v0.9.x), to avoid trading depth for
> premature breadth. 117 records, 9 corridors; the prior layers are unchanged.

### Added — the constraint substrate (`analysis/constraint_substrate.json`)
- Each `(jurisdiction × constraint)` cell is a structured **pole** from a controlled vocabulary (per
  constraint), with attributes (`exportable_token`, `blocks_supervisory_sharing`, `supervisory_sharing`)
  and a `derived_from` list of the **`tier1_legal` records it is transcribed from**. A pole exists only
  where a record backs it; absent cells are unset.
- **22/96 cells populated** today — the honest coverage frontier. Cells are missing (e.g. US/EU C1
  were never recorded) or `tier1_legal`-but-unverified (the 47-cell backlog), which is exactly why most
  corridors are not yet substrate-derivable.

### Added — `compose_via_substrate()` and the derivation artifact (`analysis/computed_substrate.json`)
- `scripts/substrate.py` implements the interaction-set rules: origin drag (C1 `exportable_token`);
  destination inbound from C7×C1 (Set D reserve×monetary-sovereignty, Set C bank/non-bank×issuer —
  `prohibition`→blocked, `channelled`→II, `usage_capped`/`open`→I); and the **Set A** overlay (C1×C6:
  if the origin's data-sovereignty blocks supervisory sharing, destination issuer eligibility is
  unsatisfiable → escalate to III). It returns **`indeterminate`** (with the missing poles) where a
  load-bearing pole is unset — it never guesses.
- **Worked result:** the fully-backed **{HK, CN, JP}** triangle derives cleanly and is cross-checked
  against the signal-table `compose()` — **HK→JP = II** (via Japan's *channelled* C7), **JP→HK = I**
  (via Hong Kong's *open* C7), and the CN edges `blocked`/III — all derived from constraint poles, all
  agreeing with the signal engine. **1/9 authored corridors** (hk-cn) is currently derivable.

### Added — enforcement (the discipline extended one level deeper)
- `build.py` loads and validates both substrate artifacts (schema tags; pole-vocabulary; every pole has
  a `derived_from`). **Substrate provenance** is enforced: a pole backed by a non-`tier1_legal` record
  fails the build. The **cross-check** is enforced: where the substrate yields a *definite* class it
  must equal the signal-table `compose()`, else the build fails (a real divergence must be declared).
  *Negative tests:* a pole backed by a `tier2_operational` record fails; flipping a pole so the derived
  class diverges from the signal engine fails. Both restored.

### Added — MCP tools (20 → 22) and site
- `constraint_substrate(jurisdiction?, constraint?)` and `compose_via_substrate(origin, destination)`
  (computes live for any pair, returns the per-set verdicts, the cross-check, or `indeterminate` with
  the missing poles). `about()` reports the substrate.
- The static site gains a **"Feasibility, composed from constraints"** section: the coverage stats and
  the worked {HK, CN, JP} triangle with per-edge interaction-set verdicts.
- Version bumped 0.8.0 → 0.9.0.

### Still open (explicitly scoped to v0.9.x — the backlog the substrate is bounded by)
- Populate the remaining constraint cells and **run the primary-source verification pass on the 47
  `unset` `tier1_legal` cells** — the only thing that lights the substrate (and retires the standing
  liability under every `compose()` result). Extend the corridor layer toward the Atlas's full
  **132-edge** matrix. Promote `operational_notes` to per-predicate tier as cells gain structure.

## [0.8.0] — 2026-06-27

> **The composition problem gets a clock.** v0.5–v0.7 made corridor feasibility *computable*; v0.8.0
> makes it *dated*. `compose(origin, destination, as_of)` applies every scheduled change in law
> effective by a date and re-runs the Atlas algorithm, so an edge can read one class today and another
> once a regime is operative. This is feature #1 from the three-feature plan, sequenced after the
> evidence split (#2) precisely because a date-aware verdict must distinguish a change in *law* from a
> change in the *market* — which the v0.7 `claim_class` axis now lets it do. 117 records, 9 corridors,
> 66 pairs; no records removed; the computed (non-temporal) layer is unchanged (9/9, 64/66).

### Added — the event calendar (`analysis/event_calendar.json`)
- Dated and contingent **changes in law** that move a jurisdiction's `compose()` signal, with three
  statuses: **`scheduled`** (an effective_date, applied by `compose(as_of>=date)`; may carry
  `precision: year` where only the operative year is known), **`contingent`** (a bill with no firm
  date — never applied by date, only surfaced as a pending "if enacted" branch), and **`in_force`**
  (already effective). Four events ship: the UK systemic/conduct regime (scheduled, 2027), the Taiwan
  VAS Act and the Korea DABA (contingent), and Japan's Act 66/2025 full enforcement (in force, no
  compose effect — included to show the calendar distinguishes a change in law from a change in
  feasibility class).
- **Every event is `claim_class: tier1_legal`, backed by `tier1_legal` records — enforced.** A market
  launch can never be an event (those live in a record's `operational_notes`). This is the v0.8.0
  inheritance of the two-axis discipline into the time dimension.

### Added — date-aware compose + the timeline artifact (`analysis/computed_timeline.json`)
- `signals_as_of(date)` in `scripts/compose.py` applies scheduled/in-force events ≤ date; `compose()`
  and the undirected reduction are now parametrised on a signal set. `edge_timeline(origin, dest)`
  computes today's class, the dated transitions that change it, and contingent "if enacted" branches.
- `computed_timeline.json` records per-corridor timelines, **illustration edges** (the authored nine
  don't touch the UK, where the headline transition is), and the undirected agreement + the count of
  **transition-caveated pairs** over time.
- **The headline result, stated honestly:** the directed edge **US→UK is Category T today and Category
  I as of 2027** (the systemic regime operative), and the regime-in-transition caveat on UK pairs
  resolves (**8 caveated pairs → 0** at the 2027 horizon). The `EU-UK` and `UK-US` undirected pairs
  **remain findings after 2027** because their residual is *structural* — the Atlas scores live-live as
  `I/II` while §5.14 authored them as cleanly bridgeable `I` — not temporal. The engine separates a
  regime-in-transition artifact (resolves by date) from a genuine modelling difference (does not).

### Added — MCP tools (18 → 20)
- `compose_corridor(origin, destination, as_of?)` gains an optional `as_of` (returns the as-of class
  plus the base class and whether it changed); new `event_calendar(jurisdiction?)` and
  `corridor_timeline(origin, destination)`. `about()` reports the temporal capability.

### Added — enforcement & site
- `build.py` loads and validates `event_calendar.json` and `computed_timeline.json` (schema tags;
  event `claim_class`/status/date rules; **event-provenance** — a backing record that is not
  `tier1_legal` fails the build). *Negative tests:* an event backed by a `tier2_operational` record
  fails; a contingent event carrying a date fails.
- The static site gains a **"Feasibility over time"** section: the headline, per-edge timelines
  (today → dated transition; contingent "if enacted" branches), and the event calendar.
- Version bumped 0.7.1 → 0.8.0.

## [0.7.1] — 2026-06-27

> **Claim-purity fix for the citable subset.** v0.7.0 shipped the lawyer-citable subset at *record*
> granularity. Review found a real, shipped consequence of that choice: `jp-epi-distribution-001` is a
> genuinely citable record (its load-bearing claim — the EPIESP inbound rule — is a proposition of
> law), but it had bundled a Tier-2 operational illustration (the USDC / SBI VC Trade admission, with
> launch dates) into its `requirement_summary`, `requirement_structured`, `source.primary`, `pinpoint`,
> and `interpretation_note` — so that market fact, and a product-approval element inside the instrument
> string, were projected under a "citable law" badge by `citable_law('JP')`. The record-level tag was
> defensible; the leak was that a record-level projection cannot drop operational material from *inside*
> an otherwise-legal record. This release fixes that by relocating operational material to a dedicated
> Tier-2 field and forbidding it in citable instrument strings — without prematurely building the full
> per-clause substrate (that is v0.9.0). 117 records, 9 corridors, citable subset still 21; no records
> removed, no tier reclassified.

### Added — `operational_notes` (the Tier-2 home a legal record needed)
- **New optional schema field `operational_notes`**: an array of `{ note, as_of?, source? }` for Tier-2
  operational/market illustrations attached to a record (a launch, a registration, a working example).
  It sits *outside* the load-bearing legal fields, is **omitted from the citable projection**
  (`citable_subset` / `citable_law`), and is rendered on the site as a clearly-labelled "Tier-2 · not
  citable as law" block so the fact is preserved, not deleted. This is the per-record capability the
  v0.7.0 design anticipated for operational facts in legal dimensions, now used on the case that needs it.

### Changed — the two contaminated citable records cleaned
- **`jp-epi-distribution-001`**: `requirement_summary`, `requirement_structured`, `source.primary`
  (now `Payment Services Act (Electronic Payment Instruments regime)`), `pinpoint`, and
  `interpretation_note` reduced to the legal claim; the USDC / SBI VC Trade admission (approval
  2025-03-04, launch 2025-03-26) moved to `operational_notes` with its SBI source. Still citable — now
  cleanly.
- **`jp-epi-permitted_activity_yield-001`**: the reported intermediary-layer lending instance (SBI VC
  Trade / USDC, reported launch 2026-03) moved out of `requirement_summary`/`requirement_structured`
  into `operational_notes`; the legitimate open tension stays in `interpretive_flag`. Its projected
  fields were already clean; this aligns the summary with the new rule.

### Added — enforcement (so the leak cannot regress)
- **`check_citable_purity()` in `build.py`** (hard error): a citable record's `source.primary` and
  `pinpoint` must cite the legal instrument only — no product/market **event** (`launch`, `admission
  via`, `went live`, `rolled out`, …) and no named commercial counterparty (SBI VC Trade, Circle,
  Progmat, …). Deliberately conservative: legal verbs (`admitted via registered EPIESP`) and case
  citations (`SEC v. Howey Co., 328 U.S. 293`) do **not** trip it. *Negative test:* re-bundling the
  USDC/SBI approval into the instrument string fails the build; restored cleanly.

### Documentation
- METHODOLOGY and taxonomy document `operational_notes` and the claim-purity rule. The README evidence
  section and the ROADMAP now state plainly that the **47 still-`unset` `tier1_legal` cells** are the
  quiet liability under every `compose()` "64/66" result — only the verification pass retires it, not
  any single feature — and make explicit *why* the time/event engine (v0.8.0) is the correct next major
  step ahead of the constraint substrate (v0.9.0). Version bumped 0.7.0 → 0.7.1.

## [0.7.0] — 2026-06-27

> **A second evidence axis, and the lawyer-citable subset.** Until now a record's `evidence_tier`
> said how well-sourced it was, but nothing in the schema said *what kind of claim* it was — a
> proposition of law a lawyer could cite, or a market/operational fact like a product launch. v0.7.0
> promotes the Corridor Atlas §7 Tier-1 (primary-source legal) vs Tier-2 (market-reported operability)
> distinction into the schema as a required, orthogonal `claim_class` field, and uses the two axes to
> define and **enforce** the lawyer-citable subset: `tier1_legal` + `in_force` + `resolution_text` =
> **21 records**. This is the load-bearing change the time/event engine (v0.8.0) and the constraint
> substrate (v0.9.0) depend on — a date-aware or constraint-level verdict must distinguish legal facts
> from operational ones. 117 records, 9 corridors, 66 pairs; no records removed.

### Added — the `claim_class` axis (orthogonal to `evidence_tier` and `status`)
- **`claim_class` is now a required schema field**, enum `tier1_legal` / `tier2_operational`.
  `tier1_legal` = a proposition of law (what a binding instrument requires/permits/prohibits, citable
  to the instrument); `tier2_operational` = a market/operational fact (what is live, who is registered,
  what launched, rails/liquidity), read as-of-dated. It is independent of `evidence_tier` (provenance
  strength) and `status` (in force vs draft): a confirmed launch is well-sourced but not law; a draft
  provision is a legal claim but not binding.
- **All 117 records tagged** via the idempotent `scripts/retag_claim_class_v0_7_0.py`: **108
  `tier1_legal` + 9 `tier2_operational`** (the `implementation_status` dimension, which reports market
  state). The field is per-record, not derived from the dimension, so a future operational claim inside
  a nominally-legal dimension can be tagged explicitly. Corridors carry no `claim_class`.

### Added — the lawyer-citable subset (the highest-value view for the core audience)
- **`citable_subset` in `dataset.json`**: the intersection `tier1_legal` + `in_force` +
  `resolution_text` (**21 records**), each projected to instrument + pinpoint + official URL + filter
  definition, so consumers don't re-derive it.
- **`citable_law(jurisdiction?, dimension?)` MCP tool** (tool count **17 → 18**) returns that subset
  with optional filters — the "show me only what I could cite" view. `citable_law('CH')` → 6;
  `citable_law('TW')` → 1 (the in-force AML layer only; the draft VAS Act is excluded by status).
- **Static-site "citable law only" toggle**, plus a `claim_class` column and filter, citable-`§`
  markers on the matrix dots, claim/tier badges and the official-URL link in the record inspector.

### Added — enforcement (so the subset can't silently drift)
- **`check_citable_integrity()` in `build.py`** (hard error): a `tier1_legal` record at
  `resolution_text` or `mixed` asserts official-text confirmation, so it **must** carry a `source.url`;
  a `resolution_text` record **must** also carry a `source.pinpoint`. A citable record cannot ship
  without a locator to the official text.
- **Signal-provenance discipline in `scripts/compose.py`** (`check_signal_provenance()`): every
  per-jurisdiction signal the `compose()` engine reads must rest on `tier1_legal` records; a signal
  resting on a `tier2_operational` fact is a build-failing violation. The computed layer now derives
  feasibility only from propositions of law — the inheritance hook for v0.8.0/v0.9.0.

### Changed
- **`COVERAGE.md`** gains a `claim_class` × `evidence_tier` count matrix and a "citable cells" block.
- **Record summaries from the MCP server** (`_summary`) now include `claim_class` and `evidence_tier`;
  `about()` reports the evidence model and the citable count.
- **`record.schema.json`** description, the static-site methodology card, the "for agents" note, and
  the roadmap updated for the two-axis model. Version bumped 0.6.0 → 0.7.0 across `build.py`,
  `CITATION.cff`, and the site.

### Integrity (unchanged invariants, re-verified)
- 117 records valid, 9 corridors, 66 compatibility pairs; computed layer reproduces **9/9** corridors
  and **64/66** §5.14 categories; the 2 findings remain under `uk_regime_in_transition`; pre-regime
  cross-check `{KR, TW}` consistent; signal provenance clean. Negative tests: stripping a citable
  record's URL fails the build; flipping a signal-driving record to `tier2_operational` fails the build.

## [0.6.0] — 2026-06-27

> **From a queryable mirror to a self-checking, computable graph.** v0.5.x stored the Architecture's
> analysis and the Atlas's corridors as two independent transcriptions, linked by a
> `compatibility_pair` foreign key but never reconciled — so **7 of 9 corridors had interaction sets
> that silently contradicted the §5.14 matrix row they pointed to**, and the matrix was an authored
> lookup table, not a computed output. v0.6.0 closes both gaps: cross-layer integrity is now enforced,
> corridors have a real schema, and a `compose()` engine *derives* feasibility and diffs it against the
> authored values. 117 records, 9 corridors, 66 pairs; no records removed.

### Added — cross-layer integrity (the highest-value, cheapest fix)
- **`check_cross_layer()` in `build.py`** asserts, for every corridor carrying a `compatibility_pair`:
  (1) its `compatibility_category` **equals** the §5.14 row's category (hard error otherwise), and
  (2) if its `interaction_sets` differ from the row's, it **must** carry a `divergence` field
  declaring and explaining the difference — else the build fails. CI runs it on every push.
- The **7 silent contradictions are now 7 declared divergences.** Each diverging corridor carries a
  `divergence` block (`against_pair`, `pair_interaction_sets`, `edge_interaction_sets`, `reason`)
  auto-derived in `scripts/build_corridors.py` from the live matrix, so it can never drift. `hk-us`
  and `hk-br` match the matrix exactly (no divergence). The `us-eu` self-contradiction (field `[A,C,D]`
  vs a secondary note reading "B, D") is resolved: secondary citations that listed an interaction-set
  tail are sanitised to point at the `divergence` field.

### Added — corridor schema (the corridor layer was unvalidated)
- **`corridor.schema.json`**, enforced by `build.py` like the node schema. One schema, two validated
  shapes via a `schema` discriminator: `corridor/v3-directed-edge` (the flat Atlas edge) and
  `corridor/v2-rich` (the deeply-verified leg-by-leg `hk-br` analysis). The rich `hk-br` corridor was
  brought under the schema (given `origin`/`destination`/`feasibility_class`/`compatibility_pair`/
  `interaction_sets` while keeping its `boundary_analysis`/`watch_list`).
- The local validation shim gained `const` / `allOf` / `anyOf` / `oneOf` / `if`-`then`-`else` so local
  and CI validation agree on the conditional shape requirements.

### Added — the computed layer (compose(): the composition problem as a running function)
- **`scripts/compose.py` → `analysis/computed_compatibility.json`.** A small, auditable rule engine
  derives each pair's feasibility from a **per-jurisdiction signal table** (regime status, inbound-gate
  type, exportable-token, egress override — each annotated with the justifying node record) using the
  Atlas's own algorithm (origin drag, then destination-determined class), and **diffs computed-vs-
  authored**:
  - reproduces **9/9** authored directed corridors and **64/66** §5.14 categories from first principles;
  - the `pre_regime` set derived from the signals (`{TW, KR}`) matches the set read directly off the
    records (`issuer_pathway.status == proposed`) — an internal consistency cross-check enforced by
    `build.py`;
  - the **2 disagreements are a finding, not a bug**, clustered under one cause: `uk_regime_in_transition`
    (EU-UK, UK-US) — the Atlas flags the UK as not operative until 2027 while the Architecture's §5.14
    treats those pairs as cleanly bridgeable Category I. This is exactly the cross-document divergence
    the engine exists to surface.
- The computed layer is a labelled **preview** (not asserted authoritative), embedded under
  `analysis.computed` in `dataset.json`, reported in the build output and `COVERAGE.md`.
- **Three new MCP tools** (17 total): `compose_corridor(origin, destination)` and
  `explain_feasibility(origin, destination)` (the first *computing* tools, not retrieval), and
  `verification_report()` (the verification queue).

### Changed
- **`COVERAGE.md`** gained a **Computed layer** section (agreement stats + findings) and a
  **Verification queue** section (the `unset` legacy backlog by jurisdiction — the declared next pass).
- **`BUILD_NOTE_v0.5.0`** §4/§5 reconciled with current data: a superseded banner makes clear its
  "resolution_text 0 / url 10/117" and "does not promote tier" statements describe **v0.5.0 only** and
  were superseded by the v0.5.1 verification pass (the authoritative figures live in the generated
  `COVERAGE.md`). The audit's "build note misstates its own data" finding is closed.
- CI gained a `compose.py` step (analysis → corridors → compose → build → site); the drift-check already
  covers `analysis/` (incl. the computed file) and `dataset.json`.
- Version bumped to **0.6.0**; landing-page roadmap updated.

### Still open (declared, not hidden)
- The corridor layer is **9 of 132** edges (the full directed matrix remains the next breadth step).
- The **51 `unset` legacy records** (US/EU/UK/SG/HK/CN/BR) still lack `evidence_tier` and `source.url`;
  they are the largest backlog and are now itemised in the verification queue.
- `compose()` is a **preview** over a deliberately small rule set; it is not a complete derivation of
  §5.14, and its computed values are labelled as such.

---

## [0.5.1] — 2026-06-27

> **Primary-source verification pass (CH, AE, TW, JP, KR).** Official-language primary `source.url`
> links added across the five v0.4.0 focus jurisdictions, with English secondary citations where an
> official English text exists, and `evidence_tier` upgraded **only where the official text confirms
> the point**. The honest result: live-regime jurisdictions move substantially to `resolution_text`;
> pre-regime jurisdictions get their in-force layer verified while their draft regimes stay flagged.
> No records added or removed; 51 of 56 new-jurisdiction records updated (the five `cross_border_data`
> records were left untouched — local data-protection law was outside this pass's scope).

### Evidence-tier movement (the 56 CH/AE/TW/JP/KR records)
- **`source.url` populated: 10 → 61 / 117** across the register.
- **`resolution_text`: 0 → 23** · **`mixed`: 0 → 14** · **`firm_summary`: 66 → 29** (the remaining
  `unset` 51 are the older seven-jurisdiction records that predate the `evidence_tier` field).
- Per jurisdiction: **Switzerland** 6 `resolution_text` / 5 `mixed` / 1 `firm_summary`; **UAE** 7 / 3 / 1;
  **Japan** 8 / 2 / 1; **Taiwan** 1 / 2 / 8; **South Korea** 1 / 2 / 8.

### Verified against official primary texts (→ `resolution_text`)
- **Switzerland** — Banking Act (BankG, SR 952.0) and Banking Ordinance (BankV, SR 952.02) on Fedlex,
  plus **FINMA Guidance 06/2024**: the regulatory authority, the issuer pathways including the
  bank-default-guarantee exemption (**BankV Art. 5 para. 3 let. f**), the no-fixed-reserve-schedule
  guarantee model, the permitted-but-guaranteed yield posture, the all-holder AML identification rule,
  and the absence of a non-domestic-currency cap.
- **United Arab Emirates** — CBUAE **Payment Token Services Regulation (Circular 2/2024)** (English
  authoritative): the regulator and licence/registration split (incl. **Art. (2)6** AED carve-out,
  **Art. (8)8**), the **Art. (22)** reserve requirement, the **Art. (12)3** holder-yield prohibition,
  the **Art. (2)4(b)/(2)5/(2)7(b)** monetary-sovereignty *channel* restriction (distinct from the
  separate **Art. (12)4** aggregate-limit power), the **Art. (2)13** free-zone carve-out, and the
  implementation timeline — with VARA Annex 1 (FRVA Rules) and the ADGM FSRA FRT framework (effective
  1 Jan 2026) cited for the free-zone pathways.
- **Japan** — Payment Services Act (Act No. 59 of 2009) via e-Gov Law Search, with the official English
  on Japanese Law Translation: the FSA authority, the closed issuer trichotomy + EPIESP intermediation,
  the no-holder-yield rule, the ¥1,000,000 funds-transfer per-transfer cap, the FATF Travel Rule, and
  the channelled-admission posture (USDC via SBI VC Trade, EPIESP registration 4 Mar 2025).
- **Taiwan** — the in-force **AML layer only**: the Money Laundering Control Act + VASP AML Registration
  Regulations (in force 30 Nov 2024), via law.moj.gov.tw.
- **South Korea** — the in-force **user-protection / AML layer only**: the Virtual Asset User Protection
  Act (Act No. 20372, in force 19 Jul 2024) via the Korea Law Information Center + the FSC commencement
  notice, and the Travel Rule under the Specified Financial Transaction Information Act.

### Confirmed-but-pending (→ `mixed`)
Points whose core is confirmed against the official text but whose operational detail awaits subordinate
rules or a separate figure: e.g. **Japan**'s Act No. 66 of 2025 trust-type 50% reserve relaxation (statute
enacted; Cabinet orders take full effect 13 Jun 2026), capital-by-entity-type figures (CH/AE/JP), Swiss
redemption / securities-classification (CISA boundary) / distribution / implementation (the FinIA reform
consultation and the 8 Apr 2026 CHF sandbox are flagged as proposed/pilot), and the TW/KR
authority + implementation records (in-force layer confirmed; issuance regime draft).

### Kept honest (→ stays `firm_summary`, official **bill** URL only)
All draft issuance/reserve/capital/yield/redemption/monetary-sovereignty/distribution provisions for the
**Taiwan Virtual Asset Service Act** (Executive Yuan bill) and the **South Korea Digital Asset Basic Act**
(bill No. 2210736) — `status: proposed`, not operative law, **not upgraded**. The five `cross_border_data`
records (Swiss FADP, UAE, Japan APPI, Taiwan PDPA, Korea PIPA) were outside this pass and are unchanged.

### Notes
- **Official-language-only flags.** Taiwan (Chinese) and South Korea (Korean) have no official English
  translation of the binding texts; those records carry the official-language primary URL and a note to
  that effect (FSC/regulator English materials are summaries). Japan attaches the Japanese Law Translation
  English as secondary; the UAE and Switzerland (FINMA) publish authoritative/official English.
- Each updated record carries a `v0.5.1_verification` tag plus one of `resolution_text_verified` /
  `mixed_partial_verified` / `draft_url_added`, and its provenance note states the verification outcome.
- `COVERAGE.md`'s "What ✅ means" caveat and the landing-page provenance item were updated to describe the
  three-tier state after the pass.
- Version bumped to **0.5.1**.

---

## [0.5.0] — 2026-06-27

> **Analysis layer + corridor layer + audit hardening.** This release answers the standing gap
> that the register encoded the Compliance Matrix *node* layer at high fidelity but left the
> Cross-Border Stablecoin Architecture working paper's *analytical* payload — the composition-problem
> apparatus — living only in PDF prose. That payload is now queryable data. The single worked
> corridor becomes a directed-edge **layer**. Every concrete finding from the external audit is
> addressed. **117 records, 9 corridors, 66 compatibility pairs.** No records removed.

### Added — the analysis layer (the headline change)
- **`analysis/compatibility.json`** — the **§5.14 pairwise compatibility matrix** encoded in full:
  all **66** unordered pairs of the twelve jurisdictions, each with `category` (I dual-authorization /
  I/II hybrid / II partnership / III composition-problem-unresolved), the operative `interaction_sets`
  (A–F), a `category_iii_axis` where applicable (prohibition / pre_regime / prohibition+pre_regime /
  counterparty_conditional), and a binding-constraint `note`. Category distribution: 34 I/II, 30 III,
  2 pure I — matching the source. Includes the three-axis summary observation.
- **`analysis/interaction_sets.json`** — the **six constraint-interaction sets** (§2.9): constraint
  pair, joint-binding mechanism, worked example.
- **`analysis/architectural_patterns.json`** — the **three-pattern PRC typology** (§3.3: direct
  subsidiary / partnership distribution / separated-entity, each with constraints and viability
  conditions), the portable **three-layer routing architecture** (§4/§6: Layer 1 compliant issuer,
  Layer 2 user-directed routing, Layer 3 yield-bearing fund), the **§4.4 five-factor operational
  test**, and the **six design principles**.
- **`analysis/open_questions.json`** — the **open questions** (§7.1–§7.5) with conditional-status flags.
- **`analysis.schema.json`** — a published JSON Schema for the analysis-layer artifacts (the
  "standard, not a table" ethos extended to the analysis layer).
- **`scripts/build_analysis.py`** — builds the four artifacts and self-checks that all 66 C(12,2)
  pairs are present. `build.py` reads and **structurally validates** them (schema tags; 66 pairs;
  valid categories, interaction sets, and jurisdictions) and folds them into `dataset.json` under
  `analysis`, so a single fetch delivers the node layer and the analysis layer together.
- **Four new MCP tools** (`mcp_server.py`): `compatibility(jurisdiction?, other?, category?)`,
  `interaction_sets()`, `architectural_patterns()`, `open_questions()`.
- **Landing-page compatibility matrix** (`build_site.py` → `index.html`): an interactive 12×12 grid,
  colour-coded by category, click a cell for the pair's category, interaction sets, and binding
  constraint. Renders from the embedded snapshot, so it works offline.

### Added — the corridor layer (1 → 9 directed edges)
- **`scripts/build_corridors.py`** emits **eight directed corridor edges** transcribed from the
  Corridor Atlas v0.2.3 §5 deep-dives: `us-eu`, `eu-us`, `us-hk`, `hk-us`, `sg-hk`, `hk-cn` (blocked),
  `us-jp`, `jp-us` — joining the existing `hk-br` anchor for **nine** corridors. Each carries
  feasibility class, compatibility category (linked to §5.14), live archetypes (RC/SC/TC/DC),
  operative interaction sets, infrastructure overlap (Agorá / mBridge / Ensemble), inbound mechanism +
  administrator, and any origin-override flag. The **directional asymmetry** is explicit (e.g. US→EU is
  Category I but EU→US is Category II via the §18 comparability gate; HK→CN is blocked at destination).

### Added — CI
- **`.github/workflows/build.yml`** runs `build_analysis.py`, `build_corridors.py`, `build.py`, and
  `build_site.py` on every push and pull request, and fails if derived artifacts are out of sync —
  turning "validated against schema" from a promise into an enforced guarantee.

### Changed — audit hardening
- **`COVERAGE.md` (legal-reader transparency).** `build.py` now emits an explicit **"What ✅ means"**
  caveat (✅ = sourced + schema-valid + no `<VERIFY` marker + human-passed pinpoint; **not** "checked
  against the official gazette text") plus an **evidence-tier breakdown** (`resolution_text` /
  `firm_summary` / `unset`, and the count of records with a populated `source.url`). The landing-page
  methodology item was rewritten to the same two-tier framing. This directly addresses the audit's
  central legal caveat that ✅ over-reads as official-text verification.
- **Repository hygiene.** The one-shot migration builders (`_build_v0_4_0.py`, `_build_v0_4_0_part2.py`,
  `_backfill_v0_3_0.py`) moved from the root into **`scripts/`** (root de-cluttered; `build.py` still
  finds all `*.yaml`).
- **Metadata fixes.** Schema `$id` changed from the `example.org` placeholder to the canonical
  `…github.io/stablecoin-rail-register/record.schema.json`. `CITATION.cff` now carries the real
  **ORCID `0009-0005-6762-084X`** and an SSRN author identifier (previously a commented-out
  placeholder). `LICENSE` / `LICENSE-DATA` titles updated to "Cross-Border Stablecoin Register (CBSR)".
  README adds a **"Name & identifiers"** note explaining that the `stablecoin-rail-register` slug,
  GitHub Pages URL, and schema `$id` are retained deliberately for URL/DOI/identifier stability while
  the canonical *name* is CBSR.
- **CN re-pin.** The nine `cn-prc-*` records, which still cited Compliance Matrix **v0.9.3** by page
  number, were re-pinned to **v0.9.6** by section label (the v0.9.3 page numbers are stale in the
  repaginated twelve-jurisdiction edition), with a `[re-pinned from v0.9.3]` note and the
  `from_matrix_v0.9.6` tag preserving provenance.
- Dataset/version bumped to **0.5.0** (`build.py REGISTER_VERSION`); `index.html` roadmap updated
  (v0.5.0 shipped; primary-source verification pass is v0.5.x; the full 132-edge corridor matrix is
  v0.6.0).

### Deliberately *not* done
- **No mass promotion of `firm_summary` → `resolution_text`, and no machine-written `source.url`s.**
  Promoting evidence tier or writing source URLs without reading each pinpoint against the official
  text would violate the project's own methodology (no machine-generated citations). That work is the
  v0.5.x verification pass and remains human-gated. The honest fix shipped here is **transparency**
  (the ✅-semantics caveat and the evidence-tier breakdown), not a verification claim the data does not
  yet support.
- **The full 132-edge corridor matrix** is not loaded; nine high-demand edges are. Depth before breadth.

---

## [0.4.0] — 2026-06-27

> **Twelve-jurisdiction expansion.** The focus set grows from seven to twelve jurisdictions.
> **Switzerland (CH), the United Arab Emirates (AE), Taiwan (TW), Japan (JP), and South Korea
> (KR)** are added as full focus jurisdictions, transcribed from the maintainer's *revised*
> research substrate: the **Multi-Jurisdiction Stablecoin Compliance Matrix v0.9.6** (the
> node-level data substrate) and **Cross-Border Stablecoin Architecture v3 (Eight Constraints,
> Twelve Jurisdictions, Three Architectural Patterns)**, with the **Cross-Border Digital-Finance
> Corridor Atlas v0.2.3** as the directed-edge companion. **117 records across 12 jurisdictions,
> 1 corridor** (56 records added; none removed). As with all transcription passes, no citation is
> machine-generated: each record carries its primary instrument + pinpoint from the Matrix v0.9.6
> entry (cited as secondary provenance) and joins the primary-source verification queue
> (`evidence_tier: firm_summary`).

### Added
- **Switzerland — 12 records** (`ch-frs-*`): the survey's "regulation-without-a-statute" regime.
  Records capture the two issuer pathways (banking/FinTech licence vs the **bank default-guarantee
  exemption** under Banking Ordinance Art. 5(3)(f)); the absence of a statutory reserve schedule
  (the guarantee, covering **principal + interest**, is the protective mechanism); the **permission-
  cluster** yield posture (holder yield permitted but structurally constrained — the register's
  clearest counter-anchor to the EU/HK/US prohibition on the C3 spine); the **CISA** securities-
  characterization boundary (C4); the strictest AML posture in the survey (FINMA Guidance 06/2024 —
  identify **every** holder including intermediate holders; anonymous transfers prohibited); **no**
  monetary-sovereignty cap (C7); and the FinIA-amendment reform track (consultation closed 6 Feb
  2026) plus the six-bank CHF sandbox (8 Apr 2026).
- **United Arab Emirates — 11 records** (`ae-pt-*`): the **federal-versus-free-zone split** (CBUAE
  PTSR, Circular 2/2024 onshore; VARA / ADGM-FSRA / DIFC-DFSA free zones). Records capture the DPT/FPT
  issuer pathways and the **AED-issuance carve-out** for free zones (C1); the onshore yield prohibition
  vs the ADGM promotion-based line (C3, the survey's closest non-US analogue to GENIUS "solely"); and
  the **monetary-sovereignty channel restriction** (C7) — foreign tokens excluded from general onshore
  payments, **a usage-channel restriction, not an aggregate cap** (Matrix Tier-2 correction).
- **Taiwan — 11 records** (`tw-frs-*`): promoted from a forthcoming window to a full jurisdiction. The
  **AML-registration layer** (amended Money Laundering Control Act + VASP Registration Regulations,
  in force 30 Nov 2024) is `status: in_force`; the draft **Virtual Asset Service Act** issuance,
  reserve, capital, yield, redemption, monetary-sovereignty (peg **NTD vs USD undecided**), and
  distribution provisions are carried as `status: proposed`, `draft_provision`-tagged (committee first
  review 3 Jun 2026; no enactment date).
- **Japan — 11 records** (`jp-epi-*`): the live **Electronic Payment Instruments** regime (Payment
  Services Act, in force 1 Jun 2023) as amended by **Act No. 66 of 2025** (trust-type backing relaxed
  to ≤50% short-term low-risk assets). Records capture the **closed issuer trichotomy** (bank /
  funds-transfer / trust) with EPIESP intermediation (C1); the issuer-layer yield prohibition with the
  SBI VC Trade USDC lending service as the intermediary-layer boundary case (C3); the **¥1,000,000**
  funds-transfer per-transfer cap; and the **channelled-admission** C7 posture (foreign tokens admitted
  via a registered EPIESP holding reserves in Japan — JPYC live 27 Oct 2025; USDC via SBI VC Trade Mar
  2025).
- **South Korea — 11 records** (`kr-frs-*`): **pre-regime**, analytically paired with Taiwan. The
  **Virtual Asset User Protection Act** (in force 19 Jul 2024) and the AML/Travel-Rule framework are
  `in_force`; the pending **Digital Asset Basic Act** issuance provisions are `status: proposed`
  (won-stablecoin issuance effectively prohibited; eligibility contested **BOK ≥51% bank consortium
  vs FSC fintech-inclusive**; draft FX-means-of-payment classification of cross-border won stablecoins
  — comparison by effect to Brazil's câmbio reclassification). Consolidated bill off the subcommittee
  agenda 12 May 2026; H2 2026 passage goal flagged uncertain.
- **Two new monetary-sovereignty (C7) archetypes** are now represented in the dataset alongside the
  EU quantitative cap, the HK professional-investor restriction, and the PRC prohibition: the **UAE
  usage-channel restriction** and the **Japan channelled-admission** model — sharpening
  `compare_dimension('monetary_sovereignty')` into a five-archetype spectrum.

### Changed
- **Schema (`record.schema.json`).** `jurisdiction` enum extended from 8 to 12 codes
  (added **CH, AE, JP, KR**; TW was already present). `description` updated to reference the
  twelve-jurisdiction substrate and Compliance Matrix v0.9.6. The change is additive (backward-
  compatible): all existing records remain valid.
- **`roadmap.yaml`.** `focus_jurisdictions` is now the full twelve; `backfill_jurisdictions` cleared
  (the focus set equals the substrate). Planned (`⬜0.4.x`) cells re-scheduled and added for the new
  jurisdictions (`securities_classification`, `custody`, `disclosure_reporting` gaps).
- **`mcp_server.py`.** `JURISDICTIONS` map extended to the twelve so `jurisdiction_profile` /
  `list_jurisdictions` resolve full names for the new codes.
- **`README.md`, `ROADMAP.md`, `taxonomy.md`, `CITATION.cff`, `index.html`** synced to the
  117-record / 12-jurisdiction state (coverage table, focus list, depth counts, status v0.4.0).
  *(`index.html` regenerated via `build_site.py`; `dataset.json` / `COVERAGE.md` / `records.md`
  regenerated via `build.py`.)*
- Dataset/version bumped to **0.4.0** (`build.py REGISTER_VERSION`).

### Pending verification
- All 56 new records are `evidence_tier: firm_summary`: the load-bearing facts are corroborated by
  the maintainer's Compliance Matrix v0.9.6 (whose added entries carry a Tier 1 / 1b / 2 / 3
  verification note), but the **article-level pinpoints and `source.url`** were not read against the
  official primary instruments in this pass. The v0.4.x verification pass will promote confirmed
  records to `resolution_text` and populate clause-level URLs. Draft-law provisions (TW, KR) are
  explicitly flagged `status: proposed` so they are not mistaken for operative law.
- **Confidence** is set conservatively: `high` for well-corroborated in-force facts (authority,
  issuer pathway, in-force status of mature regimes), `medium` for nuanced/contested points, and
  `low` for draft figures that diverge across sources (e.g., KR minimum capital).

---

## [0.3.2] — 2026-06-23

> **In-place correction — 2026-06-25 (no version bump; dataset/DOI remain 0.3.2).**
> An independent primary-source pass against the official Res 520/521 DOU text (and EUR-Lex for
> the MiCA cross-reference) surfaced four article-level / attribution errors that had propagated
> across the corridor, several Brazil records, and the companion-paper insertions. Corrected in
> place; `dataset.json` / `COVERAGE.md` / `records.md` / `index.html` regenerated (61 records, 1
> corridor — none added or removed; five Brazil records + the corridor changed).
>
> - **`Art. 76-A` attribution.** Prior drafts cited "Lei 14.286/2021 Art. 76-A". Art. 76-A is a
>   provision **inserted into Resolução BCB 277/2022** by Res 521 (new "Título VIII-A"), **not** an
>   article of Lei 14.286/2021. Legal authority is Lei 14.286 (recital: arts. 2–6, 10, 14, 15, 18;
>   chiefly Art. 5) with Art. 7-V of Lei 14.478/2022. Fixed in the corridor, `cross_border_data`,
>   and the Architecture/Matrix/build-sheet insertions.
> - **`Art. 88` de-conflated from the Travel Rule.** Res 520 Art. 88 is the **authorisation
>   adjustment period** (270-day "período de adequação"; internal-controls / cybersecurity /
>   Law 13.810/2019), not the Travel-Rule/AML hook. Travel Rule = Art. 44 + Art. 89 (phase-in).
>   Fixed in `aml_kyc`, `custody`, the corridor, and the Matrix entry.
> - **IOF status.** The prior corridor note said "IOF-Câmbio 3.5% CONFIRMED to apply." The câmbio
>   classification creates the **fato gerador**, but **no levy is in force** — collection is the
>   Receita Federal's competence and no Receita instrument exists as of Jun 2026 (a 3.5% extension
>   is in consultation vs a 1.1% "private foreign currency" characterisation). Corridor now aligns
>   with the Matrix/Architecture "unresolved" framing.
> - **Reporting label.** "DeCripto" is not in the resolution; the in-text Art. 82-A schedule label
>   is **Anexo II-A** (appended to Res 277/2022). "DeCripto" (a future Receita label; current
>   reporting is IN 1888) dropped. Fixed in `disclosure_reporting`, the corridor, the Matrix entry.
>
> Also: Travel-Rule phase-in dates made explicit (**domestic by Feb 2027**, international by
> **2 Feb 2028**, Art. 89); the MiCA cross-reference clarified rather than deleted in
> `monetary_sovereignty` (Art. 23 for ARTs; Art. 58(3) extends it to non-euro EMTs — verified
> against EUR-Lex); and the Tier-2 verification blocks re-cut into three tiers
> (confirmed-against-text / corrected / still-open) in the Matrix and Architecture insertions.
> Items still in Tier 3 (Art. 64+ pinpoint, ~5% carve-out, "reasonable assurance" wording, Res 561
> Art. 56-A/56-B, CVM Parecer 40 number) remain firm-summary-sourced.

### Fixed
- **Brazil minimum-capital figure corrected.** The Compliance-Matrix Brazil entry previously
  reported SPSAV minimum capital as **R$1m–3m (~USD 181,500–544,500)**. That range was the
  **rejected 2024 public-consultation (CP 109/110) proposal**, not the binding regime. The
  operative minimums are **R$10,800,000–R$37,200,000**, set by **Resolução Conjunta CMN/BCB
  nº 14/2025** and **Res BCB 517/2025** (both 3 Nov 2025), scaled by activity/modality (BCB
  press conference, 10 Nov 2025; ANBIMA summary). The Matrix caveat now explicitly warns against
  citing the R$1–3m figure as operative.

### Added
- **`br-vasp-capital_requirements-001`** — gives Brazil a `capital_requirements` (C2) record
  (closing a dimension gap vs the other focus jurisdictions) and lodges the corrected figure in
  the structured dataset, not only in paper prose. Tagged `evidence_tier: firm_summary` /
  `confidence: medium` pending confirmation of the per-modality breakdown against the
  Res. Conjunta 14/2025 text. Brazil depth 9 → **10**.

### Changed
- Dataset/version bumped to **0.3.2** (`build.py REGISTER_VERSION`); README status and CITATION.cff
  updated. *(index.html regenerated via `build_site.py`.)*

---

## [0.3.1] — 2026-06-23

### Added
- **Brazil promoted from corridor-only to a full focus jurisdiction** — **9 sourced, schema-valid
  records** (`regulatory_authority`, `issuer_pathway`, `reserve_backing`, `custody`,
  `disclosure_reporting`, `cross_border_data`, `monetary_sovereignty`, `aml_kyc`,
  `securities_classification`). Built from primary BCB sources via the HK→BR corridor fieldwork:
  Res BCB 519/520/521 (pub. 10 Nov 2025; in force 2 Feb 2026; audit/reporting from 4 May 2026) and
  Res BCB 561/2026 (eFX; in force 1 Oct 2026), on the base of Lei 14.478/2022 + Decreto 11.563/2023,
  with the FX limb under Lei 14.286/2021 and the securities taxonomy under CVM Parecer de Orientação 40.
- **First populated `disclosure_reporting` (C8) cell** in the register (Brazil) — Res 520 biennial
  independent audit + proof-of-reserves, and Res 521 Art. 82-A monthly BCB reporting (from 4 May 2026).
- **Totals: 60 records, 7 focus jurisdictions; verified cells 51 → 60; planned cells 18 → 13.**

### Changed
- **Corridor `hk-br-usd-stablecoin-settlement-001` corrected and verified.** Material fix: the HK
  leg's "Anchorpoint USD-pegged FRS" was wrong — Anchorpoint issues **HKDAP (HKD At Par)**; both
  first-cohort licences (FRS01 Anchorpoint, FRS02 HSBC) are HKD-referenced and **no USD FRS is
  licensed**. This reconciles the corridor with `hk-frs-issuer_pathway-001`, the Compliance Matrix,
  and Architecture §5.6 — and sharpens the HK eligibility constraint (USD coins must run offshore-FRS
  → permitted offeror → professional investors). Also: added Lei 14.286/2021 as the FX hook;
  de-conflated the two 30 Oct 2026 deadlines and added the 31 May 2027 eFX-provider deadline;
  sharpened IOF (IOF-Câmbio 3.5% confirmed + Receita Federal consultation); folded in C8,
  foreign-custody, the BCB/CVM split, and the eFX USD 10k cap.
- `roadmap.yaml` — Brazil moved from `backfill_jurisdictions` to `focus_jurisdictions`; Brazil
  planned-cell block cleared (now built). Taiwan remains parked.
- `taxonomy.md` — Brazil reclassified from corridor-only to focus.
- Dataset/version bumped to **0.3.1** (`build.py REGISTER_VERSION`). *(README.md and CITATION.cff
  version strings should be bumped to match on tagging.)*

### Pending verification
- Most BR records are `confidence: high` with primary-instrument URLs populated (official BCB
  normativos + corroborating firm analysis: Cescon, BDO, Global Legal Insights, Notabene, Chainalysis,
  CoinDesk). Residual clause-level items still flagged **inside** records, to confirm against the
  official DOU/BCB text: Res 520 segregation/audit article numbers and the "reasonable-assurance"
  wording; the ~5% own-asset liquidity carve-out and foreign-custodian conditions; Res 521's exact
  amended-resolution numbers (277/278/279) and the "Annex II-A" label; Lei 14.286/2021 Art. 76-A;
  and Res 561 Art. 56-A/56-B with the 31 May 2027 date. `custody` stays `confidence: medium` pending these.

### Post-review tightening (2026-06-23, within 0.3.1 — not a new tag)
- **Two-tier evidence marker added.** New optional schema field `evidence_tier`
  (`resolution_text` | `firm_summary` | `mixed`), independent of `confidence`. All 9 BR records set
  to `evidence_tier: firm_summary`: the load-bearing **facts** (caps + trigger, algorithmic ban +
  reserves, biennial audit, eFX ban + USD 10k, dates, IOF 3.5%) are corroborated across multiple
  independent firm/practitioner sources, but the specific **article numbers/labels** (Res 520 Art.
  4/44/88/89, Art. 64+; Res 521 Art. 82-A; "DeCripto"/"Annex II-A"; Lei 14.286/2021 Art. 76-A; Res
  561 Art. 56-A/56-B; CVM "Parecer 40") rest on those summaries and were **not** read against the
  official BCB normativo text in this pass. Overclaiming tags (`primary_source_verified_2026-06`)
  and per-record "verified to article level" notes were softened accordingly. *(Done under a local
  schema-validation shim because the sandbox had no network to install `jsonschema`; the author
  should run the real `python build.py` as the final gate.)*
- **Monetary-sovereignty framing tightened to match the register.** Pattern 2 (Matrix) and §5.8
  (Architecture) no longer say Brazil "neither caps nor prohibits": Brazil imposes a per-operation
  cap (itself a quantity limit), so the **novelty is the reclassification of the stablecoin leg as
  an FX (câmbio) operation**, not the absence of a cap. The "third monetary-sovereignty model"
  claim is now anchored on FX-channelling, where it is robust.
- **C7-mapping motive caveat added** to `br-vasp-monetary_sovereignty-001`, Matrix Pattern 2, and
  Architecture §5.8: the structural effect is comparable to the EU's monetary-sovereignty
  mechanism, but the BCB's stated motive emphasises FX-market integrity / traceability /
  balance-of-payments (dollarisation a stated concern), not the EU's explicit currency-protection
  rationale — comparison by effect, not legislative intent.
- **Stablecoin-share figure given as a range.** `br-vasp-monetary_sovereignty-001` no longer asserts
  a single "~90%": estimates range ~67–90% by metric/period; flagged to lock to one dated source
  before citing as primary.
- **As-of stamps.** Corridor gains `valid_as_of` + a `phase_in_note`; both paper insertions carry an
  explicit "as of June 2026; provisions phase in through Feb 2028" stamp **in the prose** (not only
  the editorial header), so a 2027 reader knows to re-verify.

## [0.3.0] — 2026-06-17
Archived to Zenodo — **DOI [10.5281/zenodo.20733274](https://doi.org/10.5281/zenodo.20733274)**.

### Added
- **Singapore, the United Kingdom and Mainland China deepened** to 11 / 11 / 9 dimensions
  (from 2 / 3 / 5) — **51 records total, 14 of 15 dimensions populated**. Transcribed from the
  maintainer's Compliance Matrix v0.9.3 (cited as secondary provenance).
- **`custody` dimension** populated for the first time (UK 24-hour custody rule).
- **MCP server** (`mcp_server.py`) — typed query tools over the dataset (`query`,
  `compare_dimension`, `jurisdiction_profile`, `search`, `coverage`, …) for agent access.
  See [`MCP_SERVER.md`](MCP_SERVER.md).
- **Sortable, multi-filter table view** on the landing page, alongside the coverage matrix.
- **Brazil and Taiwan** added as forthcoming jurisdiction *windows* on the landing page and in
  the roadmap (planned cells; no records yet).
- This `CHANGELOG.md`.

### Changed
- **Renamed** from *Stablecoin Rail Register* to **Cross-Border Stablecoin Register** — the name
  foregrounds the cross-jurisdictional differentiator and drops payments-vendor jargon ("rail").
  Updated across `README.md`, `CITATION.cff`, the dataset, the schema, the landing page, and the
  MCP server.
- `README.md` coverage snapshot, `ROADMAP.md`, and `roadmap.yaml` synced to the 51-record state.

### Pending verification
- Clause-level `source.url` is not yet populated. Each record carries its primary instrument and a
  pinpoint, sourced to the Compliance Matrix v0.9.3; **no citation is machine-generated**. Records
  are pending the primary-source verification pass (visiting each instrument to confirm the
  pinpoint and capture the canonical URL). The Hong Kong anchor cells are the first target (v0.3.x).

## [0.2.0] — 2026-06-17
### Added
- Dimension framework expanded **10 → 15**: split `reserve_backing` / `capital_requirements`;
  added `securities_classification`, `bank_nonbank_routing`, `monetary_sovereignty`,
  `disclosure_reporting` — giving two doctrinal spines.
- Six focus jurisdictions loaded as **30 sourced, schema-valid records** (US, HK, EU, UK, SG, CN).
- Dual-license: CC-BY-4.0 (data) + Apache-2.0 (code).
- Archived to Zenodo — **DOI 10.5281/zenodo.20730359**.

### Changed
- Jurisdiction set reoriented to the verified written substrate (Brazil → corridor-only;
  Taiwan parked).

## [0.1.0]
### Added
- Initial scaffold: `record.schema.json`, methodology, build pipeline, controlled vocabulary,
  and a corridor worked example. Spine dimension (`permitted_activity_yield`) seeded for Hong Kong
  and US §404.
