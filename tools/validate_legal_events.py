#!/usr/bin/env python3
"""Hard gate for the generated record-level legal-event ontology."""

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    value = json.loads((ROOT / "analysis" / "legal_event_ontology.json").read_text(encoding="utf-8"))
    failures = []
    if value.get("schema") != "cbsr/legal-event-ontology/v1":
        failures.append("wrong schema")
    if value.get("coverage", {}).get("records") != 152:
        failures.append("ontology does not cover 152 records")
    invalid = [row for row in value.get("records", []) if row.get("validation") != "valid"]
    if invalid:
        failures.append(f"{len(invalid)} invalid record timelines")
    if failures:
        print("legal-event validation failed:", "; ".join(failures))
        return 1
    print(
        "legal-event ontology valid: 152 records; "
        f"{value['coverage']['linked_to_first_class_event']} linked, "
        f"{value['coverage']['without_first_class_event']} explicit ontology gaps"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
