# Upgrading the register: v0.9.91 → v0.10.0

**This is an iterative upgrade of the v0.9.91 repository, not a replacement of it.** Every file
v0.9.91 shipped is still here: the 152 node records, the 9 authored corridors, both papers, the five
PDFs, the MCP server, the schemas, the build system. The change is additive plus three patched
scripts and one reproducibility fix.

> **Do not delete the old version and drop this in as a fresh tree.** Git history, the Zenodo concept
> DOI's version lineage, and the `CHANGELOG` continuity all depend on this landing as a commit *on
> top of* v0.9.91. The instructions below do that.

---

## 1. Why this is not a "copy over the old repo" job

The `cbsr-corridor-audit-v0.10.0` package that motivated this release is **not a version of the
register**. It is a 52-file audit of the register's corridor layer, and its own `docs/VERSIONS.md`
says the full register is *"not shipped in this repo (finding C1)"*. It ships an
`apply-to-full-repo/` directory containing a patch, because it was always meant to be *applied to*
the register, not swapped in for it.

This upgrade is that fold-in, done properly and carried further: the audit's transforms are folded
into the register's own builders (so `tools/migrate_from_v0_9_92.py --check` is now a **no-op**), and
the one thing the audit could not do — bind every signal to a real node record — is done here,
because the register publishes the records the audit lacked.

---

## 2. What changed, in one table

| | v0.9.91 | v0.10.0 |
|---|---|---|
| Directed edges with a record | 115 / 132 (17 indeterminate) | **132 / 132** |
| Class rule | upstream, unpublished | `tools/class_rule.py`, published + re-run on every build |
| Class inputs | implicit | `analysis/signal_table.json` (60 signals, `record_ref` bound) |
| `class_basis` per edge | — | rule, governing jurisdiction, signal, claim_class, binding_status, instrument, record_ref |
| Dated horizons | 1 (UK 2027-10-25) | **2** (US 2027-01-18 outer cap; UK 2027-10-25 gazetted) |
| `TW→CN`, `KR→CN` | `III` ("partnership route") | **`blocked`** |
| `CN→KR`, `TW→KR` | `III` | **`pre_regime`** |
| 8 token-holder → US edges | `II` | **`T`** (GENIUS §20) |
| Origin-egress override | 1 edge | **33** (all CN/SG/KR outbound rows) |
| `run_invariants.py` | 49 | **57** (+ DC1–DC8) |
| API endpoints | 95 | **229** |
| Node records / citable subset | 152 / 46 | **152 / 46 (unchanged)** |

No legal record was edited. The four class moves are a *rule* correction; the eight `T` moves are a
*binding-status* correction. Both are re-derivable from the published signal table.

---

## 3. How to land it on GitHub

### Option A — replace the working tree, keep the history (recommended)

```bash
git clone git@github.com:<you>/cbsr.git && cd cbsr
git checkout -b release/v0.10.0            # branch off the v0.9.91 tip

# copy this tree over the checkout, preserving .git
rsync -a --delete --exclude='.git/' /path/to/cbsr-v0.10.0/ ./

git add -A
git status                                  # expect: ~10 new paths, 8 modified files
```

`git status` should show, and only show:

**New**
```
analysis/signal_table.source.json      the curated signal VALUES (hashed)
analysis/signal_table.json             generated: values + record_ref
analysis/computed_corridors_directed.json
api/corridors_directed/  (132 files)
api/corridors_directed.json
api/signal_table.json
scripts/gen_signal_table.py
scripts/build_corridors_directed.py
tools/  (10 files)
docs/PAPER_ERRATA.md, docs/SIGNAL_TABLE.md, docs/VERIFICATION_BACKLOG.md,
docs/DEVELOPMENTS_SINCE_SNAPSHOT.md, docs/verification_backlog.json, docs/VERSIONS.md,
docs/audit/  (9 independent reviews)
BUILD_NOTE_v0.10.0_directed-132-and-published-class-rule.md
UPGRADE_v0.9.91_to_v0.10.0.md
```

**Modified**
```
build.py                  + directed-layer load/validate, check_directed_cross_layer,
                            check_directed_signal_provenance (SP1–SP4); REGISTER_VERSION 0.10.0
build_api.py              + api/corridors_directed/*, api/signal_table.json, index entries
run_invariants.py         + DC1–DC8; P1/P2 extended to tools/; EXPECT_VERSION 0.10.0
scripts/build_analysis.py   reproducibility fix (see §5)
.github/workflows/build.yml + the two new build steps and six new gate steps
CHANGELOG.md, CITATION.cff, README.md, PACKAGE.md, METHODOLOGY.md, ROADMAP.md, mcp.json
papers/*.md               errata E1 / F-US-1 / E8 / NF-2 / E2 + correction banner
dataset.json, api/**, analysis/**   regenerated
```

### Option B — apply the audit's patch yourself

Do **not** use `git apply`. The shipped `changes.patch` was cut against a later `build.py` snapshot
and its `build.py` hunk swallows the `def evidence_tier_summary(recs):` header, orphaning that
function's body. It also stops at the directed-layer plumbing, so it does not give you the
destination-first rule, the signal table, `class_basis`, the typed triggers, or the 33 origin
overrides. The tree in Option A is the completed fold-in.

