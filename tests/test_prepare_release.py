# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
"""Release staging must reject stale evidence and exclude historical artifacts."""
import json

import pytest

from tools import prepare_release as release


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    monkeypatch.setattr(release, "ROOT", tmp_path)
    evidence = tmp_path / "artifacts/validation"
    monkeypatch.setattr(release.verify, "EVIDENCE_DIR", evidence)
    monkeypatch.setattr(release.verify, "_source_fingerprint", lambda: "f" * 64)
    (tmp_path / "pyproject.toml").write_text('[project]\nversion = "0.11.0.post1"\n', encoding="utf-8")
    put(tmp_path / "dataset.json", {"version": "0.11.0"})
    request = {"schema": "cbsr/engineering-release-request/v1", "version": "0.11.0.post1",
               "tag": "v0.11.0.post1", "dataset_version": "0.11.0", "title": "Engineering update",
               "classification": "engineering-update-only", "maintainer_authorized": True,
               "independent_reviews_completed": False, "gold_badge_awarded": False}
    put(tmp_path / "delivery/release-request.json", request)
    dist = tmp_path / "dist"
    dist.mkdir()
    wheel = dist / "cbsr_mcp-0.11.0.post1-py3-none-any.whl"
    wheel.write_bytes(b"current version fixture")
    (dist / "cbsr_mcp-0.11.0-py3-none-any.whl").write_bytes(b"historical artifact: must not stage")
    (dist / "cbsr-0.11.0.cdx.json").write_text("old SBOM", encoding="utf-8")
    put(dist / "cbsr-0.11.0.post1.cdx.json", {"bomFormat": "CycloneDX"})
    put(dist / "licenses.json", {"licenses": []})
    audit = {"dependencies": [{"name": "example", "version": "1", "vulns": []}]}
    put(dist / "pip-audit.json", audit)
    put(evidence / "development-pip-audit.json", audit)
    smoke = {"wheel": wheel.name, "wheel_sha256": release.sha(wheel), "reproducible_builds": 2,
             "resolved_runtime": {"cbsr-mcp": "0.11.0.post1"},
             "pip_audit": "passed_no_known_vulnerabilities_live"}
    put(dist / "package-smoke.json", smoke)
    count = 2 * len(release.verify.GENERATION_STEPS) + len(release.verify.VALIDATION_STEPS) + 4
    put(evidence / "verify-summary.json", {"status": "passed", "version": "0.11.0.post1",
        "dataset_version": "0.11.0", "step_count": count, "steps_completed": ["fixture"] * count,
        "source_fingerprint_sha256": "f" * 64, "package_smoke": smoke})
    locks = tmp_path / "constraints"
    locks.mkdir()
    names = ("runtime-hashes.txt", "dev-hashes.txt", "quality-hashes.txt")
    for name in names:
        (locks / name).write_text("fixture lock", encoding="utf-8")
    put(evidence / "development-audit-binding.json", {"status": "passed", "exit_code": 0, "errors": [],
        "locks_sha256": {name: release.sha(locks / name) for name in names}})
    notes = tmp_path / "docs/releases/UPDATE_v0.11.0.post1.md"
    notes.parent.mkdir(parents=True)
    notes.write_text("Engineering update; no Gold or independent review claimed.", encoding="utf-8")
    return tmp_path


def test_release_stages_only_current_version_with_complete_checksums(inputs):
    output = inputs / "stage"
    result = release.prepare(output, "a" * 40, "push", "refs/heads/main")
    assert result["tag"] == "v0.11.0.post1"
    names = {path.name for path in (output / "assets").iterdir()}
    assert "cbsr_mcp-0.11.0-py3-none-any.whl" not in names
    assert "cbsr-0.11.0.cdx.json" not in names
    checksums = (output / "assets/SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert {line.split("  ")[1] for line in checksums} == names - {"SHA256SUMS"}
    for line in checksums:
        digest, name = line.split("  ")
        assert release.sha(output / "assets" / name) == digest
    manifest = release.read_json(output / "assets/release-manifest.json")
    assert manifest["source_commit"] == "a" * 40
    assert manifest["gold_badge_awarded"] is False


@pytest.mark.parametrize("field,value", [("status", "failed"), ("version", "0.11.0"),
    ("source_fingerprint_sha256", "old"), ("step_count", 1), ("steps_completed", [])])
def test_release_rejects_stale_or_incomplete_canonical_evidence(inputs, field, value):
    path = inputs / "artifacts/validation/verify-summary.json"
    document = release.read_json(path)
    document[field] = value
    put(path, document)
    with pytest.raises(ValueError, match="canonical"):
        release.prepare(inputs / "stage", "a" * 40)


def test_release_rejects_mutated_wheel(inputs):
    (inputs / "dist/cbsr_mcp-0.11.0.post1-py3-none-any.whl").write_bytes(b"changed")
    with pytest.raises(ValueError, match="wheel"):
        release.prepare(inputs / "stage", "a" * 40)


def test_release_rejects_old_lock_audit(inputs):
    (inputs / "constraints/dev-hashes.txt").write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="current locks"):
        release.prepare(inputs / "stage", "a" * 40)


@pytest.mark.parametrize("row", [{"vulns": [{"id": "test"}]}, {"vulns": [], "skip_reason": "test"}, {}])
def test_release_rejects_unsafe_audit(inputs, row):
    put(inputs / "dist/pip-audit.json", {"dependencies": [row]})
    with pytest.raises(ValueError, match="audit"):
        release.prepare(inputs / "stage", "a" * 40)


@pytest.mark.parametrize("field,value", [("gold_badge_awarded", True), ("maintainer_authorized", False),
    ("independent_reviews_completed", True), ("tag", "v0.11.0"), ("title", "bad\noutput=value")])
def test_release_cannot_expand_the_authorized_scope(inputs, field, value):
    path = inputs / "delivery/release-request.json"
    document = release.read_json(path)
    document[field] = value
    put(path, document)
    with pytest.raises(ValueError):
        release.prepare(inputs / "stage", "a" * 40)


@pytest.mark.parametrize("event,ref", [("push", "refs/heads/other"), ("release", "refs/tags/v0.11.0")])
def test_release_rejects_wrong_publication_ref(inputs, event, ref):
    with pytest.raises(ValueError):
        release.prepare(inputs / "stage", "a" * 40, event, ref)


def test_release_refuses_to_reuse_old_staging(inputs):
    output = inputs / "stage"
    output.mkdir()
    with pytest.raises(FileExistsError):
        release.prepare(output, "a" * 40)
