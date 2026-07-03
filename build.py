#!/usr/bin/env python3
"""Validate records, compile the dataset, and regenerate the coverage map.

Flat-layout friendly: it finds files by name/content anywhere under the repo root,
so it works whether the files sit in folders or all at the top level.

Usage:  python build.py
Writes: dataset.json, COVERAGE.md, records.md  (in the repo root)
Exit code 1 if any obligation record fails schema validation.
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, sys, pathlib, datetime
import yaml

# README<->build drift gate (see check_readme_counts.py). Guarded so an offline extract without the
# module still builds; when present, it forbids a drift-prone count from being restated in README.
try:
    from check_readme_counts import check_readme_counts as _check_readme_counts
except Exception:
    _check_readme_counts = None

# --- schema validation backend: prefer `jsonschema`, fall back to a dependency-free builtin ---------
# The repo declares `jsonschema` in requirements.txt and CI uses it for full Draft 2020-12 validation.
# But a fresh OFFLINE extract (no network, package not installed) must still build and self-validate
# without a hand-written validator. So if the import fails we use a compact, faithful subset of Draft
# 2020-12 — type/required/enum/const/properties/additionalProperties/items/allOf/if-then-else — which is
# sufficient for this repo's record + corridor schemas. The build prints which backend it used.
try:
    from jsonschema import Draft202012Validator as _ExtValidator
    VALIDATOR_BACKEND = "jsonschema (full Draft 2020-12)"
except Exception:
    _ExtValidator = None
    VALIDATOR_BACKEND = "builtin fallback (offline; structural subset of Draft 2020-12)"


class _Err:
    """Mimics jsonschema's error object surface used by this build: .message and .path."""
    def __init__(self, message, path):
        self.message = message
        self.path = list(path)


class _FallbackValidator:
    """Dependency-free structural validator — a faithful subset of JSON Schema Draft 2020-12 covering
    exactly the keywords this repo's schemas use. Not a general-purpose validator; it exists so an
    offline extract can reproduce the green build without `jsonschema` installed."""
    def __init__(self, schema):
        self.schema = schema

    def iter_errors(self, data):
        yield from self._v(data, self.schema, [])

    def _ok(self, data, schema):
        # true iff `data` validates against `schema` with no errors (used by if/then)
        for _ in self._v(data, schema, []):
            return False
        return True

    def _v(self, data, schema, path):
        if schema is True or schema == {}:
            return
        if schema is False:
            yield _Err("schema is false; no value is valid", path); return
        if not isinstance(schema, dict):
            return
        t = schema.get("type")
        if t is not None and not self._type_ok(data, t):
            yield _Err(f"{data!r} is not of type {t!r}", path); return
        if "enum" in schema and data not in schema["enum"]:
            yield _Err(f"{data!r} is not one of {schema['enum']!r}", path)
        if "const" in schema and data != schema["const"]:
            yield _Err(f"{data!r} was expected to be {schema['const']!r}", path)
        for sub in schema.get("allOf", []):
            yield from self._v(data, sub, path)
        if "if" in schema:
            if self._ok(data, schema["if"]):
                if "then" in schema:
                    yield from self._v(data, schema["then"], path)
            elif "else" in schema:
                yield from self._v(data, schema["else"], path)
        if isinstance(data, dict):
            for req in schema.get("required", []):
                if req not in data:
                    yield _Err(f"{req!r} is a required property", path)
            props = schema.get("properties", {})
            if schema.get("additionalProperties", True) is False:
                for k in data:
                    if k not in props:
                        yield _Err(f"Additional properties are not allowed ({k!r} was unexpected)", path)
            for k, v in data.items():
                if k in props:
                    yield from self._v(v, props[k], path + [k])
        if isinstance(data, list):
            items = schema.get("items")
            if isinstance(items, dict):
                for i, it in enumerate(data):
                    yield from self._v(it, items, path + [i])

    @staticmethod
    def _type_ok(data, t):
        for tt in (t if isinstance(t, list) else [t]):
            if tt == "object" and isinstance(data, dict): return True
            if tt == "array" and isinstance(data, list): return True
            if tt == "string" and isinstance(data, str): return True
            if tt == "boolean" and isinstance(data, bool): return True
            if tt == "integer" and isinstance(data, int) and not isinstance(data, bool): return True
            if tt == "number" and isinstance(data, (int, float)) and not isinstance(data, bool): return True
            if tt == "null" and data is None: return True
        return False


def _make_validator(schema):
    return _ExtValidator(schema) if _ExtValidator is not None else _FallbackValidator(schema)

ROOT = pathlib.Path(__file__).resolve().parent

# Single source of truth for the dataset/release version. Bump this when tagging
# a release; keep it in step with README, CITATION.cff, and the schema $id.
REGISTER_VERSION = "0.9.9"

def find(name):
    hits = list(ROOT.rglob(name))
    if not hits:
        sys.exit(f"missing required file: {name}")
    return hits[0]

