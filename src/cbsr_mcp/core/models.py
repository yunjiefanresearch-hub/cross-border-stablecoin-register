"""Versioned, domain-neutral policy models used at every public boundary."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

ACTION_SCHEMA = "cbsr/policy-action/v1"
MANDATE_SCHEMA = "cbsr/policy-mandate/v1"
DECISION_SCHEMA = "cbsr/policy-decision/v1"
RECEIPT_SCHEMA = "cbsr/decision-receipt/v1"


def _decimal(value: Any, field_name: str) -> Decimal | None:
    if value in (None, ""):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field_name}_must_be_a_number") from exc


@dataclass(frozen=True)
class AuditIdentity:
    """Stable audit identity; it is an identifier record, not authentication proof."""

    subject_id: str
    actor_type: str
    principal_id: str | None = None
    session_id: str | None = None
    authentication_context: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AuditIdentity":
        return cls(
            subject_id=str(value.get("subject_id") or ""),
            actor_type=str(value.get("actor_type") or ""),
            principal_id=str(value["principal_id"]) if value.get("principal_id") else None,
            session_id=str(value["session_id"]) if value.get("session_id") else None,
            authentication_context=tuple(sorted(str(item) for item in value.get("authentication_context") or ())),
        )


@dataclass(frozen=True)
class TimeWindow:
    starts_at: str
    ends_at: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TimeWindow":
        return cls(starts_at=str(value.get("starts_at") or ""), ends_at=str(value.get("ends_at") or ""))


@dataclass(frozen=True)
class HumanReviewPolicy:
    required: bool = False
    amount_threshold: Decimal | None = None
    jurisdictions: tuple[str, ...] = ()
    dimensions: tuple[str, ...] = ()
    outcomes: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "HumanReviewPolicy":
        return cls(
            required=value.get("required") is True,
            amount_threshold=_decimal(value.get("amount_threshold"), "human_review_amount_threshold"),
            jurisdictions=tuple(sorted(str(item).upper() for item in value.get("jurisdictions") or ())),
            dimensions=tuple(sorted(str(item) for item in value.get("dimensions") or ())),
            outcomes=tuple(sorted(str(item) for item in value.get("outcomes") or ())),
        )


@dataclass(frozen=True)
class Mandate:
    mandate_id: str
    version: str
    issued_by: str
    audit_identity: AuditIdentity
    active: bool = True
    revoked: bool = False
    valid_from: str | None = None
    valid_until: str | None = None
    max_amount: Decimal | None = None
    assets: tuple[str, ...] = ()
    jurisdictions: tuple[str, ...] = ()
    prohibited_jurisdictions: tuple[str, ...] = ()
    counterparties: tuple[str, ...] = ()
    allowed_time_windows: tuple[TimeWindow, ...] = ()
    human_review: HumanReviewPolicy = HumanReviewPolicy()
    schema: str = MANDATE_SCHEMA

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "Mandate":
        if value.get("schema") not in (None, MANDATE_SCHEMA):
            raise ValueError("unsupported_mandate_schema")
        audit = value.get("audit_identity")
        audit_mapping = audit if isinstance(audit, Mapping) else {}
        review = value.get("human_review")
        if isinstance(review, Mapping):
            human_review = HumanReviewPolicy.from_mapping(review)
        else:
            human_review = HumanReviewPolicy(required=value.get("human_approval_required") is True)
        windows = value.get("allowed_time_windows") or ()
        if not all(isinstance(item, Mapping) for item in windows):
            raise ValueError("allowed_time_windows_must_be_objects")
        return cls(
            mandate_id=str(value.get("mandate_id") or ""),
            version=str(value.get("version") or ""),
            issued_by=str(value.get("issued_by") or ""),
            audit_identity=AuditIdentity.from_mapping(audit_mapping),
            active=value.get("active") is not False,
            revoked=value.get("revoked") is True,
            valid_from=str(value["valid_from"]) if value.get("valid_from") else None,
            valid_until=str(value.get("valid_until") or value.get("expires_at") or "") or None,
            max_amount=_decimal(value.get("max_amount"), "max_amount"),
            assets=tuple(sorted(str(item) for item in value.get("assets") or ())),
            jurisdictions=tuple(sorted(str(item).upper() for item in value.get("jurisdictions") or ())),
            prohibited_jurisdictions=tuple(
                sorted(str(item).upper() for item in value.get("prohibited_jurisdictions") or ())
            ),
            counterparties=tuple(sorted(str(item) for item in value.get("counterparties") or ())),
            allowed_time_windows=tuple(TimeWindow.from_mapping(item) for item in windows),
            human_review=human_review,
        )

    def completeness_errors(self) -> tuple[str, ...]:
        missing = []
        if not self.mandate_id:
            missing.append("mandate_id")
        if not self.version:
            missing.append("mandate_version")
        if not self.issued_by:
            missing.append("mandate_issuer")
        if not self.audit_identity.subject_id:
            missing.append("audit_subject_id")
        if not self.audit_identity.actor_type:
            missing.append("audit_actor_type")
        return tuple(missing)


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    origin: str
    destination: str
    asset: str
    amount: Decimal
    actor: str
    mandate: Mandate
    counterparty: str | None = None
    requires_kyc: bool = False
    required_dimensions: tuple[str, ...] = ()
    as_of: str | None = None
    requested_at: str | None = None
    conflicting_evidence: bool = False
    action: str = "transfer"
    authority: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    modality: str = "request"
    obligations: tuple[str, ...] = ()
    exceptions: tuple[str, ...] = ()
    effective_window: TimeWindow | None = None
    evidence: tuple[str, ...] = ()
    uncertainty: str = "unknown"
    schema: str = ACTION_SCHEMA

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ActionRequest":
        if value.get("schema") not in (None, ACTION_SCHEMA):
            raise ValueError("unsupported_action_schema")
        mandate = value.get("mandate")
        if not isinstance(mandate, Mapping):
            raise ValueError("mandate_must_be_an_object")
        amount = _decimal(value.get("amount"), "amount")
        if amount is None:
            raise ValueError("amount_must_be_a_number")
        effective_window = value.get("effective_window")
        if effective_window is not None and not isinstance(effective_window, Mapping):
            raise ValueError("effective_window_must_be_an_object")
        return cls(
            action_id=str(value.get("action_id") or ""),
            origin=str(value.get("origin") or "").upper(),
            destination=str(value.get("destination") or "").upper(),
            asset=str(value.get("asset") or ""),
            amount=amount,
            actor=str(value.get("actor") or ""),
            mandate=Mandate.from_mapping(mandate),
            counterparty=str(value["counterparty"]) if value.get("counterparty") else None,
            requires_kyc=value.get("requires_kyc") is True,
            required_dimensions=tuple(sorted(str(item) for item in value.get("required_dimensions") or ())),
            as_of=str(value["as_of"]) if value.get("as_of") else None,
            requested_at=str(value["requested_at"]) if value.get("requested_at") else None,
            conflicting_evidence=value.get("conflicting_evidence") is True,
            action=str(value.get("action") or "transfer"),
            authority=tuple(sorted(str(item) for item in value.get("authority") or ())),
            conditions=tuple(sorted(str(item) for item in value.get("conditions") or ())),
            modality=str(value.get("modality") or "request"),
            obligations=tuple(sorted(str(item) for item in value.get("obligations") or ())),
            exceptions=tuple(sorted(str(item) for item in value.get("exceptions") or ())),
            effective_window=TimeWindow.from_mapping(effective_window) if effective_window else None,
            evidence=tuple(sorted(str(item) for item in value.get("evidence") or ())),
            uncertainty=str(value.get("uncertainty") or "unknown"),
        )


@dataclass(frozen=True)
class RuleEvidence:
    rule_id: str
    record_id: str
    jurisdiction: str
    dimension: str
    source_url: str | None
    source_disposition: str | None
    source_last_checked: str | None
    next_review_due: str | None
    binding_status: str | None
    legal_status: str | None
    review_status: str | None
    review_stage: str | None
    evidence_tier: str | None
    uncertainty: str

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "RuleEvidence":
        source = record.get("source") or {}
        freshness = record.get("freshness") or {}
        record_id = str(record.get("id") or "")
        return cls(
            rule_id=f"cbsr.rule.{record_id}",
            record_id=record_id,
            jurisdiction=str(record.get("jurisdiction") or ""),
            dimension=str(record.get("dimension") or ""),
            source_url=str(source.get("url")) if source.get("url") else None,
            source_disposition=str(record.get("source_disposition")) if record.get("source_disposition") else None,
            source_last_checked=record.get("source_last_checked") or freshness.get("source_last_checked"),
            next_review_due=record.get("next_review_due") or freshness.get("next_review_due"),
            binding_status=str(record.get("binding_status")) if record.get("binding_status") else None,
            legal_status=str(record.get("legal_status")) if record.get("legal_status") else None,
            review_status=str(freshness.get("review_status") or record.get("review_status") or "unknown"),
            review_stage=str(record.get("review_stage") or "unreviewed"),
            evidence_tier=str(record.get("evidence_tier") or "unverified"),
            uncertainty=str(record.get("uncertainty") or "high"),
        )


@dataclass(frozen=True)
class ConflictDetail:
    jurisdiction: str
    dimension: str
    binding_statuses: tuple[str, ...]
    record_ids: tuple[str, ...]
    source_urls: tuple[str, ...] = ()
    resolution: str = "human_reconciliation_required"


@dataclass(frozen=True)
class FreshnessSnapshot:
    as_of: str
    current: int
    due_for_review: int
    stale: int
    unknown: int
    source_last_checked: tuple[str, ...]
    next_review_due: tuple[str, ...]


@dataclass(frozen=True)
class DecisionResult:
    outcome: str
    reasons: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    source_urls: tuple[str, ...]
    applicable_rules: tuple[RuleEvidence, ...]
    freshness_snapshot: FreshnessSnapshot
    uncertainty: str
    mandate_id: str | None = None
    mandate_version: str | None = None
    assumptions: tuple[str, ...] = ()
    obligations: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    conflict_details: tuple[ConflictDetail, ...] = ()
    engine_version: str = "cbsr-policy-engine/1.1.0"
    ruleset_version: str = "cbsr-stablecoin-rules/1.1.0"
    evaluated_at: str = ""
    requested_as_of: str = ""
    non_legal_advice_notice: str = (
        "CBSR provides deterministic research decision support, not legal advice, "
        "transaction approval or execution authority."
    )
    schema: str = DECISION_SCHEMA
    deterministic: bool = True
    execution_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in (
            "reasons", "evidence_ids", "rule_ids", "source_urls", "applicable_rules",
            "assumptions", "obligations", "conditions", "conflict_details",
        ):
            value[key] = list(value[key])
        value["freshness_snapshot"]["source_last_checked"] = list(
            value["freshness_snapshot"]["source_last_checked"]
        )
        value["freshness_snapshot"]["next_review_due"] = list(
            value["freshness_snapshot"]["next_review_due"]
        )
        return value
