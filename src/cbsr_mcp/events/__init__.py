"""Legal-event ontology and temporal validation."""

from .ontology import ALLOWED_TRANSITIONS, validate_record_timeline

__all__ = ["ALLOWED_TRANSITIONS", "validate_record_timeline"]