SCHEMA = json.loads(find("record.schema.json").read_text(encoding="utf-8"))
VALIDATOR = _make_validator(SCHEMA)
DIMENSIONS = SCHEMA["properties"]["dimension"]["enum"]
_corr_schema_path = ROOT / "corridor.schema.json"
CORRIDOR_VALIDATOR = _make_validator(json.loads(_corr_schema_path.read_text(encoding="utf-8"))) if _corr_schema_path.exists() else None
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
        data = normalize(yaml.safe_load(f.read_text(encoding="utf-8")))
        if not isinstance(data, dict):
            continue
        if "focus_jurisdictions" in data:                         # roadmap config
            roadmap = data
        elif "corridor_id" in data:                               # corridor record
            if CORRIDOR_VALIDATOR is not None:
                cerrs = sorted(CORRIDOR_VALIDATOR.iter_errors(data), key=lambda e: str(e.path))
                if cerrs:
                    errors += [f"{f.name} (corridor): {e.message}" for e in cerrs]
                    continue
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

def render_coverage(cov, roadmap, recs=None, analysis=None):
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
    # What ✅ does and does not mean — the legal-reader caveat, made explicit.
    semantics = ("\n> **What ✅ means here.** ✅ marks a cell that has a sourced, schema-valid record "
                 "with **no `<VERIFY` marker and a human-passed pinpoint**. It does **not** by itself mean "
                 "the pinpoint has been checked against the official gazette / statutory text. Provenance is "
                 "tracked separately by `evidence_tier`: `resolution_text` = confirmed against the official "
                 "text; `mixed` = the core point is confirmed against the official text but some operational "
                 "detail is pending; `firm_summary` = corroborated by law-firm/practitioner analysis but not "
                 "yet against the official text. As of the v0.5.1 verification pass, the live-regime focus "
                 "jurisdictions (Switzerland, the UAE, Japan) and the in-force AML / user-protection layers of "
                 "the pre-regime jurisdictions (Taiwan, South Korea) carry an official `source.url` and are "
                 "`resolution_text` or `mixed`; draft provisions (the Taiwan VAS Act, the Korea Digital Asset "
                 "Basic Act) keep `status: proposed` / `firm_summary` with an official URL for the *bill*, and "
                 "the older seven-jurisdiction records predate the `evidence_tier` field (`unset`). Check the "
                 "breakdown below before citing any cell as primary authority.\n")
    n_ver = sum(1 for v in cov.values() if v == "verified")
    n_draft = sum(1 for v in cov.values() if v == "draft")
    n_planned = sum(len(v) for v in planned.values())
    tier_block = ""
    if recs is not None:
        from collections import Counter
        tc = Counter(r.get("evidence_tier", "unset") for r in recs)
        with_url = sum(1 for r in recs if (r.get("source") or {}).get("url"))
        tier_block = ("\n**Evidence-tier breakdown (records):** "
                      f"resolution_text {tc.get('resolution_text', 0)} · "
                      f"mixed {tc.get('mixed', 0)} · "
                      f"firm_summary {tc.get('firm_summary', 0)} · "
                      f"unset {tc.get('unset', 0)} · "
                      f"records with a populated `source.url`: {with_url}/{sum(tc.values())}.\n")
    claim_block = ""
    if recs is not None:
        from collections import Counter
        m = Counter((r.get("claim_class", "unset"), r.get("evidence_tier", "unset")) for r in recs)
        tiers = ["resolution_text", "mixed", "firm_summary", "unset"]
        classes = ["tier1_legal", "tier2_operational"]
        citable = sum(1 for r in recs if r.get("claim_class") == "tier1_legal"
                      and r.get("status") == "in_force"
                      and r.get("evidence_tier") == "resolution_text")
        header = "| claim_class \\ evidence_tier | " + " | ".join(tiers) + " | total |"
        sep = "|" + "---|" * (len(tiers) + 2)
        rows = []
        for cc in classes:
            cells = [str(m.get((cc, t), 0)) for t in tiers]
            rows.append(f"| **{cc}** | " + " | ".join(cells) + f" | {sum(m.get((cc, t), 0) for t in tiers)} |")
        claim_block = (
            "\n## Two-axis evidence model (the honesty view)\n"
            "`claim_class` is the *kind* of claim (a proposition of law vs a market/operational "
            "report); `evidence_tier` is *how well-sourced* it is. They are orthogonal. The "
            "**lawyer-citable subset** is the intersection `tier1_legal` + `in_force` + "
            "`resolution_text` — binding law, in force now, confirmed against the official text. "
            "Operational facts are excluded by *kind* even when well-sourced; draft provisions are "
            "excluded by *status*; unverified legal points are excluded by *tier*.\n\n"
            + header + "\n" + sep + "\n" + "\n".join(rows) + "\n\n"
            f"> **Citable cells: {citable}** records satisfy `tier1_legal` + `in_force` + "
            "`resolution_text` and carry an official `source.url` + `pinpoint` (enforced by the "
            "build). This is the subset a lawyer or supervisor can cite as current binding law; it "
            "is exposed directly by the MCP `citable_law()` tool and as `citable_subset` in "
            "`dataset.json`. The two `tier2_operational` records at `resolution_text` (e.g. a "
            "confirmed product launch) are deliberately *not* citable as law — they are true, "
            "well-sourced facts about the market, not propositions of law.\n")
    summary = (f"\n_Verified cells: {n_ver} · draft cells: {n_draft} · planned cells: {n_planned}. "
               f"Generated {datetime.date.today()}._\n")
    computed_block = ""
    if analysis and analysis.get("computed"):
        cm = analysis["computed"]
        fb = cm.get("findings_by_cause", {})
        fline = "; ".join(f"{k}: {', '.join(v)}" for k, v in fb.items()) or "none"
        computed_block = ("\n## Computed layer (preview)\n"
                          "The `compose()` engine derives each pair's feasibility from the per-jurisdiction "
                          "signal table and the Corridor Atlas algorithm, then diffs computed-vs-authored. It "
                          "is a preview, not asserted authoritative; disagreements are **findings**.\n\n"
                          f"- Directed corridors reproduced from rules: **{cm['directed_edges']['agreement']}**\n"
                          f"- §5.14 undirected categories reproduced: **{cm['undirected_pairs']['agreement']}**\n"
                          f"- Findings (computed ≠ authored): **{fline}**\n"
                          f"- Cross-layer integrity: every corridor's category is enforced against its §5.14 row; "
                          "differing interaction sets must carry a declared `divergence` field.\n")
    queue_block = ""
    if recs is not None:
        from collections import Counter
        tc2 = Counter(r.get("evidence_tier", "unset") for r in recs)
        legacy = sorted(r["jurisdiction"] for r in recs if r.get("evidence_tier", "unset") == "unset")
        lc = Counter(legacy)
        queue_block = ("\n## Verification queue\n"
                       "The backlog driving the next primary-source pass (also exposed by the MCP "
                       "`verification_report()` tool).\n\n"
                       f"- `resolution_text` {tc2.get('resolution_text',0)} · `mixed` {tc2.get('mixed',0)} · "
                       f"`firm_summary` {tc2.get('firm_summary',0)} · **`unset` {tc2.get('unset',0)} (largest backlog)**\n"
                       f"- The `unset` records are the legacy seven-jurisdiction set: "
                       f"{', '.join(f'{k} {v}' for k, v in sorted(lc.items()))}. These predate the "
                       "`evidence_tier` field and are the declared next target.\n")
    return ("# Coverage\n\n" + "\n".join(lines) + "\n" + legend + semantics + tier_block
            + claim_block + computed_block + queue_block + summary)

