"""Receipt completeness, schema and mutation/negative tests."""

from __future__ import annotations

from copy import deepcopy
import json
import pathlib

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from cbsr_mcp.domain_packs.stablecoin import STABLECOIN_PACK
from cbsr_mcp.policy import evaluate_policy
from cbsr_mcp.receipts import create_receipt, verify_receipt
from test_agenticfi_scenarios import base_action, base_evidence

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _receipt() -> dict:
    action = base_action()
    decision = evaluate_policy(action, [base_evidence()], "2026-08-20", known_record_ids={"rule-1"})
    return create_receipt(action, decision, "0.11.0")


def test_all_public_policy_schemas_accept_the_reference_objects():
    mandate_schema = json.loads((ROOT / "schemas/policy-mandate.v1.schema.json").read_text(encoding="utf-8"))
    action_schema = json.loads((ROOT / "schemas/policy-action.v1.schema.json").read_text(encoding="utf-8"))
    decision_schema = json.loads((ROOT / "schemas/policy-decision.v1.schema.json").read_text(encoding="utf-8"))
    receipt_schema = json.loads((ROOT / "schemas/policy-receipt.v1.schema.json").read_text(encoding="utf-8"))
    pack_schema = json.loads((ROOT / "schemas/domain-pack.v1.schema.json").read_text(encoding="utf-8"))
    action = base_action()
    decision = evaluate_policy(action, [base_evidence()], "2026-08-20", known_record_ids={"rule-1"})
    receipt = create_receipt(action, decision, "0.11.0")
    registry = Registry().with_resource(mandate_schema["$id"], Resource.from_contents(mandate_schema))
    Draft202012Validator(action_schema, registry=registry).validate(action)
    Draft202012Validator(mandate_schema).validate(action["mandate"])
    Draft202012Validator(decision_schema).validate(decision)
    Draft202012Validator(receipt_schema).validate(receipt)
    Draft202012Validator(pack_schema).validate(STABLECOIN_PACK.to_manifest())


def test_committed_domain_pack_manifest_matches_runtime_pack():
    committed = json.loads(
        (ROOT / "src/cbsr_mcp/domain_packs/stablecoin/manifest.json").read_text(encoding="utf-8")
    )
    assert committed == STABLECOIN_PACK.to_manifest()


def test_receipt_contains_the_complete_evidence_chain_and_is_deterministic():
    first = _receipt()
    second = _receipt()
    assert first == second
    assert first["generated_at"] == "2026-08-20T10:00:00Z"
    assert first["applicable_rules"][0]["record_id"] == "rule-1"
    assert first["source_urls"] == ["https://example.gov/rule-1"]
    assert first["freshness_snapshot"]["current"] == 1
    assert first["mandate"]["version"] == "1.0"
    assert first["engine_version"] == "cbsr-policy-engine/1.1.0"
    assert first["ruleset_version"] == "cbsr-stablecoin-rules/1.1.0"
    assert verify_receipt(first)["valid"] is True


def test_receipt_mutations_all_fail_closed():
    paths = [
        ("action", "amount"),
        ("decision", "outcome"),
        ("applicable_rules", 0),
        ("source_urls", 0),
        ("freshness_snapshot", "current"),
        ("assumptions", 0),
        ("mandate", "version"),
        ("audit_identity", "subject_id"),
        ("engine_version",),
        ("ruleset_version",),
        ("generated_at",),
    ]
    for path in paths:
        candidate = deepcopy(_receipt())
        cursor = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        key = path[-1]
        if isinstance(cursor, list):
            cursor[key] = {"tampered": True} if isinstance(cursor[key], dict) else "tampered"
        elif isinstance(cursor[key], int):
            cursor[key] += 1
        else:
            cursor[key] = "tampered"
        assert verify_receipt(candidate)["valid"] is False, path


def test_component_hashes_identify_action_and_decision_tampering():
    action_tamper = deepcopy(_receipt())
    action_tamper["action"]["amount"] = "999"
    checked = verify_receipt(action_tamper)
    assert checked["action_hash_valid"] is False
    decision_tamper = deepcopy(_receipt())
    decision_tamper["decision"]["outcome"] = "prohibited"
    checked = verify_receipt(decision_tamper)
    assert checked["decision_hash_valid"] is False
