# UK jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 14
- Legal status: `{"consultation": 1, "enacted_not_commenced": 11, "operative": 1, "proposed": 1}`
- Evidence tier: `{"firm_summary": 5, "unverified": 9}`
- Source disposition: `{"official": 9, "unavailable": 5}`
- Freshness: `{"stale": 2, "unknown": 12}`
- Review stage: `{"primary_reviewed_second_pending": 2, "unreviewed": 12}`
- Named second reviewer: 0/14

## Official source families

- `www.bankofengland.co.uk` — 1 record(s)
- `www.fca.org.uk` — 2 record(s)
- `www.legislation.gov.uk` — 6 record(s)

## Institutional and supervisory boundary

### `uk-frs-monetary_sovereignty-001` — `monetary_sovereignty`

There is no aggregate usage cap on private tokens; the inbound treatment of foreign tokens is in transition pending the operation of the systemic regime, so the structural monetary-sovereignty pole is not yet stable.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-regulatory_authority-001` — `regulatory_authority`

The Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102, in force from February 2026, make issuing a qualifying stablecoin in the UK a regulated activity under FSMA. The FCA (conduct), Bank of England (systemic), and HM Treasury (perimeter) share authority. The FCA published PS26/10 final issuance rules in June 2026; the Bank's June 2026 systemic policy includes a draft Code of Practice, and the authorities published their joint approach on 30 June 2026. The relevant regime commences 25 October 2027.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `uk-frs-securities_classification-001` — `securities_classification`

Regulated stablecoins are brought within the FSMA financial-services perimeter as a payments-adjacent regulated activity rather than as transferable securities under the RAO's investment heads.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `uk-frs-bank_nonbank_routing-001` — `bank_nonbank_routing`

Issuance is undertaken by FCA-authorized firms; systemic payment stablecoins fall additionally under Bank of England oversight, separating conduct authorization from systemic prudential supervision.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-distribution-001` — `distribution`

Offshore firms 'involved' in a sale of a cryptoasset to a UK consumer are within territorial scope. UKQS transactions (in UKQS only) are carved out from the financial-promotions regime, except for lending and borrowing arrangements. HM Treasury's 21 April 2026 draft amendment SI signals intent to bring stablecoin payments using UKQS-authorised firms into regulated payment services (consultation closed 22 May 2026).

- Institutional/legal state: `proposed` / `pending_proposal`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-issuer_pathway-001` — `issuer_pathway`

Issuers must be UK-incorporated. HM Treasury's policy note describes the regulated perimeter as triggered by any one of three lifecycle limbs (offering, redemption, backing-asset management) in the UK. However, Article 9M(2) of SI 2026/102, together with the corresponding amendment to FSMA s.418, requires all three limbs to be in the UK. This single-limb vs. all-three-limbs divergence is an open interpretive question.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Reserve, safeguarding and redemption

### `uk-frs-capital_requirements-001` — `capital_requirements`

The FCA published final rules for non-systemic UK-issued qualifying stablecoins in PS26/10 in June 2026. The Bank of England separately published a June 2026 systemic-stablecoin policy statement with a draft Code of Practice. Exact prudential obligations, systemic/non-systemic allocation and commencement still require record-level primary and independent legal review.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-redemption-001` — `redemption`

Redemption follows an issuer-controlled process within a backing-asset trust structure: third parties holding backing assets do so on trust for the benefit of stablecoin holders. Specific redemption mechanics are pending final FCA rules.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-reserve_backing-001` — `reserve_backing`

SI 2026/102 requires 1:1 backing by a backing-asset pool with annual independent review. Backing assets are carved out from the collective-investment-scheme (CIS) and alternative-investment-fund (AIF) definitions, with the carve-out activated early ahead of full regime commencement; specific backing-asset composition rules are pending final FCA rules.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Cross-border and data conditions

### `uk-frs-cross_border_data-001` — `cross_border_data`

UK GDPR applies (effectively mirroring EU GDPR post-Brexit). Cross-border data transfers to non-UK jurisdictions require an adequacy decision, an International Data Transfer Agreement (IDTA), or the UK Addendum to the EU Standard Contractual Clauses.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-monetary_sovereignty-001` — `monetary_sovereignty`

There is no aggregate usage cap on private tokens; the inbound treatment of foreign tokens is in transition pending the operation of the systemic regime, so the structural monetary-sovereignty pole is not yet stable.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## AML, KYC and financial-crime controls

### `uk-frs-aml_kyc-001` — `aml_kyc`

The cryptoassets regime supersedes the previous Money Laundering Regulations registration regime by bringing cryptoasset activities into full FSMA scope, including AML/KYC obligations; the existing Money Laundering Regulations 2017 continue to apply alongside.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Enforcement and implementation posture

