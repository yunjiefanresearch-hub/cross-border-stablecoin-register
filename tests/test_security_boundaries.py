"""Automated fail-closed regression tests for public input and repository gates.

These checks exercise software boundaries only; they are not human, legal, or
independent-review evidence.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from cbsr_mcp.policy import evaluate_policy
from cbsr_mcp.receipts import verify_receipt
from cbsr_mcp.tools import agentic, architecture
from tools import check_internal_links, check_verification_backlog


ROOT = Path(__file__).resolve().parent.parent


def _action() -> dict:
    return {
        "schema": "cbsr/policy-action/v1",
        "action_id": "security-boundary-action",
        "origin": "US",
        "destination": "EU",
        "asset": "USDC",
        "amount": "100",
        "actor": "test-agent",
        "as_of": "2026-08-20",
        "requested_at": "2026-08-20T10:00:00Z",
        "mandate": {
            "schema": "cbsr/policy-mandate/v1",
            "mandate_id": "security-boundary-mandate",
            "version": "1.0",
            "issued_by": "test-owner",
            "active": True,
            "revoked": False,
            "human_review": {"required": False},
            "audit_identity": {"subject_id": "agent:test", "actor_type": "agent"},
        },
    }


def _evidence(**overrides: object) -> dict:
    row = {
        "id": "eu-security-boundary-rule",
        "jurisdiction": "EU",
        "dimension": "issuer_pathway",
        "status": "in_force",
        "binding_status": "in_force_enacted",
        "evidence_tier": "resolution_text",
        "freshness": {"review_status": "current"},
        "review_stage": "reconciled",
        "source_disposition": "official",
        "source": {"url": "https://example.invalid/rule"},
    }
    row.update(overrides)
    return row


def _set_nested(value: dict, path: tuple[str, ...], replacement: object) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


@pytest.mark.parametrize("amount", ["NaN", "Infinity", "-Infinity"])
def test_non_finite_amounts_fail_closed_without_an_exception(amount: str):
    candidate = _action()
    candidate["amount"] = amount
    result = evaluate_policy(candidate, [_evidence()], "2026-08-20")
    assert result["outcome"] == "insufficient_evidence"
    assert result["execution_authorized"] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("mandate", "active"), 0),
        (("mandate", "revoked"), 1),
        (("mandate", "human_review", "required"), 1),
        (("requires_kyc",), 1),
    ],
)
def test_numeric_values_cannot_bypass_boolean_policy_controls(
    path: tuple[str, ...], replacement: object
):
    candidate = _action()
    _set_nested(candidate, path, replacement)
    result = evaluate_policy(candidate, [_evidence()], "2026-08-20")
    assert result["outcome"] == "insufficient_evidence"
    assert result["execution_authorized"] is False


@pytest.mark.parametrize(
    ("path", "replacement"),
    [
        (("required_dimensions",), "issuer_pathway"),
        (("mandate", "assets"), "USDC"),
        (("mandate", "human_review", "jurisdictions"), "US"),
        (("mandate", "audit_identity", "authentication_context"), "mfa"),
    ],
)
def test_scalar_values_cannot_smuggle_through_array_fields(
    path: tuple[str, ...], replacement: object
):
    candidate = _action()
    _set_nested(candidate, path, replacement)
    result = evaluate_policy(candidate, [_evidence()], "2026-08-20")
    assert result["outcome"] == "insufficient_evidence"
    assert result["execution_authorized"] is False


@pytest.mark.parametrize(
    "bad_evidence",
    [
        None,
        _evidence(source="not-an-object"),
        _evidence(freshness="not-an-object"),
    ],
)
def test_malformed_evidence_fails_closed_without_an_exception(bad_evidence: object):
    result = evaluate_policy(_action(), [bad_evidence], "2026-08-20")
    assert result["outcome"] == "insufficient_evidence"
    assert result["execution_authorized"] is False


def test_public_evaluate_action_rejects_a_non_array_dimension_filter():
    candidate = _action()
    candidate["required_dimensions"] = 42
    result = agentic.evaluate_action(candidate)
    assert result["decision"]["outcome"] == "insufficient_evidence"
    assert result["decision"]["execution_authorized"] is False


@pytest.mark.parametrize(
    "bad_date", ["not-a-date", "2026-13-99", "../../etc/passwd", "2026-08-20junk"]
)
def test_date_aware_corridor_command_rejects_non_iso_dates(bad_date: str):
    result = architecture.compose_corridor("US", "EU", as_of=bad_date)
    assert "error" in result


@pytest.mark.parametrize("component_digests", [[1], "not-an-object"])
def test_receipt_verification_rejects_malformed_component_digests(component_digests: object):
    result = verify_receipt(
        {
            "sha256": "not-a-valid-digest",
            "action": {},
            "decision": {},
            "component_digests": component_digests,
        }
    )
    assert result["valid"] is False
    assert result["action_hash_valid"] is False
    assert result["decision_hash_valid"] is False


@pytest.mark.parametrize("target", ["../../outside.md", "%2e%2e/%2e%2e/outside.md"])
def test_internal_link_gate_rejects_paths_that_escape_the_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, target: str
):
    repository = tmp_path / "repository"
    docs = repository / "docs"
    docs.mkdir(parents=True)
    (tmp_path / "outside.md").write_text("outside\n", encoding="utf-8", newline="\n")
    (docs / "page.md").write_text(
        f"[must not escape]({target})\n", encoding="utf-8", newline="\n"
    )
    monkeypatch.setattr(check_internal_links, "ROOT", repository)
    with pytest.raises(SystemExit):
        check_internal_links.main()


@pytest.mark.parametrize(
    ("field", "replacement"),
    [("status_values", None), ("items", "not-an-array")],
)
def test_backlog_validator_reports_wrong_collection_types(field: str, replacement: object):
    document = {
        "schema": "cbsr/verification-backlog/v1",
        "version": "1",
        "generated": "2026-08-20",
        "discipline": "test",
        "status_values": ["open"],
        "items": [],
    }
    document[field] = replacement
    assert check_verification_backlog.validate(document)


@pytest.mark.parametrize("as_of", ["20260820", "2026-W34-4", "2026-08-20junk"])
def test_policy_date_contract_is_consistent_across_python_versions(as_of: str):
    result = evaluate_policy(_action(), [_evidence()], as_of)
    assert result["outcome"] == "insufficient_evidence"
    assert "invalid_as_of_date" in result["reasons"]


def _workflow(name: str) -> dict:
    return yaml.load(
        (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )


def test_repaired_workflows_keep_their_security_and_release_boundaries():
    build_text = (ROOT / ".github/workflows/build.yml").read_text(encoding="utf-8")
    assert "runner.temp" not in build_text
    assert build_text.count("RUNNER_TEMP") == 6

    security = _workflow("security.yml")
    secret_scan = security["jobs"]["secret-scan"]
    assert secret_scan["steps"][-1]["env"]["GITHUB_TOKEN"] == "${{ secrets.GITHUB_TOKEN }}"
    assert secret_scan.get("permissions") is None
    assert security["jobs"]["scorecard"]["permissions"] == {
        "contents": "read",
        "security-events": "write",
        "id-token": "write",
    }

    release = _workflow("release-provenance.yml")
    publish = release["jobs"]["publish-release-assets"]
    assert publish["if"] == "github.event_name == 'release'"
    assert "workflow_dispatch" in release["on"]
    upload_command = publish["steps"][-1]["run"]
    assert "--clobber" not in upload_command
    assert '--repo "$GH_REPO"' in upload_command
    assert publish["permissions"] == {"actions": "read", "contents": "write"}


def test_repository_attributes_and_critical_outputs_are_lf_stable():
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "* text=auto eol=lf" in attributes
    for pattern in ("*.pdf binary", "*.png binary", "*.whl binary", "*.zip binary"):
        assert pattern in attributes

    critical_text = [
        ".github/workflows/build.yml",
        ".github/workflows/security.yml",
        ".github/workflows/release-provenance.yml",
        "tools/research_report.py",
        "tools/research_deliverables.py",
        "tools/delivery_report.py",
        "tools/governance_report.py",
        "research/research_manifest.json",
        "delivery/delivery_manifest.json",
    ]
    for relative in critical_text:
        assert b"\r" not in (ROOT / relative).read_bytes(), relative
