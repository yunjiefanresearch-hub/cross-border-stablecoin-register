#!/usr/bin/env python3
"""Generate a deterministic CycloneDX 1.5 SBOM for the declared CBSR package surface."""
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
import pathlib
import re
try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10
    import tomli as tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _name(spec: str) -> str:
    return re.split(r"[<>=!~\[; ]", spec, maxsplit=1)[0]


def main() -> int:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    specs = list(project.get("dependencies", []))
    for group in (project.get("optional-dependencies") or {}).values():
        specs.extend(group)
    components = []
    for spec in sorted(set(specs), key=str.lower):
        name = _name(spec)
        try:
            resolved = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            resolved = "not-installed"
        components.append({
            "type": "library",
            "name": name,
            "version": resolved,
            "purl": f"pkg:pypi/{name.lower()}@{resolved}" if resolved != "not-installed" else None,
            "properties": [{"name": "cbsr:declared-requirement", "value": spec}],
        })
    for component in components:
        if component["purl"] is None:
            del component["purl"]
    bom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": "urn:uuid:2b11306d-ec40-5d68-b049-cbsr00001100",
        "version": 1,
        "metadata": {
            "timestamp": "2026-08-20T00:00:00Z",
            "component": {
                "type": "application",
                "name": project["name"],
                "version": project["version"],
                "licenses": [{"license": {"id": "Apache-2.0"}}],
            },
        },
        "components": components,
    }
    out = ROOT / "dist" / f"cbsr-{project['version']}.cdx.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(bom, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(components)} declared components)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
