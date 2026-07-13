# CBSR corridor layer — third independent review (over v0.9.93)

_Independent re-audit of the directed-132 corridor layer and its standalone toolchain, taken over
the v0.9.93 release, against the two companion working papers (*Cross-Border Stablecoin Feasibility
Over Time* v0.1.0, *Citable by Construction* v0.1.0) and the three prior deliverables (Compliance
Matrix v0.9.7, Architecture v0.2.8, Corridor Atlas v0.2.5). Review date: 2026-07-08. Reviewer:
independent, no relationship to the author._

One-line verdict: **on every dimension this review could actually test, the register is truthful,
runnable, and externally accurate — but it ships the corridor output layer, not the machinery the
two papers are actually about.** The corridor layer is complete, independently runnable, and survives
adversarial testing; the engine that decides each edge's class (the time engine, the citable subset,
the ten build gates, the 152 node records, the event calendar, the ledger) is **not shipped** and can
be read in the papers but not run from this repository. That is a delivery-completeness gap (finding
**C1**), not a logic defect, and it remains the single highest-priority open item.

Every "verified" claim below was re-derived by running the four tools on the committed artifact, and
the jurisdictional facts were **independently web-verified against primary or high-quality secondary
sources** — not taken from the two bundled reviews.

## Q3 (accurate & runnable) — split in two

**Tool layer: runs exactly as documented.** All four tools were executed against the committed
artifact and matched their self-claims to the digit:

| check | measured result |
|---|---|
| `verify_corridors_directed.py` | 9/9 hard checks, exit 0, **0 lint**; `--strict` also green |
| `run_negative_tests.py` | 15 negative cases + positive control + "artifact never modified" assertion — every gate bites |
| `schema_reference_crosscheck.py` | rejects 54/54 adversarial mutations; with `jsonschema` installed, the bundled executor and the reference agree on all 132 edges + 56 verdicts (not a rubber stamp) |
| SHA-256 | both artifacts' hashes match the README **to the digit** |
| migration determinism | the migration reproduces the committed artifact **byte-for-byte** from the v0.9.92 snapshot |
| `out/` reproducibility | the three views regenerate **byte-for-byte** |

Everything the repository claims it can self-prove was re-run and held. The honesty of this
self-verification layer is itself a strength.

**Full-pipeline layer: does not run from a clone (C1, unchanged).** The upstream builder was invoked
and died at step 1 on the absent `analysis/compatibility.json`. The missing inputs are the 152 node
records, the root `*.yaml`, `compatibility.json`, `computed_corridor_skeletons.json`,
`event_calendar.json`, `verification_ledger.json`, `schema.json`, and the upstream `compose.py` /
`build_analysis.py`. So the papers' "build → exit 0 / 53 invariants / 10 gates bite" is almost
certainly true on the author's full tree, but is **not reproducible from this package**.

## Q1 (complete underlying content) — corridor layer PASS; as an "application substrate", incomplete

The corridor **output** layer is complete and self-consistent: 132/132 ordered pairs, exact
provenance partition (9 + 106 + 17), a 12-field required schema, and the analyst and supervisor
views. As a standalone deliverable it stands. But — sharpening the point the second review made and
this review confirms — the package **verifies** the origin-drag rule (`OD1` passes) yet does not
**contain** the logic that produces it (`class_code` on skeleton edges is inherited from the absent
`computed_corridor_skeletons.json`). The objects the papers are actually about —
`compose(origin, destination, as_of)`, the lawyer-citable subset, the ten build gates — are not here.
Honest conclusion: **corridor layer PASS; as the "application substrate" the papers describe,
incomplete.**

## Sub-question A (key facts & latest developments) — independently web-verified, very high accuracy

Six load-bearing fact-clusters were checked against primary or high-quality sources. **All accurate,
several to the digit:**

