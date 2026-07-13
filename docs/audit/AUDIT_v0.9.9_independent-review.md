# CBSR v0.9.9 — Independent Global Review & Verification

_Independent audit of the Cross-Border Stablecoin Register (v0.9.9) corridor layer and the
three companion deliverables (portfolio audit, directed-132 corridor layer, fifteen-dimension
Matrix backfill), against the four companion working papers as the "underlying research."
Review date: 2026-07-07. Reviewer: independent, no relationship to the author._

This review answers the three acceptance questions — **(1) complete underlying application
content, (2) value / applicability / functionality, (3) accurate and runnable** — and the three
emphasised sub-questions — **(A) key jurisdictional facts and latest developments, (B) most
effective realisation of value and function, (C) logic and re-verified accuracy.** It is deliberately
independent of the author's own `AUDIT_v0.9.9_global-review.md`: where I agree I say so; where I
found something the author's audit did not surface, I flag it.

Every "verified" claim below was re-derived mechanically by the two zero-dependency tools shipped
alongside this document (`tools/verify_corridors_directed.py`, `tools/build_corridor_matrix.py`),
which run on the corridor artifact **alone**. Their output is reproduced in Appendix V. In addition,
the jurisdictional facts in §5 were **independently web-verified against primary and reputable
secondary sources** (see that section for citations).

> **Revision 2 (2026-07-07).** This revision strengthens the first pass in four ways, after a
> second independent review surfaced three checkable issues (all confirmed here against the files):
> (i) a new **Major** finding — a three-way **version mismatch** across the papers, the bundle, and
> the shipped Matrix (§4, M2); (ii) the shipped JSON Schema is now **executed** by the verifier
> against every edge — an earlier revision of that schema silently rejected 2 of the 132 authored
> edges (130/132) while the verifier passed them, an internal contradiction now removed (§2, §4);
> (iii) the category cross-check **DC4** is now **recomputed** from the 132 edges (pair-key
> canonicality + inter-direction agreement) rather than trusting the artifact's self-declared flag,
> which is retained but clearly labelled as an attestation (§7); and (iv) the §5 jurisdictional facts
> are now **web-verified**, which also **overturns one shared assumption of both prior audits** — the
> "Tillis–Alsobrooks" naming is *correct*, not a likely error (§4, §5).

---

## 0. Scope — read this first: what was actually received

The single most important audit finding is about *packaging*, and it reframes acceptance question 3.

**What arrived is a _changes-only bundle_, not the runnable register.** The upload contains the
three modified pipeline scripts (`build.py`, `build_api.py`, `run_invariants.py`), the new builder
(`scripts/build_corridors_directed.py`), the **pre-generated** output
(`analysis/computed_corridors_directed.json`), two API samples, the author's audit, and the
Compliance Matrix v0.9.8. It does **not** contain the register's own data and upstream machinery.
Concretely, every one of the following inputs that the shipped scripts read is **absent** from the
bundle:

| Missing input | Needed by | Consequence if you clone only this bundle |
|---|---|---|
| the **152 node records** (per-jurisdiction YAML/JSON) | everything | no register to build |
| root corridor `*.yaml` (the 9 authored edges) | `build_corridors_directed.py` | builder cannot load authored layer |
| `analysis/compatibility.json` (§5.14 66 pairs) | builder + `build.py` DC-check + invariants | category cross-layer check cannot run |
| `analysis/computed_corridor_skeletons.json` (106) | builder | builder cannot load skeleton layer |
| `analysis/event_calendar.json` (events) | builder (transition timelines) | 17 transition edges cannot be filled |
| `analysis/computed_{compatibility,sensitivity,settlement,substrate,timeline}.json` | `build.py`, `run_invariants.py` | build/invariants abort on missing files |
| `analysis/verification_ledger.json` | ledger cross-check gate | gate cannot run |
| `schema.json`, `taxonomy.md` | validation, dimension canon | no schema validation; no dimension source |
| `scripts/build_analysis.py`, `compose.py`, `build_edge_skeletons.py`, `build_corridor_states.py` | build order | pipeline has no upstream stages |
| `run_negative_tests.py` (the 10 gates) | negative-test suite | "10/10 gates bit" not reproducible here |

