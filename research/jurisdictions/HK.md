# HK jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 14
- Legal status: `{"operative": 14}`
- Evidence tier: `{"firm_summary": 5, "resolution_text": 8, "unverified": 1}`
- Source disposition: `{"official": 10, "unavailable": 4}`
- Freshness: `{"stale": 8, "unknown": 6}`
- Review stage: `{"primary_reviewed_second_pending": 8, "unreviewed": 6}`
- Named second reviewer: 0/14

## Official source families

- `www.elegislation.gov.hk` — 10 record(s)

## Institutional and supervisory boundary

### `hk-frs-monetary_sovereignty-001` — `monetary_sovereignty`

Hong Kong does not impose a quantitative non-domestic-currency usage cap of the MiCA Article 23 type, but it draws a sovereignty-adjacent line through distribution: foreign-based issuers of non-HKD-linked FRS may offer to professional investors only, while HKD-referencing stablecoins (including those issued offshore) are pulled fully inside the licensing perimeter. The effect is to privilege the domestic-currency instrument for retail use without a numeric ceiling.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `hk-frs-regulatory_authority-001` — `regulatory_authority`

The Stablecoins Ordinance (Cap. 656), effective 1 August 2025, establishes the HKMA as primary regulator for FRS issuers, supported by HKMA Explanatory Notes (Licensing; Transitional Provisions), the Guideline on Supervision of Licensed Stablecoin Issuers, and the AML/CFT Guideline. The SFC regulates virtual asset trading platforms (VATPs) and Type 1 corporations authorised to offer stablecoins.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `hk-frs-securities_classification-001` — `securities_classification`

Specified (fiat-referenced) stablecoins are regulated by the HKMA under the Stablecoins Ordinance and are not treated as securities or futures under the SFO.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `hk-frs-bank_nonbank_routing-001` — `bank_nonbank_routing`

Issuance requires an HKMA licence open to bank and non-bank applicants; it is a licensing regime rather than a bank-only monopoly.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `hk-frs-distribution-001` — `distribution`

Permitted offerors of FRS in Hong Kong are HKMA-licensed FRS issuers, SFC-licensed VATPs, SFC-licensed Type 1 corporations, and Authorised Institutions. Foreign-based issuers of non-HKD-linked FRS may offer to professional investors only. Unlicensed activity carries HK$5 million fine + 7 years' imprisonment + HK$100,000 per day of continuing offence. Pre-existing-issuer transitional treatment required applications by 31 Oct 2025; the closing-down period began 1 Nov 2025 for non-applicants. The April 2026 cohort contrasts distribution models: HSBC plans direct retail integration via PayMe (3.3m users) and its mobile app from H2 2026; Anchorpoint plans a phased Q2 2026 B2B2C rollout of HKDAP via authorised partners.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `hk-frs-issuer_pathway-001` — `issuer_pathway`

A licence is required for (1) FRS issuers in Hong Kong, (2) issuers outside HK of stablecoins referencing the HK dollar, and (3) entities actively marketing FRS to the HK public. Eligible applicants are companies incorporated in HK under the Companies Ordinance, or authorised institutions (banks / restricted-licence / deposit-taking companies under the Banking Ordinance). Shell entities or mere pre-1-Aug-2025 establishment do not qualify for transitional treatment. The first-licence cohort (10 Apr 2026) was HSBC and Anchorpoint Financial Limited (a Standard Chartered (HK)–HKT–Animoca JV intending HKDAP on a B2B2C model); no PRC-connected entities were licensed.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Reserve, safeguarding and redemption

### `hk-frs-capital_requirements-001` — `capital_requirements`

HK$25 million minimum paid-up share capital (or currency equivalent), with HKMA empowered to require more based on business plan; HK$3 million minimum liquid capital; and excess liquid capital equivalent to at least 12 months of operating expenses. The HK$25m threshold, combined with the HK-incorporation-or-authorised-institution requirement, effectively limits applicants to banks and JV-backed large corporates.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `hk-frs-redemption-001` — `redemption`

Redemption at par value within 1 business day of a valid request. Redemption obligations are a continuing licence condition.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `hk-frs-reserve_backing-001` — `reserve_backing`

100% backing at all times; the market value of reserve assets must equal or exceed the par value of circulating stablecoins, with HKMA expecting overcollateralisation. Acceptable assets: cash, bank deposits (term <= 3 months), government and central-bank securities (residual maturity <= 1 year), and tokenised forms of the foregoing. Reserves must be strictly segregated from the issuer's other assets and protected against creditor claims via statutory trust.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Cross-border and data conditions