def check_cross_layer(corridors, analysis):
    """Enforce that the corridor layer and the §5.14 compatibility matrix AGREE.

    For every corridor carrying a `compatibility_pair` foreign key:
      - its `compatibility_category` MUST equal the matrix row's category (hard error), and
      - if its `interaction_sets` differ from the matrix row's, it MUST carry a `divergence`
        field declaring and explaining the difference (directed edge vs undirected pair).
    This turns what were silent contradictions into declared, enforced relationships — the
    register becomes internally self-consistent rather than two independent transcriptions.
    """
    errors = []
    if not analysis or "compatibility" not in analysis:
        return errors
    rows = {p["pair"]: p for p in analysis["compatibility"].get("pairs", [])}
    declared = 0
    for c in corridors:
        pair = c.get("compatibility_pair")
        if not pair:
            continue
        row = rows.get(pair)
        if row is None:
            errors.append(f"corridor {c.get('corridor_id')}: compatibility_pair {pair!r} not found in the §5.14 matrix")
            continue
        if c.get("compatibility_category") != row.get("category"):
            errors.append(f"corridor {c.get('corridor_id')}: category {c.get('compatibility_category')!r} "
                          f"contradicts §5.14 {pair} category {row.get('category')!r}")
        edge_sets = sorted(c.get("interaction_sets") or [])
        pair_sets = sorted(row.get("interaction_sets") or [])
        if edge_sets != pair_sets:
            div = c.get("divergence")
            if not div or div.get("against_pair") != pair or not div.get("reason"):
                errors.append(f"corridor {c.get('corridor_id')}: interaction_sets {edge_sets} differ from "
                              f"§5.14 {pair} {pair_sets} but no valid `divergence` field declares it")
            else:
                declared += 1
    return errors

def render_records(recs):
    lines = ["# Records\n", "| id | juris | dimension | status | confidence | state |",
             "|---|---|---|---|---|---|"]
    for r in recs:
        lines.append(f"| `{r['id']}` | {r['jurisdiction']} | {r['dimension']} | "
                     f"{r['status']} | {r['confidence']} | "
                     f"{'✍️ draft' if r['_draft'] else '✅ verified'} |")
    return "\n".join(lines) + "\n"

# ---- analysis layer (the Architecture paper's payload, encoded as queryable data) ----
ANALYSIS_FILES = ["interaction_sets.json", "architectural_patterns.json",
                  "compatibility.json", "open_questions.json"]
VALID_CATEGORIES = {"I", "I/II", "II", "III"}
VALID_SETS = {"A", "B", "C", "D", "E", "F"}

