#!/usr/bin/env python3
# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
"""Stage only the current verified engineering update, never old dist artifacts."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other locales.
import sys
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from tools import verify

ROOT = Path(__file__).resolve().parent.parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path.name}")
    return value


def validate_request(request: dict, version: str, dataset_version: str) -> None:
    if not re.fullmatch(r"\d+\.\d+\.\d+\.post[1-9]\d*", version):
        raise ValueError("engineering update must use a PEP 440 post-release version")
    expected = {
        "schema": "cbsr/engineering-release-request/v1",
        "version": version,
        "tag": "v" + version,
        "dataset_version": dataset_version,
        "classification": "engineering-update-only",
        "maintainer_authorized": True,
        "independent_reviews_completed": False,
        "gold_badge_awarded": False,
    }
    if any(request.get(key) != value for key, value in expected.items()):
        raise ValueError("release request does not match the authorized engineering-update scope")
    if version.split(".post", 1)[0] != dataset_version:
        raise ValueError("post-release must preserve the dataset base version")
    title = request.get("title")
    if not isinstance(title, str) or not title or len(title) > 160 or any(ord(c) < 32 for c in title):
        raise ValueError("release title must be a single printable line")


def validate_audit(document: dict) -> None:
    dependencies = document.get("dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        raise ValueError("missing dependency audit inventory")
    if any(not isinstance(row, dict) or row.get("vulns") != [] or "skip_reason" in row
           for row in dependencies):
        raise ValueError("dependency audit contains vulnerabilities, skipped or invalid packages")


def prepare(output: Path, commit: str, event: str = "", ref: str = "") -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("release must identify one exact source commit")
    version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    dataset = read_json(ROOT / "dataset.json")
    request = read_json(ROOT / "delivery/release-request.json")
    validate_request(request, version, dataset["version"])
    if event == "push" and ref != "refs/heads/main":
        raise ValueError("publication push must target main")
    if event == "release" and ref != "refs/tags/" + request["tag"]:
        raise ValueError("release tag must match the verified package")
    evidence = verify.EVIDENCE_DIR
    summary = read_json(evidence / "verify-summary.json")
    expected_count = 2 * len(verify.GENERATION_STEPS) + len(verify.VALIDATION_STEPS) + 4
    if (summary.get("status") != "passed" or summary.get("version") != version
            or summary.get("dataset_version") != dataset["version"]
            or summary.get("step_count") != expected_count
            or len(summary.get("steps_completed", [])) != expected_count
            or summary.get("source_fingerprint_sha256") != verify._source_fingerprint()):
        raise ValueError("canonical evidence is incomplete, failed or stale")
    wheel_name = f"cbsr_mcp-{version}-py3-none-any.whl"
    wheel = ROOT / "dist" / wheel_name
    smoke = read_json(ROOT / "dist/package-smoke.json")
    if (summary.get("package_smoke") != smoke or smoke.get("wheel") != wheel_name
            or smoke.get("wheel_sha256") != sha(wheel)
            or smoke.get("reproducible_builds") != 2
            or smoke.get("resolved_runtime", {}).get("cbsr-mcp") != version
            or smoke.get("pip_audit") != "passed_no_known_vulnerabilities_live"):
        raise ValueError("wheel does not match the reproducible live-audited canonical package")
    binding = read_json(evidence / "development-audit-binding.json")
    lock_names = ("runtime-hashes.txt", "dev-hashes.txt", "quality-hashes.txt")
    if (binding.get("status") != "passed" or binding.get("exit_code") != 0
            or binding.get("errors") != []
            or binding.get("locks_sha256") != {name: sha(ROOT / "constraints" / name) for name in lock_names}):
        raise ValueError("development audit failed or does not match current locks")
    validate_audit(read_json(evidence / "development-pip-audit.json"))
    validate_audit(read_json(ROOT / "dist/pip-audit.json"))
    notes = ROOT / "docs/releases" / f"UPDATE_v{version}.md"
    sources = [wheel, ROOT / "dist" / f"cbsr-{version}.cdx.json",
               ROOT / "dist/licenses.json", ROOT / "dist/package-smoke.json",
               ROOT / "dist/pip-audit.json", evidence / "verify-summary.json",
               evidence / "development-pip-audit.json", evidence / "development-audit-binding.json"]
    for source in [*sources, notes]:
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"missing or symlinked release input: {source.name}")
        source.resolve().relative_to(ROOT.resolve())
    # Fail if a caller tries to reuse a staging directory containing old artifacts.
    output.mkdir(parents=True, exist_ok=False)
    assets = output / "assets"
    assets.mkdir()
    for source in sources:
        shutil.copyfile(source, assets / source.name)
    shutil.copyfile(notes, output / "release-notes.md")
    manifest = {"schema": "cbsr/engineering-release-manifest/v1", "request": request,
                "source_commit": commit, "source_fingerprint_sha256": summary["source_fingerprint_sha256"],
                "artifact_sha256": {p.name: sha(p) for p in sorted(assets.iterdir())},
                "independent_reviews_completed": False, "gold_badge_awarded": False,
                "legal_currentness_certificate": False}
    (assets / "release-manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (assets / "SHA256SUMS").write_text("".join(f"{sha(p)}  {p.name}\n" for p in sorted(assets.iterdir())), encoding="utf-8", newline="\n")
    return {"tag": request["tag"], "title": request["title"], "wheel": wheel_name}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", default=os.environ.get("GITHUB_SHA", ""))
    args = parser.parse_args()
    values = prepare(args.output, args.commit, os.environ.get("GITHUB_EVENT_NAME", ""), os.environ.get("GITHUB_REF", ""))
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8", newline="\n") as handle:
            for key, value in values.items():
                handle.write(f"{key}={value}\n")
    print(json.dumps(values, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
