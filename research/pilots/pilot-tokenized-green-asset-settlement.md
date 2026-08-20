# Pilot 2 — Tokenized green-asset settlement

Pilot ID: `pilot-tokenized-green-asset-settlement`  
As of: `2026-08-20`  
Mode: deterministic offline decision support; no transaction execution.

## Evidence boundary

This controlled DvP fixture tests only the stablecoin settlement-policy leg. Green taxonomy, securities-law classification, title transfer and asset eligibility are assumed inputs and remain separate human gates.

## Actors, jurisdictions, assets and assumed facts

- Actor: Singapore green-bond seller
- Actor: EU institutional buyer
- Actor: mandated settlement-policy agent
- Actor: human legal/compliance approver
- Jurisdictions: `SG, EU`
- Assets: `USDC, USDC, tokenized_green_bond`
- Assumed fact: The delivery asset is a tokenized green bond and the payment asset is USDC.
- Assumed fact: Eligibility, green taxonomy and securities-law analysis have not been performed by CBSR.
- Assumed fact: A separate atomic-settlement system would act only after all human and external controls pass.

## Action and mandate

- Route: `SG -> EU`
- Asset / amount: `USDC` / `250000`
- Mandate: `pilot-mandate-sg-eu-green` v`1.0`
- Audit subject: `agent:pilot-runner`

## Applicable rules

| Rule | Jurisdiction | Dimension | Force | Freshness | Source |
|---|---|---|---|---|---|
| `eu-emt-issuer_pathway-001` | `EU` | `issuer_pathway` | `in_force_enacted` | `current` | unavailable |
| `sg-scs-issuer_pathway-001` | `SG` | `issuer_pathway` | `finalized_policy_pending` | `current` | unavailable |

## Deterministic decision path

1. Validate the generic DvP action, stablecoin payment leg and versioned mandate.
2. Check Singapore-to-EU route, USDC asset, counterparty, amount and validity interval.
3. Evaluate only explicit stablecoin issuer-pathway fixtures; do not infer green-asset legality.
4. Require KYC and human review because 250,000 exceeds the 100,000 threshold.
5. Emit allow_with_conditions with assumptions, obligations, sources and an unsigned replayable receipt.

## Human-review trigger

The amount exceeds 100,000 and the underlying tokenized security is outside CBSR's stablecoin domain pack.

## Decision

- Outcome: `review_required`
- Reasons: `non_final_transitional_or_superseded_rule`, `rule_not_operative`
- Conditions: `complete_kyc_before_execution`, `obtain_human_approval`
- Uncertainty: `high`
- Execution authorized: `False`

## Receipt and replay

- Receipt: `cbsr-receipt-9a18472655a434afa9990528`
- SHA-256: `5426ba7c9cadd9f8b96dfb51bbbeb9e113a7882e8e9bf07cd268072cfb9242a4`
- Integrity verified: `True`
- Decision replay identical: `True`
- Receipt replay identical: `True`
- Signing state: `unsigned`

## Limitations

- CBSR does not determine whether the token is a security, whether the bond is green, or whether title transfers.
- The current/reconciled state is a controlled test fixture and does not update the legal register.
- Atomicity, custody, settlement finality, oracle and smart-contract risks are outside the decision receipt.

## Failure cases

- Unknown asset classification or missing securities-law evidence requires legal review.
- Failed KYC/sanctions, disallowed route or expired mandate prevents progression.
- No human approval, stale stablecoin evidence or receipt-integrity failure blocks settlement.

The receipt proves deterministic integrity only; it does not authenticate a person, execute a payment, or replace legal advice.
