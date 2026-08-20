# BR jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 12
- Legal status: `{"operative": 12}`
- Evidence tier: `{"firm_summary": 2, "resolution_text": 10}`
- Source disposition: `{"official": 12}`
- Freshness: `{"stale": 10, "unknown": 2}`
- Review stage: `{"primary_reviewed_second_pending": 10, "unreviewed": 2}`
- Named second reviewer: 0/12

## Official source families

- `www.bcb.gov.br` — 10 record(s)
- `www.planalto.gov.br` — 2 record(s)

## Institutional and supervisory boundary

### `br-vasp-monetary_sovereignty-001` — `monetary_sovereignty`

Brazil does not impose a MiCA-style volume cap on the use of non-domestic-currency (e.g. USD) stablecoins as a means of exchange. Instead it asserts monetary-sovereignty control through three mechanisms: (i) reclassifying cross-border virtual-asset payments as foreign-exchange (câmbio) operations under Lei 14.286/2021 (Res BCB 521), bringing them into the FX / balance-of-payments perimeter; (ii) per-operation caps on those FX-classified operations (USD 100k SPSAV / USD 500k FX-FI where the counterparty is not FX-authorised); and (iii) closing the eFX retail rail's external settlement leg to virtual assets (Res BCB 561), so mass low-value flows cannot settle abroad in crypto. Context: estimates of the stablecoin share of Brazilian crypto activity vary by metric and period — BCB officials have cited roughly 90% of crypto flows, while some market trackers report nearer two-thirds (~67%) of crypto volume; either way stablecoins dominate, which motivated the FX framing. [share figure to be locked to a single dated source before citing as primary].

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `br-vasp-regulatory_authority-001` — `regulatory_authority`

Lei 14.478/2022 (Marco Legal dos Ativos Virtuais) and Decreto 11.563/2023 designate the Banco Central do Brasil (BCB) as the authority for virtual-asset service providers (SPSAVs), while preserving the Comissão de Valores Mobiliários (CVM) jurisdiction over virtual assets that are securities (token taxonomy follows CVM Parecer de Orientação 40). The operative VASP framework is Res BCB 519/520/521 (pub. 10 Nov 2025; in force 2 Feb 2026), supplemented by Res BCB 561/2026 for the eFX rail. The foreign-exchange classification of cross-border virtual-asset payments rests on the Foreign Exchange Law, Lei 14.286/2021.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `br-vasp-securities_classification-001` — `securities_classification`

Lei 14.478/2022 and Decreto 11.563/2023 preserve CVM jurisdiction over virtual assets that are securities (valores mobiliários) and over investor-protection issues; the functional securities-vs-virtual-asset distinction follows CVM Parecer de Orientação 40. A token with collective-investment / securities characteristics is regulated by the CVM, not (only) by the BCB SPSAV regime. Brazilian investment funds — the natural routing destination — are governed by Resolução CVM 175. A USD-referenced payment stablecoin is treated by the BCB as a foreign-exchange instrument rather than a security.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Authorisation and licensing perimeter

### `br-vasp-bank_nonbank_routing-001` — `bank_nonbank_routing`

Virtual-asset services are supervised by the Banco Central do Brasil; issuance and distribution run through authorized payment/virtual-asset service providers under the central bank's prudential perimeter.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `br-vasp-issuer_pathway-001` — `issuer_pathway`

Providing virtual-asset services in Brazil requires prior BCB authorisation as an SPSAV. Under Res BCB 520 Art. 4 there are three modalities — Intermediário, Custodiante and Corretor (intermediary / custodian / broker, the broker combining both functions); a provider may not accumulate incompatible functions. Already-regulated institutions may also offer virtual-asset services on notification to the BCB: commercial / investment / multiple banks, Caixa Econômica Federal, and securities brokers (CTVM), distributors (DTVM) and FX dealers (corretoras de câmbio). Overseas providers must be authorised before operating, requiring a local subsidiary or partnership with a licensed local entity. Grandfathering: providers operating before 2 Feb 2026 may continue while authorisation is processed (apply within ~260–270 days), but transactions with non-authorised providers are prohibited from 30 Oct 2026, after which a non-compliant provider must cease within 30 days.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Reserve, safeguarding and redemption

