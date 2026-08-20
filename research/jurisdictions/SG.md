# SG jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 13
- Legal status: `{"finalized_policy_pending": 9, "operative": 4}`
- Evidence tier: `{"firm_summary": 10, "unverified": 3}`
- Source disposition: `{"official": 7, "unavailable": 6}`
- Freshness: `{"stale": 7, "unknown": 6}`
- Review stage: `{"primary_reviewed_second_pending": 9, "unreviewed": 4}`
- Named second reviewer: 0/13

## Official source families

- `www.mas.gov.sg` — 7 record(s)

## Institutional and supervisory boundary

### `sg-scs-monetary_sovereignty-001` — `monetary_sovereignty`

There is no aggregate usage cap; foreign-currency-pegged tokens simply are not 'MAS-regulated stablecoins' and circulate as ordinary digital payment tokens, leaving market access open at the monetary-sovereignty layer.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `sg-scs-regulatory_authority-001` — `regulatory_authority`

The MAS Single-Currency Stablecoin (SCS) framework, finalised August 2023, sits alongside the Payment Services Act 2019; a separate Digital Token Service Provider (DTSP) licensing regime operates under FSMA Part 9. MAS is the sole regulator.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `primary_reviewed_second_pending`.

### `sg-scs-securities_classification-001` — `securities_classification`

Token classification follows MAS's substance-over-form test: a token with capital-markets-product characteristics is regulated under the Securities and Futures Act (SFA), not the Payment Services Act, and falls outside the SCS framework entirely. Tokens marketed as offering yield or as investments would likely be classified as securities under the SFA. The destination-product classification analysis governs whether a routing architecture that converts SCS holdings into SFA-regulated capital-markets-product shares is permissible.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Authorisation and licensing perimeter

### `sg-scs-bank_nonbank_routing-001` — `bank_nonbank_routing`

MAS-regulated single-currency stablecoins are issued by banks or by major payment institutions under the Payment Services Act; reserve assets are held in segregation for the benefit of holders.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `sg-scs-distribution-001` — `distribution`

The 'MAS-regulated stablecoin' label is restricted to SCS-framework-compliant issuers; misrepresenting a token as MAS-regulated carries financial penalties or imprisonment and placement on the MAS Investor Alert List. Retail consumer protections prohibit high-risk activities such as lending or staking using stablecoins, and foreign-issued stablecoins remain DPTs under the general regime.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `sg-scs-issuer_pathway-001` — `issuer_pathway`

The MAS Single-Currency Stablecoin (SCS) framework applies only to stablecoins pegged to the Singapore Dollar or any G10 currency and issued in Singapore; tokens pegged to other assets or issued offshore stay under the general Digital Payment Token regime and may not use the 'MAS-regulated stablecoin' label. Non-bank SCS issuers with circulation above S$5 million must hold a Major Payment Institution (MPI) licence; those below are exempt from the framework but cannot use the label. Banks are exempt from the PSA licence requirement and may issue under their banking framework. Issuers must be incorporated in Singapore.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Reserve, safeguarding and redemption

### `sg-scs-capital_requirements-001` — `capital_requirements`

An SCS issuer must hold base capital of at least S$1 million or 50% of annual operating expenses, whichever is higher, plus liquid assets sufficient for an orderly wind-down. DTSP licensees (where granted) face a separate S$250,000 base-capital requirement, a S$10,000 annual licence fee, a Singapore-based compliance officer, and annual penetration testing.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `sg-scs-redemption-001` — `redemption`

SCS holders are entitled to redemption at par value within 5 business days of a valid request, with no unreasonable fees or conditions, and customer assets are held under a statutory trust.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `sg-scs-reserve_backing-001` — `reserve_backing`

SCS reserves must be 100% backed in cash, cash equivalents, or short-term sovereign debt securities denominated in the pegged currency, valued at daily mark-to-market, segregated from the issuer's own assets, and held with MAS-approved custodians. Reserves are subject to monthly independent attestation and annual external audit, with audit reports publicly disclosed.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Cross-border and data conditions

