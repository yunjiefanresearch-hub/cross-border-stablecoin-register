# CBSR corridor layer — fifth independent review (over v0.9.95)

_Independent re-audit of the directed-132 corridor layer and its toolchain, over the v0.9.95 release.
Every tool was re-run in a clean Python 3.12 environment; all 132 edges were inspected; the `CD1`
reconciliation was recomputed by hand; and **twelve load-bearing jurisdictional facts were checked
against primary sources** (legislation.gov.uk, congress.gov, the Federal Register / OCC NPRM, the
HKMA and PBoC pages, ESMA, and central-bank primary coverage) rather than relying on the four bundled
reviews. Review date: 2026-07-08. Reviewer: independent, no relationship to the author._

One-line verdict: **an exceptionally high-quality, unusually self-critical package. It runs, it is
byte-reproducible, and its jurisdictional facts are accurate to a fine grain — and its own fourth
review had already found essentially every issue this independent pass would find, including the one
substantive error.** This review is, at almost every point, *corroborating* the register's own
judgement rather than overturning it. The one refinement it adds is a sharper statement of the US
finding (F1/VB-06).

## Q3 (accurate & runnable) — the objective part, first

**Runs: fully.** In a clean, zero-third-party-dependency environment: `verify` → 11/11 hard checks,
0 lint, `--strict` green; `run_negative_tests` → 17 gates all bite; `schema_reference_crosscheck` →
54/54 adversarial mutations rejected, and (with `jsonschema`) identical to the reference on all 132
edges + 56 verdicts; `build_corridor_matrix` → `out/` byte-reproducible; `migrate_from_v0_9_92` →
deterministic rebuild whose SHA-256 matches the README's `e03a9efe…` **to the byte**. The only thing
that does not run is by design: the full register tree is unpublished (C1), so `compose(...)`, the
event calendar, the citable subset, and the ten build gates can be read in the papers but not run.

## Primary-source fact verification (the emphasis of this review)

Twelve load-bearing claims, each checked against a primary or primary-grade source. **Every one
checked out; several to licence-number, bill-calendar, or statutory-subclause precision.** More
tellingly, the points the register itself flags as uncertain were independently found to be handled
correctly.

| load-bearing fact | register / paper claim | primary-source check | verdict |
|---|---|---|---|
| **UK** SI 2026/102 | made 2026-02-04; **in force 2027-10-25**; regime-in-transition until then | legislation.gov.uk: "come into force on 25th October 2027 (the full commencement day)"; FCA final rules 2026-06-30 | ✅ primary |
| **Taiwan** VAS Act | third reading **2026-06-30**; 9 subsidiary items; ~21-mo transition; CBC+FSC dual approval → channelled Cat. II; issuer-yield prohibited | multi-source incl. FSC: "third reading on June 30, 2026"; nine sub-laws; early-2027 commencement; "barred from paying yield" | ✅ (confirms VB-R1) |
| **US** GENIUS effective date | (coded live / Cat. II) | OCC NPRM / Federal Register: effective on the earlier of 18 months (**2027-01-18**) or 120 days after final rules; mid-2026 only **proposed** rules (comments due 2026-05-01) | ⚠️ **F1 (below)** |
| **US** CLARITY H.R. 3633 | Calendar No. 423; committee 15-9; needs floor + reconciliation + signature | congress.gov: "Calendar No. 423 … Reported in Senate"; 15-9 on 2026-05-14 | ✅ primary |
| **US** "Tillis" naming | README previously asserted the *Tillis*–Alsobrooks naming "confirmed" | the two crossover votes are **Gallego and Alsobrooks**; no independent support for the Tillis half | ✅ v0.9.95 **retraction** (VB-01) is correct |
| **EU** MiCA threshold | v0.9.95 corrected "or" → statutory **"and"** (F-EU) | statute is conjunctive ("exceed 1 million transactions **and** … 200 million EUR"); practitioner literature is genuinely split ("… **or** … whichever first") | ✅ correction matches the statute; the split is exactly why flagging it was right |
| **EU** MiCA transitional | **2026-07-01** outer cap; ESMA no extension; intra-regime gating | transitional "can run until July 1, 2026," several states curtailed/skipped | ✅ |
| **Settlement blocs** | three experiments split by bloc; only Agorá is BIS-led; mBridge post-2024 is PRC-Gulf; Agorá includes Bank of Korea | BIS left mBridge 2024-10, now PBoC/HK/Thailand/UAE/Saudi, ~95% digital-yuan volume; Agorá seven central banks incl. Bank of Korea | ✅ primary (the §5.2 "correction" holds) |
| **Hong Kong** first licences | 2026-04-10 to HSBC + Anchorpoint; 36 applicants; no PRC-connected entity in the first tranche | HKMA: licences to Anchorpoint (FRS01) and HSBC (FRS02); 36 applications | ✅ primary (to licence number) |
| **China** 银发〔2026〕42号 | in force 2026-02-06; repeals No. 237 | verified in the fourth review against the PBoC 条法司 page (VB-04 closed) | ✅ |
| **CD1** reconciliation | 32/32/33/17/9/9 from the Atlas baseline via two deltas | recomputed by hand: baseline 32/32/27/8/11/22 → TW enacted (pre −9, T +9) → origin drag (blocked −2, pre −4, III +6) = **exact** | ✅ zero residual |
| **DG1/DG2** (v0.9.95) | close the distribution-conserving-permutation and stale-drift holes | reran the probe: the histogram-conserving `US→CN`-as-open mutation now **fails DG1** | ✅ the new gates bite |