### `uk-frs-implementation_status-001` — `implementation_status`

SI 2026/102 was made in February 2026 and the relevant issuer regime is scheduled to commence on 25 October 2027. The FCA published final stablecoin-issuance rules in PS26/10 in June 2026. The Bank of England published its systemic-stablecoin policy statement and draft Code of Practice in June 2026, followed by a joint Bank/FCA approach on 30 June 2026. Bank finalisation and record-level commencement mapping remain pending.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `uk-frs-regulatory_authority-001` — `regulatory_authority`

The Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102, in force from February 2026, make issuing a qualifying stablecoin in the UK a regulated activity under FSMA. The FCA (conduct), Bank of England (systemic), and HM Treasury (perimeter) share authority. The FCA published PS26/10 final issuance rules in June 2026; the Bank's June 2026 systemic policy includes a draft Code of Practice, and the authorities published their joint approach on 30 June 2026. The relevant regime commences 25 October 2027.

- Institutional/legal state: `enacted_not_commenced` / `made_not_commenced`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `uk-frs-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `unverified`; `high` uncertainty | FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; Money Launder…<br>AML/KYC — full FSMA scope; MLR registration regime superseded | `unknown`; `unreviewed` |
| `uk-frs-bank_nonbank_routing-001` | `bank_nonbank_routing` | `enacted_not_commenced` / `made_not_commenced` | `firm_summary`; `high` uncertainty | FSMA 2026 (conduct + systemic regimes); Banking Act 2009 (systemic)<br>Authorized-firm issuance; FCA conduct vs. BoE systemic split | `unknown`; `unreviewed` |
| `uk-frs-capital_requirements-001` | `capital_requirements` | `enacted_not_commenced` / `made_not_commenced` | `unverified`; `high` uncertainty | [FCA PS26/10; Bank of England June 2026 systemic-stablecoin policy sta…](https://www.fca.org.uk/publication/policy/ps26-10.pdf)<br>FCA PS26/10 Summary and Ch. 2-3; exact capital-rule mapping pending | `unknown`; `unreviewed` |
| `uk-frs-cross_border_data-001` | `cross_border_data` | `enacted_not_commenced` / `made_not_commenced` | `unverified`; `high` uncertainty | [UK GDPR (Data Protection Act 2018)](https://www.legislation.gov.uk/uksi/2026/102/contents/made)<br>Cross-border transfer — adequacy / IDTA / UK Addendum to EU SCCs | `unknown`; `unreviewed` |
| `uk-frs-custody-001` | `custody` | `enacted_not_commenced` / `made_not_commenced` | `unverified`; `high` uncertainty | [FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; FCA CP25/14](https://www.legislation.gov.uk/uksi/2026/102/contents/made)<br>Custody — 24-hour rule; safeguarding licence for regulated custodians | `unknown`; `unreviewed` |
| `uk-frs-distribution-001` | `distribution` | `proposed` / `pending_proposal` | `unverified`; `high` uncertainty | FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; HM Treasury d…<br>Distribution — offshore 'involved' test; UKQS financial-promotions carve-out; payments amendment | `unknown`; `unreviewed` |
| `uk-frs-implementation_status-001` | `implementation_status` | `enacted_not_commenced` / `made_not_commenced` | `unverified`; `high` uncertainty | [SI 2026/102; FCA PS26/10; Bank of England June 2026 policy statement/…](https://www.bankofengland.co.uk/paper/2026/boe-and-fcas-approach-to-joint-regulation-of-systemic-stablecoin-issuers)<br>Joint approach, Introduction and Table C; FCA PS26/10 Summary; commencement 25 Oct 2027 | `unknown`; `unreviewed` |
| `uk-frs-issuer_pathway-001` | `issuer_pathway` | `enacted_not_commenced` / `made_not_commenced` | `firm_summary`; `high` uncertainty | [SI 2026/102, Art. 9M(2); FSMA s.418 (as amended); HM Treasury policy…](https://www.legislation.gov.uk/uksi/2026/102/contents/made)<br>reg 9M(2) (issuing a qualifying stablecoin; all three limbs) vs HMT policy note (any one limb) | `stale`; `primary_reviewed_second_pending` |
| `uk-frs-monetary_sovereignty-001` | `monetary_sovereignty` | `enacted_not_commenced` / `made_not_commenced` | `firm_summary`; `high` uncertainty | FSMA 2026; Bank of England systemic stablecoin regime<br>Monetary-sovereignty treatment of foreign tokens — pending systemic-regime operation | `unknown`; `unreviewed` |
| `uk-frs-permitted_activity_yield-001` | `permitted_activity_yield` | `consultation` / `pending_proposal` | `unverified`; `high` uncertainty | [SI 2026/102; FCA PS26/10; Bank of England June 2026 systemic policy/d…](https://www.fca.org.uk/publication/policy/ps26-10.pdf)<br>Holder-yield/remuneration mapping pending; do not infer from reserve remuneration | `unknown`; `unreviewed` |
| `uk-frs-redemption-001` | `redemption` | `enacted_not_commenced` / `made_not_commenced` | `unverified`; `high` uncertainty | [FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102](https://www.legislation.gov.uk/uksi/2026/102/contents/made)<br>Redemption — issuer-controlled; backing-asset trust structure | `unknown`; `unreviewed` |
| `uk-frs-regulatory_authority-001` | `regulatory_authority` | `enacted_not_commenced` / `made_not_commenced` | `firm_summary`; `high` uncertainty | [Financial Services and Markets Act 2000 (Cryptoassets) Regulations 20…](https://www.legislation.gov.uk/uksi/2026/102/contents/made)<br>FCA/BoE supervisory architecture under FSMA 2000 (as amended by SI 2026/102) | `stale`; `primary_reviewed_second_pending` |
| `uk-frs-reserve_backing-001` | `reserve_backing` | `enacted_not_commenced` / `made_not_commenced` | `unverified`; `high` uncertainty | [Financial Services and Markets Act 2000 (Cryptoassets) Regulations 20…](https://www.legislation.gov.uk/uksi/2026/102/contents/made)<br>1:1 backing; CIS/AIF carve-out for backing assets | `unknown`; `unreviewed` |
| `uk-frs-securities_classification-001` | `securities_classification` | `enacted_not_commenced` / `made_not_commenced` | `firm_summary`; `high` uncertainty | Financial Services and Markets Act 2000 (Regulated Activities) Order;…<br>Regulated-activity perimeter for stablecoins vs. the investment (securities) heads | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `uk-frs-aml_kyc-001`

The cryptoassets regime supersedes the previous Money Laundering Regulations registration regime by bringing cryptoasset activities into full FSMA scope, including AML/KYC obligations; the existing Money Laundering Regulations 2017 continue to apply alongside.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `2026-02-01`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `uk-frs-bank_nonbank_routing-001`

Issuance is undertaken by FCA-authorized firms; systemic payment stablecoins fall additionally under Bank of England oversight, separating conduct authorization from systemic prudential supervision.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `enacted_not_commenced`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `uk-frs-capital_requirements-001`

The FCA published final rules for non-systemic UK-issued qualifying stablecoins in PS26/10 in June 2026. The Bank of England separately published a June 2026 systemic-stablecoin policy statement with a draft Code of Practice. Exact prudential obligations, systemic/non-systemic allocation and commencement still require record-level primary and independent legal review.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `enacted_not_commenced`; effective from `2027-10-25`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-cross_border_data-001`

