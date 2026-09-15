"""Typed, deterministic and side-effect-free AgenticFi policy core."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.

import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from collections import Counter
from datetime import date, datetime, timezone
from typing import Any, Iterable, Mapping

from .core.models import (
    ActionRequest,
    ConflictDetail,
    DecisionResult,
    FreshnessSnapshot,
    RuleEvidence,
)
from .domain_packs.stablecoin import STABLECOIN_PACK

OUTCOMES = {
    "allow",
    "allow_with_conditions",
    "review_required",
    "prohibited",
    "insufficient_evidence",
}
ENGINE_VERSION = "cbsr-policy-engine/1.1.0"
_UNCERTAINTY_ORDER = {"low": 0, "medium": 1, "mixed": 2, "high": 3, "unknown": 4}


def _iso_date(value: str, error: str) -> date:
    try:
        parsed = date.fromisoformat(value)
        if parsed.isoformat() != value:
            raise ValueError(error)
        return parsed
    except (TypeError, ValueError) as exc:
        raise ValueError(error) from exc


def _iso_datetime(value: str, error: str) -> datetime:
    try:
        normalized = value.replace("Z", "+00:00")
        result = datetime.fromisoformat(normalized)
        return result if result.tzinfo else result.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as exc:
        raise ValueError(error) from exc


def _snapshot(rules: list[RuleEvidence], as_of: str) -> FreshnessSnapshot:
    counts = Counter(rule.review_status or "unknown" for rule in rules)
    return FreshnessSnapshot(
        as_of=as_of,
        current=counts.get("current", 0),
        due_for_review=counts.get("due_for_review", 0),
        stale=counts.get("stale", 0),
        unknown=counts.get("unknown", 0),
        source_last_checked=tuple(sorted({value for value in (r.source_last_checked for r in rules) if value})),
        next_review_due=tuple(sorted({value for value in (r.next_review_due for r in rules) if value})),
    )


def _uncertainty(rules: list[RuleEvidence]) -> str:
    if not rules:
        return "unknown"
    return max((rule.uncertainty for rule in rules), key=lambda item: _UNCERTAINTY_ORDER.get(item, 4))


def _result(
    outcome: str,
    reasons: list[str],
    evidence: Iterable[Mapping[str, Any]] = (),
    *,
    as_of: str,
    candidate: ActionRequest | None = None,
    assumptions: list[str] | None = None,
    obligations: list[str] | None = None,
    conditions: list[str] | None = None,
    conflicts: list[ConflictDetail] | None = None,
) -> dict[str, Any]:
    if outcome not in OUTCOMES:
        raise ValueError(f"unsupported outcome: {outcome}")
    rules = sorted(
        (RuleEvidence.from_record(row) for row in evidence),
        key=lambda item: (item.rule_id, item.source_url or ""),
    )
    mandate = candidate.mandate if candidate else None
    return DecisionResult(
        outcome=outcome,
        reasons=tuple(sorted(set(reasons))),
        evidence_ids=tuple(sorted({rule.record_id for rule in rules if rule.record_id})),
        rule_ids=tuple(sorted({rule.rule_id for rule in rules if rule.record_id})),
        source_urls=tuple(sorted({rule.source_url for rule in rules if rule.source_url})),
        applicable_rules=tuple(rules),
        freshness_snapshot=_snapshot(rules, as_of),
        uncertainty=_uncertainty(rules),
        mandate_id=mandate.mandate_id if mandate else None,
        mandate_version=mandate.version if mandate else None,
        assumptions=tuple(sorted(set(assumptions or []))),
        obligations=tuple(sorted(set(obligations or []))),
        conditions=tuple(sorted(set(conditions or []))),
        conflict_details=tuple(conflicts or ()),
        engine_version=ENGINE_VERSION,
        ruleset_version=STABLECOIN_PACK.ruleset_version,
        evaluated_at=f"{as_of}T00:00:00Z",
        requested_as_of=as_of,
    ).to_dict()


def _input_failure(reason: str, as_of: str = "1970-01-01") -> dict[str, Any]:
    return _result(
        "insufficient_evidence",
        [reason],
        as_of=as_of,
        assumptions=["caller_input_is_untrusted", "offline_snapshot_only"],
    )


def _window_allows(candidate: ActionRequest, as_of: date) -> bool:
    windows = candidate.mandate.allowed_time_windows
    if not windows:
        return True
    instant = _iso_datetime(candidate.requested_at or f"{as_of.isoformat()}T00:00:00Z", "invalid_requested_at")
    return any(
        _iso_datetime(window.starts_at, "invalid_time_window")
        <= instant
        <= _iso_datetime(window.ends_at, "invalid_time_window")
        for window in windows
    )


def evaluate_policy(
    action: Mapping[str, Any],
    evidence: Iterable[Mapping[str, Any]],
    as_of: str,
    *,
    known_record_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Evaluate an action against a mandate and explicit evidence; never execute it."""
    if not isinstance(action, Mapping):
        return _input_failure("action_must_be_an_object")
    if not isinstance(as_of, str):
        return _input_failure("invalid_as_of_date")
    required = ("action_id", "origin", "destination", "asset", "amount", "actor", "mandate")
    missing = [key for key in required if action.get(key) in (None, "", {})]
    if missing:
        return _input_failure("missing_context:" + ",".join(sorted(missing)), as_of)
    try:
        candidate = ActionRequest.from_mapping(action)
        today = _iso_date(as_of, "invalid_as_of_date")
    except ValueError as exc:
        return _input_failure(str(exc), as_of if len(as_of) >= 10 else "1970-01-01")
    if not all((candidate.action_id, candidate.origin, candidate.destination, candidate.asset, candidate.actor)):
        return _input_failure("missing_required_string_context", today.isoformat())
    if len(candidate.origin) != 2 or len(candidate.destination) != 2:
        return _input_failure("jurisdiction_codes_must_be_iso_alpha_2", today.isoformat())
    completeness = candidate.mandate.completeness_errors()
    if completeness:
        return _input_failure("incomplete_mandate:" + ",".join(completeness), today.isoformat())
    domain_errors = STABLECOIN_PACK.validate_action(action)
    if domain_errors:
        return _input_failure("domain_validation:" + ",".join(domain_errors), today.isoformat())

    try:
        supplied_rows = list(evidence)
    except TypeError:
        return _input_failure("evidence_must_be_an_array", today.isoformat())
    rows = []
    for row in supplied_rows:
        if not isinstance(row, Mapping):
            return _input_failure("evidence_records_must_be_objects", today.isoformat())
        source = row.get("source")
        freshness = row.get("freshness")
        if source is not None and not isinstance(source, Mapping):
            return _input_failure("evidence_source_must_be_an_object", today.isoformat())
        if freshness is not None and not isinstance(freshness, Mapping):
            return _input_failure("evidence_freshness_must_be_an_object", today.isoformat())
        rows.append(dict(row))
    malformed_ids = [str(row.get("id") or "") for row in rows if not row.get("id")]
    if malformed_ids:
        return _input_failure("malformed_evidence_record", today.isoformat())
    if known_record_ids is not None:
        unknown = sorted({str(row.get("id")) for row in rows if str(row.get("id")) not in known_record_ids})
        if unknown:
            return _input_failure("unknown_evidence_record:" + ",".join(unknown), today.isoformat())

    dimensions = set(candidate.required_dimensions or STABLECOIN_PACK.default_dimensions)
    obligations = list(STABLECOIN_PACK.obligations_for(dimensions))
    assumptions = [
        f"evaluation_as_of:{today.isoformat()}",
        "offline_committed_snapshot",
        "audit_identity_is_asserted_not_authenticated_by_cbsr",
    ]
    mandate = candidate.mandate
    requested = {candidate.origin, candidate.destination}

    def decided(outcome: str, reason: str) -> dict[str, Any]:
        return _result(
            outcome,
            [reason],
            rows,
            as_of=today.isoformat(),
            candidate=candidate,
            assumptions=assumptions,
            obligations=obligations,
        )

    if mandate.revoked or not mandate.active:
        return decided("prohibited", "mandate_revoked_or_inactive")
    try:
        if mandate.valid_from and _iso_date(mandate.valid_from, "invalid_mandate_valid_from") > today:
            return decided("prohibited", "mandate_not_yet_valid")
        if mandate.valid_until and _iso_date(mandate.valid_until, "invalid_mandate_valid_until") < today:
            return decided("prohibited", "mandate_expired")
        if not _window_allows(candidate, today):
            return decided("prohibited", "outside_mandate_time_window")
    except ValueError as exc:
        return _input_failure(str(exc), today.isoformat())
    if candidate.amount < 0:
        return _input_failure("amount_must_be_non_negative_number", today.isoformat())
    if requested & set(mandate.prohibited_jurisdictions):
        return decided("prohibited", "prohibited_jurisdiction_in_mandate")
    if mandate.max_amount is not None and candidate.amount > mandate.max_amount:
        return decided("prohibited", "amount_exceeds_mandate")
    if mandate.assets and candidate.asset not in set(mandate.assets):
        return decided("prohibited", "asset_outside_mandate")
    if mandate.jurisdictions and not requested <= set(mandate.jurisdictions):
        return decided("prohibited", "jurisdiction_outside_mandate")
    if mandate.counterparties and candidate.counterparty not in set(mandate.counterparties):
        return decided("prohibited", "counterparty_outside_mandate")
    if not rows:
        return _result(
            "insufficient_evidence",
            ["no_applicable_regulatory_evidence"],
            as_of=today.isoformat(),
            candidate=candidate,
            assumptions=assumptions,
            obligations=obligations,
        )
    if any(row.get("binding_status") == "prohibition" for row in rows):
        return decided("prohibited", "applicable_regulatory_prohibition")

    conditions: list[str] = []
    reasons: list[str] = []
    review = mandate.human_review
    if (
        review.required
        or (review.amount_threshold is not None and candidate.amount >= review.amount_threshold)
        or bool(requested & set(review.jurisdictions))
        or bool(dimensions & set(review.dimensions))
    ):
        conditions.append("obtain_human_approval")
    if candidate.requires_kyc:
        conditions.append("complete_kyc_before_execution")
    freshness = [(row.get("freshness") or {}).get("review_status") for row in rows]
    if any(value in {"stale", "due_for_review", "unknown", None} for value in freshness):
        reasons.append("evidence_not_current")
    if any(row.get("review_stage") != "reconciled" for row in rows):
        reasons.append("independent_second_review_incomplete")
    if any(row.get("status") in {"proposed", "consultation", "transitional", "superseded"} for row in rows):
        reasons.append("non_final_transitional_or_superseded_rule")
    if any(
        row.get("binding_status")
        in {"pending_proposal", "made_not_commenced", "finalized_policy_pending", "no_regime"}
        for row in rows
    ):
        reasons.append("rule_not_operative")

    cells: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        key = (str(row.get("jurisdiction") or ""), str(row.get("dimension") or ""))
        cells.setdefault(key, []).append(row)
    conflicts: list[ConflictDetail] = []
    for (jurisdiction, dimension), cell_rows in sorted(cells.items()):
        statuses = sorted({str(row.get("binding_status")) for row in cell_rows})
        legal_statuses = sorted({str(row.get("legal_status")) for row in cell_rows if row.get("legal_status")})
        if len(statuses) > 1 or len(legal_statuses) > 1:
            conflicts.append(
                ConflictDetail(
                    jurisdiction=jurisdiction,
                    dimension=dimension,
                    binding_statuses=tuple(statuses),
                    record_ids=tuple(sorted(str(row.get("id")) for row in cell_rows if row.get("id"))),
                    source_urls=tuple(sorted({
                        str((row.get("source") or {}).get("url"))
                        for row in cell_rows if (row.get("source") or {}).get("url")
                    })),
                )
            )
    if conflicts or candidate.conflicting_evidence:
        reasons.append("conflicting_evidence")
    if reasons:
        return _result(
            "review_required",
            reasons,
            rows,
            as_of=today.isoformat(),
            candidate=candidate,
            assumptions=assumptions,
            obligations=obligations,
            conditions=conditions,
            conflicts=conflicts,
        )
    if review.outcomes and "allow" in review.outcomes:
        conditions.append("obtain_human_approval")
    if conditions:
        return _result(
            "allow_with_conditions",
            ["operative_current_reconciled_evidence"],
            rows,
            as_of=today.isoformat(),
            candidate=candidate,
            assumptions=assumptions,
            obligations=obligations,
            conditions=conditions,
        )
    return _result(
        "allow",
        ["operative_current_reconciled_evidence"],
        rows,
        as_of=today.isoformat(),
        candidate=candidate,
        assumptions=assumptions,
        obligations=obligations,
    )
