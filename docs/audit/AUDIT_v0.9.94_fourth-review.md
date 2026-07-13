# CBSR corridor layer — fourth independent review (over v0.9.94)

_Independent re-audit of the directed-132 corridor layer and its toolchain, over the v0.9.94 release.
Every tool was re-run; all 132 edges were read field by field; an adversarial probe
(`probe_uncovered_gates.py`) was written; and every load-bearing legal fact was re-verified against
primary sources (not taken from the three bundled reviews). Review date: 2026-07-08. Reviewer:
independent, no relationship to the author._

One-line verdict: **the tool layer is honest and hash-reproducible; but the gates guard shape, not
semantics — and this project's entire value proposition lives in the semantics.** The reproducibility
story holds to the digit; the jurisdictional facts are highly accurate (several to a licence number);
but a class of semantic error slips every existing gate, and the single most important jurisdiction
(the US) is, on the reviewer's reading, misclassified at the snapshot.

This document records the review's findings and what v0.9.95 does about each.

## The three most important findings (missed by the three prior reviews)

### F1 — the US is not in force at the snapshot, yet is read as a live jurisdiction (major; DOCUMENTED, not changed)

GENIUS Act §20 sets the effective date at the earlier of 18 months after enactment or 120 days after
final rules — at the latest **2027-01-18**. §3(a)'s issuance prohibitions wait for that date; OCC's
2026-03-02 action was a *proposed* rule, with foreign-issuer provisions that "may not occur until
January 18, 2027," and as of 2026-06-19 the key foreign-issuer rules were still proposed. So on
**2026-06-30 the US sat in the same structural position as the UK and Taiwan**: enacted, with a
statutory effective date, not commenced. Yet:

- the paper's own §3.1 says *"must be in force, not merely located"* and §3.3 says *"enactment is not
  commencement"* — and on that basis it holds UK and TW at `T`;
- but it lets **11 inbound-US edges** resolve to **Category II** via GENIUS §18, a not-yet-operative
  mechanism;
- so the headline *"only one pending transition carries a future date (UK 2027-10-25)"* is **wrong**:
  the 2027-01-18 backstop is a statutory scheduled trigger — a **second** dated horizon, and (the fifth
  review sharpens this) an **earlier** one than the UK's. The 8 inbound-US edges (would-be `T`) and the
  UK's 8 `T` edges are symmetric in number, so by §4.2 the US ranks at least level with the UK and, by
  the earlier date, ahead of it.

This is the one place the register's own standard is not applied to its most important jurisdiction.

> **v0.9.95 response: documented, not changed.** This is a post-cutoff legal reading that this
> downstream repo cannot itself adjudicate, and the US classification is generated upstream from the
> (unshipped) signal table — reclassifying 11 edges here would be an unverified override that could
> introduce error. It is tracked as **`verification_backlog` VB-06 (high priority)** and flagged for
> upstream primary-source adjudication with the GENIUS text. If confirmed, the upstream fix is:
> US → `T`, add 2027-01-18 as a scheduled trigger, and correct the headline and the §4.1 ordering.

### F2 — the class dimension of 132 edges carries only 12 numbers of information (major; partially mitigated + documented)

For all 99 edges from non-tokenless origins, `class_code` is a **pure function of the destination,
zero exceptions** (mechanically confirmed; the 9 token-holder rows of `out/corridor_matrix.md` are
cell-for-cell identical). Consequences the reviewer draws, all confirmed:

