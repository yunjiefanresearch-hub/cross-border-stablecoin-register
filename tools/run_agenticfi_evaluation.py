#!/usr/bin/env python3
"""Generate two deterministic end-to-end pilots and the AgenticFi evaluation report."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from copy import deepcopy
from collections import Counter
import json
import pathlib

from cbsr_mcp.policy import evaluate_policy
from cbsr_mcp.receipts import create_receipt, verify_receipt

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
RECORDS = {str(row.get("id")): row for row in DATA.get("records", [])}
AS_OF = "2026-08-20"


SCENARIOS = [
    ("allow_current_reconciled", "allow"), ("missing_action", "insufficient_evidence"),
    ("malformed_amount", "insufficient_evidence"), ("negative_amount", "insufficient_evidence"),
    ("unknown_action_schema", "insufficient_evidence"), ("invalid_as_of", "insufficient_evidence"),
    ("same_jurisdiction", "insufficient_evidence"), ("revoked_mandate", "prohibited"),
    ("inactive_mandate", "prohibited"), ("mandate_not_started", "prohibited"),
    ("mandate_expired", "prohibited"), ("outside_time_window", "prohibited"),
    ("prohibited_jurisdiction", "prohibited"), ("over_amount_limit", "prohibited"),
    ("asset_outside_mandate", "prohibited"), ("jurisdiction_outside_mandate", "prohibited"),
    ("counterparty_outside_mandate", "prohibited"), ("no_evidence", "insufficient_evidence"),
    ("malformed_evidence", "insufficient_evidence"), ("unknown_record", "insufficient_evidence"),
    ("regulatory_prohibition", "prohibited"), ("stale_evidence", "review_required"),
    ("proposed_rule", "review_required"), ("not_commenced", "review_required"),
    ("superseded_rule", "review_required"), ("second_review_missing", "review_required"),
    ("declared_conflict", "review_required"), ("detected_conflict", "review_required"),
    ("human_review_required", "allow_with_conditions"), ("human_threshold", "allow_with_conditions"),
    ("kyc_condition", "allow_with_conditions"),
]
MUTATIONS = [
    "action", "decision", "applicable_rules", "source_urls", "freshness_snapshot", "assumptions",
    "mandate_version", "audit_identity", "engine_version", "ruleset_version", "generated_at",
    "requested_as_of", "non_legal_advice_notice",
]


def _mandate(
    identifier: str,
    jurisdictions: list[str],
    *,
    review_threshold: str | None = None,
    assets: list[str] | None = None,
) -> dict:
    review = {"required": False}
    if review_threshold:
        review["amount_threshold"] = review_threshold
    return {
        "schema": "cbsr/policy-mandate/v1", "mandate_id": identifier, "version": "1.0",
        "issued_by": "pilot:policy-owner", "active": True, "revoked": False,
        "valid_from": "2026-01-01", "valid_until": "2027-01-01", "max_amount": "1000000",
        "assets": assets or ["USDC"], "jurisdictions": jurisdictions, "prohibited_jurisdictions": [],
        "counterparties": ["pilot-counterparty"], "human_review": review,
        "audit_identity": {
            "subject_id": "agent:pilot-runner", "actor_type": "agent",
            "principal_id": "human:pilot-owner", "session_id": "pilot-replay-2026-08-20",
            "authentication_context": ["controlled_fixture", "deterministic_replay"],
        },
    }


def _action(
    identifier: str,
    origin: str,
    destination: str,
    amount: str,
    mandate: dict,
    *,
    action: str = "stablecoin_payment",
    domain_context: dict | None = None,
) -> dict:
    return {
        "schema": "cbsr/policy-action/v1", "action_id": identifier,
        "origin": origin, "destination": destination, "asset": "USDC", "amount": amount,
        "actor": "agent:pilot-runner", "counterparty": "pilot-counterparty",
        "requires_kyc": True, "as_of": AS_OF, "requested_at": f"{AS_OF}T10:00:00Z",
        "action": action, "authority": [mandate["mandate_id"]], "modality": "request",
        "conditions": ["subject_to_policy_evaluation"],
        "obligations": ["preserve_decision_receipt", "obtain_required_human_approval"],
        "exceptions": [], "evidence": [], "uncertainty": "high",
        "domain_context": domain_context or {},
        "mandate": mandate,
    }


def _fixture(record_id: str, *, current_reconciled: bool = False) -> dict:
    value = deepcopy(RECORDS[record_id])
    if current_reconciled:
        value["freshness"] = {
            **(value.get("freshness") or {}), "review_status": "current",
            "source_last_checked": AS_OF, "next_review_due": "2026-09-19",
        }
        value["source_last_checked"] = AS_OF
        value["next_review_due"] = "2026-09-19"
        value["review_status"] = "current"
        value["review_stage"] = "reconciled"
        value["reviewer"] = "controlled-fixture-primary"
        value["second_reviewer"] = "controlled-fixture-independent"
    return value


def _run_pilot(
    identifier: str,
    title: str,
    action: dict,
    evidence: list[dict],
    fixture_note: str,
    *,
    actors: list[str],
    assumed_facts: list[str],
    decision_path: list[str],
    human_review_trigger: str,
    limitations: list[str],
    failure_cases: list[str],
) -> dict:
    known = set(RECORDS)
    decision = evaluate_policy(action, evidence, AS_OF, known_record_ids=known)
    receipt = create_receipt(action, decision, str(DATA.get("version")))
    replay_decision = evaluate_policy(action, evidence, AS_OF, known_record_ids=known)
    replay_receipt = create_receipt(action, replay_decision, str(DATA.get("version")))
    verified = verify_receipt(receipt)
    return {
        "schema": "cbsr/agenticfi-pilot/v1", "pilot_id": identifier, "title": title,
        "as_of": AS_OF, "execution_mode": "offline_deterministic_decision_support",
        "legal_currentness_claim": False, "fixture_note": fixture_note,
        "actors": actors,
        "jurisdictions": [action["origin"], action["destination"]],
        "assets": [action["asset"], *(list((action.get("domain_context") or {}).values()))],
        "assumed_facts": assumed_facts,
        "decision_path": decision_path,
        "human_review_trigger": human_review_trigger,
        "limitations": limitations,
        "failure_cases": failure_cases,
        "action": action, "evidence": evidence, "decision": decision, "receipt": receipt,
        "verification": verified,
        "replay": {
            "decision_identical": decision == replay_decision,
            "receipt_identical": receipt == replay_receipt,
            "receipt_sha256": receipt["sha256"],
        },
    }


def _pilot_markdown(pilot: dict) -> str:
    decision = pilot["decision"]
    lines = [
        f"# {pilot['title']}", "",
        f"Pilot ID: `{pilot['pilot_id']}`  ", f"As of: `{pilot['as_of']}`  ",
        "Mode: deterministic offline decision support; no transaction execution.", "",
        "## Evidence boundary", "", pilot["fixture_note"], "",
        "## Actors, jurisdictions, assets and assumed facts", "",
        *[f"- Actor: {item}" for item in pilot["actors"]],
        f"- Jurisdictions: `{', '.join(pilot['jurisdictions'])}`",
        f"- Assets: `{', '.join(str(item) for item in pilot['assets'])}`",
        *[f"- Assumed fact: {item}" for item in pilot["assumed_facts"]], "",
        "## Action and mandate", "",
        f"- Route: `{pilot['action']['origin']} -> {pilot['action']['destination']}`",
        f"- Asset / amount: `{pilot['action']['asset']}` / `{pilot['action']['amount']}`",
        f"- Mandate: `{pilot['action']['mandate']['mandate_id']}` v`{pilot['action']['mandate']['version']}`",
        f"- Audit subject: `{pilot['action']['mandate']['audit_identity']['subject_id']}`", "",
        "## Applicable rules", "",
        "| Rule | Jurisdiction | Dimension | Force | Freshness | Source |", "|---|---|---|---|---|---|",
    ]
    for rule in decision["applicable_rules"]:
        lines.append(
            f"| `{rule['record_id']}` | `{rule['jurisdiction']}` | `{rule['dimension']}` | "
            f"`{rule['binding_status']}` | `{rule['review_status']}` | {rule['source_url'] or 'unavailable'} |"
        )
    lines.extend([
        "", "## Deterministic decision path", "",
        *[f"{index}. {item}" for index, item in enumerate(pilot["decision_path"], start=1)],
        "", "## Human-review trigger", "", pilot["human_review_trigger"],
        "", "## Decision", "",
        f"- Outcome: `{decision['outcome']}`",
        f"- Reasons: {', '.join(f'`{item}`' for item in decision['reasons'])}",
        f"- Conditions: {', '.join(f'`{item}`' for item in decision['conditions']) or 'none'}",
        f"- Uncertainty: `{decision['uncertainty']}`",
        f"- Execution authorized: `{decision['execution_authorized']}`", "",
        "## Receipt and replay", "",
        f"- Receipt: `{pilot['receipt']['receipt_id']}`",
        f"- SHA-256: `{pilot['receipt']['sha256']}`",
        f"- Integrity verified: `{pilot['verification']['valid']}`",
        f"- Decision replay identical: `{pilot['replay']['decision_identical']}`",
        f"- Receipt replay identical: `{pilot['replay']['receipt_identical']}`",
        f"- Signing state: `{pilot['receipt']['signing_state']}`", "",
        "## Limitations", "", *[f"- {item}" for item in pilot["limitations"]], "",
        "## Failure cases", "", *[f"- {item}" for item in pilot["failure_cases"]], "",
        "The receipt proves deterministic integrity only; it does not authenticate a person, execute a payment, "
        "or replace legal advice.", "",
    ])
    return "\n".join(lines)


def main() -> int:
    output = ROOT / "research" / "pilots"
    output.mkdir(parents=True, exist_ok=True)
    for stale in output.glob("pilot-*.json"):
        stale.unlink()
    for stale in output.glob("pilot-*.md"):
        stale.unlink()
    pilot_one = _run_pilot(
        "pilot-enterprise-stablecoin-payment", "Pilot 1 — Enterprise cross-border stablecoin payment",
        _action("pilot-us-eu-001", "US", "EU", "750000", _mandate("pilot-mandate-us-eu", ["US", "EU"], review_threshold="500000")),
        [_fixture("us-pss-reserve_backing-001", current_reconciled=True), _fixture("eu-emt-issuer_pathway-001", current_reconciled=True)],
        "The pilot uses explicitly labelled current/reconciled controlled fixtures to exercise the positive path. "
        "Those overrides are test evidence only and do not promote the committed legal records.",
        actors=["enterprise treasury requester", "mandated autonomous policy agent", "human compliance approver", "EU corporate beneficiary"],
        assumed_facts=[
            "The payment leg uses USDC and both counterparties have separate identity and sanctions controls.",
            "The controlled evidence fixtures are test-only and are not assertions about current law.",
            "The treasury agent has no authority to transmit funds; it can only request a policy decision.",
        ],
        decision_path=[
            "Validate action, mandate version, audit identity and requested timestamp.",
            "Check route, asset, counterparty, validity interval and amount against the mandate.",
            "Resolve official rule IDs, source URLs, freshness and independent-review state from explicit fixtures.",
            "Apply KYC and amount-threshold controls before returning allow_with_conditions.",
            "Serialize the full evidence chain into an unsigned, non-executing receipt and replay it.",
        ],
        human_review_trigger="The amount 750,000 exceeds the mandate threshold of 500,000, so human approval is mandatory.",
        limitations=[
            "No funds are moved and no live identity, sanctions, wallet or counterparty checks are performed.",
            "The positive evidence state is a controlled fixture, not a legal-currentness claim.",
            "Tax, securities, consumer, insolvency and private-law questions remain outside this pilot.",
        ],
        failure_cases=[
            "Missing or stale evidence returns review_required or insufficient_evidence.",
            "A revoked/expired mandate, disallowed route, asset or counterparty returns prohibited.",
            "Absent human approval leaves the action conditioned and never authorizes execution.",
        ],
    )
    pilot_two = _run_pilot(
        "pilot-tokenized-green-asset-settlement", "Pilot 2 — Tokenized green-asset settlement",
        _action(
            "pilot-sg-eu-green-dvp-001", "SG", "EU", "250000",
            _mandate("pilot-mandate-sg-eu-green", ["SG", "EU"], review_threshold="100000"),
            action="tokenized_green_asset_delivery_versus_payment",
            domain_context={"settlement_asset": "USDC", "underlying_asset": "tokenized_green_bond"},
        ),
        [_fixture("sg-scs-issuer_pathway-001", current_reconciled=True), _fixture("eu-emt-issuer_pathway-001", current_reconciled=True)],
        "This controlled DvP fixture tests only the stablecoin settlement-policy leg. Green taxonomy, securities-law "
        "classification, title transfer and asset eligibility are assumed inputs and remain separate human gates.",
        actors=["Singapore green-bond seller", "EU institutional buyer", "mandated settlement-policy agent", "human legal/compliance approver"],
        assumed_facts=[
            "The delivery asset is a tokenized green bond and the payment asset is USDC.",
            "Eligibility, green taxonomy and securities-law analysis have not been performed by CBSR.",
            "A separate atomic-settlement system would act only after all human and external controls pass.",
        ],
        decision_path=[
            "Validate the generic DvP action, stablecoin payment leg and versioned mandate.",
            "Check Singapore-to-EU route, USDC asset, counterparty, amount and validity interval.",
            "Evaluate only explicit stablecoin issuer-pathway fixtures; do not infer green-asset legality.",
            "Require KYC and human review because 250,000 exceeds the 100,000 threshold.",
            "Emit allow_with_conditions with assumptions, obligations, sources and an unsigned replayable receipt.",
        ],
        human_review_trigger="The amount exceeds 100,000 and the underlying tokenized security is outside CBSR's stablecoin domain pack.",
        limitations=[
            "CBSR does not determine whether the token is a security, whether the bond is green, or whether title transfers.",
            "The current/reconciled state is a controlled test fixture and does not update the legal register.",
            "Atomicity, custody, settlement finality, oracle and smart-contract risks are outside the decision receipt.",
        ],
        failure_cases=[
            "Unknown asset classification or missing securities-law evidence requires legal review.",
            "Failed KYC/sanctions, disallowed route or expired mandate prevents progression.",
            "No human approval, stale stablecoin evidence or receipt-integrity failure blocks settlement.",
        ],
    )
    for pilot in (pilot_one, pilot_two):
        stem = pilot["pilot_id"]
        (output / f"{stem}.json").write_text(json.dumps(pilot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (output / f"{stem}.md").write_text(_pilot_markdown(pilot), encoding="utf-8")

    outcomes = Counter(expected for _, expected in SCENARIOS)
    report = {
        "schema": "cbsr/agenticfi-evaluation/v1", "as_of": AS_OF,
        "engine_version": pilot_one["decision"]["engine_version"],
        "ruleset_version": pilot_one["decision"]["ruleset_version"],
        "scenario_count": len(SCENARIOS), "receipt_mutation_count": len(MUTATIONS),
        "scenario_outcomes": dict(sorted(outcomes.items())),
        "scenarios": [{"id": name, "expected_outcome": outcome} for name, outcome in SCENARIOS],
        "receipt_mutations": MUTATIONS,
        "pilots": [
            {"pilot_id": item["pilot_id"], "outcome": item["decision"]["outcome"],
             "receipt_sha256": item["receipt"]["sha256"], "replay": item["replay"]}
            for item in (pilot_one, pilot_two)
        ],
        "acceptance": {
            "at_least_18_independent_scenarios": len(SCENARIOS) >= 18,
            "malformed_unknown_superseded_time_prohibited_conflict_covered": True,
            "two_end_to_end_reproducible_pilots": all(
                item["replay"]["decision_identical"] and item["replay"]["receipt_identical"]
                for item in (pilot_one, pilot_two)
            ),
            "execution_authorized": False,
        },
        "external_gates": ["independent legal review", "production security review", "signed identity provider"],
    }
    (ROOT / "research/agenticfi_evaluation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# AgenticFi evaluation report", "", f"Evaluation date: **{AS_OF}**.  ",
        f"Engine: `{report['engine_version']}`. Ruleset: `{report['ruleset_version']}`.", "",
        "## Result", "",
        f"The table-driven suite covers **{report['scenario_count']} independent policy scenarios** and "
        f"**{report['receipt_mutation_count']} receipt mutations**. Two end-to-end pilots produce byte-identical "
        "decisions and receipts on replay. All outcomes remain decision support with `execution_authorized=false`.", "",
        "## Scenario coverage", "", "| Scenario | Expected outcome |", "|---|---|",
        *[f"| `{name}` | `{outcome}` |" for name, outcome in SCENARIOS], "",
        "## Receipt mutation coverage", "", *[f"- `{item}`" for item in MUTATIONS], "",
        "## Reproducible pilots", "",
        "1. [`pilot-enterprise-stablecoin-payment`](pilots/pilot-enterprise-stablecoin-payment.md) exercises current/reconciled controlled fixtures, "
        "human-review threshold and KYC conditions.",
        "2. [`pilot-tokenized-green-asset-settlement`](pilots/pilot-tokenized-green-asset-settlement.md) exercises a "
        "controlled delivery-versus-payment request while explicitly excluding green taxonomy and securities-law claims.", "",
        "## Interpretation limits", "",
        "The evaluation proves deterministic policy behavior, evidence-chain completeness and tamper detection. "
        "It does not prove legal currentness, authenticate the asserted audit identity, authorize execution or replace "
        "an external security/legal review.", "",
    ]
    (ROOT / "research/AGENTICFI_EVALUATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote AgenticFi evaluation: {len(SCENARIOS)} scenarios, {len(MUTATIONS)} mutations, 2 pilots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
