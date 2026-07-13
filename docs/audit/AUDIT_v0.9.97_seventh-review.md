# CBSR corridor layer — seventh independent review (over v0.9.97)

_Independent re-audit of the directed-132 corridor layer and its toolchain, over the v0.9.97 release.
Every tool was re-run in a clean Python 3.12 environment; the twelve load-bearing facts were
re-checked against primary sources (S.394 / GENIUS §20, the OCC bulletin, EUR-Lex MiCA Art. 23(1) and
Art. 50(3), the BIS/mBridge and Agorá membership record); the class = f(destination) compression was
reproduced; and a fresh adversarial probe was run against the DG1/DG2 gates. Review date: 2026-07-08.
Reviewer: independent, no relationship to the author._

One-line verdict: **the highest engineering honesty I have audited — runs, byte-reproducible, SHA
true, gates really bite, backlog really public — and its own §6.1 thesis ("the gates are defenses,
not a cure") is more true than the author proved. Honesty is not correctness: the headline is
falsified by the register's own VB-06, a directional legal error remains in the papers, the bloc
attribution has three factual slips, and the three-axis model is nearly empty at this layer.** The
review both confirms VB-06/VB-07/E3 against primary sources and adds five findings the six prior
passes did not surface — including one that produced a **fully green, self-consistent, false**
artifact.

## Confirmed against primary sources

- **VB-06 (US), confirmed and load-bearing.** GENIUS §20 sets the effective date at the earlier of 18
  months after enactment or 120 days after final rules; the OCC bulletin fixes enactment at 18 July
  2025 → outer cap **18 January 2027**, and only proposed rules existed at the snapshot. So the US is
  enacted-not-commenced, and the artifact's asymmetry is hard: **8 inbound-UK edges are `T` with a
  2027-10-25 trigger; 8 inbound-US edges are `II` with no timeline** — the same legal posture, coded
  opposite. The paper's "single dated horizon" headline is **wrong** (two horizons, US earlier).
- **VB-07 (MiCA threshold), confirmed vs EUR-Lex.** Art. 23(1) is conjunctive ("… **and** EUR
  200 000 000, respectively"). The papers' §3.7 "or" is a **directional** legal error (an "or" cap
  bites earlier). The artifact was corrected in v0.9.95; the papers were not.
- **E3 (yield line), confirmed and stronger than the errata said.** MiCA Art. 50(3) is the cleanest
  holding-period test anywhere — *"any remuneration or any other benefit related to the length of
  time during which a holder … holds such e-money token shall be treated as interest"* — in force
  since June 2024, **before** GENIUS. §4.5's ~1.5-jurisdiction framing is an **under**-statement.
- **BIS/mBridge**, confirmed (withdrawal 31 Oct 2024).

## The finding: a self-consistent lie passes all 11 gates (→ new gate `CF1`)

The fourth review's probe found a *histogram-conserving* class permutation and prompted `DG1`/`DG2`.
This review asked whether those close the hole. They do not. Two destinations with equal token-holder
in-degree — **CN and KR, both 9** — can have their classes swapped, and if **every** inbound edge's
prose (including the tokenless-origin edges) is rewritten to match, the result:

```
SCHEMA DC1 DC3 DC4a DC4b DC4c OD1 CD1 IB1 DG1 DG2   → all PASS
11/11 hard checks passed; 0 lint(s) (--strict); exit 0
```

…on an artifact that asserts **Mainland China has no prohibition** (`pre_regime`) and **South Korea
has an issuance prohibition it does not have** (`blocked`) — the exact reversal of the register's own
`status: confirmed` VB-04. **`DG1` and `DG2` are internal-consistency gates; a self-consistent lie
passes them.** This is not a refutation of the register — it is the strongest possible confirmation of
its own *Citable by Construction* §6.1 ("the gates are defenses, not a cure; only a primary-source
verification pass retires the liability"), true beyond the author's own argument. Before v0.9.98 the
only thing standing between this poison and a green CI was the SHA / migration reproducibility — which
is **provenance control, not semantic control**, and assumes the legacy snapshot is trusted.

> **v0.9.98 response — `CF1`, a confirmed-fact anchor.** A twelfth hard check pins a small set of
> destination classes to the **primary-source-confirmed** items in `verification_backlog.json`: CN is
> `blocked` (VB-04), TW is `T` (VB-R1). On the fully self-consistent CN↔KR poison above, all of
> SCHEMA/DC*/OD1/CD1/IB1/DG1/DG2 still pass and **`CF1` is the only gate that fails** (a negative test
> asserts exactly this). `CF1` is honest about being **partial** — it anchors only the confirmed
> facts, so a coherent lie about an *unanchored* class still passes; full closure is the upstream
> [`PROPOSAL_signal_table.md`](PROPOSAL_signal_table.md) recompute, where class becomes a function of
> published, `record_ref`-bearing signals rather than a hand-editable field. `CF1` anchors to verified
> *facts* (not builder logic), so it is the independent check finding F6 asks for, not more of the
> hand-copying F6 warns against.

## The other four new findings (documented)

- **D — bloc attribution errors in the papers (E7 in the errata).** mBridge is not a "PRC-and-Gulf
  group" (Thailand is a full participant, neither PRC nor Gulf); Agorá's seven central banks include
  the **Bank of Korea and the Bank of Mexico**, which are **not G7**, so "the G7-aligned bloc" is
  wrong. And a genuine tension worth publishing: **Korea is both an Agorá member and the register's
  sole `pre_regime` origin** — the settlement-bloc axis and the regulatory-maturity axis are not
  co-linear.
- **E — the inbound-US prose makes a market fact do a law's job (E8 in the errata).** *"none granted
  to date"* for the §18 gate reads as "live but unused"; per §20 it is "not yet in force." This is the
  §2.1 error the register claims to eradicate, and the **mechanism** of the F1/VB-06 miscoding — the
  cause the six prior reviews did not locate.
- **C — `CD1` is not independent of `DG1`/`OD1`.** Because class is `f(destination)`, the distribution
  is a checksum over the same ~12 signals; `CD1` cannot fail unless `DG1` or `OD1` already has. The
  effective rank of the "12 hard checks" is below 12. (Documented, not a defect — the checks are still
  worth running; they are just not 12 independent dimensions.)
- **A — the three-axis evidence model is nearly empty at this layer.** `evidence_tier` is present on
  **8/132** edges, all `firm_summary` (none `resolution_text`), and **no edge carries a `record_ref`**.
  The schema description was made honest in v0.9.95 (an unenforced label); the paper text should say
  the same, so no reader believes the signal-provenance axis is enforced here.

## Q1 / Q2 / Q3, briefly

- **Q1 (complete):** no — C1. The compose engine, the event calendar, the 152 node records, and the
  ten build gates are unshipped, so *Feasibility Over Time*'s subject and *Citable by Construction*'s
  four flagship numbers (152 records / citable=46 / 9-of-9 / 64-of-66) are not third-party verifiable
  here. The 17 negative tests bite the **corridor-layer** gates, not the five build gates the paper
  describes.
- **Q2 (value):** the tool layer maximises it; the data layer is honestly self-calibrated to "~12
  signals + one deep corridor + a reusable honesty discipline." The scarce assets (HK→BR, the yield
  line, the trigger typology, the discipline) are the real contribution.
- **Q3 (accurate & runnable):** runs, reproduces to the byte, SHA true — no overstatement in the
  engineering. The facts are accurate except where the register itself flags them (VB-06/07) plus the
  three bloc slips (E7).

## Priorities

**P0 (gate publication):** E1/VB-06 (reclassify the 8 inbound-US edges to `T` upstream, or declare the
divergence in the paper; `PAPER_ERRATA.md` has the wording) and E2 (the §3.7/Matrix "or" → "and").
**P1:** C1 (publish the tree); E7 (bloc attribution + the KR tension); E8 (US prose as the claim-class
example). **P2:** land `PROPOSAL_signal_table.md` (closes F1/F2/F6 **and** the self-consistent poison,
because class stops being a hand-editable field); document C (CD1 non-independence) and A (empty
evidence axis); E3 (raise the yield line, lead with Art. 50(3)).

## Verdict

Runs, reproduces, and is honestly framed; `CF1` now anchors the confirmed facts and catches the
self-consistent poison this review built, but the honest limit remains — only the signal-table
recompute or a primary-source pass closes the semantic hole in full. The register's rarest quality
holds: its own machinery and backlog had already surfaced most of what an independent auditor finds,
and where they had not (the self-consistent poison, the bloc slips, the claim-class mechanism), the
findings sharpen the register's own thesis rather than overturn it. **Fix E1 and E2, then publish the
tree.**

---

## Appendix V — commands re-run for this review

```bash
python3 tools/verify_corridors_directed.py            # 12/12, 0 lints (CF1 added)
python3 tools/verify_corridors_directed.py --strict   # 12/12, exit 0
python3 tools/run_negative_tests.py                   # ALL GATES BITE (18 cases incl. CF1)
pip install jsonschema && python3 tools/schema_reference_crosscheck.py   # 54/54; two implementations agree
python3 tools/build_corridor_matrix.py                # out/ regenerates byte-identically
python3 tools/check_verification_backlog.py           # backlog well-formed
python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json   # [OK]; SHA e03a9efe…
```
