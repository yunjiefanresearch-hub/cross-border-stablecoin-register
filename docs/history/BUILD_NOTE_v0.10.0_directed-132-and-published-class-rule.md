# Build note — v0.10.0: the directed-132 corridor layer and a published class rule

## Why this release exists

Through v0.9.91 the register described its own corridor layer honestly and unflatteringly:

```
edge layer: 9 rich + 106 computed skeletons = 115/132 edges with a record (17 indeterminate)
```

Two things are wrong with that line, and this release fixes both.

The first is coverage. Nine of the one hundred and thirty-two directed edges were flagship corridors
with real analytical content; one hundred and six were skeletons; seventeen were nothing at all. A
directed feasibility map that carries a record for eighty-seven percent of its edges is not a map of
the graph, it is a map of a favourite corner of it. **Every ordered pair of the twelve jurisdictions
now carries a directed-edge record**, and each one states which precedence step decided its class, on
whose signal, resting on which instrument, at what binding status, with a locator into the node record
that justifies it.

The second is deeper, and it is the reason this is a minor-version release rather than a patch. The
`class_code` column *arrived finished*. The rule that produced it lived upstream and unpublished. A
consumer — increasingly a machine — could read `HK→BR: Category II` and had no way to ask *why*, and
no way to check. That opacity concealed two real errors, which the ninth independent review found and
which this release corrects.

## The two corrections

### 1. The class rule is destination-first (NF-1)

*Corridor Atlas* v0.2.5 §3.4 states the precedence plainly: three classes are determined entirely by
the destination, and the destination sets the class on every edge except the twenty-seven where an
origin-side issuance gap overrides it. The artifact applied **origin drag first**. The consequence was
not academic. `TW→CN` and `KR→CN` read `Category III` — glossed in the register's own prose as *"no
direct issuance; partnership / coordination route"* — while the inbound mechanism on those very edges
read *"issuance and circulation prohibited"*. The artifact contradicted itself, in the optimistic
direction, and no gate could see it, because the verifier encoded the rule as an axiom copied by hand
out of the builder.

The rule is now `tools/class_rule.py:class_of`, published, executable, and applied to all 132 edges:

```
1. destination inbound_gate == prohibited        -> blocked
2. destination inbound_gate == none              -> pre_regime
3. origin token_regime != authorizable           -> III        (origin drag)
4. destination gate binding_status == made_not_commenced -> T
5. otherwise the operative gate type: authorization -> I ; channel|comparability -> II
```

Four edges move: `TW→CN`, `KR→CN` to `blocked`; `CN→KR`, `TW→KR` to `pre_regime`.

### 2. The United States is enacted, not commenced (E1 / F-US-1 / E8)

GENIUS Act §20 sets the effective date at the earlier of eighteen months after enactment
(**18 January 2027**) or one hundred and twenty days after the primary federal payment stablecoin
regulators issue final regulations. At the 30 June 2026 snapshot only *proposed* rules had issued. So
the §18 foreign-issuer comparability gate is **not yet available**, and the eight token-holder→US edges
are `T`, not `II`, with a `scheduled_with_cap` trigger.

The previous coding said, in effect, "the gate is live but no one has passed through it". That
sentence states a **market observation** where a **proposition of law** is required, which is exactly
the claim-class conflation the companion methodology paper's first axis exists to prevent. It also
made the flagship *Feasibility Over Time* claim — *"only one pending transition carries a future
date"* — false: there are two, and the United States one is **earlier**.

## What makes this checkable rather than merely asserted

The point of publishing a rule is that someone can run it. Four independent things now do:

| Check | What it proves | Where |
|---|---|---|
| `DC5` | all 132 class codes are re-derived from the published rule **on every build** | `run_invariants.py` |
| `DC7` | flipping **every** `tier2_operational` market signal moves **0** classes | `run_invariants.py` |
| `TIER1-LIVE` | the control: flipping **one** `tier1_legal` signal moves **9** classes | `tools/recompute_classes.py` |
| `PR1` | an independent re-derivation reproduces every class, rule, instrument and `resolves_to` | `tools/recompute_classes.py` |

`DC7` without `TIER1-LIVE` would be worthless — a class function that read *nothing* would also pass
it. Together they say something precise: the class rule reads exactly two signals, both propositions
of law, and it reads them.

Beyond that: a 17-gate verifier (`tools/verify_corridors_directed.py`), a 31-case negative-test suite
that breaks each gate on a throwaway copy and confirms it bites, and
`tools/migrate_from_v0_9_92.py --check`, the executable specification of this release's edge shape,
which exits 0 only when a clean regeneration reproduces it. The migration script is, as of this
release, a **no-op** — which is the signal that the fold-in is complete.

