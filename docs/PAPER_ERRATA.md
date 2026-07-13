# Pre-publication errata for the upstream papers

**Scope.** This sheet lists corrections the **upstream companion papers and the Matrix** need before
release — not changes to this downstream `cbsr-corridor-audit` package. Each entry gives the finding,
the affected text, and drafted replacement wording where the correction is unambiguous.

> **What changed in v0.10.0, and why this sheet is now more urgent, not less.**
> Through v0.9.99 the artifact was *also* wrong on the US column and on the four tokenless-origin edges
> into a prohibition or a pre-regime destination — so the papers and the artifact were wrong *together*,
> and only this markdown held the corrected picture. That is the deepest tension in a portfolio whose
> thesis is that a legal reference consumed by software must be **citable by construction**: the
> correction lived in the one format the papers themselves say a machine consumer cannot be relied on
> to read.
>
> **v0.10.0 fixed the artifact.** The 8 inbound-US edges are now `T` with a `scheduled_with_cap` trigger
> at the GENIUS §20 outer cap; `TW→CN` / `KR→CN` are `blocked`; `CN→KR` / `TW→KR` are `pre_regime`; the
> §18 prose no longer lets a market observation do a proposition of law's job; and gate `CF1` anchors
> US = `T` so the regression cannot silently return.
>
> The contradiction between materials shipped together therefore **still exists, and its direction has
> flipped**: the register is now right *in its machine-readable data*, and the papers are wrong *in
> their prose*. **E1, F-US-1, E8 and NF-2 gate publication.**

The single most important one — E1 — is a direct contradiction between two materials a reader would
receive together.

---

## E1 — the "single dated horizon" headline (MUST fix before publishing)

**The contradiction.** *Cross-Border Stablecoin Feasibility Over Time* (v0.1.0) states that only one
pending transition carries a future date — the UK systemic-stablecoin regime, operative
**25 October 2027**. But the register's own `verification_backlog.json` **VB-06** (high priority)
establishes that this is **wrong**: the US GENIUS Act is, on 2026-06-30, in the same
enacted-not-commenced posture, with operative provisions taking effect no later than **18 January
2027** — a **second** dated horizon, and an **earlier** one. So the two materials a reader receives
together disagree with each other, and the register is the one that is right.

**Why it matters.** The "single dated horizon" claim is load-bearing: it anchors the paper's
"deliberately sparse forward map" narrative and the §4.2 sensitivity ordering. With the US corrected,
there are two anchors, the US one comes first, and the US (8 would-be-`T` inbound edges) leads the UK
(8 `T` inbound edges) on sensitivity.

**Nuance to preserve (VB-06, sixth review).** The UK date (25 Oct 2027) is a single gazetted
commencement date. The US date (18 Jan 2027) is an *earlier-of* **outer cap** (18 months after
enactment, or 120 days after final rules) — it can fall sooner. Model the US trigger as *scheduled
with a cap*, not as a fixed gazetted date and not as an undated contingency.

**Drafted replacement (for the headline / abstract sentence):**

> ~~"Only one pending transition carries a future date: the UK systemic-stablecoin regime, operative
> 25 October 2027."~~
>
> **"Two pending transitions carry future dates. The earlier is the US GENIUS Act framework: its
> operative provisions take effect on the earlier of eighteen months after enactment (18 January
> 2027) or one hundred and twenty days after final rules — an outer cap that may fall sooner. The
> later is the UK systemic-stablecoin regime, with commencement gazetted for 25 October 2027. Because
> the US horizon is both earlier and higher in in-degree, it leads the forward sensitivity ordering."**

