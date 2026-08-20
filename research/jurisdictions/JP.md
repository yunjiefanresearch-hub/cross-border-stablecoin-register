# JP jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 14
- Legal status: `{"operative": 14}`
- Evidence tier: `{"firm_summary": 4, "mixed": 2, "resolution_text": 8}`
- Source disposition: `{"official": 10, "unavailable": 4}`
- Freshness: `{"stale": 1, "unknown": 13}`
- Review stage: `{"primary_reviewed_second_pending": 1, "unreviewed": 13}`
- Named second reviewer: 0/14

## Official source families

- `laws.e-gov.go.jp` — 10 record(s)

## Institutional and supervisory boundary

### `jp-epi-monetary_sovereignty-001` — `monetary_sovereignty`

There is no aggregate cap. Japan does not prohibit foreign-currency tokens; it admits them through a registered Electronic Payment Instruments Exchange Service Provider (EPIESP) that holds reserves in Japan equal to customers' holdings, provided the foreign issuer does not itself issue, redeem, or solicit to Japanese users. This is an open-but-channelled monetary-sovereignty posture: the currency-of-denomination is not capped, but inbound foreign tokens are routed through a registered domestic intermediary holding local reserves.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `jp-epi-regulatory_authority-001` — `regulatory_authority`

Fiat-referenced, par-redeemable stablecoins are Electronic Payment Instruments under the Payment Services Act. The 2022 amendment took effect 1 June 2023 and created the category; Act No. 66 of 2025 (in force June 2025, with implementing cabinet orders to follow) relaxed the trust-type backing rule. The FSA is the single supervisor of issuers and intermediaries; Local Finance Bureaus administer funds-transfer and intermediary registrations under FSA delegation.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-securities_classification-001` — `securities_classification`

Electronic payment instruments (the stablecoin category) are regulated under the Payment Services Act and are distinct from securities regulated under the Financial Instruments and Exchange Act.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `jp-epi-bank_nonbank_routing-001` — `bank_nonbank_routing`

Issuance runs through a closed trichotomy — banks, funds-transfer service providers, and trust companies — with distribution by registered EPI service providers, so roles are separated by licensed function.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-distribution-001` — `distribution`

Foreign-issued stablecoins may be handled by a registered EPIESP if it sets aside reserves in Japan equal to customers' holdings and the foreign issuer does not itself issue, redeem, or solicit to Japanese users. Intermediation and distribution therefore run through the registered EPIESP channel rather than the foreign issuer directly.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-issuer_pathway-001` — `issuer_pathway`

A closed trichotomy: only (a) banks (deposit-type), (b) registered funds-transfer service providers, and (c) trust companies or trust banks (trust-type) may issue Electronic Payment Instruments. Distribution and intermediation require registration as an Electronic Payment Instruments Exchange Service Provider (EPIESP). The issuer trichotomy is the binding eligibility constraint and the structural hallmark of the regime.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Reserve, safeguarding and redemption

### `jp-epi-capital_requirements-001` — `capital_requirements`

Capital requirements are set by entity type under the Payment Services Act and the FSA framework (banking, funds-transfer, or trust licensing); there is no separate aggregate stablecoin capital cap.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-redemption-001` — `redemption`

Redemption is at par on demand. Funds-transfer-type tokens are subject to a 1,000,000 yen per-transfer cap.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-reserve_backing-001` — `reserve_backing`

Full backing is the baseline; funds-transfer and bank types hold liquid backing. For the trust-type, Act No. 66 of 2025 permits up to fifty percent of issuance value to be held in low-risk short-term assets (Japanese or US government bonds with no more than three months remaining maturity, or terminable time deposits). The bond-eligibility detail was the subject of an FSA consultation that ran until 27 February 2026; final standards were pending at that date.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.


## Cross-border and data conditions

### `jp-epi-cross_border_data-001` — `cross_border_data`

