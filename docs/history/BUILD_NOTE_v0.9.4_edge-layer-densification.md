# Build note — v0.9.4: densifying the edge layer

*Authored 2026-06-27. Continues the v0.9.3 roadmap's named gap: the edge layer was "computed-complete but
rich-record-sparse."*

## The gap

v0.9.2 lit up the substrate: 124/132 directed edges became *derivable*. But derivable is not the same as
*recorded*. Only **9** corridors carried a rich record — the full Atlas model with `inbound_mechanism`,
`administrator`, `archetypes`, and `infrastructure_overlap` — and the other 115 derivable edges were just
a class label produced on demand. The reviewer named this precisely: "算全了但富记录稀疏" (computed-complete
but rich-record-sparse).

## What's derivable, and what isn't

The honest question is which parts of a rich corridor record can be *derived* from facts the register
already holds, and which are *empirical* and would need new research:

- **Derivable (re-projections of existing facts):** the **feasibility class** (already the substrate's job,
  already cross-checked); the **inbound mechanism** `test` and `administrator` (each destination's inbound
  gate and supervisor are captured in its C1/C7 records — e.g. the US gate is the GENIUS §18 comparability
  determination administered by Treasury/OCC); the **directed interaction sets** (which sets fired, from
  the substrate verdicts); a **baseline archetype** set (the hand-authored records show the rule: full
  `[RC,SC,TC,DC]` for a feasible corridor, reduced `[RC,DC]` for a blocked one — HK→CN).
- **Empirical (NOT derivable; needs sources):** `infrastructure_overlap` — *which* multilateral settlement
  projects (Project Agora, mBridge, Project Ensemble) actually touch a given corridor — is real-world
  knowledge, not a function of the constraint poles. So is the bespoke inbound `detail` ("none granted to
  date", "US-held reserves") and the curated prose.

## What v0.9.4 does

`scripts/build_edge_skeletons.py` emits a **computed skeleton** for every derivable directed edge that
lacks a hand-authored record. Each skeleton carries the derivable fields above, plus an explicit
`enrichment_backlog` listing what it does *not* have (`infrastructure_overlap`, bespoke detail, curated
archetypes, prose, primary-source verification). The empirical fields are set to `null` — not guessed.
**115 skeletons** result, so the edge layer now has a record for **124/132** edges (9 rich + 115
skeletons). The 8 without one are the non-origin-dragged edges *into the UK*, whose inbound gate is in
transition — the time engine owns those.

This is the same authored-vs-computed discipline the whole register runs on: the 9 hand-authored records
are the *enriched* tier (analogous to the authored signal table and the authored constraint cells); the
skeletons are the *computed* tier (analogous to the computed compose and the substrate). And it is doubly
gated, so it can't drift into fabrication:

- **Cross-check.** Every skeleton's class must equal the signal `compose()`; the build fails on any
  divergence. (Verified: tampering a skeleton's class fails the build.)
- **Provenance.** Every skeleton cites the `tier1_legal` records its derived fields rest on (the
  destination's C1/C7, the origin's C1); the build fails if any skeleton cites a missing or non-tier1
  record. (Verified: tampering provenance fails the build.)

Surfaced where the other layers are: MCP gains `edge_coverage` and `corridor_skeleton(origin, dest)`
(**25 → 27 tools**; `corridor_skeleton` returns the rich record if one exists, else the skeleton), and the
site's substrate panel gains an "edges with a record" coverage card.

## What this buys, and what's still owed

It buys **structure across the whole corridor space**: every derivable edge now answers, with provenance,
"what is the inbound mechanism, who administers it, what archetypes and interaction sets are in play, and
what class does it compose to" — not just a bare class. It does **not** buy **enrichment** or
**citability**:

1. **Verification (57 cells)** remains the gate to `resolution_text`; until it runs, the skeletons — like
   `compose()`, the substrate, and the stakeholder profiles — are preview, not citable authority.
2. **Enrichment** of the 115 skeletons into rich records — the empirical `infrastructure_overlap`, bespoke
   inbound detail, curated archetypes — is genuine per-edge factual work, and is deliberately left as a
   backlog rather than fabricated. This is the honest boundary: the register now derives everything the
   constraint layer can support for every edge, and stops exactly where new facts would be required.
