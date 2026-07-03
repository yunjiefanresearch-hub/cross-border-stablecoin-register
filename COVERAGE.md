# Coverage

| Jurisdiction | Auth | Issu | Resv | Cap | Yield* | Sec* | Rout | Redm | Cust | AML | XB | MonSov | Disc | Dist | Impl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **US** | · | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | · | · | · | ✅ | ✅ | ✅ | · | · |
| **HK** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | · | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **EU** | ✅ | ✅ | ✅ | · | ✅ | ✅ | ✅ | · | · | · | ✅ | ✅ | ✅ | · | · |
| **UK** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ |
| **SG** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | · | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ |
| **CN** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | · | · | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ |
| **BR** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | · | ✅ | ✅ | ✅ | ✅ | ✅ | · | · |
| **CH** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **AE** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ |
| **TW** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **JP** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **KR** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜0.4.x | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Legend:** ✅ verified · ✍️ draft (contains `<VERIFY`) · ⬜vX.Y planned · · out of current scope. `Yield*` = `permitted_activity_yield` (the spine dimension).

> **What ✅ means here.** ✅ marks a cell that has a sourced, schema-valid record with **no `<VERIFY` marker and a human-passed pinpoint**. It does **not** by itself mean the pinpoint has been checked against the official gazette / statutory text. Provenance is tracked separately by `evidence_tier`: `resolution_text` = confirmed against the official text; `mixed` = the core point is confirmed against the official text but some operational detail is pending; `firm_summary` = corroborated by law-firm/practitioner analysis but not yet against the official text. As of the v0.5.1 verification pass, the live-regime focus jurisdictions (Switzerland, the UAE, Japan) and the in-force AML / user-protection layers of the pre-regime jurisdictions (Taiwan, South Korea) carry an official `source.url` and are `resolution_text` or `mixed`; draft provisions (the Taiwan VAS Act, the Korea Digital Asset Basic Act) keep `status: proposed` / `firm_summary` with an official URL for the *bill*, and the older seven-jurisdiction records predate the `evidence_tier` field (`unset`). Check the breakdown below before citing any cell as primary authority.

**Evidence-tier breakdown (records):** resolution_text 48 · mixed 14 · firm_summary 63 · unset 27 · records with a populated `source.url`: 100/152.

## Two-axis evidence model (the honesty view)
`claim_class` is the *kind* of claim (a proposition of law vs a market/operational report); `evidence_tier` is *how well-sourced* it is. They are orthogonal. The **lawyer-citable subset** is the intersection `tier1_legal` + `in_force` + `resolution_text` — binding law, in force now, confirmed against the official text. Operational facts are excluded by *kind* even when well-sourced; draft provisions are excluded by *status*; unverified legal points are excluded by *tier*.

| claim_class \ evidence_tier | resolution_text | mixed | firm_summary | unset | total |
|---|---|---|---|---|---|
| **tier1_legal** | 46 | 11 | 63 | 23 | 143 |
| **tier2_operational** | 2 | 3 | 0 | 4 | 9 |

> **Citable cells: 46** records satisfy `tier1_legal` + `in_force` + `resolution_text` and carry an official `source.url` + `pinpoint` (enforced by the build). This is the subset a lawyer or supervisor can cite as current binding law; it is exposed directly by the MCP `citable_law()` tool and as `citable_subset` in `dataset.json`. The two `tier2_operational` records at `resolution_text` (e.g. a confirmed product launch) are deliberately *not* citable as law — they are true, well-sourced facts about the market, not propositions of law.

## Computed layer (preview)
The `compose()` engine derives each pair's feasibility from the per-jurisdiction signal table and the Corridor Atlas algorithm, then diffs computed-vs-authored. It is a preview, not asserted authoritative; disagreements are **findings**.

- Directed corridors reproduced from rules: **9/9**
- §5.14 undirected categories reproduced: **64/66**
- Findings (computed ≠ authored): **uk_regime_in_transition: EU-UK, UK-US**
- Cross-layer integrity: every corridor's category is enforced against its §5.14 row; differing interaction sets must carry a declared `divergence` field.

## Verification queue
The backlog driving the next primary-source pass (also exposed by the MCP `verification_report()` tool).

- `resolution_text` 48 · `mixed` 14 · `firm_summary` 63 · **`unset` 27 (largest backlog)**
- The `unset` records are the legacy seven-jurisdiction set: CN 8, HK 1, KR 3, SG 3, TW 3, UK 9. These predate the `evidence_tier` field and are the declared next target.

_Verified cells: 152 · draft cells: 0 · planned cells: 24. Generated 2026-07-03._