def load_analysis():
    """Load + structurally validate the analysis/ artifacts. Returns (analysis_dict, errors)."""
    adir = ROOT / "analysis"
    if not adir.is_dir():
        return None, []                      # analysis layer optional; absence is not an error
    analysis, errors = {}, []
    juris = set(SCHEMA["properties"]["jurisdiction"]["enum"])
    for name in ANALYSIS_FILES:
        f = adir / name
        if not f.exists():
            errors.append(f"analysis/{name}: missing")
            continue
        try:
            obj = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"analysis/{name}: invalid JSON ({e})")
            continue
        if "schema" not in obj:
            errors.append(f"analysis/{name}: missing 'schema' tag")
        analysis[name.replace(".json", "")] = obj
    # deep-check the compatibility matrix (the load-bearing artifact)
    comp = analysis.get("compatibility")
    if comp is not None:
        pairs = comp.get("pairs", [])
        expected = {"-".join(sorted([a, b])) for i, a in enumerate(comp.get("jurisdictions", []))
                    for b in comp.get("jurisdictions", [])[i + 1:]}
        seen = set()
        for p in pairs:
            if p.get("category") not in VALID_CATEGORIES:
                errors.append(f"compatibility: pair {p.get('pair')} has invalid category {p.get('category')!r}")
            for s in p.get("interaction_sets", []):
                if s not in VALID_SETS:
                    errors.append(f"compatibility: pair {p.get('pair')} has invalid interaction set {s!r}")
            for j in p.get("jurisdictions", []):
                if j not in juris:
                    errors.append(f"compatibility: pair {p.get('pair')} references unknown jurisdiction {j!r}")
            seen.add(p.get("pair"))
        missing = expected - seen
        if missing:
            errors.append(f"compatibility: missing pairs {sorted(missing)}")
    # optional computed layer (the compose() preview): load + light-validate if present
    cf = adir / "computed_compatibility.json"
    if cf.exists():
        try:
            cobj = json.loads(cf.read_text(encoding="utf-8"))
            if cobj.get("schema") != "cbsr-analysis/computed_compatibility":
                errors.append("computed_compatibility.json: missing/incorrect 'schema' tag")
            pc = cobj.get("pre_regime_crosscheck", {})
            if pc and pc.get("consistent") is False:
                errors.append(f"computed: pre_regime cross-check inconsistent — signals {pc.get('from_signals')} "
                              f"vs records {pc.get('from_records')} (the signal table and the node records disagree)")
            sp = cobj.get("signal_provenance", {})
            if sp and sp.get("clean") is False:
                for v in sp.get("violations", []):
                    errors.append(f"computed: signal-provenance violation — {v}")
            analysis["computed"] = cobj
        except json.JSONDecodeError as e:
            errors.append(f"computed_compatibility.json: invalid JSON ({e})")
    # optional event calendar + computed timeline (the v0.8.0 time engine)
    ev = adir / "event_calendar.json"
    if ev.exists():
        try:
            eobj = json.loads(ev.read_text(encoding="utf-8"))
            if eobj.get("schema") != "cbsr-analysis/event_calendar":
                errors.append("event_calendar.json: missing/incorrect 'schema' tag")
            juris = set(SCHEMA["properties"]["jurisdiction"]["enum"])
            for e in eobj.get("events", []):
                eid = e.get("id", "<no id>")
                if e.get("jurisdiction") not in juris:
                    errors.append(f"event {eid}: unknown jurisdiction {e.get('jurisdiction')!r}")
                if e.get("claim_class") != "tier1_legal":
                    errors.append(f"event {eid}: claim_class must be tier1_legal (a change in law), got {e.get('claim_class')!r}")
                if e.get("status") not in {"scheduled", "contingent", "in_force"}:
                    errors.append(f"event {eid}: invalid status {e.get('status')!r}")
                if e.get("status") == "scheduled" and not e.get("effective_date"):
                    errors.append(f"event {eid}: scheduled events require an effective_date")
                if e.get("status") == "contingent" and e.get("effective_date"):
                    errors.append(f"event {eid}: contingent events must not carry an effective_date")
            analysis["event_calendar"] = eobj
        except json.JSONDecodeError as e:
            errors.append(f"event_calendar.json: invalid JSON ({e})")
    tf = adir / "computed_timeline.json"
    if tf.exists():
        try:
            tobj = json.loads(tf.read_text(encoding="utf-8"))
            if tobj.get("schema") != "cbsr-analysis/computed_timeline":
                errors.append("computed_timeline.json: missing/incorrect 'schema' tag")
            ep = tobj.get("event_provenance", {})
            if ep and ep.get("clean") is False:
                for v in ep.get("violations", []):
                    errors.append(f"timeline: event-provenance violation — {v}")
            analysis["computed_timeline"] = tobj
        except json.JSONDecodeError as e:
            errors.append(f"computed_timeline.json: invalid JSON ({e})")
    # optional constraint substrate (the v0.9.0 deeper engine)
    sf = adir / "constraint_substrate.json"
    if sf.exists():
        try:
            sobj = json.loads(sf.read_text(encoding="utf-8"))
            if sobj.get("schema") != "cbsr-analysis/constraint_substrate":
                errors.append("constraint_substrate.json: missing/incorrect 'schema' tag")
            juris = set(SCHEMA["properties"]["jurisdiction"]["enum"])
            vocab = sobj.get("pole_vocabulary", {})
            for j, cells in sobj.get("cells", {}).items():
                if j not in juris:
                    errors.append(f"substrate: unknown jurisdiction {j!r}")
                for c, cell in cells.items():
                    if c in vocab and cell.get("pole") not in vocab[c]:
                        errors.append(f"substrate {j}.{c}: pole {cell.get('pole')!r} not in vocabulary")
                    if not cell.get("derived_from"):
                        errors.append(f"substrate {j}.{c}: pole has no derived_from record")
            analysis["constraint_substrate"] = sobj
        except json.JSONDecodeError as e:
            errors.append(f"constraint_substrate.json: invalid JSON ({e})")
    cs = adir / "computed_substrate.json"
    if cs.exists():
        try:
            csobj = json.loads(cs.read_text(encoding="utf-8"))
            if csobj.get("schema") != "cbsr-analysis/computed_substrate":
                errors.append("computed_substrate.json: missing/incorrect 'schema' tag")
            spv = csobj.get("substrate_provenance", {})
            if spv and spv.get("clean") is False:
                for v in spv.get("violations", []):
                    errors.append(f"substrate: provenance violation — {v}")
            xc = csobj.get("cross_check", {})
            if xc and xc.get("clean") is False:
                errors.append(f"substrate: cross-check vs signal compose() disagrees on "
                              f"{xc.get('disagreements_with_signal')} (a definite substrate class must match the signal compose, or be declared)")
            analysis["computed_substrate"] = csobj
        except json.JSONDecodeError as e:
            errors.append(f"computed_substrate.json: invalid JSON ({e})")
    # optional verification worklist (the v0.9.1 verification-pass harness)
    wf = adir / "verification_worklist.json"
    if wf.exists():
        try:
            wobj = json.loads(wf.read_text(encoding="utf-8"))
            if wobj.get("schema") != "cbsr-analysis/verification_worklist":
                errors.append("verification_worklist.json: missing/incorrect 'schema' tag")
            analysis["verification_worklist"] = wobj
        except json.JSONDecodeError as e:
            errors.append(f"verification_worklist.json: invalid JSON ({e})")
    # optional stakeholder database + computed projections (the v0.9.3 Atlas §8 layer)
    sdb = adir / "stakeholder_database.json"
    if sdb.exists():
        try:
            sdobj = json.loads(sdb.read_text(encoding="utf-8"))
            if sdobj.get("schema") != "cbsr-analysis/stakeholder_database":
                errors.append("stakeholder_database.json: missing/incorrect 'schema' tag")
            # every persona must declare a lens + at least one primary constraint
            for sid, sk in sdobj.get("stakeholders", {}).items():
                if not sk.get("lens") or not sk.get("primary_constraints"):
                    errors.append(f"stakeholder_database: persona {sid!r} missing lens/primary_constraints")
            analysis["stakeholder_database"] = sdobj
        except json.JSONDecodeError as e:
            errors.append(f"stakeholder_database.json: invalid JSON ({e})")
    spf = adir / "computed_stakeholder_profiles.json"
    if spf.exists():
        try:
            spobj = json.loads(spf.read_text(encoding="utf-8"))
            if spobj.get("schema") != "cbsr-analysis/computed_stakeholder_profiles":
                errors.append("computed_stakeholder_profiles.json: missing/incorrect 'schema' tag")
            prov = spobj.get("provenance", {})
            if prov.get("clean") is False:
                errors.append(f"stakeholder profiles: provenance not clean — missing records "
                              f"{prov.get('missing_records')}, non-tier1 profiles {prov.get('nontier1_profiles')} "
                              f"(every projected line must rest on an existing tier1_legal record)")
            analysis["computed_stakeholder_profiles"] = spobj
        except json.JSONDecodeError as e:
            errors.append(f"computed_stakeholder_profiles.json: invalid JSON ({e})")
    # optional computed corridor skeletons (the v0.9.4 edge-layer densification)
    csk = adir / "computed_corridor_skeletons.json"
    if csk.exists():
        try:
            ckobj = json.loads(csk.read_text(encoding="utf-8"))
            if ckobj.get("schema") != "cbsr-analysis/computed_corridor_skeletons":
                errors.append("computed_corridor_skeletons.json: missing/incorrect 'schema' tag")
            prov = ckobj.get("provenance", {})
            if prov.get("clean") is False:
                errors.append(f"corridor skeletons: provenance not clean — non-tier1 skeletons "
                              f"{prov.get('nontier1_skeletons')} (every derived field must rest on a tier1_legal record)")
            xc = ckobj.get("cross_check", {})
            if xc.get("clean") is False:
                errors.append(f"corridor skeletons: cross-check vs signal compose() disagrees on "
                              f"{xc.get('disagreements_with_signal')} (a skeleton class must match the signal compose)")
            analysis["computed_corridor_skeletons"] = ckobj
        except json.JSONDecodeError as e:
            errors.append(f"computed_corridor_skeletons.json: invalid JSON ({e})")
    # optional computed convergence view (the v0.9.9 yield-line §4.5 reshape)
    cvg = adir / "computed_convergence.json"
    if cvg.exists():
        try:
            cvobj = json.loads(cvg.read_text(encoding="utf-8"))
            if cvobj.get("schema") != "cbsr-analysis/computed_convergence":
                errors.append("computed_convergence.json: missing/incorrect 'schema' tag")
            prov = cvobj.get("provenance", {})
            if prov.get("clean") is False or prov.get("asserts_new_facts") is True:
                errors.append("convergence: provenance not clean — this view only reshapes existing "
                              "permitted_activity_yield records and must assert no new facts")
            analysis["computed_convergence"] = cvobj
        except json.JSONDecodeError as e:
            errors.append(f"computed_convergence.json: invalid JSON ({e})")
    # optional verification ledger (the v0.9.5 external primary-source pass audit trail)
    vl = adir / "verification_ledger.json"
    if vl.exists():
        try:
            vobj = json.loads(vl.read_text(encoding="utf-8"))
            if vobj.get("schema") != "cbsr/verification_ledger":
                errors.append("verification_ledger.json: missing/incorrect 'schema' tag")
            analysis["verification_ledger"] = vobj
        except json.JSONDecodeError as e:
            errors.append(f"verification_ledger.json: invalid JSON ({e})")
    return (analysis or None), errors

