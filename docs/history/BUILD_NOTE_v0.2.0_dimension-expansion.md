# Build Note — v0.2.0: Mapping the written portfolio into the register

**Date:** 2026-06-17 · **Maintainer:** Yunjie Fan · **Scope:** schema expansion (10 → 15 dimensions), jurisdiction reorientation, first substantive record load (30 verified records).

This note answers the question that drove the build: *given everything I have written, does the register need additional editable dimensions, and how much of my writing can it actually hold?* The short answer is **yes — four new dimensions plus one split — and the expansion moves roughly two full papers' worth of content from "unusable" to "first-class data."** The long answer follows.

---

## 1. What was mapped

The merged PDF (211 pp.) is not one paper; it is a **portfolio of six pieces** sharing one analytical spine. The register has now been populated from the parts that carry verified, pinpoint-level regulatory facts.

| Pt. | Piece (working title) | Pages | What it contributes to the register |
|---|---|---|---|
| 1 | Cross-Border Stablecoin Architecture (working paper) | 1–85 | The **eight-constraint framework** (C1–C8) and the six-jurisdiction comparison. This is the schema's backbone. |
| 2 | Narrowing the §404 Prohibition (policy brief) | 85–112 | US yield prohibition mechanics: GENIUS §4(a)(11), the "solely in connection with holding" line, CLARITY §404. |
| 3 | When Wallets Become Brokers (Reves) | 113–140 | Securities-classification doctrine — the basis for the **new `securities_classification` dimension**. |
| 4 | Three Mechanisms / Three Currency Areas | 141–156 | The monetary-sovereignty spectrum (EU cap / HK restriction / PRC prohibition) — basis for **`monetary_sovereignty`**. |
| 5 | Reves' Fourth Factor + op-eds | 157–172 | Reinforces the securities-classification and routing analysis. |
| 6 | **Multi-Jurisdiction Compliance Matrix v0.9.3** | 173–210 | The **data substrate**: 6 jurisdictions × 10 dimensions of sourced, pinpoint-level fact. Every record's `secondary` provenance cites this. |

**Implication:** the register was originally scoped to the spine of Part 1 (the yield boundary) plus a thin slice of Part 6. Parts 3 and 4 — two distinct doctrinal contributions — had **no home in the schema at all**. That is the gap this version closes.

---

## 2. The core finding — three vocabularies, one substrate

Your written work uses **three overlapping vocabularies** for the same underlying facts. They had never been reconciled in one place, and the code only spoke the narrowest of the three.

| Architecture paper — **8 Constraints** | Compliance Matrix — **10 Dimensions** | Code (original) — **10 Dimensions** | Could the original code hold it? |
|---|---|---|---|
| C1 Issuer Eligibility | Issuer pathways & eligibility | `issuer_pathway` | ✅ |
| C2 Reserve Composition **and** Custody | Reserve / Capital (two columns) + Custody | `reserve_capital` (one field) + `custody` | ⚠️ reserve & capital **conflated** |
| C3 Yield Prohibition *(spine)* | Yield & interest treatment | `permitted_activity_yield` | ✅ (the spine) |
| C4 Securities-Classification Boundaries | (carried in prose / Reves analysis) | — | ❌ **no dimension** |
| C5 Bank / Non-Bank Status & Routing | (carried in prose) | — | ❌ **no dimension** |
| C6 Cross-Border Payment & Data Sovereignty | Cross-border data treatment | `cross_border_data` | ✅ |
| C7 Monetary Sovereignty & Reserve-Currency Asymmetry | Non-domestic currency caps (comparison row) | — | ❌ **no dimension** |
| C8 Disclosure / Reporting / Supervisory Coordination | (distribution + disclosure prose) | `distribution` only | ❌ **partial** |

The middle column (the Matrix) is the richest, but even it splits Reserve from Capital and adds a "non-domestic currency caps" comparison row that the constraint list folds into C2/C7. The right column — what the code could actually store — **dropped C4, C5, C7, most of C8, and the reserve/capital distinction on the floor.**