### Then

```bash
git commit -m "v0.10.0: directed-132 corridor layer, published class rule, US enacted-not-commenced"
git push -u origin release/v0.10.0
# open the PR; CI runs the full sequence + all gates
git tag -a v0.10.0 -m "CBSR v0.10.0" && git push --tags   # after merge; Zenodo mints the version DOI
```

---

## 4. Verifying the upgrade locally

Run the sequence, then every gate. All of it is offline and dependency-free except `jsonschema`
(optional — `build.py` degrades to a built-in structural validator).

```bash
python3 scripts/build_analysis.py
python3 scripts/compose.py
python3 scripts/substrate.py
python3 scripts/build_edge_skeletons.py
python3 scripts/stakeholders.py
python3 scripts/build_worklist.py
python3 scripts/gen_signal_table.py            # NEW — must precede the directed builder
python3 scripts/build_corridors_directed.py    # NEW
python3 build.py
python3 scripts/build_corridor_states.py
python3 scripts/build_sensitivity.py
python3 scripts/build_settlement.py
python3 scripts/build_forward_view.py
python3 build_api.py
```

Expected tail of `build.py`:

```
edge layer: 9 rich + 106 computed skeletons = 115/132 edges with a record (17 indeterminate); ...
directed-132 layer: 132/132 ordered pairs (9 authored + 106 skeleton + 17 transition); ...
directed classes: {'I': 32, 'II': 24, 'III': 29, 'T': 25, 'blocked': 11, 'pre_regime': 11}; ...
signal table: 60 signals across 12 jurisdictions; 20 record-binding finding(s) (10 on class-driving ...
```

(The `edge layer:` line still reports 115/132. That is deliberate: it describes the *skeleton* layer's
own coverage, which is unchanged. The `directed-132 layer:` line beneath it is the answer to "does
every jurisdiction pair have a corridor".)

Then the gates:

```bash
python3 run_invariants.py                     # 57/57 invariants hold
python3 run_negative_tests.py                 # 10/10 gates bit
python3 check_readme_counts.py                # OK
python3 tools/verify_corridors_directed.py    # 17/17 hard checks passed; 0 lints
python3 tools/run_negative_tests.py           # 31 negative + 2 positive + 2 non-mutation
python3 tools/recompute_classes.py --prove-tier2-inert
python3 tools/migrate_from_v0_9_92.py --check analysis/computed_corridors_directed.json   # exit 0
python3 tools/schema_reference_crosscheck.py
python3 tools/check_verification_backlog.py
```

`migrate_from_v0_9_92.py --check` exiting 0 is the completion criterion: it asserts, independently of
the builder, that every `class_code` equals the published rule over the signal table, that
`class_basis` is present, that `T ⇔ as_of_timeline`, that `origin_override` matches the Atlas, and
that no drift marker survives. **The migration script is now a no-op**, which is what "the fold-in is
complete" means.

---

## 5. One thing to know before you push

`scripts/build_analysis.py` was **not** reproducible in v0.9.91, which is why the CI workflow
explicitly refused to run it (*"those generators would revert them"*). Re-running it reverted
Taiwan's `enacted_not_commenced` axis on 11 pairs, dropped the `trigger_kind` fields from
`open_questions.json`, and reinstated two "BIS Project Ensemble" attributions that errata E7 had
already corrected in the artifact. The committed data could not be rebuilt from the committed
scripts.

It is fixed. `build_analysis.py` now reproduces `analysis/compatibility.json` and
`analysis/open_questions.json` byte-for-byte, CI runs it, and the repository's own reproducibility
gate (`git diff --exit-code -I'"generated"' -- dataset.json analysis/ api/`) now covers it.

If you have local edits to those two artifacts made *after* the last `build_analysis.py` run, port
them into the builder before you push, or CI will revert them for you.

---

## 6. Downstream consumers

- **`api/corridors_directed/<O>-<D>.json`** — one file per directed edge. Read `class_code`,
  `class_basis` (why), `as_of_timeline` (when, and whether the date is gazetted or a cap), and
  `origin_override`.
- **`api/signal_table.json`** — the inputs. A consumer that does not want to trust `class_code` can
  re-derive all 132 from this file and `tools/class_rule.py`, which is 100 lines of standard library.
- **`infrastructure_overlap`** changed shape in this release, from a free-text string to
  `{"bloc": <enum>, "note": <text>}` with `bloc ∈ {agora, mbridge, ensemble, cross-bloc, none}`. If
  you projected the string, read `.bloc`.
- **`record_ref`** is a bare node-record id string, or `null`. Everything that qualifies it —
  `match`, the record's own `binding_status`, and any declared `divergence` — lives in the sibling
  `record_ref_meta`, so a citation is never diluted by the caveat attached to it. A `null` always
  carries a `record_ref_gap.reason`.

---

## 7. What the papers now say that they did not

`pdf/` still holds the **pre-correction** PDFs. The `.md` files under `papers/` are the source of
truth and carry the corrections; re-export the PDFs before circulating them. The corrections are
`docs/PAPER_ERRATA.md` items **E1, F-US-1, E8, NF-2, E2**, and the headline is blunt:

> *Feasibility Over Time* v0.1.0 said only one pending transition carried a future date. There are
> two, and the United States one is the earlier.
