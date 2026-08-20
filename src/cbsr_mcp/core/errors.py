"""Versioned error envelopes for public CBSR integrations."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PublicError:
    code: str
    message: str
    details: dict[str, Any] | None = None
    schema: str = "cbsr/error/v1"

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def error(code: str, message: str, **details: Any) -> dict[str, Any]:
    return PublicError(code=code, message=message, details=details or None).to_dict()
