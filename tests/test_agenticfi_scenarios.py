"""Table-driven AgenticFi acceptance suite covering independent policy paths."""

from __future__ import annotations

from copy import deepcopy

import pytest

from cbsr_mcp.policy import evaluate_policy


def base_action() -> dict:
    return {
        "schema": "cbsr/policy-action/v1",
        "action_id": "scenario-action",
        "origin": "US",
        "destination": "EU",
        "asset": "USDC",
        "amount": "100",
        "actor": "agent:treasury",
        "counterparty": "cp-1",
        "as_of": "2026-08-20",
        "requested_at": "2026-08-20T10:00:00Z",
        "mandate": {
            "schema": "cbsr/policy-mandate/v1",
            "mandate_id": "mandate-scenario",
            "version": "1.0",
            "issued_by": "human:policy-owner",
            "active": True,
            "revoked": False,
            "valid_from": "2026-01-01",
            "valid_until": "2027-01-01",
            "max_amount": "1000",
            "assets": ["USDC"],
            "jurisdictions": ["US", "EU"],
            "prohibited_jurisdictions": ["CN"],
            "counterparties": ["cp-1"],
            "human_review": {"required": False},
            "audit_identity": {
                "subject_id": "agent:treasury", "actor_type": "agent",
                "principal_id": "human:policy-owner", "session_id": "session-1",
                "authentication_context": ["mfa"],
            },
        },
    }


def base_evidence(**updates) -> dict:
    value = {
        "id": "rule-1", "jurisdiction": "EU", "dimension": "issuer_pathway",
        "status": "in_force", "binding_status": "in_force_enacted", "legal_status": "operative",
        "evidence_tier": "resolution_text", "source_disposition": "official",
        "source_last_checked": "2026-08-20", "next_review_due": "2026-09-19",
        "freshness": {"review_status": "current", "source_last_checked": "2026-08-20"},
        "review_stage": "reconciled", "uncertainty": "low",
        "source": {"url": "https://example.gov/rule-1"},
    }
    value.update(updates)
    return value


def nested(value: dict, path: str, replacement) -> dict:
    result = deepcopy(value)
    cursor = result
    parts = path.split(".")
    for item in parts[:-1]:
        cursor = cursor[item]
    cursor[parts[-1]] = replacement
    return result


