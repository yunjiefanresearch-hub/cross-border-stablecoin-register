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


def _workflow_events(workflow: dict) -> dict:
    """Return the event mapping under either YAML 1.1 or 1.2 parsing."""
    events = workflow.get("on") if "on" in workflow else workflow.get(True)
    if not isinstance(events, dict):
        raise ValueError("release workflow must declare an explicit event mapping")
    return events


def _normalized_run(step: dict) -> str:
    command = step.get("run")
    if not isinstance(command, str):
        raise ValueError("reviewed release shell must be a string")
    return " ".join(command.replace("\\\n", " ").split())


def validate_release_boundary(workflow: dict) -> None:
    """Keep source execution out of the signing and release-write jobs."""
    pinned_action_names(workflow)
    validate_default_permissions(workflow)
    events = _workflow_events(workflow)
    if set(events) != {"release", "push", "workflow_dispatch"}:
        raise ValueError("release workflow has an unreviewed trigger")
    if events["release"] != {"types": ["published"]}:
        raise ValueError("release assets may only follow a published release")
    if events["push"] != {
        "branches": ["main"],
        "paths": ["delivery/release-request.json"],
    }:
        raise ValueError("publication pushes must be limited to the main release request")
    if events["workflow_dispatch"] not in (None, {}):
        raise ValueError("manual verification must not accept publication inputs")

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

    verifier = jobs["verify-wheel"]
    if verifier.get("outputs") != {
        "tag": "${{ steps.release.outputs.tag }}",
        "title": "${{ steps.release.outputs.title }}",
        "wheel": "${{ steps.release.outputs.wheel }}",
    }:
        raise ValueError("release metadata must come from the verified preparation step")
    verifier_steps = verifier.get("steps", [])
    canonical_index = next(
        (index for index, step in enumerate(verifier_steps)
         if isinstance(step, dict) and "python -m tools.verify" in str(step.get("run", ""))),
        None,
    )
    prepare_index = next(
        (index for index, step in enumerate(verifier_steps)
         if isinstance(step, dict) and step.get("id") == "release"),
        None,
    )
    if canonical_index is None or prepare_index is None or prepare_index <= canonical_index:
        raise ValueError("release preparation must follow canonical verification")
    if _normalized_run(verifier_steps[prepare_index]) != (
        "python -m tools.prepare_release --output artifacts/release"
    ):
        raise ValueError("release preparation command is not the reviewed entry point")
    artifact_name = "cbsr-release-evidence-${{ github.run_id }}"
    uploads = [step for step in verifier_steps
               if str(step.get("uses", "")).startswith("actions/upload-artifact@")]
    if len(uploads) != 1 or uploads[0].get("with") != {
        "name": artifact_name,
        "path": "artifacts/release/",
        "if-no-files-found": "error",
    }:
        raise ValueError("verification must upload only the prepared release directory")

    if jobs["attest-wheel"].get("needs") != "verify-wheel":
        raise ValueError("attestation requires successful verification")
    publisher = jobs["publish-release-assets"]
    if publisher.get("needs") != ["verify-wheel", "attest-wheel"]:
        raise ValueError("publication requires both verification and attestation")
    if publisher.get("if") != "github.event_name == 'release' || github.event_name == 'push'":
        raise ValueError("publication is limited to reviewed release and request events")
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
            if name != "publish-release-assets":
                raise ValueError("attestation cannot execute repository or shell code")

    downloads = {
        name: [step for step in jobs[name]["steps"]
               if str(step.get("uses", "")).startswith("actions/download-artifact@")]
        for name in expected_actions
    }
    for name, steps in downloads.items():
        if len(steps) != 1 or steps[0].get("with") != {
            "name": artifact_name,
            "path": "release-evidence",
        }:
            raise ValueError(f"{name} must consume the same-run release evidence")
    attest_steps = jobs["attest-wheel"]["steps"]
    attest = next(
        (step for step in attest_steps
         if str(step.get("uses", "")).startswith("actions/attest-build-provenance@")),
        None,
    )
    if attest is None or attest.get("with") != {
        "subject-path": "release-evidence/assets/${{ needs.verify-wheel.outputs.wheel }}"
    }:
        raise ValueError("attestation must name the verified current-version wheel")

    publisher_runs = [step for step in publisher["steps"] if "run" in step]
    expected_runs = {
        "github.event_name == 'push'": {
            "env": {
                "GH_TOKEN": "${{ secrets.GITHUB_TOKEN }}",
                "GH_REPO": "${{ github.repository }}",
                "RELEASE_TAG": "${{ needs.verify-wheel.outputs.tag }}",
                "RELEASE_TITLE": "${{ needs.verify-wheel.outputs.title }}",
                "RELEASE_COMMIT": "${{ github.sha }}",
            },
            "command": (
                'set -euo pipefail gh api --method POST "repos/$GH_REPO/git/refs" '
                '-f "ref=refs/tags/$RELEASE_TAG" -f "sha=$RELEASE_COMMIT" '
                'gh release create "$RELEASE_TAG" release-evidence/assets/* --verify-tag '
                '--title "$RELEASE_TITLE" --notes-file release-evidence/release-notes.md '
                '--repo "$GH_REPO"'
            ),
        },
        "github.event_name == 'release'": {
            "env": {
                "GH_TOKEN": "${{ secrets.GITHUB_TOKEN }}",
                "GH_REPO": "${{ github.repository }}",
                "RELEASE_TAG": "${{ github.event.release.tag_name }}",
            },
            "command": (
                'set -euo pipefail gh release upload "$RELEASE_TAG" '
                'release-evidence/assets/* --repo "$GH_REPO"'
            ),
        },
    }
    if len(publisher_runs) != len(expected_runs):
        raise ValueError("publisher must retain exactly the reviewed release commands")
    for step in publisher_runs:
        expected = expected_runs.get(step.get("if"))
        if (expected is None or step.get("shell") != "bash"
                or step.get("env") != expected["env"]
                or _normalized_run(step) != expected["command"]):
            raise ValueError("publisher shell or environment is outside the reviewed whitelist")


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