### `br-vasp-capital_requirements-001` — `capital_requirements`

Minimum capital for SPSAVs is set by Resolução Conjunta CMN/BCB nº 14/2025 and Res BCB 517/2025 (both 3 Nov 2025), scaled by activity/modality. Per the BCB's 10 Nov 2025 press conference the range is R$10,800,000–R$37,200,000 (ANBIMA: 'VASPs must now hold R$10.8 million to R$37.2 million in minimum capital'). Res BCB 519/520 do not hard-code a capital figure; they cross-refer to this methodology. FX-authorised institutions (banks, DTVM/CTVM, corretoras de câmbio) remain subject to their existing prudential regimes. IMPORTANT: the frequently-cited R$1m–3m (~USD 181,500–544,500) range was the REJECTED 2024 public-consultation (CP 109/110) proposal, NOT the binding regime.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `br-vasp-reserve_backing-001` — `reserve_backing`

For a fiat-referenced virtual asset (stablecoin), Res BCB 520/2025 defines the reserve assets as the fiduciary currency plus public debt issued by the same governments that issue those currencies (Art. 2, III), requires proof of reserves, and prohibits algorithmic reserve control with public disclosure of the criteria (Arts. 64+). In force 2 Feb 2026.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Cross-border and data conditions

### `br-vasp-cross_border_data-001` — `cross_border_data`

Res BCB 521 integrates authorised SPSAVs' virtual-asset international payments and transfers into the Brazilian foreign-exchange (câmbio) market, regulating the Foreign Exchange Law (Lei 14.286/2021). In scope: international payment/transfer with virtual assets; settlement of international card obligations; transfers to/from self-hosted wallets; and purchase/sale/exchange of fiat-referenced virtual assets. Each operation carries a per-operation cap that binds when the foreign counterparty is NOT authorised to operate in the Brazilian FX market: USD 100,000 for an SPSAV and USD 500,000 for an FX-authorised institution (bank / DTVM / CTVM / corretora de câmbio). Operations require purpose classification under BCB FX codes, identification/traceability of parties (KYT), and identification of self-hosted-wallet owners; cash settlement is prohibited.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `br-vasp-monetary_sovereignty-001` — `monetary_sovereignty`

Brazil does not impose a MiCA-style volume cap on the use of non-domestic-currency (e.g. USD) stablecoins as a means of exchange. Instead it asserts monetary-sovereignty control through three mechanisms: (i) reclassifying cross-border virtual-asset payments as foreign-exchange (câmbio) operations under Lei 14.286/2021 (Res BCB 521), bringing them into the FX / balance-of-payments perimeter; (ii) per-operation caps on those FX-classified operations (USD 100k SPSAV / USD 500k FX-FI where the counterparty is not FX-authorised); and (iii) closing the eFX retail rail's external settlement leg to virtual assets (Res BCB 561), so mass low-value flows cannot settle abroad in crypto. Context: estimates of the stablecoin share of Brazilian crypto activity vary by metric and period — BCB officials have cited roughly 90% of crypto flows, while some market trackers report nearer two-thirds (~67%) of crypto volume; either way stablecoins dominate, which motivated the FX framing. [share figure to be locked to a single dated source before citing as primary].

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## AML, KYC and financial-crime controls

### `br-vasp-aml_kyc-001` — `aml_kyc`

Res BCB 520 Art. 44 internalises the FATF Travel Rule as a domestic obligation: for each transfer the originator's institution must transmit complete data on the originator (name, CPF/CNPJ, account) and the beneficiary, including wallet addresses, plus suspicious-activity reporting and AML/CTF (PLD/FT) governance. Res BCB 521 adds Know-Your-Transaction (KYT) duties, requiring identification of self-hosted-wallet owners. Travel-Rule implementation is phased over two stages (Art. 89): first domestic transfers between Brazil-established PSAVs (by February 2027), then international transfers (full compliance by 2 February 2028); during the phase-in SPSAVs may rely on documented client self-declarations. Separately, Art. 88 is the authorisation adjustment/transition provision (the 270-day 'período de adequação' for entities already operating at entry into force), which carries general compliance obligations — internal controls, cybersecurity, and Law 13.810/2019 (UN Security Council sanctions) screening — but is NOT itself the Travel-Rule hook.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Enforcement and implementation posture

