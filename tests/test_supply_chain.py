# Copyright the Cross-Border Stablecoin Register contributors.
# SPDX-License-Identifier: Apache-2.0
import hashlib
import pathlib
import subprocess
import sys
import zipfile

import pytest
import yaml

from tools.install_local_wheel import install_command, write_wheel_requirement
from tools.package_smoke import package_install_command
from tools.verify_security_governance import ROOT, pinned_action_names, validate_release_boundary


def test_local_wheel_requirement_has_exact_hash_and_escaped_file_uri(tmp_path):
    folder = tmp_path / "space and 日本語"
    folder.mkdir()
    wheel = folder / "cbsr_mcp-0.11.0-py3-none-any.whl"
    wheel.write_bytes(b"wheel test fixture\x00\xff")
    manifest = tmp_path / "local-wheel.txt"
    expected = hashlib.sha256(wheel.read_bytes()).hexdigest()
    assert write_wheel_requirement(wheel, manifest) == expected
    assert manifest.read_bytes() == (
        f"cbsr-mcp @ {wheel.resolve().as_uri()} --hash=sha256:{expected}\n"
    ).encode("utf-8")
    assert "%20" in manifest.read_text(encoding="utf-8")


@pytest.mark.parametrize("name", ["other-1-py3-none-any.whl", "cbsr_mcp-1.tar.gz", "cbsr_mcp-1-py3-none-any.whl.bak"])
def test_local_installer_rejects_non_cbsr_wheel_inputs(tmp_path, name):
    path = tmp_path / name
    path.write_bytes(b"not a permitted wheel")
    with pytest.raises(ValueError):
        write_wheel_requirement(path, tmp_path / "requirements.txt")


def test_local_install_cannot_download_or_resolve_unhashed_dependencies():
    command = install_command("python", pathlib.Path("local-wheel.txt"))
    assert command[:4] == ["python", "-m", "pip", "install"]
    for flag in ["--require-hashes", "--only-binary=:all:", "--no-index", "--no-deps"]:
        assert flag in command


@pytest.mark.parametrize("uses", ["actions/checkout@v5", "actions/checkout@main", "actions/checkout@abc123", "docker://alpine:latest"])
def test_workflow_gate_rejects_mutable_action_references(uses):
    with pytest.raises(ValueError):
        pinned_action_names({"jobs": {"test": {"steps": [{"uses": uses}]}}})


def test_workflow_gate_accepts_full_shas_and_local_actions():
    expected = "actions/checkout"
    workflow = {"jobs": {"test": {"steps": [
        {"uses": expected + "@" + "a" * 40},
        {"uses": "./.github/actions/check"},
        {"uses": "docker://example/image@sha256:" + "b" * 64},
        {"run": "python -m pytest"},
    ]}}}
    assert pinned_action_names(workflow) == {expected}


def test_workflow_gate_also_checks_reusable_workflow_jobs():
    with pytest.raises(ValueError):
        pinned_action_names({"jobs": {"test": {"uses": "example/project/.github/workflows/check.yml@main"}}})


def test_runtime_smoke_resolves_complete_hashed_graph_and_local_wheel():
    local = pathlib.Path("local-wheel.txt")
    command = package_install_command("python", local, [])
    assert "--require-hashes" in command
    assert "--only-binary=:all:" in command
    assert "--no-deps" not in command
    assert command.count("--requirement") == 2
    assert command[-1] == str(local)
    assert any(path.endswith("runtime-hashes.txt") for path in command)


def test_pip_accepts_exact_wheel_hash_and_rejects_tampering_without_network(tmp_path):
    wheel = tmp_path / "cbsr_mcp-0.0.1-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("cbsr_mcp-0.0.1.dist-info/METADATA", "Metadata-Version: 2.1\nName: cbsr-mcp\nVersion: 0.0.1\n")
        archive.writestr("cbsr_mcp-0.0.1.dist-info/WHEEL", "Wheel-Version: 1.0\nGenerator: cbsr-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        archive.writestr("cbsr_mcp-0.0.1.dist-info/RECORD", "")
    manifest = tmp_path / "wheel.txt"
    digest = write_wheel_requirement(wheel, manifest)
    command = install_command(sys.executable, manifest)
    command.insert(3, "--isolated")
    command.extend(["--dry-run", "--ignore-installed", "--no-cache-dir", "--disable-pip-version-check"])
    valid = subprocess.run(command, capture_output=True, text=True, check=False)
    assert valid.returncode == 0, valid.stdout + valid.stderr
    manifest.write_text(manifest.read_text(encoding="utf-8").replace(digest, "0" * 64), encoding="utf-8")
    invalid = subprocess.run(command, capture_output=True, text=True, check=False)
    assert invalid.returncode != 0
    assert "DO NOT MATCH THE HASHES" in invalid.stderr


def release_workflow():
    return yaml.safe_load((ROOT / ".github/workflows/release-provenance.yml").read_text(encoding="utf-8"))


def test_release_write_privileges_are_isolated_from_builds():
    validate_release_boundary(release_workflow())


@pytest.mark.parametrize("job", ["verify-wheel", "attest-wheel"])
def test_release_gate_rejects_extra_write_permissions(job):
    document = release_workflow()
    document["jobs"][job]["permissions"]["contents"] = "write"
    with pytest.raises(ValueError, match="permissions"):
        validate_release_boundary(document)


@pytest.mark.parametrize("job", ["attest-wheel", "publish-release-assets"])
def test_release_gate_rejects_repository_execution_in_privileged_jobs(job):
    document = release_workflow()
    document["jobs"][job]["steps"].append({"run": "python -m tools.verify"})
    with pytest.raises(ValueError, match="only upload"):
        validate_release_boundary(document)
