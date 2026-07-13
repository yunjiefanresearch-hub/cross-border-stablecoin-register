# CBSR corridor layer — ninth independent review (over v0.9.99), and what v0.10.0 does with it

_Independent re-audit of the directed-132 corridor layer, its toolchain, and the four companion
papers, over the v0.9.99 release. Every tool was re-run in a clean Python 3.12 environment; both ZIPs
and all four papers were expanded; the migration was replayed and its SHA compared against the
README's; the `jsonschema` reference oracle was installed and run; all 132 edges and the 12×12 matrix
were inspected; and every load-bearing jurisdictional fact was re-verified against a primary or
near-primary source rather than against the package's own claim that it had verified it. Review date:
2026-07-08. Reviewer: independent._

**One-line verdict on v0.9.99.** The engineering was flawless and the self-critique was the most
rigorous the reviewer has audited — and the package was, nonetheless, shipping a **known-wrong
class in its machine-readable layer** while the correction lived only in a human-readable errata
markdown. For a portfolio whose thesis is *"a legal reference consumed by machines must be citable by
construction,"* that is the deepest tension in the whole body of work, and it is the one thing that
had to close before publication.

---

## 1. Reproduction (unchanged verdict: exemplary)

| tool | result |
|---|---|
| `verify_corridors_directed.py` | 13/13 hard checks, 1 lint (`m7`), exit 0 |
| `verify_corridors_directed.py --strict` | exit 1 — **RED by design** (m7 / NF-1), as documented |
| `run_negative_tests.py` | 19 negative cases + positive control + non-mutation assertion, all pass |
| `schema_reference_crosscheck.py` | 54/54 adversarial mutations rejected; with `jsonschema` installed, **Layer 2 agrees with the reference implementation on all 132 edges and all 56 mutation verdicts** |
| `build_corridor_matrix.py` | all three `out/` views regenerate **byte-for-byte** |
| `migrate_from_v0_9_92.py` | deterministic rebuild from the v0.9.92 snapshot; SHA `9898d230…` **matches the README** |
| `check_verification_backlog.py` | well-formed |

Zero dependencies, offline, standard library. The claim is true. This is the strongest reproducibility
posture the reviewer has seen in an open legal dataset.

---

## 2. Primary-source verification of the load-bearing facts

The reviewer did **not** rely on the package's `status: confirmed` labels. Six load-bearing facts were
re-checked independently.