def evidence_tier_summary(recs):
    """Transparency: break verified records down by evidence_tier (firm_summary vs resolution_text)."""
    from collections import Counter
    c = Counter(r.get("evidence_tier", "unset") for r in recs)
    with_url = sum(1 for r in recs if (r.get("source") or {}).get("url"))
    return c, with_url

# ---- the two-axis evidence model: claim_class (kind) x evidence_tier (provenance) ----
# The lawyer-citable subset is the intersection of:
#   claim_class == tier1_legal   (a proposition of law, not a market/operational report)
#   status      == in_force      (binding now, not draft/transitional/consultation)
#   evidence_tier == resolution_text  (confirmed against the official statutory text)
CITABLE_FILTER = {
    "claim_class": "tier1_legal",
    "status": "in_force",
    "evidence_tier": "resolution_text",
    "description": ("Lawyer-citable: a proposition of law (tier1_legal), currently in force, "
                    "confirmed against the official statutory/regulatory text (resolution_text). "
                    "Operational/market facts (tier2_operational) are excluded by kind even when "
                    "well-sourced; draft provisions are excluded by status; unverified legal points "
                    "are excluded by evidence_tier."),
}

def is_citable(r):
    return (r.get("claim_class") == "tier1_legal"
            and r.get("status") == "in_force"
            and r.get("evidence_tier") == "resolution_text")

