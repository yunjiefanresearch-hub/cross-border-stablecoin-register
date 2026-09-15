# Copyright the CBSR contributors.
# SPDX-License-Identifier: Apache-2.0
import json
from types import SimpleNamespace

import pytest

from tools import audit_locked_dependencies as audit


def test_audit_covers_dev_quality_and_included_runtime_without_resolving(tmp_path):
    command = audit.audit_command(tmp_path / "audit.json")
    assert command.count("--requirement") == 3
    assert str(audit.ROOT / "constraints/runtime-hashes.txt") in command
    assert str(audit.ROOT / "constraints/dev-hashes.txt") in command
    assert str(audit.ROOT / "constraints/quality-hashes.txt") in command
    assert "-r runtime-hashes.txt" in (audit.ROOT / "constraints/dev-hashes.txt").read_text(encoding="utf-8")
    assert all(flag in command for flag in ("--require-hashes", "--disable-pip", "--strict"))
    assert "--ignore-vuln" not in command


@pytest.mark.parametrize("exit_code", [0, 1, 2])
def test_audit_preserves_failure_and_binds_locks(tmp_path, monkeypatch, exit_code):
    monkeypatch.setenv("CBSR_EVIDENCE_DIR", str(tmp_path))
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=exit_code))
    monkeypatch.setattr(audit, "expected_dependencies", lambda: {("pytest", "9.1.1")})
    (tmp_path / "development-pip-audit.json").write_text(
        json.dumps({"dependencies": [{"name": "pytest", "version": "9.1.1", "vulns": []}]}), encoding="utf-8")
    assert audit.main() == exit_code
    report = json.loads((tmp_path / "development-audit-binding.json").read_text(encoding="utf-8"))
    assert report["status"] == ("passed" if exit_code == 0 else "failed")
    assert set(report["locks_sha256"]) == set(audit.LOCKS)
    assert all(len(digest) == 64 for digest in report["locks_sha256"].values())


def test_real_audit_parser_covers_every_marker_selected_pin(tmp_path):
    from pip_audit._dependency_source.requirement import RequirementSource
    paths = [audit.ROOT / "constraints" / name for name in audit.LOCKS]
    source = RequirementSource(paths, require_hashes=True, disable_pip=True)
    actual = {(audit.canonicalize_name(dependency.name), str(dependency.version)) for dependency in source.collect()}
    assert actual == audit.expected_dependencies()
    assert {"mcp", "pypdf", "pytest", "coverage"} <= {name for name, version in actual}


@pytest.mark.parametrize("rows", [[], [{"name": "pytest", "version": "9.1.1", "vulns": [{"id": "test"}]}]])
def test_success_exit_cannot_hide_incomplete_or_vulnerable_output(tmp_path, monkeypatch, rows):
    monkeypatch.setenv("CBSR_EVIDENCE_DIR", str(tmp_path))
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0))
    monkeypatch.setattr(audit, "expected_dependencies", lambda: {("pytest", "9.1.1")})
    (tmp_path / "development-pip-audit.json").write_text(json.dumps({"dependencies": rows}), encoding="utf-8")
    assert audit.main() == 1