| fact | verdict |
|---|---|
| **GENIUS Act effective date** | **Confirmed, and the register is right against its own papers.** §20: the Act takes effect on the earlier of 18 months after enactment (**2027-01-18**) or 120 days after the primary federal payment stablecoin regulators issue final regulations. At 2026-06-30 only proposed rules existed: OCC NPRM (published FR 2026-03-02, comments closed 2026-05-01), FDIC NPRM and FinCEN/OFAC joint NPRM (both 2026-04-10), Treasury §4(c) NPRM (April 2026), NCUA proposal (February 2026). So *Feasibility* §3.2's *"The GENIUS Act is in force"* is **wrong**, and the "single dated horizon (UK)" headline is **wrong**. `VB-06` / errata `E1` / `F-US-1` are correct. |
| **Taiwan VAS Act** | **Confirmed and current.** Third reading 2026-06-30; commencement set separately; dual FSC **and** Central Bank approval for stablecoin issuance; issuer-paid yield barred; ~21-month operator transition; nine subsidiary items, FSC pointing to Q1 2027. The register's TW → channelled Category II treatment, `F-TW-2` and `VB-R1` all hold. |
| **PRC 银发〔2026〕42号** | **Confirmed against the PBoC primary source.** In force on publication 2026-02-06, repealing 237号; bar on unapproved offshore RMB-pegged stablecoin issuance and on onshore RWA tokenization; paired with CSRC 公告〔2026〕1号. `VB-04` closed correctly; CN = `blocked` is sound. |
| **MiCA Art. 143(3) transitional expiry** | **Highly accurate.** Staggered national windows beneath a 2026-07-01 outer cap; no extension; Member States may only shorten. §3.10's "the earliest deadline binds" nuance is right. Errata `F-EU-3` ("only Circle") is a correct catch. |
| **Settlement blocs** | **Structure confirmed; errata `E7`'s two corrections are right.** mBridge post-BIS-withdrawal (2024-10-31) includes **Thailand** — neither PRC nor Gulf. Project Agorá's seven include the **Bank of Korea** and the **Bank of Mexico** — neither is G7. The papers' §5.2 *thesis* (rival, non-overlapping bloc rails) is nonetheless strongly supported. |
| **HK first licence cohort** (the seed edge's live anchor) | **Confirmed against the HKMA primary source.** 2026-04-10, two licences, both HKD-referenced, 36 applications, under Cap. 656 (in force 2025-08-01). The `HK→BR` seed edge's four-dimensional analysis is the most valuable and least reproducible asset in the package. |

**Conclusion of §2.** The *register* side is accurate and current. The *paper* side carries several
real errors — and every one of them had already been correctly identified by the register's own errata
sheet. The register out-audits its own papers.

---

## 3. The three findings this review adds

### NF-9.1 (P0) — a methodology paper about machine-readable law was shipping a known-wrong class *in its machine-readable layer*

This is the finding that subsumes E1, E8, F-US-1 and the eighth review's NF-1, and it is a **structural**
observation about the delivery, not a new fact.

Three materials ship together, and they disagree with each other:

| a consumer that reads … | receives … |
|---|---|
| only the **papers** | "GENIUS is in force"; "a single dated horizon (UK)"; "a PRC-and-Gulf group"; "only Circle" |
| only the **machine-readable artifact** | `→US` = Category `II` — a live comparability gate — which is **wrong**, and `TW→CN` / `KR→CN` = `III` (*"partnership route"*) into a prohibition, which is **wrong and optimistic** |
| the **`PAPER_ERRATA.md` + backlog prose** as well | the fully corrected picture |

So the corrections existed — meticulously, honestly, with priorities and drafted replacement wording —
**in the one format the papers' own thesis says a consumer cannot be relied on to read.** *Citable by
Construction* §1.1: *"A machine brings none of that … the judgment the human reader supplied tacitly
must be supplied explicitly, encoded in fields, enforced at build time."* The errata were prose. The
artifact was the field. The field was wrong.

Two micro-findings sharpen it:

- **`VB-06`'s own `claim` field carried the stale value.** It read *"11 inbound edges read Category II,
  driven by GENIUS §18"* while its `confirmed` field (correctly) discussed **8** edges and **§20**. A
  machine querying the backlog's `claim` field alone — the obvious field to query — got the wrong count
  and the wrong section.
- **Three version strings coexist** (register `0.9.9` / papers `0.9.91` / repo `0.9.99`). `VERSIONS.md`
  records the skew honestly, but an external consumer still meets three numbers for one thing.

**Disposition in v0.10.0: RESOLVED.** The artifact now carries the corrected classes, the corrected
prose, a typed trigger, a `class_basis` stating the binding status of the instrument the class rests
on, and a `CF1` anchor that fails the build if the old coding returns. `VB-06`'s `claim` field is
fixed. The remaining contradiction is one-directional and stated as such: **the register is now right
in its data, and the papers are wrong in their prose** — which is exactly the direction the errata
sheet is designed to close.

### NF-9.2 (P0) — the eighth review's own NF-2 arithmetic was itself an artefact of the bug it was reporting

The eighth review recomputed §4.2's sensitivity ordering **against the shipped artifact** and concluded
that Taiwan and Korea are "tied at 20 edges each" and that Mainland China "is not insensitive." Both
conclusions are downstream of the origin-drag-first rule that NF-1 says is wrong. Recomputed under the
**published Atlas's destination-first precedence**:

| jurisdiction | edges reclassified by its trigger | inbound | outbound |
|---|---:|---:|---:|
| **KR** (DABA enacted + commenced) | **21** | 11 | 10 |
| **TW** (VAS Act commencement) | **18** | 9 | 9 |
| **UK** (2027-10-25, gazetted) | **8** | 8 | 0 |
| **US** (≤ 2027-01-18, outer cap) | **8** | 8 | 0 |
| **CN** | **0** | 0 | 0 |

So §4.2's two headline claims — *"South Korea is the single highest-sensitivity jurisdiction"* and
*"Mainland China is insensitive"* — are **both true**, but only once NF-1 is fixed, and Taiwan is
second rather than tied. **The correction to the artifact rescues the paper's prose.** That is
independent evidence for resolving NF-1 in favour of the Atlas, and it is a nice illustration of why a
sensitivity ordering should be computed, not argued.

Note the second, distinct ordering the paper conflates with this one: **the dated horizons arrive
US (≤ 2027-01-18) before UK (2027-10-25)**, and Taiwan and Korea carry no date at all. A forward map
must report both orderings; §4.2 reports neither cleanly.

**Disposition in v0.10.0: RECOMPUTED, not documented.** `tools/compute_sensitivity.py` applies each
pending change in law to a copy of the signal table, re-derives all 132 classes, and counts the moves.
Output: `out/corridor_sensitivity.md`, regenerated in CI.

### NF-9.3 (major) — the "declared delta" mechanism was laundering a rule reversal as a fact

`CD1` reconciled the artifact's distribution to the Atlas baseline via *"two declared deltas — Taiwan
enacted, and origin drag on the CN/TW/KR mutual edges."* The first is a **fact update** (a jurisdiction's
binding status moved). The second is a **rule reversal** (the classifier disagrees with the published
Atlas). Both were recorded in the same ledger, in the same sentence, with the same standing — which is
how a rule reversal survives eight reviews inside a package whose entire discipline is to separate
kinds of claim from one another.

