# Compliance Matrix v0.9.x — Brazil insertion (paste-ready, house-style)

> **Verification status — two evidence tiers (as of June 2026).** Facts below are separated by
> provenance, not merely confirmed/unconfirmed.
> **Tier 1 — well-corroborated** (agreed across multiple independent firm/practitioner sources and
> consistent with the statutory structure): the 10 Nov 2025 / 2 Feb 2026 / 4 May 2026 dates and
> Res 561 (30 Apr 2026 / in force 1 Oct 2026); the eFX crypto-settlement ban + USD 10k ceiling; the
> USD 100k / 500k FX caps and their not-FX-authorised-counterparty trigger; the algorithmic-
> stablecoin prohibition (fiat / public-debt-only reserves); the biennial independent audit; the
> R$10.8m–R$37.2m SPSAV minimum-capital range (the earlier R$1–3m figure was a rejected 2024-
> consultation proposal).
> **Tier 1b — confirmed against the resolution text in this pass:** Res 520 **Art. 4**
> (modalities), **Art. 28–30** (segregation / proof-of-reserves / biennial reasonable-assurance
> audit / §1 website disclosure), **Art. 44** (Travel Rule) + **Art. 89** (two-stage phase-in:
> domestic by **Feb 2027**, international by **2 Feb 2028**); Res 521 **Art. 76-A** (the câmbio-
> inclusion hook, **inserted into Res 277/2022** as a new Título VIII-A) and **Art. 82-A** (monthly
> reporting **per Anexo II-A**, the official schedule label appended to Res 277/2022); the USD 100k
> cap wording.
> **Tier 2 — corrected in this pass (prior drafts carried an error):** (i) "Lei 14.286/2021 Art.
> 76-A" — 76-A is a **Res 277/521** provision, not an article of the FX *Law*; the legal authority
> is **Lei 14.286 (chiefly Art. 5)** read with Lei 14.478 Art. 7-V; (ii) Res 520 **Art. 88** was
> mis-framed as a Travel-Rule/AML hook — it is the **authorisation adjustment period** (270-day
> adequação for existing operators), separate from the Art. 44/89 Travel Rule; (iii) the
> **"DeCripto"** return label — not in the resolution; the in-text label is **Anexo II-A**; (iv)
> IOF is **not in force** — the câmbio classification creates the *fato gerador*, but the Receita
> Federal has issued no levy (see the Compliance-Posture note).
> **Tier 3 — still open; confirm against the official text before citing as resolution text:** the
> Art. 64+ asset-curation pinpoint and the ~5% own-asset liquidity carve-out; the "reasonable
> assurance" wording (the audit article itself is Art. 30); the per-modality capital breakdown; Res
> 561 **Art. 56-A / 56-B**; and the CVM **Parecer de Orientação 40** number.
> **As-of note.** Brazil is in rolling implementation (Res 561 in force 1 Oct 2026; registration
> deadlines 30 Oct 2026; eFX-provider authorisation 31 May 2027; Travel Rule phased — domestic by
> Feb 2027, international by 2 Feb 2028; IOF unresolved) — a reader after mid-2026 should re-verify
> these moving parts. Add to v0.9.4 (pre-release) or fold into v1.0 (Sept 2026).

---

## A. Deltas to existing sections

**Coverage line (cover page).** Replace with:
> Coverage: United States · European Union · United Kingdom · Singapore · Hong Kong SAR · Mainland China · **Brazil**

**How to Use This Matrix.** "six stablecoin regimes" → **"seven stablecoin regimes."**
(v1.1 still adds Switzerland and the United Arab Emirates.)

**Executive Summary — insert after the Mainland China paragraph:**

