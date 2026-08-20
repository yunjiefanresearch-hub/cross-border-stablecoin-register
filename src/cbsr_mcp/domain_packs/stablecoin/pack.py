"""Versioned stablecoin domain pack for the domain-neutral policy engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass(frozen=True)
class StablecoinDomainPack:
    schema: str = "cbsr/domain-pack/v1"
    name: str = "stablecoin"
    version: str = "1.1.0"
    ruleset_version: str = "cbsr-stablecoin-rules/1.1.0"
    default_dimensions: tuple[str, ...] = (
        "issuer_pathway",
        "reserve_backing",
        "redemption",
        "aml_kyc",
        "cross_border_data",
        "distribution",
    )
    supported_assets: tuple[str, ...] = (
        "fiat_referenced_stablecoin",
        "payment_stablecoin",
        "e_money_token",
        "asset_referenced_token",
    )

    def obligations_for(self, dimensions: set[str]) -> tuple[str, ...]:
        mapping = {
            "aml_kyc": "verify_applicable_aml_kyc_and_sanctions_controls",
            "cross_border_data": "verify_cross_border_data_transfer_basis",
            "distribution": "verify_distribution_and_offering_permissions",
            "issuer_pathway": "verify_issuer_and_intermediary_authorizations",
            "reserve_backing": "verify_reserve_composition_custody_and_attestation",
            "redemption": "verify_redemption_rights_timing_and_par_value",
            "permitted_activity_yield": "verify_yield_and_interest_restrictions",
            "capital_requirements": "verify_capital_liquidity_and_safeguarding",
        }
        return tuple(sorted(mapping[item] for item in dimensions if item in mapping))

    def validate_action(self, action: Mapping[str, object]) -> tuple[str, ...]:
        errors = []
        if str(action.get("origin") or "") == str(action.get("destination") or ""):
            errors.append("origin_and_destination_must_differ")
        if not str(action.get("asset") or "").strip():
            errors.append("stablecoin_asset_is_required")
        return tuple(errors)

    def to_manifest(self) -> dict[str, object]:
        value = asdict(self)
        value["default_dimensions"] = list(self.default_dimensions)
        value["supported_assets"] = list(self.supported_assets)
        value["obligation_catalog"] = {
            dimension: list(self.obligations_for({dimension})) for dimension in self.default_dimensions
        }
        value["execution_boundary"] = "decision_support_only"
        return value


STABLECOIN_PACK = StablecoinDomainPack()