def citable_projection(r):
    """Project a citable record down to what a citation needs: instrument + pinpoint + url."""
    src = r.get("source") or {}
    return {
        "id": r["id"], "jurisdiction": r["jurisdiction"], "dimension": r["dimension"],
        "instrument": src.get("primary"), "pinpoint": src.get("pinpoint"), "url": src.get("url"),
        "last_reviewed": r.get("last_reviewed"),
    }

def check_citable_integrity(recs):
    """Enforce that a record claiming official-text confirmation actually points to that text.

    A `tier1_legal` record at `resolution_text` or `mixed` asserts that its core legal point is
    confirmed against the official instrument — so it MUST carry a `source.url` (the official text),
    and a `resolution_text` record MUST additionally carry a `source.pinpoint` (where in the text).
    Without this, the citable subset could not be trusted as 'confirmed against the source'.
    """
    errors = []
    for r in recs:
        if r.get("claim_class") != "tier1_legal":
            continue
        et = r.get("evidence_tier")
        src = r.get("source") or {}
        if et in ("resolution_text", "mixed") and not src.get("url"):
            errors.append(f"{r['id']}: claim_class tier1_legal at evidence_tier '{et}' asserts "
                          f"official-text confirmation but has no source.url")
        if et == "resolution_text" and not src.get("pinpoint"):
            errors.append(f"{r['id']}: claim_class tier1_legal at evidence_tier 'resolution_text' "
                          f"has no source.pinpoint (cannot cite without a locator)")
    return errors

def claim_class_matrix(recs):
    """Return the claim_class x evidence_tier count matrix (the honesty view)."""
    from collections import Counter
    m = Counter((r.get("claim_class", "unset"), r.get("evidence_tier", "unset")) for r in recs)
    return m

# Operational tells that must not appear in a CITABLE record's instrument string or pinpoint.
# Kept deliberately conservative: legal verbs ("admitted via registered EPIESP") and case citations
# ("SEC v. Howey Co., 328 U.S. 293") are excluded; only product/market EVENTS and named commercial
# counterparties trip it. Operational illustration belongs in the `operational_notes` field instead.
import re as _re
_OP_EVENT = _re.compile(r"\b(admission via|admitted via [A-Z]|launch(?:ed|es|ing)?|went live|rolled out|first .*? to register|listing of)\b", _re.I)
_OP_ENTITY = _re.compile(r"\b(SBI VC Trade|SBI Group|Circle|Coinbase|Binance|JPYC Inc|Progmat|Project Pax)\b")
_CASE_CITE = _re.compile(r"\bv\.\s|\bU\.S\.\s|\bF\.\d|\bS\.\sCt|\bNo\.\s\d")

def check_citable_purity(recs):
    """A citable record must cite the instrument only — no operational event/entity in source/pinpoint.

    The citable projection (source.primary as the instrument, plus the pinpoint locator) is what a
    lawyer is shown as 'citable law'. If a tier1_legal record bundles a product approval, launch, or a
    named commercial counterparty into source.primary or pinpoint, that operational material would be
    projected as binding law. This forbids it: such material must live in `operational_notes` (Tier-2),
    which the projection omits. Conservative by design — legal verbs and case citations don't trip it.
    """
    errors = []
    for r in recs:
        if not is_citable(r):
            continue
        src = r.get("source") or {}
        sp = src.get("primary", "") or ""
        pin = src.get("pinpoint", "") or ""
        for seg in (s.strip() for s in sp.split(";")):
            if _CASE_CITE.search(seg):           # legal case citation, not operational
                continue
            if _OP_EVENT.search(seg) or _OP_ENTITY.search(seg):
                errors.append(f"{r['id']}: citable record's source.primary contains operational material "
                              f"({seg!r}); cite the instrument only and move the example to operational_notes")
        if _OP_ENTITY.search(pin) or _OP_EVENT.search(pin):
            errors.append(f"{r['id']}: citable record's pinpoint contains operational material "
                          f"({pin!r}); the pinpoint must locate the legal text only")
    return errors

