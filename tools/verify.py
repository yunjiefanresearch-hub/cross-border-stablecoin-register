#!/usr/bin/env python3
"""The single canonical CBSR verification entry point.

CI, Windows, contributor docs and release packaging all call this module. It is
fail-fast and non-bootstrap: install the reviewed development graph first. The
verifier then proves committed-output freshness, second-pass determinism,
research reproduction, package reproducibility, clean wheel operation, all six
AgenticFi tools, warning-free import, vulnerability status and licence inventory.
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
import importlib.metadata
import json
import os
import pathlib
import platform
import subprocess
import sys
from typing import Iterable

from packaging.requirements import Requirement

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVIDENCE_DIR = pathlib.Path(os.environ.get("CBSR_EVIDENCE_DIR", ROOT / "artifacts" / "validation"))
if not EVIDENCE_DIR.is_absolute():
    EVIDENCE_DIR = ROOT / EVIDENCE_DIR

GENERATION_STEPS = [
    ("MCP registry manifest", "tools/sync_tool_manifest.py"),
    ("analysis", "scripts/build_analysis.py"),
    ("compose", "scripts/compose.py"),
    ("substrate", "scripts/substrate.py"),
    ("edge skeletons", "scripts/build_edge_skeletons.py"),
    ("stakeholders", "scripts/stakeholders.py"),
    ("verification worklist", "scripts/build_worklist.py"),
    ("legal event ontology", "tools/build_legal_event_ontology.py"),
    ("signal table", "scripts/gen_signal_table.py"),
    ("directed corridors", "scripts/build_corridors_directed.py"),
    ("dataset", "build.py"),
    ("corridor states", "scripts/build_corridor_states.py"),
    ("sensitivity", "scripts/build_sensitivity.py"),
    ("settlement", "scripts/build_settlement.py"),
    ("forward view", "scripts/build_forward_view.py"),
    ("forward sensitivity", "scripts/regen_forward_sensitivity.py"),
    ("API", "build_api.py"),
    ("pages", "build_pages.py"),
    ("site", "build_site.py"),
    ("research outputs", "tools/research_report.py"),
    ("AgenticFi evaluation", "tools/run_agenticfi_evaluation.py"),
    ("mixed-method research delivery", "tools/research_deliverables.py"),
    ("institutional whitepaper PDF", "tools/build_whitepaper_pdf.py"),
    ("governance and public-interest mappings", "tools/governance_report.py"),
    ("formal delivery reports", "tools/delivery_report.py"),
]

VALIDATION_STEPS = [
    ("dependency hash lock/provenance consistency", "tools/hash_constraints.py", "--check"),
    ("complete development and quality dependency audit", "tools/audit_locked_dependencies.py"),
    ("identifier gate", "tools/check_identifiers.py"),
    ("MCP documentation gate", "tools/check_docs_sync.py"),
    ("internal Markdown link gate", "tools/check_internal_links.py"),
    ("README count gate", "check_readme_counts.py"),
    ("invariants", "run_invariants.py"),
    ("legacy negative tests", "run_negative_tests.py"),
    ("directed corridor gates", "tools/verify_corridors_directed.py"),
    ("directed negative tests", "tools/run_negative_tests.py"),
    ("class-rule proof", "tools/recompute_classes.py", "--prove-tier2-inert"),
    ("migration no-op", "tools/migrate_from_v0_9_92.py", "--check", "analysis/computed_corridors_directed.json"),
    ("schema cross-check", "tools/schema_reference_crosscheck.py"),
    ("verification backlog", "tools/check_verification_backlog.py"),
    ("persisted review metadata", "tools/migrate_review_fields.py", "--check"),
    ("legal event ontology", "tools/validate_legal_events.py"),
    ("freshness and AgenticFi tests", "-m", "pytest", "-q"),
    ("research reproduction", "tools/verify_research_reproduction.py"),
    ("AgenticFi scenario, schema, receipt and pilot delivery", "tools/verify_agenticfi_delivery.py"),
    ("quantitative, qualitative, claims, dossier and whitepaper delivery", "tools/verify_research_delivery.py"),
    ("institutional whitepaper PDF contract", "tools/verify_whitepaper_pdf.py"),
    ("DPG, SDG, GDC and DPI governance delivery", "tools/verify_governance_delivery.py"),
    ("repository high-confidence secret scan", "tools/secret_scan.py"),
    ("security workflow and governance evidence delivery", "tools/verify_security_governance.py"),
    ("formal transformation and release delivery", "tools/verify_delivery.py"),
]

REPRO_FILES = (
    "dataset.json", "COVERAGE.md", "records.md", "index.html", "console.html", "corridors.html",
    "mcp.json", "DPG_STANDARD.md",
)
REPRO_DIRS = ("analysis", "api", "research", "delivery", "docs/whitepaper", "docs/governance", "docs/delivery")

SOURCE_FINGERPRINT_DIRS = ("src", "tools", "scripts", "tests", "schemas", ".github", "constraints")
SOURCE_FINGERPRINT_ROOTS = (
    "pyproject.toml", "record.schema.json", "build.py", "build_api.py", "build_pages.py",
    "build_site.py", "run_invariants.py", "run_negative_tests.py", "setup_windows.ps1",
    "verify_windows.ps1", "run_mcp.ps1", "pytest.ini", ".coveragerc", ".gitattributes", "Makefile",
)


class VerificationFailure(RuntimeError):
    pass


def _sha(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _constraint_pins() -> dict[str, str]:
    pins: dict[str, str] = {}
    for file_name in ("runtime.txt", "dev.txt"):
        path = ROOT / "constraints" / file_name
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "-")):
                continue
            requirement = Requirement(stripped)
            if requirement.marker is not None and not requirement.marker.evaluate():
                continue
            exact = [spec.version for spec in requirement.specifier if spec.operator == "=="]
            if len(exact) != 1 or len(list(requirement.specifier)) != 1:
                raise VerificationFailure(f"non-exact constraint in {path}: {line}")
            pins[requirement.name.lower().replace("_", "-")] = exact[0]
    return pins


def _preflight() -> None:
    missing = []
    for module in ("yaml", "jsonschema", "pytest", "pip_audit", "packaging"):
        try:
            __import__(module)
        except ModuleNotFoundError:
            missing.append(module)
    if sys.version_info[:2] == (3, 10):
        try:
            __import__("tomli")
        except ModuleNotFoundError:
            missing.append("tomli")
    if missing:
        raise VerificationFailure(
            "verification prerequisites are missing: " + ", ".join(missing) + "\n"
            "Install first with: python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt"
        )

    mismatches = []
    for name, expected in sorted(_constraint_pins().items()):
        try:
            actual = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            mismatches.append(f"{name}: missing (expected {expected})")
            continue
        if actual != expected:
            mismatches.append(f"{name}: {actual} (expected {expected})")
    if mismatches:
        raise VerificationFailure(
            "the active environment does not match committed constraints:\n  - "
            + "\n  - ".join(mismatches)
            + "\nRecreate the environment; do not patch it ad hoc."
        )
    print(f"PREFLIGHT OK: Python {platform.python_version()} and committed dependency constraints match.")


def _artifact_paths() -> Iterable[pathlib.Path]:
    for rel in REPRO_FILES:
        path = ROOT / rel
        if path.is_file():
            yield path
    for rel in REPRO_DIRS:
        directory = ROOT / rel
        if directory.is_dir():
            yield from sorted(path for path in directory.rglob("*") if path.is_file())


def _snapshot() -> dict[str, str]:
    return {
        path.relative_to(ROOT).as_posix(): _sha(path)
        for path in sorted(_artifact_paths(), key=lambda item: item.relative_to(ROOT).as_posix())
    }


def _source_fingerprint() -> str:
    """Fingerprint inputs so cross-interpreter evidence cannot be reused after edits."""
    paths: set[pathlib.Path] = set()
    for relative in SOURCE_FINGERPRINT_ROOTS:
        path = ROOT / relative
        if path.is_file():
            paths.add(path)
    paths.update(path for path in ROOT.glob("*.yaml") if path.is_file())
    for relative in SOURCE_FINGERPRINT_DIRS:
        directory = ROOT / relative
        if directory.is_dir():
            paths.update(path for path in directory.rglob("*") if path.is_file() and path.suffix not in {".pyc", ".pyo"})
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix()):
        relative = path.relative_to(ROOT).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        digest.update(bytes.fromhex(_sha(path)))
    return digest.hexdigest()


def _diff(left: dict[str, str], right: dict[str, str]) -> list[str]:
    keys = sorted(set(left) | set(right))
    return [key for key in keys if left.get(key) != right.get(key)]


def _run(label: str, args: list[str], completed: list[str]) -> None:
    command = [sys.executable, *args]
    print(f"\n[{len(completed) + 1:02d}] {label}: {' '.join(command)}", flush=True)
    env = os.environ.copy()
    source_paths = [str(ROOT / "src"), str(ROOT)]
    if env.get("PYTHONPATH"):
        source_paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(source_paths)
    result = subprocess.run(command, cwd=ROOT, env=env, check=False)
    if result.returncode:
        raise VerificationFailure(f"{label} failed with exit {result.returncode}")
    completed.append(label)
    print(f"RECHECK OK: {label}", flush=True)


def _run_generation(pass_number: int, completed: list[str]) -> None:
    for label, *args in GENERATION_STEPS:
        _run(f"generation pass {pass_number}: {label}", args, completed)


def _write_summary(status: str, completed: list[str], extra: dict | None = None) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    constraints = hashlib.sha256()
    for name in ("runtime.txt", "dev.txt"):
        constraints.update((ROOT / "constraints" / name).read_bytes())
    summary = {
        "schema": "cbsr/verification-summary/v2",
        "status": status,
        "version": "0.11.0",
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "constraints_sha256": constraints.hexdigest(),
        "source_fingerprint_sha256": _source_fingerprint(),
        "steps_completed": completed,
        "step_count": len(completed),
        "external_evidence": {
            "github_actions_python_3_10_to_3_13": "requires successful remote workflow run",
            "windows_clean_room": "requires successful windows-latest or physical Windows 11 run",
        },
    }
    if extra:
        summary.update(extra)
    (EVIDENCE_DIR / "verify-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )


def main() -> int:
    completed: list[str] = []
    try:
        _preflight()
        baseline = _snapshot()
        _run_generation(1, completed)
        first = _snapshot()
        drift = _diff(baseline, first)
        if drift:
            preview = "\n  - ".join(drift[:30])
            raise VerificationFailure(
                "committed/generated artifact drift detected after pass 1:\n  - " + preview
                + (f"\n  ... and {len(drift) - 30} more" if len(drift) > 30 else "")
                + "\nReview and commit regenerated outputs, then rerun the canonical verifier."
            )
        completed.append("committed artifact hash gate")
        print(f"RECHECK OK: committed artifact hash gate ({len(first)} artifacts unchanged)")

        _run_generation(2, completed)
        second = _snapshot()
        nondeterministic = _diff(first, second)
        if nondeterministic:
            raise VerificationFailure(
                "second generation pass was not byte-deterministic:\n  - "
                + "\n  - ".join(nondeterministic[:30])
            )
        completed.append("second-pass deterministic hash gate")
        print(f"RECHECK OK: second-pass deterministic hash gate ({len(second)} artifacts identical)")

        for label, *args in VALIDATION_STEPS:
            _run(label, args, completed)
        _run("CycloneDX SBOM", ["tools/generate_sbom.py"], completed)
        _run("reproducible package + clean-install + six-tool smoke + pip-audit", ["tools/package_smoke.py"], completed)

        package_report = json.loads((ROOT / "dist" / "package-smoke.json").read_text(encoding="utf-8"))
        _write_summary("passed", completed, {
            "reproducible_artifact_count": len(second),
            "generation_passes": 2,
            "package_smoke": package_report,
        })
        print(f"\nVERIFY OK: {len(completed)} atomic steps passed with immediate recheck.")
        print(f"Evidence: {EVIDENCE_DIR / 'verify-summary.json'}")
        return 0
    except VerificationFailure as error:
        _write_summary("failed", completed, {"failure": str(error)})
        print(f"\nVERIFY FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
