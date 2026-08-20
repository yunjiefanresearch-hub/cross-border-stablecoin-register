# CH jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 14
- Legal status: `{"operative": 14}`
- Evidence tier: `{"firm_summary": 3, "mixed": 5, "resolution_text": 6}`
- Source disposition: `{"official": 11, "unavailable": 3}`
- Freshness: `{"unknown": 14}`
- Review stage: `{"unreviewed": 14}`
- Named second reviewer: 0/14

## Official source families

- `www.fedlex.admin.ch` — 5 record(s)
- `www.finma.ch` — 6 record(s)

## Institutional and supervisory boundary

### `ch-frs-monetary_sovereignty-001` — `monetary_sovereignty`

There is no monetary-sovereignty usage cap: foreign-currency stablecoins are not restricted by volume or channel. The practical constraints are the bank-guarantee structure and the AML holder-identification requirement, not distribution caps. Switzerland thus sits at the permissive end of the C7 spectrum, in contrast to the EU's Article 23 quantitative cap, the UAE's onshore channel restriction, and the PRC prohibition.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-regulatory_authority-001` — `regulatory_authority`

Switzerland has no bespoke stablecoin statute: stablecoins are regulated by applying existing financial law — the Banking Act and Banking Ordinance (notably Banking Ordinance Art. 5(3)(f), which removes guaranteed funds from the deposit definition), the DLT Act and the Financial Market Infrastructure Act (FinMIA), the Collective Investment Schemes Act (CISA), and the Anti-Money Laundering Act (AMLA). FINMA Guidance 06/2024 sets out FINMA's supervisory position on stablecoins, including AML treatment and the conditions of the bank-guarantee exemption. FINMA is the primary supervisor; the SNB oversees systemic financial market infrastructures.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-securities_classification-001` — `securities_classification`

If a stablecoin arrangement is structured so that assets are held for the account of holders (rather than as a contractual claim against the issuer), collective-investment-scheme rules under the Collective Investment Schemes Act (CISA) may apply. The operative characterization question is whether holding assets for holders to generate yield converts the arrangement into a CIS — the Swiss analogue to the securities-classification spine.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `ch-frs-bank_nonbank_routing-001` — `bank_nonbank_routing`

Depending on structure, stablecoin issuance may require a banking licence or operate under the DLT framework; the bank/non-bank line turns on whether deposits are accepted and how reserves are held.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-distribution-001` — `distribution`

There is no monetary-sovereignty usage cap and no distribution-volume restriction; foreign-currency stablecoins are not channel-restricted. The bank-guarantee structure and the FINMA holder-identification requirement are the practical distribution constraints, not caps.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-issuer_pathway-001` — `issuer_pathway`

Two issuer pathways. Pathway 1 (licensed institution): an issuer holding a banking licence, or a FinTech licence under Art. 1b of the Banking Act, may issue stablecoins as a licensed institution. Pathway 2 (bank default-guarantee exemption): a non-bank issuer avoids the deposit-taking prohibition by securing a default guarantee (Bankengarantie) from a Swiss bank covering the deposited funds; under Banking Ordinance Art. 5(3)(f) funds covered by such a guarantee are not deposits, so the issuer is not engaged in unauthorized deposit-taking. The entire non-bank issuance market runs through this single textual aperture.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Reserve, safeguarding and redemption

### `ch-frs-capital_requirements-001` — `capital_requirements`

For licensed-institution pathways, capital requirements apply per the Banking Act / FinTech-licence framework. For the bank-guarantee pathway there is no separate stablecoin capital schedule; the guarantee performs the protective function in place of a prescribed capital buffer.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-redemption-001` — `redemption`

Redemption is a payment claim against the issuer (or, on issuer default, against the guaranteeing bank). There is no statutory at-par redemption mandate; the claim is contractual, backed by the guarantee. Stablecoin holders are not deposit-insured — the bank guarantee, not deposit insurance, is the protection.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-reserve_backing-001` — `reserve_backing`

There is no statutory reserve schedule (no mandated asset list or percentages). Under the bank-guarantee pathway the protective mechanism is the guarantee, not a prescribed reserve portfolio: the guarantee must cover the principal plus interest of the deposited funds. If the arrangement is structured so that assets are held for the account of holders (rather than as a claim against the issuer), collective investment scheme (CIS) rules under CISA may apply.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Cross-border and data conditions

### `ch-frs-cross_border_data-001` — `cross_border_data`

