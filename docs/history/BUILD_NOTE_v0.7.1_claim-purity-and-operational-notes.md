# Build Note — v0.7.1: Claim purity for the citable subset

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** close a real, shipped leak in the
v0.7.0 lawyer-citable subset — a Tier-2 operational fact projected as binding law — without prematurely
building the per-clause substrate that v0.9.0 is for.

## 1. The finding (review was right, and falsifiable)

v0.7.0 defined the citable subset at **record** granularity: a record is citable iff
`claim_class == tier1_legal AND status == in_force AND evidence_tier == resolution_text`. The argument
for record granularity was that each record has a single clean load-bearing claim. That argument is
*almost* right — and the place it isn't was already sitting in the shipped subset.

`jp-epi-distribution-001` is genuinely citable: its load-bearing claim is the EPIESP inbound rule, a
proposition of law citable to the Payment Services Act. But the record had bundled a **Tier-2
operational illustration** — the USDC / SBI VC Trade admission, with approval and launch dates — into
*five* fields at once:

- the second sentence of `requirement_summary`;
- a `working_example` key in `requirement_structured`;
- `source.primary` (`"Payment Services Act; FSA approval of USDC admission via SBI VC Trade"`);
- the `pinpoint` (`"… USDC via SBI VC Trade (Mar 2025)"`);
- an `interpretation_note` calling it "the live proof."

Because `citable_law()` projects `source.primary` (as the instrument) and `pinpoint`, a lawyer calling
`citable_law('JP')` was shown a product approval and a launch date **inside the instrument string**,
badged as citable law. The record-level tag was defensible; the leak is structural — a record-level
projection cannot drop operational material from *inside* an otherwise-legal record.

A full audit of all 21 citable records (precise detector: named commercial entity, or a launch/approval
*event* with a date — not the legal verb "admitted," not case names like "Howey Co.") found exactly two
genuinely affected: `jp-epi-distribution-001` (all five fields) and `jp-epi-permitted_activity_yield-001`
(one hedged boundary-case sentence; its projected fields were already clean). The other three earlier
flags were false positives. So the leak is narrow and fixable in a point release.

## 2. The fix, and the line not crossed

The review proposed a "minimal" and a "full" version. The **full** version — every clause inside a
record carrying its own tier — *is* the v0.9.0 constraint substrate; building it now would be exactly
the premature-substrate move the sequencing is designed to avoid. So v0.7.1 ships a clean form of the
**minimal** version:

- **`operational_notes`** (new optional field): an array of `{ note, as_of?, source? }` for Tier-2
  illustration attached to a record. It is **omitted from the citable projection**, rendered on the
  site as a "Tier-2 · not citable as law" block (so the fact is preserved, not deleted), and is the
  per-record home for operational facts in legal dimensions that the v0.7.0 design anticipated but had
  not used.
- **The two records were cleaned**: load-bearing fields reduced to the legal claim; `source.primary`
  for the distribution record is now `Payment Services Act (Electronic Payment Instruments regime)`; the
  USDC/SBI material moved to `operational_notes` (the SBI press release rides along as its source). Both
  records remain citable — now cleanly. The legitimate open tension in the yield record stays in
  `interpretive_flag`, where it belongs.

One cell stays one record (no artificial splitting); only the *citable view* of that record is made
purely legal. This is also the natural seed of the v0.9.0 substrate, where each C-dimension predicate
will carry its own tier and `operational_notes` becomes per-predicate.

## 3. Enforcement (so it can't regress)

`check_citable_purity()` in `build.py` (hard error, CI-enforced): a citable record's `source.primary`
and `pinpoint` must cite the legal instrument only — no product/market **event**
(`launch`, `admission via`, `went live`, `rolled out`, …) and no named commercial counterparty
(SBI VC Trade, Circle, Progmat, …). The detector is deliberately conservative: legal verbs
(`admitted via registered EPIESP`) and case citations (`SEC v. Howey Co., 328 U.S. 293`) do not trip
it. *Negative test:* re-bundling the USDC/SBI approval into the instrument string fails the build with a
precise message; restored cleanly.

## 4. The liability this does *not* fix (stated plainly)

`claim_class`, the citable gates, and the signal-provenance discipline bound the blast radius of bad
data, but they do not retire the standing liability under the whole computed layer: **47 `tier1_legal`
cells are still `unset`** — transcribed from the Compliance Matrix, not yet confirmed against the
official text. Every `compose()` "9/9 corridors, 64/66 §5.14 categories" result rests on the
hand-curated signal table and those still-unverified cells. **No single feature retires this — only the
primary-source verification pass does**, which is why it is bundled into v0.9.0 and tracked in the
verification queue (`COVERAGE.md`, MCP `verification_report()`).

## 5. Sequencing (why the time engine is next, not the substrate)

The deeper idea is the constraint substrate (#3). But its prerequisites — the evidence split and the
signal-provenance gate — are exactly what v0.6.0–v0.7.1 delivered. The **time/event engine** (#1) is
therefore the now-unblocked, highest-applicability, lowest-shallowness-risk next major step: it
inherits the tier split for free (`compose(as_of=…)` filters to citable facts that carry their dates),
and it answers the question users actually ask ("blocked today, Category I after 2027-10-25"). The
substrate is the later, deeper thesis. The review's best contribution was flagging which two ideas were
under-weighted; its final ranking simply predated the two versions that already discharged the other
half of its plan.

## 6. Validation

- `build.py`: **117 records valid, 9 corridors, 66 pairs**; computed layer **9/9** + **64/66**;
  signal provenance clean; pre-regime `{KR, TW}` consistent; **citable subset = 21** (unchanged — the
  two records stay citable, now clean); `claim_class` matrix unchanged (108 legal / 9 operational).
- Negative tests pass: citable-URL strip; signal-provenance flip; **citable-purity re-bundle** — all
  fail the build as intended, all restored.
- Static site regenerated at v0.7.1; `operational_notes` embedded and rendered as a Tier-2 block; app
  JS passes `node --check`. Fresh-extract reproduces all metrics. Shim remains outside the package.