The eighth review found the *symptom* (`OD1` treats the rule as an axiom; `CF1`'s anchors all sat on
one side of it). NF-9.3 names the *mechanism*: the reconciliation ledger had no type system. A delta
that changes what the rule *is* must never be enterable in the same field as a delta that changes what
the *world* is.

**Disposition in v0.10.0: RESOLVED.** Both `CD1` deltas are now fact updates (Taiwan enacted; the US
enacted-not-commenced). The rule itself is published as data-plus-code (`data/signal_table.json` +
`tools/class_rule.py`) and re-derived by `PR1`, so a rule change is a **code and table diff**, visible
in review, and can no longer be entered as a distribution footnote.

---

## 4. Answers to the three standing questions

### Q1 — Is a complete underlying application shipped? *No, but the gap narrowed materially.*

What was absent in v0.9.99 and is **now present**: the per-jurisdiction **signal table** (the ~12
signals that drive everything), the **class rule** as executable code, a **recompute** that proves the
132 classes follow from them, the **signal-provenance** and **binding-status-cap** gates the
methodology paper argues for, `claim_class` and `binding_status` as first-class schema fields, and a
**recomputed sensitivity** view.

What is **still absent** (finding **C1**, unchanged in kind): the 152 **node records** (so `record_ref`
is null everywhere — `VB-11`), `compose(origin, destination, as_of)` over a full **event calendar**,
the **lawyer-citable subset** and its ten build gates, and `analysis/compatibility.json` (so the
flagship **computed-vs-authored category divergence** of *CbC* §5.2 still cannot be reproduced —
finding **N2**). Publishing that tree remains the single highest-value next step.

### Q2 — Does the package maximise its value / applicability / functionality? *The tool layer, yes. The data layer is now honest about being thin — and less thin.*

The 12×12 matrix printed out makes the structural fact visible: every destination column is
homogeneous, so the 99 token-holding-origin edges are literally `f(destination)`. The README's
"calibrated pitch" said so. **v0.10.0 makes it a theorem rather than a confession**: the 12 rows are
published, the expansion is executable, and a reader can now check the claim in one command instead of
taking it on trust. The eighth review's sharper version of the complaint — that 25% of the edges rested
on a `tier2` market signal — is closed: origin drag reads a legal signal, and the market signal is
*proved* inert by flipping it.

The genuinely scarce assets are unchanged and remain the reason to read this repository: the `HK→BR`
seed edge, the §4.5 yield-line convergence (now carried in the signal table for five jurisdictions),
the six-way trigger typology (now expressible in the schema), and the honesty discipline.

### Q3 — Does it run, and are the facts right? *Yes, and yes on the register side.*

See §§1–2. Everything runs, reproduces byte-for-byte, and every load-bearing legal fact checks out
against a primary or near-primary source. The errors were in the **papers**, and in **one column of the
artifact** — and both were already correctly diagnosed by the package's own machinery. The remaining
work is to make the papers say what the register already knows.

