# US jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 9
- Legal status: `{"operative": 7, "proposed": 2}`
- Evidence tier: `{"firm_summary": 5, "resolution_text": 4}`
- Source disposition: `{"official": 5, "unavailable": 4}`
- Freshness: `{"stale": 5, "unknown": 4}`
- Review stage: `{"primary_reviewed_second_pending": 6, "unreviewed": 3}`
- Named second reviewer: 0/9

## Official source families

- `www.congress.gov` — 3 record(s)
- `www.federalregister.gov` — 2 record(s)

## Institutional and supervisory boundary

### `us-pss-monetary_sovereignty-001` — `monetary_sovereignty`

The US issues the reserve currency and imposes no aggregate usage cap on private dollar tokens. A foreign payment stablecoin may be offered in the US only where the foreign regime is determined comparable by the Treasury and the issuer registers — an admission-by-determination channel rather than an open market.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `us-pss-securities_classification-001` — `securities_classification`

A payment stablecoin structured to comply with the GENIUS Act (1:1 backing, no issuer yield, par redemption) is positioned as a non-security: under the Reves family-resemblance test the instrument resembles a payment/exchange medium rather than an investment note, and the absence of yield removes the principal Howey 'expectation of profit' hook. The contested boundary is not the stablecoin itself but the adjacent routing step: whether a wallet/intermediary that routes a user's payment-stablecoin balance into 1940-Act registered tokenised money market fund shares is thereby distributing securities and acting as a broker. The author's analysis (Reves' fourth factor — the presence of an alternative regulatory regime) argues registered-fund shares are already comprehensively regulated, weighing against re-characterising the routing as an unregistered securities activity.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Authorisation and licensing perimeter

### `us-pss-bank_nonbank_routing-001` — `bank_nonbank_routing`

The regime separates roles along a routing chain. A bank operating as a Layer 1 issuer under the GENIUS Act operates under bank supervision; non-bank permitted issuers operate under the OCC/FDIC payment-stablecoin charter. CLARITY §404 adds an intermediary layer: 'covered parties' (digital-asset service providers and affiliates) may not pay yield on held balances, but may facilitate user-initiated activity. The author synthesises a generalisable three-layer routing architecture: (1) a compliant issuer layer (GENIUS-compliant payment stablecoin), (2) an authorised routing layer (the wallet/intermediary that executes the user's signed instruction), and (3) a yield-bearing tokenised cash-management layer (registered tokenised MMF). The binding question is which entity in the chain holds which authorisation, and whether the routing layer's action is a permitted facilitation or a prohibited yield/brokerage activity.

- Institutional/legal state: `proposed` / `pending_proposal`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `primary_reviewed_second_pending`.

### `us-pss-issuer_pathway-001` — `issuer_pathway`

Permitted payment stablecoin issuers are a defined set: subsidiaries of insured depository institutions, federally qualified non-bank payment stablecoin issuers approved by the OCC, and state-qualified issuers operating under an OCC-certified comparable state regime. An authorizable private token exists.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Reserve, safeguarding and redemption

### `us-pss-capital_requirements-001` — `capital_requirements`

De novo PPSIs must hold minimum capital of the greater of $5 million or the chartering-condition amount, for 36 months. An operational backstop of 12 months of operating expenses must be held in cash, FDIC-insured deposits, or short-dated Treasuries (<=93 days). Two consecutive quarter-ends below the capital or backstop requirement trigger mandatory liquidation.

- Institutional/legal state: `proposed` / `pending_proposal`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.

### `us-pss-reserve_backing-001` — `reserve_backing`

1:1 backing of outstanding payment stablecoins at fair value is required by the enacted GENIUS Act (Sec. 4(a)(1)). The detailed list of PERMISSIBLE reserve assets is set by the OCC NPRM (proposed 12 CFR Sec. 15.11(b)) and is NOT yet final — that composition is a pending overlay, not part of the in-force statutory proposition.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `resolution_text` / `low`.
- Decision-use gate: `stale` / `primary_reviewed_second_pending`.


## Cross-border and data conditions

### `us-pss-cross_border_data-001` — `cross_border_data`

Issuers are subject to the Bank Secrecy Act and OFAC sanctions administration; there is no data-localization rule that bars supervisory information-sharing with foreign regulators.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `us-pss-monetary_sovereignty-001` — `monetary_sovereignty`

The US issues the reserve currency and imposes no aggregate usage cap on private dollar tokens. A foreign payment stablecoin may be offered in the US only where the foreign regime is determined comparable by the Treasury and the issuer registers — an admission-by-determination channel rather than an open market.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## AML, KYC and financial-crime controls

No dedicated record is present for this theme. The absence is a documented scope gap, not a legal conclusion.

## Enforcement and implementation posture

### `us-pss-disclosure_reporting-001` — `disclosure_reporting`

Issuers must publish monthly reserve composition certified by an independent accountant and are subject to federal and state supervisory reporting; supervisory coordination is available.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `us-pss-bank_nonbank_routing-001` | `bank_nonbank_routing` | `proposed` / `pending_proposal` | `firm_summary`; `high` uncertainty | GENIUS Act (issuer charters); CLARITY Act §404 'covered parties' (pen…<br>CLARITY Act Sec. 404 covered-party definition (H.R.3633, House-passed, not enacted) | `unknown`; `primary_reviewed_second_pending` |
| `us-pss-capital_requirements-001` | `capital_requirements` | `proposed` / `pending_proposal` | `firm_summary`; `high` uncertainty | [GENIUS Act capital provisions; OCC/FDIC NPRM (de novo capital; operat…](https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation)<br>capital left to OCC/FDIC rulemaking; figures from the OCC/FDIC NPRM (proposed) | `stale`; `primary_reviewed_second_pending` |
| `us-pss-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | GENIUS Act; Bank Secrecy Act; OFAC regulations<br>AML/sanctions perimeter; cross-border information-sharing | `unknown`; `unreviewed` |
| `us-pss-disclosure_reporting-001` | `disclosure_reporting` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | GENIUS Act<br>Monthly reserve certification and disclosure; supervisory reporting | `unknown`; `unreviewed` |
| `us-pss-issuer_pathway-001` | `issuer_pathway` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Guiding and Establishing National Innovation for U.S. Stablecoins Act…](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text)<br>GENIUS Act Sec. 3-4 (permitted payment stablecoin issuers: IDI subsidiaries; OCC-qualified non-banks; certifi… | `stale`; `primary_reviewed_second_pending` |
| `us-pss-monetary_sovereignty-001` | `monetary_sovereignty` | `operative` / `in_force_enacted` | `firm_summary`; `high` uncertainty | GENIUS Act<br>Foreign payment stablecoin issuers — comparability determination and registration | `unknown`; `unreviewed` |
| `us-pss-permitted_activity_yield-001` | `permitted_activity_yield` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [GENIUS Act §4(a)(11); OCC NPRM §15.10(c)(4) / anti-evasion §15.10(c)(…](https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation)<br>GENIUS Act Sec. 4(a)(11) (no interest/yield in connection with holding, use, or retention) | `stale`; `primary_reviewed_second_pending` |
| `us-pss-reserve_backing-001` | `reserve_backing` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [GENIUS Act Sec. 4(a)(1) (1:1 fair-value reserve backing)](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text)<br>GENIUS Act Sec. 4(a)(1) (1:1 fair-value backing of outstanding payment stablecoins) | `stale`; `primary_reviewed_second_pending` |
| `us-pss-securities_classification-001` | `securities_classification` | `operative` / `in_force_enacted` | `resolution_text`; `low` uncertainty | [Reves v. Ernst & Young, 494 U.S. 56 (1990); SEC v. W.J. Howey Co., 32…](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text)<br>GENIUS Act securities carve-out (amending the '33/'34 Acts and ICA40 for permitted payment stablecoins) | `stale`; `primary_reviewed_second_pending` |

## Record-level propositions and unresolved work

### `us-pss-bank_nonbank_routing-001`

The regime separates roles along a routing chain. A bank operating as a Layer 1 issuer under the GENIUS Act operates under bank supervision; non-bank permitted issuers operate under the OCC/FDIC payment-stablecoin charter. CLARITY §404 adds an intermediary layer: 'covered parties' (digital-asset service providers and affiliates) may not pay yield on held balances, but may facilitate user-initiated activity. The author synthesises a generalisable three-layer routing architecture: (1) a compliant issuer layer (GENIUS-compliant payment stablecoin), (2) an authorised routing layer (the wallet/intermediary that executes the user's signed instruction), and (3) a yield-bearing tokenised cash-management layer (registered tokenised MMF). The binding question is which entity in the chain holds which authorisation, and whether the routing layer's action is a permitted facilitation or a prohibited yield/brokerage activity.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `proposed`; effective from `None`; event `us-clarity-act-enacted`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `us-pss-capital_requirements-001`

De novo PPSIs must hold minimum capital of the greater of $5 million or the chartering-condition amount, for 36 months. An operational backstop of 12 months of operating expenses must be held in cash, FDIC-insured deposits, or short-dated Treasuries (<=93 days). Two consecutive quarter-ends below the capital or backstop requirement trigger mandatory liquidation.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `proposed`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `us-pss-cross_border_data-001`

Issuers are subject to the Bank Secrecy Act and OFAC sanctions administration; there is no data-localization rule that bars supervisory information-sharing with foreign regulators.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `us-pss-disclosure_reporting-001`

Issuers must publish monthly reserve composition certified by an independent accountant and are subject to federal and state supervisory reporting; supervisory coordination is available.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `us-pss-issuer_pathway-001`

Permitted payment stablecoin issuers are a defined set: subsidiaries of insured depository institutions, federally qualified non-bank payment stablecoin issuers approved by the OCC, and state-qualified issuers operating under an OCC-certified comparable state regime. An authorizable private token exists.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `us-clarity-act-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `us-pss-monetary_sovereignty-001`

The US issues the reserve currency and imposes no aggregate usage cap on private dollar tokens. A foreign payment stablecoin may be offered in the US only where the foreign regime is determined comparable by the Treasury and the issuer registers — an admission-by-determination channel rather than an open market.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `us-genius-act-effective`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `us-pss-permitted_activity_yield-001`

GENIUS Act §4(a)(11) prohibits permitted/foreign payment stablecoin issuers from paying any form of interest or yield (cash, tokens, or other consideration) to a holder 'solely in connection with the holding, use, or retention' of a payment stablecoin. The word 'solely' is the textual hinge: it reaches payments tied to the act of holding, not payments produced by some other operative event (user-initiated routing, market-making, transfers). OCC NPRM §15.10(c)(4) and FDIC NPRM §350.3(b)(4) add a rebuttable presumption that affiliate / related-third-party arrangements (including white-label) violate the prohibition, rebuttable by written non-evasion showing; the anti-evasion rule (proposed §15.10(c)(6)) treats any sidestep arrangement as a violation. Permitted: merchant-funded discounts; issuer profit-sharing with non-affiliated white-label partners without yield pass-through. The intermediary layer is the pending CLARITY Act §404, extending the prohibition to 'covered parties' (digital-asset service providers and affiliates) under prongs (A) 'solely in connection with holding' and (B) 'economically or functionally equivalent' to bank-deposit interest.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `us-clarity-act-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `us-pss-reserve_backing-001`

1:1 backing of outstanding payment stablecoins at fair value is required by the enacted GENIUS Act (Sec. 4(a)(1)). The detailed list of PERMISSIBLE reserve assets is set by the OCC NPRM (proposed 12 CFR Sec. 15.11(b)) and is NOT yet final — that composition is a pending overlay, not part of the in-force statutory proposition.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `us-pss-securities_classification-001`

A payment stablecoin structured to comply with the GENIUS Act (1:1 backing, no issuer yield, par redemption) is positioned as a non-security: under the Reves family-resemblance test the instrument resembles a payment/exchange medium rather than an investment note, and the absence of yield removes the principal Howey 'expectation of profit' hook. The contested boundary is not the stablecoin itself but the adjacent routing step: whether a wallet/intermediary that routes a user's payment-stablecoin balance into 1940-Act registered tokenised money market fund shares is thereby distributing securities and acting as a broker. The author's analysis (Reves' fourth factor — the presence of an alternative regulatory regime) argues registered-fund shares are already comprehensively regulated, weighing against re-characterising the routing as an unregistered securities activity.

- Source disposition: `official`; check status: `checked`.
- Temporal state: `operative`; effective from `None`; event `us-clarity-act-enacted`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

## Legal-event relationships

### `us-clarity-act-enacted` — US CLARITY Act enacted (digital-asset market structure; intermediary yield + routing layer live)

- Status: `contingent`; effective date: `None`; trigger kind: `contingent-no-date`.
- Linked records: `us-pss-bank_nonbank_routing-001`, `us-pss-permitted_activity_yield-001`, `us-pss-securities_classification-001`, `us-pss-issuer_pathway-001`.
- Internal basis: GENIUS is already in force (the issuer-level layer). CLARITY is the pending market-structure layer (H.R. 3633): us-pss-bank_nonbank_routing-001 binds on it, and the us-pss-permitted_activity_yield-001 / us-pss-securities_classification-001 / us-pss-issuer_pathway-001 cells carry its Sec. 404 and market-structure parts as flagged pending overlays.

### `us-genius-act-effective` — US GENIUS Act takes effect; §18 foreign-issuer comparability gate becomes operative (outer cap ≤ 2027-01-18)

- Status: `scheduled`; effective date: `2027-01-18`; trigger kind: `scheduled-with-cap`.
- Linked records: `us-pss-monetary_sovereignty-001`.
- Internal basis: GENIUS Act s.20: the Act takes effect on the EARLIER of 18 months after enactment (2027-01-18) or 120 days after the primary federal payment stablecoin regulators issue final regulations. On commencement the s.18 comparability gate moves from made_not_commenced to operative.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [GENIUS Act Sec. 4(a)(1) (1:1 fair-value reserve backing)](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text) — GENIUS Act Sec. 4(a)(1) (1:1 fair-value backing of outstanding payment stablecoins).
2. [GENIUS Act capital provisions; OCC/FDIC NPRM (de novo capital; operational backstop; liquidation trigger)](https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation) — capital left to OCC/FDIC rulemaking; figures from the OCC/FDIC NPRM (proposed).
3. [GENIUS Act §4(a)(11); OCC NPRM §15.10(c)(4) / anti-evasion §15.10(c)(6); FDIC NPRM §350.3(b)(4); CLARITY Act (H.R. 3633) §404(c)(1) (Tillis…](https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation) — GENIUS Act Sec. 4(a)(11) (no interest/yield in connection with holding, use, or retention).
4. [Guiding and Establishing National Innovation for U.S. Stablecoins Act (GENIUS Act)](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text) — GENIUS Act Sec. 3-4 (permitted payment stablecoin issuers: IDI subsidiaries; OCC-qualified non-banks; certified state regimes).
5. [Reves v. Ernst & Young, 494 U.S. 56 (1990); SEC v. W.J. Howey Co., 328 U.S. 293 (1946); Investment Company Act of 1940 (registered MMFs); C…](https://www.congress.gov/bill/119th-congress/senate-bill/1582/text) — GENIUS Act securities carve-out (amending the '33/'34 Acts and ICA40 for permitted payment stablecoins).

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
