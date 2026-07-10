# CBSR corridor layer — eighth independent review (over v0.9.98)

_Independent re-audit of the directed-132 corridor layer, its toolchain, and the four companion
papers, over the v0.9.98 release. Every tool was re-run in a clean Python 3.12 environment with the
network off (the zero-dependency claim was tested for real); all 132 edges were inspected; the class
compression and the CD1 arithmetic were reproduced; the twelve load-bearing facts were re-checked
against primary sources; and a set of data probes (Appendix B) backed each new finding. Review date:
2026-07-08. Reviewer: independent, no relationship to the author._

One-line verdict: **engineering is flawless — runs, byte-reproducible, SHA true, every gate bites,
the backlog is genuinely public. The semantics are still one notch optimistic, and three of the flaws
are new to this review — including that the single rule deciding 25% of the edges has no legal
provenance and contradicts the package's own published classification scale.**

## What v0.9.99 does with this review

| finding | severity | disposition in v0.9.99 |
|---|---|---|
| **NF-1** origin-drag-first vs the Atlas's destination-first (III=33, `TW/KR→CN` = III + "prohibited") | major / P0 | **documented + lint `m7`** (fires on the two edges); `--strict` now **RED** by design. Not silently reclassified (a deliberate rule, cascades through OD1/CD1). Reconcile upstream — `PAPER_ERRATA.md` NF-1. |
| **NF-2** §4.2 sensitivity ranking (TW & KR tied at 20; CN not insensitive) | major / P0 | **documented** — `PAPER_ERRATA.md` NF-2 (paper-side; also auto-fixed by resolving NF-1 via option (a)). |
| **NF-3** origin-drag driven by a `tier2` market signal in `PROPOSAL_signal_table.md` | major | **fixed in the proposal**: split `token_regime` (tier1, drives class) / `token_in_issue` (tier2, enrichment); documented the outbound-US consequence E1 omits. |
| **NF-4** the 9 `→TW` edges' contingent event `tw-vas-act-enacted` (enactment already happened) | major | **fixed in the artifact** (renamed to `tw-vas-act-commencement`) + new hard check **`TL1`**. |
| **F-TW-2** Taiwan administrator understates the CBC (co-approver, not consultee) | — | **fixed in the artifact** (`FSC + CBC (dual approval)`). |
| **F-US-1 / F-JP-1 / F-EU-2 / F-EU-3** paper facts | — | **documented** (errata + VB-08); **VB-03 closed**. |
| **NF-5 / NF-6** three-axis emptiness, schema slack, check non-independence | minor | **documented** (extends findings A/C). |

The artifact changed this release (NF-4 + F-TW-2), so the SHA moved to
`9898d230b902d55177d78d5750278c296d6cd792a6a9e608586eed7aa2b492e2`; it still reproduces byte-for-byte
from the v0.9.92 snapshot, and `out/` still regenerates byte-for-byte.

## The three new findings, in full

### NF-1 (P0) — the rule deciding 25% of the map contradicts the published Atlas, optimistically

Corridor Atlas v0.2.5 and Feasibility §3.9 are **destination-first**: *"Every edge terminating in the
People's Republic of China is, and remains, blocked at destination"*; *"27 edges are Category III."*
The artifact applies **origin-drag-first without exception**, so III = 33 and inbound-CN is
`{blocked: 9, III: 2}`. The two excess edges, `TW→CN` and `KR→CN`, are `class_code = III` (labelled
*"partnership / coordination route"*) while their own `inbound_mechanism.test` reads *"Issuance and
circulation prohibited."* A single edge asserting both that a workaround exists and that issuance is
banned — and in the **optimistic** direction, the only place in the whole package where the data makes
a corridor look *more* open than the law allows.

Three gates that ought to catch it do not, and the reason is structural: `OD1` encodes origin-drag-first
as *"the declared canonical ordering"* (it treats the rule as an axiom, so it cannot flag the rule);
`CD1` records the deviation as an *"origin drag on the CN/TW/KR mutual edges"* **declared delta**,
laundering a **rule reversal** into the same ledger as the genuine "Taiwan enacted" fact update; and
`CF1`'s anchor is scoped to *token-holder-origin* inbound edges, so the primary-source-confirmed fact
`CN = blocked` (VB-04) never reaches `TW→CN` / `KR→CN`. The anchors all fall on the same side of the
rule.

