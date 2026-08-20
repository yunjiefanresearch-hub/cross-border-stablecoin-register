# Pilot 1 — Enterprise cross-border stablecoin payment

Pilot ID: `pilot-enterprise-stablecoin-payment`  
As of: `2026-08-20`  
Mode: deterministic offline decision support; no transaction execution.

## Evidence boundary

The pilot uses explicitly labelled current/reconciled controlled fixtures to exercise the positive path. Those overrides are test evidence only and do not promote the committed legal records.

## Actors, jurisdictions, assets and assumed facts

- Actor: enterprise treasury requester
- Actor: mandated autonomous policy agent
- Actor: human compliance approver
- Actor: EU corporate beneficiary
- Jurisdictions: `US, EU`
- Assets: `USDC`
- Assumed fact: The payment leg uses USDC and both counterparties have separate identity and sanctions controls.
- Assumed fact: The controlled evidence fixtures are test-only and are not assertions about current law.
- Assumed fact: The treasury agent has no authority to transmit funds; it can only request a policy decision.

## Action and mandate

- Route: `US -> EU`
- Asset / amount: `USDC` / `750000`
- Mandate: `pilot-mandate-us-eu` v`1.0`
- Audit subject: `agent:pilot-runner`

## Applicable rules

| Rule | Jurisdiction | Dimension | Force | Freshness | Source |
|---|---|---|---|---|---|
| `eu-emt-issuer_pathway-001` | `EU` | `issuer_pathway` | `in_force_enacted` | `current` | unavailable |
| `us-pss-reserve_backing-001` | `US` | `reserve_backing` | `in_force_enacted` | `current` | https://www.congress.gov/bill/119th-congress/senate-bill/1582/text |

## Deterministic decision path

1. Validate action, mandate version, audit identity and requested timestamp.
2. Check route, asset, counterparty, validity interval and amount against the mandate.
3. Resolve official rule IDs, source URLs, freshness and independent-review state from explicit fixtures.
4. Apply KYC and amount-threshold controls before returning allow_with_conditions.
5. Serialize the full evidence chain into an unsigned, non-executing receipt and replay it.

## Human-review trigger

The amount 750,000 exceeds the mandate threshold of 500,000, so human approval is mandatory.

## Decision

- Outcome: `allow_with_conditions`
- Reasons: `operative_current_reconciled_evidence`
- Conditions: `complete_kyc_before_execution`, `obtain_human_approval`
- Uncertainty: `high`
- Execution authorized: `False`

## Receipt and replay

- Receipt: `cbsr-receipt-6c35fae9c10cca501a8a3da9`
- SHA-256: `3e846a0d89be3f6e5869523bc90a112e17a19e1f6f75d576eb929cd1b5eab674`
- Integrity verified: `True`
- Decision replay identical: `True`
- Receipt replay identical: `True`
- Signing state: `unsigned`

## Limitations

- No funds are moved and no live identity, sanctions, wallet or counterparty checks are performed.
- The positive evidence state is a controlled fixture, not a legal-currentness claim.
- Tax, securities, consumer, insolvency and private-law questions remain outside this pilot.

## Failure cases

- Missing or stale evidence returns review_required or insufficient_evidence.
- A revoked/expired mandate, disallowed route, asset or counterparty returns prohibited.
- Absent human approval leaves the action conditioned and never authorizes execution.

The receipt proves deterministic integrity only; it does not authenticate a person, execute a payment, or replace legal advice.