The author's README/AUDIT/INTEGRATION report `build.py → exit 0`, `132/132`, `53/53 invariants`,
`10/10 gates`. **Those results are almost certainly true on the author's full tree, but they are not
reproducible from this bundle** — a fresh clone of what was uploaded fails at build step 1 for missing
inputs. This is not a logic defect; it is a **delivery-completeness defect**, and it is the reason
acceptance question 3 ("runnable") needs a split answer (see §3).

**How this review responds.** Rather than take the author's pipeline results on faith, I verified
everything about the corridor layer that is checkable from the artifact alone, and I shipped two
**zero-dependency** tools (standard library only, no `pip install`, no missing files) so the corridor
layer is now runnable and legible **standalone** — closing the gap for the one artifact that matters
most to the stated goal ("all jurisdictions bridge to each other"). See §8 and Appendix V.

> Note on "previous chat background" (sub-question B). The prior conversation that produced this
> engagement is not available to this reviewer. I therefore audited against the four companion
> working papers (Compliance Matrix, Architecture, Corridor Atlas, Feasibility-Over-Time) and the
> methodology paper (Citable by Construction) as the authoritative statement of the "underlying
> research." Where the code implements what those papers describe, I treat that as faithful to the
> engagement's intent.

---

## 1. Complete underlying application content — **PASS for the corridor layer; INCOMPLETE as a repo**

**The corridor layer itself is complete and correct.** Independently verified from the artifact:

- **132 / 132 ordered pairs present** — every one of the 12 × 11 directed pairs carries a
  `corridor/v3-directed-edge` record. No pair missing, none extra. (verifier DC1)
- **Provenance partitions exactly**: 9 authored + 106 computed skeletons + 17 computed transition
  = 132. (verifier DC3)
- **The category cross-layer relationship holds, recomputed from the edges**: every edge's
  `compatibility_pair` is the canonical key of its endpoints (DC4a), and both directed edges of all
  66 unordered pairs agree on `compatibility_category` (DC4b). The artifact's own self-check flag is
  additionally present and clean (DC4c, attested — see §7 for the honest scope of this).
- **Every edge validates against the shipped JSON Schema** — the verifier now *executes*
  `tools/corridor_directed.schema.json` against all 132 records (132/132). (verifier SCHEMA)

This directly settles the concern that motivated the engagement — that corridors covered only the
flagship **HK → BR**. They do not: HK → BR is **one cell of 132**, and one of only **9** authored
deep-dives. The full mutual graph is present. §8 shows it as a 12 × 12 matrix.

**But the deliverable is not a standalone repo** (see §0). The *content that exists* is complete; the
*content shipped in this bundle* is a patch layer over a register that was not included. For acceptance
question 1 the honest verdict is: **the corridor layer passes; the bundle is not self-contained.**

---

## 2. Value / applicability / functionality — **HIGH in concept; now realised standalone**

The design is right: feasibility is *composed* from propositions of law and shipped as a labelled
preview, not transcribed; the directed layer is queryable JSON plus a static API and is guarded by a
CI invariant (DC2, category-vs-§5.14). Multiple audiences are served (operators, supervisors,
lawyers, researchers). All of that is genuine value.

The gap was that **none of it could be exercised without the full tree**, and there was **no view that
makes the all-pairs result legible** — the very thing the engagement was about. This review closes both:

- `tools/verify_corridors_directed.py` — re-checks the layer **from the artifact alone**, zero
  dependencies. It (a) **executes** the shipped JSON Schema against every edge via a bundled minimal
  validator — so the verifier and the schema can never disagree; (b) **recomputes** the category
  cross-layer relationship (pair-key canonicality DC4a, inter-direction agreement DC4b) rather than
  trusting the artifact's flag; and (c) checks coverage, provenance, the origin-drag invariant,
  distribution reconciliation, and bloc logic. Exit 0 = the layer is sound. (Appendix V.)
