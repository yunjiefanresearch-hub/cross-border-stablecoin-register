#!/usr/bin/env python3
"""
CBSR public-stats collector: PyPI + Zenodo. No auth, stdlib only.

Appends one timestamped JSON object per run to metrics/public_stats.jsonl.
Run locally (`python metrics/pull_public_stats.py`) or from the weekly workflow.

Signals it captures:
  - PyPI downloads for cbsr-mcp (install layer, NOT usage: see runbook §0)
  - Zenodo views/downloads for the register DOI (version-level, timestamped)
"""
from __future__ import annotations
import json, os, sys, time, urllib.request, urllib.error

PYPI_PKG   = os.environ.get("CBSR_PYPI_PKG", "cbsr-mcp")
ZENODO_ID  = os.environ.get("CBSR_ZENODO_ID", "20730358")   # from DOI 10.5281/zenodo.20730358
OUT        = os.environ.get("CBSR_STATS_OUT", os.path.join(os.path.dirname(__file__), "public_stats.jsonl"))
UA         = {"User-Agent": "cbsr-stats/1.0 (+https://github.com/yunjiefanresearch-hub)"}

def _get(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def pypi():
    try:
        d = _get(f"https://pypistats.org/api/packages/{PYPI_PKG}/recent")
        return {"ok": True, **d.get("data", {})}
    except urllib.error.HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}", "note": "404 = package not published / no data yet"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def zenodo():
    try:
        d = _get(f"https://zenodo.org/api/records/{ZENODO_ID}")
        s = d.get("stats", {})
        return {"ok": True, "version": d.get("metadata", {}).get("version"),
                "views": s.get("views"), "downloads": s.get("downloads"),
                "unique_views": s.get("unique_views"), "unique_downloads": s.get("unique_downloads")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def main():
    rec = {"captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "pypi": pypi(), "zenodo": zenodo()}
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    json.dump(rec, sys.stdout, ensure_ascii=False, indent=2); print()

if __name__ == "__main__":
    main()
