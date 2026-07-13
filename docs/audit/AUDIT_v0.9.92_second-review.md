# CBSR corridor layer — second independent review (over v0.9.92), resolved in v0.9.93

_Independent re-audit of the directed-132 corridor layer and its standalone toolchain, taken over
the v0.9.92 tooling release and against the two companion working papers (*Cross-Border Stablecoin
Feasibility Over Time* v0.1.0 and *Citable by Construction* v0.1.0) and the three prior deliverables
(Compliance Matrix v0.9.7, Architecture v0.2.8, Corridor Atlas v0.2.5) as the underlying research.
Review date: 2026-07-08. Reviewer: independent, no relationship to the author._

This review takes as its baseline the first independent review (`AUDIT_v0.9.9_independent-review.md`,
which raised C1/M1/M2 and the lints m1/m4/m5 and confirmed the Tillis–Alsobrooks naming). It asks
the same three acceptance questions — **(1) complete underlying application content, (2) value /
applicability / functionality, (3) accurate and runnable** — and reports what the first review did
not surface, together with what v0.9.93 does about it.

Every "verified" and "fixed" claim below was re-derived mechanically by the four zero-dependency
tools, run on the corridor artifact **alone**. The findings were confirmed on the v0.9.92 artifact;
the resolutions were confirmed on the v0.9.93 artifact and its updated tools.

---

## 0. Runnability, restated precisely

**Tool layer: runs, exactly as documented.** All four tools were executed against the committed
artifact:

| tool | result |
|---|---|
| `verify_corridors_directed.py` | 9/9 hard checks, exit 0 (v0.9.92: 3 lints; **v0.9.93: 0 lints**) |
| `run_negative_tests.py` | 15 negative cases + positive control + non-mutation assertion, exit 0 — every gate bites |
| `schema_reference_crosscheck.py` | rejects every adversarial mutation (v0.9.92: 46; **v0.9.93: 54**); with `jsonschema` installed, the bundled executor and the reference agree on every verdict |
| `build_corridor_matrix.py` | regenerates `out/` byte-for-byte |

`--strict` and `--json` behave as described. **v0.9.93 makes `--strict` green** (the three lints are
gone).

**Full-pipeline layer: still not runnable from a clone (finding C1, unchanged).** As the package
states plainly, `build.py → run_invariants.py` depends on the 152 node records, `event_calendar.json`,
`compatibility.json`, `computed_corridor_skeletons.json`, `build_edge_skeletons.py`, and the rest of
the register tree — none shipped. Cloning this repo and running the author's build fails at step 1.
This is a **delivery-completeness** gap, not a logic defect, and it is the single highest-value item
still open.

## 1. Underlying content: corridor layer complete; as an *application* substrate, incomplete (C1)

**Complete:** all 132 directed edges are present with an exact provenance partition (9 authored +
106 skeleton + 17 transition = 132), a 12-field required schema, the 12×12 analyst grid, and the
per-jurisdiction supervisor cut. The corridor layer is a deliverable artifact in its own right.

**Incomplete as the "underlying application":** the machinery both papers are *about* cannot be run
from this repository — `compose(origin, destination, as_of)` (the entire subject of *Feasibility Over
Time*), the lawyer-citable subset and the ten build gates (the entire subject of *Citable by
Construction*), the 152 node records, the event calendar, and the ledger. A precise sharpening: the
package *verifies* the origin-drag rule (check `OD1` passes) but does not *contain* the rule that
produces it — `class_code` on the skeleton edges is inherited from the absent
`computed_corridor_skeletons.json`. The layer can check its own internal coherence; it does not carry
the upstream logic that decides each class. **Publishing the full register tree is the highest-value
next step**, consistent with C1.

## 2. New findings beyond the first review (the increment)

The first review caught C1/M1/M2 and the lints and corrected Tillis–Alsobrooks (all independently
re-confirmed here). The following were **not** surfaced there. Each was reproduced mechanically.

### N1 — `infrastructure_overlap` free text, and a silent authored-edge miss (minor, **fixed**)

`infrastructure_overlap` was free text with ten distinct spellings for five blocs. More consequential:
the two **authored** edges **US→HK** and **HK→US** carried *"No shared production or pilot settlement
rail; commercial rails subject to both regimes."* A `startswith`/substring reader buckets that to
`none`, yet the true relationship is **cross-bloc** — the US sits on Project Agorá, Hong Kong on
mBridge (and Project Ensemble). Because the gate `IB1` exempted authored edges, this error passed CI
silently. A full-corpus re-computation (partition function vs the stored value) confirmed the mismatch
was **exactly** these two edges and no others.

> **Resolution (v0.9.93).** The field is now a structured object `{"bloc": <enum>, "note": <text>}`
> with `bloc ∈ {agora, mbridge, ensemble, cross-bloc, none}`. `IB1` reads the enum and checks **all
> 132 edges, authored included**; the US↔HK edges are corrected to `cross-bloc`; the fragile prose
> heuristic is retired; and a negative test flips an authored edge's `bloc` to prove the widened gate
> now bites. The schema declares the object strictly (`additionalProperties: false`), and the
> reference-oracle battery gains a mutation asserting the **legacy string shape is now rejected**.