- `tools/build_corridor_matrix.py` — emits the **12 × 12 class matrix** (`out/corridor_matrix.md`,
  `.csv`) and the **per-jurisdiction supervisor view** (`out/corridor_per_jurisdiction.md`). This is
  what turns "every jurisdiction bridges to every other" from a sentence into a grid a reader can scan
  and a spreadsheet can consume.
- `tools/corridor_directed.schema.json` — a JSON Schema for a directed edge, describing the **exact**
  field shapes in the build (including the object-valued `origin_override` on the SG→HK edge and both
  in-use `schema` tags), so all 132 records validate by construction even outside the register's own
  `schema.json`. The expectation that every edge *should* carry the v3 tag is surfaced as a non-fatal
  lint (m1), not a schema-level reject — see §4.

---

## 3. Accurate and runnable — **ACCURATE (with one cross-artifact inconsistency); RUNNABLE split**

**Runnable — split verdict:**

- The author's **full pipeline is not runnable from this bundle** (missing inputs, §0). Treat the
  "exit 0 / 53 invariants / 10 gates" figures as author-reported on the full tree, not reproduced here.
- The **corridor layer is now runnable standalone** via the two shipped tools. Verified today:
  `verify_corridors_directed.py → 9/9 hard checks pass, exit 0` (one non-fatal lint);
  `build_corridor_matrix.py → 132 edges, three views written`. (Appendix V.)

**Accurate — high, on both axes I can test.** Two independent axes: (i) **cross-document consistency**
between the code and all five papers — high (§5, §7); and (ii) **live external accuracy** — in this
revision I web-verified the load-bearing jurisdictional facts against primary and reputable secondary
sources, and they hold up with precision (dates, clause substance, vote counts, statute numbers all
check out — §5). Two exceptions remain, both about *artifacts disagreeing with each other or with the
world*, not about the corridor logic: the **Compliance Matrix v0.9.8 still describes Taiwan as an
un-enacted bill** (M1), and the **paper/bundle/Matrix version strings do not line up** (M2, new). The
directed corridor layer itself is accurate.

---

## 4. Findings, prioritised

