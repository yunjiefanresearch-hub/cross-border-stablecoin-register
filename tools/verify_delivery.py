#!/usr/bin/env python3
"""Validate completeness and honesty of the formal delivery package."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> int:
    required = {
        "TRANSFORMATION_LOG.md", "BASELINE_REPRODUCTION.md", "baseline_reproduction.json",
        "RISK_REGISTER.md", "risk_register.json", "DECISION_LOG.md", "decision_log.json",
        "COMPATIBILITY_MATRIX.md", "compatibility_matrix.csv", "MIGRATION_NOTES_v0.11.md",
        "ROLLBACK_NOTES_v0.11.md", "PR_STACK_PLAN.md", "REMOTE_GITHUB_RUNBOOK.md",
        "FINAL_SCORECARD.md", "final_scorecard.json", "external_gates.json", "delivery_manifest.json",
    }
    actual = {path.name for path in (ROOT / "delivery").iterdir() if path.is_file()}
    missing = sorted(required - actual)
    if missing:
        raise SystemExit("formal delivery files missing: " + ", ".join(missing))
    baseline = _load("delivery/baseline_reproduction.json")
    if baseline["current_metrics"]["records"] != 152:
        raise SystemExit("baseline reproduction record count is not 152")
    risks = _load("delivery/risk_register.json")["risks"]
    if len(risks) < 10 or any(not row.get("owner_role") or not row.get("target_date") for row in risks):
        raise SystemExit("risk register is incomplete")
    decisions = _load("delivery/decision_log.json")["decisions"]
    if len(decisions) < 10:
        raise SystemExit("decision log is incomplete")
    external = _load("delivery/external_gates.json")
    if external.get("release_ready") is not False or any(row["status"] in {"passed", "completed"} for row in external["gates"]):
        raise SystemExit("external gates are overclaimed")
    score = _load("delivery/final_scorecard.json")
    if score.get("release_ready") is not False:
        raise SystemExit("scorecard overclaims release readiness")
    score_rows = score.get("scorecard", [])
    if [row.get("category_id") for row in score_rows] != list("ABCDEFG"):
        raise SystemExit("scorecard must contain the exact seven A-G categories")
    score_contract = {"numerator", "denominator", "evidence_paths", "failing_criteria", "remediation", "confidence"}
    if any(not score_contract <= set(row) for row in score_rows):
        raise SystemExit("scorecard evidence/remediation contract is incomplete")
    doc_required = {
        "CBSR_V0_11_TRANSFORMATION_LOG.md", "BASELINE_REPRODUCTION.md", "RISK_REGISTER.md",
        "DECISION_LOG.md", "COMPATIBILITY_MATRIX.md", "AGENTICFI_EVALUATION_REPORT.md",
        "CLAIMS_LEDGER.md", "CBSR_V0_11_SCORECARD.md", "RELEASE_NOTES_v0.11.0_DRAFT.md",
    }
    doc_actual = {path.name for path in (ROOT / "docs/delivery").iterdir() if path.is_file()}
    if doc_required - doc_actual:
        raise SystemExit("exact docs/delivery contract missing: " + ", ".join(sorted(doc_required - doc_actual)))
    transformation = (ROOT / "docs/delivery/CBSR_V0_11_TRANSFORMATION_LOG.md").read_text(encoding="utf-8")
    atomic_fields = ("Task ID", "Files", "Sources", "Commands", "Result", "Independent review", "Negative test", "Unresolved risks", "Status")
    if any(field not in transformation for field in atomic_fields):
        raise SystemExit("atomic transformation log contract is incomplete")
    if transformation.count("PASS_WITH_LIMITATION") < 4 or "BLOCKED" not in transformation:
        raise SystemExit("transformation log does not preserve limitations/blocked states")
    manifest = _load("delivery/delivery_manifest.json")
    for row in manifest["files"]:
        path = ROOT / row["path"]
        if not path.is_file() or path.stat().st_size != row["bytes"]:
            raise SystemExit(f"delivery manifest size mismatch: {row['path']}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise SystemExit(f"delivery manifest hash mismatch: {row['path']}")
    if manifest["file_count"] != len(manifest["files"]):
        raise SystemExit("delivery manifest count mismatch")
    print(f"delivery valid: {len(risks)} risks, {len(decisions)} decisions, {manifest['file_count']} hashed files, external gates explicit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
