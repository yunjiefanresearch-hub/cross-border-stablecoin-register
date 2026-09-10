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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "artifacts/validation/coverage.json")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/validation/gold-coverage.json")
    parser.add_argument("--enforce", action="store_true", help="Fail below 90%% statements / 80%% branches")
    args = parser.parse_args()
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
    report = {
        "schema": "cbsr/gold-coverage/v1",
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "coverage_tool_version": coverage["meta"]["version"],
        "scope": "All repository Python source, including generators and historical scripts; tests and installed/build artifacts excluded.",
        "limitations": "This run measures pytest, not the canonical verifier's separate subprocess suites. Python only: JavaScript, earlier badge levels, people, reviews and hosting evidence remain separate requirements.",
        "project_python": project,
        "runtime_python_diagnostic_only": runtime,
        "missing_source_files": missing,
        "coverage_thresholds_met": project["thresholds_met"] and not missing,
        "gold_badge_awarded": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, indent=2))
    return int(bool(missing) or (args.enforce and not report["coverage_thresholds_met"]))


if __name__ == "__main__":
    raise SystemExit(main())