| # | Sev. | Finding | Evidence | Remediation |
|---|---|---|---|---|
| **C1** | **Critical** | Bundle is changes-only; the register data + upstream scripts + schema/taxonomy are absent, so the author's build/invariants/negative-tests cannot run from what was uploaded. | §0 table; every `analysis/*.json` input except the pre-generated output is missing; `scripts/build_*` upstream stages absent. | Ship the full register tree (or a release tarball) alongside the patch; **and/or** use the zero-dep tools here for standalone corridor verification. Add a one-line "this is a patch, apply onto vX of the register" banner to the bundle README (done in this bundle's `README.md`). |
| **M1** | **Major** | Compliance Matrix **v0.9.8** (dated July 2026) still states Taiwan's VAS Act "remains a bill … no third reading yet," contradicting the register's regime-in-transition treatment and the Feasibility paper's third-reading enactment on 2026-06-30. The v0.9.8 backfill deliberately left per-jurisdiction prose unchanged, so it shipped a known-stale Taiwan cell. | Matrix v0.9.8 lines 52 & 910 vs. Feasibility §3.3; directed layer classes TW as transition; author audit §A already lists TW "third reading 2026-06-30." | Update the Taiwan cells: status → *enacted 2026-06-30, commencement pending nine subsidiary items (est. Q1 2027; operator re-application by end Q1 2028)*; `binding_status = made_not_commenced`. This is the one place the paper set and the register disagree on a binding status. |
| **M2** | **Major** | **Three-way version mismatch (new).** The two companion PDFs cite the register as **v0.9.91** and the Compliance Matrix as **v0.9.7**; this bundle's README/AUDIT call it register **v0.9.9** / Matrix **v0.9.8**; and the Matrix file actually shipped in the `files__11_` companion set is **v0.9.7** (matching the papers, *not* the bundle). So a reader gets two different Matrix versions across the two archives, and neither the register version (v0.9.9 vs v0.9.91) nor the Matrix version (v0.9.7 vs v0.9.8) reconciles with the papers. | `grep` of both PDFs → `CBSR v0.9.91`, `Compliance Matrix v0.9.7`; bundle README/AUDIT → `v0.9.9`/`v0.9.8`; `files__11_` ships `…Matrix_v0.9.7.{md,pdf}`; data artifact `generated: 2026-07-07`. | Align the version strings, or ship a one-line version map in the bundle stating which register/Matrix revision the papers and the patch each correspond to. (This subsumes and explains the M1 Taiwan staleness: the v0.9.7 Matrix the papers cite predates the 2026-06-30 Taiwan enactment and is defensible; the v0.9.8 Matrix in *this* bundle post-dates it and is not.) |
| **m1** | Minor | The flagship **HK → BR** seed edge (`hk-br-usd-stablecoin-settlement-001`) is the **only** edge still on schema tag `corridor/v2-rich`; the other 131 are `corridor/v3-directed-edge`. The register's own DC1–DC4 do not check the per-edge schema string, so it passes CI unnoticed. | verifier surfaces it as a WARN; `schema` tag census = 131 × v3, 1 × v2-rich. **Note:** an earlier revision of the shipped schema pinned `schema` to a single const, which *rejected* this edge (and the SG→HK object-`origin_override` edge) → 130/132, contradicting the verifier that passed them. This revision's schema validates all 132 and keeps tag-uniformity as this lint. | Migrate the seed corridor's `schema` field to `corridor/v3-directed-edge` (content is otherwise valid), or add a "uniform schema tag" invariant (DC5). |
| **m2** | Minor | HK → BR authored edge sets `infrastructure_overlap: null` where computed edges use the string `"none (…)"`. | field census: 131 have `infrastructure_overlap`, 1 lacks it. | Semantically fine (Brazil is off all substrates); for uniformity, emit the `"none (…)"` string on the authored edge too. |
| **m3** | Minor | New Taiwan Dollar is coded **`NTD`** across register + Atlas + Matrix; ISO 4217 is **`TWD`**. Internally consistent, but a downstream ISO consumer expects `TWD`. | `CCY["TW"]="NTD"` in the builder; matrix "peg currency (NTD vs USD)". | Optional: carry `TWD` as the canonical code with `NTD` as an alias, or note the deviation once in `taxonomy.md`. |
| **m4** | Minor | The bundle README's build order references upstream scripts (`build_edge_skeletons.py`, `build_corridor_states.py`, `run_negative_tests.py`) that are correct pointers to the full repo but are **not present here**, with no note saying so. | README build order vs. §0 missing list. | State explicitly that the bundle is a patch and list its external prerequisites (done in this bundle's `README.md`). |

**Two footnote items — now web-verified, and one correction to *both* prior audits:**

- **"Tillis–Alsobrooks compromise" is CORRECT — do not change it.** The author's audit and the first
  pass of *this* audit both flagged this as a likely error, suspecting the two crossover votes
  (Gallego + Alsobrooks) had been mis-transcribed. Web verification shows the register was precise and
  both facts are true of *different things*: the two Democratic **committee votes** on 2026-05-14 were
  Ruben Gallego and Angela Alsobrooks, **but the stablecoin-yield compromise language itself was
  negotiated and authored by Thom Tillis and Angela Alsobrooks** — confirmed by CoinDesk, the Bank
  Policy Institute's own statement, Elliptic, and Banking Dive. Naming the *compromise* after its
  drafters (Tillis–Alsobrooks) is accurate; the reviewer suggestion to rename it "Gallego/Alsobrooks"
  would have introduced an error. A one-line footnote distinguishing the two facts is still worthwhile.
- **HK Stablecoins Ordinance "Cap. 656" is correct.** Confirmed: the Ordinance commenced 2025-08-01,
  and the HKMA granted the first stablecoin licences on 2026-04-10 (to two issuers), with a stated
  "open but very selective" posture on further grants — matching the register. The stray "Cap. 566"
  seen elsewhere is the typo. Pin the citable cell to the Gazette.

---

## 5. Sub-question A — key jurisdictional facts and latest developments — **WEB-VERIFIED, HIGH ACCURACY**

