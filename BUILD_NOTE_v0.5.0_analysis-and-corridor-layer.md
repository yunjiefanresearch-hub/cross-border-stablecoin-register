# Build Note — v0.5.0: Making the analysis queryable

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** encode the Architecture working
paper's analytical payload as a queryable **analysis layer**; expand the **corridor layer** from one
edge to nine; add CI; close every concrete finding from the external audit.

This note answers the two questions an external audit put to the register: **(1) does it contain the
full content of the three companion works, and (2) does it maximize the value, applicability, and
functionality of the underlying research?** The v0.4.0 answer to (1) was "the Matrix node layer at
high fidelity, but the Architecture paper only as *vocabulary* and the Atlas only as a *single
example*." That is the gap this release closes — and closing it is also most of the answer to (2),
because the Architecture paper's analytical payload *is* the work's headline contribution.

---

## 1. The diagnosis (what the audit was right about)

Three source layers, three very different encoding depths in v0.4.0:

| Source layer | v0.4.0 encoding | Why it mattered |
|---|---|---|
| Compliance Matrix (node data, 12×15) | **High** — 117 records | The substrate was well-served. |
| Architecture (analysis) | **Low** — only the C1–C8 vocabulary, in `constraint_ref` | The paper's *actual* contribution — the composition-problem apparatus: six interaction sets, three architectural patterns, the §5.14 pairwise compatibility matrix, the §7 open questions — lived only in PDF prose. A reader querying the dataset got node facts but not the analysis that composes them. |
| Corridor Atlas (edge data, 132) | **Very low** — 1 of 132 edges | "Corridor layer" was a single worked example, not a layer. |

The audit's framing was fair: the register was transparent about these boundaries (the roadmap
deferred the matrix and the corridor expansion), but transparency about a gap is not the same as
closing it. The single highest-value action was to make the §5.14 matrix and its surrounding
apparatus **queryable**, because that is the contribution most underserved by prose-only encoding.

---

## 2. The analysis layer (the headline change)

A new layer sits beside the node layer: four structured, schema-validated JSON artifacts in
`analysis/`, folded into `dataset.json` under `analysis`, built by `scripts/build_analysis.py`, and
validated by `build.py`.

- **`compatibility.json`** — the **§5.14 pairwise compatibility matrix in full**: all **66** unordered
  pairs of the twelve jurisdictions, each with category (I / I/II / II / III), operative interaction
  sets (A–F), a Category-III axis where applicable, and the binding constraint. The category
  distribution (34 I/II, 30 III, 2 pure I) reproduces the paper. The builder self-checks that every
  C(12,2) pair is present; `build.py` re-checks categories, interaction sets, and jurisdictions.
- **`interaction_sets.json`** — the six constraint-interaction sets (§2.9), each with its constraint
  pair, joint-binding mechanism, and worked example.
- **`architectural_patterns.json`** — the three-pattern PRC typology (§3.3), the three-layer routing
  architecture (§4/§6), the §4.4 five-factor operational test, and the six design principles.
- **`open_questions.json`** — the open questions (§7.1–§7.5) with conditional-status flags.

The layer is exposed three ways, matching the register's existing access model: as **data**
(`dataset.json` / the standalone files), to **agents** (four new MCP tools — `compatibility`,
`interaction_sets`, `architectural_patterns`, `open_questions`), and to **humans** (an interactive
12×12 compatibility matrix on the landing page, colour-coded by category, click a cell for the pair
detail). A published `analysis.schema.json` keeps the "standard, not a table" positioning.

**Why this is the right answer to "maximize value."** The composition-problem framing is, by the
author's own account, the novel contribution. Until now a data consumer could not query it. Now they
can ask "what is the compatibility category for Hong Kong × Mainland China, and which interaction
sets bind?" and get a structured answer with its source — the analysis, not just the nodes.

---

## 3. The corridor layer (1 → 9 directed edges)

