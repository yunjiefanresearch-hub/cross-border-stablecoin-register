#!/usr/bin/env python3
"""Build the full 152-record temporal ontology and reciprocal event-link audit."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from cbsr_mcp.events.ontology import (  # noqa: E402
    ALLOWED_TRANSITIONS, LEGAL_STATES, ONTOLOGY_VERSION, validate_record_timeline,
)


def main() -> int:
    calendar = json.loads((ROOT / "analysis" / "event_calendar.json").read_text(encoding="utf-8"))
    events = {str(event["id"]): event for event in calendar.get("events", [])}
    rows = []
    reciprocal_errors = []
    for path in sorted(ROOT.glob("*.yaml")):
        if path.name == "_TEMPLATE.yaml":
            continue
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict) or "jurisdiction" not in record or "dimension" not in record or "corridor_id" in record:
            continue
        event_id = record.get("event_id")
        issues = validate_record_timeline(record)
        if event_id:
            event = events.get(str(event_id))
            if not event:
                issues.append("event_id does not exist in event_calendar")
            elif record.get("id") not in event.get("records", []):
                issues.append("event_calendar does not reciprocally reference record")
        rows.append({
            "record_id": record.get("id"),
            "jurisdiction": record.get("jurisdiction"),
            "dimension": record.get("dimension"),
            "legal_status": record.get("legal_status"),
            "effective_from": str(record.get("effective_from")) if record.get("effective_from") else None,
            "effective_until": str(record.get("effective_until")) if record.get("effective_until") else None,
            "event_id": event_id,
            "validation": "valid" if not issues else "invalid",
            "issues": issues,
        })
        reciprocal_errors.extend(f"{record.get('id')}: {issue}" for issue in issues)
    artifact = {
        "schema": ONTOLOGY_VERSION,
        "as_of": "2026-08-20",
        "states": list(LEGAL_STATES),
        "allowed_transitions": {key: list(value) for key, value in ALLOWED_TRANSITIONS.items()},
        "date_rules": [
            "effective_until must be later than effective_from",
            "proposed/consultation/finalized-policy/no-regime states do not form closed operative intervals",
            "superseded requires effective_until",
            "event links are reciprocal between source records and event_calendar",
        ],
        "coverage": {
            "records": len(rows),
            "linked_to_first_class_event": sum(bool(row["event_id"]) for row in rows),
            "without_first_class_event": sum(not row["event_id"] for row in rows),
            "invalid": sum(row["validation"] == "invalid" for row in rows),
        },
        "records": rows,
        "limitations": (
            "A null event_id means no event has been modelled for that record; it is not evidence that no legal event exists."
        ),
    }
    path = ROOT / "analysis" / "legal_event_ontology.json"
    path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}: {len(rows)} records, {len(reciprocal_errors)} validation issue(s)")
    return 1 if reciprocal_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
