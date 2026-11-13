# Build Note — v0.9.1: The verification harness (earned tiers + the scoped pass)

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** make the primary-source verification pass
— the work that lights up the v0.9.0 substrate and retires the standing liability — *real, safe, and
scoped*, without fabricating any verification.

## 1. The honest constraint

The liability has been named since v0.7: **47 `tier1_legal` cells are unverified** (`evidence_tier`
unset), and every `compose()`/substrate result rests on them. The obvious "next step" is to verify them.
But verification means confirming each claim against the official statutory text, and an inventory of the
47 cells shows they uniformly carry `source.primary` + `pinpoint` **but no `source.url`** — i.e. they
genuinely require fetching and reading the official text, which is external work. This environment has no
network, and citations must never be machine-generated. Faking a URL or a "confirmed" tier would be
worse than an honest `unset`. So v0.9.1 ships the **harness**, not fake verifications.

## 2. `evidence_tier` is now earned, not asserted

`build.check_evidence_tier_requirements` enforces necessary conditions, grounded in the dataset's real
tier semantics (all 23 `resolution_text` and 14 `mixed` records carry url + pinpoint; all pass):

- `resolution_text` ⟹ `source.url` + `pinpoint` + `last_reviewed`
- `mixed` ⟹ `source.url` + `pinpoint`
- `firm_summary` ⟹ `pinpoint`

These are *necessary*, not *sufficient* — the tier stays a human judgment, but it can no longer be
claimed without the corroborating provenance, so a promotion only lands if the evidence is actually
present. *Negative tests:* claiming `resolution_text` after stripping the `url` fails; a
`verification.method=official_text` on a `firm_summary` record fails (method/tier inconsistency). Both
restored.

## 3. The verification worklist — the liability as an actionable checklist

`scripts/build_worklist.py` → `analysis/verification_worklist.json` turns "47 unset" into a precise,
per-cell, machine-readable worklist: for each unverified record, the instrument + pinpoint and exactly
what is missing to reach each tier. The headline:

- **47 `tier1_legal` cells unverified, all lacking a `source.url`**;
- by jurisdiction: **HK 10 · SG 10 · UK 10 · CN 8 · US 5 · EU 4** — and notably JP/AE/CH/BR/TW/KR are
  already fully tiered, which is exactly why **JP is the substrate's most-derivable node** (the {HK, CN,
  JP} triangle works because JP's cells are verified);
- by constraint: **C2** (reserve/capital) is the largest bucket (12), then C1/C3.

Exposed by the new MCP tool `verification_worklist(jurisdiction?)` (22 → 23 tools).

## 4. The `verification` block — a safe, auditable promotion path

New optional record field `verification` `{verified_by, verified_on, method (official_text |
practitioner_corroboration), against {instrument, url, pinpoint}, excerpt?}`, schema-validated. It is the
audit trail of *how* a cell was confirmed, so a future promotion is traceable rather than a bare tier
bump. Demonstrated by formalizing the provenance of an **already-confirmed** cell —
`jp-epi-monetary_sovereignty-001`, the JP C7 (`channelled`) pole behind the substrate's **HK→JP = II**
derivation — using the `source` already in the record, not new evidence. This shows the format and that
the gate accepts a consistent block; it invents nothing.

## 5. What this version deliberately does NOT do

It does not promote any of the 47 cells. The inventory shows none can be legitimately promoted from
inside the dataset (all lack a url, none carry verbatim text or practitioner corroboration). Promoting
them requires the external primary-source pass — which the harness now scopes and guards. The substrate
coverage (22/96), the citable subset (21), and all counts are therefore unchanged. This is the honest
increment: the machinery that makes the pass safe, not a façade of completed verification.

## 6. Validation

- Full pipeline green at v0.9.1 (order: build_analysis → build_corridors → compose → substrate →
  **build_worklist** → build → build_site): 117 records, 9 corridors; computed 9/9 · 64/66; time engine
  caveated 8→0; substrate 22/96 provenance+cross-check clean; **47 cells worklisted, evidence_tier gate
  enforced (all 117 pass)**; citable 21.
- Negative tests pass (all fail the build as intended, all restored): the seven prior gates, plus
  **claim `resolution_text` without a url** and **a verification/tier inconsistency**.
- Static site regenerated at v0.9.1; the substrate section's "Verification frontier" line renders; app
  JS passes `node --check`. Fresh extract reproduces all metrics. The local `jsonschema` shim remains
  outside the package.
