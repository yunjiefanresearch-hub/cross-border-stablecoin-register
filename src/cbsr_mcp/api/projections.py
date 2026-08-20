"""Central public record serialization."""

from typing import Any, Mapping


def public_record_projection(record: Mapping[str, Any]) -> dict[str, Any]:
    source = record.get("source") or {}
    freshness = record.get("freshness") or {}
    return {
        "id": record.get("id"),
        "jurisdiction": record.get("jurisdiction"),
        "dimension": record.get("dimension"),
        "claim_class": record.get("claim_class"),
        "evidence_tier": record.get("evidence_tier") or "unverified",
        "binding_status": record.get("binding_status"),
        "legal_status": record.get("legal_status"),
        "status": record.get("status"),
        "instrument": source.get("primary") or record.get("instrument_label_local"),
        "pinpoint": source.get("pinpoint"),
        "url": source.get("url"),
        "source_disposition": record.get("source_disposition"),
        "source_check_status": record.get("source_check_status"),
        "source_last_checked": record.get("source_last_checked"),
        "next_review_due": record.get("next_review_due"),
        "review_status": freshness.get("review_status") or record.get("review_status"),
        "review_stage": record.get("review_stage"),
        "reviewer": record.get("reviewer"),
        "second_reviewer": record.get("second_reviewer"),
        "uncertainty": record.get("uncertainty"),
        "event_id": record.get("event_id"),
        "freshness": freshness,
    }
