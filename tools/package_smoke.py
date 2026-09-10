#!/usr/bin/env python3
"""Build twice, install the wheel cleanly, smoke all six tools, and audit it.

The command is deliberately repository-external at import time: a passing smoke
test must resolve the dataset embedded in the wheel, not a file in the checkout.
"""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
RUNTIME_CONSTRAINTS = ROOT / "constraints" / "runtime.txt"
DEV_CONSTRAINTS = ROOT / "constraints" / "dev.txt"
SOURCE_DATE_EPOCH = "1787184000"  # 2026-08-20T00:00:00Z


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _constraint_digest() -> str:
    digest = hashlib.sha256()
    for name in ("runtime.txt", "dev.txt"):
        digest.update((ROOT / "constraints" / name).read_bytes())
    return digest.hexdigest()


def _normalise_frozen(line: str) -> str:
    name, version = line.split("==", 1)
    return f"{name.lower().replace('_', '-')}=={version}"


def _run(command: list[str], cwd: pathlib.Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    # The installed-wheel smoke must never see the checkout through an inherited
    # interpreter path. Callers may opt in explicitly via ``env`` where needed.
    merged.pop("PYTHONPATH", None)
    merged.pop("PYTHONHOME", None)
    merged.update({
        "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PYTHONUTF8": "1",
        "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
    })
    if env:
        merged.update(env)
    completed = subprocess.run(command, cwd=cwd, env=merged, text=True, capture_output=True, check=False)
    if completed.returncode:
        if completed.stdout:
            print(completed.stdout, file=sys.stderr)
        if completed.stderr:
            print(completed.stderr, file=sys.stderr)
        raise SystemExit(f"command failed ({completed.returncode}): {' '.join(command)}")
    return completed


def _venv_python(directory: pathlib.Path) -> pathlib.Path:
    if os.name == "nt":
        return directory / "Scripts" / "python.exe"
    return directory / "bin" / "python"


def _build(outdir: pathlib.Path, cwd: pathlib.Path) -> pathlib.Path:
    _run([
        sys.executable, "-m", "build", "--wheel", "--no-isolation",
        "--outdir", str(outdir), str(ROOT)
    ], cwd=cwd)
    wheels = sorted(outdir.glob("cbsr_mcp-*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"expected one CBSR wheel in {outdir}, found {len(wheels)}")
    return wheels[0]


def main() -> int:
    DIST.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cbsr-package-smoke-") as raw_temp:
        temp = pathlib.Path(raw_temp)
        first = _build(temp / "wheel-a", temp)
        second = _build(temp / "wheel-b", temp)
        first_sha = _sha256(first)
        second_sha = _sha256(second)
        if first_sha != second_sha:
            raise SystemExit(f"wheel is not byte-reproducible: {first_sha} != {second_sha}")

        published_wheel = DIST / first.name
        shutil.copy2(first, published_wheel)

        venv = temp / "clean-venv"
        _run([sys.executable, "-m", "venv", str(venv)], cwd=temp)
        python = _venv_python(venv)
        cache = pathlib.Path(
            os.environ.get("CBSR_PIP_CACHE_DIR")
            or os.environ.get("PIP_CACHE_DIR")
            or temp / "pip-cache"
        )
        common_env = {"PIP_CACHE_DIR": str(cache)}
        wheelhouse = os.environ.get("CBSR_WHEELHOUSE")
        index_args = ["--no-index", "--find-links", wheelhouse] if wheelhouse else []
        _run([
            str(python), "-m", "pip", "install", *index_args, "--constraint", str(DEV_CONSTRAINTS),
            "pip", "setuptools", "wheel"
        ], cwd=temp, env=common_env)
        _run([
            str(python), "-m", "pip", "install", *index_args, "--constraint", str(RUNTIME_CONSTRAINTS),
            str(published_wheel)
        ], cwd=temp, env=common_env)

        smoke = r'''
import json
import warnings
warnings.simplefilter("error")
from cbsr_mcp import server
from cbsr_mcp.data.repository import DATA, RECORDS
from cbsr_mcp.tools import agentic
from cbsr_mcp.tools.registry import count as registry_count, definitions

action = {
    "action_id": "package-smoke-001", "origin": "US", "destination": "EU",
    "asset": "USDC", "amount": "100", "actor": "package-smoke",
    "counterparty": "cp-1", "as_of": "2026-08-20",
    "requested_at": "2026-08-20T10:00:00Z",
    "mandate": {
        "schema": "cbsr/policy-mandate/v1", "mandate_id": "package-smoke-mandate",
        "version": "1.0", "issued_by": "package-smoke-owner", "active": True,
        "valid_from": "2026-01-01", "valid_until": "2027-01-01", "max_amount": "1000",
        "assets": ["USDC"], "jurisdictions": ["US", "EU"],
        "prohibited_jurisdictions": ["CN"], "counterparties": ["cp-1"],
        "human_review": {"required": False, "amount_threshold": "500"},
        "audit_identity": {"subject_id": "agent:package-smoke", "actor_type": "agent",
                           "principal_id": "human:test-owner"}
    }
}
searched = agentic.search_evidence("reserve", "US", 2)
rule = agentic.get_rule("us-pss-reserve_backing-001")
evaluated = agentic.evaluate_action(action)
compared = agentic.compare_jurisdictions("US", "EU", ["reserve_backing"])
watched = agentic.watch_changes(jurisdiction="US")
audited = agentic.audit_decision(evaluated["receipt"])
result = {
    "version": DATA.get("version"),
    "records": len(RECORDS),
    "registered_tools": len(server.mcp._tool_manager._tools),
    "registry_tools": registry_count(),
    "agenticfi_capabilities": sorted(name for name in {item.name for item in definitions()} if name in {
        "search_evidence", "get_rule", "evaluate_action", "compare_jurisdictions", "watch_changes", "audit_decision"
    }),
    "search_count": searched["count"],
    "rule_id": rule["record"]["id"],
    "decision": evaluated["decision"]["outcome"],
    "execution_authorized": evaluated["decision"]["execution_authorized"],
    "comparison_count": compared["count"],
    "watch_due": len(watched["records_needing_review"]),
    "receipt_valid": audited["valid"],
    "signing_state": audited["signing_state"],
}
assert result["version"] == "0.11.0"
assert result["records"] == 152
assert result["registered_tools"] == result["registry_tools"]
assert len(result["agenticfi_capabilities"]) == 6
assert result["rule_id"] == "us-pss-reserve_backing-001"
assert result["decision"] == "review_required"
assert result["execution_authorized"] is False
assert result["receipt_valid"] is True
assert result["signing_state"] == "unsigned"
print(json.dumps(result, sort_keys=True))
'''
        smoke_result = _run([str(python), "-c", smoke], cwd=temp, env={
            **common_env, "PYTHONWARNINGS": "error", "PYTHONPATH": ""
        })
        smoke_data = json.loads(smoke_result.stdout.strip().splitlines()[-1])

        purelib = _run([
            str(python), "-c", "import sysconfig; print(sysconfig.get_paths()['purelib'])"
        ], cwd=temp).stdout.strip()
        freeze = _run([str(python), "-m", "pip", "freeze", "--all"], cwd=temp).stdout.splitlines()
        auditable = [
            line for line in freeze
            if not line.lower().startswith("cbsr-mcp==") and not line.lower().startswith("cbsr-mcp @")
        ]
        audit_requirements = temp / "audit-requirements.txt"
        audit_requirements.write_text("\n".join(auditable) + "\n", encoding="utf-8", newline="\n")
        audit_path = DIST / "pip-audit.json"
        snapshot_raw = os.environ.get("CBSR_OFFLINE_AUDIT_SNAPSHOT")
        if snapshot_raw:
            snapshot_path = pathlib.Path(snapshot_raw).resolve()
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
            if snapshot.get("constraints_sha256") != _constraint_digest():
                raise SystemExit("offline audit snapshot does not match the committed dependency lock")
            if snapshot.get("known_vulnerabilities"):
                raise SystemExit("offline audit snapshot contains known vulnerabilities")
            covered = {_normalise_frozen(item) for item in snapshot.get("packages", [])}
            installed = {_normalise_frozen(item) for item in auditable if "==" in item}
            missing_from_snapshot = sorted(installed - covered)
            if missing_from_snapshot:
                raise SystemExit(
                    "offline audit snapshot does not cover: " + ", ".join(missing_from_snapshot)
                )
            audit_status = "passed_locked_graph_against_2026-08-20_live_snapshot"
            audit_evidence = snapshot_path.relative_to(ROOT).as_posix()
        else:
            audit_cache = pathlib.Path(os.environ.get("CBSR_PIP_AUDIT_CACHE_DIR", temp / "pip-audit-cache"))
            _run([
                sys.executable, "-m", "pip_audit", "--requirement", str(audit_requirements),
                "--no-deps", "--disable-pip",
                "--format", "json", "--output", str(audit_path),
                "--progress-spinner", "off", "--cache-dir", str(audit_cache), "--strict"
            ], cwd=temp, env={"PIP_CACHE_DIR": str(cache)})
            audit_status = "passed_no_known_vulnerabilities_live"
            audit_evidence = audit_path.relative_to(ROOT).as_posix()
        _run([sys.executable, "tools/license_report.py"], cwd=ROOT, env={
            "CBSR_LICENSE_PATH": purelib
        })

        resolved = json.loads(_run([
            str(python), "-c",
            "import importlib.metadata as m,json; print(json.dumps({n:m.version(n) for n in "
            "['cbsr-mcp','mcp','pydantic','pydantic-settings']}))"
        ], cwd=temp).stdout)
        report = {
            "schema": "cbsr/package-smoke/v1",
            "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "wheel": published_wheel.name,
            "wheel_sha256": first_sha,
            "reproducible_builds": 2,
            "warning_policy": "error",
            "resolved_runtime": resolved,
            "smoke": smoke_data,
            "pip_audit": audit_status,
            "pip_audit_evidence": audit_evidence,
            "license_inventory": "dist/licenses.json",
        }
        (DIST / "package-smoke.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8", newline="\n",
        )

    print(f"package smoke passed: 2 reproducible wheels, clean install, 6 tools, warning-free, audit clean ({first_sha})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
