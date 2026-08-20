"""Typed AgenticFi decision-support tools."""
from __future__ import annotations
import json
from typing import Optional
from ..core.catalog import DIMENSIONS, JURISDICTIONS
from ..core.errors import error
from ..data.repository import DATA, RECORDS, record_summary
from ..domain_packs.stablecoin import STABLECOIN_PACK
from ..policy import evaluate_policy
from ..receipts import create_receipt, verify_receipt
from .architecture import EVENT_CALENDAR
from .registry import tool
_summary = record_summary


@tool
def search_evidence(keyword: str, jurisdiction: Optional[str] = None, limit: int = 20) -> dict:
    """Search provenance-bearing regulatory evidence for an AgenticFi decision."""
    needle = keyword.strip().lower()
    if not needle:
        return {**error("invalid_keyword", "keyword must not be empty"), "count": 0, "records": []}
    j = jurisdiction.upper() if jurisdiction else None
    rows = []
    for record in RECORDS:
        if j and record.get("jurisdiction") != j:
            continue
        if needle in json.dumps(record, ensure_ascii=False).lower():
            rows.append(_summary(record))
    safe_limit = max(1, min(int(limit), 100))
    return {"keyword": keyword, "jurisdiction": j, "count": len(rows), "records": rows[:safe_limit]}


@tool
def get_rule(record_id: str) -> dict:
    """Return one rule with legal force, provenance, freshness, and decision-use warnings."""
    for record in RECORDS:
        if record.get("id") != record_id:
            continue
        freshness = record.get("freshness") or {}
        operative = record.get("binding_status") == "in_force_enacted"
        return {
            "record": record,
            "decision_use": {
                "operative": operative,
                "unconditional_allow_eligible": (
                    operative
                    and freshness.get("review_status") == "current"
                    and record.get("review_stage") == "reconciled"
                    and record.get("source_disposition") == "official"
                ),
                "warnings": [
                    warning for warning, applies in (
                        ("evidence is not current", freshness.get("review_status") != "current"),
                        ("instrument is not operative positive law", not operative),
                        ("evidence is not official resolution text", record.get("evidence_tier") != "resolution_text"),
                        ("independent second review is incomplete", record.get("review_stage") != "reconciled"),
                        ("source disposition is not official", record.get("source_disposition") != "official"),
                    ) if applies
                ],
            },
        }
    return error("record_not_found", f"No record with id '{record_id}'.", record_id=record_id)


@tool
def evaluate_action(action: dict) -> dict:
    """Evaluate, but never execute, an action against its mandate and applicable CBSR evidence."""
    origin = str(action.get("origin") or "").upper()
    destination = str(action.get("destination") or "").upper()
    dimensions = set(action.get("required_dimensions") or STABLECOIN_PACK.default_dimensions)
    evidence = [
        record for record in RECORDS
        if record.get("jurisdiction") in {origin, destination}
        and record.get("dimension") in dimensions
    ]
    as_of = str(action.get("as_of") or DATA.get("generated") or "2026-08-20")
    decision = evaluate_policy(action, evidence, as_of, known_record_ids={str(row.get("id")) for row in RECORDS})
    receipt = create_receipt(action, decision, str(DATA.get("version")))
    return {
        "decision": decision,
        "receipt": receipt,
        "notice": "Decision support only. execution_authorized is always false; no transaction was sent.",
    }


@tool
def compare_jurisdictions(left: str, right: str, dimensions: Optional[list[str]] = None) -> dict:
    """Compare two jurisdictions on requested dimensions with freshness and evidence gaps visible."""
    a, b = left.upper(), right.upper()
    requested = dimensions or list(DIMENSIONS)
    if a not in JURISDICTIONS or b not in JURISDICTIONS:
        return error("unknown_jurisdiction", "unknown jurisdiction", valid=sorted(JURISDICTIONS))
    rows = []
    for dimension in requested:
        sides = {}
        for code in (a, b):
            sides[code] = [
                _summary(record) for record in RECORDS
                if record.get("jurisdiction") == code and record.get("dimension") == dimension
            ]
        rows.append({"dimension": dimension, "jurisdictions": sides, "gap": not sides[a] or not sides[b]})
    return {"left": a, "right": b, "count": len(rows), "comparisons": rows}


@tool
def watch_changes(since: Optional[str] = None, jurisdiction: Optional[str] = None) -> dict:
    """Return records needing review plus dated/contingent regulatory events; no network polling."""
    j = jurisdiction.upper() if jurisdiction else None
    records_due = []
    for record in RECORDS:
        if j and record.get("jurisdiction") != j:
            continue
        freshness = record.get("freshness") or {}
        if freshness.get("review_status") in {"due_for_review", "stale", "unknown"}:
            if since and str(freshness.get("source_last_checked") or "") < since:
                continue
            records_due.append(_summary(record))
    events = []
    for event in EVENT_CALENDAR.get("events", []):
        if j and event.get("jurisdiction") != j:
            continue
        event_date = event.get("effective_date") or event.get("as_of")
        if since and event_date and str(event_date) < since:
            continue
        events.append(event)
    return {
        "mode": "offline_snapshot",
        "since": since,
        "jurisdiction": j,
        "records_needing_review": records_due,
        "events": events,
        "notice": "This tool reads the packaged snapshot; refresh requires a researched repository update.",
    }


@tool
def audit_decision(receipt: dict) -> dict:
    """Recompute a receipt hash and report tampering; does not imply a digital signature."""
    return verify_receipt(receipt)
