# Brazil — jurisdiction build-sheet (corridor → full jurisdiction, v0.3.x)

**Purpose.** Corroborating substrate for promoting Brazil from *corridor-only* to a full
register jurisdiction, and for adding Brazil to the Compliance Matrix and Architecture
papers. Every requirement below is corroborated by the resolution text + firm analysis
surfaced in the Jun 2026 verification pass. **Per METHODOLOGY.md, final clause-level
confirmation against the official DOU/BCB text is the author's step — these are not
finished "verified" records.**

**Headline.** The corridor fieldwork has already verified enough primary material to
support **~9 BR records — more than the 5 the roadmap scoped** (`regulatory_authority`,
`issuer_pathway`, `cross_border_data`, `monetary_sovereignty`, `aml_kyc`). The three
extras (`reserve_backing`, `custody`, `disclosure_reporting`) are corridor-driven; note
that **`disclosure_reporting` (C8) is empty across *all six* focus jurisdictions**, so a
BR C8 record would be the register's first populated C8 cell.

---

## The framework in one line
BCB Resolutions **519/520/521** (pub. 10 Nov 2025; in force **2 Feb 2026**; audit+reporting
from **4 May 2026**) operationalise the Virtual-Assets Law (**Lei 14.478/2022** + **Decreto
11.563/2023**); Resolution **561/2026** (pub. 30 Apr 2026; in force **1 Oct 2026**) amends
the eFX rules in **Res 277/2022**. The FX-classification limb rests on the **Foreign Exchange
Law, Lei 14.286/2021** (not the Virtual-Assets Law).

---

## Recommended BR records

| id | dim | C-ref | status / eff. | one-line requirement | primary pinpoint | feeds |
|---|---|---|---|---|---|---|
| `br-vasp-regulatory_authority-001` | regulatory_authority | — | in_force / 2026-02-02 | BCB is the VASP authority (Lei 14.478/2022 + Decreto 11.563/2023); CVM retains jurisdiction over securities-like tokens. Framework = Res 519/520/521 + 561. | Lei 14.478/2022; Decreto 11.563/2023; Res 519/520/521 | Matrix row 1; Arch §5.x |
| `br-vasp-issuer_pathway-001` | issuer_pathway | C1 | in_force / 2026-02-02 | VASPs ("SPSAVs") need BCB authorisation; 3 modalities — intermediary / custodian / broker (Res 520 Art 4); mandatory Brazil establishment; eligible already-regulated FIs may also serve on notification; 270-day grandfathering to **30 Oct 2026**. | Res 519; Res 520 Art 4, Art 20–23 | Matrix "issuer"; Arch §5.x |
| `br-vasp-reserve_backing-001` ⊕ | reserve_backing | C2(reserve) | in_force / 2026-02-02 | Stablecoin = "ativo virtual referenciado em moeda fiduciária"; reserve asset defined as fiat + government bonds of the *same* government; **algorithmic / unbacked fiat-pegged tokens prohibited** (asset curation). | Res 520 glossary; Art 64+ (curadoria) | Matrix "reserve"; corridor `br_custody_assets` |
| `br-vasp-custody-001` ⊕ | custody | C2(custody) | in_force / 2026-02-02 | Patrimonial segregation (Art 28–30): client fiat in individualised accounts; client VAs in distinct wallets; ≤5% own-asset co-mingling for liquidity if identified; foreign-custodian conditions (home-country authorisation, BR representative, enforceable guarantees, segregation, record access). | Res 520 Art 28–30; foreign-custody provisions | corridor `br_custody_assets` |
| `br-vasp-disclosure_reporting-001` ⊕★ | disclosure_reporting | C8 | in_force / 2026-02-02 (audit/reporting 2026-05-04) | Proof-of-reserves methods documented; **independent audit, biennial, reasonable-assurance** (Art 30 III), report **publicly disclosed on website** (Art 30 §1); Res 521 monthly FX reporting from 4 May 2026; IN BCB 701 technical certification. | Res 520 Art 30 III + §1; Res 521 reporting; IN BCB 701 | **first C8 cell**; corridor `br_custody_assets` |
| `br-vasp-cross_border_data-001` | cross_border_data | C6 | in_force / 2026-02-02 | VA international payments/transfers are câmbio ops (Res 521 inserts Art 76-A into Res 277/2022; legal base Lei 14.286/2021); per-op caps USD 100k SPSAV / USD 500k FX-FI when counterparty not BCB-FX-authorised; traceability (wallet owner, origin/destination); self-hosted-wallet identification. | Res 521 (Art 76-A in Res 277/2022); Lei 14.286/2021 | Matrix "cross-border"; corridor `br_vasp_fx_rail` |
| `br-vasp-monetary_sovereignty-001` | monetary_sovereignty | C7 | in_force / 2026-02-02 | **No MiCA-style volume cap** on non-BRL stablecoins; instead, non-BRL stablecoin flows are routed through the FX regime (balance-of-payments capture) + per-operation caps + the eFX crypto exclusion (Res 561). A *distinct* sovereignty model. | Res 521; Res 561; Lei 14.286/2021 | Matrix Pattern 2; Arch §5.x |
| `br-vasp-aml_kyc-001` | aml_kyc | — | in_force / 2026-02-02 | PLD/FT governance (Res 519/520); KYC; Travel Rule phased (Art 44 + Art 89) — domestic by **Feb 2027**, international full compliance **2 Feb 2028**; interim client self-declaration permitted if documented. NB Art 88 = authorisation adjustment period (270-day adequação), not the Travel-Rule hook. | Res 519; Res 520; Res 521 (Travel Rule) | Matrix "AML"; corridor |
| `br-vasp-securities_classification-001` ⊕(opt) | securities_classification | C4 | in_force / 2026-02-02 | CVM jurisdiction over securities-like tokens (valores mobiliários) preserved alongside BCB; BCB technical position to Congress would classify USD stablecoins as "private foreign currency" (IOF 1.1% vs 3.5%). Brazilian C4 analogue = token classification + asset curation. | Decreto 11.563/2023; CVM regime; Res 520 Art 64+ | corridor C4 link; *Reves* paper (if developed) |
| `br-vasp-implementation_status-001` (opt) | implementation_status | — | transitional | Timeline: 2 Feb 2026 in force · 4 May 2026 audit/reporting · 30 Oct 2026 grandfathering + eFX Unicad · 31 May 2027 unauth. eFX-provider authorisation · Feb 2027 Travel Rule stage 1 (domestic) · 2 Feb 2028 full Travel Rule (international). | Res 519/520/521; Res 561 Art 56-A/56-B | corridor watch_list |

