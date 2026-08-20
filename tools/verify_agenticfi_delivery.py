#!/usr/bin/env python3
"""Hard-gate the AgenticFi schemas, scenario report and two pilot evidence chains."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import pathlib

from jsonschema import Draft202012Validator

from cbsr_mcp.domain_packs.stablecoin import STABLECOIN_PACK
from cbsr_mcp.receipts import verify_receipt

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))
    manifest = json.loads((ROOT / "src/cbsr_mcp/domain_packs/stablecoin/manifest.json").read_text(encoding="utf-8"))
    if manifest != STABLECOIN_PACK.to_manifest():
        raise SystemExit("stablecoin domain-pack manifest drift")
    report = json.loads((ROOT / "research/agenticfi_evaluation.json").read_text(encoding="utf-8"))
    if report.get("scenario_count", 0) < 18:
        raise SystemExit("fewer than 18 AgenticFi scenarios")
    required_names = {"malformed_amount", "unknown_record", "superseded_rule", "outside_time_window", "prohibited_jurisdiction", "detected_conflict"}
    names = {row["id"] for row in report.get("scenarios", [])}
    if not required_names <= names:
        raise SystemExit("required independent scenarios missing")
    pilot_files = sorted((ROOT / "research/pilots").glob("*.json"))
    if len(pilot_files) != 2:
        raise SystemExit(f"expected two JSON pilots, found {len(pilot_files)}")
    receipt_fields = {
        "applicable_rules", "source_urls", "freshness_snapshot", "assumptions", "uncertainty",
        "mandate", "audit_identity", "engine_version", "ruleset_version", "generated_at",
        "requested_as_of", "non_legal_advice_notice",
    }
    required_pilots = {
        "pilot-enterprise-stablecoin-payment",
        "pilot-tokenized-green-asset-settlement",
    }
    if {json.loads(path.read_text(encoding="utf-8"))["pilot_id"] for path in pilot_files} != required_pilots:
        raise SystemExit("required enterprise-payment and tokenized-green-asset pilots are missing")
    for path in pilot_files:
        pilot = json.loads(path.read_text(encoding="utf-8"))
        if not pilot.get("replay", {}).get("decision_identical") or not pilot.get("replay", {}).get("receipt_identical"):
            raise SystemExit(f"pilot is not reproducible: {path.name}")
        if not verify_receipt(pilot["receipt"])["valid"]:
            raise SystemExit(f"pilot receipt invalid: {path.name}")
        if not receipt_fields <= set(pilot["receipt"]):
            raise SystemExit(f"pilot receipt incomplete: {path.name}")
        if pilot.get("legal_currentness_claim") is not False:
            raise SystemExit(f"pilot overclaims legal currentness: {path.name}")
        required_sections = {
            "actors", "jurisdictions", "assets", "assumed_facts", "decision_path",
            "human_review_trigger", "limitations", "failure_cases",
        }
        if not required_sections <= set(pilot) or any(not pilot[field] for field in required_sections):
            raise SystemExit(f"pilot delivery contract incomplete: {path.name}")
        markdown = path.with_suffix(".md").read_text(encoding="utf-8")
        for heading in ("Actors, jurisdictions, assets and assumed facts", "Deterministic decision path", "Human-review trigger", "Limitations", "Failure cases"):
            if f"## {heading}" not in markdown:
                raise SystemExit(f"pilot narrative missing {heading}: {path.name}")
    print(f"AgenticFi delivery valid: {report['scenario_count']} scenarios, {len(pilot_files)} pilots")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