This revision does what the first pass could not: I checked the register's load-bearing jurisdictional
claims **against live primary and reputable secondary sources**. The empirical grounding is unusually
strong — several claims are accurate down to the statute number, the effective date, and the committee
vote count. Findings by jurisdiction:

- **Taiwan — confirmed to the day.** The Legislative Yuan passed the *Virtual Asset Service Act* at
  **third reading on 2026-06-30**; stablecoin issuance requires **dual FSC + central-bank** approval;
  issuers must hold **100% segregated reserves in trust** and are **barred from paying yield**; existing
  VASPs get a **~21-month** transition (12 months to apply, 21 to be licensed, one 3-month extension);
  **nine subordinate rules** are pending; and **commencement is set separately by the Executive Yuan** —
  i.e. *made, not commenced*. (FSC statement; The Block; CryptoSlate; CoinLaw; BigGo.) This is exactly the
  register's regime-in-transition treatment — and exactly what the Matrix v0.9.8 cell contradicts (M1).
- **China — confirmed to the clause.** **PBoC 银发〔2026〕42号**, eight-department notice, **effective
  2026-02-06**, **repealing 银发〔2021〕237号**; the operative sentence — *without lawful approval, no
  entity inside or outside China may issue an RMB-pegged stablecoin offshore* — is verbatim, as is the
  **long-arm** framing (protective + personal jurisdiction). The paired **CSRC 公告〔2026〕1号** on
  offshore ABS-token issuance was issued the same day. Chinese law-firm commentary characterises it
  precisely as a **conditional prohibition** that leaves a licensing door open ("dynamic assessment"),
  which is the register's §3.9 "tightening settled, relaxation still open" reading. (CSRC's own site;
  Deheng; Guantao; Hankun; Zhonglun.) This underwrites the entire **CN column = BLK**.
- **BIS / mBridge / Agorá — confirmed, and it validates the IB1 bloc partition.** BIS **withdrew from
  Project mBridge on 2024-10-31** ("graduation"); the residual members are PBoC, HKMA, Bank of Thailand,
  Central Bank of the UAE, and SAMA (China-dominant). Project **Agorá** is **seven G7-aligned central
  banks** — NY Fed, Banque de France (Eurosystem), Bank of England, Bank of Japan, Bank of Korea, Banco
  de México, Swiss National Bank — plus 40+ private institutions. Intersecting with the 12-jurisdiction
  universe, Agorá = **{US, EU, UK, CH, JP, KR}** and mBridge = **{CN, HK, AE}** — **exactly** the
  builder's `INFRA` sets. This confirms the Feasibility §5.2 *correction* (Agorá is BIS-led; mBridge is
  now PBoC + Gulf, **not** BIS; Ensemble is HKMA-led) — the repudiated "all three are BIS" error is
  absent from the code. (BIS; OMFIF; Cointelegraph; Forbes; Ledger Insights.)
- **United States — confirmed, and it resolves the footnote.** **GENIUS Act** signed **2025-07-18**
  (rulemaking deadline 2026-07-18); **CLARITY (H.R. 3633)** passed the House 2025-07-17 (294–134), cleared
  **Senate Banking 15–9 on 2026-05-14** (Gallego + Alsobrooks the two Democratic votes), placed on the
  Senate calendar as **Calendar No. 423 on 2026-06-01**, and **missed the July-4 signing target** — now
  stalled pending three disputes. The **yield compromise** — no passive/interest-like yield, activity-based
  rewards permitted, joint SEC/CFTC/Treasury rulemaking within a year — was **authored by Tillis and
  Alsobrooks**, so the register's "Tillis–Alsobrooks" naming is **correct** (see §4). The register's
  treatment of CLARITY as *contingent, undated, ~50-50* is vindicated by events. (CoinDesk; Banking Dive;
  Elliptic; ABA Banking Journal.)
- **EU / MiCA — confirmed.** The **Article 143(3)** grandfathering window closes **2026-07-01** (the
  18-month outer limit, no extension) — precisely the register's cliff date and mechanism; category
  unchanged, single passport. (ESMA.) As of today (2026-07-07) this cliff has **just passed** — a
  living-document update for v1.0, not an error.
