#!/usr/bin/env python3
"""Validate the complete research, dossier, claims and whitepaper delivery."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _rows(path: pathlib.Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    ledger = json.loads((ROOT / "research/source_ledger_2026-08-20.json").read_text(encoding="utf-8"))
    if len(ledger.get("records", [])) != 152:
        raise SystemExit("source ledger must contain 152 records")
    dossier_headings = {
        "Institutional and supervisory boundary", "Authorisation and licensing perimeter",
        "Reserve, safeguarding and redemption", "Cross-border and data conditions",
        "AML, KYC and financial-crime controls", "Enforcement and implementation posture",
        "Legal-event relationships", "Bibliography",
    }
    dossiers = sorted((ROOT / "research/jurisdictions").glob("*.md"))
    if len(dossiers) != 12:
        raise SystemExit("expected twelve jurisdiction dossiers")
    for path in dossiers:
        text = path.read_text(encoding="utf-8")
        if len(text.splitlines()) < 150:
            raise SystemExit(f"dossier is not substantive: {path.name}")
        missing = sorted(heading for heading in dossier_headings if f"## {heading}" not in text)
        if missing:
            raise SystemExit(f"dossier headings missing from {path.name}: {missing}")
    if len(_rows(ROOT / "research/quantitative/jurisdiction_metrics.csv")) != 12:
        raise SystemExit("quantitative jurisdiction CSV must contain twelve rows")
    if len(_rows(ROOT / "research/quantitative/dimension_metrics.csv")) < 15:
        raise SystemExit("quantitative dimension CSV is incomplete")
    dashboard = json.loads((ROOT / "research/quantitative/data_quality_dashboard.json").read_text(encoding="utf-8"))
    required_metrics = {
        "records", "jurisdictions", "dimensions", "records_with_source_url",
        "official_source_disposition", "primary_text_resolution", "decision_ready_citable",
        "freshness_current", "freshness_stale", "high_impact_current_reconciled",
        "missing_source_checked_date", "invalid_date_relationships",
        "uncertainty_high_or_unknown", "primary_reviewer_coverage",
        "independent_second_reviewer_coverage", "first_class_event_coverage",
        "superseded_records", "directed_corridors", "temporally_sensitive_class_moves",
    }
    if {row["metric"] for row in dashboard.get("metrics", [])} < required_metrics:
        raise SystemExit("data-quality dashboard is missing required dimensions")
    if any("denominator" not in row or "definition" not in row for row in dashboard["metrics"]):
        raise SystemExit("dashboard metrics lack denominator or definition")
    if len(_rows(ROOT / "research/qualitative/coded_cases.csv")) != 152:
        raise SystemExit("qualitative coded-case table must contain 152 rows")
    worksheet = _rows(ROOT / "research/qualitative/SECOND_CODER_WORKSHEET.csv")
    if any(row.get("second_coder") for row in worksheet):
        raise SystemExit("second-coder identity was fabricated")
    claims = json.loads((ROOT / "research/claims/claims_ledger.json").read_text(encoding="utf-8"))
    if claims.get("claim_count", 0) < 157:
        raise SystemExit("claims ledger is incomplete")
    required_claim_fields = {"reviewer", "second_reviewer", "review_date", "status", "strength", "limitation"}
    if any(not required_claim_fields <= set(row) for row in claims["claims"]):
        raise SystemExit("claims ledger review and limitation contract is incomplete")
    if claims.get("independent_review_status") != "not_completed":
        raise SystemExit("claims ledger overclaims independent review")
    whitepaper = (ROOT / "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md").read_text(encoding="utf-8")
    exact_title = "# CBSR AgenticFi Policy Infrastructure: Versioned, Citable and Time-Aware Rules for Autonomous Finance"
    expected_sections = [
        "Executive summary", "The evidence and responsibility gap", "Scope and non-claims",
        "Research method and source hierarchy", "CBSR legal-evidence model",
        "Jurisdictional coverage and empirical findings", "Legal-event ontology",
        "Temporal and freshness engine", "Domain-pack architecture", "Deterministic action evaluation",
        "Agent identity, mandate and human approval", "Know-your-agent considerations",
        "MCP, API and decision receipts", "Security, privacy and threat model",
        "Governance, conflicts and corrections", "Quantitative findings", "Qualitative findings",
        "SDG alignment", "Global Digital Compact and DPI safeguard alignment",
        "DPG Standard readiness", "Pilot cases", "Tests, evaluation and failure cases",
        "Adoption and integration model", "Limitations", "Three-year roadmap", "Conclusion",
        "Primary-source bibliography", "Reproducibility appendix",
    ]
    if not whitepaper.startswith(exact_title) or any(f"## {index}. {title}" not in whitepaper for index, title in enumerate(expected_sections, start=1)):
        raise SystemExit("whitepaper title or exact 28-section contract is incomplete")
    if len(whitepaper.splitlines()) < 350:
        raise SystemExit("institutional whitepaper is incomplete")
    if "external peer review and independent legal review not completed" not in whitepaper:
        raise SystemExit("whitepaper external-review boundary missing")
    manifest = json.loads((ROOT / "research/research_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("file_count", 0) < 30:
        raise SystemExit("research manifest unexpectedly small")
    print(f"research delivery valid: 152 cases, 12 dossiers, {claims['claim_count']} claims, {manifest['file_count']} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