- The *computed-vs-authored category reconciliation* has structurally **nothing to reconcile** at this
  layer — the 9 authored edges' categories equal the mechanical rule output, so
  `cross_check.category_mismatches` is necessarily empty (this is the **cause** behind the phenomenon
  README's N2 only described).
- `archetypes` is a deterministic relabel of `class_code`, so **`SC` (sovereignty-constrained) appears
  on I/II/T but is absent from `blocked` (into CN) and `pre_regime` (into KR)** — the two places
  sovereignty bites hardest.
- Copying an `f(destination)` fact 11 times invites drift — which is exactly finding **F-TW** below.

> **v0.9.95 response.** The drift risk is now caught by two new gates (see F3 / DG1 / DG2). The
> archetype-derivation asymmetry and the deeper "publish a signal table so the class is computed once,
> not copied" fix are **upstream** (see the shortest-path note); they are documented here and in the
> Open-findings table rather than papered over.

### F3 — 14 semantic mutations all pass `--strict` (major; two gates added, the rest clarified)

The probe holds every one of the (then) 9 hard checks' invariants while corrupting meaning:

| mutation | pre-v0.9.95 |
|---|---|
| distribution-conserving permutation: read `US→CN` as "Category I" | **not caught** |
| full header fabrication (incl. a fake `provenance.basis: every driving signal is tier1_legal`) | not caught |
| `evidence_tier` self-promoted to `resolution_text` | not caught |
| `source.primary` swapped for a fictitious `17 U.S.C. § 9999` | not caught |
| UK effective date → 1999-01-01 / delete all 17 `T` edges' `as_of_timeline` | not caught |

The first is the worst: an artifact reading **Mainland China as "fully open"** could score 9/9 + 0
lint, because `OD1` only looks at the origin and `CD1` only at the histogram — nothing looked at the
destination gate. The last two land on the methodology paper's heart: the schema's `evidence_tier`
description restated the citable-integrity and binding-status gates **that do not exist in this repo**.

> **v0.9.95 response.**
> - **`DG1` (destination-class homogeneity)** is added as a hard check: for token-holding origins, all
>   edges into a destination share one `class_code`. A histogram-conserving permutation must break
>   per-destination homogeneity, so `DG1` catches exactly the probe's first (and worst) mutation. A
>   negative test performs the distribution-conserving swap and asserts `DG1` fails while `CD1` passes.
> - **`DG2` (destination regime-status consistency)** is added: no destination may be described as
>   both regime-absent and regime-present across its inbound edges — closing the F-TW drift class.
> - **The `evidence_tier` schema description is corrected** to say plainly that the citable-integrity
>   and binding-status gates run in the FULL register build, not here; `evidence_tier` in this repo is
>   a declared, **unenforced** label. The remaining semantic mutations (fabricated provenance/source,
>   deleted timelines) require the upstream signal table and binding-status gate to catch at the fact
>   level; they are documented, not silently claimed as covered.

## Direct answers to the three acceptance questions

**Q1 (complete?)** No, and more so than C1 said: beyond the physical gaps (152 records, signal table,
event calendar, compose engine, ten gates), there is an **expressive** gap — 115/132 edges carry no
temporal field, only 2 of the paper's 11 triggers are materialized, and `today_class` is a hard-coded
constant, so the *Over Time* title has no runnable support in this package. The three-axis model does
not reach the corridor layer either: `claim_class` and `binding_status` never appear; `evidence_tier`
coverage is ~6%; and 8 authored edges' `source.primary` are the author's own working papers — the very
class citation-purity forbids.

**Q2 (value shown?)** Not fully, and emphasised in the wrong place. The advertised "132 pairs and
*why*" is a 12-number expansion; the genuinely scarce assets are buried: the 17 KB **HK→BR** seed edge
(four-dimensional analysis, `record_refs`, a `watch_list` precise to *Res 561, 2026-10-01*, and a
`reviewed_against` honest to "pinpoints NOT yet read against the official DOU text") — the one thing
hard to reproduce, and the only edge missing `archetypes` and `inbound_mechanism`; the **§4.5 yield
line**, which is *under*-stated (MiCA Art. 50 bans EMT interest and treats holding-period-linked
remuneration as interest — the clearest, earliest, most citable expression of the functional line, in
force from 2024-06-30 — and with Taiwan's VASA prohibition and the Korea Ahn draft, the evidence is ~5
jurisdictions, not the ~1.5 the paper claims); and the six-way **trigger typology**, the most portable
contribution, which lacks even a `trigger_kind` field.

**Q3 (accurate & runnable?)**
- Runnable: **yes.** Both SHA-256s match to the digit, `out/` reproduces byte-for-byte, the migration
  is deterministic, all negative tests bite. (Layer-2 oracle needs network; correctly isolated in CI.)
- Facts: **very high accuracy, several to licence-number level** — HK's first two licences 2026-04-10,
  Anchorpoint FRS01 / HSBC FRS02, 36 applications; SI 2026/102 made 2026-02-04, in force 2027-10-25;
  银发〔2026〕42号 verified at the PBoC 条法司 page ("本通知自发布之日起施行…237号同时废止", **VB-04
  closed**); Agorá seven central banks incl. Bank of Korea; CLARITY 309-page text 2026-05-12, 15-9 on
  2026-05-14, Calendar No. 423 on 2026-06-01.
- Accuracy breaks in three places, none catchable by the prior gates: **(1)** MiCA Art. 23's threshold
  written as "or" where the official text is conjunctive ("1 million transactions **and** EUR
  200 000 000, respectively") — **F-EU, corrected**; **(2)** F1 (US binding status); **(3)** the
  Taiwan prose self-contradiction — **F-TW, corrected**.
- **One item corrected immediately:** the README Headline asserted the *"Tillis–Alsobrooks"* naming is
  *correct* — but the two documented crossover votes are Gallego and Alsobrooks, and the author's own
  `verification_backlog` VB-01 marks the Tillis half unconfirmed. The README asserted, in the most
  visible place, exactly what the backlog says is unverified. **Retracted in v0.9.95.**

## Logic appropriateness — the positive conclusion

`CD1`'s arithmetic was independently recomputed and **closes with no residual**: baseline
32/32/27/8/11/22 → Taiwan enacted (pre −9, T +9) → six CN/TW/KR mutual edges' origin drag
(blocked −2, pre −4, III +6) = 32/32/33/17/9/9. Origin-drag-first is leak-free. The remaining
open logical point is that the **I/II criterion is under-determined**: by "each end separately
authorizable" the US should be I; by "can the same token be recognized" the EU should be II; the
register switches between the two silently, and the oft-cited `US→EU=I` vs `EU→US=II` is just a
"different destination" restatement. Documented as part of F1/F2; upstream.

## The shortest fix path (reviewer's recommendation)

**One action closes three problems**: publish `signal_table.json` (12 jurisdictions × 4 signals, each
with a `record_ref` + `binding_status`) as part of the artifact, have builder/verifier/migration all
read it, and have the verifier **recompute all 132 `class_code`s from it**. That closes F2's opacity,
the probe's provenance/source mutations, and **F6** (today `TOKENLESS` / `TRANSITION_DESTS` / `INFRA` /
`ATLAS_BASELINE` are hand-copied across three files — the builder comment's "cannot disagree by
construction" is the problem: the verifier is not independent, it is the builder's hand-copy). It also
rewrites the pitch from "132 pairs and why" to "**the deterministic expansion of 12 signals + one
genuinely deep corridor**" — a smaller, more defensible claim. This is **upstream** and out of scope
for this downstream package; it is the recommended next release.

## What v0.9.95 changed, in one list

- **Added gates** `DG1` (destination-class homogeneity) and `DG2` (destination regime-status
  consistency), each with a biting negative test; hard checks 9 → **11**.
- **Corrected facts in the artifact**: F-TW (Taiwan "draft" → enacted, consistent across all TW
  edges) and F-EU (MiCA Art. 58(3) "or" → statutory "and", with EBA-methodology-pending note).
- **Retracted** the README *Tillis* over-statement to match VB-01.
- **Closed VB-04** against the PBoC primary source; **fixed** the VB-04 CJK bracket typo and added a
  bracket-balance content check to `check_verification_backlog.py` (it had only checked shape).
- **Added backlog items** VB-06 (US classification, high priority), VB-07 (MiCA threshold), and
  resolved VB-R2 (MiCA Art. 50 strengthening the §4.5 yield line).
- **Clarified** the schema's `evidence_tier` description (gates run upstream, not here).
- **Documented** (not changed): F1 (US), F2 information content, the archetype/`SC` asymmetry, F6
  (verifier-is-builder's-copy), and the residual semantic mutations — all upstream, with the signal
  table as the fix.

What remains open is upstream and stated, not hidden: **C1** and its dependents **F1 / N2 / F2 / F6**,
the **M1** version-skew, and the primary-source pins in the backlog.

---

## Appendix V — commands re-run for this review

```bash
python3 tools/verify_corridors_directed.py            # 11/11, 0 lints
python3 tools/verify_corridors_directed.py --strict   # 11/11, exit 0
python3 tools/run_negative_tests.py                   # ALL GATES BITE (17 cases incl. DG1/DG2)
pip install jsonschema && python3 tools/schema_reference_crosscheck.py   # 54/54; two implementations agree
python3 tools/build_corridor_matrix.py                # out/ regenerates byte-identically
python3 tools/check_verification_backlog.py           # backlog well-formed (+ bracket-balance content check)
python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json   # [OK] current shape
```
