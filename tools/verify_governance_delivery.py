#!/usr/bin/env python3
"""Fail closed when governance and public-interest mappings are incomplete."""
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

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _common(rows: list[dict], label: str, evidence_key: str = "evidence_files") -> None:
    required = {"owner_role", "reviewed_date", "target_date", "verification_command"}
    for row in rows:
        missing = sorted(required - row.keys())
        if missing:
            raise SystemExit(f"{label} row missing fields: {missing}")
        if not row.get(evidence_key):
            raise SystemExit(f"{label} row has no evidence")


def main() -> int:
    dpg = _load("analysis/dpg_evidence_matrix.json")
    dpg_rows = dpg["indicators"]
    expected_dpg = {"1", "2", "3", "4", "5", "6", "7", "8", "9A", "9B", "9C"}
    if {row["indicator"] for row in dpg_rows} != expected_dpg:
        raise SystemExit("DPG matrix must contain indicators 1-8 and 9A-9C exactly once")
    if any(row.get("external_determination") is not False for row in dpg_rows):
        raise SystemExit("DPG self-assessment must not claim an external determination")
    _common(dpg_rows, "DPG")
    if any(not row.get("interpretation") or not row.get("next_action") for row in dpg_rows):
        raise SystemExit("DPG rows lack interpretation or next action")

    sdg_rows = _load("analysis/sdg_mapping.json")["mappings"]
    if {row["target"] for row in sdg_rows} != {"9.1", "8.10", "16.4", "16.6", "16.10", "17.18"}:
        raise SystemExit("SDG mapping does not match the approved target set")
    if any(row.get("causal_claim") is not False or row.get("measurement_status") != "not_evaluated" for row in sdg_rows):
        raise SystemExit("SDG mapping overclaims measurement or causality")
    _common(sdg_rows, "SDG", "evidence")
    required_sdg = {"measurable_project_indicator", "claim_strength", "causal_limitation", "data_limitation"}
    if any(not required_sdg <= set(row) for row in sdg_rows):
        raise SystemExit("SDG rows lack measurable indicator or claim limitations")

    gdc_rows = _load("analysis/gdc_mapping.json")["mappings"]
    if len(gdc_rows) < 6 or any(row.get("external_determination") is not False for row in gdc_rows):
        raise SystemExit("GDC mapping is incomplete or overclaims external assurance")
    _common(gdc_rows, "GDC")

    dpi_payload = _load("analysis/dpi_safeguards_mapping.json")
    dpi_rows = dpi_payload["principles"]
    expected_dpi = {f"F{number}" for number in range(1, 10)} | {f"O{number}" for number in range(1, 10)}
    if {row["principle_id"] for row in dpi_rows} != expected_dpi:
        raise SystemExit("DPI safeguards mapping must contain F1-F9 and O1-O9 exactly once")
    if len(dpi_payload["risks"]) != 13:
        raise SystemExit("DPI safeguards risk map must contain all 13 risk groups")
    if any(row.get("external_determination") is not False for row in dpi_rows):
        raise SystemExit("DPI mapping must not claim an external determination")
    _common(dpi_rows, "DPI")
    _common(dpi_payload["risks"], "DPI risk", "repository_controls")
    for name in (
        "DPG_SUBMISSION_READINESS.md", "OPENSSF_READINESS.md",
        "ARCHIVAL_AND_PERSISTENT_IDENTIFIERS.md", "FAIR_METADATA_AND_VERSIONING.md",
    ):
        path = ROOT / "docs/governance" / name
        if not path.is_file() or len(path.read_text(encoding="utf-8").splitlines()) < 7:
            raise SystemExit(f"governance delivery missing or incomplete: {name}")
    print("governance delivery valid: 11 DPG indicators, 6 SDG targets, 6 GDC commitments, 18 DPI principles, 13 risks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
