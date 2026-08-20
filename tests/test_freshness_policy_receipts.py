from copy import deepcopy

from cbsr_mcp.freshness import derive_freshness
from cbsr_mcp.policy import evaluate_policy
from cbsr_mcp.receipts import create_receipt, verify_receipt


def action(**overrides):
    value = {
        "action_id": "act-001",
        "origin": "US",
        "destination": "EU",
        "asset": "USDC",
        "amount": "100",
        "actor": "treasury-agent",
        "counterparty": "cp-1",
        "as_of": "2026-08-20",
        "requested_at": "2026-08-20T10:00:00Z",
        "mandate": {
            "schema": "cbsr/policy-mandate/v1",
            "mandate_id": "mandate-001",
            "version": "1.0",
            "issued_by": "treasury-policy-owner",
            "active": True,
            "valid_from": "2026-01-01",
            "valid_until": "2027-01-01",
            "max_amount": "1000",
            "assets": ["USDC"],
            "jurisdictions": ["US", "EU"],
            "prohibited_jurisdictions": ["CN"],
            "counterparties": ["cp-1"],
            "human_review": {"required": False, "amount_threshold": "500"},
            "audit_identity": {
                "subject_id": "agent:treasury-01", "actor_type": "agent",
                "principal_id": "human:owner-01", "session_id": "session-001",
                "authentication_context": ["mfa", "workload_identity"],
            },
        },
    }
    value.update(overrides)
    return value


def evidence(**overrides):
    value = {
        "id": "eu-emt-issuer_pathway-001",
        "jurisdiction": "EU",
        "dimension": "issuer_pathway",
        "status": "in_force",
        "binding_status": "in_force_enacted",
        "evidence_tier": "resolution_text",
        "freshness": {"review_status": "current"},
        "review_stage": "reconciled",
        "source_disposition": "official",
        "source": {"url": "https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng"},
    }
    value.update(overrides)
    return value


def test_freshness_is_deterministic_and_exposes_overdue_age():
    row = {"source_last_checked": "2026-07-01", "binding_status": "in_force_enacted", "evidence_tier": "resolution_text"}
    result = derive_freshness(row, "2026-08-20")
    assert result["review_status"] == "stale"
    assert result["next_review_due"] == "2026-07-31"
    assert result["days_overdue"] == 20
    assert result == derive_freshness(row, "2026-08-20")


def test_missing_context_is_insufficient_evidence():
    assert evaluate_policy({}, [], "2026-08-20")["outcome"] == "insufficient_evidence"


def test_revoked_mandate_is_prohibited():
    candidate = action()
    candidate["mandate"]["revoked"] = True
    assert evaluate_policy(candidate, [evidence()], "2026-08-20")["outcome"] == "prohibited"


def test_mandate_limit_cannot_be_overridden_by_regulatory_allow():
    candidate = action(amount="1001")
    assert evaluate_policy(candidate, [evidence()], "2026-08-20")["outcome"] == "prohibited"


def test_regulatory_prohibition_cannot_be_overridden_by_mandate():
    row = evidence(binding_status="prohibition")
    assert evaluate_policy(action(), [row], "2026-08-20")["outcome"] == "prohibited"


def test_stale_and_proposed_evidence_require_review():
    stale = evidence(freshness={"review_status": "stale"})
    proposed = evidence(status="proposed", binding_status="pending_proposal")
    assert evaluate_policy(action(), [stale], "2026-08-20")["outcome"] == "review_required"
    assert evaluate_policy(action(), [proposed], "2026-08-20")["outcome"] == "review_required"


def test_current_operative_evidence_can_allow_with_conditions():
    candidate = action()
    candidate["mandate"]["human_review"] = {"required": True}
    result = evaluate_policy(candidate, [evidence()], "2026-08-20")
    assert result["outcome"] == "allow_with_conditions"
    assert result["conditions"] == ["obtain_human_approval"]


def test_current_operative_evidence_can_allow_but_never_execute():
    result = evaluate_policy(action(), [evidence()], "2026-08-20")
    assert result["outcome"] == "allow"
    assert result["execution_authorized"] is False
    assert result["schema"] == "cbsr/policy-decision/v1"
    assert result["rule_ids"] == ["cbsr.rule.eu-emt-issuer_pathway-001"]
    assert result["source_urls"]
    assert result["engine_version"] == "cbsr-policy-engine/1.1.0"
    assert result["ruleset_version"] == "cbsr-stablecoin-rules/1.1.0"
    assert "verify_issuer_and_intermediary_authorizations" in result["obligations"]


def test_current_evidence_without_independent_reconciliation_requires_review():
    row = evidence(review_stage="primary_reviewed_second_pending")
    result = evaluate_policy(action(), [row], "2026-08-20")
    assert result["outcome"] == "review_required"
    assert "independent_second_review_incomplete" in result["reasons"]


def test_last_reviewed_does_not_manufacture_a_source_check():
    result = derive_freshness(
        {"last_reviewed": "2026-08-20", "binding_status": "in_force_enacted",
         "evidence_tier": "resolution_text", "source_disposition": "official"},
        "2026-08-20",
    )
    assert result["review_status"] == "unknown"
    assert result["source_last_checked"] is None


def test_policy_replay_is_byte_for_byte_deterministic():
    first = evaluate_policy(action(), [evidence()], "2026-08-20")
    second = evaluate_policy(action(), [evidence()], "2026-08-20")
    assert first == second


def test_receipt_detects_tampering_and_states_unsigned_boundary():
    decision = evaluate_policy(action(), [evidence()], "2026-08-20")
    receipt = create_receipt(action(), decision, "0.11.0")
    assert verify_receipt(receipt)["valid"] is True
    assert receipt["signing_state"] == "unsigned"
    tampered = deepcopy(receipt)
    tampered["decision"]["outcome"] = "prohibited"
    assert verify_receipt(tampered)["valid"] is False