UK GDPR applies (effectively mirroring EU GDPR post-Brexit). Cross-border data transfers to non-UK jurisdictions require an adequacy decision, an International Data Transfer Agreement (IDTA), or the UK Addendum to the EU Standard Contractual Clauses.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `enacted_not_commenced`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-custody-001`

Any firm holding client crypto-assets for more than 24 hours, or with the ability to override client authority, is a regulated custodian requiring a safeguarding licence. This 24-hour custody rule has significant operational implications for wallet operators with UK user exposure.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `enacted_not_commenced`; effective from `2026-02-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-distribution-001`

Offshore firms 'involved' in a sale of a cryptoasset to a UK consumer are within territorial scope. UKQS transactions (in UKQS only) are carved out from the financial-promotions regime, except for lending and borrowing arrangements. HM Treasury's 21 April 2026 draft amendment SI signals intent to bring stablecoin payments using UKQS-authorised firms into regulated payment services (consultation closed 22 May 2026).

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `proposed`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `uk-frs-implementation_status-001`

SI 2026/102 was made in February 2026 and the relevant issuer regime is scheduled to commence on 25 October 2027. The FCA published final stablecoin-issuance rules in PS26/10 in June 2026. The Bank of England published its systemic-stablecoin policy statement and draft Code of Practice in June 2026, followed by a joint Bank/FCA approach on 30 June 2026. Bank finalisation and record-level commencement mapping remain pending.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `enacted_not_commenced`; effective from `2027-10-25`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-issuer_pathway-001`

Issuers must be UK-incorporated. HM Treasury's policy note describes the regulated perimeter as triggered by any one of three lifecycle limbs (offering, redemption, backing-asset management) in the UK. However, Article 9M(2) of SI 2026/102, together with the corresponding amendment to FSMA s.418, requires all three limbs to be in the UK. This single-limb vs. all-three-limbs divergence is an open interpretive question.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `enacted_not_commenced`; effective from `2026-02-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-monetary_sovereignty-001`

