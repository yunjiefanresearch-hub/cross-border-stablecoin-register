# `analysis/signal_table.json` — the twelve rows every class is derived from

**Status: shipped and executable as of v0.10.0.** `docs/PROPOSAL_signal_table.md` designed this file
and then declined to build it downstream. That refusal was right at the time, and understanding *why*
it was right is the whole point of this document.

---

## 1. What it is

Twelve rows, one per jurisdiction. Each carries the signals the corridor class actually depends on:

| signal | claim_class | read by the class function? | what it is |
|---|---|:---:|---|
| `token_regime` | `tier1_legal` | **yes** | Is there an authorizable issuance regime **in force** at the origin? Values: `authorizable`, `not_commenced`, `prohibited`, `none`. |
| `inbound_gate` | `tier1_legal` | **yes** | What legal test gates entry into the destination, and is the instrument in force? Values: `authorization`, `channel`, `comparability`, `prohibited`, `none`. |
| `egress_override` | `tier1_legal` | no | Does the origin impose an export/egress restriction? Drives `origin_override` (gate `OO1`). |
| `yield_line` | `tier1_legal` | no | The §4.5 convergence: is holder-yield prohibited? Documentation. |
| `token_in_issue` | `tier2_operational` | **never** | Does a circulating exportable token exist *as a matter of market fact*? Enrichment only. |
| `settlement_blocs` | `tier2_operational` | **never** | Agorá / mBridge / Ensemble membership. Drives `infrastructure_overlap` (gate `IB1`). |

Every signal also carries an `instrument` (what it rests on), a `binding_status` (the binding state of
that instrument), an `evidence_tier` (how well it is known), and a `record_ref` — which is **`null` on
all sixty signals**, because the 152 node records are not published (finding **C1**, tracked as `VB-11`).

## 2. The rule (`tools/class_rule.py`)

```
1. destination inbound_gate == prohibited                  → blocked
2. destination inbound_gate == none                        → pre_regime
3. origin token_regime != authorizable                     → III        (origin drag)
4. destination gate binding_status == made_not_commenced   → T
5. otherwise the gate type: authorization → I ; channel|comparability → II
```

This is **Corridor Atlas v0.2.5 §3.4 and §4.1**, verbatim in substance:

> *"Three classes are determined entirely by the destination. Every edge terminating in Mainland China
> is Blocked … Every edge terminating in Taiwan or South Korea is Pre-regime … (the edges whose origin
> is Mainland China, Taiwan, or South Korea fall instead to Category III, since the origin has no
> exportable token)."*
>
> *"The single most consequential structural fact in the matrix is that the destination sets the class
> on every edge except the twenty-seven where an origin-side issuance gap overrides it."*

and the Atlas's own edge register scores `KR → PRC` as **×** (blocked) and `TW → KR` as **○**
(pre-regime), not as `III`.

**Steps 1–2 rank above origin drag.** A prohibition and a pre-regime absence are terminal facts about
the destination: no origin-side token, present or future, completes the corridor. Category III means
*"the composition is unresolved; partnership or coordination routes remain"* — which is **false** into a
jurisdiction that bans the instrument. Ranking origin drag first (as the artifact did through v0.9.99)
gave `TW→CN` and `KR→CN` a class that says a workaround exists next to prose that says issuance is
banned: the only place in the whole package where the data made a corridor look **more open** than the
law allows.

## 3. Why this could not simply be reverse-engineered (and how the objection was met)

`PROPOSAL_signal_table.md` refused to build the table downstream, and its reason is worth quoting:

> *"Reconstructing the table by reading it back off the current 132 `class_code`s would bake in the very
> US = `II` classification F1 says is wrong — and would present a 'class recomputed from signals'
> guarantee whose signals were reverse-engineered from the classes. That is a false independence, the
> opposite of what the proposal is for."*

This is exactly right, and it is the trap that v0.10.0 had to avoid. The table was therefore written
**from the primary-source legal facts** — GENIUS §§18/20; SI 2026/102; Taiwan's VAS Act; 银发〔2026〕42号;
MiCA Titles III/IV and Art. 58(3); the Payment Services Act EPI regime; Cap. 656; BCB Res. 519/520/521;
the CBUAE PTSR; VAUPA and the un-enacted DABA — and only then compared against the artifact.

**It disagreed with the v0.9.99 artifact on 12 of 132 edges:**

| edges | artifact said | the signals say | why |
|---|---|---|---|
| 8 × token-holder → US | `II` | `T` | GENIUS §20: the §18 gate is enacted, **not in force** (effective ≤ 2027-01-18) |
| `TW→CN`, `KR→CN` | `III` | `blocked` | destination prohibition ranks above origin drag |
| `CN→KR`, `TW→KR` | `III` | `pre_regime` | destination pre-regime ranks above origin drag |

Those twelve edges were then corrected in the **artifact**, not in the table. A signal table that agrees
with the artifact by construction proves nothing. One that overturns it proves the recompute is real.

## 4. The gates over the table itself

Three gates run on every push (`tools/recompute_classes.py`), each with a negative test:

