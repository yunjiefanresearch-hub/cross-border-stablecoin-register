# Cross-Border Stablecoin Architecture — Brazil insertions (paste-ready, paper voice)

> **Scope note.** These insertions extend the paper from six to seven surveyed
> jurisdictions and add the HK→BR corridor (already in the register) as a worked pairwise
> cell. The numbering assumes Brazil enters as a new **§5.8** and the existing Pairwise
> Compatibility Analysis becomes **§5.9** (and §2's "six jurisdictions" → "seven" throughout).
> **Verification status — three evidence tiers (as of June 2026; aligns with register v0.3.2).**
> **Tier 1 (well-corroborated**, across multiple independent firm/practitioner sources and
> consistent with the statutory structure): the publication / in-force / audit dates and the
> Res 561 timeline; the USD 100k / 500k caps + not-FX-authorised-counterparty trigger; the eFX
> ban + USD 10k ceiling; the algorithmic-stablecoin prohibition + fiat/public-debt reserves; the
> biennial independent audit; the R$10.8m–R$37.2m SPSAV minimum-capital range.
> **Tier 1b (confirmed against the resolution text in this pass):** Res 520 **Art. 4** (the three
> SPSAV modalities), **Art. 28–30** (segregation / proof-of-reserves / biennial reasonable-
> assurance audit / §1 website disclosure), **Art. 44** (Travel Rule) and **Art. 89** (two-stage
> phase-in: domestic by **Feb 2027**, international by **2 Feb 2028**); Res 521 **Art. 76-A** —
> the câmbio-inclusion hook **inserted into Res 277/2022** (new Título VIII-A), **not** an article
> of Lei 14.286/2021 — and **Art. 82-A** (monthly reporting **per Anexo II-A**, the official
> schedule label appended to Res 277/2022); the USD 100k cap wording.
> **Tier 2 (corrected in this pass — prior drafts carried an error):** "Lei 14.286/2021 Art. 76-A"
> (76-A is a Res 277/521 provision; the *legal* authority is Lei 14.286, chiefly Art. 5, read with
> Lei 14.478 Art. 7-V); the framing of Res 520 **Art. 88** as a Travel-Rule/AML-controls hook
> (Art. 88 is the **authorisation adjustment period** — the 270-day adequação for existing
> operators — distinct from the Art. 44/89 Travel Rule); and the **"DeCripto"** return label (not
> in the resolution; the in-text label is **Anexo II-A**).
> **Tier 3 (still open; confirm against the official text before relying as resolution text):** the
> Art. 64+ asset-curation pinpoint and the ~5% own-asset liquidity carve-out; the per-modality
> capital breakdown within the R$10.8–37.2m range; Res 561 **Art. 56-A / 56-B**; the CVM **Parecer
> de Orientação 40** number; and the IOF treatment (see below — the câmbio classification creates
> the *fato gerador*, but no Receita Federal levy is in force as of June 2026).

---

## 1. New section — §5.8 Brazil — BCB Virtual-Assets Framework + eFX (Lei 14.478/2022; Res 519/520/521; Res 561)

> *Insert after §5.7 (People's Republic of China); renumber the Pairwise Compatibility
> Analysis to §5.9.*

Brazil operates under the Virtual-Assets Law (Lei 14.478/2022, the *Marco Legal dos Ativos Virtuais*) and Decreto 11.563/2023, which designate the Banco Central do Brasil as the competent authority for virtual-asset service providers while preserving the Comissão de Valores Mobiliários jurisdiction over virtual assets that are securities. The operative provider framework is the trio of Resolutions BCB 519, 520 and 521, published November 10, 2025 and in force February 2, 2026, with audit and reporting obligations commencing May 4, 2026. Issuer eligibility, in the sense the eight-constraint framework uses the term, is a provider-authorisation question rather than a stablecoin-issuer-licensing question: Brazil does not license a domestic USD- or BRL-referenced stablecoin issuer in the manner of the GENIUS Act or MiCA, but requires prior BCB authorisation as a *prestadora de serviços de ativos virtuais* (SPSAV) across three modalities defined in Resolution 520 Article 4 — intermediation, custody, and brokerage — with mandatory Brazilian establishment and a minimum capital, scaled by activity, in the range R$10.8 million to R$37.2 million under Resolução Conjunta CMN/BCB nº 14/2025 and Resolution BCB 517/2025 (the lower R$1–3 million figure that circulated earlier was a 2024-consultation proposal that was not retained). Reserve composition is policed not through an issuer reserve schedule but through an asset-curation gate in Resolution 520, which prohibits providers from offering or intermediating algorithmic stablecoins or any fiat-pegged token without effective, verifiable liquid-asset backing, and which defines the eligible reserve asset as the reference fiat currency plus government bonds of the issuing government. Custody and disclosure are addressed by a patrimonial-segregation regime requiring client assets to be held separately from the provider's own, with documented proof-of-reserves methods and a biennial, reasonable-assurance independent audit publicly disclosed on the provider's website; FATF Travel-Rule obligations are internalised at Resolution 520 Article 44 and phased over two stages under Article 89 (domestic provider-to-provider transfers by February 2027, then international transfers, with full compliance by February 2, 2028), and Resolution 521 Article 82-A adds monthly foreign-exchange reporting to the BCB from May 4, 2026.

The constraint that distinguishes Brazil from the six jurisdictions previously surveyed is its treatment of the monetary-sovereignty problem (C7). Brazil neither caps non-domestic-currency stablecoin usage by aggregate volume, as the European Union does through MiCA Article 23, nor prohibits issuance, as the People's Republic of China does. Instead, Resolution 521 reclassifies authorised providers' cross-border virtual-asset payments as foreign-exchange (câmbio) operations regulated under the Foreign Exchange Law (Lei 14.286/2021) — operationally, by inserting Article 76-A into Resolution 277/2022 (a new Título VIII-A bringing virtual-asset services into the câmbio market) — bringing them within the balance-of-payments perimeter, and imposes a per-operation cap that binds whenever the foreign counterparty is not authorised to operate in the Brazilian foreign-exchange market: USD 100,000 for a PSAV and USD 500,000 for an FX-authorised institution. Resolution 561, published April 30, 2026 and in force October 1, 2026, closes the complementary low-value retail rail — the electronic international payment service (eFX), which is itself capped at USD 10,000 per operation — to virtual-asset settlement on the external leg, requiring settlement through a foreign-exchange operation or a non-resident real account. Brazil therefore resolves the monetary-sovereignty constraint through a third architectural mechanism — foreign-exchange channeling combined with a per-operation ceiling — distinct from both the aggregate-volume cap and the prohibition. The distinguishing feature is the reclassification rather than the ceiling as such: a per-operation cap is itself a quantitative limit, so the contrast with the European Union is not merely per-transaction versus aggregate but the prior step of routing the stablecoin leg through the foreign-exchange perimeter, where it inherits FX registration, reporting, and (potentially) IOF obligations. Above the ceilings, no virtual-asset rail is available and the operation reverts to traditional câmbio. A caveat on the comparison is warranted: although the structural effect resembles the European Union's monetary-sovereignty mechanism, the BCB's stated rationale emphasises foreign-exchange-market integrity, traceability, and balance-of-payments measurement — with dollarisation a stated concern — rather than the explicit currency-protection rationale of MiCA Article 23, so the mapping to C7 is by structural effect rather than by legislative intent.

The securities-classification constraint (C4) operates through the BCB/CVM jurisdictional division: a token with the characteristics of a security is regulated by the CVM rather than (only) by the BCB provider regime (the functional securities-versus-virtual-asset test follows CVM Parecer de Orientação 40), and Brazilian investment funds — the natural routing destination — are governed by Resolução CVM 175. As with the analysis in §4, the Brazilian resolution of C4 to date is one of token classification and asset curation rather than a developed treatment of routing a stablecoin balance into a registered fund; the application of the CVM funds framework to a tokenised money-market-fund routing arrangement is not yet elaborated in the public record and is identified in §8.4 as a subject for further work. The principal unresolved variable is the financial-transaction tax (IOF): the foreign-exchange classification under Resolution 521 creates the taxable event (fato gerador), but no levy is yet in force — the power to impose IOF rests with the Receita Federal, not the BCB, and as of June 2026 the Receita has issued no instrument bringing collection into effect; a proposal to extend IOF-Câmbio at the standard 3.5% rate to stablecoin purchases (against a competing "private foreign currency" characterisation at a reduced rate) remains in consultation, so the outcome cannot be anticipated here. This account states Brazil's framework as of June 2026; several provisions phase in on a rolling schedule (the eFX virtual-asset settlement ban from October 1, 2026, the non-authorised-provider and eFX-registration deadlines of October 30, 2026, the eFX-provider authorisation deadline of May 31, 2027, the first Travel-Rule stage for domestic provider-to-provider transfers by February 2027, and full Travel-Rule compliance for international transfers by February 2, 2028), and the IOF treatment remains unresolved, so the position should be re-verified for any date materially later than mid-2026.

---

## 2. New pairwise cells — add to §5.9 (was §5.8) Pairwise Compatibility Analysis

> *Insert in jurisdiction order; both cells are Category II with a per-operation sizing
> ceiling — the rail exists but is capped, so the constraint is sizing, not unresolved
> composition (Category III).*

**United States × Brazil — Category II (with a per-operation sizing ceiling).** Issuer eligibility is non-coextensive: a GENIUS-Act payment-stablecoin issuer is not authorised as a Brazilian PSAV, and vice versa. A USD-referenced payment stablecoin reaching Brazil must move through the authorised-VASP-in-FX channel of Resolution 521, i.e. through partnership with a BCB-authorised provider, because the retail eFX rail is closed to virtual-asset settlement on the external leg (Resolution 561). The per-operation cap — USD 100,000 where the Brazilian counterparty operates as a PSAV, USD 500,000 where it is an FX-authorised institution — binds because the US issuer is not authorised in the Brazilian foreign-exchange market; above the cap the flow reverts to traditional câmbio. The GENIUS Act yield prohibition and reserve constraints apply on the United States side; Brazil's asset-curation gate (Resolution 520) independently requires that the instrument be an auditable-reserve, non-algorithmic stablecoin. The §18 comparability mechanism does not assist, as it runs to foreign issuers circulating in the United States, not to United States issuers circulating abroad. Operative interaction sets: A (issuer eligibility × cross-border payment), D (reserve composition × monetary sovereignty).

**Hong Kong × Brazil — Category II (with a per-operation sizing ceiling).** This pair is worked in detail as the HK→BR USD-settlement corridor in the companion register. On the Hong Kong side the operative constraint is eligibility rather than a numeric cap: because the first-cohort FRS licences are HKD-referenced (Anchorpoint's HKDAP and HSBC) and no USD-referenced FRS has been licensed, a USD-referenced coin cannot use a domestically licensed Hong Kong issuance pathway and must be an offshore non-HKD FRS distributed through a permitted offeror to professional investors; where the flow routes into a tokenised money-market fund, the SFC treats that fund as a tokenised security. On the Brazilian side the constraint is the rail-and-cap structure: the authorised-VASP-in-FX channel within the USD 100,000 / 500,000 per-operation ceiling, using an auditable-reserve stablecoin. The two legs gate on different axes — Hong Kong on who may issue and offer and to whom, Brazil on which rail and up to what size — so a single USD-stablecoin instrument cannot serve both as one uniform rail; the corridor's architecture must satisfy a four-way composition of rail, per-operation cap, auditable-reserve eligibility, and Hong Kong perimeter eligibility simultaneously. Operative interaction sets: A (issuer eligibility × cross-border payment), D (reserve composition × monetary sovereignty), E (securities classification × cross-border payment, where the flow touches a tokenised fund).

---

## 3. Edits to §8 (Limits and Research Agenda)

**§8.3, limit 1 — remove Brazil from the not-surveyed list.** The sentence currently reads
that the paper "does not survey other jurisdictions … Japan, the United Arab Emirates,
Switzerland, **Brazil**, the Bahamas, and Bermuda …". Strike "Brazil," from the list (Brazil
is now surveyed in §5.8). The remaining sentence stands.

**§8.4, research agenda item 1 — move Brazil from "developing variation" to "completed; deepen."**
Replace the parenthetical "(Brazil, India, the Republic of Korea)" with "(India, the Republic
of Korea)," and add a sentence: "Brazil, surveyed in §5.8, is the first jurisdiction in this
paper to resolve the monetary-sovereignty constraint by foreign-exchange channeling rather
than by volume cap or prohibition; the open lines for Brazil are the application of the CVM
investment-funds framework (Resolução CVM 175) to a tokenised-fund routing arrangement and
the IOF treatment of foreign-exchange-classified stablecoin operations."

**Optional cross-reference in §3 or §6.** The HK×BR corridor is a clean illustration of a
composition that is feasible but bounded: the rail exists on both legs, yet no single
instrument serves both uniformly. If a forward reference is wanted, cite the register
corridor `hk-br-usd-stablecoin-settlement-001` as the worked example.