There is no aggregate usage cap on private tokens; the inbound treatment of foreign tokens is in transition pending the operation of the systemic regime, so the structural monetary-sovereignty pole is not yet stable.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `enacted_not_commenced`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `uk-frs-permitted_activity_yield-001`

Yield is not expressly addressed in SI 2026/102. The FCA published PS26/10 final issuance rules in June 2026 and the Bank published its systemic policy/draft Code. The exact holder-yield and remuneration treatment has not yet been mapped and independently reviewed for this record, so no substantive conclusion is promoted.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `consultation`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-redemption-001`

Redemption follows an issuer-controlled process within a backing-asset trust structure: third parties holding backing assets do so on trust for the benefit of stablecoin holders. Specific redemption mechanics are pending final FCA rules.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `enacted_not_commenced`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-regulatory_authority-001`

The Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102, in force from February 2026, make issuing a qualifying stablecoin in the UK a regulated activity under FSMA. The FCA (conduct), Bank of England (systemic), and HM Treasury (perimeter) share authority. The FCA published PS26/10 final issuance rules in June 2026; the Bank's June 2026 systemic policy includes a draft Code of Practice, and the authorities published their joint approach on 30 June 2026. The relevant regime commences 25 October 2027.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `enacted_not_commenced`; effective from `2027-10-25`; event `uk-systemic-regime-operative`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-reserve_backing-001`

SI 2026/102 requires 1:1 backing by a backing-asset pool with annual independent review. Backing assets are carved out from the collective-investment-scheme (CIS) and alternative-investment-fund (AIF) definitions, with the carve-out activated early ahead of full regime commencement; specific backing-asset composition rules are pending final FCA rules.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `enacted_not_commenced`; effective from `2026-02-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `uk-frs-securities_classification-001`

Regulated stablecoins are brought within the FSMA financial-services perimeter as a payments-adjacent regulated activity rather than as transferable securities under the RAO's investment heads.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `enacted_not_commenced`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

## Legal-event relationships

### `uk-systemic-regime-operative` — UK systemic stablecoin regime + FCA conduct regime operative (SI 2026/102 full commencement)

- Status: `scheduled`; effective date: `2027-10-25`; trigger kind: `fully-scheduled`.
- Linked records: `uk-frs-regulatory_authority-001`.
- Internal basis: FSMA 2026 framework via SI 2026/102: made 4 Feb 2026; the BoE systemic-stablecoin regime and FCA conduct regime become operative on full commencement 25 Oct 2027.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [FCA PS26/10; Bank of England June 2026 systemic-stablecoin policy statement and draft Code](https://www.fca.org.uk/publication/policy/ps26-10.pdf) — FCA PS26/10 Summary and Ch. 2-3; exact capital-rule mapping pending.
2. [FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102](https://www.legislation.gov.uk/uksi/2026/102/contents/made) — Redemption — issuer-controlled; backing-asset trust structure.
3. [FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; FCA CP25/14](https://www.legislation.gov.uk/uksi/2026/102/contents/made) — Custody — 24-hour rule; safeguarding licence for regulated custodians.
4. [Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102](https://www.legislation.gov.uk/uksi/2026/102/contents/made) — 1:1 backing; CIS/AIF carve-out for backing assets.
5. [Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102](https://www.legislation.gov.uk/uksi/2026/102/contents/made) — FCA/BoE supervisory architecture under FSMA 2000 (as amended by SI 2026/102).
6. [SI 2026/102, Art. 9M(2); FSMA s.418 (as amended); HM Treasury policy note](https://www.legislation.gov.uk/uksi/2026/102/contents/made) — reg 9M(2) (issuing a qualifying stablecoin; all three limbs) vs HMT policy note (any one limb).
7. [SI 2026/102; FCA PS26/10; Bank of England June 2026 policy statement/draft Code; Bank/FCA joint approach](https://www.bankofengland.co.uk/paper/2026/boe-and-fcas-approach-to-joint-regulation-of-systemic-stablecoin-issuers) — Joint approach, Introduction and Table C; FCA PS26/10 Summary; commencement 25 Oct 2027.
8. [SI 2026/102; FCA PS26/10; Bank of England June 2026 systemic policy/draft Code](https://www.fca.org.uk/publication/policy/ps26-10.pdf) — Holder-yield/remuneration mapping pending; do not infer from reserve remuneration.
9. [UK GDPR (Data Protection Act 2018)](https://www.legislation.gov.uk/uksi/2026/102/contents/made) — Cross-border transfer — adequacy / IDTA / UK Addendum to EU SCCs.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