- **United Kingdom — consistent.** SI **2026/102**, full commencement **2027-10-25** with preliminary
  provisions 21 days after making; resolves to a clean **Category I**. The FCA's final rules/guidance
  landed **2026-06-30** — i.e. the paper's "expected summer policy statement" has now arrived (living-doc
  update, not a defect). Matches Feasibility §3.1 / Atlas §5.

**Internal cross-consistency (unchanged from the first pass, still verified mechanically).** The bloc
edge counts corroborate the membership above: **30** intra-Agorá directed edges (6 nodes → 6×5 — the
Atlas's "twelve → thirty" jump when JP/KR joined) and **6** intra-mBridge edges (3 nodes → 3×2), with
cross-bloc pairs tagged `cross-bloc` for the "rival, non-interoperable rails" reading. (verifier IB1)

**Net on sub-question A:** the register's jurisdictional facts are not merely internally consistent with
the papers — they are **externally accurate** against live sources, and the one previously-suspected error
(Tillis–Alsobrooks) is in fact correct. The only accuracy defects are cross-artifact, not factual: the
stale Taiwan Matrix cell (M1) and the version drift (M2). The living-document items (MiCA cliff passed,
FCA rules landed, Agorá in real-value testing since 2026-05) are updates for v1.0, expected of a
snapshot dated 2026-06-30.

---

## 6. Sub-question B — value/function realisation vs the engagement — **STRONG, and the corridor goal is met**

The engagement's throughline (audit → optimise → ground in the real register → integrate → reconcile)
is coherent and, importantly, its headline objective is achieved: **all-pairs mutual bridging exists and
is now legible.** The corridor concern is fully answered:

- **Every jurisdiction bridges to every other** at the graph level: 132/132 edges (§1).
- **HK → BR is demonstrably no longer the whole story** — it is the seed corridor (`…-001`), one of
  9 authored and 132 total. (It is also the schema straggler, m1 — a nice tell that it is the oldest record.)
- The new **12 × 12 matrix** (§8) makes the structure scannable; the **per-jurisdiction view** gives a
  supervisor the "corridors touching my jurisdiction, and to/from whom" cut the Feasibility paper §4.4
  argues for, from the same 132 edges.

Value is presented as working, self-checking artifacts (a builder, an invariant, an API, and now a
standalone verifier + matrix), which is the correct register for a machine-readable-reference project.

---

## 7. Sub-question C — logic and re-verified accuracy — **SOUND**

- **Origin-drag-first is applied consistently and is a *declared* choice.** Every edge out of a
  token-less origin (CN, TW, KR) is Category III, and every Category III edge originates in CN/TW/KR —
  no leakage either way. (verifier OD1) The 6-edge difference from the authored Atlas (which lets a
  prohibition/pre-regime *destination* dominate on the CN/TW/KR mutual edges) is surfaced as a
  computed-vs-authored **finding**, exactly the labelled-preview discipline of Citable by Construction
  §5.2 — not an error.
- **The class distribution reconciles to the Atlas baseline exactly, via two declared deltas.**
  Atlas baseline `32 I · 32 II · 27 III · 8 T · 11 blocked · 22 pre-regime` → CBSR
  `32 · 32 · 33 · 17 · 9 · 9` through: **(a)** Taiwan enacted (9 token-holder→TW edges move
  pre-regime → T), and **(b)** origin-drag on the 6 CN/TW/KR mutual edges (TW→CN, KR→CN leave
  *blocked*; CN→TW, KR→TW, CN→KR, TW→KR leave *pre-regime*; all six become III). Net:
  III +6, T +9, blocked −2, pre-regime −13, I and II unchanged. The verifier reconstructs this
  arithmetic from the Atlas baseline and confirms it equals the artifact's actual counts. (verifier CD1)
- **The category cross-layer invariant is independent of the ordering and holds — now recomputed, not
  taken on trust.** The property DC2 enforces (each edge's `compatibility_category` equals its §5.14 pair
  category) is untouched by the origin-drag-vs-destination-dominant question. In the first pass the
  verifier checked this by *reading the artifact's own `cross_check.clean` flag* — an attestation, not an
  independent test, which a careless reader could mistake for verification. This revision **recomputes**
  what the 132 edges permit: **DC4a** confirms every edge's `compatibility_pair` is the canonical
  alphabetical key of its endpoints, and **DC4b** confirms both directed edges of all 66 unordered pairs
  agree on `compatibility_category` (0 disagreements) — the pair-level consistency that DC2 is *about*.
  The artifact's flag (**DC4c**) is retained but explicitly labelled as self-attested, with the one thing
  that genuinely can't be re-derived offline called out: deriving each pair's category from the underlying
  jurisdiction properties needs `analysis/compatibility.json`, which is absent from the bundle (§0).
- **Dimension reconciliation is correct.** The Matrix v0.9.8 backfill (10 → 15 dimensions; C1–C8 map;
  reserve/capital/**custody** split; issuer/**routing** split; **securities** and **monetary-sovereignty**
  promoted; **disclosure** separated; 14 `tier1_legal` + 1 `tier2_operational` implementation-status)
  matches `taxonomy.md` and Citable by Construction §7.2. Substantive legal content is unchanged —
  correctly, *except* the Taiwan staleness (M1).

---

## 8. The corridor deep-dive (the engagement's headline ask): the full 12 × 12 matrix

Generated by `tools/build_corridor_matrix.py` from the artifact; full copy in `out/corridor_matrix.md`.

```
origin\dest  US  EU  UK  SG  HK  CN  BR  CH  AE  JP  TW  KR
US            —   I   T   I   I  BLK  II   I  II  II   T  PRE
EU           II   —   T   I   I  BLK  II   I  II  II   T  PRE
UK           II   I   —   I   I  BLK  II   I  II  II   T  PRE
SG           II   I   T   —   I  BLK  II   I  II  II   T  PRE
HK           II   I   T   I   —  BLK  II   I  II  II   T  PRE
CN          III III III III III   —  III III III III III III
BR           II   I   T   I   I  BLK   —   I  II  II   T  PRE
CH           II   I   T   I   I  BLK  II   —  II  II   T  PRE
AE           II   I   T   I   I  BLK  II   I   —  II   T  PRE
JP           II   I   T   I   I  BLK  II   I  II   —   T  PRE
TW          III III III III III III III III III III   —  III
KR          III III III III III III III III III III III   —
```

`I` dual-authorization · `II` recognition/comparability channel · `III` composition unresolved
(origin has no exportable token) · `T` regime-in-transition · `BLK` blocked · `PRE` pre-regime.

**How to read it honestly (this is the substantive point, not a caveat).** A complete graph is *not*
a claim that every pair is operable today. The three visually dominant features are all **facts of law**,
not coverage gaps:

- the **CN column is entirely `BLK`** — China prohibits foreign-stablecoin circulation (Feasibility §3.9);
- the **KR column is entirely `PRE`** and the **UK/TW columns entirely `T`** — destination regimes are
  absent (KR) or adopted-but-not-operative (UK, TW);
- the **CN/TW/KR rows are entirely `III`** — those origins have no exportable authorizable token, so the
  corridor reduces to partnership/coordination, not direct issuance (Atlas §3).

So "all jurisdictions bridge to each other" is true in the precise and useful sense the register supports:
**every pair has a directed-edge record that states its class and the reason for it.** 32 pairs are open
now (I), 32 are channelled (II), and the remaining 68 are unresolved/pending/blocked/pre-regime *because
the law makes them so* — which is exactly what a feasibility map should report rather than paper over.

---

## 9. Verdict

| Question | Verdict |
|---|---|
| 1. Complete underlying content | **Corridor layer: PASS** (132/132, provenance clean, category recomputed clean, schema-valid). **Bundle as a repo: INCOMPLETE** (register data + upstream scripts absent — C1); version strings do not line up (M2). |
| 2. Value / applicability / functionality | **HIGH**, and now exercisable standalone via the shipped verifier (which *executes* the schema and *recomputes* the category check) + matrix + schema. |
| 3. Accurate and runnable | **Accurate: high** — jurisdictional facts web-verified against live sources; two cross-artifact defects only (M1 stale Taiwan cell, M2 version drift), not corridor-logic errors. **Runnable: split** — author's full pipeline not reproducible from this bundle; corridor layer runnable standalone (verified, **9/9** hard checks, exit 0). |
| A. Facts / latest developments | **WEB-VERIFIED, high accuracy** — Taiwan, China (42号), BIS/mBridge/Agorá, US (GENIUS/CLARITY), MiCA, UK all confirmed to statute number / date / vote count against primary + reputable secondary sources; the previously-suspected "Tillis–Alsobrooks" error is in fact **correct**. Living-doc updates (MiCA cliff passed, FCA rules landed) noted. |
| B. Value realised vs engagement | **STRONG** — the all-pairs mutual-bridging goal is met and made legible; HK → BR is 1 of 132. |
| C. Logic & accuracy | **SOUND** — origin-drag declared, distribution reconciles, category invariant now **recomputed** (DC4a/DC4b) not merely attested, dimension backfill correct. |

**Bottom line.** The intellectual content — the directed-132 corridor layer and the fifteen-dimension
reconciliation — is complete, internally consistent, logically sound, and (as this revision now shows by
live web check) **externally accurate**; it fully answers the "every jurisdiction bridges to every other"
objective. What stands between it and a clean release is not the logic but the **packaging and
housekeeping**: ship the register the patch applies to (**C1**), align the version strings across papers /
bundle / Matrix (**M2**), and bring the Matrix's Taiwan cell into line with the enacted status (**M1**).
Everything else is minor. The tools in this bundle make the corridor layer verifiable — schema executed,
category recomputed — and legible on its own in the meantime.

---

## Appendix V — reproduction (run today, this bundle, no external files, no pip install)

```
$ python3 tools/verify_corridors_directed.py
[PASS] SCHEMA  all 132 edges validate against corridor_directed.schema.json (executed)
[PASS] DC1     covers all 132 = 12x11 ordered pairs
[PASS] DC3     provenance partitions 132 (9 authored + 106 skeleton + 17 transition)
[PASS] DC4a    [recomputed] compatibility_pair == canonical alphabetical key of {o,d}
[PASS] DC4b    [recomputed] both directions of each of 66 pairs share compatibility_category
[PASS] DC4c    [self-attested] artifact cross_check.clean == true, 0 mismatches
[PASS] OD1     origin-drag-first: FROM {CN,TW,KR} => III, and every III is FROM {CN,TW,KR}
[PASS] CD1     class distribution reconciles to Atlas baseline via 2 declared deltas
[PASS] IB1     infrastructure bloc tag matches Agora/mBridge/Ensemble/cross-bloc partition
[WARN] m1  authored edge(s) still on legacy 'corridor/v2-rich' tag (schema-valid; migrate for tag-uniformity)
         -> hk-br-usd-stablecoin-settlement-001 (HK->BR)
[NOTE] DC4c is the artifact's own flag, not an independent check. Full per-pair re-derivation from
       jurisdiction properties needs analysis/compatibility.json (absent from this bundle); DC4a + DC4b
       recompute everything the 132 edges permit and both pass.
class distribution: {'I': 32, 'II': 32, 'III': 33, 'T': 17, 'blocked': 9, 'pre_regime': 9}
provenance:         {'authored': 9, 'computed_skeleton': 106, 'computed_transition': 17}
9/9 hard checks passed; 1 warning(s)          # exit 0

# adversarial self-test (not shipped in the tool): the schema executor accepts all 132 real edges
# AND rejects deliberately corrupted ones — missing-required, bad enum, bad schema tag, non-J12
# jurisdiction, pattern failure, wrong origin_override type, bad interaction_sets member — so
# "132/132 executed" is a genuine pass, not a rubber stamp.

$ python3 tools/build_corridor_matrix.py
wrote out/corridor_matrix.md, out/corridor_matrix.csv, out/corridor_per_jurisdiction.md
  132 edges | class distribution: {'I': 32, 'II': 32, 'III': 33, 'T': 17, 'blocked': 9, 'pre_regime': 9}
```