v0.9.99 adds **lint `m7`** (a Category III edge whose `inbound_mechanism` asserts a prohibition), which
fires on exactly these two edges and turns `--strict` **red**. The rule itself is a genuine modeling
decision that cascades through the classifier, so it is left for the author to reconcile
(`PAPER_ERRATA.md` NF-1, options (a)/(b)) rather than silently rewritten downstream — but it is no
longer invisible.

### NF-2 (P0) — the sensitivity ranking is arithmetic, and the arithmetic is wrong

§4.2 calls Korea *"the single highest-sensitivity jurisdiction."* Recomputed (Appendix B): Taiwan's
commencement and Korea's legislation each reclassify **20 edges** — tied. §3.3 itself says Taiwan's
enactment "operationalizes no signal," so Taiwan's both-directions trigger is still pending at Korea's
scale; §3.3 and §4.2 contradict each other. And "Mainland China is insensitive" is false under the
artifact's rule (`KR→CN`, `TW→CN` flip `III→blocked` when Korea/Taiwan gain tokens) — a contradiction
that **disappears** the moment NF-1 is fixed via destination-first, which is itself an argument for
that fix.

### NF-3 (major) — the official fix embeds the violation it claims to close

`PROPOSAL_signal_table.md` is this repo's P2 design "closes F1/F2/F6 and the poison." But its earlier
draft drove origin-drag from a `token_holder` signal whose `record_ref` was `node/*#issuer-market`
with `binding_status: in_force` — a **market** record. *Citable by Construction* §4.2's signal-provenance
gate makes a class-driving signal resting on a `tier2_operational` fact a **build-failing violation**,
and the artifact's `provenance.basis` self-certifies "every driving signal is tier1_legal." So the fix
embedded the very violation it exists to close, on the signal that decides **33/132 edges (25%)**.

v0.9.99 corrects the proposal: origin-drag reads `token_regime` (tier1_legal); `token_in_issue` is a
no-`binding_status` enrichment that must not touch `class_code`. And it documents the consequence the
reviewer's *reductio* exposes: the **only** thing keeping the US/UK **outbound** edges out of `III`
today is the market signal (USDC / GBP e-money issuers exist). Switch origin-drag to a legal signal and
— depending on whether it fires on "no authorizable regime" or "regime not in force" — the US and UK
outbound edges can collapse to `III`. So **`PAPER_ERRATA.md` E1 is incomplete**: it moves the 8
inbound-US edges to `T` but is silent on the outbound-US edges, tacitly relying on the market signal.
The author must decide the origin-drag semantics and apply it in **both** directions before `SIG1` can
go green.

### NF-4 (major, fixed) — a contingent trigger named after an event that already happened

The 9 `→TW` transition edges carried `as_of_timeline.contingent = [{event_id: "tw-vas-act-enacted",
status: "contingent", ...}]`. Per Feasibility §2.1 a *contingent* trigger is one whose enactment has
**not** happened — but Taiwan's enactment happened on 2026-06-30 (`VB-R1`, confirmed); the pending fact
is **commencement**. A machine reading `status=contingent, event_id=tw-vas-act-enacted` would infer the
Act is unpassed, contradicting the same edge's `inbound_mechanism` ("enacted 2026-06-30") and the
premise `DG2` relies on. Two fields, opposite answers, no cross-check. **Fixed**: the event is renamed
`tw-vas-act-commencement`, and new hard check **`TL1`** forbids a contingent event named after a
completed act (a negative test confirms `TL1` bites).

## The facts (twelve re-checked against primary sources)

All twelve load-bearing facts hold. Highlights and the corrections:

- **Confirmed:** Taiwan third reading 2026-06-30 + issuer-yield prohibition (VB-R1); GENIUS §20
  earlier-of effective date (VB-06); CLARITY 15-9 / Calendar 423; Gallego+Alsobrooks (VB-01); MiCA
  Art. 143(3) outer date 2026-07-01; BIS mBridge exit 2024-10-31; **Japan Act No. 66 promulgated
  2025-06-13 (VB-03 closed)**; Japan foreign-stablecoin recognition Ordinance in force 2026-06-01.
