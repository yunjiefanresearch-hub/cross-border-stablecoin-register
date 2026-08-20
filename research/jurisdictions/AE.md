# AE jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 13
- Legal status: `{"operative": 13}`
- Evidence tier: `{"firm_summary": 3, "mixed": 3, "resolution_text": 7}`
- Source disposition: `{"official": 10, "unavailable": 3}`
- Freshness: `{"unknown": 13}`
- Review stage: `{"unreviewed": 13}`
- Named second reviewer: 0/13

## Official source families

- `rulebook.centralbank.ae` — 10 record(s)

## Institutional and supervisory boundary

### `ae-pt-monetary_sovereignty-001` — `monetary_sovereignty`

The CBUAE PTSR imposes a channel restriction grounded in monetary sovereignty: no merchant may accept a virtual asset as payment for goods or services unless it is a Dirham Payment Token from a CBUAE-licensed issuer. Foreign payment tokens may be accepted only to buy virtual assets or derivatives, not for general onshore payments. This is a usage-channel restriction, not an aggregate cap — there is no volume ceiling, but foreign tokens are excluded from the general-payments channel, which is reserved for CBUAE-licensed Dirham Payment Tokens.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-regulatory_authority-001` — `regulatory_authority`

The UAE operates a federal-versus-free-zone split. Onshore, the Central Bank of the UAE (CBUAE) Payment Token Services Regulation (PTSR, Circular 2/2024) governs payment-token issuance and use. The financial free zones run their own fiat-referenced-token regimes: VARA (Dubai, outside the DIFC); the ADGM Financial Services Regulatory Authority (FSRA) under its Fiat-Referenced Token (FRT) framework; and the DIFC's Dubai Financial Services Authority (DFSA) under its Crypto Token rules.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-securities_classification-001` — `securities_classification`

Payment tokens are regulated by the CBUAE as payment instruments under the Payment Token Services Regulation; securities are a separate perimeter under the SCA.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `ae-pt-bank_nonbank_routing-001` — `bank_nonbank_routing`

The CBUAE licenses payment-token issuers; the regime admits bank and non-bank issuers under the payment-token charter rather than a bank-only model.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-distribution-001` — `distribution`

The CBUAE channel restriction is the distribution-side constraint: foreign payment tokens are excluded from the general-payments channel and may be accepted only to buy virtual assets or derivatives. Free-zone issuers cannot issue AED tokens and are carved out of the onshore payment perimeter. There is no aggregate volume cap.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-issuer_pathway-001` — `issuer_pathway`

Onshore, a Dirham Payment Token (DPT) may be issued only by a CBUAE-licensed, UAE-incorporated entity; a Foreign Payment Token (FPT) is a registered foreign issuer's token that may be used only to purchase virtual assets or derivatives, not for general payments. Banks may issue payment tokens through a subsidiary. Free-zone issuers operate under the VARA/FSRA/DFSA frameworks but cannot issue AED tokens — AED issuance is reserved to the CBUAE regime.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Reserve, safeguarding and redemption

### `ae-pt-capital_requirements-001` — `capital_requirements`

Onshore, capital requirements are as specified by the CBUAE PTSR. Free-zone issuers face capital requirements per the relevant VARA/FSRA/DFSA framework. The specific figures differ by perimeter.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-redemption-001` — `redemption`

Onshore (CBUAE): redemption at par, no later than the next business day. ADGM: redemption at par within T+2. Free-zone frameworks specify their own redemption timelines.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-reserve_backing-001` — `reserve_backing`

Onshore: 100% backing, segregated in UAE banks. The bank-subsidiary option requires at least 50% cash plus UAE government bonds / CBUAE monetary bills. Free-zone frameworks impose their own reserve requirements (e.g., the ADGM FRT framework requires high-quality liquid reserves).

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Cross-border and data conditions

### `ae-pt-cross_border_data-001` — `cross_border_data`

The Federal Personal Data Protection Law (PDPL) applies onshore. The DIFC and ADGM have their own data-protection regimes (DIFC Data Protection Law; ADGM Data Protection Regulations). Cross-border data-transfer rules vary by zone.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-monetary_sovereignty-001` — `monetary_sovereignty`

The CBUAE PTSR imposes a channel restriction grounded in monetary sovereignty: no merchant may accept a virtual asset as payment for goods or services unless it is a Dirham Payment Token from a CBUAE-licensed issuer. Foreign payment tokens may be accepted only to buy virtual assets or derivatives, not for general onshore payments. This is a usage-channel restriction, not an aggregate cap — there is no volume ceiling, but foreign tokens are excluded from the general-payments channel, which is reserved for CBUAE-licensed Dirham Payment Tokens.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## AML, KYC and financial-crime controls

### `ae-pt-aml_kyc-001` — `aml_kyc`

Federal AML/CFT law applies across onshore and free zones, the FATF travel rule applies, and each regulator (CBUAE, VARA, FSRA, DFSA) imposes AML/CFT obligations within its perimeter.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.


## Enforcement and implementation posture

### `ae-pt-implementation_status-001` — `implementation_status`

In-force regime. Milestones: CBUAE Payment Token Services Regulation (Circular 2/2024) issued (2024); one-year transition period for existing arrangements (2024-2025); transition period closes and AED tokens (AE Coin, Zand AED) go live, with the DFSA recognising USD tokens (USDC, RLUSD) (2025-2026). Multiple AED tokens and DFSA-recognised USD tokens are now live.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ae-pt-regulatory_authority-001` — `regulatory_authority`

