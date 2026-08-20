"""Deterministic freshness classification for CBSR records.

Freshness is deliberately derived, not asserted by the build.  A successful build never upgrades
the legal status of a record and never turns an old review into a current one.  Consumers receive
the same classification for the same record and ``as_of`` date, including an explicit overdue age.
"""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from collections import Counter
from datetime import date, timedelta
from typing import Iterable, Mapping, Any

from .evidence.review import SOURCE_DISPOSITIONS

DEFAULT_AS_OF = "2026-08-20"

# Fast-moving, not-yet-operative material needs a shorter review cycle than settled official text.
SLA_DAYS = {
    "pending_proposal": 7,
    "no_regime": 7,
    "made_not_commenced": 14,
    "finalized_policy_pending": 14,
    "in_force_enacted": 30,
    "prohibition": 30,
}


def _iso(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def source_disposition(record: Mapping[str, Any]) -> str:
    """Return the persisted source classification, never a legal-force classification."""
    value = str(record.get("source_disposition") or "unavailable")
    return value if value in SOURCE_DISPOSITIONS else "unavailable"


def derive_freshness(record: Mapping[str, Any], as_of: str = DEFAULT_AS_OF) -> dict[str, Any]:
    """Derive review status from committed dates; never mutates ``record``."""
    today = _iso(as_of)
    if today is None:
        raise ValueError("as_of must be an ISO date (YYYY-MM-DD)")
    # last_reviewed is editorial metadata and is deliberately NOT a substitute for evidence
    # that the linked source was opened. This prevents an editorial pass from manufacturing
    # fresh legal evidence.
    checked_text = record.get("source_last_checked")
    checked = _iso(str(checked_text)) if checked_text else None
    binding = str(record.get("binding_status") or "")
    sla = SLA_DAYS.get(binding, 30)
    disposition = source_disposition(record)
    uncertainty = str(record.get("uncertainty") or (
        "low" if record.get("evidence_tier") == "resolution_text" else
        "medium" if record.get("evidence_tier") == "mixed" else "high"
    ))

    if checked is None:
        return {
            "as_of": today.isoformat(),
            "source_last_checked": None,
            "next_review_due": None,
            "review_status": "unknown",
            "days_overdue": None,
            "sla_days": sla,
            "source_disposition": disposition,
            "uncertainty": uncertainty,
        }

    due = checked + timedelta(days=sla)
    overdue = (today - due).days
    if overdue <= 0:
        status = "current"
        days_overdue = 0
    elif overdue <= 7:
        status = "due_for_review"
        days_overdue = overdue
    else:
        status = "stale"
        days_overdue = overdue
    return {
        "as_of": today.isoformat(),
        "source_last_checked": checked.isoformat(),
        "next_review_due": due.isoformat(),
        "review_status": status,
        "days_overdue": days_overdue,
        "sla_days": sla,
        "source_disposition": disposition,
        "uncertainty": uncertainty,
    }


def enrich_records(records: Iterable[Mapping[str, Any]], as_of: str = DEFAULT_AS_OF) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for record in records:
        row = dict(record)
        row["freshness"] = derive_freshness(record, as_of)
        enriched.append(row)
    return enriched


def freshness_report(records: Iterable[Mapping[str, Any]], as_of: str = DEFAULT_AS_OF) -> dict[str, Any]:
    source_records = list(records)
    rows = [derive_freshness(record, as_of) for record in source_records]
    counts = Counter(row["review_status"] for row in rows)
    dispositions = Counter(row["source_disposition"] for row in rows)
    stages = Counter(str(record.get("review_stage") or "unreviewed") for record in source_records)
    reviewers = sum(1 for record in source_records if record.get("reviewer"))
    second_reviewers = sum(1 for record in source_records if record.get("second_reviewer"))
    high_impact = [
        (record, row) for record, row in zip(source_records, rows)
        if record.get("claim_class") == "tier1_legal"
        and record.get("binding_status") == "in_force_enacted"
        and record.get("dimension") in {
            "issuer_pathway", "reserve_backing", "redemption", "aml_kyc",
            "distribution", "cross_border_data", "permitted_activity_yield",
        }
    ]
    return {
        "schema": "cbsr/freshness-report/v2",
        "as_of": as_of,
        "policy": {"sla_days_by_binding_status": SLA_DAYS, "grace_days": 7},
        "counts": {key: counts.get(key, 0) for key in ("current", "due_for_review", "stale", "unknown")},
        "source_disposition_counts": {
            key: dispositions.get(key, 0)
            for key in ("official", "secondary", "unavailable", "not_applicable")
        },
        "review_stage_counts": dict(sorted(stages.items())),
        "reviewer_coverage": {
            "primary_reviewer": {"count": reviewers, "denominator": len(source_records)},
            "independent_second_reviewer": {"count": second_reviewers, "denominator": len(source_records)},
        },
        "high_impact_sla": {
            "count": len(high_impact),
            "current_reconciled": sum(
                1 for record, row in high_impact
                if row["review_status"] == "current" and record.get("review_stage") == "reconciled"
            ),
            "breached_or_incomplete": sum(
                1 for record, row in high_impact
                if row["review_status"] != "current" or record.get("review_stage") != "reconciled"
            ),
        },
        "decision_rule": (
            "unconditional allow requires current evidence and reconciled independent second review"
        ),
    }
