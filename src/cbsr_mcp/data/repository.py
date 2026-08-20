"""Offline repository for the one committed CBSR dataset."""

from __future__ import annotations

import json
import pathlib
from typing import Any


def load_dataset() -> dict[str, Any]:
    """Load packaged data first, then a source-checkout dataset; never use the network."""
    try:
        from importlib.resources import files

        packaged = files("cbsr_mcp").joinpath("data").joinpath("dataset.json")
        if packaged.is_file():
            return json.loads(packaged.read_text(encoding="utf-8"))
    except (ImportError, ModuleNotFoundError, FileNotFoundError, TypeError):
        pass
    here = pathlib.Path(__file__).resolve()
    for base in here.parents:
        candidate = base / "dataset.json"
        if candidate.is_file():
            return json.loads(candidate.read_text(encoding="utf-8"))
    raise RuntimeError("dataset.json not found; run `python build.py` or reinstall the wheel")


DATA = load_dataset()
RECORDS: list[dict[str, Any]] = DATA.get("records", [])
CORRIDORS: list[dict[str, Any]] = DATA.get("corridors", [])


def record_summary(record: dict[str, Any]) -> dict[str, Any]:
    """Compact public projection with provenance and review state."""
    source = record.get("source") or {}
    return {
        "id": record.get("id"),
        "jurisdiction": record.get("jurisdiction"),
        "dimension": record.get("dimension"),
        "constraint_ref": record.get("constraint_ref"),
        "requirement_summary": record.get("requirement_summary"),
        "source": {
            "primary": source.get("primary"),
            "pinpoint": source.get("pinpoint"),
            "url": source.get("url") or None,
            "disposition": record.get("source_disposition"),
        },
        "status": record.get("status"),
        "legal_status": record.get("legal_status"),
        "effective_date": record.get("effective_date"),
        "effective_from": record.get("effective_from"),
        "effective_until": record.get("effective_until"),
        "confidence": record.get("confidence"),
        "claim_class": record.get("claim_class"),
        "evidence_tier": record.get("evidence_tier", "unverified"),
        "binding_status": record.get("binding_status"),
        "last_reviewed": record.get("last_reviewed"),
        "source_last_checked": record.get("source_last_checked"),
        "source_check_status": record.get("source_check_status"),
        "next_review_due": record.get("next_review_due"),
        "review_status": record.get("review_status"),
        "review_stage": record.get("review_stage"),
        "reviewer": record.get("reviewer"),
        "second_reviewer": record.get("second_reviewer"),
        "freshness": record.get("freshness"),
        "event_id": record.get("event_id"),
        "version_added": record.get("version_added"),
    }