The logic-to-fact mapping is sound: Taiwan's approval gate → channelled Cat. II, the UK's
enacted-not-commenced → `T` flipping to Cat. I on the gazetted day, China's ban → destination-blocked
plus outbound origin-drag into Cat. III, Japan's same-day reserve relaxation (a null-effect control)
vs foreign-stablecoin equivalence recognition (conditioned as Cat. II) — all match the primary
record, and the classifications are legally defensible.

### The one substantive error, independently confirmed and now stated precisely: F1 / VB-06

The data inconsistency the fourth review flagged is **materially present**, and the primary sources
confirm the reading behind it:

- **8 inbound-US edges are coded `II`** (live, via the GENIUS §18 comparability gate) **with no
  `as_of_timeline`** — i.e. treated as available today;
- **8 inbound-UK edges are coded `T`** with a scheduled **2027-10-25** trigger resolving to Cat. I.

But per the primary sources the GENIUS Act's operative provisions were **not in force on 2026-06-30**
(effective date ≤ 2027-01-18; foreign-issuer rules still proposed). By the paper's own discipline the
US sits in the **same** enacted-not-commenced position as the UK and Taiwan, so the 8 inbound-US edges
should read `T` with a **2027-01-18** scheduled trigger. The consequences, stated precisely (this is
the review's one sharpening over v0.9.95's own VB-06 wording):

1. the headline *"only one pending transition carries a future date (UK 2027-10-25)"* is **wrong** —
   there is a **second** dated horizon, and at **2027-01-18 it is EARLIER** than the UK's;
2. the two jurisdictions are **symmetric in count** (8 would-be-`T` US edges vs 8 `T` UK edges), so in
   §4.2 the US ranks at least level with the UK and, by the earlier date, **ahead** of it — not at
   medium sensitivity;
3. the "deliberately sparse forward map" has **two** date anchors, not one.

The register lists this as **VB-06 (high priority) but does not change the artifact**, because it is a
post-cutoff legal reading generated upstream from the unshipped signal table, and a downstream
override of 8 edges could introduce error. That process restraint is **defensible**; the substantive
conclusion stands — **the paper's central "single dated horizon" narrative is weakened by the
discipline the register applies everywhere else.** This is the place to adjudicate upstream with the
GENIUS primary text and then correct the headline and the §4 ordering.

## Q1 (complete underlying content) — corridor layer complete; two honest gaps