### `sg-scs-cross_border_data-001` — `cross_border_data`

Cross-border personal-data transfer is governed by the Personal Data Protection Act 2012 (PDPA), which requires reasonable safeguards — consent, contract, certification, or transfer to a jurisdiction with comparable protection. MAS Outsourcing Guidelines and Technology Risk Management Guidelines apply to data hosting.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `sg-scs-monetary_sovereignty-001` — `monetary_sovereignty`

There is no aggregate usage cap; foreign-currency-pegged tokens simply are not 'MAS-regulated stablecoins' and circulate as ordinary digital payment tokens, leaving market access open at the monetary-sovereignty layer.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## AML, KYC and financial-crime controls

### `sg-scs-aml_kyc-001` — `aml_kyc`

AML/CFT obligations apply under MAS Notice PSN02 (payment services) and Notice PSN03 (digital payment tokens), including the FATF travel rule for digital-payment-token transfers, FATF-aligned KYC, transaction monitoring, and suspicious-transaction reporting.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `primary_reviewed_second_pending`.


## Enforcement and implementation posture

### `sg-scs-implementation_status-001` — `implementation_status`

The Payment Services Act came into force in January 2020; the SCS framework was finalised on 15 August 2023; the FSMA Part 9 DTSP regime took effect 30 June 2025 with no transitional arrangement; full SCS-framework implementation is targeted for mid-2026.

- Institutional/legal state: `finalized_policy_pending` / `finalized_policy_pending`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `sg-scs-regulatory_authority-001` — `regulatory_authority`