---

## 5. What v0.10.0 does not fix, and should say so

- **C1 / N2 / VB-11.** The tree is still unpublished. `record_ref` is null on all 60 signals.
- **VB-09** (new, major). Whether a US state-qualified issuer or a UK authorized EMI holds an
  *"exportable, comprehensively authorizable private token"* in the Atlas's sense. It decides **22
  outbound edges**. v0.10.0 does not settle it; it **states** it, as a `tier1_legal` signal with an open
  backlog item, instead of letting a market record decide it silently. The reviewer regards making this
  decision visible as more valuable than making it confidently.
- **The `CF1` poison remains partial.** Three destination classes are anchored to externally verified
  facts. A coherent lie about an **unanchored** signal (say `BR.inbound_gate`) still passes every gate,
  because `PR1` proves *derivation*, not *truth*. Only a primary-source pass over the remaining nine
  jurisdictions closes it. The README says exactly this.
- **`CD1` is still a checksum**, not an independent dimension: because class is `f(destination)`, it
  cannot fail unless `DG1`/`OD1` already have. The 16 hard checks are not 16 independent dimensions
  (findings C / NF-6).
- **The papers.** Every item in `PAPER_ERRATA.md` remains a paper-side change. **E1, F-US-1, E8 and
  NF-2 now gate publication more sharply than before**, because the artifact has moved and the papers
  have not: the two materials still contradict each other, in the opposite direction.

---

## 6. Priorities after v0.10.0

**P0 (gate publication):** the paper-side corrections — E1 + F-US-1 + E8 (two dated horizons, US
first; "GENIUS is in force" is wrong; the claim-class rewrite), NF-2 (§4.2 rewritten against
`out/corridor_sensitivity.md`), E2 (the §3.7/Matrix `or` → `and`), E4 (Matrix v0.9.8, Taiwan).

**P1:** C1 — publish the node records and the event calendar, populate `record_ref` (`VB-11`), and turn
`compose(as_of)` on. Resolve **VB-09** against the primary instruments. F-JP-1 (the JFSA
information-sharing condition — it *strengthens* §5.3).

**P2:** extend `CF1`'s anchors as the remaining nine jurisdictions are primary-verified; reconcile the
Atlas's §3.3-vs-edge-register mismatch on Korea's override (`VB-10`); collapse the three version
strings; state in the README that the 16 hard checks have effective rank ≈ 7–8.

---

## 7. Verdict

The eighth review called this "the most honest package I have audited, and now honest about one more
thing." The ninth adds: **honesty about a defect and correction of the defect are different acts, and
a methodology paper about machine-readable law is judged on the second.** v0.10.0 performs it. The
core classification rule is now published, destination-first, derived from a table whose own provenance
gates run in CI, and demonstrably independent of every market fact in the register. The one column that
was wrong is right, anchored, and regression-tested.

What remains is no longer a contradiction inside the register. It is the ordinary work of making four
papers say what their register already knows, and of publishing the tree.

---

## Appendix — commands re-run for this review

```bash
# over v0.9.99 (the reviewed release)
python3 tools/verify_corridors_directed.py            # 13/13; 1 lint (m7); exit 0
python3 tools/verify_corridors_directed.py --strict   # exit 1 — RED by design
python3 tools/run_negative_tests.py                   # 19 cases; ALL GATES BITE
pip install jsonschema && python3 tools/schema_reference_crosscheck.py   # Layer 2 agrees, 132 + 56
python3 tools/build_corridor_matrix.py                # out/ byte-identical
python3 tools/migrate_from_v0_9_92.py --in data/legacy/... --out /tmp/x   # SHA 9898d230…

# over v0.10.0 (this release)
python3 tools/verify_corridors_directed.py --strict   # 16/16; 0 lints; exit 0 — no --allow-lint
python3 tools/run_negative_tests.py                   # 31 cases; ALL GATES BITE
python3 tools/recompute_classes.py --prove-tier2-inert
python3 tools/compute_sensitivity.py
python3 tools/schema_reference_crosscheck.py          # 188/188 rejected; 192 verdicts agree
```
