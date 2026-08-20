#!/usr/bin/env python3
"""Create the deterministic, Git-history-free Windows/local deployment ZIP."""
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
import pathlib
import stat
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERSION = "0.11.0"
ARCHIVE_ROOT = "cross-border-stablecoin-register"
EXCLUDED_DIRS = {
    ".git", ".venv", ".pytest_cache", "__pycache__", "node_modules",
    "artifacts", ".tox", ".nox",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
ZIP_TIME = (2026, 8, 20, 0, 0, 0)


def _sha(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _files() -> list[pathlib.Path]:
    result = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.is_file() and path.suffix not in EXCLUDED_SUFFIXES and path.name != ".DS_Store":
            result.append(path)
    return sorted(result, key=lambda value: value.relative_to(ROOT).as_posix())


def main(output: str | None = None) -> int:
    destination = pathlib.Path(output or f"/workspace/CBSR-v{VERSION}-local-deploy-r4.zip").resolve()
    files = _files()
    required = {
        "LOCAL_DEPLOY_WINDOWS.md", "setup_windows.ps1", "verify_windows.ps1", "run_mcp.ps1",
        f"dist/cbsr_mcp-{VERSION}-py3-none-any.whl", f"dist/cbsr-{VERSION}.cdx.json",
        "dist/pip-audit.json", "dist/licenses.json", "dist/package-smoke.json",
        "constraints/runtime.txt", "constraints/dev.txt", "docs/validation/PLATFORM_EVIDENCE.md",
        "docs/validation/LOCAL_LINUX_MATRIX.md", "docs/validation/local-linux-matrix.json",
        "docs/validation/pip-audit-snapshot-2026-08-20.json",
        "docs/validation/A_REPRODUCIBILITY_CLOSEOUT.md",
        "docs/validation/R3_REGULATORY_ARCHITECTURE_CLOSEOUT.md",
        "docs/validation/R4_AGENTICFI_RESEARCH_GOVERNANCE_CLOSEOUT.md",
        "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md",
        "research/agenticfi_evaluation.json", "research/AGENTICFI_EVALUATION_REPORT.md",
        "research/research_manifest.json", "research/claims/claims_ledger.csv",
        "analysis/dpg_evidence_matrix.json", "analysis/gdc_mapping.json",
        "analysis/dpi_safeguards_mapping.json", "analysis/sdg_mapping.json",
        "delivery/TRANSFORMATION_LOG.md", "delivery/BASELINE_REPRODUCTION.md",
        "delivery/RISK_REGISTER.md", "delivery/DECISION_LOG.md",
        "delivery/COMPATIBILITY_MATRIX.md", "delivery/MIGRATION_NOTES_v0.11.md",
        "delivery/ROLLBACK_NOTES_v0.11.md", "delivery/PR_STACK_PLAN.md",
        "delivery/FINAL_SCORECARD.md", "delivery/delivery_manifest.json",
    }
    present = {path.relative_to(ROOT).as_posix() for path in files}
    missing = sorted(required - present)
    if missing:
        raise SystemExit("release inputs missing: " + ", ".join(missing))

    with tempfile.TemporaryDirectory(prefix="cbsr-release-") as temp:
        temp_root = pathlib.Path(temp)
        checksums = []
        for rel in sorted(value for value in present if value.startswith("dist/")):
            checksums.append(f"{_sha(ROOT / rel)}  {rel}")
        checksum_path = temp_root / "SHA256SUMS"
        checksum_path.write_text("\n".join(checksums) + "\n", encoding="utf-8")
        manifest_path = temp_root / "RELEASE_MANIFEST.json"
        summary_path = ROOT / "artifacts" / "validation" / "verify-summary.json"
        if not summary_path.is_file():
            raise SystemExit("canonical verification evidence missing; run python -m tools.verify first")
        verification = json.loads(summary_path.read_text(encoding="utf-8"))
        if verification.get("status") != "passed":
            raise SystemExit("latest canonical verification did not pass")
        matrix = json.loads((ROOT / "docs/validation/local-linux-matrix.json").read_text(encoding="utf-8"))
        if matrix.get("status") != "passed" or len(matrix.get("versions", [])) != 4:
            raise SystemExit("current four-version local Linux matrix is incomplete")
        if matrix.get("shared_source_fingerprint_sha256") != verification.get("source_fingerprint_sha256"):
            raise SystemExit("local Linux matrix predates the current source fingerprint")
        if matrix.get("shared_wheel_sha256") != verification.get("package_smoke", {}).get("wheel_sha256"):
            raise SystemExit("local Linux matrix wheel differs from the latest canonical package")
        current_constraints = hashlib.sha256()
        for name in ("runtime.txt", "dev.txt"):
            current_constraints.update((ROOT / "constraints" / name).read_bytes())
        if verification.get("constraints_sha256") != current_constraints.hexdigest():
            raise SystemExit("canonical verification evidence predates the committed dependency lock")
        manifest_path.write_text(json.dumps({
            "schema": "cbsr/local-release-manifest/v1",
            "version": VERSION,
            "generated": "2026-08-20",
            "file_count_excluding_manifest": len(files),
            "local_verification": verification,
            "external_platform_evidence": {
                "github_actions_python_3_10_to_3_13": "not established by this local ZIP build",
                "windows_11_clean_room": "not established by this Linux ZIP build",
                "instructions": "docs/validation/PLATFORM_EVIDENCE.md",
            },
            "local_linux_matrix": {
                "status": "passed",
                "evidence": "docs/validation/local-linux-matrix.json",
                "scope": "Python 3.10-3.13 local Linux; not GitHub Actions or Windows",
                "source_fingerprint_sha256": matrix["shared_source_fingerprint_sha256"],
                "wheel_sha256": matrix["shared_wheel_sha256"],
            },
            "legal_currentness_certificate": False,
            "independent_reviews": {
                "legal_second_review": "not_completed",
                "security_review": "not_completed",
                "whitepaper_peer_review": "not_completed",
                "qualitative_second_coder": "not_completed",
            },
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        members = [(path, path.relative_to(ROOT).as_posix()) for path in files]
        members.extend([(checksum_path, "SHA256SUMS"), (manifest_path, "RELEASE_MANIFEST.json")])
        destination.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for source, rel in sorted(members, key=lambda item: item[1]):
                info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{rel}", ZIP_TIME)
                info.compress_type = zipfile.ZIP_DEFLATED
                mode = source.stat().st_mode
                info.external_attr = ((stat.S_IMODE(mode) or 0o644) & 0xFFFF) << 16
                archive.writestr(info, source.read_bytes())

    digest = _sha(destination)
    sidecar = destination.with_suffix(destination.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {destination.name}\n", encoding="utf-8")
    print(json.dumps({"zip": str(destination), "bytes": destination.stat().st_size,
                      "files": len(files) + 2, "sha256": digest}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(_sys.argv[1] if len(_sys.argv) > 1 else None))
