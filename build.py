#!/usr/bin/env python3
"""Validate records, compile the dataset, and regenerate the coverage map.

Flat-layout friendly: it finds files by name/content anywhere under the repo root,
so it works whether the files sit in folders or all at the top level.

Usage:  python build.py
Writes: dataset.json, COVERAGE.md, records.md  (in the repo root)
Exit code 1 if any obligation record fails schema validation.
"""
import json, sys, pathlib, datetime
import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent

def find(name):
    hits = list(ROOT.rglob(name))
    if not hits:
        sys.exit(f"missing required file: {name}")
    return hits[0]

SCHEMA = json.loads(find("record.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
DIMENSIONS = SCHEMA["properties"]["dimension"]["enum"]
DIM_SHORT = {
    "regulatory_authority": "Auth", "issuer_pathway": "Issu",
    "reserve_backing": "Resv", "capital_requirements": "Cap",
    "permitted_activity_yield": "Yield*", "securities_classification": "Sec*",
    "bank_nonbank_routing": "Rout", "redemption": "Redm", "custody": "Cust",
    "aml_kyc": "AML", "cross_border_data": "XB", "monetary_sovereignty": "MonSov",
    "disclosure_reporting": "Disc", "distribution": "Dist",
    "implementation_status": "Impl",
}

def normalize(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    return obj

def has_verify(obj):
    if isinstance(obj, str):
        return "<VERIFY" in obj
    if isinstance(obj, dict):
        return any(has_verify(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_verify(v) for v in obj)
    return False

def load_all():
    records, corridors, roadmap, errors = [], [], {}, []
    for f in sorted(ROOT.rglob("*.yaml")):
        if f.name == "_TEMPLATE.yaml":
            continue
        data = normalize(yaml.safe_load(f.read_text()))
        if not isinstance(data, dict):
            continue
        if "focus_jurisdictions" in data:                         # roadmap config
            roadmap = data
        elif "corridor_id" in data:                               # corridor record
            corridors.append(data)
        elif "jurisdiction" in data and "dimension" in data:      # obligation record
            errs = sorted(VALIDATOR.iter_errors(data), key=lambda e: str(e.path))
            if errs:
                errors += [f"{f.name}: {e.message}" for e in errs]
                continue
            data["_draft"] = has_verify(data)
            records.append(data)
    return records, corridors, roadmap, errors

def coverage(recs):
    cov = {}
    for r in recs:
        key = (r["jurisdiction"], r["dimension"])
        state = "draft" if r["_draft"] else "verified"
        if cov.get(key) != "verified":
            cov[key] = state
    return cov

def render_coverage(cov, roadmap):
    juris = roadmap.get("focus_jurisdictions", []) + roadmap.get("backfill_jurisdictions", [])
    planned = roadmap.get("planned", {})
    lines = ["| Jurisdiction | " + " | ".join(DIM_SHORT[d] for d in DIMENSIONS) + " |",
             "|" + "---|" * (len(DIMENSIONS) + 1)]
    for j in juris:
        cells = []
        for d in DIMENSIONS:
            st = cov.get((j, d))
            if st == "verified":   cells.append("✅")
            elif st == "draft":    cells.append("✍️")
            elif d in planned.get(j, {}): cells.append(f"⬜{planned[j][d]}")
            else: cells.append("·")
        lines.append(f"| **{j}** | " + " | ".join(cells) + " |")
    legend = ("\n**Legend:** ✅ verified · ✍️ draft (contains `<VERIFY`) · ⬜vX.Y planned · "
              "· out of current scope. `Yield*` = `permitted_activity_yield` (the spine dimension).\n")
    n_ver = sum(1 for v in cov.values() if v == "verified")
    n_draft = sum(1 for v in cov.values() if v == "draft")
    n_planned = sum(len(v) for v in planned.values())
    summary = (f"\n_Verified cells: {n_ver} · draft cells: {n_draft} · planned cells: {n_planned}. "
               f"Generated {datetime.date.today()}._\n")
    return "# Coverage\n\n" + "\n".join(lines) + "\n" + legend + summary

def render_records(recs):
    lines = ["# Records\n", "| id | juris | dimension | status | confidence | state |",
             "|---|---|---|---|---|---|"]
    for r in recs:
        lines.append(f"| `{r['id']}` | {r['jurisdiction']} | {r['dimension']} | "
                     f"{r['status']} | {r['confidence']} | "
                     f"{'✍️ draft' if r['_draft'] else '✅ verified'} |")
    return "\n".join(lines) + "\n"

def main():
    recs, corridors, roadmap, errors = load_all()
    if errors:
        print("SCHEMA VALIDATION FAILED:")
        for e in errors: print("  -", e)
        sys.exit(1)
    cov = coverage(recs)
    dataset = {
        "name": "Stablecoin Rail Register", "version": "0.1.0",
        "generated": str(datetime.date.today()), "record_count": len(recs),
        "records": [{k: v for k, v in r.items() if k != "_draft"} for r in recs],
        "corridors": corridors,
    }
    (ROOT / "dataset.json").write_text(json.dumps(dataset, indent=2, ensure_ascii=False))
    (ROOT / "COVERAGE.md").write_text(render_coverage(cov, roadmap))
    (ROOT / "records.md").write_text(render_records(recs))
    print(f"OK — {len(recs)} records valid, {len(corridors)} corridor(s); "
          f"{sum(1 for v in cov.values() if v=='verified')} verified / "
          f"{sum(1 for v in cov.values() if v=='draft')} draft cell(s).")
    print("     wrote dataset.json, COVERAGE.md, records.md")

if __name__ == "__main__":
    main()