The Swiss Federal Act on Data Protection (FADP) applies (revised FADP in force September 2023). Cross-border data transfer requires adequate protection in the recipient state or appropriate safeguards. Switzerland maintains adequacy recognition with the EU.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-monetary_sovereignty-001` — `monetary_sovereignty`

There is no monetary-sovereignty usage cap: foreign-currency stablecoins are not restricted by volume or channel. The practical constraints are the bank-guarantee structure and the AML holder-identification requirement, not distribution caps. Switzerland thus sits at the permissive end of the C7 spectrum, in contrast to the EU's Article 23 quantitative cap, the UAE's onshore channel restriction, and the PRC prohibition.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## AML, KYC and financial-crime controls

### `ch-frs-aml_kyc-001` — `aml_kyc`

FINMA Guidance 06/2024 imposes the strictest AML posture in the survey: the issuer must identify every holder, including intermediate holders, treating each as a customer, and anonymous transfers are prohibited. Full AMLA obligations apply and the FATF travel rule applies.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Enforcement and implementation posture

### `ch-frs-disclosure_reporting-001` — `disclosure_reporting`

FINMA guidance imposes AML, disclosure and reporting expectations on issuers, with supervisory coordination available.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-implementation_status-001` — `implementation_status`

Guidance-in-force regime. Milestones: FINMA Guidance 06/2024 published (Jul 2024); bank-guarantee and licensed-institution pathways in operation (2024-2025); consultation on a Financial Institutions Act (FinIA) amendment creating a dedicated payment-instrument-institution licence to replace the guarantee workaround closed (6 Feb 2026); six-bank CHF stablecoin sandbox launched (8 Apr 2026). If enacted, the FinIA amendment would replace the guarantee workaround with a purpose-built regime.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `mixed` / `medium`.
- Decision-use gate: `unknown` / `unreviewed`.

### `ch-frs-regulatory_authority-001` — `regulatory_authority`

