# Developments since the 30 June 2026 snapshot

The companion papers are explicitly a **dated, register-backed living document**: their as-of is
**30 June 2026**, and *Feasibility Over Time* §3.3/§6 argue that only a register with dated snapshots
can absorb movement without silently going stale. This file is the tracking list for developments
that occurred, or became imminent, **between that snapshot and 8 July 2026** — the window the third
independent review examined.

**These are dating updates, not errors, and not verification gaps.** None changes a corridor
feasibility class or contradicts the artifact; each is a moving part to re-verify before the papers'
as-of is advanced. They are recorded here as flagged by the third review
([`AUDIT_v0.9.93_third-review.md`](AUDIT_v0.9.93_third-review.md)); each should be **primary-verified**
at the point the register snapshot is rolled forward. Items below are stated as the review reported
them, not asserted here as independently re-confirmed post-snapshot.

| area | at the 30 June 2026 snapshot | flagged development (to verify before rolling the snapshot) | artifact impact |
|---|---|---|---|
| **US GENIUS effective date** (§3.2, VB-06) | enacted 2025-07-18; **not in force**; effective on the earlier of 2027-01-18 or final rules + 120 days (§20); only proposed rules issued (OCC, FDIC, FinCEN/OFAC, Treasury, NCUA) | no final rules reported as of 8 July 2026, so the **2027-01-18 outer cap still binds**. If final rules issue before ~2026-09-20, the effective date moves *earlier* than the cap and the trigger resolves sooner | **the artifact now models this** (v0.10.0): 8 inbound-US edges are `T` with a `scheduled_with_cap` trigger at the cap. Re-read `US.inbound_gate.operative_date` in `analysis/signal_table.json` the moment final rules issue |
| **US CLARITY** (§3.2) | Polymarket ~48% for 2026 passage, down from ~74% a month earlier | drift toward ~42–46% reported since the snapshot | none — the figure is dated data about expectation, and the trigger is modelled as contingent (applied by no date). Note this is a **market** fact and by §2.1's discipline can never move a class |
| **EU MiCA cliff** (§3.10) | 1 July 2026 outer cap **pending** (snapshot is the day before) | the outer cap date has now **passed**; national side-doors close, passport-only for serving EU clients | none — MiCA is live before and after; this is an intra-regime gating change, not a class flip (as the paper already states) |
| **UK perimeter** (§3.1) | FCA summer-2026 policy statement on the three-limb territorial perimeter **expected** | FCA final rules reported to have landed around 30 June 2026 | none to the class (commencement is still the gazetted 25 Oct 2027); the perimeter interpretation the paper flagged as open may now be resolvable |
| **Taiwan commencement** (§3.3) | enacted 30 June 2026; commencement set separately, FSC pointing to ~Q1 2027 | presidential promulgation is due ~10 days after third reading; the Executive Yuan then sets the commencement date — i.e. promulgation around early July 2026 may have occurred or be imminent | none yet — Taiwan stays a `T` regime-in-transition destination until a commencement date is gazetted; the artifact's `as_of_timeline` already models this |
| **UK perimeter SI** (§3.1) | UKQS treated within the FCA dealing/arranging perimeter | HMT is reported to have laid an **amendment draft SI on 2026-04-21** moving qualifying stablecoins *out of* the dealing/arranging perimeter (fourth review) | none to the class; if confirmed, it refines how the UK inbound gate is characterized once commenced — a `reviewed_against` update for the UK edges |
| **Japan intermediary regime** (§3.6) | recognition pathway for foreign trust-type stablecoins as EPIs | Japan reported to have created, the same day (2026-06-01), a new **電子決済手段・暗号資産サービス仲介業** (electronic-payment-instrument / crypto-asset service intermediary business) (fourth review) | none to the class; a new intermediary category to fold into the JP node record and inbound-mechanism prose |
| **Korea DABA split** (§3.x) | stablecoin rules discussed within the DABA framework | a **2026-04-16 assessment** reportedly proposes splitting stablecoin rules *out of* DABA into separate legislation (fourth review) | none to the class (KR stays `pre_regime`); a structural note for the KR node and for the `pre_regime` characterization when it resolves |

## What changed in v0.10.0

The row above is the one that mattered. The register had *correctly identified* (VB-06, five releases
running) that the United States was enacted-not-commenced, and the artifact had nonetheless kept coding
it as a live Category II gate. v0.10.0 applies the correction. The lesson for this file: a
"development since the snapshot" tracker is not a substitute for fixing what the snapshot already got
wrong, and a `status: open` on a high-priority item is not a data change.

## Why none of the remaining items needs a data change now

The corridor artifact is dated (`generated`, `valid_as_of`, and per-edge `as_of_timeline`) and its
forward transitions are conditioned, not forecast: a contingent trigger "moves no horizon until a
date is fixed." So a drift in a prediction-market figure, the passing of an already-modelled dated
cliff, or an expected policy statement landing does **not** change any class or invariant. When the
register snapshot is rolled forward, these are the cells to re-read against primary sources; until
then, recording them here keeps the map honest about what has moved without pretending the artifact
is stale.
