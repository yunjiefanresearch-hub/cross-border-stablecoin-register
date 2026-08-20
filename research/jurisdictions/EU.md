# EU jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 9
- Legal status: `{"operative": 9}`
- Evidence tier: `{"firm_summary": 6, "resolution_text": 3}`
- Source disposition: `{"official": 4, "unavailable": 5}`
- Freshness: `{"stale": 4, "unknown": 5}`
- Review stage: `{"primary_reviewed_second_pending": 4, "unreviewed": 5}`
- Named second reviewer: 0/9

## Official source families

- `eur-lex.europa.eu` — 4 record(s)

## Institutional and supervisory boundary

### `eu-emt-monetary_sovereignty-001` — `monetary_sovereignty`

For a non-EU-currency EMT, MiCA caps usage as a means of exchange at EUR 200 million per day or 1 million transactions per day (the Article 23 thresholds, applied to significant EMTs via Article 58(3)), measured on a quarterly-average basis. The cap applies only to use as a means of exchange within a single currency area, not to store-of-value use or to trading on crypto-asset venues. A separate reporting obligation triggers at EUR 100 million in issuance value globally. This is the canonical quantitative monetary-sovereignty cap and the clearest instance of Constraint 7.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `eu-emt-regulatory_authority-001` — `regulatory_authority`

The Markets in Crypto-Assets Regulation (MiCA, Reg. (EU) 2023/1114) governs EMTs and ARTs, supervised by the EBA (significant tokens), ESMA, and national competent authorities. MiCA's Article 143(3) transitional grandfathering closes on a staggered national schedule capped at 1 July 2026, the outer limit (the longest window any Member State could grant; ESMA has confirmed no extension). Most Member States set shorter windows and closed earlier, so the deadline binding a given corridor is the earliest among the Member States it touches, not the 1 July 2026 cap. A PSD2/MiCAR interplay question is addressed by the EBA No-Action Letter (10 June 2025).

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `eu-emt-securities_classification-001` — `securities_classification`

E-money tokens and asset-referenced tokens are crypto-assets governed by MiCA and are carved out of the MiFID II financial-instrument (securities) perimeter; they are not treated as transferable securities.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `eu-emt-bank_nonbank_routing-001` — `bank_nonbank_routing`

Because EMT issuers must be credit institutions or e-money institutions, issuance sits inside the bank / e-money prudential framework; reserve assets must be safeguarded and segregated from the issuer's estate.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `eu-emt-issuer_pathway-001` — `issuer_pathway`

Issuance of an e-money token is restricted to entities authorized as credit institutions or electronic money institutions; no other entity may issue. An authorizable private token exists.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Reserve, safeguarding and redemption

### `eu-emt-reserve_backing-001` — `reserve_backing`

MiCA requires EMT reserves to hold at least 60% in bank deposits; ART reserves at least 30% in bank deposits. (Distinct from the US/HK same-currency short-dated-sovereign model.)

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Cross-border and data conditions

### `eu-emt-cross_border_data-001` — `cross_border_data`

Authorization passports across the single market; personal data is governed by the GDPR, which is a data-protection regime rather than a localization barrier to supervisory information-sharing.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `eu-emt-monetary_sovereignty-001` — `monetary_sovereignty`

For a non-EU-currency EMT, MiCA caps usage as a means of exchange at EUR 200 million per day or 1 million transactions per day (the Article 23 thresholds, applied to significant EMTs via Article 58(3)), measured on a quarterly-average basis. The cap applies only to use as a means of exchange within a single currency area, not to store-of-value use or to trading on crypto-asset venues. A separate reporting obligation triggers at EUR 100 million in issuance value globally. This is the canonical quantitative monetary-sovereignty cap and the clearest instance of Constraint 7.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## AML, KYC and financial-crime controls

No dedicated record is present for this theme. The absence is a documented scope gap, not a legal conclusion.

## Enforcement and implementation posture

### `eu-emt-disclosure_reporting-001` — `disclosure_reporting`

Issuers publish a crypto-asset white paper and are subject to ongoing disclosure; issuers of significant EMTs report to and are supervised by the EBA, with ESMA coordination.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `eu-emt-regulatory_authority-001` — `regulatory_authority`

