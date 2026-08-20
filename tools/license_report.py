#!/usr/bin/env python3
"""Emit installed-package licence metadata for review; unknown values remain explicit."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import importlib.metadata
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main() -> int:
    packages = []
    requested_path = os.environ.get("CBSR_LICENSE_PATH")
    distributions = importlib.metadata.distributions(path=[requested_path]) if requested_path else importlib.metadata.distributions()
    for dist in distributions:
        metadata = dist.metadata
        name = metadata.get("Name")
        if not name:
            continue
        expression = metadata.get("License-Expression") or metadata.get("License") or "UNKNOWN"
        packages.append({"name": name, "version": dist.version, "license": expression})
    packages.sort(key=lambda row: row["name"].lower())
    report = {
        "schema": "cbsr/license-inventory/v1",
        "generated": "2026-08-20",
        "scope": (
            "clean wheel-install environment"
            if requested_path
            else "packages installed in the interpreter used to run this script"
        ),
        "manual_review_required": any(row["license"] == "UNKNOWN" for row in packages),
        "packages": packages,
    }
    out = ROOT / "dist" / "licenses.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(packages)} packages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