- **F-US-1:** §3.2 "GENIUS is in force" is wrong (it was not, on the snapshot) — folds into E1/VB-06.
- **F-JP-1:** the recognition Ordinance was promulgated 2026-05-19 / in force 2026-06-01, and §5.3
  omits its operational conditions — equivalence + audited reserves + **home-regulator information-
  sharing with the JFSA** (the hardest gate, and the one that most strengthens the §5.2/§5.3 thesis).
- **F-TW-2 (fixed):** Taiwan issuance needs **FSC + CBC** approval; "FSC (CBC consulted)" understated it.
- **F-EU-2 (→ VB-08):** §3.10's per-country grace table and the "ESMA 2026-04-17 no-extension" date
  carry no `record_ref` and conflict across secondary sources (Lithuania 6 vs 12 months; Poland
  "closed" vs "never opened" — it has no national MiCA law; ESMA's formal statement is 2024-12-17).
- **F-EU-3:** §3.10 "only Circle's USDC/EURC hold EMT authorisation" is stale — soften to "including."

## Q1 / Q2 briefly

- **Q1 (complete):** no, and beyond C1 there is an **expressive** gap — the six-way trigger typology
  the paper claims as a contribution has only two slots in the schema (`scheduled` / `contingent`), so
  five kinds (enacted-not-commenced, scheduled-with-cap, intra-regime-gating, parameterization, the
  open compositional question) cannot be expressed; and the three-axis evidence model has one axis
  present at 6% coverage — `claim_class` and `binding_status` are **not even schema fields**, and no
  edge carries a `record_ref`. So the lawyer-citable intersection is *undefined*, not merely empty, at
  this layer.
- **Q2 (value):** the tool layer maximises it; the data layer's real content is even lower than the
  README's honest self-calibration, because 25% of the classes rest on a `tier2` market signal (NF-3).
  The scarce assets remain the HK→BR seed edge (whose `watch_list` shape is, ironically, the prototype
  the timeline schema in NF-4 needs), the yield line, the trigger typology, and the honesty discipline.

## Priorities

**P0 (gate publication):** NF-1 (reconcile the rule; recommend fixing the artifact to destination-first,
which also fixes NF-2's CN claim), NF-2 (rewrite §4.2), E1/F-US-1 (US → `T`; "GENIUS in force" is
wrong) — **after** NF-3 (decide the outbound-US treatment), and E2 (the §3.7/Matrix "or"→"and").
**P1:** NF-3 (the token-signal split, before the signal table lands), NF-4 (done here) + generalise the
`watch_list` shape into the timeline schema, C1 (publish the tree), F-JP-1, F-TW-2 (done here).
**P2:** the schema fields for the three-axis model; VB-08; the README note that the 13 hard checks have
effective rank ~6–7; the doc-drift fixes.

## Verdict

The most honest package I have audited, and now honest about one more thing: its core classification
rule is optimistic, unsourced, and was invisible to its own gates because their anchors all sat on one
side. v0.9.99 fixes what a downstream auditor safely can (the Taiwan timeline and administrator, the
proposal's embedded violation, the closeable backlog items) and — rather than paper over NF-1 — turns
`--strict` red to keep it in view. **Reconcile NF-1 and NF-3, resolve E1 in both directions, then
publish the tree.**

---

## Appendix — commands and probes re-run for this review

```bash
python3 tools/verify_corridors_directed.py            # 13/13 hard checks; 1 lint (m7); exit 0
python3 tools/verify_corridors_directed.py --strict   # exit 1 — RED by design (m7 / NF-1)
python3 tools/run_negative_tests.py                   # 19 negative + control; ALL GATES BITE
python3 tools/schema_reference_crosscheck.py          # 54/54 rejected; Layer 2 SKIP (no network)
python3 tools/build_corridor_matrix.py                # out/ regenerates byte-identically
python3 tools/check_verification_backlog.py           # well-formed; 8 open/tracked + 2 resolved
python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json   # [OK]; SHA 9898d230…
```

(Probes backing NF-1/NF-2/NF-4/NF-5 are in the review body; each is a few lines of stdlib `json` +
`collections.Counter` over `data/computed_corridors_directed.json`.)