### `br-vasp-disclosure_reporting-001` — `disclosure_reporting`

Res BCB 520 requires SPSAVs to document proof-of-reserves methods and to publish reports and reserve attestations, with an independent audit on a biennial basis (sources: 'biennial / biannual independent audit cycle'). Res BCB 521 Art. 82-A adds mandatory monthly reporting to the BCB of all FX transactions and international transfers involving virtual assets (including self-hosted-wallet data and counterparty identification), following the model used for traditional international transactions; the information is reported per 'Anexo II-A' and the obligation commences 4 May 2026. Instrução Normativa BCB 701 (22 Jan 2026) sets the form of the independent technical certification for intermediation/custody.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `br-vasp-regulatory_authority-001` — `regulatory_authority`

Lei 14.478/2022 (Marco Legal dos Ativos Virtuais) and Decreto 11.563/2023 designate the Banco Central do Brasil (BCB) as the authority for virtual-asset service providers (SPSAVs), while preserving the Comissão de Valores Mobiliários (CVM) jurisdiction over virtual assets that are securities (token taxonomy follows CVM Parecer de Orientação 40). The operative VASP framework is Res BCB 519/520/521 (pub. 10 Nov 2025; in force 2 Feb 2026), supplemented by Res BCB 561/2026 for the eFX rail. The foreign-exchange classification of cross-border virtual-asset payments rests on the Foreign Exchange Law, Lei 14.286/2021.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `br-vasp-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Res BCB 520/2025 Art. 44 (Travel Rule) + Art. 89 (two-stage phase-in:…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520)<br>Res BCB 520/2025 (PLD/FTP obligations on SPSAVs; ≥3 responsible administrators including AML/CFT; GAFI Recs 1… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Lei 14.478/2022; BCB regulations](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520)<br>Res BCB 520/2025 Art. 20 (besides SPSAVs, only commercial/exchange/investment/multiple banks, Caixa, CTVM/DTV… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-capital_requirements-001` | `capital_requirements` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Resolução Conjunta CMN/BCB nº 14/2025; Res BCB 517/2025 (both 3 Nov 2…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=517)<br>Resolução Conjunta CMN/BCB nº 14/2025 + Res BCB nº 517/2025 (both 3 Nov 2025): minimum capital R$10,800,000 t… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | [Res BCB 521/2025 (virtual assets in the FX market); Lei 14.286/2021 (…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=521)<br>Res BCB 521 — per-operation caps (USD 100k SPSAV / USD 500k FX-FI when counterparty not FX-authorised); amend… | `unknown`; `unreviewed` |
| `br-vasp-custody-001` | `custody` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Res BCB 520/2025 — patrimonial segregation (segregação patrimonial)](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520)<br>Res BCB 520/2025 (patrimonial segregation: client funds in individualised payment/deposit accounts; client vi… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-disclosure_reporting-001` | `disclosure_reporting` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Res BCB 520/2025 (proof-of-reserves + biennial independent audit + pu…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520)<br>Res BCB 520/2025 (proof of reserves; periodic audits; transparent information flows); Res BCB 521/2025 (month… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Res BCB 519/2025 (authorisation regime); Res BCB 520/2025 Art. 4 (pro…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=519)<br>Lei 14.478/2022 (BCB authorisation required to provide virtual-asset services); Res BCB 519/2025 (authorisati… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Res BCB 521/2025 (FX reclassification + caps); Res BCB 561/2026 (eFX…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=521)<br>Res BCB 521/2025 (amends Res 277/278/279 of 31 Dec 2022): virtual-asset services brought into the FX market —… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | [Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); BCB implementing r…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520)<br>Res BCB 520/2025 (VASPs may not offer credit to clients or raise funds from the public except via share issua… | `unknown`; `unreviewed` |
| `br-vasp-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); Decreto 11.563/202…](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm)<br>Lei 14.478/2022 arts. 2-9; Decreto 11.563/2023 (BCB designated competent authority for virtual-asset services… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Res BCB 520/2025 — stablecoin definition + asset-curation / listing-p…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520)<br>Res BCB 520/2025 Art. 2, III (reserve assets of a fiat-referenced token = the fiduciary currency and public d… | `stale`; `primary_reviewed_second_pending` |
| `br-vasp-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Lei 14.478/2022 + Decreto 11.563/2023 (CVM carve-out); CVM Parecer de…](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm)<br>Lei 14.478/2022; Decreto 11.563/2023 (BCB over payment/VASP activity; CVM jurisdiction preserved over tokens… | `stale`; `primary_reviewed_second_pending` |

## Record-level propositions and unresolved work

### `br-vasp-aml_kyc-001`

Res BCB 520 Art. 44 internalises the FATF Travel Rule as a domestic obligation: for each transfer the originator's institution must transmit complete data on the originator (name, CPF/CNPJ, account) and the beneficiary, including wallet addresses, plus suspicious-activity reporting and AML/CTF (PLD/FT) governance. Res BCB 521 adds Know-Your-Transaction (KYT) duties, requiring identification of self-hosted-wallet owners. Travel-Rule implementation is phased over two stages (Art. 89): first domestic transfers between Brazil-established PSAVs (by February 2027), then international transfers (full compliance by 2 February 2028); during the phase-in SPSAVs may rely on documented client self-declarations. Separately, Art. 88 is the authorisation adjustment/transition provision (the 270-day 'período de adequação' for entities already operating at entry into force), which carries general compliance obligations — internal controls, cybersecurity, and Law 13.810/2019 (UN Security Council sanctions) screening — but is NOT itself the Travel-Rule hook.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-bank_nonbank_routing-001`

Virtual-asset services are supervised by the Banco Central do Brasil; issuance and distribution run through authorized payment/virtual-asset service providers under the central bank's prudential perimeter.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-capital_requirements-001`

Minimum capital for SPSAVs is set by Resolução Conjunta CMN/BCB nº 14/2025 and Res BCB 517/2025 (both 3 Nov 2025), scaled by activity/modality. Per the BCB's 10 Nov 2025 press conference the range is R$10,800,000–R$37,200,000 (ANBIMA: 'VASPs must now hold R$10.8 million to R$37.2 million in minimum capital'). Res BCB 519/520 do not hard-code a capital figure; they cross-refer to this methodology. FX-authorised institutions (banks, DTVM/CTVM, corretoras de câmbio) remain subject to their existing prudential regimes. IMPORTANT: the frequently-cited R$1m–3m (~USD 181,500–544,500) range was the REJECTED 2024 public-consultation (CP 109/110) proposal, NOT the binding regime.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-cross_border_data-001`

Res BCB 521 integrates authorised SPSAVs' virtual-asset international payments and transfers into the Brazilian foreign-exchange (câmbio) market, regulating the Foreign Exchange Law (Lei 14.286/2021). In scope: international payment/transfer with virtual assets; settlement of international card obligations; transfers to/from self-hosted wallets; and purchase/sale/exchange of fiat-referenced virtual assets. Each operation carries a per-operation cap that binds when the foreign counterparty is NOT authorised to operate in the Brazilian FX market: USD 100,000 for an SPSAV and USD 500,000 for an FX-authorised institution (bank / DTVM / CTVM / corretora de câmbio). Operations require purpose classification under BCB FX codes, identification/traceability of parties (KYT), and identification of self-hosted-wallet owners; cash settlement is prohibited.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-custody-001`

Res BCB 520 requires mandatory patrimonial segregation: client funds — both fiat and virtual assets — must be fully segregated from the SPSAV's own funds, held in accounts/wallets distinct from corporate treasury, demonstrable beyond accounting records. Custody may be outsourced to a licensed custodian, but regulatory accountability cannot be transferred. (Sources also report a limited own-asset liquidity carve-out and conditions for using foreign custodians; the specific percentage and the foreign-custodian conditions remain to be confirmed against the resolution text.)

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-disclosure_reporting-001`

Res BCB 520 requires SPSAVs to document proof-of-reserves methods and to publish reports and reserve attestations, with an independent audit on a biennial basis (sources: 'biennial / biannual independent audit cycle'). Res BCB 521 Art. 82-A adds mandatory monthly reporting to the BCB of all FX transactions and international transfers involving virtual assets (including self-hosted-wallet data and counterparty identification), following the model used for traditional international transactions; the information is reported per 'Anexo II-A' and the obligation commences 4 May 2026. Instrução Normativa BCB 701 (22 Jan 2026) sets the form of the independent technical certification for intermediation/custody.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-05-04`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-issuer_pathway-001`

Providing virtual-asset services in Brazil requires prior BCB authorisation as an SPSAV. Under Res BCB 520 Art. 4 there are three modalities — Intermediário, Custodiante and Corretor (intermediary / custodian / broker, the broker combining both functions); a provider may not accumulate incompatible functions. Already-regulated institutions may also offer virtual-asset services on notification to the BCB: commercial / investment / multiple banks, Caixa Econômica Federal, and securities brokers (CTVM), distributors (DTVM) and FX dealers (corretoras de câmbio). Overseas providers must be authorised before operating, requiring a local subsidiary or partnership with a licensed local entity. Grandfathering: providers operating before 2 Feb 2026 may continue while authorisation is processed (apply within ~260–270 days), but transactions with non-authorised providers are prohibited from 30 Oct 2026, after which a non-compliant provider must cease within 30 days.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-monetary_sovereignty-001`

Brazil does not impose a MiCA-style volume cap on the use of non-domestic-currency (e.g. USD) stablecoins as a means of exchange. Instead it asserts monetary-sovereignty control through three mechanisms: (i) reclassifying cross-border virtual-asset payments as foreign-exchange (câmbio) operations under Lei 14.286/2021 (Res BCB 521), bringing them into the FX / balance-of-payments perimeter; (ii) per-operation caps on those FX-classified operations (USD 100k SPSAV / USD 500k FX-FI where the counterparty is not FX-authorised); and (iii) closing the eFX retail rail's external settlement leg to virtual assets (Res BCB 561), so mass low-value flows cannot settle abroad in crypto. Context: estimates of the stablecoin share of Brazilian crypto activity vary by metric and period — BCB officials have cited roughly 90% of crypto flows, while some market trackers report nearer two-thirds (~67%) of crypto volume; either way stablecoins dominate, which motivated the FX framing. [share figure to be locked to a single dated source before citing as primary].

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-permitted_activity_yield-001`

The VASP framework and the central bank's implementing rulemaking are still being finalized; whether and how issuers or intermediaries may pass through yield is not yet settled.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-regulatory_authority-001`

Lei 14.478/2022 (Marco Legal dos Ativos Virtuais) and Decreto 11.563/2023 designate the Banco Central do Brasil (BCB) as the authority for virtual-asset service providers (SPSAVs), while preserving the Comissão de Valores Mobiliários (CVM) jurisdiction over virtual assets that are securities (token taxonomy follows CVM Parecer de Orientação 40). The operative VASP framework is Res BCB 519/520/521 (pub. 10 Nov 2025; in force 2 Feb 2026), supplemented by Res BCB 561/2026 for the eFX rail. The foreign-exchange classification of cross-border virtual-asset payments rests on the Foreign Exchange Law, Lei 14.286/2021.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-reserve_backing-001`

For a fiat-referenced virtual asset (stablecoin), Res BCB 520/2025 defines the reserve assets as the fiduciary currency plus public debt issued by the same governments that issue those currencies (Art. 2, III), requires proof of reserves, and prohibits algorithmic reserve control with public disclosure of the criteria (Arts. 64+). In force 2 Feb 2026.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `br-vasp-securities_classification-001`

Lei 14.478/2022 and Decreto 11.563/2023 preserve CVM jurisdiction over virtual assets that are securities (valores mobiliários) and over investor-protection issues; the functional securities-vs-virtual-asset distinction follows CVM Parecer de Orientação 40. A token with collective-investment / securities characteristics is regulated by the CVM, not (only) by the BCB SPSAV regime. Brazilian investment funds — the natural routing destination — are governed by Resolução CVM 175. A USD-referenced payment stablecoin is treated by the BCB as a foreign-exchange instrument rather than a security.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2026-02-02`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

## Legal-event relationships

No first-class event is mapped for this jurisdiction. This is an ontology gap, not proof of no legal change.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); BCB implementing rulemaking](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520) — Res BCB 520/2025 (VASPs may not offer credit to clients or raise funds from the public except via share issuance; client virtual assets may not be used for proprietary operations….
2. [Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); Decreto 11.563/2023 (BCB as VASP authority; CVM carve-out for securities tokens)](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm) — Lei 14.478/2022 arts. 2-9; Decreto 11.563/2023 (BCB designated competent authority for virtual-asset services; CVM retains jurisdiction over tokens that are securities).
3. [Lei 14.478/2022 + Decreto 11.563/2023 (CVM carve-out); CVM Parecer de Orientação 40; Resolução CVM 175 (investment funds)](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm) — Lei 14.478/2022; Decreto 11.563/2023 (BCB over payment/VASP activity; CVM jurisdiction preserved over tokens with securities characteristics).
4. [Lei 14.478/2022; BCB regulations](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520) — Res BCB 520/2025 Art. 20 (besides SPSAVs, only commercial/exchange/investment/multiple banks, Caixa, CTVM/DTVM and FX brokers may provide intermediation/custody, with restrictions….
5. [Res BCB 519/2025 (authorisation regime); Res BCB 520/2025 Art. 4 (provider modalities)](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=519) — Lei 14.478/2022 (BCB authorisation required to provide virtual-asset services); Res BCB 519/2025 (authorisation process); Res BCB 520/2025 Art. 4 (three SPSAV modalities: intermed….
6. [Res BCB 520/2025 (proof-of-reserves + biennial independent audit + published reports); Res BCB 521/2025 Art. 82-A (monthly BCB reporting);…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520) — Res BCB 520/2025 (proof of reserves; periodic audits; transparent information flows); Res BCB 521/2025 (monthly FX-operations reporting from 4 May 2026).
7. [Res BCB 520/2025 Art. 44 (Travel Rule) + Art. 89 (two-stage phase-in: domestic by Feb 2027, international by 2 Feb 2028) + Art. 88 (authori…](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520) — Res BCB 520/2025 (PLD/FTP obligations on SPSAVs; ≥3 responsible administrators including AML/CFT; GAFI Recs 15-16 alignment); Lei 14.478/2022.
8. [Res BCB 520/2025 — patrimonial segregation (segregação patrimonial)](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520) — Res BCB 520/2025 (patrimonial segregation: client funds in individualised payment/deposit accounts; client virtual assets in segregated wallets; foreign-custodian conditions — hom….
9. [Res BCB 520/2025 — stablecoin definition + asset-curation / listing-policy rules](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520) — Res BCB 520/2025 Art. 2, III (reserve assets of a fiat-referenced token = the fiduciary currency and public debt issued by the same governments); Arts. 64+ (asset curation; algori….
10. [Res BCB 521/2025 (FX reclassification + caps); Res BCB 561/2026 (eFX exclusion); Lei 14.286/2021](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=521) — Res BCB 521/2025 (amends Res 277/278/279 of 31 Dec 2022): virtual-asset services brought into the FX market — international payments/transfers, stablecoin trades, and payment of e….
11. [Res BCB 521/2025 (virtual assets in the FX market); Lei 14.286/2021 (Foreign Exchange Law)](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=521) — Res BCB 521 — per-operation caps (USD 100k SPSAV / USD 500k FX-FI when counterparty not FX-authorised); amends the Res 277/278/279 FX trio, inserting Art. 76-A into Res 277/2022 a….
12. [Resolução Conjunta CMN/BCB nº 14/2025; Res BCB 517/2025 (both 3 Nov 2025) — SPSAV minimum-capital methodology](https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=517) — Resolução Conjunta CMN/BCB nº 14/2025 + Res BCB nº 517/2025 (both 3 Nov 2025): minimum capital R$10,800,000 to R$37,200,000 scaled by the set of activities performed.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