- **Taiwan** — Virtual Asset Service Act **third reading 2026-06-30**; issuance needs **FSC + central
  bank** approval; **100% reserves, issuer-yield prohibited**; ~**21-month** transition; **9** pieces
  of secondary legislation; **commencement set separately by the Executive Yuan**. Matches the
  register's "enacted-not-commenced → channelled Category II" treatment.
- **US** — GENIUS in force; CLARITY (H.R. 3633) at **Calendar No. 423**, **reported 2026-06-01**,
  **committee 15-9 on 2026-05-14** — confirmed from Congress.gov. Polymarket "**near 48%, down from
  ~74% a month earlier**" is exactly right for the late-June snapshot.
- **UK** — SI **2026/102**, **made 2026-02-04**, legislation.gov.uk reg. 1(2) "**come into force on
  25th October 2027**", preparatory provisions +21 days — exact.
- **Japan** — Act No. 66 of 2025; reserve relaxation to 50% short-term assets **and** the same-day
  (2026-06-01) Cabinet Office Ordinance recognizing foreign trust-type stablecoins as EPIs — the
  Category II recognition pathway the paper describes.
- **BIS / mBridge / Agorá** — BIS **withdrew from mBridge 2024-10-31**, now PBOC/HKMA/Thailand/UAE/
  Saudi with ~95% volume in digital yuan (dollar-bypass); Agorá is BIS-led with seven G7-aligned
  central banks + 40-plus institutions (dollar-routing). The code's `INFRA` member sets match these
  real memberships, and the §5.2 "correction" (only Agorá is BIS-led) holds.
- **EU MiCA** — Art. 143(3) transitional **1 July 2026 outer cap**, ESMA **confirmed no extension on
  2026-04-17**; the staggered national-window list and the USDC/EURC-authorized / USDT-delisted facts
  all confirm.

**A residual (honestly flagged, now tracked as backlog):** the **Tillis** half of the yield-provision
attribution (VB-01), the PRC 42号 re-verification (VB-04, does not bear on the blocked class), and the
Japan Act No. 66 **promulgation** pinpoint (VB-03; the load-bearing 2026-06-01 effective date is
confirmed). All are recorded in [`verification_backlog.json`](verification_backlog.json).

## Sub-question C (logic appropriate; accuracy re-checked) — composition self-consistent; reconciliation exact

Read line by line and re-derived:

- **Origin-drag-first** — tokenless = {CN, TW, KR}; every edge from them is III, and every III is from
  them (`OD1`). III is exactly 3×11 = 33, no exceptions.
- **Bloc partition** — recomputed over 132 edges: agora=30 (6×5), mbridge=6 (3×2), ensemble=2 (HK↔SG),
  cross-bloc=36 (6 agora × 3 mBridge × both directions), none=58, total 132. The two authored US↔HK
  edges are correctly **cross-bloc** (N1 fix confirmed).
- **Class reconciliation (`CD1`)** — the register's 32/32/33/17/9/9 vs the Atlas baseline
  32/32/27/8/11/22 is explained **exactly** by the two declared deltas: origin-drag on the 6 CN/TW/KR
  mutual edges (**III +6**), Taiwan enacted (**T +9**), hence **pre −13** and **blocked −2**; I and II
  unchanged. The arithmetic closes with no residual.

The `compatibility_category` vs directed `class_code` split (US→EU = I while EU→US = II, sharing the
undirected pair category) lands correctly — the papers' "direction matters" thesis, with `DC4b`
recomputing every pair.

## Q2 (value maximized) — high in concept; corridor layer already delivers; the gap is the unshipped machinery

The design is sound (feasibility composed from legal propositions, shipped as a labelled preview;
queryable JSON + static API + CI invariants; serving operators, supervisors, lawyers, researchers),
and the tool layer already delivers the original "whole map, legible" goal (matrix + supervisor views
+ zero-dependency verification). The one gap is large but singular: the highest-value machinery is not
runnable (**C1**).

## New observations beyond the first two reviews (the increment)