def check_evidence_tier_requirements(recs):
    """Make evidence_tier EARNED, not asserted: a record may only claim a tier it has the evidence for.

    Necessary conditions (grounded in the dataset's tier semantics):
      - resolution_text (confirmed against official text) => source.url AND source.pinpoint AND last_reviewed
      - mixed (core point confirmed)                      => source.url AND source.pinpoint
      - firm_summary (practitioner-corroborated)          => source.pinpoint
    A `verification` block, if present, must be consistent: method=official_text requires the tier to be
    resolution_text or mixed; method=practitioner_corroboration is incompatible with resolution_text.
    These are NECESSARY (not sufficient) conditions — the tier remains a human judgment, but it can no
    longer be claimed without the corroborating provenance. This is the gate the verification pass runs
    behind: a promotion only lands if the evidence is actually present.
    """
    errors = []
    for r in recs:
        et = r.get("evidence_tier")
        src = r.get("source") or {}
        if et in ("resolution_text", "mixed"):
            if not src.get("url"):
                errors.append(f"{r['id']}: evidence_tier={et} requires source.url (the official-text pointer)")
            if not src.get("pinpoint"):
                errors.append(f"{r['id']}: evidence_tier={et} requires source.pinpoint")
        if et == "resolution_text" and not r.get("last_reviewed"):
            errors.append(f"{r['id']}: evidence_tier=resolution_text requires last_reviewed (when the text was checked)")
        if et == "firm_summary" and not src.get("pinpoint"):
            errors.append(f"{r['id']}: evidence_tier=firm_summary requires source.pinpoint")
        ver = r.get("verification")
        if isinstance(ver, dict):
            m = ver.get("method")
            if m == "official_text" and et not in ("resolution_text", "mixed"):
                errors.append(f"{r['id']}: verification.method=official_text but evidence_tier={et!r} "
                              f"(official-text confirmation should promote to resolution_text or mixed)")
            if m == "practitioner_corroboration" and et == "resolution_text":
                errors.append(f"{r['id']}: verification.method=practitioner_corroboration is inconsistent with "
                              f"evidence_tier=resolution_text (which asserts confirmation against the official text)")
            ag = ver.get("against") or {}
            if ag.get("url") and src.get("url") and ag["url"] != src.get("url"):
                errors.append(f"{r['id']}: verification.against.url does not match source.url")
    return errors

def check_binding_status(recs):
    """Enforce the binding-status cap on citability (the v0.9.5 axis).

    binding_status is the third evidence axis: the binding status of the instrument a cell rests on,
    orthogonal to evidence_tier (how well-sourced) and claim_class (legal vs operational). The central
    finding of the external verification pass is that citability is capped by binding status,
    independent of whether the official text was located. So:

      - A `resolution_text` cell MUST have binding_status == in_force_enacted. You cannot cite as CURRENT
        LAW a proposition resting on a bill, an NPRM, a consultation, a made-but-not-commenced instrument,
        a finalized-but-unlegislated policy, or a prohibition. This is what keeps the citable subset honest
        even after the verification pass located the text (e.g. UK SI 2026/102 is read but not yet in force).
      - Conversely, any cell whose binding_status is not in_force_enacted MUST NOT be resolution_text.
    """
    blocked = {"made_not_commenced", "finalized_policy_pending", "pending_proposal", "prohibition", "no_regime"}
    errors = []
    for r in recs:
        bs = r.get("binding_status")
        et = r.get("evidence_tier")
        if et == "resolution_text" and bs != "in_force_enacted":
            errors.append(f"{r['id']}: evidence_tier=resolution_text requires binding_status=in_force_enacted "
                          f"(citable as current law), but binding_status={bs!r} — a non-enacted/not-in-force "
                          f"instrument cannot be cited as current law")
        if bs in blocked and et == "resolution_text":
            errors.append(f"{r['id']}: binding_status={bs!r} (not in force as enacted law) is incompatible "
                          f"with evidence_tier=resolution_text")
    return errors

def check_verification_ledger(recs, analysis):
    """Cross-check every record against the verification ledger (drift detection).

    The ledger (analysis/verification_ledger.json) is the audit trail of the external primary-source pass:
    per cell, the binding_status assigned, the official URL attached, and the tier the disposition applied.
    This gate verifies the committed records still agree with the committed ledger — so a later hand-edit
    that, say, promotes a pending_proposal cell to resolution_text, or strips a verified URL, fails the
    build. The ledger and the records are independently committed files; this keeps them from drifting.
    """
    if not analysis:
        return []
    ledger = analysis.get("verification_ledger")
    if not ledger:
        return []
    by_id = {r["id"]: r for r in recs}
    errors = []
    for e in ledger.get("entries", []):
        cid = e.get("cell")
        r = by_id.get(cid)
        if r is None:
            errors.append(f"verification_ledger: entry for {cid!r} has no matching record")
            continue
        if r.get("binding_status") != e.get("binding_status"):
            errors.append(f"verification_ledger drift: {cid} binding_status is "
                          f"{r.get('binding_status')!r} but the ledger says {e.get('binding_status')!r}")
        if r.get("evidence_tier", "unset") != e.get("applied_tier"):
            errors.append(f"verification_ledger drift: {cid} evidence_tier is "
                          f"{r.get('evidence_tier', 'unset')!r} but the ledger applied {e.get('applied_tier')!r}")
        if e.get("official_url") and (r.get("source") or {}).get("url") != e.get("official_url"):
            errors.append(f"verification_ledger drift: {cid} source.url does not match the ledger's official_url")
    return errors