> **Brazil.** The Banco Central do Brasil (BCB) published its virtual-asset framework —
> Resolutions 519, 520 and 521 — on November 10, 2025, in force February 2, 2026, with audit
> and reporting obligations commencing May 4, 2026. Resolution 561, published April 30, 2026
> and in force October 1, 2026, separately closes the retail eFX rail's external settlement
> leg to virtual assets. Brazil's distinctive choice falls on the monetary-sovereignty axis:
> it imposes no MiCA-style aggregate-volume cap (the EU approach under MiCA Article 23) and
> does not prohibit issuance (the PRC approach), but it is not a no-limits regime — it
> reclassifies cross-border virtual-asset payments as foreign-exchange (câmbio) operations
> under the Foreign Exchange Law (Lei 14.286/2021), operationally via Article 76-A inserted
> into Resolution 277/2022, and subjects them to a per-operation cap — USD 100,000 for a
> virtual-asset service provider (PSAV) and USD 500,000 for an FX-authorised institution —
> that binds when the foreign counterparty is not authorised to operate in the Brazilian FX
> market. The operative novelty is the reclassification of the stablecoin leg as an FX
> operation, not the cap as such (a per-operation cap is itself a quantitative limit).
> Resolution 520 adds an asset-curation gate prohibiting algorithmic and unbacked
> fiat-pegged tokens, and a patrimonial-segregation regime with a biennial, reasonable-
> assurance independent audit publicly disclosed on the provider's website. The CVM retains
> jurisdiction over tokens that are securities.

**Pattern 2 (monetary sovereignty asymmetry) — extend.** The pattern currently contrasts the
EU volume cap with the PRC prohibition. Add Brazil as a **third resolution of the same
problem**, stated precisely: Brazil imposes **no MiCA-style means-of-exchange / aggregate-volume
cap**, yet it is not a no-limits regime — it **reclassifies** non-BRL stablecoin flows into the
foreign-exchange (câmbio) regime (capturing them in balance-of-payments statistics), **overlays a
per-operation cap** (USD 100k SPSAV / USD 500k FX-authorised institution, binding when the
counterparty is not FX-authorised), and forecloses the mass-market eFX rail to crypto. The
operative novelty is the **jurisdictional reclassification of the stablecoin leg as an FX
operation**, not the cap as such: a per-operation cap is itself a quantity limit, so anchoring the
contrast on "caps vs no caps" would collapse the EU comparison into a difference of degree
(per-transaction vs aggregate) and weaken the "third type" claim. Anchored on reclassification, the
three-way contrast (EU aggregate-volume cap · PRC prohibition · BR FX-channelling + per-operation
cap) holds: the monetary-sovereignty constraint admits structurally different solutions, not just
looser or tighter thresholds. **Caveat on the C7 mapping.** Brazil's structural *effect* is
comparable to the EU's monetary-sovereignty mechanism, but its stated *motive* differs — the BCB
frames the measure mainly around FX-market integrity, traceability and balance-of-payments capture
(with dollarization a stated concern), rather than the EU's explicit euro-protection rationale; the
comparison here is by effect, not by legislative intent.

---

## B. Brazil — full jurisdictional entry

### Brazil
**Status:** Live regime entering force; main provisions in force February 2, 2026; audit and BCB reporting from May 4, 2026; eFX crypto-settlement ban (Res 561) in force October 1, 2026; key recent action — BCB published Resolutions 519/520/521 (Nov 10, 2025) and Resolution 561 (Apr 30, 2026).

**Statutory Framework**
Lei 14.478/2022 (Marco Legal dos Ativos Virtuais) establishes the virtual-assets regime; Decreto 11.563/2023 designates the BCB as the competent authority while preserving CVM jurisdiction over virtual assets that are securities. Resolutions BCB 519, 520 and 521 (Nov 10, 2025; in force Feb 2, 2026) operationalise PSAV authorisation, conduct, custody/segregation, and the entry of virtual-asset international payments into the foreign-exchange market. The FX limb regulates the Foreign Exchange Law, Lei 14.286/2021 — operationally, Res 521 inserts Article 76-A into Res 277/2022 (a new Título VIII-A) as the câmbio-inclusion hook; note Art. 76-A is a provision of Res 277/521, not of Lei 14.286 itself. Resolution BCB 561/2026 amends Res 277/2022 to govern the eFX (electronic international payment) service.

**Regulators**
   • Banco Central do Brasil (BCB) — virtual-asset service providers, custody, and the foreign-exchange perimeter
   • Comissão de Valores Mobiliários (CVM) — virtual assets classified as securities (valores mobiliários); investment funds under Resolução CVM 175