The corridor layer is complete and internally coherent (132/132, provenance partitioned, schema
executed, categories agree across directions, origin drag leak-free, distribution reconciled, bloc
tags structured and rechecked on all 132). Two gaps must be stated: the **physical** gap (C1 — the
152 node records, `analysis/*.json`, the compose engine, the event calendar, the ten build gates, and
the upstream scripts are not shipped, so the papers' most novel mechanism is not reproducible), and
the **expressive** gap (only **17/132** edges carry a temporal field; only **8** carry a scheduled
trigger, all pointing at the **one** UK event, so 1 of the paper's 11 triggers is materialized; the
three-axis model does not reach the corridor layer — `claim_class` and `binding_status` never appear
on an edge and `evidence_tier` covers **8/132 ≈ 6%**; and 9 authored edges cite the author's own
companion papers as `source.primary`, the class citation-purity is meant to exclude).

## Q2 (value maximized) — under-shown, and emphasized in the wrong place

The advertised "132 pairs and *why*" over-states: for the 99 edges from token-holding origins,
`class_code` is a **pure function of the destination, zero exceptions** (the 9 token-holder rows of
`out/corridor_matrix.md` are cell-for-cell identical), so the class dimension carries **12 numbers**,
not 132 judgements. The genuinely scarce, hard-to-reproduce assets are under-shown: the 17 KB
**HK→BR** seed edge; the **§4.5 yield line**, which is *under*-reported (MiCA Art. 50 from 2024-06-30,
plus Taiwan VASA and the Korea Ahn draft → ~5 jurisdictions, not ~1.5, now recorded as VB-R2); and the
six-way **trigger typology**, the most portable contribution, still without a `trigger_kind` field.
The most persuasive thing here is the **honesty infrastructure**: the queryable, CI-validated
verification backlog; the negative-test proof that every gate bites; the labelled-preview stance; the
living-developments tracker; and the fourth review's adversarial probe leading to the DG1/DG2 gates —
a "find your own hole and close it with a biting test" discipline that this review independently
confirms works.

## Logic — the positive conclusion, and one open point

`CD1` closes with **zero residual** (recomputed independently). Origin-drag-first is leak-free. One
logical point remains open (upstream): the **I/II criterion is under-determined** — by "each end
separately authorizable" the US is I; by "can the same token be recognized" the EU is II; the register
switches between the two silently, and the oft-cited `US→EU=I` vs `EU→US=II` is a "different
destination" restatement rather than a genuine directional asymmetry. This is of a piece with F1/F2.

## Recommendations (by return on effort) — unchanged from the fourth review, now doubly evidenced

1. **Publish `signal_table.json`** (12 jurisdictions × 4 signals, each with `record_ref` +
   `binding_status`), have builder / verifier / migration read it, and have the verifier **recompute
   all 132 `class_code`s from it**. One action closes F2's opacity, the probe's fabricated
   provenance/source mutations, and F6 (the verifier's partition constants are hand-copied from the
   builder — "cannot disagree by construction" is precisely why the verifier is not independent). It
   also rewrites the pitch to the more defensible "the deterministic expansion of 12 signals + one
   deep corridor." A concrete schema and integration are proposed in
   [`PROPOSAL_signal_table.md`](PROPOSAL_signal_table.md). **Populating `binding_status` for the US is
   where F1 gets resolved.**
2. **Adjudicate F1/VB-06 upstream with the GENIUS primary text.** If confirmed, set the US inbound
   edges to `T`, add a 2027-01-18 scheduled trigger, and correct the headline and the §4 ordering.
3. **Push the three-axis model down to the corridor layer** (at least `claim_class` / `binding_status`
   / `trigger_kind` on edges), and upgrade the §4.5 yield line from ~1.5 to the ~5 jurisdictions the
   evidence supports (VB-R2).

## Verdict

Runs, reproduces to the byte, and is accurate to a fine grain; the one substantive error is the
register's own flagged F1/VB-06, which this review confirms against primary sources and states more
precisely. What remains open is upstream and disclosed, not hidden. The register's most distinctive
quality — that its own adversarial review had already found what an independent auditor would — is
rare, and it holds up.

---

## Appendix V — commands re-run for this review

```bash
python3 tools/verify_corridors_directed.py            # 11/11, 0 lints
python3 tools/verify_corridors_directed.py --strict   # 11/11, exit 0
python3 tools/run_negative_tests.py                   # ALL GATES BITE (17 cases)
pip install jsonschema && python3 tools/schema_reference_crosscheck.py   # 54/54; two implementations agree
python3 tools/build_corridor_matrix.py                # out/ regenerates byte-identically
python3 tools/check_verification_backlog.py           # backlog well-formed
python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json   # [OK]; SHA e03a9efe…
```