def main():
    recs, corridors, roadmap, errors = load_all()
    analysis, aerrors = load_analysis()
    errors += aerrors
    errors += check_cross_layer(corridors, analysis)
    errors += check_citable_integrity(recs)
    errors += check_citable_purity(recs)
    errors += check_evidence_tier_requirements(recs)
    errors += check_binding_status(recs)
    errors += check_verification_ledger(recs, analysis)
    readme_path = ROOT / "README.md"
    if _check_readme_counts and readme_path.exists():
        errors += _check_readme_counts(readme_path.read_text(encoding="utf-8"))
    if errors:
        print("VALIDATION FAILED:")
        for e in errors: print("  -", e)
        sys.exit(1)
    cov = coverage(recs)
    citable = [citable_projection(r) for r in recs if is_citable(r)]
    dataset = {
        "name": "Cross-Border Stablecoin Register", "version": REGISTER_VERSION,
        "generated": str(datetime.date.today()), "record_count": len(recs),
        "records": [{k: v for k, v in r.items() if k != "_draft"} for r in recs],
        "corridors": corridors,
        "citable_subset": {
            "filter": CITABLE_FILTER,
            "count": len(citable),
            "records": citable,
        },
    }
    if analysis is not None:
        dataset["analysis"] = analysis
    (ROOT / "dataset.json").write_text(json.dumps(dataset, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "COVERAGE.md").write_text(render_coverage(cov, roadmap, recs, analysis), encoding="utf-8")
    (ROOT / "records.md").write_text(render_records(recs), encoding="utf-8")
    print(f"OK — {len(recs)} records valid, {len(corridors)} corridor(s); "
          f"{sum(1 for v in cov.values() if v=='verified')} verified / "
          f"{sum(1 for v in cov.values() if v=='draft')} draft cell(s).")
    print(f"     schema validation backend: {VALIDATOR_BACKEND}")
    cm_matrix = claim_class_matrix(recs)
    n_legal = sum(v for (cc, _), v in cm_matrix.items() if cc == "tier1_legal")
    n_oper = sum(v for (cc, _), v in cm_matrix.items() if cc == "tier2_operational")
    print(f"     claim_class: {n_legal} tier1_legal · {n_oper} tier2_operational; "
          f"citable subset (tier1_legal + in_force + resolution_text): {len(citable)} records.")
    if analysis is not None:
        comp = analysis.get("compatibility", {})
        print(f"     analysis layer: {len(comp.get('pairs', []))} compatibility pairs, "
              f"{len(analysis.get('interaction_sets', {}).get('sets', []))} interaction sets, "
              f"{len(analysis.get('open_questions', {}).get('questions', []))} open questions.")
        ndiv = sum(1 for c in corridors if c.get("divergence"))
        print(f"     cross-layer: {len(corridors)} corridors checked against §5.14; "
              f"{ndiv} declared divergence(s); category agreement enforced.")
        cm = analysis.get("computed")
        if cm:
            nf = sum(len(v) for v in cm.get("findings_by_cause", {}).values())
            print(f"     computed layer (preview): directed {cm['directed_edges']['agreement']} · "
                  f"undirected {cm['undirected_pairs']['agreement']} reproduce authored; "
                  f"{nf} finding(s) {list(cm.get('findings_by_cause', {}).keys()) or ''}.")
        tl = analysis.get("computed_timeline")
        ec = analysis.get("event_calendar")
        if tl and ec:
            ot = tl.get("undirected_agreement_over_time", [])
            cav0 = ot[0]["transition_caveated_pairs"]["count"] if ot else "?"
            cavN = ot[-1]["transition_caveated_pairs"]["count"] if ot else "?"
            print(f"     time engine: {len(ec.get('events', []))} events (provenance "
                  f"clean={tl.get('event_provenance', {}).get('clean')}); transition-caveated pairs "
                  f"{cav0} today → {cavN} at horizon; date-aware compose() available.")
        sub = analysis.get("computed_substrate")
        if sub:
            cov = sub.get("coverage", {})
            print(f"     constraint substrate: {cov.get('cells_populated')}/96 cells "
                  f"(provenance clean={sub.get('substrate_provenance', {}).get('clean')}); "
                  f"authored corridors derivable {cov.get('authored_corridors_definite')}; "
                  f"cross-check vs signal clean={sub.get('cross_check', {}).get('clean')}.")
        wl = analysis.get("verification_worklist")
        if wl:
            h = wl.get("headline", {})
            print(f"     verification worklist: {h.get('tier1_legal_unverified')} tier1_legal cells unverified "
                  f"(all lacking url={h.get('all_unverified_lack_url')}); evidence_tier gate enforced.")
        sp = analysis.get("computed_stakeholder_profiles")
        if sp:
            sdb = analysis.get("stakeholder_database", {})
            np = len(sp.get("profiles", []))
            npe = len(sdb.get("stakeholders", {}))
            print(f"     stakeholder projection (Atlas §8): {npe} personas; {np} worked profiles; "
                  f"provenance clean={sp.get('provenance', {}).get('clean')} (no new facts; preview).")
        ck = analysis.get("computed_corridor_skeletons")
        if ck:
            cv = ck.get("coverage", {})
            print(f"     edge layer: {cv.get('authored_rich_corridors')} rich + {cv.get('computed_skeletons')} "
                  f"computed skeletons = {cv.get('edges_with_a_record')}/{cv.get('edges_total')} edges with a record "
                  f"({cv.get('indeterminate_edges')} indeterminate); cross-check clean={ck.get('cross_check', {}).get('clean')}.")
    print("     wrote dataset.json, COVERAGE.md, records.md")

if __name__ == "__main__":
    main()
