#!/usr/bin/env python3
"""Cross-check deterministic research outputs against the compiled dataset."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from collections import Counter
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    dataset = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
    report = json.loads((ROOT / "research" / "quantitative_baseline.json").read_text(encoding="utf-8"))
    ledger = json.loads((ROOT / "research" / "source_ledger_2026-08-20.json").read_text(encoding="utf-8"))
    records = dataset.get("records", [])
    expected_jurisdictions = sorted({str(row.get("jurisdiction")) for row in records})
    errors = []

    if report.get("dataset_version") != dataset.get("version"):
        errors.append("research dataset_version does not match dataset.json")
    if report.get("as_of") != dataset.get("generated"):
        errors.append("research as_of does not match deterministic build date")
    if report.get("records") != len(records):
        errors.append("research record count does not match dataset.json")
    if report.get("jurisdictions") != len(expected_jurisdictions):
        errors.append("research jurisdiction count does not match dataset.json")
    if ledger.get("schema") != "cbsr/source-ledger/v2":
        errors.append("source ledger schema is not v2")
    ledger_rows = ledger.get("records", [])
    if len(ledger_rows) != len(records) or len({row.get("record_id") for row in ledger_rows}) != len(records):
        errors.append("source ledger is not a unique row-for-record census")
    required_ledger_fields = {
        "source_url", "pinpoint", "source_last_checked", "next_review_due", "review_status",
        "reviewer", "second_reviewer", "source_disposition", "uncertainty",
    }
    if any(not required_ledger_fields <= set(row) for row in ledger_rows):
        errors.append("source ledger omits required review/provenance fields")

    expected_freshness = dict(sorted(Counter(
        (row.get("freshness") or {}).get("review_status", "unknown") for row in records
    ).items()))
    if report.get("by_freshness") != expected_freshness:
        errors.append("research freshness distribution is stale")

    dossiers = ROOT / "research" / "jurisdictions"
    actual_dossiers = sorted(path.stem for path in dossiers.glob("*.md"))
    if actual_dossiers != expected_jurisdictions:
        errors.append(f"jurisdiction dossier set mismatch: {actual_dossiers} != {expected_jurisdictions}")
    for code in expected_jurisdictions:
        text = (dossiers / f"{code}.md").read_text(encoding="utf-8")
        count = sum(1 for row in records if row.get("jurisdiction") == code)
        if f"- Record population: {count}" not in text:
            errors.append(f"{code} dossier record count is stale")
        if len(text.splitlines()) < 100:
            errors.append(f"{code} dossier is an inventory stub rather than a substantive record matrix")
        if "## Line-by-line record matrix" not in text:
            errors.append(f"{code} dossier omits the line-by-line record matrix")
        if "## Release gate" not in text:
            errors.append(f"{code} dossier omits its legal-review release gate")

    if errors:
        print("research reproduction failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(
        f"research reproduction passed: {len(records)} records, "
        f"{len(expected_jurisdictions)} dossiers, freshness {expected_freshness}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
