"""Versioned legal-state ontology shared by research and build validation."""

from __future__ import annotations

from datetime import date
from typing import Any, Mapping

ONTOLOGY_VERSION = "cbsr/legal-event-ontology/v1"
LEGAL_STATES = (
    "consultation", "proposed", "enacted_not_commenced", "finalized_policy_pending",
    "operative", "prohibited", "no_regime", "superseded",
)
ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
    "consultation": ("proposed", "finalized_policy_pending", "superseded"),
    "proposed": ("enacted_not_commenced", "operative", "superseded"),
    "finalized_policy_pending": ("enacted_not_commenced", "operative", "superseded"),
    "enacted_not_commenced": ("operative", "superseded"),
    "operative": ("superseded", "prohibited"),
    "prohibited": ("proposed", "enacted_not_commenced", "operative", "superseded"),
    "no_regime": ("consultation", "proposed", "enacted_not_commenced", "operative"),
    "superseded": (),
}


def _date(value: Any) -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def validate_record_timeline(record: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    status = record.get("legal_status")
    if status not in LEGAL_STATES:
        errors.append(f"unknown legal_status {status!r}")
    start = _date(record.get("effective_from"))
    end = _date(record.get("effective_until"))
    if record.get("effective_from") and start is None:
        errors.append("effective_from is not an ISO date")
    if record.get("effective_until") and end is None:
        errors.append("effective_until is not an ISO date")
    if start and end and end <= start:
        errors.append("effective_until must be later than effective_from")
    if status in {"consultation", "proposed", "finalized_policy_pending", "no_regime"} and end:
        errors.append(f"{status} cannot carry effective_until as an operative interval")
    if status == "superseded" and not end:
        errors.append("superseded status requires effective_until")
    return errors


def transition_allowed(source: str, destination: str) -> bool:
    return destination in ALLOWED_TRANSITIONS.get(source, ())