The Act on the Protection of Personal Information (APPI) governs personal data and cross-border handling.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-monetary_sovereignty-001` — `monetary_sovereignty`

There is no aggregate cap. Japan does not prohibit foreign-currency tokens; it admits them through a registered Electronic Payment Instruments Exchange Service Provider (EPIESP) that holds reserves in Japan equal to customers' holdings, provided the foreign issuer does not itself issue, redeem, or solicit to Japanese users. This is an open-but-channelled monetary-sovereignty posture: the currency-of-denomination is not capped, but inbound foreign tokens are routed through a registered domestic intermediary holding local reserves.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## AML, KYC and financial-crime controls

### `jp-epi-aml_kyc-001` — `aml_kyc`

The FATF Travel Rule is operative (2022 amendment). Intermediaries hold a large share of customer crypto-assets in cold storage, segregate user funds via trust, and enter liability-sharing agreements with issuers.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Enforcement and implementation posture

### `jp-epi-disclosure_reporting-001` — `disclosure_reporting`

EPI service providers register with the FSA and are subject to disclosure and reporting obligations, with supervisory coordination available.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-implementation_status-001` — `implementation_status`

Live regime. Milestones: Electronic Payment Instruments regime in force (1 June 2023); USDC admitted via the intermediary channel (March 2025); Act No. 66 of 2025 enacted, relaxing trust-type reserves (June 2025); JPYC Inc. registered as a Type II funds-transfer provider (18 August 2025); JPYC, the first registered yen stablecoin, launched (27 October 2025); a megabank trust-structured stablecoin (MUFG, Mizuho, SMBC via Progmat and Project Pax) targeted by the end of FY2026 (31 March 2027).

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `jp-epi-regulatory_authority-001` — `regulatory_authority`

