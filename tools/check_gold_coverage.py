#!/usr/bin/env python3
# Copyright the CBSR contributors.
# SPDX-License-Identifier: Apache-2.0
"""Report measured Gold coverage without confusing an audit with qualification."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

COMMON_LIMITATIONS = (
    "Execution coverage does not prove that every executed line has an effective assertion. "
    "The legacy negative suite's temporary source copies are outside the checkout measurement root, "
    "and the clean-wheel smoke's independent runtime environment has no coverage tooling; "
    "their results remain separate verification evidence, not measured coverage here. "
    "Python only: JavaScript, earlier badge levels, people, reviews and hosting evidence remain separate requirements."
)


def metrics(files: dict) -> dict:
    totals = {key: sum(row["summary"][key] for row in files.values()) for key in (
        "num_statements", "covered_lines", "num_branches", "covered_branches",
    )}
    statements = totals["num_statements"]
    branches = totals["num_branches"]
    totals["statement_percent"] = 100 * totals["covered_lines"] / statements if statements else None
    totals["branch_percent"] = 100 * totals["covered_branches"] / branches if branches else None
    totals["thresholds_met"] = bool(statements and branches and
        totals["covered_lines"] * 100 >= statements * 90 and
        totals["covered_branches"] * 100 >= branches * 80)
    return totals


def current_source_fingerprint() -> str:
    """Use the canonical verifier's exact source scope, not a second definition."""
    if __package__:
        from .verify import _source_fingerprint
    else:
        from verify import _source_fingerprint
    return _source_fingerprint()


def verification_binding(path: Path, files: dict) -> dict:
    """Keep failed/missing/stale evidence visible, but never qualifying."""
    errors = []
    summary = {}
    try:
        summary = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(summary, dict):
            raise ValueError("verification summary must be an object")
    except (OSError, ValueError) as error:
        errors.append(f"Cannot read verification summary: {error}")
        summary = {}
    if summary.get("schema") != "cbsr/verification-summary/v2":
        errors.append("Unsupported or absent canonical verification summary schema.")
    if summary.get("status") != "passed":
        errors.append("Canonical verification did not pass.")
    current = current_source_fingerprint()
    if summary.get("source_fingerprint_sha256") != current:
        errors.append("Verification source fingerprint does not match the current checkout.")
    contexts = files.get("tools/verify.py", {}).get("contexts", {})
    if not any("canonical" in values for values in contexts.values()):
        errors.append("Coverage must include the canonical verifier context; export JSON with --show-contexts.")
    return {
        "summary_path": str(path),
        "schema": summary.get("schema"),
        "status": summary.get("status"),
        "source_fingerprint_sha256": summary.get("source_fingerprint_sha256"),
        "current_source_fingerprint_sha256": current,
        "valid": not errors,
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "artifacts/validation/coverage.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/validation/gold-coverage.json")
    parser.add_argument("--enforce", action="store_true", help="Fail below 90%% statements / 80%% branches")
    parser.add_argument("--verification-summary", type=Path, help="Bind canonical coverage to its successful, current-source summary")
    args = parser.parse_args(argv)
    coverage = json.loads(args.input.read_text(encoding="utf-8"))
    if coverage.get("meta", {}).get("branch_coverage") is not True:
        parser.error("branch measurement is required; a statement-only report cannot qualify")
    files = {name.replace("\\", "/"): row for name, row in coverage["files"].items()}
    tracked = subprocess.check_output(
        ["git", "-c", "safe.directory=*", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.py"],
        cwd=ROOT, text=True, encoding="utf-8",
    ).splitlines()
    expected = {name for name in tracked if not name.startswith(("tests/", "artifacts/", "dist/"))}
    missing = sorted(expected - files.keys())
    project = metrics(files)
    runtime = metrics({name: row for name, row in files.items() if name.startswith("src/")})
    binding = verification_binding(args.verification_summary, files) if args.verification_summary else None
    evidence_valid = binding is None or binding["valid"]
    mode = "canonical_subprocess" if binding is not None else "pytest_only"
    limitations = (
        "This run measures canonical verification, including pytest and same-environment subprocesses. "
        "The CI workflow uses a fresh checkout, erased coverage data and a per-attempt summary path; "
        "a matching source fingerprint alone does not establish freshness of locally reused coverage files. "
        if binding is not None else
        "This report has no canonical verification binding: the legacy command measures pytest and its "
        "same-environment subprocesses, not the canonical verifier's separate suites. "
    )
    report = {
        "schema": "cbsr/gold-coverage/v2",
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "coverage_tool_version": coverage["meta"]["version"],
        "scope": "All repository Python source, including generators and historical scripts; tests and installed/build artifacts excluded.",
        "measurement_mode": mode,
        "limitations": limitations + COMMON_LIMITATIONS,
        "verification_evidence": binding,
        "project_python": project,
        "runtime_python_diagnostic_only": runtime,
        "missing_source_files": missing,
        "coverage_thresholds_met": project["thresholds_met"] and not missing and evidence_valid,
        "gold_badge_awarded": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))
    return int(bool(missing) or not evidence_valid or (args.enforce and not report["coverage_thresholds_met"]))


if __name__ == "__main__":
    raise SystemExit(main())