**Issuer Pathways and Eligibility**
   • Providing virtual-asset services requires prior BCB authorisation as a PSAV (prestadora de serviços de ativos virtuais)
   • Three provider modalities under Res 520 Art. 4: intermediary (intermediação), custodian (custódia), broker (corretagem — combining both functions); a provider may not accumulate incompatible functions
   • Provider must be a Brazil-established entity; fit-and-proper and minimum-capital expectations apply
   • Already-regulated institutions (banks, payment institutions, DTVM/CTVM, corretoras de câmbio) may provide virtual-asset services within their existing authorisation, on notification
   • Grandfathering: providers already operating before Feb 2, 2026 may continue while authorisation is processed; transactions with non-authorised providers are prohibited from October 30, 2026
   [⚠ interpretive question] The resolutions distinguish provider modalities and impose differentiated obligations, but the boundary between "intermediação" and "corretagem" for a provider that both routes and holds client assets is an application question that BCB authorisation practice will settle.

**Reserve and Backing Requirements**
   • Asset curation (Res 520): PSAVs may not offer or intermediate algorithmic stablecoins, or any fiat-pegged token without effective, verifiable liquid-asset backing (reserves limited to fiat currency or public-debt securities); the provider maintains a board-approved listing policy reviewing the white paper, code and backing
   • Eligible reserve asset for a fiat-referenced token is defined as the fiat currency plus government bonds issued by the same government(s) that issue that currency
   • The framework regulates providers rather than imposing a domestic stablecoin-issuer reserve schedule of the GENIUS/MiCA kind; backing is policed at the curation/listing gate