### N2 — the flagship computed-vs-authored **category** divergence is not reproducible here (minor; a sharpening of C1, **documented; upstream to fix**)

*Citable by Construction* §5.2 leans on two computed-vs-authored **category** disagreements (EU–UK
and UK–US, where one layer treats a regime-in-transition pair as not-yet-bridgeable and the other as
cleanly bridgeable). That headline example **cannot be reproduced from this package**: it needs
`analysis/compatibility.json` (absent, C1), and the artifact's own `divergence` fields record a
*different* kind of divergence — the per-direction **interaction-set** refinement (each direction's
`interaction_sets` differ from the undirected pair), which is declarative, not the silent category
kind. The artifact reports `cross_check.clean = true` with `category_mismatches: []`; i.e. **zero**
category mismatches are present here. This is not a contradiction in the paper — the category
divergence lives upstream in the compatibility layer — but a reader cannot check the paper's flagship
reconciliation example against this repo.

> **Status.** Open, upstream. Bringing `computed_compatibility.json` (or `compatibility.json`) into
> the full-tree release makes the EU–UK / UK–US category divergence runnable. No change is possible
> in this package without that input; the distinction between the two *kinds* of divergence is now
> stated in `README`, `CHANGELOG`, and here so no reader conflates them.

### N3 — internal Atlas version drift (very minor, **fixed**)

The artifact's `divergence.reason` and per-edge `source` strings cited *"Corridor Atlas v0.2.3"* while
the shipped Atlas — and every paper — is **v0.2.5**. Same root cause as M2 (internal version drift).

> **Resolution (v0.9.93).** All 15 occurrences (7 `divergence.reason`, 8 `source`) aligned to v0.2.5;
> the builder carries an `ATLAS_VERSION` constant.

### N4 — a transition class could silently default to a clean Category I (minor robustness, **fixed**)

In `scripts/build_corridors_directed.py`, a regime-in-transition edge whose destination has no
scheduled or contingent resolution in the event calendar defaulted to `[{"resolves_to": "I"}]`. The
current artifact is correct (Taiwan → II is baked in from the calendar), but a jurisdiction added to
`TRANSITION_DESTS` later without a calendar entry would be **silently** mislabelled a clean `I`. The
companion `inbound_gate`-to-class map had the same "unknown ⇒ I" shape.

> **Resolution (v0.9.93).** Both now **raise** with a diagnostic instead of defaulting, so the
> omission is loud. The current output is unchanged; the trap for the *next* transition destination
> is removed.

## 3. Priority ordering (by return on effort)

1. **Publish the full register tree** (or a release tarball). Retires **C1**, makes **N2** runnable,
   and turns the time engine, the citable subset, and the ten gates from *readable* into *runnable*.
   Single highest-value item, unchanged from the first review.
2. **~~Align version strings + stamp `register_version`~~ (done, v0.9.93 / M2, N3).**
3. **Compliance Matrix Taiwan cell (M1)** — retire the version-skew with an upstream Matrix `v0.9.8`
   reading *"enacted at third reading 2026-06-30; pending nine items of subsidiary legislation;
   estimated commencement Q1 2027,"* `binding_status = made_not_commenced`. The corridor layer here
   already encodes Taiwan as enacted-not-commenced, so this is the last place the Matrix and this
   layer disagree on Taiwan's binding status, and the disagreement is purely one of as-of date.
4. **~~Structure `infrastructure_overlap` + widen `IB1` + clear the seed-edge lints~~ (done, v0.9.93 /
   N1, m1/m4/m5).**
5. **~~Harden the builder's transition-class default~~ (done, v0.9.93 / N4).**

## 4. Verdict

The corridor layer and its toolchain remain a genuinely strong, self-checking deliverable, and the
first review's positive assessment stands. This second pass found one substantive machine-checkable
error (N1, the silently-miscarried US↔HK cross-bloc edges), two version/robustness issues (N3, N4),
and one reproducibility sharpening of C1 (N2). v0.9.93 fixes N1, N3, N4, M2, and the three lints by
deterministic, reproducible transforms, and widens the settlement-bloc gate so the N1 class of error
cannot recur silently. What remains open — **C1** and its dependent **N2**, and the **M1**
version-skew — is upstream, and is stated rather than hidden.

---

## Appendix V — commands re-run for this review

```bash
python3 tools/verify_corridors_directed.py            # 9/9, 0 lints (v0.9.93)
python3 tools/verify_corridors_directed.py --strict   # 9/9, exit 0
python3 tools/run_negative_tests.py                   # ALL GATES BITE, exit 0
pip install jsonschema && python3 tools/schema_reference_crosscheck.py   # 54/54; two implementations agree
python3 tools/build_corridor_matrix.py                # out/ regenerates byte-identically
python3 tools/migrate_from_v0_9_92.py \
    --in data/legacy/computed_corridors_directed.v0.9.92.json \
    --out /tmp/regen.json                             # reproduces data/computed_corridors_directed.json
python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json  # [OK]
```