You had, in effect, **written two whole papers (securities classification; monetary sovereignty) that the data model could not represent.**

---

## 3. Answer to the driving question: yes, add editable dimensions

The schema went from **10 → 15 dimensions**. Nine were kept as-is; one was split; four were added. Each addition is justified *from your own writing* — no dimension was invented speculatively.

### 3a. The split: `reserve_capital` → `reserve_backing` + `capital_requirements`
Your Matrix treats these as **two columns** for good reason: they answer different questions and move independently. *Reserve backing* is "what stands behind each token" (HK: 100% cash / ≤3-mo deposits / ≤1-yr govt; EU: EMT ≥60% bank deposits). *Capital* is "what the issuer must hold to operate" (HK: HK$25m paid-up + HK$3m liquid + 12-mo opex; US de-novo: $5m / 36 mo). Conflating them made it impossible to record, e.g., the US case where reserve rules and de-novo capital come from different instruments. **The split is required to transcribe the Matrix faithfully.**

### 3b. The four additions

| New dimension | Constraint | Why your writing needs it | Proof record now in the register |
|---|---|---|---|
| **`securities_classification`** *(promoted to second spine)* | C4 | Backed by two pieces (When Wallets Become Brokers; Reves' Fourth Factor). The Reves/§404 boundary is doctrinally as load-bearing as the yield boundary. | `us-pss-securities_classification-001` |
| **`bank_nonbank_routing`** | C5 | The OCC §15.10(c)(4) / FDIC §350.3(b)(4) rebuttable-presumption and anti-evasion §15.10(c)(6) analysis has no home under "distribution." | `us-pss-bank_nonbank_routing-001` |
| **`monetary_sovereignty`** | C7 | The entire three-currency-area comparison (EU Art. 23 quantitative cap / HK qualitative restriction / PRC total prohibition) is a first-class finding with nowhere to live. | `eu-emt-monetary_sovereignty-001`, `hk-frs-monetary_sovereignty-001`, `cn-prc-monetary_sovereignty-001` |
| **`disclosure_reporting`** | C8 | Disclosure, reporting triggers (EU €100M), and supervisory-coordination / indirect-pathway constraints (PRC A-share + SAFE + PBOC/CAC) were being crushed into "distribution." | (CN distribution record carries the C8 indirect-pathway layers; dedicated cells planned) |

Two supporting fields were also added so records can carry the *structure* of your analysis, not just prose:
- **`constraint_ref`** — links each record back to C1–C8 (and composites like `C4×C7`), so the register is navigable by your own framework.
- **`interpretive_flag`** `{tension, resolution_channel}` — carries the Matrix's "[interpretive question]" flags as structured data (e.g. UK Art. 9M(2) all-three-limbs vs HMT any-one; HK PDPO s.33 pending commencement).

**Net:** the schema now has **two spines** (yield + securities classification) and can represent all eight constraints. This is the single most consequential change in the build.

---

## 4. Jurisdiction reorientation

A mismatch surfaced between where the code pointed and where your verified content actually is.

| | Original code | Your actual deep content | Action taken |
|---|---|---|---|
| **Focus** | HK, TW, BR | US, EU, UK, SG, HK, CN | **Reoriented** focus to the six you actually wrote. |
| Taiwan | scaffolded as focus | **0 mentions** in the PDF | Parked — `roadmap.yaml`: "no substrate." |
| Brazil | flagship corridor | **2 passing mentions** (future only) | Demoted to **corridor-only**; corridor file retained but flagged. |
| US | "anchor" only | the doctrinal anchor **and** deepest content | Promoted to full focus. |
| EU/UK/SG/CN | "backfill 0.3.0" | richly sourced in the Matrix | Promoted to focus; now populated. |

The corridor file (`hk-br-usd-stablecoin-settlement.yaml`) deliberately **retains its `<VERIFY` markers** — it is a modeling exercise, not an obligation record, and the build pipeline correctly excludes it from verified counts.

---

## 5. How much content was previously unusable — the payoff

Before this build the register held **2 draft records, 0 verified**, on the old 10-dimension / TW-BR axis. The two seed records both carried unresolved `<VERIFY` markers.

After this build:

- **30 verified records, 0 drafts**, across **6 jurisdictions × 15 dimensions**.
- The HK column alone is now **11 records deep** (authority, issuer pathway, reserve backing, capital, yield, redemption, AML, cross-border data, monetary sovereignty, distribution, implementation status) — a near-complete jurisdiction profile transcribed from pp. 21–23 and 25–26.
- The prior open `<VERIFY>` on the HK yield spine is **resolved** to its exact pinpoint: Stablecoins Ordinance (Cap. 656) **Schedule 2, s.15 ("Non-interest bearing")**.
- The two previously-homeless papers now have **proof records**: `securities_classification` and `bank_nonbank_routing` (US), and a three-jurisdiction `monetary_sovereignty` set (EU / HK / CN) that captures the cap-vs-restriction-vs-prohibition spectrum as structured data.

In coverage terms: the schema expansion **converted the Reves/securities work and the monetary-sovereignty work from prose with no data representation into queryable, citable, version-stamped records.** That is the "deep use" you were after — your comparison tables are now machine-readable facts, each sourced to a primary instrument with your Matrix v0.9.3 page as secondary provenance.

> **Provenance discipline maintained throughout.** Per the register's own rule ("never let an AI tool generate citations — a single fabricated source is fatal"), every record here **transcribes your verified pinpoints** and cites **your Compliance Matrix v0.9.3** as secondary provenance. No citation was generated; each record's `interpretation_note` states this explicitly.

---

## 6. Record inventory (this build)

| Jurisdiction | Records | Dimensions covered |
|---|---|---|
| **HK** | 11 | authority, issuer_pathway, reserve_backing, capital_requirements, yield, redemption, aml_kyc, cross_border_data, monetary_sovereignty, distribution, implementation_status |
| **US** | 5 | yield, **securities_classification**, **bank_nonbank_routing**, reserve_backing, capital_requirements |
| **EU** | 4 | authority, yield, **monetary_sovereignty** (Art. 23 — the quantitative-cap exemplar), reserve_backing |
| **UK** | 3 | authority, issuer_pathway (interpretive flag), yield |
| **SG** | 2 | authority, yield |
| **CN** | 5 | authority, issuer_pathway (prohibited), cross_border_data (PIPL/DSL/Mar-2024), monetary_sovereignty (total non-RMB prohibition), distribution (indirect-pathway layers) |
| **Total** | **30** | 15-dimension schema, all verified |

---

## 7. What remains (next cells)

The visible `⬜` planned cells in `COVERAGE.md` are deliberate — this is an actively-built standard. The highest-value next loads, all with substrate already in your portfolio:

1. **`disclosure_reporting` dedicated cells** (C8) — EU MiCA reporting triggers, US supervisory coordination; the dimension exists, the cells are planned.
2. **`securities_classification` beyond the US** — apply the Reves analysis comparatively (EU/UK MiFID-adjacent treatment).
3. **HK `securities_classification` + `bank_nonbank_routing`** — the SFC professional-investor / FRS perimeter touches both.
4. **Custody** across focus jurisdictions (planned 0.3.0) — the C2 custody half, now cleanly separable from reserve backing.
5. A second **corridor** built from *your* jurisdictions (e.g. HK↔EU or US↔SG) to replace the BR placeholder with a flow you have actually sourced.

---

*Generated as part of the v0.2.0 build. The register validates clean (`python build.py` → 30 records valid, 30 verified / 0 draft). See `COVERAGE.md` for the live grid and `taxonomy.md` for the full 15-dimension ↔ 8-constraint mapping.*