- **`SIG1` — signal-provenance.** Every signal the class function reads is `tier1_legal`;
  `token_in_issue` is `tier2_operational` and carries no `binding_status`. This is *Citable by
  Construction* §4.2: *"a derived conclusion may rest only on propositions of law, never on a market
  fact."* Proved **empirically**, not just declared: `--prove-tier2-inert` flips all twelve
  `token_in_issue` values, scrambles the settlement blocs, and asserts that **zero** classes move — with
  a control that flipping one `tier1_legal` signal *does* move nine.

- **`SIG2` — binding-status cap.** A signal at `evidence_tier == resolution_text` must have
  `binding_status == in_force_enacted`. This is *CbC* §3.1/§4.2: *"an instrument may be located, read,
  and confirmed, and still not be in force."*

  **`SIG2` is the gate that produces the US reclassification.** The GENIUS text has been read carefully
  and its §20 effective-date rule is confirmed against the primary record — but the instrument is not in
  force, so the signal is capped at `mixed`, and a gate that is not in force cannot be a live Category
  II gate. It is `T`. The same cap holds the UK's `inbound_gate` and Taiwan's `token_regime` below the
  top tier. The paper's abstract discipline turns out to have a concrete, load-bearing consequence, and
  the register did not enforce it on itself until now.

- **`SIG3` — instrument present.** A `tier1_legal` signal names a non-empty `instrument`.

And one gate over the pair:

- **`PR1`** — the published rule reproduces all 132 `class_code`s, all `class_basis.rule`s, all
  instruments and all `resolves_to` values in the artifact, exactly. This closes findings **F2** (the
  class was a function of the destination but the function was opaque) and **F6** (the verifier's
  partition constants were *hand-copied from the builder*, so "they cannot disagree by construction" was
  the problem, not the reassurance).

## 5. What the table does **not** claim

- **It does not claim its signals are true.** `PR1` proves *derivation*, not *truth*. Three destination
  classes are anchored to primary-source-confirmed facts by verifier gate `CF1` (CN = `blocked` per
  `VB-04`; TW = `T` per `VB-R1`; US = `T` per `VB-06`). The other nine are not. A coherent lie about an
  unanchored signal still passes every gate. Only a primary-source verification pass retires that
  liability — *CbC* §6.1: *"the gates are defenses, not a cure."*

- **It does not settle `VB-09`.** The US and UK rows say `token_regime = authorizable`, on the ground
  that state trust/money-transmitter regimes and the Electronic Money Regulations 2011 authorize
  issuance today, in law. The Atlas defines *"exportable, comprehensively authorizable private token"*
  but does not pin it to an instrument. Two readings are defensible:

  | reading | origin drag fires when … | consequence |
  |---|---|---|
  | **(a) adopted here** | no authorizable regime exists at all | US/UK stay token-holders; only the destination gate transitions |
  | (b) | the *comprehensive* regime is not in force | **all 11 outbound-US and all 11 outbound-UK edges collapse to `III`**, and the entire I/II structure changes |

  Reading (a) is what the previous artifact *implicitly* assumed — but it assumed it via
  `token_in_issue`, a market fact, which is the signal-provenance violation the eighth review's **NF-3**
  identified. The table makes the assumption a **stated `tier1_legal` signal with an open backlog item**.
  It is the single decision with the largest unexamined footprint in the layer, and it is now visible
  rather than buried.

- **It does not supply `record_ref`.** Sixty nulls. A fabricated locator would violate the citation
  firewall (*CbC* §4.3: *"no tool generates or infers a citation"*). Tracked as `VB-11`; closed by
  publishing the node records (finding **C1**).

- **It does not carry the settlement-bloc reading into any class.** Bloc membership is
  `tier2_operational` — the *Feasibility* paper concedes as much in §5.1 — and is proved inert.

## 6. Regenerating everything from the table

```bash
python3 tools/class_rule.py                            # derive 132 classes; run the table's gates
python3 tools/recompute_classes.py --prove-tier2-inert # PR1 + SIG1/2/3 + the inertness proof
python3 tools/recompute_classes.py --trace             # out/derivation_trace.md — every cell, with its rule
python3 tools/compute_sensitivity.py --write           # out/corridor_sensitivity.md — the §4.2 ordering
python3 tools/run_negative_tests.py                    # break each gate; each must fail the build
```

## 7. Folding this upstream

The register's own build should emit `signal_table.json` from the 152 node records rather than have it
hand-written here, and `scripts/build_corridors_directed.py` should call `class_rule.class_of` rather
than carry its own copy of the precedence. At that point:

- `record_ref` populates from the node records (`VB-11` closes),
- `evidence_tier` on each signal becomes the node record's own tier rather than a downstream estimate,
- `SIG2` becomes an instance of the register's existing binding-status gate rather than a re-implementation,
- and `tools/migrate_from_v0_9_92.py` becomes a no-op, which is the sign the fold-in is complete.

Until then, the honest description of this file is: **a downstream reconstruction of the signal table
from the primary-source legal facts, published so that the class rule is auditable, and explicitly not
a substitute for the node records it should be derived from.**