### `hk-frs-cross_border_data-001` — `cross_border_data`

Personal data is governed by the Personal Data (Privacy) Ordinance (PDPO). Cross-border data transfer governance under PDPO Section 33 remains pending final commencement. HKMA Supervisory Policy Manual provisions on outsourcing and data hosting apply.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `hk-frs-monetary_sovereignty-001` — `monetary_sovereignty`

Hong Kong does not impose a quantitative non-domestic-currency usage cap of the MiCA Article 23 type, but it draws a sovereignty-adjacent line through distribution: foreign-based issuers of non-HKD-linked FRS may offer to professional investors only, while HKD-referencing stablecoins (including those issued offshore) are pulled fully inside the licensing perimeter. The effect is to privilege the domestic-currency instrument for retail use without a numeric ceiling.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## AML, KYC and financial-crime controls

### `hk-frs-aml_kyc-001` — `aml_kyc`

The HKMA AML/CFT Guideline for licensed stablecoin issuers applies: standard FATF KYC, transaction monitoring, and suspicious-transaction reporting, plus distribution-channel KYC obligations executed via licensed VATPs and SFC Type 1 corporations.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Enforcement and implementation posture

### `hk-frs-disclosure_reporting-001` — `disclosure_reporting`

Licensed issuers must meet disclosure, reserve-attestation and reporting requirements under HKMA supervision, with supervisory coordination available.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `hk-frs-implementation_status-001` — `implementation_status`

Live regime. Key milestones: HKMA discussion paper (Jan 2022); FSTB/HKMA consultation (Dec 2023); conclusions + sandbox (Jul 2024); Ordinance and guidelines effective (1 Aug 2025); Ant/JD applications suspended (18-20 Oct 2025); pre-existing-issuer application deadline (31 Oct 2025); closing-down period begins (1 Nov 2025); transitional operating window ends (31 Jan 2026); first two licences granted (10 Apr 2026, HSBC = FRS02, Anchorpoint = FRS01). Expected: Anchorpoint HKDAP B2B2C launch (Q2 2026); HSBC retail launch via PayMe (H2 2026); HKMA second-cohort licences (Q3 2026).

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `hk-frs-regulatory_authority-001` — `regulatory_authority`

