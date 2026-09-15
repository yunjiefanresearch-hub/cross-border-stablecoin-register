#!/usr/bin/env python3
"""Persist conservative review/temporal metadata in every source record YAML.

The migration is mechanical. It never invents a source check or reviewer: a source check date
is copied only when an existing verification entry identifies the same URL. Missing evidence
tiers become ``unverified`` rather than being guessed.
"""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse
from datetime import date, datetime, timedelta
import json
import pathlib
from urllib.parse import urlparse

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
AS_OF = date.fromisoformat("2026-08-20")
SLA_DAYS = {
    "pending_proposal": 7,
    "no_regime": 7,
    "made_not_commenced": 14,
    "finalized_policy_pending": 14,
    "in_force_enacted": 30,
    "prohibition": 30,
}
OFFICIAL_DOMAINS = {
    "bcb.gov.br", "csrc.gov.cn", "elegislation.gov.hk", "english.ey.gov.tw",
    "eur-lex.europa.eu", "federalregister.gov", "fedlex.admin.ch", "finma.ch",
    "congress.gov", "fca.org.uk", "bankofengland.co.uk", "law.go.kr",
    "law.moj.gov.tw", "lawmaking.go.kr", "president.gov.tw",
    "laws.e-gov.go.jp", "legislation.gov.uk", "mas.gov.sg", "planalto.gov.br",
    "rulebook.centralbank.ae",
}
LEGAL_STATUS = {
    "in_force_enacted": "operative",
    "made_not_commenced": "enacted_not_commenced",
    "finalized_policy_pending": "finalized_policy_pending",
    "pending_proposal": "proposed",
    "prohibition": "prohibited",
    "no_regime": "no_regime",
}
FIELDS = (
    "evidence_tier", "source_last_checked", "next_review_due", "review_status",
    "reviewer", "second_reviewer", "review_stage", "reconciliation_status",
    "review_disagreement", "source_disposition", "source_check_status",
    "effective_from", "effective_until", "event_id", "legal_status", "uncertainty",
)


def _normalize(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def _event_map() -> dict[str, str]:
    path = ROOT / "analysis" / "event_calendar.json"
    if not path.is_file():
        return {}
    calendar = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    for event in calendar.get("events", []):
        for record_id in event.get("records", []):
            result.setdefault(str(record_id), str(event.get("id")))
    return result


def _disposition(url: str | None) -> str:
    if not url:
        return "unavailable"
    host = (urlparse(url).hostname or "").lower()
    if any(host == domain or host.endswith("." + domain) for domain in OFFICIAL_DOMAINS):
        return "official"
    return "secondary"


def _expected(record: dict, events: dict[str, str]) -> dict:
    source = record.get("source") or {}
    verification = record.get("verification") or {}
    against = verification.get("against") or {}
    url = source.get("url")
    checked = None
    if url and against.get("url") == url and verification.get("verified_on"):
        checked = str(verification["verified_on"])
    binding = str(record.get("binding_status") or "")
    due = None
    status = "unknown"
    if checked:
        due_date = date.fromisoformat(checked) + timedelta(days=SLA_DAYS.get(binding, 30))
        due = due_date.isoformat()
        overdue = (AS_OF - due_date).days
        status = "current" if overdue <= 0 else "due_for_review" if overdue <= 7 else "stale"
    reviewer = verification.get("verified_by") or None
    disposition = _disposition(url)
    tier = record.get("evidence_tier") or "unverified"
    legal_status = LEGAL_STATUS.get(binding, "proposed")
    if record.get("status") == "consultation":
        legal_status = "consultation"
    return {
        "evidence_tier": tier,
        "source_last_checked": checked,
        "next_review_due": due,
        "review_status": status,
        "reviewer": reviewer,
        "second_reviewer": None,
        "review_stage": "primary_reviewed_second_pending" if reviewer else "unreviewed",
        "reconciliation_status": "not_started",
        "review_disagreement": None,
        "source_disposition": disposition,
        "source_check_status": (
            "checked" if checked else "source_unavailable" if disposition == "unavailable" else "not_checked"
        ),
        "effective_from": record.get("effective_date"),
        "effective_until": None,
        "event_id": events.get(str(record.get("id"))),
        "legal_status": legal_status,
        "uncertainty": "low" if tier == "resolution_text" else "medium" if tier == "mixed" else "high",
    }


def _record_files() -> list[pathlib.Path]:
    paths = []
    for path in sorted(ROOT.rglob("*.yaml")):
        if path.name == "_TEMPLATE.yaml":
            continue
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and "jurisdiction" in value and "dimension" in value and "corridor_id" not in value:
            paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    events = _event_map()
    failures: list[str] = []
    changed = 0
    paths = _record_files()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        record = _normalize(yaml.safe_load(text))
        expected = _expected(record, events)
        missing = [field for field in FIELDS if field not in record]
        mismatches = [field for field in FIELDS if field in record and record.get(field) != expected[field]]
        if not missing and not mismatches:
            continue
        if args.check:
            failures.append(f"{path.name}: missing={','.join(missing)} mismatch={','.join(mismatches)}")
            continue
        if mismatches:
            failures.append(f"{path.name}: review metadata conflicts with deterministic migration ({', '.join(mismatches)})")
            continue
        additions = {field: expected[field] for field in missing}
        block = yaml.safe_dump(additions, allow_unicode=True, sort_keys=False, default_flow_style=False).rstrip()
        path.write_text(
            text.rstrip() + "\n\n# CBSR v0.11 review/temporal metadata (mechanically migrated; null means not evidenced)\n"
            + block + "\n",
            encoding="utf-8", newline="\n",
        )
        changed += 1
    if len(paths) != 152:
        failures.append(f"expected 152 source records, found {len(paths)}")
    if failures:
        print("review-field migration failed:")
        for failure in failures[:30]:
            print("  -", failure)
        return 1
    print(f"review-field migration {'check passed' if args.check else 'completed'}: {len(paths)} records, {changed} changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
