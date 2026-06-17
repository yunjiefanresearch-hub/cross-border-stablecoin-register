#!/usr/bin/env python3
"""Validate records, compile the dataset, and generate the coverage map.

Usage: python scripts/build.py
Outputs: dist/dataset.json, dist/COVERAGE.md, dist/records.md
Exit code 1 if any record fails schema validation.
"""
import json, sys, pathlib, datetime
import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "record.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)

DIMENSIONS = SCHEMA["properties"]["dimension"]["enum"]
DIM_SHORT = {
    "regulatory_authority": "Auth", "issuer_pathway": "Issu", "reserve_capital": "Resv",
    "permitted_activity_yield": "Yield*", "redemption": "Redm", "custody": "Cust",
    "aml_kyc": "AML", "cross_border_data": "XB", "distribution": "Dist",
    "implementation_status": "Impl",
}

def normalize(obj):
    """YAML parses unquoted dates into date objects; coerce to ISO strings everywhere
    so records validate against the schema and serialize cleanly to JSON."""
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

def load_records():
    recs, errors = [], []
    for f in sorted((ROOT / "data").glob("*.yaml")):
        if f.name.startswith("_") or f.name.lower() == "readme.md":
            continue
        data = normalize(yaml.safe_load(f.read_text()))
        errs = sorted(VALIDATOR.iter_errors(data), key=lambda e: e.path)
        if errs:
            for e in errs:
                errors.append(f"{f.name}: {e.message}")
            continue
        data["_draft"] = has_verify(data)
        recs.append(data)
    return recs, errors

def load_corridors():
    out = []
    for f in sorted((ROOT / "corridors").glob("*.yaml")):
        out.append(normalize(yaml.safe_load(f.read_text())))
    return out

def coverage(recs):
    """(jurisdiction, dimension) -> 'verified' | 'draft'"""
    cov = {}
    for r in recs:
        key = (r["jurisdiction"], r["dimension"])
        state = "draft" if r["_draft"] else "verified"
        if cov.get(key) != "verified":
            cov[key] = state
    return cov

def render_coverage(cov, roadmap):
    focus = roadmap.get("focus_jurisdictions", [])
    backfill = roadmap.get("backfill_jurisdictions", [])
    juris = focus + backfill
    planned = roadmap.get("planned", {})
    lines = []
    header = "| Jurisdiction | " + " | ".join(DIM_SHORT[d] for d in DIMENSIONS) + " |"
    sep = "|" + "---|" * (len(DIMENSIONS) + 1)
    lines += [header, sep]
    for j in juris:
        cells = []
        for d in DIMENSIONS:
            st = cov.get((j, d))
            if st == "verified":
                cells.append("✅")
            elif st == "draft":
                cells.append("✍️")
            elif d in planned.get(j, {}):
                cells.append(f"⬜{planned[j][d]}")
            else:
                cells.append("·")
        lines.append(f"| **{j}** | " + " | ".join(cells) + " |")
    legend = ("\n**Legend:** ✅ verified · ✍️ draft (contains `<VERIFY`) · "
              "⬜vX.Y planned · · out of current scope. "
              "`Yield*` = `permitted_activity_yield` (the spine dimension).\n")
    n_ver = sum(1 for v in cov.values() if v == "verified")
    n_draft = sum(1 for v in cov.values() if v == "draft")
    n_planned = sum(len(v) for v in planned.values())
    summary = (f"\n_Verified cells: {n_ver} · draft cells: {n_draft} · "
               f"planned cells: {n_planned}. Generated {datetime.date.today()}._\n")
    return "# Coverage\n\n" + "\n".join(lines) + "\n" + legend + summary

def render_records(recs):
    lines = ["# Records\n",
             "| id | juris | dimension | status | confidence | state |",
             "|---|---|---|---|---|---|"]
    for r in recs:
        lines.append(f"| `{r['id']}` | {r['jurisdiction']} | {r['dimension']} | "
                     f"{r['status']} | {r['confidence']} | "
                     f"{'✍️ draft' if r['_draft'] else '✅ verified'} |")
    return "\n".join(lines) + "\n"

def main():
    recs, errors = load_records()
    if errors:
        print("SCHEMA VALIDATION FAILED:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    corridors = load_corridors()
    roadmap = yaml.safe_load((ROOT / "roadmap.yaml").read_text())
    cov = coverage(recs)

    dist = ROOT / "dist"
    dataset = {
        "name": "Stablecoin Rail Register",
        "version": "0.1.0",
        "generated": str(datetime.date.today()),
        "record_count": len(recs),
        "records": [{k: v for k, v in r.items() if k != "_draft"} for r in recs],
        "corridors": corridors,
    }
    (dist / "dataset.json").write_text(json.dumps(dataset, indent=2, ensure_ascii=False))
    (dist / "COVERAGE.md").write_text(render_coverage(cov, roadmap))
    (dist / "records.md").write_text(render_records(recs))

    print(f"OK — {len(recs)} records valid, {len(corridors)} corridor(s).")
    print(f"     {sum(1 for v in cov.values() if v=='verified')} verified cell(s), "
          f"{sum(1 for v in cov.values() if v=='draft')} draft cell(s).")
    print("     wrote dist/dataset.json, dist/COVERAGE.md, dist/records.md")

if __name__ == "__main__":
    main()
