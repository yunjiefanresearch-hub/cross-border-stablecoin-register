#!/usr/bin/env python3
# Copyright the CBSR contributors.
# SPDX-License-Identifier: Apache-2.0
"""Audit the full locked development and measurement graph, not just runtime."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other locales.
import sys
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

import hashlib
import json
import os
from pathlib import Path
import subprocess

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).resolve().parent.parent
LOCKS = ("runtime-hashes.txt", "dev-hashes.txt", "quality-hashes.txt")


def audit_command(output: Path) -> list[str]:
    return [sys.executable, "-m", "pip_audit",
            # With --disable-pip, the parser does not expand nested -r includes.
            "--requirement", str(ROOT / "constraints/runtime-hashes.txt"),
            "--requirement", str(ROOT / "constraints/dev-hashes.txt"),
            "--requirement", str(ROOT / "constraints/quality-hashes.txt"),
            "--require-hashes", "--disable-pip", "--strict",
            "--progress-spinner", "off", "--format", "json", "--output", str(output)]


def expected_dependencies() -> set[tuple[str, str]]:
    expected = set()
    for name in ("runtime.txt", "dev.txt", "quality.txt"):
        for line in (ROOT / "constraints" / name).read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith(("#", "-")):
                continue
            requirement = Requirement(line)
            if requirement.marker and not requirement.marker.evaluate():
                continue
            pins = list(requirement.specifier)
            if len(pins) != 1 or pins[0].operator != "==":
                raise ValueError(f"audit input is not exactly pinned: {line}")
            expected.add((canonicalize_name(requirement.name), pins[0].version))
    return expected


def main() -> int:
    directory = Path(os.environ.get("CBSR_EVIDENCE_DIR", ROOT / "artifacts/validation"))
    if not directory.is_absolute():
        directory = ROOT / directory
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / "development-pip-audit.json"
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    result = subprocess.run(audit_command(output), cwd=ROOT, env=environment, check=False)
    errors = []
    if result.returncode == 0:
        try:
            rows = json.loads(output.read_text(encoding="utf-8"))["dependencies"]
            actual = {(canonicalize_name(row["name"]), row["version"]) for row in rows}
            if actual != expected_dependencies():
                errors.append("Audit inventory does not equal the complete current-platform locked graph.")
            if any(row.get("vulns") or "skip_reason" in row for row in rows):
                errors.append("Audit output contains vulnerabilities or skipped packages.")
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f"Invalid audit output: {error}")
    exit_code = result.returncode or int(bool(errors))
    # Never interpret a failed audit or an old output file as successful evidence.
    binding = {"schema": "cbsr/development-dependency-audit/v1",
               "status": "passed" if exit_code == 0 else "failed",
               "exit_code": exit_code, "errors": errors, "python": sys.version,
               "platform": sys.platform, "scope": "runtime + development + quality locks; current platform markers",
               "locks_sha256": {name: hashlib.sha256((ROOT / "constraints" / name).read_bytes()).hexdigest()
                                for name in LOCKS},
               "audit_output": output.name}
    (directory / "development-audit-binding.json").write_text(
        json.dumps(binding, indent=2) + "\n", encoding="utf-8", newline="\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
