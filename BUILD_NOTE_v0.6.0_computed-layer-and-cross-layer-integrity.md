# Build Note — v0.6.0: From a queryable mirror to a self-checking, computable graph

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** enforce cross-layer integrity; give
the corridor layer a real schema; take the first step from *storing* the analysis to *computing* it.

v0.5.x put the Architecture's analysis and the Atlas's corridors into the register as data. But it put
them in as **two independent transcriptions**, linked by a `compatibility_pair` foreign key that
nothing enforced. The cost was exactly the failure mode flagged in review: **seven of nine corridors
had interaction sets that silently contradicted the §5.14 matrix row their foreign key pointed to**,
and `us-eu` even contradicted itself (field `[A,C,D]` vs a secondary note reading "B, D"). The matrix
was an authored lookup table, not a computed output, and the four analysis MCP tools retrieved but did
not *compute*. v0.6.0 closes that gap.

---

## 1. The diagnosis (what review was right about)

The two layers were a **mirror**, not a **graph**. CI's drift-check guaranteed "derived artifacts match
their source," but could not guarantee "the two hand-authored layers agree with each other," because
they were two independent sources. The seven contradictions were real and sitting in the data:

| corridor | edge sets | §5.14 row | row sets |
|---|---|---|---|
| us-eu / eu-us | [A,C,D] | EU-US | [B,D] |
| us-hk | [A,C,D] | HK-US | [A,C] |
| jp-us / us-jp | [A,C] | JP-US | [A,C,E,F] |
| sg-hk | [A,D] | HK-SG | [A,F] |
| hk-cn | [A,D,F] | CN-HK | [A,F] |
| hk-us | [A,C] | HK-US | [A,C] ✓ |

Some of this divergence is **legitimate**: a directed edge (US→EU, read at the EU inbound gate) can
have different operative interaction sets than the undirected §5.14 pair EU-US, because the Atlas and
the Architecture are different-granularity documents. But a register that exposes both as queryable
data and *neither reconciles nor flags the difference* gives two answers to "what governs US↔EU" and
tells the user nothing. The fix is to **declare and enforce**, not to overwrite a faithful source.

---

## 2. Cross-layer integrity (the cheapest, highest-value fix)

`build.py` now runs `check_cross_layer()` on every build (and in CI). For each corridor with a
`compatibility_pair`:

1. its `compatibility_category` **must equal** the §5.14 row's category — a hard error otherwise; and
2. if its `interaction_sets` differ from the row's, it **must** carry a `divergence` field
   (`against_pair`, `pair_interaction_sets`, `edge_interaction_sets`, `reason`) — else the build fails.

The seven contradictions are now **seven declared divergences**, auto-derived in
`scripts/build_corridors.py` from the live matrix (so they can never drift out of sync), each
explaining that the directed-edge sets come from the Atlas read at the inbound gate while the
undirected sets come from Architecture §5.14. `hk-us` and `hk-br` match exactly and carry no
divergence. The `us-eu` self-contradiction is gone: secondary citations that listed an interaction-set
tail are sanitised to point at the `divergence` field. Stripping any divergence now fails the build
with a precise message — the contradictions can never silently return.

---

## 3. A real corridor schema

The corridor layer had **no schema** — `build.py` appended anything with a `corridor_id`. It also had
two ad-hoc shapes (the rich leg-by-leg `hk-br`; the flat directed edges). v0.6.0 adds
`corridor.schema.json`, enforced like the node schema, with **one schema and two validated shapes** via
a `schema` discriminator: `corridor/v3-directed-edge` and `corridor/v2-rich`. The `hk-br` anchor was
brought under the schema (given the directed-edge foreign-key fields while keeping its
`boundary_analysis`/`watch_list`). The local validation shim gained `const`/`allOf`/`anyOf`/`oneOf`/
`if`-`then`-`else` so it enforces the conditional shape requirements exactly as real `jsonschema` does
in CI.

---

## 4. The computed layer — compose(): the composition problem as a running function

This is the step from mirror to graph. The Architecture's central claim is that cross-border
feasibility is a *composition* of single-jurisdiction constraints; the Atlas's classifications are the
hand-output of that composition. `scripts/compose.py` makes it a function.

- It derives a **per-jurisdiction signal table** — `regime_status`, `inbound_gate` type,
  `exportable_token`, `egress_override` — each annotated with the node record that justifies it. The
  `pre_regime` set is read **programmatically off the records** (`issuer_pathway.status == proposed`)
  and cross-checked against the signal table; `build.py` fails if they disagree.
- `compose_directed(origin, destination)` applies the Atlas's own algorithm (§3.2): origin drag first
  (no exportable token ⇒ Category III), then the destination-determined inbound class.
- It **diffs computed-vs-authored**: the 9 authored corridor `feasibility_class` values, and (via a
  documented reduction) the 66 authored §5.14 categories.

The result is the honest, useful kind: it reproduces **9/9** authored corridors and **64/66** §5.14
categories from first principles. The **2 disagreements are a finding, not a bug** — both are the
`uk_regime_in_transition` cause: the Atlas flags the UK as not operative until 2027 (`T`), while the
Architecture's §5.14 treats US-UK and EU-UK as cleanly bridgeable Category I. That is precisely the
cross-document divergence the engine exists to surface (is the data wrong, or does the composition rule
need refining?). The layer is a labelled **preview** over a deliberately small rule set — not asserted
authoritative, and explicitly not a complete derivation of §5.14 — embedded at `analysis.computed`,
reported in the build output and `COVERAGE.md`, and exposed by the new `compose_corridor` /
`explain_feasibility` MCP tools (the first tools that *compute* rather than retrieve).

---

## 5. The smaller findings, closed

- **Verification queue.** `COVERAGE.md` and the new `verification_report()` MCP tool now expose the
  backlog explicitly: the **51 `unset` legacy records** (US/EU/UK/SG/HK/CN/BR), broken down by
  jurisdiction, are named as the next verification target.
- **Build-note contradiction.** The v0.5.0 build note's "resolution_text 0 / url 10/117 / does not
  promote tier" prose is now fronted by a superseded banner pointing at the v0.5.1 pass; the
  authoritative figures always live in the generated `COVERAGE.md`.

---

## 6. What is still open (declared, not hidden)

- The corridor layer is **9 of 132** edges. The full directed matrix is the next breadth step
  (compute first, then verify per edge).
- `compose()` is a **preview** over the destination-determined core rule; broadening the rule set
  (and treating the UK-transition finding) is future work.
- The **51 `unset` legacy records** remain unverified — itemised in the verification queue.

## 7. Validation

`python build.py` (under the local `jsonschema` shim) reports: **117 records valid, 9 corridors
(schema-validated), 66 compatibility pairs, 7 declared cross-layer divergences, computed layer 9/9
directed · 64/66 undirected, 2 findings, 0 draft cells.** Stripping a divergence, or breaking a
corridor's category, fails the build. The maintainer should run real `python build.py` (with
`jsonschema` installed) and the CI workflow as the final gate before tagging.