**Prerequisite — now satisfied on the artifact side.** E1 was blocked on the reclassification of the 8
inbound-US edges from `II` to `T` (VB-06), which needed an honest `binding_status` in a published
signal table. **v0.10.0 ships that table** ([`../analysis/signal_table.json`](../analysis/signal_table.json)):
the US `inbound_gate` is `made_not_commenced` with `operative_date: 2027-01-18`, `date_kind: outer_cap`,
and gate `SIG2` (a `resolution_text` signal must be `in_force_enacted`) caps its evidence tier — so the
recomputed class is `T`, exactly as VB-06 predicted. `CF1` now anchors it, and a negative test proves
the old coding fails the build.

**Nothing upstream blocks E1 any longer. Only the paper's prose is outstanding.**

---

## E2 — MiCA Art. 58(3) threshold: "or" → "and" (§3.7 and the Matrix)

The artifact was corrected in v0.9.95 (F-EU): MiCA Art. 23(1), applied to EMTs mutatis mutandis by
Art. 58(3), is **conjunctive** — the issuer must stop issuing only when transactions are *"higher than
1 million … and EUR 200 000 000 respectively."* **Feasibility Over Time §3.7 and the Compliance
Matrix still write "or,"** which makes the cap bite earlier than the statute. Change "or" to "and" in
both, and note (as the artifact does) that the EBA operative measurement methodology is still pending.
Tracked as `VB-07`. (Practitioner literature is genuinely split, which is why the register flagged it;
the statutory text is nonetheless conjunctive.)

## E3 — §4.5 yield line: ~1.5 → ~5 jurisdictions

§4.5 documents the "reward-for-holding-period is prohibited" convergence at citable depth for the US
and Singapore only (~1.5 jurisdictions). The evidence is stronger (`VB-R1`/`VB-R2`): **MiCA Art. 50**
(in force 2024-06-30) prohibits EMT interest and expressly treats holding-period-linked remuneration
as interest; **Taiwan's VAS Act** prohibits issuer yield; and the **Korea Ahn draft** bars
interest/discount/other reward to holders. Raise the documented breadth to the ~5 jurisdictions the
evidence supports. This is an *under*-statement — correcting it strengthens the paper.

## E4 — Compliance Matrix Taiwan cell (M1)

Matrix v0.9.7's Taiwan cell reads *"remains a bill … no third reading yet,"* correct as of its own
cut-off but superseded by the 30 June 2026 third reading. Issue a Matrix **v0.9.8** with Taiwan as
*enacted at third reading 2026-06-30; nine subsidiary items pending; estimated commencement early
2027*, `binding_status = made_not_commenced`. The corridor layer already treats Taiwan this way.

## E5 — "Tillis–Alsobrooks" attribution (VB-01)

Any paper text that names the stablecoin-yield compromise as the *"Tillis–Alsobrooks"* provision
should be softened: the two documented committee crossover votes are **Gallego and Alsobrooks**, and
the **Tillis** half is not independently confirmed. (This repo's README already retracted the claim in
v0.9.95; the papers need the same discipline.)

## E6 — Corridor Atlas version string (N3, papers)

The corridor artifact's Atlas references were aligned `v0.2.3` → `v0.2.5` in v0.9.93. If any paper or
the Matrix still cites *"Corridor Atlas v0.2.3,"* align it to the shipped **v0.2.5** for consistency.

## E7 — geopolitical bloc attribution in §5.2 / the abstract (three factual slips + one tension)

The seventh review checked the bloc membership against the primary record and found the papers'
characterisation imprecise in three places, plus one genuinely interesting internal tension:

- **mBridge is not a "PRC-and-Gulf group."** Post-BIS-withdrawal (31 Oct 2024) mBridge continues with
  China, **Thailand**, Saudi Arabia, Hong Kong, and the UAE. **Thailand is a full participant and is
  neither PRC nor Gulf** — the abstract's "People's-Republic-of-China-and-Gulf group" omits it and
  mis-scopes the bloc.