## The signal table, and what binding it to the records surfaced

`analysis/signal_table.json` publishes the sixty per-jurisdiction signals the class rule reads. The
corridor audit that first proposed it shipped it with `record_ref: null` on every signal, because the
152 node records were not published with it and *fabricating a locator was declined* — the citation
firewall forbids a tool from generating or inferring a citation, and a null is honest where a
plausible-looking locator would not be.

The register publishes those records. So the locators are supplied, not declined, and backlog item
**VB-11** closes: 39 of the 60 signals carry a `record_ref`, including **all 24 class-driving ones**;
the other 21 carry an explicit, reasoned `record_ref_gap` (12 `token_in_issue` market facts, which may
never be given a legal locator, and 9 `none`-valued egress overrides, because the absence of an export
restriction is not an instrument).

Binding the two layers together did what an honest join always does: it produced **disagreements**.
Twenty of them, ten on class-driving signals, and they are published as data under
`record_binding_findings` rather than reconciled away. The load-bearing one *is* errata E1:

> `us-pss-monetary_sovereignty-001` codes the GENIUS **Act** as `in_force_enacted`. It is: the Act was
> enacted on 18 July 2025. The signal codes the **§18 gate**, whose effective date §20 sets in the
> future. Act-enacted is not section-operative.

Nothing was overwritten. A legal record is corrected by a primary-source verification pass, not by a
build script — so the record stands, the signal stands, and the disagreement between them is a
first-class, queryable finding. That is the computed-versus-authored discipline applied to itself.

Backlog item **VB-09** stays open, and is now *visible* rather than implicit: the US and UK
`token_regime` signals rest on the state trust/money-transmitter regimes and the Electronic Money
Regulations 2011, which the register carries no record for, so their locators are tagged
`match: related_dimension`, never `same_instrument`. If that reading is wrong, all twenty-two
outbound US and UK edges fall to Category III and the entire I/II structure of the map changes. The
register now says so in its own data.

## The reproducibility bug this release found in itself

Re-running the canonical build sequence on the v0.9.91 tree **regressed committed data**.
`scripts/build_analysis.py` still described Taiwan as pre-regime on eleven pairs (v0.9.91 had
hand-corrected the artifact to `enacted_not_commenced` after the 30 June enactment without updating
the builder), still dropped the `trigger_kind` fields from `open_questions.json`, and still carried two
"BIS Project Ensemble" attributions that errata E7 had corrected in the artifact.

That is a latent reproducibility lie of exactly the kind the register exists to refuse: the committed
data could not be rebuilt from the committed scripts. The builder now reproduces
`analysis/compatibility.json` and `analysis/open_questions.json` byte-for-byte. It was found by running
the sequence and diffing, not by reading — which is the argument for running it in CI, where it now is.

## Version collapse

Three numbers described one object: the register at `0.9.91`, the corridor artifact's
`register_version` at `0.9.9`, and its `artifact_revision` at `0.10.0`. They are now one, **0.10.0**,
and the `V1`/`V2`/`V3`/`L1` invariants enforce agreement across `build.py`, `dataset.json`,
`CITATION.cff`, `README.md`, `PACKAGE.md`, the verification ledger and both papers. The companion
works (Matrix v0.9.7, Architecture v0.2.8, Atlas v0.2.5) keep their own versions: they are different
works, not different names for this one.

## What did not change

The 152 node records. The 46-record citable subset. The 9 authored corridors. The 66-pair §5.14
matrix. The 6 interaction sets. **No legal record was edited by this release**, and no feasibility
class moved on the strength of a new fact — the four `blocked`/`pre_regime` moves are a *rule*
correction, and the eight `T` moves are a *binding-status* correction. Both are re-derivable, on
demand, from a signal table whose values are hashed and whose provenance is published.

## Verification

```
python3 scripts/build_analysis.py
python3 scripts/compose.py
python3 scripts/build_edge_skeletons.py
python3 scripts/gen_signal_table.py            # NEW
python3 scripts/build_corridors_directed.py    # NEW
python3 build.py
python3 scripts/build_forward_view.py
python3 scripts/build_sensitivity.py
python3 scripts/build_settlement.py
python3 scripts/build_corridor_states.py
python3 build_api.py

python3 run_invariants.py                      # 57/57
python3 run_negative_tests.py                  # 10/10 gates bite
python3 check_readme_counts.py                 # OK
python3 tools/verify_corridors_directed.py     # 17/17 hard checks, 0 lints
python3 tools/run_negative_tests.py            # 31 negative + 2 positive + 2 non-mutation
python3 tools/recompute_classes.py --prove-tier2-inert
python3 tools/migrate_from_v0_9_92.py --check analysis/computed_corridors_directed.json   # exit 0
```