The MAS Single-Currency Stablecoin (SCS) framework, finalised August 2023, sits alongside the Payment Services Act 2019; a separate Digital Token Service Provider (DTSP) licensing regime operates under FSMA Part 9. MAS is the sole regulator.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `primary_reviewed_second_pending`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `sg-scs-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MAS Notice PSN02; MAS Notice PSN03<br>PS Act 2019 DPT licensing; MAS Notices PSN02/PSN03 (AML/CFT, travel rule) | `unknown`; `primary_reviewed_second_pending` |
| `sg-scs-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MAS Stablecoin Regulatory Framework; Payment Services Act 2019<br>Eligible issuers (banks / major payment institutions); reserve segregation | `unknown`; `unreviewed` |
| `sg-scs-capital_requirements-001` | `capital_requirements` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023); FS…](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: base capital and liquid-asset requirements | `stale`; `primary_reviewed_second_pending` |
| `sg-scs-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `unverified`; `high` uncertainty | Personal Data Protection Act 2012 (PDPA); MAS Outsourcing and Technol…<br>PDPA cross-border transfer safeguards; MAS data-hosting guidelines | `unknown`; `unreviewed` |
| `sg-scs-distribution-001` | `distribution` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [Payment Services Act 2019 / MAS Single-Currency Stablecoin Regulatory…](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: label/disclosure on distribution | `stale`; `primary_reviewed_second_pending` |
| `sg-scs-implementation_status-001` | `implementation_status` | `finalized_policy_pending` / `finalized_policy_pending` | `unverified`; `high` uncertainty | Payment Services Act 2019; MAS SCS framework; FSMA Part 9<br>Implementation timeline — PSA 2020; SCS Aug 2023; DTSP Jun 2025; full SCS mid-2026 | `unknown`; `unreviewed` |
| `sg-scs-issuer_pathway-001` | `issuer_pathway` | `finalized_policy_pending` / `finalized_policy_pending` | `unverified`; `high` uncertainty | Payment Services Act 2019 (PSA, amended 2022); MAS Single-Currency St…<br>SCS framework — peg scope (SGD/G10, Singapore-issued); MPI licence > S$5m; Singapore incorporation | `unknown`; `unreviewed` |
| `sg-scs-monetary_sovereignty-001` | `monetary_sovereignty` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [MAS Stablecoin Regulatory Framework; Payment Services Act 2019](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: SGD/G10 label scope; foreign-pegged tokens treated as ordinary DPTs | `stale`; `primary_reviewed_second_pending` |
| `sg-scs-permitted_activity_yield-001` | `permitted_activity_yield` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [MAS Single-Currency Stablecoin framework (Aug 2023) — issuer activity…](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: no lending/staking by SCS issuers; SGD/G10 label scope | `stale`; `primary_reviewed_second_pending` |
| `sg-scs-redemption-001` | `redemption` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023)](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: redemption at par within 5 business days | `stale`; `primary_reviewed_second_pending` |
| `sg-scs-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MAS Single-Currency Stablecoin framework (Aug 2023); Payment Services…<br>MAS authority under the Payment Services Act 2019 | `unknown`; `primary_reviewed_second_pending` |
| `sg-scs-reserve_backing-001` | `reserve_backing` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023)](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: 100% reserve in low-risk assets | `stale`; `primary_reviewed_second_pending` |
| `sg-scs-securities_classification-001` | `securities_classification` | `finalized_policy_pending` / `finalized_policy_pending` | `firm_summary`; `high` uncertainty | [Securities and Futures Act (SFA); MAS substance-over-form classificat…](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework)<br>SCS framework: 'MAS-regulated stablecoin' label vs DPT classification | `stale`; `primary_reviewed_second_pending` |

## Record-level propositions and unresolved work

### `sg-scs-aml_kyc-001`

AML/CFT obligations apply under MAS Notice PSN02 (payment services) and Notice PSN03 (digital payment tokens), including the FATF travel rule for digital-payment-token transfers, FATF-aligned KYC, transaction monitoring, and suspicious-transaction reporting.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `sg-scs-bank_nonbank_routing-001`

MAS-regulated single-currency stablecoins are issued by banks or by major payment institutions under the Payment Services Act; reserve assets are held in segregation for the benefit of holders.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `sg-scs-capital_requirements-001`

An SCS issuer must hold base capital of at least S$1 million or 50% of annual operating expenses, whichever is higher, plus liquid assets sufficient for an orderly wind-down. DTSP licensees (where granted) face a separate S$250,000 base-capital requirement, a S$10,000 annual licence fee, a Singapore-based compliance officer, and annual penetration testing.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `2023-08-15`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `sg-scs-cross_border_data-001`

Cross-border personal-data transfer is governed by the Personal Data Protection Act 2012 (PDPA), which requires reasonable safeguards — consent, contract, certification, or transfer to a jurisdiction with comparable protection. MAS Outsourcing Guidelines and Technology Risk Management Guidelines apply to data hosting.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `sg-scs-distribution-001`

The 'MAS-regulated stablecoin' label is restricted to SCS-framework-compliant issuers; misrepresenting a token as MAS-regulated carries financial penalties or imprisonment and placement on the MAS Investor Alert List. Retail consumer protections prohibit high-risk activities such as lending or staking using stablecoins, and foreign-issued stablecoins remain DPTs under the general regime.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `None`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `sg-scs-implementation_status-001`

The Payment Services Act came into force in January 2020; the SCS framework was finalised on 15 August 2023; the FSMA Part 9 DTSP regime took effect 30 June 2025 with no transitional arrangement; full SCS-framework implementation is targeted for mid-2026.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `finalized_policy_pending`; effective from `2023-08-15`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `sg-scs-issuer_pathway-001`

The MAS Single-Currency Stablecoin (SCS) framework applies only to stablecoins pegged to the Singapore Dollar or any G10 currency and issued in Singapore; tokens pegged to other assets or issued offshore stay under the general Digital Payment Token regime and may not use the 'MAS-regulated stablecoin' label. Non-bank SCS issuers with circulation above S$5 million must hold a Major Payment Institution (MPI) licence; those below are exempt from the framework but cannot use the label. Banks are exempt from the PSA licence requirement and may issue under their banking framework. Issuers must be incorporated in Singapore.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `finalized_policy_pending`; effective from `2023-08-15`; event `sg-scs-legislation-enacted`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `sg-scs-monetary_sovereignty-001`

There is no aggregate usage cap; foreign-currency-pegged tokens simply are not 'MAS-regulated stablecoins' and circulate as ordinary digital payment tokens, leaving market access open at the monetary-sovereignty layer.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `None`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `sg-scs-permitted_activity_yield-001`

Yield is not directly prohibited, but the MAS-regulated SCS label is restricted to SGD or G10-pegged tokens issued from Singapore-incorporated entities, and SCS issuers are forbidden from engaging in lending or staking. The activity prohibition (no lend/stake) is the operative yield-adjacent constraint rather than a flat interest ban.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `None`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `sg-scs-redemption-001`

SCS holders are entitled to redemption at par value within 5 business days of a valid request, with no unreasonable fees or conditions, and customer assets are held under a statutory trust.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `2023-08-15`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `sg-scs-regulatory_authority-001`

The MAS Single-Currency Stablecoin (SCS) framework, finalised August 2023, sits alongside the Payment Services Act 2019; a separate Digital Token Service Provider (DTSP) licensing regime operates under FSMA Part 9. MAS is the sole regulator.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `sg-scs-reserve_backing-001`

SCS reserves must be 100% backed in cash, cash equivalents, or short-term sovereign debt securities denominated in the pegged currency, valued at daily mark-to-market, segregated from the issuer's own assets, and held with MAS-approved custodians. Reserves are subject to monthly independent attestation and annual external audit, with audit reports publicly disclosed.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `2023-08-15`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `sg-scs-securities_classification-001`

Token classification follows MAS's substance-over-form test: a token with capital-markets-product characteristics is regulated under the Securities and Futures Act (SFA), not the Payment Services Act, and falls outside the SCS framework entirely. Tokens marketed as offering yield or as investments would likely be classified as securities under the SFA. The destination-product classification analysis governs whether a routing architecture that converts SCS holdings into SFA-regulated capital-markets-product shares is permissible.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `finalized_policy_pending`; effective from `None`; event `sg-scs-legislation-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

## Legal-event relationships

### `sg-scs-legislation-enacted` — Singapore SCS framework implementing legislation enacted (MAS-regulated stablecoin regime live)

- Status: `contingent`; effective date: `None`; trigger kind: `contingent-not-class-change`.
- Linked records: `sg-scs-reserve_backing-001`, `sg-scs-redemption-001`, `sg-scs-permitted_activity_yield-001`, `sg-scs-securities_classification-001`, `sg-scs-capital_requirements-001`, `sg-scs-distribution-001`, `sg-scs-monetary_sovereignty-001`, `sg-scs-issuer_pathway-001`.
- Internal basis: The PS Act 2019 DPT baseline is already in force. The SCS-specific framework is finalised MAS policy pending implementing legislation; the sg-scs-* requirement cells carry it as binding_status=finalized_policy_pending, status=transitional.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023)](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: 100% reserve in low-risk assets.
2. [MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023)](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: redemption at par within 5 business days.
3. [MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023); FSMA Part 9 (DTSP)](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: base capital and liquid-asset requirements.
4. [MAS Single-Currency Stablecoin framework (Aug 2023) — issuer activity restrictions](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: no lending/staking by SCS issuers; SGD/G10 label scope.
5. [MAS Stablecoin Regulatory Framework; Payment Services Act 2019](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: SGD/G10 label scope; foreign-pegged tokens treated as ordinary DPTs.
6. [Payment Services Act 2019 / MAS Single-Currency Stablecoin Regulatory Framework](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: label/disclosure on distribution.
7. [Securities and Futures Act (SFA); MAS substance-over-form classification](https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework) — SCS framework: 'MAS-regulated stablecoin' label vs DPT classification.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