Switzerland has no bespoke stablecoin statute: stablecoins are regulated by applying existing financial law — the Banking Act and Banking Ordinance (notably Banking Ordinance Art. 5(3)(f), which removes guaranteed funds from the deposit definition), the DLT Act and the Financial Market Infrastructure Act (FinMIA), the Collective Investment Schemes Act (CISA), and the Anti-Money Laundering Act (AMLA). FINMA Guidance 06/2024 sets out FINMA's supervisory position on stablecoins, including AML treatment and the conditions of the bank-guarantee exemption. FINMA is the primary supervisor; the SNB oversees systemic financial market infrastructures.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `unknown` / `unreviewed`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `ch-frs-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [FINMA Guidance 06/2024; Anti-Money Laundering Act (AMLA)](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/)<br>AML — identify every holder incl. intermediate holders; anonymous transfers prohibited | `unknown`; `unreviewed` |
| `ch-frs-bank_nonbank_routing-001` | `bank_nonbank_routing` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Banking Act; DLT Act (2021); FINMA stablecoin guidance<br>Banking-licence vs. DLT-framework routing for issuance | `unknown`; `unreviewed` |
| `ch-frs-capital_requirements-001` | `capital_requirements` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [Banking Act / FinTech-licence framework; FINMA Guidance 06/2024](https://www.fedlex.admin.ch/eli/cc/1934/121/de)<br>Capital — per licence for licensed institutions; no separate schedule under the guarantee pathway | `unknown`; `unreviewed` |
| `ch-frs-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | Federal Act on Data Protection (revised FADP, in force Sep 2023)<br>Cross-border transfer — adequacy or safeguards; EU adequacy maintained | `unknown`; `unreviewed` |
| `ch-frs-disclosure_reporting-001` | `disclosure_reporting` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | FINMA stablecoin guidance; AMLA<br>AML, disclosure and supervisory reporting expectations | `unknown`; `unreviewed` |
| `ch-frs-distribution-001` | `distribution` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [FINMA Guidance 06/2024; Banking Act framework](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/)<br>Distribution — no caps/channel restriction; guarantee + holder-ID are the practical limits | `unknown`; `unreviewed` |
| `ch-frs-implementation_status-001` | `implementation_status` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [FINMA Guidance 06/2024; FinIA-amendment consultation (closed 6 Feb 20…](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/)<br>Timeline — guidance Jul 2024; FinIA consultation closed 6 Feb 2026; 6-bank CHF sandbox 8 Apr 2026 | `unknown`; `unreviewed` |
| `ch-frs-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Banking Act Art. 1b (FinTech licence); Banking Ordinance Art. 5(3)(f)…](https://www.fedlex.admin.ch/eli/cc/2014/273/de)<br>Issuer pathways — licensed-institution vs bank-guarantee exemption (BankO Art. 5(3)(f)) | `unknown`; `unreviewed` |
| `ch-frs-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [FINMA Guidance 06/2024 (no usage cap); Banking Act framework](https://www.fedlex.admin.ch/eli/cc/2014/273/de)<br>Monetary sovereignty — no usage cap; foreign-currency tokens unrestricted | `unknown`; `unreviewed` |
| `ch-frs-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [FINMA Guidance 06/2024; Banking Ordinance Art. 5(3)(f)](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/)<br>Yield permitted; bank guarantee must cover interest (structural constraint, not prohibition) | `unknown`; `unreviewed` |
| `ch-frs-redemption-001` | `redemption` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/)<br>Redemption — contractual claim vs issuer / guaranteeing bank; no statutory par mandate; not deposit-insured | `unknown`; `unreviewed` |
| `ch-frs-regulatory_authority-001` | `regulatory_authority` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Banking Act and Banking Ordinance; FINMA Guidance 06/2024 (Stablecoin…](https://www.fedlex.admin.ch/eli/cc/1934/121/de)<br>FINMA as primary stablecoin supervisor; SNB for systemic FMIs; no bespoke statute | `unknown`; `unreviewed` |
| `ch-frs-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024; Collective In…](https://www.fedlex.admin.ch/eli/cc/2014/273/de)<br>Reserve/backing — no statutory schedule; guarantee covers principal + interest; CISA characterization risk | `unknown`; `unreviewed` |
| `ch-frs-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `mixed`; `medium` uncertainty | [Collective Investment Schemes Act (CISA); FINMA Guidance 06/2024](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/)<br>CISA characterization where assets are held for the account of holders | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `ch-frs-aml_kyc-001`

FINMA Guidance 06/2024 imposes the strictest AML posture in the survey: the issuer must identify every holder, including intermediate holders, treating each as a customer, and anonymous transfers are prohibited. Full AMLA obligations apply and the FATF travel rule applies.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-bank_nonbank_routing-001`

Depending on structure, stablecoin issuance may require a banking licence or operate under the DLT framework; the bank/non-bank line turns on whether deposits are accepted and how reserves are held.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `ch-frs-capital_requirements-001`

For licensed-institution pathways, capital requirements apply per the Banking Act / FinTech-licence framework. For the bank-guarantee pathway there is no separate stablecoin capital schedule; the guarantee performs the protective function in place of a prescribed capital buffer.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-cross_border_data-001`

The Swiss Federal Act on Data Protection (FADP) applies (revised FADP in force September 2023). Cross-border data transfer requires adequate protection in the recipient state or appropriate safeguards. Switzerland maintains adequacy recognition with the EU.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `2023-09-01`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `ch-frs-disclosure_reporting-001`

FINMA guidance imposes AML, disclosure and reporting expectations on issuers, with supervisory coordination available.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `ch-frs-distribution-001`

There is no monetary-sovereignty usage cap and no distribution-volume restriction; foreign-currency stablecoins are not channel-restricted. The bank-guarantee structure and the FINMA holder-identification requirement are the practical distribution constraints, not caps.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-implementation_status-001`

Guidance-in-force regime. Milestones: FINMA Guidance 06/2024 published (Jul 2024); bank-guarantee and licensed-institution pathways in operation (2024-2025); consultation on a Financial Institutions Act (FinIA) amendment creating a dedicated payment-instrument-institution licence to replace the guarantee workaround closed (6 Feb 2026); six-bank CHF stablecoin sandbox launched (8 Apr 2026). If enacted, the FinIA amendment would replace the guarantee workaround with a purpose-built regime.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `2024-07-01`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-issuer_pathway-001`

Two issuer pathways. Pathway 1 (licensed institution): an issuer holding a banking licence, or a FinTech licence under Art. 1b of the Banking Act, may issue stablecoins as a licensed institution. Pathway 2 (bank default-guarantee exemption): a non-bank issuer avoids the deposit-taking prohibition by securing a default guarantee (Bankengarantie) from a Swiss bank covering the deposited funds; under Banking Ordinance Art. 5(3)(f) funds covered by such a guarantee are not deposits, so the issuer is not engaged in unauthorized deposit-taking. The entire non-bank issuance market runs through this single textual aperture.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-monetary_sovereignty-001`

There is no monetary-sovereignty usage cap: foreign-currency stablecoins are not restricted by volume or channel. The practical constraints are the bank-guarantee structure and the AML holder-identification requirement, not distribution caps. Switzerland thus sits at the permissive end of the C7 spectrum, in contrast to the EU's Article 23 quantitative cap, the UAE's onshore channel restriction, and the PRC prohibition.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-permitted_activity_yield-001`

Paying yield to holders is NOT prohibited — Switzerland is the clearest survey example of a regime where holder yield is permitted but structurally constrained. Under the bank-guarantee pathway the guarantee must cover any interest earned, so the cost of offering yield is the cost of guaranteeing it; the protective mechanism scales with the yield offered. This contrasts sharply with the prohibition cluster (EU Art. 50; HK Sched. 2 s.15; US GENIUS Act § 4(a)(11)).

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-redemption-001`

Redemption is a payment claim against the issuer (or, on issuer default, against the guaranteeing bank). There is no statutory at-par redemption mandate; the claim is contractual, backed by the guarantee. Stablecoin holders are not deposit-insured — the bank guarantee, not deposit insurance, is the protection.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-regulatory_authority-001`

Switzerland has no bespoke stablecoin statute: stablecoins are regulated by applying existing financial law — the Banking Act and Banking Ordinance (notably Banking Ordinance Art. 5(3)(f), which removes guaranteed funds from the deposit definition), the DLT Act and the Financial Market Infrastructure Act (FinMIA), the Collective Investment Schemes Act (CISA), and the Anti-Money Laundering Act (AMLA). FINMA Guidance 06/2024 sets out FINMA's supervisory position on stablecoins, including AML treatment and the conditions of the bank-guarantee exemption. FINMA is the primary supervisor; the SNB oversees systemic financial market infrastructures.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-reserve_backing-001`

There is no statutory reserve schedule (no mandated asset list or percentages). Under the bank-guarantee pathway the protective mechanism is the guarantee, not a prescribed reserve portfolio: the guarantee must cover the principal plus interest of the deposited funds. If the arrangement is structured so that assets are held for the account of holders (rather than as a claim against the issuer), collective investment scheme (CIS) rules under CISA may apply.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `ch-frs-securities_classification-001`

If a stablecoin arrangement is structured so that assets are held for the account of holders (rather than as a contractual claim against the issuer), collective-investment-scheme rules under the Collective Investment Schemes Act (CISA) may apply. The operative characterization question is whether holding assets for holders to generate yield converts the arrangement into a CIS — the Swiss analogue to the securities-classification spine.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
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

1. [Banking Act / FinTech-licence framework; FINMA Guidance 06/2024](https://www.fedlex.admin.ch/eli/cc/1934/121/de) — Capital — per licence for licensed institutions; no separate schedule under the guarantee pathway.
2. [Banking Act Art. 1b (FinTech licence); Banking Ordinance Art. 5(3)(f) (deposit exclusion); FINMA Guidance 06/2024](https://www.fedlex.admin.ch/eli/cc/2014/273/de) — Issuer pathways — licensed-institution vs bank-guarantee exemption (BankO Art. 5(3)(f)).
3. [Banking Act and Banking Ordinance; FINMA Guidance 06/2024 (Stablecoins)](https://www.fedlex.admin.ch/eli/cc/1934/121/de) — FINMA as primary stablecoin supervisor; SNB for systemic FMIs; no bespoke statute.
4. [Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/) — Redemption — contractual claim vs issuer / guaranteeing bank; no statutory par mandate; not deposit-insured.
5. [Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024; Collective Investment Schemes Act (CISA)](https://www.fedlex.admin.ch/eli/cc/2014/273/de) — Reserve/backing — no statutory schedule; guarantee covers principal + interest; CISA characterization risk.
6. [Collective Investment Schemes Act (CISA); FINMA Guidance 06/2024](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/) — CISA characterization where assets are held for the account of holders.
7. [FINMA Guidance 06/2024 (no usage cap); Banking Act framework](https://www.fedlex.admin.ch/eli/cc/2014/273/de) — Monetary sovereignty — no usage cap; foreign-currency tokens unrestricted.
8. [FINMA Guidance 06/2024; Anti-Money Laundering Act (AMLA)](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/) — AML — identify every holder incl. intermediate holders; anonymous transfers prohibited.
9. [FINMA Guidance 06/2024; Banking Act framework](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/) — Distribution — no caps/channel restriction; guarantee + holder-ID are the practical limits.
10. [FINMA Guidance 06/2024; Banking Ordinance Art. 5(3)(f)](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/) — Yield permitted; bank guarantee must cover interest (structural constraint, not prohibition).
11. [FINMA Guidance 06/2024; FinIA-amendment consultation (closed 6 Feb 2026)](https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/) — Timeline — guidance Jul 2024; FinIA consultation closed 6 Feb 2026; 6-bank CHF sandbox 8 Apr 2026.

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