- **Project Agorá is not "seven central banks of the G7-aligned bloc."** The seven are the Bank of
  France (Eurosystem), the Bank of Japan, the **Bank of Korea**, the **Bank of Mexico**, the Swiss
  National Bank, the Bank of England, and the Federal Reserve Bank of New York. **Korea and Mexico are
  not G7.** Call it "seven central banks convened by the BIS around major reserve currencies," not
  "the G7-aligned bloc."
- **The corridor tag set** `agora = {US, EU, UK, CH, JP, KR}` is itself correct for the in-scope
  members (it rightly includes Korea and omits out-of-scope Mexico); it is the *papers'* prose that
  over-tightens "Agorá = G7."

**The tension worth surfacing (not a defect).** Korea is simultaneously an **Agorá member** (in the
register's own bloc tag) **and the register's sole `pre_regime` origin** — the §4.2 top-sensitivity
jurisdiction. So the papers' clean "one geopolitical fracture, three layers" narrative has a node that
sits on the "Western settlement axis" while having no operative issuance regime of its own. This is a
**more interesting finding than a flaw**: it shows the settlement-bloc axis and the
regulatory-maturity axis are not co-linear, and the paper would be stronger for saying so explicitly.

## E8 — the inbound-US prose makes a market fact do a law's job (§2.1 discipline; ties to E1/VB-06)

The 8 inbound-US edges carry `inbound_mechanism.detail` ending *"… none granted to date"* for the
GENIUS §18 comparability gate — which reads as *"the gate is live, merely unused."* But per §20 the
§18 gate is **not yet in force** (effective ≤ 2027-01-18): the correct statement is *"not yet
available,"* not *"available but unused."* A **market observation is doing the work of a proposition
of law** — precisely the error *Citable by Construction* §2.1 says the register eradicates, and the
**mechanism** behind the F1/VB-06 miscoding (the six prior reviews recorded the symptom, the seventh
located the cause). **Done in the artifact (v0.10.0).** The 8 inbound-US edges now read *"the §18 pathway … is NOT YET
AVAILABLE: per §20 the Act takes effect on the earlier of 2027-01-18 or 120 days after final rules, and
at the 2026-06-30 snapshot only proposed rules had issued."* **The corrected example belongs in CbC §4.2
as a real captured case of the claim-class gate**, which is far stronger than the paper's current
hypothetical illustration: a market observation ("no determination has been granted") sat in a field a
machine reads as law, in the author's own flagship instance, and survived six reviews. `EV1` (every
class-driving signal is `tier1_legal`) and `SIG2` (a `resolution_text` signal must be `in_force_enacted`)
are the two gates that now make it impossible.

## NF-1 — origin-drag-first vs destination-first [RESOLVED in v0.10.0, in favour of the Atlas]

