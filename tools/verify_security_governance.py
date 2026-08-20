#!/usr/bin/env python3
"""Validate security workflow declarations, templates and evidence semantics."""
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


def _require(relative: str, tokens: tuple[str, ...] = ()) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"required security/governance file missing: {relative}")
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise SystemExit(f"{relative} missing required declarations: {missing}")


def main() -> int:
    _require(".github/workflows/build.yml", ("python -m tools.verify", '"3.10"', '"3.13"', "windows-clean-room"))
    _require(".github/workflows/codeql.yml", ("github/codeql-action/init@v4", "github/codeql-action/analyze@v4"))
    _require(".github/workflows/dependency-review.yml", ("actions/dependency-review-action@v4", "fail-on-severity"))
    _require(".github/workflows/security.yml", ("gitleaks/gitleaks-action@v2", "ossf/scorecard-action@v2.4.4", "upload-sarif@v4"))
    _require(".github/workflows/release-provenance.yml", ("actions/attest-build-provenance@v3", "python -m tools.verify"))
    _require(".github/dependabot.yml", ("package-ecosystem: pip", "package-ecosystem: github-actions"))
    for name in ("bug.yml", "data-source.yml", "security.yml", "release.yml", "dependency-update.yml", "regulatory-correction.yml", "config.yml"):
        _require(f".github/ISSUE_TEMPLATE/{name}")
    for name in ("SECURITY.md", "PRIVACY.md", "docs/security/THREAT_MODEL.md", "docs/security/EXTERNAL_SECURITY_REVIEW_TEMPLATE.md"):
        _require(name)
    _require("SECURITY.md", ("3 business days", "7 business days", "90 days", "coordinated disclosure", "Good-faith research safe harbour"))
    governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
    if "0 of 152 records are current" not in governance or "no independent second review has been completed" not in governance:
        raise SystemExit("GOVERNANCE.md is not synchronized with the current freshness/review boundary")
    dpg = json.loads((ROOT / "analysis/dpg_evidence_matrix.json").read_text(encoding="utf-8"))
    for row in dpg["indicators"]:
        for relative in row["evidence_files"]:
            if not (ROOT / relative).exists():
                raise SystemExit(f"DPG evidence path does not exist: {relative}")
    print("security/governance declarations valid: workflows, templates, evidence paths and no-overclaim semantics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
