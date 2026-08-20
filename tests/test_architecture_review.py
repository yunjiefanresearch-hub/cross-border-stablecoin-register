import json
import pathlib

from jsonschema import Draft202012Validator

from cbsr_mcp import server
from cbsr_mcp.api.projections import public_record_projection
from cbsr_mcp.events.ontology import transition_allowed, validate_record_timeline
from cbsr_mcp.tools import architecture, register, research, agentic  # noqa: F401
from cbsr_mcp.tools.registry import definitions, metadata

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_source_tests_import_the_checkout_not_a_previously_installed_wheel():
    import cbsr_mcp

    assert pathlib.Path(cbsr_mcp.__file__).resolve().is_relative_to(ROOT / "src")


def test_tool_registry_is_the_complete_metadata_source():
    specs = definitions()
    assert len(specs) == len({item.name for item in specs})
    assert len(specs) == len(server.mcp._tool_manager._tools)
    assert {"search_evidence", "get_rule", "evaluate_action", "compare_jurisdictions", "watch_changes", "audit_decision"} <= {item.name for item in specs}
    assert all(item.summary and item.signature and item.module for item in specs)
    manifest = json.loads((ROOT / "mcp.json").read_text(encoding="utf-8"))
    assert manifest["tools"] == metadata()


def test_legacy_server_data_symbols_remain_compatible_aliases():
    from cbsr_mcp.core.catalog import DIMENSIONS
    from cbsr_mcp.data.repository import CORRIDORS, DATA, RECORDS

    assert server.DATA is DATA
    assert server.RECORDS is RECORDS
    assert server.CORRIDORS is CORRIDORS
    assert server.DIMENSIONS is DIMENSIONS
    assert len(server.RECORDS) == 152


def test_source_ledger_covers_every_record_without_fake_second_review():
    ledger = json.loads((ROOT / "research" / "source_ledger_2026-08-20.json").read_text(encoding="utf-8"))
    assert ledger["schema"] == "cbsr/source-ledger/v2"
    assert len(ledger["records"]) == 152
    assert len({row["record_id"] for row in ledger["records"]}) == 152
    assert ledger["counts"]["second_reviewer_present"] == 0
    required = {
        "source_url", "pinpoint", "source_last_checked", "next_review_due", "review_status",
        "reviewer", "second_reviewer", "source_disposition", "uncertainty",
    }
    assert all(required <= set(row) for row in ledger["records"])


def test_static_api_exposes_review_and_temporal_state():
    payload = json.loads((ROOT / "api" / "records.json").read_text(encoding="utf-8"))
    assert len(payload["data"]) == 152
    required = {
        "freshness", "source_disposition", "source_check_status", "source_last_checked", "next_review_due",
        "review_status", "review_stage", "reviewer", "second_reviewer", "legal_status",
    }
    assert all(required <= set(row) for row in payload["data"])


def test_public_projection_keeps_legal_status_separate_from_source_disposition():
    value = public_record_projection({
        "id": "x", "source": {}, "legal_status": "prohibited",
        "source_disposition": "unavailable", "freshness": {"review_status": "unknown"},
    })
    assert value["legal_status"] == "prohibited"
    assert value["source_disposition"] == "unavailable"


def test_source_check_status_is_exposed_in_static_and_mcp_projections():
    source_record = {
        "id": "x", "source": {}, "source_check_status": "not_checked",
        "source_disposition": "official", "freshness": {"review_status": "unknown"},
    }
    assert public_record_projection(source_record)["source_check_status"] == "not_checked"

    from cbsr_mcp.data.repository import record_summary

    assert record_summary(source_record)["source_check_status"] == "not_checked"


def test_policy_decision_schema_accepts_real_decision():
    from cbsr_mcp.policy import evaluate_policy

    action_value = {
        "action_id": "a", "origin": "US", "destination": "EU", "asset": "USDC",
        "amount": "1", "actor": "agent",
        "mandate": {
            "schema": "cbsr/policy-mandate/v1", "mandate_id": "m-1", "version": "1.0",
            "issued_by": "test-owner", "active": True, "valid_from": "2026-01-01",
            "valid_until": "2027-01-01", "jurisdictions": ["US", "EU"],
            "prohibited_jurisdictions": [], "human_review": {"required": False},
            "audit_identity": {"subject_id": "agent:test", "actor_type": "agent"},
        },
    }
    evidence = [{
        "id": "eu-emt-issuer_pathway-001", "jurisdiction": "EU", "dimension": "issuer_pathway",
        "status": "in_force", "binding_status": "in_force_enacted", "evidence_tier": "resolution_text",
        "review_stage": "reconciled", "freshness": {"review_status": "current"},
        "source": {"url": "https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng"},
    }]
    decision = evaluate_policy(action_value, evidence, "2026-08-20")
    schema = json.loads((ROOT / "schemas" / "policy-decision.v1.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(decision)
    assert decision["requested_as_of"] == "2026-08-20"
    assert decision["execution_authorized"] is False
    assert "not legal advice" in decision["non_legal_advice_notice"].lower()


def test_legal_event_ontology_has_full_record_coverage_and_valid_dates():
    value = json.loads((ROOT / "analysis" / "legal_event_ontology.json").read_text(encoding="utf-8"))
    assert value["coverage"]["records"] == 152
    assert value["coverage"]["invalid"] == 0
    assert transition_allowed("proposed", "enacted_not_commenced")
    assert not transition_allowed("operative", "proposed")
    assert validate_record_timeline({
        "legal_status": "operative", "effective_from": "2026-01-01", "effective_until": "2025-01-01"
    }) == ["effective_until must be later than effective_from"]


def test_server_is_only_a_thin_composition_root():
    source = (ROOT / "src" / "cbsr_mcp" / "server.py").read_text(encoding="utf-8")
    assert len(source.splitlines()) <= 80
    assert "def evaluate_action" not in source
    assert "bind(mcp)" in source
