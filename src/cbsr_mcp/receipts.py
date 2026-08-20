"""Canonical, tamper-evident and evidence-complete decision receipts."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.

import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from typing import Any, Mapping

from .serialization.canonical import sha256_digest


def _generated_at(action: Mapping[str, Any], decision: Mapping[str, Any]) -> str:
    explicit = action.get("requested_at") or decision.get("evaluated_at")
    if explicit:
        return str(explicit)
    as_of = action.get("as_of") or (decision.get("freshness_snapshot") or {}).get("as_of") or "1970-01-01"
    return f"{str(as_of)[:10]}T00:00:00Z"


def create_receipt(action: Mapping[str, Any], decision: Mapping[str, Any], dataset_version: str) -> dict[str, Any]:
    mandate = action.get("mandate") if isinstance(action.get("mandate"), Mapping) else {}
    audit_identity = mandate.get("audit_identity") if isinstance(mandate.get("audit_identity"), Mapping) else {}
    action_value = dict(action)
    decision_value = dict(decision)
    component_digests = {
        "action_sha256": sha256_digest(action_value),
        "decision_sha256": sha256_digest(decision_value),
    }
    payload = {
        "schema": "cbsr/decision-receipt/v1",
        "dataset_version": dataset_version,
        "receipt_id": "",
        "generated_at": _generated_at(action, decision),
        "requested_as_of": decision.get("requested_as_of") or action.get("as_of"),
        "non_legal_advice_notice": decision.get("non_legal_advice_notice"),
        "action": action_value,
        "decision": decision_value,
        "applicable_rules": list(decision.get("applicable_rules") or []),
        "source_urls": list(decision.get("source_urls") or []),
        "freshness_snapshot": dict(decision.get("freshness_snapshot") or {}),
        "assumptions": list(decision.get("assumptions") or []),
        "uncertainty": decision.get("uncertainty") or "unknown",
        "mandate": {
            "mandate_id": mandate.get("mandate_id"),
            "version": mandate.get("version"),
            "issued_by": mandate.get("issued_by"),
        },
        "audit_identity": dict(audit_identity),
        "engine_version": decision.get("engine_version"),
        "ruleset_version": decision.get("ruleset_version"),
        "component_digests": component_digests,
        "signing_state": "unsigned",
        "execution_authorized": False,
    }
    payload["receipt_id"] = "cbsr-receipt-" + sha256_digest(payload)[:24]
    return {**payload, "sha256": sha256_digest(payload)}


def verify_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    supplied = receipt.get("sha256")
    payload = {key: value for key, value in receipt.items() if key != "sha256"}
    computed = sha256_digest(payload)
    component = receipt.get("component_digests") or {}
    action_valid = component.get("action_sha256") == sha256_digest(receipt.get("action") or {})
    decision_valid = component.get("decision_sha256") == sha256_digest(receipt.get("decision") or {})
    valid = bool(supplied) and supplied == computed and action_valid and decision_valid
    return {
        "valid": valid,
        "receipt_hash_valid": bool(supplied) and supplied == computed,
        "action_hash_valid": action_valid,
        "decision_hash_valid": decision_valid,
        "supplied_sha256": supplied,
        "computed_sha256": computed,
        "signing_state": receipt.get("signing_state", "unknown"),
        "warning": "Integrity only; this receipt is not digitally signed and proves no author identity.",
    }
