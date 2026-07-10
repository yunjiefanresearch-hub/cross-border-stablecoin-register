# Verification backlog

This is the corridor layer's **published residual** — the claims not yet confirmed against the
official text, kept as first-class, queryable data rather than hidden behind the headline counts.
The machine-readable source is [`verification_backlog.json`](verification_backlog.json), validated
in CI by [`../tools/check_verification_backlog.py`](../tools/check_verification_backlog.py).

> *"The residual … must be published as first-class, queryable data, not concealed behind the
> headline counts … the gates are defenses against misuse but do not themselves confirm a single
> claim, only primary-source verification does."* — *Citable by Construction*, §6.1–6.2

A backlog item is retired only by a primary-source verification pass, never by assertion.

> **This claim changed in v0.10.0, and the change is the point.** Through v0.9.99 this section read:
> *"None of the corridor layer's feasibility classes depends on an open item below."* That was **false**
> — `VB-06` decided **8 edges**, and it sat open for five releases. It is now `confirmed_and_applied`.
> The honest statement today is narrower: **one open item, `VB-09`, decides 22 outbound edges**, and it is
> flagged as such rather than described as touching "only a naming or a pinpoint date." The rest of the
> open items touch a naming, a date, a Tier-2 attribution, or a jurisdiction whose class is fixed regardless.

## Open / tracked

| id | juris. | claim | status | what's needed |
|---|---|---|---|---|
| **VB-01** | US | The stablecoin-yield compromise is the *"Tillis–Alsobrooks"* provision | partially confirmed | Alsobrooks + the Gallego/Alsobrooks crossover votes are confirmed; pin the **Tillis** half to a primary source. (The README over-statement of this was retracted in v0.9.95.) |
| **VB-02** | SG | Singapore is a member of Project Ensemble (`INFRA ensemble={HK,SG}`) | open | Confirm SG's **formal** Ensemble membership vs an Ensemble–Guardian *alignment*. The bloc enum stays a defensible Tier-2 judgment; the SG↔HK edge note states the caveat |
| **VB-03** | JP | Act No. 66 of 2025 was **promulgated 13 June 2025** | partially confirmed | The **effective** date (2026-06-01) and the recognition pathway are confirmed; reconcile the ~7-day promulgation-vs-enactment discrepancy against the primary gazette |
| **VB-08** | EU | §3.10's per-country MiCA grace table, and "ESMA confirmed no extension on 2026-04-17" | open | Sources conflict (Lithuania 6 vs 12 months; Poland has no national MiCA law at all); ESMA's formal transitional-measures statement is 2024-12-17. Downgrade to `firm_summary` until checked against ESMA's official Art. 143(3) list |
| **VB-09** | US, UK | US state trust/money-transmitter regimes and the UK EMRs 2011 make each a **token-holding origin** in law today | **open — HIGH PRIORITY (decides 22 edges)** | The Atlas defines *"exportable, comprehensively authorizable private token"* but pins it to no instrument. Reading (a) — origin drag fires only where **no** authorizable regime exists — keeps US/UK token-holders (adopted in v0.10.0). Reading (b) — it fires whenever the *comprehensive* regime is not in force — collapses **all 11 outbound-US and all 11 outbound-UK edges to `III`**. Confirm against the primary instruments. Previously decided *silently* by a `tier2` market record (NF-3); now a stated `tier1_legal` signal |
| **VB-10** | KR | Korea's outbound edges carry a **conditional, dormant** origin-egress override (Korea FX) | open | Atlas v0.2.5's edge register says so on all 11 KR rows; its §3.3 prose names only CN and SG. Pin the Korean FX instrument + administrator to a primary source and reconcile the Atlas's internal mismatch |
| **VB-11** | all 12 | Every signal in `analysis/signal_table.json` traces to a node record via `record_ref` | open | `record_ref` is `null` on all 60 signals and all 132 `class_basis` objects, because the 152 node records are unpublished (**C1**). Fabricating locators was declined: the citation firewall (*CbC* §4.3) forbids a tool from generating a citation, and a null is honest where a plausible-looking locator is not |
| **VB-07** | EU | The MiCA Art. 58(3) ceiling triggers on **either** 1M/day **or** €200m/day | partially confirmed | Statutory text is conjunctive ("**and** … respectively"); the artifact was corrected in v0.9.95 (F-EU). Propagate "or"→"and" to the upstream papers (§3.7, Matrix); the EBA operative methodology is separately unfinished |
| **VB-05** | HK | SFC secondary-trading circular, **20 Apr 2026** | open | Confirm the exact date against the primary SFC source (the per-edge `CONFIRM` marker re-homed in v0.9.93) |

**Closed and applied:**

- **VB-04** (PRC 银发〔2026〕42号) — verified against the PBoC 条法司 primary page
  (*"本通知自发布之日起施行…237号同时废止"*); status `confirmed`, `evidence_tier` `resolution_text`.
  Anchors `CN = blocked` in verifier gate `CF1`, and — from v0.10.0 — all **11** inbound-CN edges, not 9.
- **VB-03** (Japan Act No. 66 of 2025) — promulgated 2025-06-13; closed by the eighth review.
- **VB-06** (the US classification) — **`confirmed_and_applied` in v0.10.0.** GENIUS §20 sets the
  effective date at the earlier of 2027-01-18 or final rules + 120 days; at the snapshot only proposed
  rules existed. The 8 token-holder→US edges now read `T` with a `scheduled_with_cap` trigger; the §18
  prose is rewritten (E8); `CF1` anchors `US = T`; a negative test re-introduces the old coding and
  confirms the build fails. **This item's own `claim` field carried an internal error for five releases**
  — it said *"11 inbound edges … GENIUS §18"* where the artifact had 8 such edges and the operative
  section is §20 — so a machine querying `claim` alone got the stale value. Corrected in v0.10.0.

## Resolved since the 30 June 2026 snapshot

| id | juris. | claim | note |
|---|---|---|---|
| **VB-R1** | TW | Taiwan's Virtual Asset Service Act **prohibits issuer-paid yield** | **Confirmed** by the enacted text; Matrix v0.9.7 already clusters TW with EU/HK. Upgrades the §4.5 yield-line for Taiwan from backlog. |
| **VB-R2** | EU | The holding-period-reward yield line is expressed earliest and clearest by **MiCA Art. 50** | Art. 50 bans EMT interest and treats holding-period-linked remuneration as interest (in force 2024-06-30). With TW (VB-R1) and the Korea Ahn draft, the yield line is evidenced across **~5 jurisdictions**, not the ~1.5 the paper claims — an **under-statement** the paper can upgrade (the mirror of an over-statement, equally a discipline issue). |

## How this connects to the rest of the repo

- **Per-edge backlog.** The HK→BR seed edge also carries its open item in its own
  `verification_backlog` field inside the artifact (VB-05 here mirrors it for central tracking).
- **Bloc attribution.** VB-02 is cross-referenced in the `INFRA` definition comment in both
  `tools/verify_corridors_directed.py` and `scripts/build_corridors_directed.py`, and in the
  generated note on the two SG↔HK edges.
- **Living document.** Developments after the snapshot that are not verification gaps but dating
  updates are tracked separately in [`DEVELOPMENTS_SINCE_SNAPSHOT.md`](DEVELOPMENTS_SINCE_SNAPSHOT.md).