SCENARIOS = [
    ("allow_current_reconciled", {}, [base_evidence()], "allow", "operative_current_reconciled_evidence"),
    ("missing_action", {"__replace__": {}}, [], "insufficient_evidence", "missing_context"),
    ("malformed_amount", {"amount": "not-a-number"}, [base_evidence()], "insufficient_evidence", "amount_must_be_a_number"),
    ("negative_amount", {"amount": "-1"}, [base_evidence()], "insufficient_evidence", "amount_must_be_non_negative_number"),
    ("unknown_action_schema", {"schema": "cbsr/policy-action/v99"}, [base_evidence()], "insufficient_evidence", "unsupported_action_schema"),
    ("invalid_as_of", {"__as_of__": "not-a-date"}, [base_evidence()], "insufficient_evidence", "invalid_as_of_date"),
    ("same_jurisdiction", {"destination": "US"}, [base_evidence()], "insufficient_evidence", "domain_validation"),
    ("revoked_mandate", {"mandate.revoked": True}, [base_evidence()], "prohibited", "mandate_revoked_or_inactive"),
    ("inactive_mandate", {"mandate.active": False}, [base_evidence()], "prohibited", "mandate_revoked_or_inactive"),
    ("mandate_not_started", {"mandate.valid_from": "2026-09-01"}, [base_evidence()], "prohibited", "mandate_not_yet_valid"),
    ("mandate_expired", {"mandate.valid_until": "2026-08-19"}, [base_evidence()], "prohibited", "mandate_expired"),
    ("outside_time_window", {"mandate.allowed_time_windows": [{"starts_at": "2026-08-20T12:00:00Z", "ends_at": "2026-08-20T13:00:00Z"}]}, [base_evidence()], "prohibited", "outside_mandate_time_window"),
    ("prohibited_jurisdiction", {"destination": "CN", "mandate.jurisdictions": ["US", "CN"]}, [base_evidence(jurisdiction="CN")], "prohibited", "prohibited_jurisdiction_in_mandate"),
    ("over_amount_limit", {"amount": "1001"}, [base_evidence()], "prohibited", "amount_exceeds_mandate"),
    ("asset_outside_mandate", {"asset": "EURC"}, [base_evidence()], "prohibited", "asset_outside_mandate"),
    ("jurisdiction_outside_mandate", {"destination": "JP"}, [base_evidence(jurisdiction="JP")], "prohibited", "jurisdiction_outside_mandate"),
    ("counterparty_outside_mandate", {"counterparty": "cp-2"}, [base_evidence()], "prohibited", "counterparty_outside_mandate"),
    ("no_evidence", {}, [], "insufficient_evidence", "no_applicable_regulatory_evidence"),
    ("malformed_evidence", {}, [base_evidence(id="")], "insufficient_evidence", "malformed_evidence_record"),
    ("unknown_record", {}, [base_evidence(id="unknown-rule")], "insufficient_evidence", "unknown_evidence_record"),
    ("regulatory_prohibition", {}, [base_evidence(binding_status="prohibition", legal_status="prohibited")], "prohibited", "applicable_regulatory_prohibition"),
    ("stale_evidence", {}, [base_evidence(freshness={"review_status": "stale"})], "review_required", "evidence_not_current"),
    ("proposed_rule", {}, [base_evidence(status="proposed", binding_status="pending_proposal", legal_status="proposed")], "review_required", "rule_not_operative"),
    ("not_commenced", {}, [base_evidence(binding_status="made_not_commenced", legal_status="enacted_not_commenced")], "review_required", "rule_not_operative"),
    ("superseded_rule", {}, [base_evidence(status="superseded", legal_status="superseded")], "review_required", "non_final_transitional_or_superseded_rule"),
    ("second_review_missing", {}, [base_evidence(review_stage="primary_reviewed_second_pending")], "review_required", "independent_second_review_incomplete"),
    ("declared_conflict", {"conflicting_evidence": True}, [base_evidence()], "review_required", "conflicting_evidence"),
    ("detected_conflict", {}, [base_evidence(), base_evidence(id="rule-2", binding_status="pending_proposal", legal_status="proposed", source={"url": "https://example.gov/rule-2"})], "review_required", "conflicting_evidence"),
    ("human_review_required", {"mandate.human_review": {"required": True}}, [base_evidence()], "allow_with_conditions", "operative_current_reconciled_evidence"),
    ("human_threshold", {"mandate.human_review": {"required": False, "amount_threshold": "100"}}, [base_evidence()], "allow_with_conditions", "operative_current_reconciled_evidence"),
    ("kyc_condition", {"requires_kyc": True}, [base_evidence()], "allow_with_conditions", "operative_current_reconciled_evidence"),
]


@pytest.mark.parametrize("name,patch,evidence,expected,reason", SCENARIOS, ids=[item[0] for item in SCENARIOS])
def test_agenticfi_scenario(name, patch, evidence, expected, reason):
    del name
    candidate = {} if "__replace__" in patch else base_action()
    for key, value in patch.items():
        if key in {"__replace__", "__as_of__"}:
            continue
        candidate = nested(candidate, key, value) if "." in key else {**candidate, key: value}
    as_of = patch.get("__as_of__", "2026-08-20")
    known = {"rule-1", "rule-2"}
    result = evaluate_policy(candidate, evidence, as_of, known_record_ids=known)
    assert result["outcome"] == expected
    assert any(item.startswith(reason) for item in result["reasons"])
    assert result["execution_authorized"] is False


def test_full_conflict_retains_both_rules_sources_and_resolution():
    evidence = [
        base_evidence(),
        base_evidence(
            id="rule-2", binding_status="pending_proposal", legal_status="proposed",
            source={"url": "https://example.gov/rule-2"},
        ),
    ]
    result = evaluate_policy(base_action(), evidence, "2026-08-20", known_record_ids={"rule-1", "rule-2"})
    conflict = result["conflict_details"][0]
    assert conflict["record_ids"] == ("rule-1", "rule-2")
    assert len(conflict["source_urls"]) == 2
    assert conflict["resolution"] == "human_reconciliation_required"


def test_decision_replay_is_exact_for_the_full_receipt_input():
    first = evaluate_policy(base_action(), [base_evidence()], "2026-08-20", known_record_ids={"rule-1"})
    second = evaluate_policy(base_action(), [base_evidence()], "2026-08-20", known_record_ids={"rule-1"})
    assert first == second
    assert first["applicable_rules"][0]["source_last_checked"] == "2026-08-20"
    assert first["mandate_version"] == "1.0"