**Capital Requirements**
   • Minimum-capital and prudential expectations are set for PSAVs by modality under Res 519/520; FX-authorised institutions remain subject to their existing prudential regime
   • Minimum capital for SPSAVs is set by **Resolução Conjunta CMN/BCB nº 14/2025** and **Res BCB 517/2025** (both 3 Nov 2025), scaled by activity/modality, in the range **R$10,800,000–R$37,200,000** (per the BCB's 10 Nov 2025 press conference; ANBIMA: "R$10.8 million to R$37.2 million in minimum capital"). Res 519/520 themselves do not hard-code a figure — they cross-refer to this capital methodology
   [⚠ Tier 2 — firm-summary; confirm against Res. Conjunta 14/2025 + Res 517 text] NB the often-cited **R$1m–3m** range was the **rejected 2024 public-consultation (CP 109/110) proposal**, not the binding regime — do not cite R$1–3m / USD 181,500–544,500 as operative.

**Yield and Interest Treatment**
   • No express prohibition on issuer-paid yield to stablecoin holders analogous to GENIUS Act § 4(a)(11) or MiCA Article 50
   • Res 520 prohibits PSAVs from offering credit (oferta de crédito), which constrains some pass-through structures
   • A token marketed as yield-bearing or as an investment would likely be a security under CVM jurisdiction (functional test per CVM Parecer de Orientação 40), leaving the BCB PSAV perimeter
   [⚠ interpretive question] Brazil's yield axis diverges from the US/EU express-ban model: the constraint operates indirectly (credit prohibition + securities reclassification) rather than as a holder-yield ban. This is itself a comparative data point for Pattern 1.

**Redemption Mechanics**
   • The framework does not impose a GENIUS/MiCA-style at-par holder-redemption right on a domestic stablecoin issuer; redemption is governed by provider terms, the custody/segregation rules, and (for securities-like tokens) CVM rules
   [⚠ interpretive question] Confirm whether any redemption-timing obligation attaches to fiat-referenced-token providers under Res 520.

**AML / KYC Framework**
   • PLD/FT (AML/CFT) governance under Res 519/520: KYC, transaction monitoring, suspicious-activity reporting, recordkeeping, FATF-aligned
   • Travel Rule internalised at Res 520 Art. 44 (originator + beneficiary data, incl. wallet addresses), phased over two stages per Art. 89 — domestic provider-to-provider transfers by February 2027, then international transfers, full compliance by February 2, 2028; documented client self-declaration permitted during the phase-in. Res 521 adds Know-Your-Transaction duties. Separately, Res 520 Art. 88 is the authorisation adjustment period (the 270-day "período de adequação" for entities already operating at entry into force), which carries general compliance obligations — internal controls, cybersecurity, and Law 13.810/2019 (UN sanctions) screening — but is not itself the Travel-Rule hook
   • Identification of self-hosted (autocustodiada) wallet owners required for FX-classified operations

**Cross-Border Data Treatment**
   • Lei Geral de Proteção de Dados (LGPD, Lei 13.709/2018) governs personal data, including international transfers (adequacy, standard contractual clauses, or consent)
   • Res 521 requires identification/traceability of parties (and self-hosted-wallet owners) to cross-border virtual-asset operations; Art. 82-A mandates monthly BCB reporting of FX/virtual-asset operations from 4 May 2026 (the information is reported per Anexo II-A, the official schedule appended to Res 277/2022; the "DeCripto" label sometimes seen in commentary is not in the resolution text), feeding the balance-of-payments perimeter

**Distribution and Offering Restrictions**
   • Only BCB-authorised PSAVs (and already-regulated institutions within scope) may offer virtual-asset services in Brazil; non-authorised-provider transactions prohibited from October 30, 2026
   • Cross-border virtual-asset payments must run through the authorised-VASP-in-FX channel (Res 521); the retail eFX rail may not settle the external leg in virtual assets (Res 561), and is itself capped at USD 10,000 per operation
   • Above the per-operation FX caps, no crypto rail is available and the flow reverts to traditional câmbio (bank FX desk / DTVM)

**Implementation Timeline**
   • December 2022: Lei 14.478/2022 enacted (Marco Legal dos Ativos Virtuais)
   • June 2023: Decreto 11.563/2023 designates the BCB
   • November 10, 2025: Resolutions BCB 519/520/521 published
   • January 22, 2026: Instrução Normativa BCB 701 (independent technical certification)
   • February 2, 2026: main provisions in force
   • April 30, 2026: Resolution BCB 561 published (eFX)
   • May 4, 2026: audit and BCB reporting obligations commence
   • October 1, 2026: Resolution 561 in force (eFX crypto-settlement ban)
   • October 30, 2026: non-authorised-provider prohibition; eFX-modality Unicad registration deadline for authorised institutions
   • May 31, 2027: unauthorised eFX providers must apply for payment-institution authorisation
   • February 2027: Travel Rule stage 1 — domestic provider-to-provider transfers
   • February 2, 2028: full Travel Rule compliance — international transfers

**Compliance Posture for Cross-Border Operations**
Brazil's framework is best read not as a stablecoin-issuer regime but as a **virtual-asset-service-provider and foreign-exchange regime**: it does not license a domestic USD or BRL stablecoin issuer the way GENIUS or MiCA do, but it decides, at the provider and FX-rail level, which cross-border stablecoin flows are permitted and how large each may be. For a cross-border operator the binding facts are three. First, the eligible rail is the authorised-VASP-in-FX channel; the retail eFX rail is closed to crypto on the external leg and is in any case a low-value rail (USD 10,000 per operation). Second, the per-operation cap — USD 100,000 for a PSAV, USD 500,000 for an FX-authorised institution — bites whenever the foreign counterparty is not BCB-FX-authorised, which is the ordinary B2B case; above the cap the operation reverts to traditional câmbio. Third, only auditable-reserve tokens may be used: the asset-curation gate excludes algorithmic and opaque-reserve coins regardless of rail. The open variable is tax: the câmbio classification under Res 521 creates the IOF taxable event (fato gerador), but no levy is yet in force — the power to impose IOF is the Receita Federal's, not the BCB's, and as of June 2026 the Receita has issued no instrument bringing collection into effect. A Receita / Ministério da Fazenda proposal would extend IOF-Câmbio at 3.5% to stablecoin purchases (against a competing "private foreign currency" characterisation at a reduced 1.1% rate), but it remains in consultation; this is the principal cost uncertainty for the channel.
   [⚠ interpretive question] IOF treatment — the câmbio classification under Res 521 creates the taxable event (fato gerador), but IOF is not yet levied: collection is the Receita Federal's competence and no Receita instrument is in force as of June 2026. A proposal (IOF-Câmbio 3.5% on stablecoin purchases vs a "private foreign currency" 1.1% treatment) is in consultation pending Receita Federal / Ministério da Fazenda action.