The UAE operates a federal-versus-free-zone split. Onshore, the Central Bank of the UAE (CBUAE) Payment Token Services Regulation (PTSR, Circular 2/2024) governs payment-token issuance and use. The financial free zones run their own fiat-referenced-token regimes: VARA (Dubai, outside the DIFC); the ADGM Financial Services Regulatory Authority (FSRA) under its Fiat-Referenced Token (FRT) framework; and the DIFC's Dubai Financial Services Authority (DFSA) under its Crypto Token rules.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `ae-pt-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [UAE federal AML/CFT law; CBUAE / VARA / FSRA / DFSA AML rules](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>AML — federal AML/CFT + FATF travel rule; per-regulator obligations | `unknown`; `unreviewed` |
| `ae-pt-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | CBUAE Payment Token Services Regulation (2024)<br>Licensing of bank and non-bank payment-token issuers | `unknown`; `unreviewed` |
| `ae-pt-capital_requirements-001` | `capital_requirements` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Capital — per CBUAE PTSR onshore; per free-zone framework | `unknown`; `unreviewed` |
| `ae-pt-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Federal Personal Data Protection Law (PDPL); DIFC Data Protection Law…<br>Cross-border data — PDPL onshore; DIFC/ADGM own regimes; transfer rules vary by zone | `unknown`; `unreviewed` |
| `ae-pt-distribution-001` | `distribution` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE PTSR (Circular 2/2024)](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Distribution — channel restriction; free-zone issuers carved out of onshore perimeter | `unknown`; `unreviewed` |
| `ae-pt-implementation_status-001` | `implementation_status` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE PTSR (Circular 2/2024); DFSA recognition of USD tokens](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Timeline — PTSR 2024; one-year transition closed; AED + DFSA-recognised USD tokens live | `unknown`; `unreviewed` |
| `ae-pt-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Issuer pathways — DPT (CBUAE-licensed); FPT (foreign, VA/derivative-only); bank subsidiary; free-zone cannot… | `unknown`; `unreviewed` |
| `ae-pt-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE Payment Token Services Regulation (Circular 2/2024)](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Channel restriction — merchants may accept only CBUAE-licensed Dirham Payment Tokens for goods/services; fore… | `unknown`; `unreviewed` |
| `ae-pt-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Yield — prohibited onshore; ADGM permits reserve income but bans investment/savings promotion | `unknown`; `unreviewed` |
| `ae-pt-redemption-001` | `redemption` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Redemption — CBUAE par <= next business day; ADGM par within T+2 | `unknown`; `unreviewed` |
| `ae-pt-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE Payment Token Services Regulation (Circular 2/2024); VARA / ADG…](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Regulators — CBUAE onshore; VARA / ADGM-FSRA / DIFC-DFSA free zones | `unknown`; `unreviewed` |
| `ae-pt-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [CBUAE PTSR (Circular 2/2024); ADGM FRT framework](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation)<br>Reserve/backing — 100% segregated in UAE banks; bank-subsidiary >=50% cash + UAE govt bonds/CBUAE bills | `unknown`; `unreviewed` |
| `ae-pt-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | CBUAE Payment Token Services Regulation (2024)<br>Payment-token perimeter (CBUAE) vs. securities (SCA) | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `ae-pt-aml_kyc-001`

Federal AML/CFT law applies across onshore and free zones, the FATF travel rule applies, and each regulator (CBUAE, VARA, FSRA, DFSA) imposes AML/CFT obligations within its perimeter.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-bank_nonbank_routing-001`

The CBUAE licenses payment-token issuers; the regime admits bank and non-bank issuers under the payment-token charter rather than a bank-only model.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `ae-pt-capital_requirements-001`

Onshore, capital requirements are as specified by the CBUAE PTSR. Free-zone issuers face capital requirements per the relevant VARA/FSRA/DFSA framework. The specific figures differ by perimeter.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-cross_border_data-001`

The Federal Personal Data Protection Law (PDPL) applies onshore. The DIFC and ADGM have their own data-protection regimes (DIFC Data Protection Law; ADGM Data Protection Regulations). Cross-border data-transfer rules vary by zone.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `ae-pt-distribution-001`

The CBUAE channel restriction is the distribution-side constraint: foreign payment tokens are excluded from the general-payments channel and may be accepted only to buy virtual assets or derivatives. Free-zone issuers cannot issue AED tokens and are carved out of the onshore payment perimeter. There is no aggregate volume cap.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-implementation_status-001`

In-force regime. Milestones: CBUAE Payment Token Services Regulation (Circular 2/2024) issued (2024); one-year transition period for existing arrangements (2024-2025); transition period closes and AED tokens (AE Coin, Zand AED) go live, with the DFSA recognising USD tokens (USDC, RLUSD) (2025-2026). Multiple AED tokens and DFSA-recognised USD tokens are now live.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-issuer_pathway-001`

Onshore, a Dirham Payment Token (DPT) may be issued only by a CBUAE-licensed, UAE-incorporated entity; a Foreign Payment Token (FPT) is a registered foreign issuer's token that may be used only to purchase virtual assets or derivatives, not for general payments. Banks may issue payment tokens through a subsidiary. Free-zone issuers operate under the VARA/FSRA/DFSA frameworks but cannot issue AED tokens — AED issuance is reserved to the CBUAE regime.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-monetary_sovereignty-001`

The CBUAE PTSR imposes a channel restriction grounded in monetary sovereignty: no merchant may accept a virtual asset as payment for goods or services unless it is a Dirham Payment Token from a CBUAE-licensed issuer. Foreign payment tokens may be accepted only to buy virtual assets or derivatives, not for general onshore payments. This is a usage-channel restriction, not an aggregate cap — there is no volume ceiling, but foreign tokens are excluded from the general-payments channel, which is reserved for CBUAE-licensed Dirham Payment Tokens.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-permitted_activity_yield-001`

Issuer-paid yield is prohibited onshore (CBUAE). ADGM permits the issuer to earn reserve income but bans the promotion of the token as an investment or savings product. The operative line in ADGM is promotion, not the earning of reserve income — an approach that resembles the US 'solely in connection with holding' analysis more than a flat prohibition.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-redemption-001`

Onshore (CBUAE): redemption at par, no later than the next business day. ADGM: redemption at par within T+2. Free-zone frameworks specify their own redemption timelines.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-regulatory_authority-001`

The UAE operates a federal-versus-free-zone split. Onshore, the Central Bank of the UAE (CBUAE) Payment Token Services Regulation (PTSR, Circular 2/2024) governs payment-token issuance and use. The financial free zones run their own fiat-referenced-token regimes: VARA (Dubai, outside the DIFC); the ADGM Financial Services Regulatory Authority (FSRA) under its Fiat-Referenced Token (FRT) framework; and the DIFC's Dubai Financial Services Authority (DFSA) under its Crypto Token rules.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-reserve_backing-001`

Onshore: 100% backing, segregated in UAE banks. The bank-subsidiary option requires at least 50% cash plus UAE government bonds / CBUAE monetary bills. Free-zone frameworks impose their own reserve requirements (e.g., the ADGM FRT framework requires high-quality liquid reserves).

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ae-pt-securities_classification-001`

Payment tokens are regulated by the CBUAE as payment instruments under the Payment Token Services Regulation; securities are a separate perimeter under the SCA.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

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

1. [CBUAE PTSR (Circular 2/2024)](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Distribution — channel restriction; free-zone issuers carved out of onshore perimeter.
2. [CBUAE PTSR (Circular 2/2024); ADGM FRT framework](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Reserve/backing — 100% segregated in UAE banks; bank-subsidiary >=50% cash + UAE govt bonds/CBUAE bills.
3. [CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Redemption — CBUAE par <= next business day; ADGM par within T+2.
4. [CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Yield — prohibited onshore; ADGM permits reserve income but bans investment/savings promotion.
5. [CBUAE PTSR (Circular 2/2024); DFSA recognition of USD tokens](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Timeline — PTSR 2024; one-year transition closed; AED + DFSA-recognised USD tokens live.
6. [CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Capital — per CBUAE PTSR onshore; per free-zone framework.
7. [CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Issuer pathways — DPT (CBUAE-licensed); FPT (foreign, VA/derivative-only); bank subsidiary; free-zone cannot issue AED.
8. [CBUAE Payment Token Services Regulation (Circular 2/2024)](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Channel restriction — merchants may accept only CBUAE-licensed Dirham Payment Tokens for goods/services; foreign tokens VA/derivative-only.
9. [CBUAE Payment Token Services Regulation (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — Regulators — CBUAE onshore; VARA / ADGM-FSRA / DIFC-DFSA free zones.
10. [UAE federal AML/CFT law; CBUAE / VARA / FSRA / DFSA AML rules](https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation) — AML — federal AML/CFT + FATF travel rule; per-regulator obligations.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
