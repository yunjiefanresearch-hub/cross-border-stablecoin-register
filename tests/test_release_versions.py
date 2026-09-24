# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
"""An engineering post-release must not masquerade as newly reviewed source data."""
import json

import pytest

from tools import check_identifiers, governance_report, package_release, verify


def version_fixture(tmp_path, monkeypatch, package="0.11.0.post1", dataset="0.11.0", manifest=None, init=None):
    monkeypatch.setattr(check_identifiers, "ROOT", tmp_path)
    (tmp_path / "dataset.json").write_text(json.dumps({"version": dataset}), encoding="utf-8")
    (tmp_path / "mcp.json").write_text(json.dumps({
        "version": manifest or package, "dataset_version": dataset,
    }), encoding="utf-8")
    (tmp_path / "server.json").write_text(json.dumps({
        "version": package, "packages": [{"identifier": "cbsr-mcp", "version": package}],
    }), encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text(f'[project]\nversion = "{package}"\n', encoding="utf-8")
    init_path = tmp_path / "src" / "cbsr_mcp" / "__init__.py"
    init_path.parent.mkdir(parents=True)
    init_path.write_text(f'__version__ = "{init or package}"\n', encoding="utf-8")


def test_post_release_preserves_dataset_version(tmp_path, monkeypatch):
    version_fixture(tmp_path, monkeypatch)
    assert check_identifiers.check_versions() == []


@pytest.mark.parametrize("override", [
    {"manifest": "0.11.0"}, {"init": "0.11.0"}, {"package": "0.11.1"},
])
def test_release_rejects_package_or_dataset_drift(tmp_path, monkeypatch, override):
    version_fixture(tmp_path, monkeypatch, **override)
    assert check_identifiers.check_versions()


def test_manifest_cannot_mislabel_bundled_dataset(tmp_path, monkeypatch):
    version_fixture(tmp_path, monkeypatch)
    path = tmp_path / "mcp.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["dataset_version"] = "0.11.1"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    assert check_identifiers.check_versions() == [
        "mcp.json dataset_version must identify the actual bundled dataset version"
    ]


@pytest.mark.parametrize("field", ["server", "package"])
def test_registry_descriptor_rejects_stale_package_version(tmp_path, monkeypatch, field):
    version_fixture(tmp_path, monkeypatch)
    path = tmp_path / "server.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    if field == "server":
        registry["version"] = "0.11.0"
    else:
        registry["packages"][0]["version"] = "0.11.0"
    path.write_text(json.dumps(registry), encoding="utf-8")
    assert check_identifiers.check_versions() == [
        "server.json registry descriptor must identify the exact current package release"
    ]


def test_verification_summary_identifies_package_and_dataset_separately(tmp_path, monkeypatch):
    version_fixture(tmp_path, monkeypatch)
    constraints = tmp_path / "constraints"
    constraints.mkdir()
    for name in ("runtime.txt", "dev.txt"):
        (constraints / name).write_text("", encoding="utf-8")
    monkeypatch.setattr(verify, "ROOT", tmp_path)
    monkeypatch.setattr(verify, "EVIDENCE_DIR", tmp_path / "evidence")
    monkeypatch.setattr(verify, "_source_fingerprint", lambda: "f" * 64)
    monkeypatch.setattr(verify.platform, "platform", lambda: "test-platform")
    verify._write_summary("passed", ["fixture"])
    summary = json.loads((tmp_path / "evidence" / "verify-summary.json").read_text(encoding="utf-8"))
    assert summary["version"] == "0.11.0.post1"
    assert summary["dataset_version"] == "0.11.0"


def test_local_release_package_uses_current_software_version():
    project = verify.tomllib.loads((verify.ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert package_release.VERSION == project["project"]["version"]


def test_governance_evidence_points_at_current_package_sbom(tmp_path, monkeypatch):
    version_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(governance_report, "ROOT", tmp_path)
    security_row = next(row for row in governance_report._dpg() if row["indicator"] == "9A")
    assert "dist/cbsr-0.11.0.post1.cdx.json" in security_row["evidence_files"]
    assert "dist/cbsr-0.11.0.cdx.json" not in security_row["evidence_files"]


def test_make_setup_isolates_build_and_install_by_exact_package_version():
    makefile = (verify.ROOT / "Makefile").read_text(encoding="utf-8")
    assert 'LOCAL_WHEEL_DIR = artifacts/local-wheel/$(shell python -c "from tools.package_release import VERSION; print(VERSION)")' in makefile
    assert "setup: setup-deps" in makefile
    assert ".DEFAULT_GOAL := setup" in makefile
    assert '--outdir "$(LOCAL_WHEEL_DIR)"' in makefile
    assert '--wheel-dir "$(LOCAL_WHEEL_DIR)"' in makefile
    assert "tools/install_local_wheel.py" in makefile
    assert "rm " not in makefile and "Remove-Item" not in makefile