The Markets in Crypto-Assets Regulation (MiCA, Reg. (EU) 2023/1114) governs EMTs and ARTs, supervised by the EBA (significant tokens), ESMA, and national competent authorities. MiCA's Article 143(3) transitional grandfathering closes on a staggered national schedule capped at 1 July 2026, the outer limit (the longest window any Member State could grant; ESMA has confirmed no extension). Most Member States set shorter windows and closed earlier, so the deadline binding a given corridor is the earliest among the Member States it touches, not the 1 July 2026 cap. A PSD2/MiCAR interplay question is addressed by the EBA No-Action Letter (10 June 2025).

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `eu-emt-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MiCA, Regulation (EU) 2023/1114; EMD2 (Directive 2009/110/EC)<br>Issuer prudential status; safeguarding/segregation of reserve assets | `unknown`; `unreviewed` |
| `eu-emt-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MiCA, Regulation (EU) 2023/1114; GDPR (Regulation (EU) 2016/679)<br>Passporting; data protection and cross-border supervisory cooperation | `unknown`; `unreviewed` |
| `eu-emt-disclosure_reporting-001` | `disclosure_reporting` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MiCA, Regulation (EU) 2023/1114<br>White-paper and ongoing disclosure; significant-EMT supervision and reporting | `unknown`; `unreviewed` |
| `eu-emt-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Markets in Crypto-Assets Regulation (MiCA), Regulation (EU) 2023/1114<br>Title IV — EMT issuance restricted to authorized credit institutions or e-money institutions | `unknown`; `unreviewed` |
| `eu-emt-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Regulation (EU) 2023/1114 (MiCA), Art. 58(3) (applying the Art. 23 me…](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng)<br>Art. 58(3) (applying Art. 23 mutatis mutandis to non-EU-currency EMTs) | `stale`; `primary_reviewed_second_pending` |
| `eu-emt-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Regulation (EU) 2023/1114 (MiCA), Article 50](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng)<br>Art. 50 (no interest paid to EMT holders) | `stale`; `primary_reviewed_second_pending` |
| `eu-emt-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Regulation (EU) 2023/1114 (MiCA)](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng)<br>Titles III/IV; EBA/ESMA/NCA supervisory architecture | `stale`; `primary_reviewed_second_pending` |
| `eu-emt-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | [Regulation (EU) 2023/1114 (MiCA), reserve composition provisions](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng)<br>reserve composition set in MiCA + Level-2 RTS; deposit-% pinpoint pending RTS line-read | `stale`; `primary_reviewed_second_pending` |
| `eu-emt-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | MiCA, Regulation (EU) 2023/1114; MiFID II (Directive 2014/65/EU)<br>Scope — EMT/ART as crypto-assets outside the MiFID II financial-instrument definition | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `eu-emt-bank_nonbank_routing-001`

Because EMT issuers must be credit institutions or e-money institutions, issuance sits inside the bank / e-money prudential framework; reserve assets must be safeguarded and segregated from the issuer's estate.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `eu-emt-cross_border_data-001`

Authorization passports across the single market; personal data is governed by the GDPR, which is a data-protection regime rather than a localization barrier to supervisory information-sharing.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `eu-emt-disclosure_reporting-001`

Issuers publish a crypto-asset white paper and are subject to ongoing disclosure; issuers of significant EMTs report to and are supervised by the EBA, with ESMA coordination.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `eu-emt-issuer_pathway-001`

Issuance of an e-money token is restricted to entities authorized as credit institutions or electronic money institutions; no other entity may issue. An authorizable private token exists.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `eu-emt-monetary_sovereignty-001`

For a non-EU-currency EMT, MiCA caps usage as a means of exchange at EUR 200 million per day or 1 million transactions per day (the Article 23 thresholds, applied to significant EMTs via Article 58(3)), measured on a quarterly-average basis. The cap applies only to use as a means of exchange within a single currency area, not to store-of-value use or to trading on crypto-asset venues. A separate reporting obligation triggers at EUR 100 million in issuance value globally. This is the canonical quantitative monetary-sovereignty cap and the clearest instance of Constraint 7.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `eu-emt-permitted_activity_yield-001`

MiCA Article 50 imposes a yield ban on EMT holders: holders may not receive interest. The prohibition attaches to the holding of the token, paralleling the US GENIUS §4(a)(11) structure but expressed as a flat ban rather than a 'solely'-qualified one.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `eu-emt-regulatory_authority-001`

The Markets in Crypto-Assets Regulation (MiCA, Reg. (EU) 2023/1114) governs EMTs and ARTs, supervised by the EBA (significant tokens), ESMA, and national competent authorities. MiCA's Article 143(3) transitional grandfathering closes on a staggered national schedule capped at 1 July 2026, the outer limit (the longest window any Member State could grant; ESMA has confirmed no extension). Most Member States set shorter windows and closed earlier, so the deadline binding a given corridor is the earliest among the Member States it touches, not the 1 July 2026 cap. A PSD2/MiCAR interplay question is addressed by the EBA No-Action Letter (10 June 2025).

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `eu-mica-art143-transitional-expiry`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `eu-emt-reserve_backing-001`

MiCA requires EMT reserves to hold at least 60% in bank deposits; ART reserves at least 30% in bank deposits. (Distinct from the US/HK same-currency short-dated-sovereign model.)

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `eu-emt-securities_classification-001`

E-money tokens and asset-referenced tokens are crypto-assets governed by MiCA and are carved out of the MiFID II financial-instrument (securities) perimeter; they are not treated as transferable securities.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

## Legal-event relationships

### `eu-mica-art143-transitional-expiry` — EU MiCA Article 143(3) transitional grandfathering expiry (national side-doors close; admissible-token set narrows)

- Status: `scheduled`; effective date: `2026-07-01`; trigger kind: `intra-regime-gating`.
- Linked records: `eu-emt-regulatory_authority-001`.
- Internal basis: MiCA Article 143(3) (Reg. (EU) 2023/1114) transitional grandfathering for CASPs providing services under pre-existing national law. eu-emt-regulatory_authority-001 carries the corrected staggered framing; this event carries the dated national schedule structurally so compose()/timeline can reflect it.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [Regulation (EU) 2023/1114 (MiCA)](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng) — Titles III/IV; EBA/ESMA/NCA supervisory architecture.
2. [Regulation (EU) 2023/1114 (MiCA), Art. 58(3) (applying the Art. 23 means-of-exchange thresholds to non-EU-currency EMTs)](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng) — Art. 58(3) (applying Art. 23 mutatis mutandis to non-EU-currency EMTs).
3. [Regulation (EU) 2023/1114 (MiCA), Article 50](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng) — Art. 50 (no interest paid to EMT holders).
4. [Regulation (EU) 2023/1114 (MiCA), reserve composition provisions](https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng) — reserve composition set in MiCA + Level-2 RTS; deposit-% pinpoint pending RTS line-read.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
