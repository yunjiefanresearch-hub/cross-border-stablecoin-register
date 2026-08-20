"""Domain-pack protocol for plugging sector rules into the generic policy core."""

from typing import Mapping, Protocol


class DomainPack(Protocol):
    schema: str
    name: str
    version: str
    ruleset_version: str
    default_dimensions: tuple[str, ...]
    supported_assets: tuple[str, ...]

    def obligations_for(self, dimensions: set[str]) -> tuple[str, ...]: ...
    def validate_action(self, action: Mapping[str, object]) -> tuple[str, ...]: ...
    def to_manifest(self) -> dict[str, object]: ...