⊕ = beyond the roadmap's planned 5 · ★ = fills the empty-everywhere C8 cell · (opt) = optional/secondary

---

## Open / contested cells to flag with `[⚠ interpretive question]`

- **IOF.** Res 521 classifies these as FX ops, creating the IOF taxable event (fato gerador) —
  but no levy is in force: collection is the Receita Federal's competence, and as of Jun 2026
  no Receita instrument is in effect. A proposal (IOF-Câmbio 3.5% on stablecoin purchases vs a
  "private foreign currency" 1.1% treatment) is in consultation. Resolution channel: pending
  Receita / Min. Fazenda action / Congress.
- **Yield axis.** Brazil has **no explicit issuer-paid-yield ban** analogous to GENIUS
  §4(a)(11) / MiCA Art 50; Res 520 Art 12 prohibits *credit offering* by VASPs. The "yield"
  Matrix cell for Brazil should record this divergence (a genuine comparative data point).
- **Asset segregation in statute.** PL 4.932/2023 (in Congress) would legislate VASP/user
  asset segregation above the resolution level — a watch item for `custody`.

---

## Which papers get Brazil (and how)

- **Compliance Matrix v0.9.3 → add Brazil as the 7th jurisdiction** across all ten matrix
  dimensions. Coverage line, Executive Summary, and **Pattern 2 (monetary sovereignty)**
  all change: Brazil is a *third* sovereignty model after EU volume-caps and PRC-prohibition
  — the "FX-channeling + per-operation cap" model. This is the strongest reason Brazil is
  not redundant with the existing six.
- **Cross-Border Stablecoin Architecture → add §5.x Brazil**, add **HK×BR** (this corridor)
  and **US×BR** cells to the §5.8 pairwise compatibility table, and **remove Brazil from the
  "not surveyed" lists** in §8.3 (limit 1) and §8.4 (research agenda). The corridor's
  four-way composition maps onto §5.8's Category + interaction-set vocabulary; HK×BR is most
  naturally a **Category II / III** cell (capped rail + no domestic USD FRS).
- **Reves' Fourth Factor and Stablecoin Routing Across Six Jurisdictions → optional.**
  Adding Brazil here needs net-new analysis (the CVM-175 tokenised-fund routing analogue);
  the corridor's Brazil C4 material is token-classification + asset-curation, which is
  C4-adjacent but not the routing-into-fund question the paper is built on.
- **Not affected:** *Narrowing the Section 404 Prohibition* and *When Wallets Become Brokers*
  are US-§404-specific; Brazil has no §404 analogue.
