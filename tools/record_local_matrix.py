#!/usr/bin/env python3
"""Aggregate already-passed local Linux verifier evidence without relabelling it CI."""
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

ROOT = pathlib.Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "artifacts" / "validation"
OUT_JSON = ROOT / "docs" / "validation" / "local-linux-matrix.json"
OUT_MD = ROOT / "docs" / "validation" / "LOCAL_LINUX_MATRIX.md"
EXPECTED = ("3.10", "3.11", "3.12", "3.13")


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    rows = []
    for minor in EXPECTED:
        base = EVIDENCE / f"linux-python-{minor}"
        summary_path = base / "verify-summary.json"
        log_path = base / "verify.log"
        if not summary_path.is_file() or not log_path.is_file():
            raise SystemExit(f"missing local evidence for Python {minor}: {base}")
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if summary.get("status") != "passed" or int(summary.get("step_count", 0)) < 60:
            raise SystemExit(f"Python {minor} evidence is not a complete current canonical pass")
        if not str(summary.get("python", "")).startswith(f"{minor}."):
            raise SystemExit(f"Python {minor} evidence was produced by {summary.get('python')}")
        package = summary.get("package_smoke", {})
        rows.append({
            "requested_minor": minor,
            "python": summary["python"],
            "platform": summary["platform"],
            "status": summary["status"],
            "step_count": summary["step_count"],
            "generation_passes": summary["generation_passes"],
            "reproducible_artifact_count": summary["reproducible_artifact_count"],
            "constraints_sha256": summary["constraints_sha256"],
            "source_fingerprint_sha256": summary.get("source_fingerprint_sha256"),
            "wheel_sha256": package["wheel_sha256"],
            "pip_audit": package["pip_audit"],
            "warning_policy": package["warning_policy"],
            "log_sha256": _sha(log_path),
        })

    constraint_hashes = {row["constraints_sha256"] for row in rows}
    source_hashes = {row["source_fingerprint_sha256"] for row in rows}
    wheel_hashes = {row["wheel_sha256"] for row in rows}
    if len(constraint_hashes) != 1:
        raise SystemExit("matrix summaries were not produced from one constraint set")
    if None in source_hashes or len(source_hashes) != 1:
        raise SystemExit("matrix summaries were not produced from one source fingerprint")
    if len(wheel_hashes) != 1:
        raise SystemExit("wheel bytes differ across Python versions")

    payload = {
        "schema": "cbsr/local-linux-matrix/v1",
        "generated": "2026-08-20",
        "scope": "local Linux execution; not GitHub Actions evidence",
        "status": "passed",
        "versions": rows,
        "shared_constraints_sha256": rows[0]["constraints_sha256"],
        "shared_source_fingerprint_sha256": rows[0]["source_fingerprint_sha256"],
        "shared_wheel_sha256": rows[0]["wheel_sha256"],
        "external_gates": {
            "github_actions": "unverified_external",
            "windows_11": "unverified_external",
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    lines = [
        "# Local Linux Python matrix",
        "",
        "> This is evidence from local Linux execution on 2026-08-20. It is not a",
        "> substitute for a successful GitHub Actions run or a Windows 11 transcript.",
        "",
        "| Python | Canonical steps | Generated artifacts | Warning policy | Audit | Wheel SHA-256 |",
        "|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['python']} | {row['step_count']}/{row['step_count']} | "
            f"{row['reproducible_artifact_count']} × {row['generation_passes']} passes | "
            f"`{row['warning_policy']}` | `{row['pip_audit']}` | `{row['wheel_sha256']}` |"
        )
    lines.extend([
        "",
        f"All four runs used constraint digest `{rows[0]['constraints_sha256']}`, source fingerprint",
        f"`{rows[0]['source_fingerprint_sha256']}` and produced",
        "the same wheel bytes. Raw logs are transient build evidence; their SHA-256 values and",
        "the complete machine-readable results are recorded in `local-linux-matrix.json`.",
        "",
        "GitHub Actions and Windows remain external release gates as described in",
        "`PLATFORM_EVIDENCE.md`.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"recorded {len(rows)} local Linux passes in {OUT_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
