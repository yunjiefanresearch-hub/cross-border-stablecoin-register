"""Typed evidence-review state, separate from the legal-force ontology."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

SOURCE_DISPOSITIONS = frozenset({"official", "secondary", "unavailable", "not_applicable"})
SOURCE_CHECK_STATUSES = frozenset({"checked", "not_checked", "source_unavailable"})
REVIEW_STAGES = frozenset({
    "unreviewed", "primary_reviewed_second_pending", "reconciliation_required", "reconciled",
})


@dataclass(frozen=True)
class ReviewState:
    source_disposition: str
    source_check_status: str
    source_last_checked: str | None
    next_review_due: str | None
    review_status: str
    reviewer: str | None
    second_reviewer: str | None
    review_stage: str
    reconciliation_status: str
    uncertainty: str

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "ReviewState":
        disposition = str(record.get("source_disposition") or "unavailable")
        if disposition not in SOURCE_DISPOSITIONS:
            raise ValueError(f"invalid source_disposition: {disposition}")
        check_status = str(record.get("source_check_status") or "not_checked")
        if check_status not in SOURCE_CHECK_STATUSES:
            raise ValueError(f"invalid source_check_status: {check_status}")
        stage = str(record.get("review_stage") or "unreviewed")
        if stage not in REVIEW_STAGES:
            raise ValueError(f"invalid review_stage: {stage}")
        return cls(
            source_disposition=disposition,
            source_check_status=check_status,
            source_last_checked=record.get("source_last_checked"),
            next_review_due=record.get("next_review_due"),
            review_status=str(record.get("review_status") or "unknown"),
            reviewer=record.get("reviewer"),
            second_reviewer=record.get("second_reviewer"),
            review_stage=stage,
            reconciliation_status=str(record.get("reconciliation_status") or "not_started"),
            uncertainty=str(record.get("uncertainty") or "high"),
        )

    @property
    def decision_ready(self) -> bool:
        return (
            self.source_disposition == "official"
            and self.review_status == "current"
            and self.review_stage == "reconciled"
            and bool(self.reviewer)
            and bool(self.second_reviewer)
        )