**The conflict, as it stood.** Corridor Atlas v0.2.5 §3.4/§4.1 and Feasibility §3.9 are
**destination-first**: *"Every edge terminating in the People's Republic of China is, and remains,
blocked at destination"*; *"27 edges are Category III"*; *"the destination sets the class on every edge
except the twenty-seven where an origin-side issuance gap overrides it."* The Atlas's own per-edge
register scores `KR → PRC` as **×** and `TW → KR` as **○**. The **artifact** applied
**origin-drag-first without exception**, giving III = 33 and inbound-CN = `{blocked: 9, III: 2}`. The
two excess edges, `TW→CN` and `KR→CN`, were internally self-contradictory: `class_code = III`
(*"partnership / coordination route"*) beside `inbound_mechanism.test = "Issuance and circulation
prohibited"* — in the **optimistic** direction.

**Resolution: option (a).** v0.10.0 changes the **artifact**, because the Atlas is the published
classification scale and a ban is more binding than "the origin has no token".

- The rule is now published as data-plus-code: [`../analysis/signal_table.json`](../analysis/signal_table.json)
  + [`../tools/class_rule.py`](../tools/class_rule.py), with precedence
  **prohibition > pre-regime > origin drag > in-transition > gate type**.
- Four edges move: `TW→CN`, `KR→CN` → `blocked`; `CN→KR`, `TW→KR` → `pre_regime`. III = 29.
- `OD1` is redefined from an **axiom** into a **check** that derives each destination's class from the
  artifact and enforces the precedence. Lint `m7` fires on nothing; `--strict` is green **without**
  `--allow-lint`.
- `CD1`'s deltas are now both **fact updates**, not a rule reversal laundered as one (ninth review,
  NF-9.3).

**Consequence for the papers: none.** Destination-first is what the Atlas and Feasibility §3.9 already
say. The papers were right; the artifact was wrong. What *does* need changing is §4.2 — see NF-2.

## NF-2 — §4.2/§4.3 sensitivity: recomputed under the corrected rule [P0, paper-side]

The eighth review recomputed §4.2 **against the shipped (origin-drag-first) artifact** and reported
*"Taiwan and Korea are exactly tied at 20 edges each"* and *"Mainland China is not insensitive."*
**Both of those conclusions were themselves artefacts of the NF-1 bug.** Recomputed under the
destination-first precedence by [`../tools/compute_sensitivity.py`](../tools/compute_sensitivity.py)
(output: [`../out/corridor_sensitivity.md`](../out/corridor_sensitivity.md), regenerated in CI):

| jurisdiction | trigger | kind | edges reclassified | inbound | outbound |
|---|---|---|---:|---:|---:|
| **KR** | Digital Asset Basic Act enacted + commenced | contingent, no date | **21** | 11 | 10 |
| **TW** | VAS Act commencement | contingent, no gazetted date | **18** | 9 | 9 |
| **UK** | SI 2026/102 commencement | scheduled | **8** | 8 | 0 |
| **US** | GENIUS §20 effective date | scheduled **with cap** | **8** | 8 | 0 |
| **CN** | — (no positive trigger exists) | open question | **0** | 0 | 0 |

**What the paper must change:**

1. **"South Korea is the single highest-sensitivity jurisdiction" is TRUE** (21 edges) — keep it. But the
   *reason* §4.2 gives is only half right: Korea leads not merely because a both-directions trigger
   touches twice the edge count, but because **Taiwan's outbound edges into CN and KR cannot move at
   all** (their destinations foreclose them), while Korea's cannot move only into CN.
2. **Taiwan is second at 18, not tied.** Delete any claim of a tie. The two regime-in-transition
   destinations differ on *three* axes, not two: certainty of timing, resolved class (I vs II), **and
   the number of edges their triggers can reach.**
3. **"Mainland China is insensitive" is TRUE** — and it is true *because* NF-1 was fixed. Under
   origin-drag-first it was false. This is independent evidence for resolving NF-1 the way v0.10.0 did.
4. **Add the second ordering the paper conflates with the first.** Sensitivity-by-edge-count and
   arrival-of-dated-horizon are different questions with different answers:
   - by edge count: **KR (21) > TW (18) > UK (8) = US (8) > CN (0)**
   - by dated horizon: **US (≤ 2027-01-18, outer cap) then UK (2027-10-25, gazetted)**; TW and KR carry
     no date and move no horizon.
   §4.2 currently ranks by the first while calling the UK *"the highest-sensitivity scheduled
   jurisdiction"* — a claim about the second — and omits the US horizon entirely. Both orderings belong
   in the text, named and separated.
5. §4.1's "both-directions triggers touch roughly twice the edge count" survives, but the arithmetic is
   **21 and 18**, not "twice 8 or 9": the destination-side foreclosures cut into it.

## F-US-1 — §3.2 "the GENIUS Act is in force" is wrong (folds into E1/VB-06) [P0]

§3.2 states *"The GENIUS Act is in force and governs the issuer level."* On the 2026-06-30 snapshot it
was **not** in force (effective ≤ 2027-01-18; only proposed rules existed — OCC NPRM published FR
2026-03-02, comments closed 2026-05-01; FDIC and FinCEN/OFAC NPRMs 2026-04-10; Treasury §4(c) NPRM April
2026; NCUA proposal February 2026). Confirmed against Congress.gov, the Federal Register and OCC
Bulletin 2026-3 by the fifth, eighth and ninth reviews.

**Drafted replacement:**

> ~~"The GENIUS Act is in force and governs the issuer level, including the §4(a)(11) prohibition…"~~
>
> **"The GENIUS Act is enacted (18 July 2025) and governs the issuer level once operative. Under §20 it
> takes effect on the earlier of eighteen months after enactment (18 January 2027) or one hundred and
> twenty days after the primary federal payment stablecoin regulators issue final regulations; as of the
> 30 June 2026 snapshot only proposed rules had issued, so the outer cap binds and may fall sooner. The
> §4(a)(11) prohibition on issuer-paid yield to holders and the §18 foreign-issuer comparability gate are
> therefore enacted but not yet operative."**

`scheduled_with_cap` is now a first-class trigger kind in the corridor schema
(`as_of_timeline.scheduled[].status`, with `date_kind: "outer_cap"`), and the artifact carries it on the
8 inbound-US edges. **v0.10.0 has applied this on the artifact side; only the paper is outstanding.**

## F-JP-1 — §3.6/§5.3 Japan recognition: date + the operational conditions [strengthens the paper]

Two fixes, the second substantive. (1) The Cabinet Office Ordinance recognising foreign trust-type
stablecoins was **promulgated 2026-05-19, in force 2026-06-01** (not "a same-day ordinance"). (2) §5.3
omits the recognition pathway's **operational conditions**, which are its most load-bearing content:
the foreign issuer must hold a licence **equivalent** to Japan's regime; reserves must be
appropriately managed and audited; and — the hard part — **the issuer's home regulator must have an
information-sharing / cooperation arrangement with the JFSA** (and the foreign trust beneficial
interest is expressly *not* a security under the FIEA). "The home regulator must be able to share
information with the JFSA" is a **far harder gate than equivalence** — it closes the door on
jurisdictions with no MOU — and stating it materially strengthens §5.3's "recognition = interoperability
protocol" thesis and corroborates the §5.2 bloc structure.

## F-EU-3 — §3.10 "only Circle's USDC and EURC hold MiCA EMT authorisation" is stale

By mid-2026 EMT authorisation extends well beyond Circle (multiple bank and fintech issuers). The
qualifier "the largest" rescues the sentence, but it misleads a machine reader; soften to "including."

## origin_override — RESOLVED in the artifact; one Atlas inconsistency remains for the papers

Atlas v0.2.5 §3.3 names **Mainland China and Singapore** as the override origins, but its own per-edge
register also carries *"[conditional origin-egress override (Korea FX, dormant)]"* on **all 11 KR rows**.
The artifact carried the flag on exactly **one** authored edge (`SG→HK`), and no gate checked it — so a
signal Feasibility §2.1 lists among the five that drive the class was ~99% absent.

**v0.10.0 populates it on all 33 edges** (CN: `active`; SG: `active`; KR: `conditional_dormant`), as a
structured object, gated by new hard check **`OO1`**.

**For the papers:** reconcile Atlas §3.3's two-origin prose with its own three-origin edge register, and
either name Korea's conditional-dormant override in §3.3 or drop it from the register. Tracked as
`VB-10`; the Korean FX instrument and its administrator are a `firm_summary` attribution pending a
primary source.

---

## Summary

| id | material | change | driven by | status |
|---|---|---|---|---|
| **NF-1** | artifact | destination-first precedence; inbound-CN all `blocked`, inbound-KR all `pre_regime` | review 8 | **RESOLVED v0.10.0** (in favour of the published Atlas; the papers were right) |
| **VB-06 / F1** | artifact | 8 inbound-US edges `II` → `T`, `scheduled_with_cap` @ 2027-01-18 | reviews 4/5/6/8/9 | **RESOLVED v0.10.0**; `CF1` anchors it; a negative test guards it |
| **E8** | artifact prose | US "none granted to date" → "the gate is not in force" | review 7 | **RESOLVED v0.10.0**; use as CbC §4.2's real captured case |
| **NF-3** | artifact + proposal | origin drag reads `token_regime` (tier1), never `token_in_issue` (tier2) | review 8 | **RESOLVED v0.10.0**; proved inert; the outbound question is now `VB-09` |
| **origin_override** | artifact | flag on all 33 CN/SG/KR outbound edges + gate `OO1` | review 8 | **RESOLVED v0.10.0**; Atlas §3.3-vs-register mismatch → `VB-10` |
| **E1** | Feasibility headline/abstract | single → **two** dated horizons; the US (≤ 2027-01-18, outer cap) leads the UK (2027-10-25, gazetted) | VB-06 | **OPEN — PUBLISH-GATING.** The artifact now contradicts the paper, in the paper's disfavour |
| **F-US-1** | Feasibility §3.2 | "GENIUS is in force" → enacted, operative ≤ 2027-01-18 | reviews 8/9 | **OPEN — PUBLISH-GATING** |
| **NF-2** | Feasibility §4.2/§4.3 | KR 21 > TW 18 > UK 8 = US 8 > CN 0; keep "Korea highest" and "China insensitive" (both true post-NF-1); delete the tie; add the **dated-horizon** ordering separately | reviews 8/9 | **OPEN — PUBLISH-GATING**; recomputed by tool, see `out/corridor_sensitivity.md` |
| **E2** | Feasibility §3.7, Matrix | "or" → "and" on the Art. 58(3) cap | VB-07 / F-EU | **OPEN** (artifact + signal table already conjunctive) |
| **E4** | Matrix (→ v0.9.8) | Taiwan "bill" → enacted-not-commenced | M1 | **OPEN — PUBLISH-GATING** |
| **E3** | Feasibility §4.5 | yield line ~1.5 → ~5 jurisdictions; lead with MiCA Art. 50 | VB-R1 / VB-R2 | **OPEN** (signal table already carries all five) |
| **E5** | any paper naming | drop the unconfirmed "Tillis" half | VB-01 | **OPEN** |
| **E6** | any paper citing the Atlas | "v0.2.3" → "v0.2.5" | N3 | **OPEN** |
| **E7** | Feasibility §5.2 / abstract | mBridge includes **Thailand** (not "PRC-and-Gulf"); Agorá's seven include **Korea and Mexico** (not "G7-aligned"); surface the Korea tension as a finding | review 7 | **OPEN** |
| **F-JP-1** | Feasibility §3.6 / §5.3 | Ordinance promulgated 2026-05-19, in force 2026-06-01; add the three recognition conditions, esp. **JFSA information-sharing** | review 8 | **OPEN** (the signal table now carries all three; this *strengthens* §5.3) |
| **F-EU-3** | Feasibility §3.10 | EMT authorisation "only Circle" → "including Circle" | review 8 | **OPEN** |
| **F-EU-2 / VB-08** | Feasibility §3.10 | per-country grace table + the "ESMA 2026-04-17" date → `firm_summary` | review 8 | **OPEN** |
| **VB-09** | Atlas + signal table | pin *"exportable, comprehensively authorizable private token"* to an instrument for the US and UK | review 8 (NF-3) / 9 | **OPEN — decides 22 outbound edges** |

**Publication is now gated by four paper-side items only: E1, F-US-1, NF-2 and E4.** Every artifact-side
prerequisite they were blocked on has landed in v0.10.0. Two materials shipped together still contradict
each other — but the register is now the one that is right in machine-readable data, and the papers are
the ones that are wrong in prose. That is a strictly better place to be, and it is a state the errata
sheet exists to end.