1. **Singapore ∈ Project Ensemble unverified (VB-02).** The code puts SG in `ensemble={HK,SG}`,
   affecting the SG↔HK bloc tag and SG's attribution. The first two reviews externally verified the
   agora/mbridge member sets but not ensemble. Ensemble is HKMA-led and the paper positions it as
   "bridging from Hong Kong," but SG's **formal** membership was not found. Consistent with the paper's
   own Tier-2 labelling of the substrate; a specific attribution item for the backlog.
2. **Taiwan yield prohibition now confirmed by enacted text → §4.5 upgradeable (VB-R1).** *Feasibility*
   §4.5's yield-line convergence claimed US + Singapore at citable depth and put Taiwan in backlog.
   This review confirmed Taiwan **explicitly prohibits issuer-paid yield**, and Matrix v0.9.7 already
   groups it in the prohibition cluster (EU, HK) — so the convergence is **stronger** than the paper
   claimed. An upgrade for the next paper revision.
3. **Living-document drift (snapshot 6-30 → 7-8)** — CLARITY odds ~48%→~42-46%; the MiCA 7-1 cliff has
   **passed**; FCA final rules reported landed 6-30; Taiwan presidential promulgation due ~10 days
   after third reading. None are errors; all are v1.0 dating updates, tracked in
   [`DEVELOPMENTS_SINCE_SNAPSHOT.md`](DEVELOPMENTS_SINCE_SNAPSHOT.md).
4. **M1 (Matrix Taiwan cell stale) confirmed, not an internal contradiction.** Matrix v0.9.7 reads
   "remains a bill … no third reading yet," honest about its own cut-off (top-line ⚠ conditional-status
   banner, "June 2026 state"), and predates the third reading; the corridor layer already treats Taiwan
   as enacted-not-commenced. A version skew for an upstream Matrix v0.9.8.
5. **N2 (flagship category divergence not reproducible) confirmed.** The 7 shipped `divergence` fields
   record only *interaction-set* differences and `category_mismatches` is empty, so *Citable*'s §5.2
   headline EU–UK / UK–US **category** divergence genuinely cannot be reproduced from this artifact.
   Open until the compatibility layer is published (a facet of C1).

## What v0.9.94 does in response

- **VB-02 (SG ∈ Ensemble)** — the two SG↔HK edge notes no longer assert "Both ends on Project
  Ensemble" (a v0.9.93 canonicalization that dropped the earlier, more careful "Ensemble + Guardian
  alignment" wording this review flagged). They now read as an HKMA-Ensemble / MAS-Guardian
  **alignment** with the Tier-2 membership caveat, and the `INFRA` definition is annotated. The bloc
  **enum** is unchanged (a defensible Tier-2 judgment; IB1 still passes).
- **The residual is now published and machine-checkable** — `docs/verification_backlog.json`
  (VB-01…VB-05 open, VB-R1 resolved) with `tools/check_verification_backlog.py` validating it in CI,
  which is exactly the *Citable by Construction* §6.2 discipline applied to this layer.
- **Living-document drift is tracked** — `docs/DEVELOPMENTS_SINCE_SNAPSHOT.md`.
- **This review is folded in** at `docs/AUDIT_v0.9.93_third-review.md`.

What remains open is upstream and stated, not hidden: **C1** and its dependent **N2**, the **M1**
version-skew, and the primary-source pins in the backlog.

---

## Appendix V — commands re-run for this review

```bash
python3 tools/verify_corridors_directed.py            # 9/9, 0 lints
python3 tools/verify_corridors_directed.py --strict   # 9/9, exit 0
python3 tools/run_negative_tests.py                   # ALL GATES BITE
pip install jsonschema && python3 tools/schema_reference_crosscheck.py   # 54/54; two implementations agree
python3 tools/build_corridor_matrix.py                # out/ regenerates byte-identically
python3 tools/check_verification_backlog.py           # backlog well-formed
python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json   # [OK] current shape
# upstream builder, for the record:
python3 scripts/build_corridors_directed.py           # FileNotFoundError: analysis/compatibility.json  (C1)
```
