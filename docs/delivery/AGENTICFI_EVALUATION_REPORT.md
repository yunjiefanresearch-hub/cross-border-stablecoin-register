# AgenticFi evaluation report

Evaluation date: **2026-08-20**.  
Engine: `cbsr-policy-engine/1.1.0`. Ruleset: `cbsr-stablecoin-rules/1.1.0`.

## Result

The table-driven suite covers **31 independent policy scenarios** and **13 receipt mutations**. Two end-to-end pilots produce byte-identical decisions and receipts on replay. All outcomes remain decision support with `execution_authorized=false`.

## Scenario coverage

| Scenario | Expected outcome |
|---|---|
| `allow_current_reconciled` | `allow` |
| `missing_action` | `insufficient_evidence` |
| `malformed_amount` | `insufficient_evidence` |
| `negative_amount` | `insufficient_evidence` |
| `unknown_action_schema` | `insufficient_evidence` |
| `invalid_as_of` | `insufficient_evidence` |
| `same_jurisdiction` | `insufficient_evidence` |
| `revoked_mandate` | `prohibited` |
| `inactive_mandate` | `prohibited` |
| `mandate_not_started` | `prohibited` |
| `mandate_expired` | `prohibited` |
| `outside_time_window` | `prohibited` |
| `prohibited_jurisdiction` | `prohibited` |
| `over_amount_limit` | `prohibited` |
| `asset_outside_mandate` | `prohibited` |
| `jurisdiction_outside_mandate` | `prohibited` |
| `counterparty_outside_mandate` | `prohibited` |
| `no_evidence` | `insufficient_evidence` |
| `malformed_evidence` | `insufficient_evidence` |
| `unknown_record` | `insufficient_evidence` |
| `regulatory_prohibition` | `prohibited` |
| `stale_evidence` | `review_required` |
| `proposed_rule` | `review_required` |
| `not_commenced` | `review_required` |
| `superseded_rule` | `review_required` |
| `second_review_missing` | `review_required` |
| `declared_conflict` | `review_required` |
| `detected_conflict` | `review_required` |
| `human_review_required` | `allow_with_conditions` |
| `human_threshold` | `allow_with_conditions` |
| `kyc_condition` | `allow_with_conditions` |

## Receipt mutation coverage

- `action`
- `decision`
- `applicable_rules`
- `source_urls`
- `freshness_snapshot`
- `assumptions`
- `mandate_version`
- `audit_identity`
- `engine_version`
- `ruleset_version`
- `generated_at`
- `requested_as_of`
- `non_legal_advice_notice`

## Reproducible pilots

1. [`pilot-enterprise-stablecoin-payment`](../../research/pilots/pilot-enterprise-stablecoin-payment.md) exercises current/reconciled controlled fixtures, human-review threshold and KYC conditions.
2. [`pilot-tokenized-green-asset-settlement`](../../research/pilots/pilot-tokenized-green-asset-settlement.md) exercises a controlled delivery-versus-payment request while explicitly excluding green taxonomy and securities-law claims.

## Interpretation limits

The evaluation proves deterministic policy behavior, evidence-chain completeness and tamper detection. It does not prove legal currentness, authenticate the asserted audit identity, authorize execution or replace an external security/legal review.