The Stablecoins Ordinance (Cap. 656), effective 1 August 2025, establishes the HKMA as primary regulator for FRS issuers, supported by HKMA Explanatory Notes (Licensing; Transitional Provisions), the Guideline on Supervision of Licensed Stablecoin Issuers, and the AML/CFT Guideline. The SFC regulates virtual asset trading platforms (VATPs) and Type 1 corporations authorised to offer stablecoins.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `hk-frs-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | [HKMA AML/CFT Guideline for licensed stablecoin issuers (under Cap. 65…](https://www.elegislation.gov.hk/hk/cap656)<br>AMLO + Ordinance AML obligations on licensees | `unknown`; `unreviewed` |
| `hk-frs-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Stablecoins Ordinance (Cap. 656)<br>Licensing of issuers (bank and non-bank); not bank-only | `unknown`; `unreviewed` |
| `hk-frs-capital_requirements-001` | `capital_requirements` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), capital requirements](https://www.elegislation.gov.hk/hk/cap656)<br>HK$25m paid-up capital (statutory) | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | [Personal Data (Privacy) Ordinance (PDPO); s.33 (cross-border transfer…](https://www.elegislation.gov.hk/hk/cap656)<br>PDPO (Cap. 486) data obligations; HKMA outsourcing/data guidance | `unknown`; `unreviewed` |
| `hk-frs-disclosure_reporting-001` | `disclosure_reporting` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Stablecoins Ordinance (Cap. 656)<br>Disclosure, reserve attestation and supervisory reporting | `unknown`; `unreviewed` |
| `hk-frs-distribution-001` | `distribution` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), offering / distribution restriction…](https://www.elegislation.gov.hk/hk/cap656)<br>permitted-offeror closed loop; HK$5m / 7-year offence | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-implementation_status-001` | `implementation_status` | `operative` / `in_force_enacted` | `unverified`; `high` uncertainty | Stablecoins Ordinance (Cap. 656) commencement + HKMA licensing actions<br>Timeline Jan 2022 -> Q3 2026; first cohort 10 Apr 2026 | `unknown`; `unreviewed` |
| `hk-frs-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), licensing provisions](https://www.elegislation.gov.hk/hk/cap656)<br>licensable regulated activities; s.8(1) licensing offence | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656) — HKD-referencing perimeter + non-HK…](https://www.elegislation.gov.hk/hk/cap656)<br>offshore HKD-referencing issuance is licensable; non-HKD FRS offering limited | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), Schedule 2, s.15 (Non-interest bear…](https://www.elegislation.gov.hk/hk/cap656)<br>Sch. 2 s.15 (no interest on issued stablecoins) | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-redemption-001` | `redemption` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), redemption requirements](https://www.elegislation.gov.hk/hk/cap656)<br>par redemption within 1 business day | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), in force 1 Aug 2025](https://www.elegislation.gov.hk/hk/cap656)<br>HKMA as the licensing/supervisory authority | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Stablecoins Ordinance (Cap. 656), reserve / backing requirements](https://www.elegislation.gov.hk/hk/cap656)<br>100% backing; same-currency reserve with HKD/USD exception; segregation/trust | `stale`; `primary_reviewed_second_pending` |
| `hk-frs-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Stablecoins Ordinance (Cap. 656); Securities and Futures Ordinance (C…<br>HKMA stablecoin perimeter vs. the SFO securities/futures definitions | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `hk-frs-aml_kyc-001`

The HKMA AML/CFT Guideline for licensed stablecoin issuers applies: standard FATF KYC, transaction monitoring, and suspicious-transaction reporting, plus distribution-channel KYC obligations executed via licensed VATPs and SFC Type 1 corporations.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-bank_nonbank_routing-001`

Issuance requires an HKMA licence open to bank and non-bank applicants; it is a licensing regime rather than a bank-only monopoly.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `hk-frs-capital_requirements-001`

HK$25 million minimum paid-up share capital (or currency equivalent), with HKMA empowered to require more based on business plan; HK$3 million minimum liquid capital; and excess liquid capital equivalent to at least 12 months of operating expenses. The HK$25m threshold, combined with the HK-incorporation-or-authorised-institution requirement, effectively limits applicants to banks and JV-backed large corporates.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-cross_border_data-001`

Personal data is governed by the Personal Data (Privacy) Ordinance (PDPO). Cross-border data transfer governance under PDPO Section 33 remains pending final commencement. HKMA Supervisory Policy Manual provisions on outsourcing and data hosting apply.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-disclosure_reporting-001`

Licensed issuers must meet disclosure, reserve-attestation and reporting requirements under HKMA supervision, with supervisory coordination available.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `hk-frs-distribution-001`

Permitted offerors of FRS in Hong Kong are HKMA-licensed FRS issuers, SFC-licensed VATPs, SFC-licensed Type 1 corporations, and Authorised Institutions. Foreign-based issuers of non-HKD-linked FRS may offer to professional investors only. Unlicensed activity carries HK$5 million fine + 7 years' imprisonment + HK$100,000 per day of continuing offence. Pre-existing-issuer transitional treatment required applications by 31 Oct 2025; the closing-down period began 1 Nov 2025 for non-applicants. The April 2026 cohort contrasts distribution models: HSBC plans direct retail integration via PayMe (3.3m users) and its mobile app from H2 2026; Anchorpoint plans a phased Q2 2026 B2B2C rollout of HKDAP via authorised partners.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-implementation_status-001`

Live regime. Key milestones: HKMA discussion paper (Jan 2022); FSTB/HKMA consultation (Dec 2023); conclusions + sandbox (Jul 2024); Ordinance and guidelines effective (1 Aug 2025); Ant/JD applications suspended (18-20 Oct 2025); pre-existing-issuer application deadline (31 Oct 2025); closing-down period begins (1 Nov 2025); transitional operating window ends (31 Jan 2026); first two licences granted (10 Apr 2026, HSBC = FRS02, Anchorpoint = FRS01). Expected: Anchorpoint HKDAP B2B2C launch (Q2 2026); HSBC retail launch via PayMe (H2 2026); HKMA second-cohort licences (Q3 2026).

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `hk-frs-issuer_pathway-001`

A licence is required for (1) FRS issuers in Hong Kong, (2) issuers outside HK of stablecoins referencing the HK dollar, and (3) entities actively marketing FRS to the HK public. Eligible applicants are companies incorporated in HK under the Companies Ordinance, or authorised institutions (banks / restricted-licence / deposit-taking companies under the Banking Ordinance). Shell entities or mere pre-1-Aug-2025 establishment do not qualify for transitional treatment. The first-licence cohort (10 Apr 2026) was HSBC and Anchorpoint Financial Limited (a Standard Chartered (HK)–HKT–Animoca JV intending HKDAP on a B2B2C model); no PRC-connected entities were licensed.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-monetary_sovereignty-001`

Hong Kong does not impose a quantitative non-domestic-currency usage cap of the MiCA Article 23 type, but it draws a sovereignty-adjacent line through distribution: foreign-based issuers of non-HKD-linked FRS may offer to professional investors only, while HKD-referencing stablecoins (including those issued offshore) are pulled fully inside the licensing perimeter. The effect is to privilege the domestic-currency instrument for retail use without a numeric ceiling.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-permitted_activity_yield-001`

The Stablecoins Ordinance Schedule 2 Section 15 (Non-interest bearing) provides that the licensee must not pay any interest on issued stablecoins. Direct payments from issuer to holder are reached by the prohibition.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-redemption-001`

Redemption at par value within 1 business day of a valid request. Redemption obligations are a continuing licence condition.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-regulatory_authority-001`

The Stablecoins Ordinance (Cap. 656), effective 1 August 2025, establishes the HKMA as primary regulator for FRS issuers, supported by HKMA Explanatory Notes (Licensing; Transitional Provisions), the Guideline on Supervision of Licensed Stablecoin Issuers, and the AML/CFT Guideline. The SFC regulates virtual asset trading platforms (VATPs) and Type 1 corporations authorised to offer stablecoins.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-reserve_backing-001`

100% backing at all times; the market value of reserve assets must equal or exceed the par value of circulating stablecoins, with HKMA expecting overcollateralisation. Acceptable assets: cash, bank deposits (term <= 3 months), government and central-bank securities (residual maturity <= 1 year), and tokenised forms of the foregoing. Reserves must be strictly segregated from the issuer's other assets and protected against creditor claims via statutory trust.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `2025-08-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `hk-frs-securities_classification-001`

Specified (fiat-referenced) stablecoins are regulated by the HKMA under the Stablecoins Ordinance and are not treated as securities or futures under the SFO.

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

1. [HKMA AML/CFT Guideline for licensed stablecoin issuers (under Cap. 656)](https://www.elegislation.gov.hk/hk/cap656) — AMLO + Ordinance AML obligations on licensees.
2. [Personal Data (Privacy) Ordinance (PDPO); s.33 (cross-border transfer, not yet commenced)](https://www.elegislation.gov.hk/hk/cap656) — PDPO (Cap. 486) data obligations; HKMA outsourcing/data guidance.
3. [Stablecoins Ordinance (Cap. 656) — HKD-referencing perimeter + non-HKD FRS professional-investor restriction](https://www.elegislation.gov.hk/hk/cap656) — offshore HKD-referencing issuance is licensable; non-HKD FRS offering limited.
4. [Stablecoins Ordinance (Cap. 656), Schedule 2, s.15 (Non-interest bearing)](https://www.elegislation.gov.hk/hk/cap656) — Sch. 2 s.15 (no interest on issued stablecoins).
5. [Stablecoins Ordinance (Cap. 656), capital requirements](https://www.elegislation.gov.hk/hk/cap656) — HK$25m paid-up capital (statutory).
6. [Stablecoins Ordinance (Cap. 656), in force 1 Aug 2025](https://www.elegislation.gov.hk/hk/cap656) — HKMA as the licensing/supervisory authority.
7. [Stablecoins Ordinance (Cap. 656), licensing provisions](https://www.elegislation.gov.hk/hk/cap656) — licensable regulated activities; s.8(1) licensing offence.
8. [Stablecoins Ordinance (Cap. 656), offering / distribution restrictions and offence provisions](https://www.elegislation.gov.hk/hk/cap656) — permitted-offeror closed loop; HK$5m / 7-year offence.
9. [Stablecoins Ordinance (Cap. 656), redemption requirements](https://www.elegislation.gov.hk/hk/cap656) — par redemption within 1 business day.
10. [Stablecoins Ordinance (Cap. 656), reserve / backing requirements](https://www.elegislation.gov.hk/hk/cap656) — 100% backing; same-currency reserve with HKD/USD exception; segregation/trust.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
