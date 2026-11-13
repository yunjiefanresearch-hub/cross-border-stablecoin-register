# Build Note — v0.9.0: The constraint substrate

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** build feature #3 — derive corridor
feasibility by composing per-jurisdiction C1–C8 constraint poles through the six interaction-set rules,
as a real, enforced, *additive* layer. Deliberately **not** bundled with the full 132-edge matrix or the
verification pass (v0.9.x), to avoid trading depth for premature breadth.

## 1. What the substrate is, and why it is the deep one

v0.6–v0.8 computed feasibility from a hand-curated per-jurisdiction **inbound gate** (one value per
jurisdiction) and then dated it. That is a shortcut: it collapses eight distinct constraints into a
single gate. The substrate is the thesis the shortcut stood in for — each `(jurisdiction × constraint
C1–C8)` is a structured **pole**, and `compose_via_substrate(origin, dest)` derives a corridor's class
by composing the two jurisdictions' poles **through the six interaction-set rules** (§2.9):

- origin drag (C1 `exportable_token`): no exportable token ⇒ III;
- destination inbound from C7×C1 (Set D reserve×monetary-sovereignty, Set C bank/non-bank×issuer):
  `prohibition` ⇒ blocked, `channelled` ⇒ II, `usage_capped`/`open` ⇒ I;
- the **Set A** overlay (C1×C6): if the origin's data-sovereignty blocks supervisory sharing, the
  destination's issuer eligibility is unsatisfiable ⇒ escalate to III (the Pattern-A mechanism).

## 2. The discipline that keeps it honest (and the scope line)

The whole sequencing — #2 before #1 before #3 — was about not letting a deeper feature manufacture a
deeper liability. The substrate honours that in three ways:

1. **Provenance, one level deeper.** Every pole cites the `tier1_legal` record(s) it is transcribed
   from; `build.py` rejects a pole backed by a `tier2_operational` record. *Negative test:* pointing a
   pole at `jp-epi-implementation_status-001` (tier2_operational) fails the build.
2. **It never guesses.** A pole exists only where a record backs it; where a load-bearing pole is unset,
   the engine returns **`indeterminate`** and names the missing poles. So coverage is an honest readout,
   not a façade: **22/96 cells populated**, **1/9 authored corridors derivable** today. The cells are
   missing (US/EU C1 were never recorded) or `tier1_legal`-but-unverified (the 47-cell backlog) — which
   is precisely why most corridors are indeterminate.
3. **Cross-checked, not asserted.** Where the substrate yields a *definite* class it must equal the
   signal-table `compose()`; `build.py` fails on a disagreement (a genuine divergence must be declared).
   *Negative test:* flipping JP C7 from `channelled` to `open` makes the substrate derive HK→JP = I
   while the signal engine says II — the build fails on the cross-check. Both restored.

The scope line: I did **not** author records or poles just to make more corridors derivable. The
indeterminate frontier is the truth, and it makes the verification pass *load-bearing* rather than
cosmetic — the substrate stays dark until the cells are populated and verified.

## 3. The worked proof: the {HK, CN, JP} triangle

These three jurisdictions each have the C1 + C7 cells the rules need, forming a closed, fully-backed
triangle. All six directed edges derive from constraint poles and agree with the signal engine:

| edge | substrate | via | signal |
|---|---|---|---|
| HK→JP | **II** | Set D — Japan's *channelled* C7 (EPIESP reserve channel) | II |
| JP→HK | **I** | Sets C+D — Hong Kong's *open* C7 (dual authorization) | I |
| HK→CN | blocked | Set C — CN C1 prohibition | blocked |
| CN→HK | III | origin drag — CN has no exportable token | III |
| JP→CN | blocked | Set C — CN C1 prohibition | blocked |
| CN→JP | III | origin drag | III |

HK→JP and JP→HK are the non-degenerate cases: a Category II and a Category I **derived** from reserve /
monetary-sovereignty poles, not looked up. (Set A is implemented and unit-correct but *latent* at this
coverage — it needs an exportable-yet-data-restricted origin to fire, which no populated cell currently
is; the §3 controlling-person variant of Pattern A is a refinement for later.)

## 4. Surfaces: MCP (20 → 22) and the site

- **MCP**: `constraint_substrate(jurisdiction?, constraint?)` and `compose_via_substrate(origin,
  destination)` (computes live for any pair; returns per-set verdicts and the cross-check, or
  `indeterminate` with the missing poles). Verified via the mock: HK→JP = II (agrees), JP→HK = I
  (agrees), HK→CN = blocked (agrees), US→EU = indeterminate (missing US.C1, EU.C1).
- **Site**: a "Feasibility, composed from constraints" section with the coverage stats and the worked
  triangle.

## 5. The liability, restated — and now operationalised

The standing liability has been stated since v0.7: **47 `tier1_legal` cells are `unset`**, and every
`compose()` result rests on the hand-curated table beneath it. The substrate does not fix this — it
**operationalises** it: the substrate's coverage *is* the inverse of the backlog, so "light up the
substrate" and "retire the liability" are now the same task (the v0.9.x verification + cell-authoring
pass). That is the honest reason the verification pass is split out and named, not folded in here.

## 6. Validation

- Full pipeline green at v0.9.0 (order: build_analysis → build_corridors → compose → **substrate** →
  build → build_site): **117 records, 9 corridors, 66 pairs**; computed layer 9/9 · 64/66; time engine
  4 events, caveated 8→0; **substrate 22/96, provenance clean, cross-check clean, authored derivable
  1/9**; citable subset 21.
- Negative tests pass (all fail the build as intended, all restored): citable-URL strip;
  signal-provenance flip; citable-purity re-bundle; event tier2 basis; contingent-with-date;
  **substrate pole on a tier2 record**; **substrate pole diverging from the signal compose()**.
- Static site regenerated at v0.9.0; substrate section renders; app JS passes `node --check`. Fresh
  extract reproduces all metrics. The local `jsonschema` shim remains outside the package.