Fiat-referenced, par-redeemable stablecoins are Electronic Payment Instruments under the Payment Services Act. The 2022 amendment took effect 1 June 2023 and created the category; Act No. 66 of 2025 (in force June 2025, with implementing cabinet orders to follow) relaxed the trust-type backing rule. The FSA is the single supervisor of issuers and intermediaries; Local Finance Bureaus administer funds-transfer and intermediary registrations under FSA delegation.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `jp-epi-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (2022 amendment); FSA AML framework](https://laws.e-gov.go.jp/)<br>AML — FATF travel rule operative; intermediary cold storage / trust segregation / liability-sharing | `unknown`; `unreviewed` |
| `jp-epi-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Payment Services Act (Electronic Payment Instruments regime)<br>Closed issuer trichotomy; distribution via registered EPIESP | `unknown`; `unreviewed` |
| `jp-epi-capital_requirements-001` | `capital_requirements` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [Payment Services Act; FSA framework (by entity type)](https://laws.e-gov.go.jp/)<br>Capital — by entity type (banking / funds-transfer / trust); no separate aggregate cap | `unknown`; `unreviewed` |
| `jp-epi-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Act on the Protection of Personal Information (APPI)<br>Cross-border data — APPI governs personal data and cross-border handling | `unknown`; `unreviewed` |
| `jp-epi-disclosure_reporting-001` | `disclosure_reporting` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Payment Services Act (Electronic Payment Instruments regime)<br>EPIESP registration; disclosure and supervisory reporting | `unknown`; `unreviewed` |
| `jp-epi-distribution-001` | `distribution` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/)<br>Distribution — foreign tokens handled via a registered EPIESP holding JP reserves equal to customer holdings;… | `unknown`; `unreviewed` |
| `jp-epi-implementation_status-001` | `implementation_status` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act commencement + FSA registrations (JPYC; USDC via…](https://laws.e-gov.go.jp/)<br>Timeline — EPI 1 Jun 2023; USDC Mar 2025; Act 66/2025 Jun 2025; JPYC 27 Oct 2025; megabank trust token by FY2… | `unknown`; `unreviewed` |
| `jp-epi-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/)<br>Issuer pathway — closed trichotomy (bank / funds-transfer / trust); intermediation via registered EPIESP | `unknown`; `unreviewed` |
| `jp-epi-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/)<br>Monetary sovereignty — no cap; foreign tokens admitted via registered EPIESP holding JP reserves | `stale`; `primary_reviewed_second_pending` |
| `jp-epi-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/)<br>Yield — holders not remunerated; issuer earns reserve interest | `unknown`; `unreviewed` |
| `jp-epi-redemption-001` | `redemption` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/)<br>Redemption — at par on demand; funds-transfer-type JPY 1,000,000 per-transfer cap | `unknown`; `unreviewed` |
| `jp-epi-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Payment Services Act (Electronic Payment Instruments regime, in force…](https://laws.e-gov.go.jp/)<br>Regulators — FSA single supervisor; Local Finance Bureaus by delegation | `unknown`; `unreviewed` |
| `jp-epi-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [Payment Services Act; Act No. 66 of 2025 (trust-type backing relaxati…](https://laws.e-gov.go.jp/)<br>Reserve/backing — full backing baseline; trust-type up to 50% short-term low-risk assets (Act 66/2025) | `unknown`; `unreviewed` |
| `jp-epi-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Payment Services Act (Electronic Payment Instruments regime); Financi…<br>EPI perimeter under the PSA vs. the FIEA securities perimeter | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `jp-epi-aml_kyc-001`

The FATF Travel Rule is operative (2022 amendment). Intermediaries hold a large share of customer crypto-assets in cold storage, segregate user funds via trust, and enter liability-sharing agreements with issuers.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-bank_nonbank_routing-001`

Issuance runs through a closed trichotomy — banks, funds-transfer service providers, and trust companies — with distribution by registered EPI service providers, so roles are separated by licensed function.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `jp-epi-capital_requirements-001`

Capital requirements are set by entity type under the Payment Services Act and the FSA framework (banking, funds-transfer, or trust licensing); there is no separate aggregate stablecoin capital cap.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-cross_border_data-001`

The Act on the Protection of Personal Information (APPI) governs personal data and cross-border handling.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `jp-epi-disclosure_reporting-001`

EPI service providers register with the FSA and are subject to disclosure and reporting obligations, with supervisory coordination available.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `jp-epi-distribution-001`

Foreign-issued stablecoins may be handled by a registered EPIESP if it sets aside reserves in Japan equal to customers' holdings and the foreign issuer does not itself issue, redeem, or solicit to Japanese users. Intermediation and distribution therefore run through the registered EPIESP channel rather than the foreign issuer directly.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-implementation_status-001`

Live regime. Milestones: Electronic Payment Instruments regime in force (1 June 2023); USDC admitted via the intermediary channel (March 2025); Act No. 66 of 2025 enacted, relaxing trust-type reserves (June 2025); JPYC Inc. registered as a Type II funds-transfer provider (18 August 2025); JPYC, the first registered yen stablecoin, launched (27 October 2025); a megabank trust-structured stablecoin (MUFG, Mizuho, SMBC via Progmat and Project Pax) targeted by the end of FY2026 (31 March 2027).

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-issuer_pathway-001`

A closed trichotomy: only (a) banks (deposit-type), (b) registered funds-transfer service providers, and (c) trust companies or trust banks (trust-type) may issue Electronic Payment Instruments. Distribution and intermediation require registration as an Electronic Payment Instruments Exchange Service Provider (EPIESP). The issuer trichotomy is the binding eligibility constraint and the structural hallmark of the regime.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `jp-foreign-stablecoin-recognition`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-monetary_sovereignty-001`

There is no aggregate cap. Japan does not prohibit foreign-currency tokens; it admits them through a registered Electronic Payment Instruments Exchange Service Provider (EPIESP) that holds reserves in Japan equal to customers' holdings, provided the foreign issuer does not itself issue, redeem, or solicit to Japanese users. This is an open-but-channelled monetary-sovereignty posture: the currency-of-denomination is not capped, but inbound foreign tokens are routed through a registered domestic intermediary holding local reserves.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `jp-foreign-stablecoin-recognition`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-permitted_activity_yield-001`

Holders are not remunerated: Electronic Payment Instruments are payment instruments, and issuer economics come from reserve interest. Whether an intermediary-layer (EPIESP) lending service over an admitted foreign token is issuer-paid yield or a separate intermediary product is an open C3xC5 boundary question at the intermediary level, not a feature of the issuer-layer rule.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-redemption-001`

Redemption is at par on demand. Funds-transfer-type tokens are subject to a 1,000,000 yen per-transfer cap.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-regulatory_authority-001`

Fiat-referenced, par-redeemable stablecoins are Electronic Payment Instruments under the Payment Services Act. The 2022 amendment took effect 1 June 2023 and created the category; Act No. 66 of 2025 (in force June 2025, with implementing cabinet orders to follow) relaxed the trust-type backing rule. The FSA is the single supervisor of issuers and intermediaries; Local Finance Bureaus administer funds-transfer and intermediary registrations under FSA delegation.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2023-06-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-reserve_backing-001`

Full backing is the baseline; funds-transfer and bank types hold liquid backing. For the trust-type, Act No. 66 of 2025 permits up to fifty percent of issuance value to be held in low-risk short-term assets (Japanese or US government bonds with no more than three months remaining maturity, or terminable time deposits). The bond-eligibility detail was the subject of an FSA consultation that ran until 27 February 2026; final standards were pending at that date.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2025-06-01`; event `jp-act66-2025-full-enforcement`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `jp-epi-securities_classification-001`

Electronic payment instruments (the stablecoin category) are regulated under the Payment Services Act and are distinct from securities regulated under the Financial Instruments and Exchange Act.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

## Legal-event relationships

### `jp-act66-2025-full-enforcement` — Japan Act No. 66 of 2025 full enforcement (trust-type reserve relaxation)

- Status: `scheduled`; effective date: `2026-06-01`; trigger kind: `dated-empty-effect`.
- Linked records: `jp-epi-reserve_backing-001`.
- Internal basis: Act No. 66 of 2025 relaxing trust-type reserve rules; refines an already-live EPI regime.

### `jp-foreign-stablecoin-recognition` — Japan recognises equivalent foreign trust-type stablecoins as Electronic Payment Instruments (Cabinet Office Ordinance)

- Status: `in_force`; effective date: `2026-06-01`; trigger kind: `inbound-recognition`.
- Linked records: `jp-epi-monetary_sovereignty-001`, `jp-epi-issuer_pathway-001`.
- Internal basis: Cabinet Office Ordinance effective 1 Jun 2026 recognising foreign trust-type stablecoins judged equivalent to the Japanese regime as electronic payment instruments, admitted through a registered EPIESP; opens an inbound recognition channel whose reach is set by the equivalence criteria.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [Payment Services Act (2022 amendment); FSA AML framework](https://laws.e-gov.go.jp/) — AML — FATF travel rule operative; intermediary cold storage / trust segregation / liability-sharing.
2. [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/) — Distribution — foreign tokens handled via a registered EPIESP holding JP reserves equal to customer holdings; foreign issuer may not issue/redeem/solicit to JP users.
3. [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/) — Issuer pathway — closed trichotomy (bank / funds-transfer / trust); intermediation via registered EPIESP.
4. [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/) — Monetary sovereignty — no cap; foreign tokens admitted via registered EPIESP holding JP reserves.
5. [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/) — Redemption — at par on demand; funds-transfer-type JPY 1,000,000 per-transfer cap.
6. [Payment Services Act (Electronic Payment Instruments regime)](https://laws.e-gov.go.jp/) — Yield — holders not remunerated; issuer earns reserve interest.
7. [Payment Services Act (Electronic Payment Instruments regime, in force 1 Jun 2023) as amended by Act No. 66 of 2025](https://laws.e-gov.go.jp/) — Regulators — FSA single supervisor; Local Finance Bureaus by delegation.
8. [Payment Services Act commencement + FSA registrations (JPYC; USDC via SBI VC Trade)](https://laws.e-gov.go.jp/) — Timeline — EPI 1 Jun 2023; USDC Mar 2025; Act 66/2025 Jun 2025; JPYC 27 Oct 2025; megabank trust token by FY2026.
9. [Payment Services Act; Act No. 66 of 2025 (trust-type backing relaxation)](https://laws.e-gov.go.jp/) — Reserve/backing — full backing baseline; trust-type up to 50% short-term low-risk assets (Act 66/2025).
10. [Payment Services Act; FSA framework (by entity type)](https://laws.e-gov.go.jp/) — Capital — by entity type (banking / funds-transfer / trust); no separate aggregate cap.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