`scripts/build_corridors.py` transcribes eight high-demand directed edges from the Corridor Atlas
v0.2.3 §5 deep-dives, joining the existing `hk-br` anchor for nine corridors. Each carries the Atlas
attributes: feasibility class, compatibility category (linked to §5.14), live archetypes
(RC/SC/TC/DC), operative interaction sets, infrastructure overlap (Agorá / mBridge / Ensemble), the
inbound mechanism and its administrator, and any origin-override flag. The point the single example
could not make is now explicit in the data: **direction matters**. US→EU is Category I, but EU→US is
Category II (the §18 comparability gate); US→JP is a channel determination; HK→CN is blocked at the
destination. Nine edges is not the full 132-edge matrix (that is v0.6.0) — but it is enough to make
"corridor layer" a layer rather than a claim.

---

## 4. Audit hardening (the GitHub- and legal-reader findings)

- **CI.** `.github/workflows/build.yml` runs the analysis builder, the corridor builder, `build.py`,
  and `build_site.py` on every push and pull request and fails if derived artifacts drift. The
  register's central promise — "validated against the schema" — is now enforced, not asserted.
- **The ✅ over-reading (the audit's central legal caveat).** `build.py` now prints, in `COVERAGE.md`,
  an explicit statement of what ✅ does and does not mean, plus an **evidence-tier breakdown**. **At the
  v0.5.0 cut this breakdown read `resolution_text` 0 · `firm_summary` 66 · `unset` 51 · `source.url`
  10/117; those figures describe v0.5.0 only and are now superseded — see the banner at the top of §5
  and `CHANGELOG.md` [0.5.1].** The landing-page methodology item was rewritten from "verified means
  checked against the instrument" to the honest two-tier framing. A legal reader can now see, at a
  glance, the split between practitioner-corroborated and official-text-verified cells (the current,
  authoritative numbers are always in the generated `COVERAGE.md`).
- **Repository hygiene.** The one-shot migration builders moved to `scripts/`; the root is de-cluttered.
- **Naming.** A README "Name & identifiers" note resolves the CBSR-vs-`stablecoin-rail-register`
  inconsistency by *documenting* it: the canonical name is CBSR, but the repo slug, Pages URL, and
  schema `$id` are retained deliberately for URL/DOI/identifier stability (renaming would break inbound
  links and the schema identifier for no functional gain).
- **Metadata.** Schema `$id` moved off the `example.org` placeholder to the canonical github.io URL;
  the real ORCID (`0009-0005-6762-084X`) and an SSRN author id added to `CITATION.cff`; the nine CN
  records re-pinned from Compliance Matrix v0.9.3 to v0.9.6.

---

## 5. What this version deliberately does *not* do

> **Superseded note (read first).** This build note describes **v0.5.0**, which intentionally stopped
> short of the verification pass. **v0.5.1 then performed exactly that pass** — official `source.url`
> links and `evidence_tier` upgrades for Switzerland, the UAE, Japan and the in-force AML layers of
> Taiwan/South Korea (`resolution_text` 0→23, `mixed` 0→14, `source.url` 10→61/117), with drafts kept
> `firm_summary`. So the "does not promote" item just below was **true for v0.5.0 and is no longer the
> current state** — the authoritative figures live in the generated `COVERAGE.md`. See `CHANGELOG.md`
> [0.5.1]. (v0.6.0 then added the cross-layer integrity check, the corridor schema, and the compose()
> computed layer.)

- **It does not promote `firm_summary` to `resolution_text`, and it does not write `source.url`s by
  machine.** *(v0.5.0 scope.)* Doing either without reading each pinpoint against the official text
  would violate the project's own citation firewall (no machine-generated citations). That work was
  done, human-gated, in the **v0.5.1** verification pass; v0.5.0's honest contribution was *transparency*
  about the tier, not a verification claim the data did not yet support.
- **It does not load all 132 Atlas edges** — nine high-demand directed edges, with the full matrix on
  the v0.6.0 roadmap. Depth before breadth.

---

## 6. Validation

`python build.py` (run under the local `jsonschema` shim, since the sandbox has no network to
`pip install jsonschema`) reports: **117 records valid, 9 corridors, 66 compatibility pairs, 0 draft
cells.** The shim implements Draft 2020-12 type/enum/pattern/required/additionalProperties/minLength
checks and was self-tested against deliberately malformed records. The maintainer should run the real
`python build.py` (with `jsonschema` installed) and the CI workflow as the final gate before tagging.
