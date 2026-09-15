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
import re

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _require(relative: str, tokens: tuple[str, ...] = ()) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"required security/governance file missing: {relative}")
    text = path.read_text(encoding="utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise SystemExit(f"{relative} missing required declarations: {missing}")


def pinned_action_names(workflow: dict) -> set[str]:
    """Check immutable external actions without coupling gates to mutable tags."""
    if not isinstance(workflow, dict) or not isinstance(workflow.get("jobs"), dict):
        raise ValueError("workflow must contain a jobs mapping")
    names: set[str] = set()
    for job in workflow["jobs"].values():
        if not isinstance(job, dict) or not isinstance(job.get("steps", []), list):
            raise ValueError("workflow job/steps must be a mapping/list")
        entries = [job, *job.get("steps", [])]
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("workflow step must be a mapping")
            uses = entry.get("uses")
            if uses is None:
                continue
            if not isinstance(uses, str):
                raise ValueError("workflow uses value must be a string")
            if uses.startswith("./"):
                continue  # local actions inherit the checked-out source revision
            if uses.startswith("docker://"):
                if not re.fullmatch(r"docker://[^@]+@sha256:[0-9a-f]{64}", uses):
                    raise ValueError(f"container action must use an immutable digest: {uses}")
                continue
            if not re.fullmatch(r"[^@\s]+@[0-9a-f]{40}", uses):
                raise ValueError(f"external action must use a full commit SHA: {uses}")
            names.add(uses.split("@", 1)[0])
    return names


def validate_default_permissions(workflow: dict) -> None:
    """Require explicit read-only defaults; grant writes only to reviewed jobs."""
    permissions = workflow.get("permissions")
    if permissions == "read-all":
        return
    if not isinstance(permissions, dict) or any(
        value not in ("read", "none") for value in permissions.values()
    ):
        raise ValueError("workflow default permissions must be explicit and read-only")


def validate_release_boundary(workflow: dict) -> None:
    """Keep source execution out of the signing and release-write jobs."""
    pinned_action_names(workflow)
    jobs = workflow["jobs"]
    if set(jobs) != {"verify-wheel", "attest-wheel", "publish-release-assets"}:
        raise ValueError("release must retain three separately reviewed jobs")
    expected_permissions = {
        "verify-wheel": {"contents": "read"},
        "attest-wheel": {"contents": "read", "id-token": "write", "attestations": "write"},
        "publish-release-assets": {"contents": "write"},
    }
    for name, permissions in expected_permissions.items():
        if jobs[name].get("permissions") != permissions:
            raise ValueError(f"unexpected release permissions: {name}")
    if jobs["attest-wheel"].get("needs") != "verify-wheel":
        raise ValueError("attestation requires successful verification")
    publisher = jobs["publish-release-assets"]
    if publisher.get("needs") != "attest-wheel" or publisher.get("if") != "github.event_name == 'release'":
        raise ValueError("publication requires attestation and a release event")
    expected_actions = {
        "attest-wheel": {"actions/download-artifact", "actions/attest-build-provenance"},
        "publish-release-assets": {"actions/download-artifact"},
    }
    for name, allowed in expected_actions.items():
        if pinned_action_names({"jobs": {name: jobs[name]}}) != allowed:
            raise ValueError(f"unreviewed action in privileged release job: {name}")
        for step in jobs[name]["steps"]:
            if str(step.get("uses", "")).startswith("./"):
                raise ValueError("privileged release jobs cannot run local actions")
            if "run" not in step:
                continue
            command = " ".join(step["run"].replace("\\\n", " ").split())
            expected = (
                'set -euo pipefail gh release upload "$RELEASE_TAG" '
                'release-evidence/dist/*.whl release-evidence/dist/*.json '
                'release-evidence/dist/SHA256SUMS --repo "$GH_REPO"'
            )
            if name != "publish-release-assets" or command != expected:
                raise ValueError("privileged release job must only upload existing verified assets")


def _require_actions(relative: str, expected: tuple[str, ...] = ()) -> None:
    document = yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))
    names = pinned_action_names(document)
    validate_default_permissions(document)
    missing = sorted(set(expected) - names)
    if missing:
        raise SystemExit(f"{relative} missing required actions: {missing}")


def main() -> int:
    _require(".github/workflows/build.yml", ("python -m tools.verify", '"3.10"', '"3.13"', "windows-clean-room"))
    for path in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
        _require_actions(path.relative_to(ROOT).as_posix())
    _require_actions(".github/workflows/codeql.yml", ("github/codeql-action/init", "github/codeql-action/analyze"))
    _require_actions(".github/workflows/dependency-review.yml", ("actions/dependency-review-action",))
    _require(".github/workflows/dependency-review.yml", ("fail-on-severity",))
    _require_actions(".github/workflows/security.yml", ("gitleaks/gitleaks-action", "ossf/scorecard-action", "github/codeql-action/upload-sarif"))
    _require_actions(".github/workflows/release-provenance.yml", ("actions/attest-build-provenance",))
    _require(".github/workflows/release-provenance.yml", ("python -m tools.verify",))
    validate_release_boundary(yaml.safe_load((ROOT / ".github/workflows/release-provenance.yml").read_text(encoding="utf-8")))
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
