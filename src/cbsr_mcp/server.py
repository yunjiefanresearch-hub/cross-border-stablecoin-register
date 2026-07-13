#!/usr/bin/env python3
"""
Cross-Border Stablecoin Register — MCP server.

Exposes the register as typed query tools over the Model Context Protocol so that
agents can query the cross-jurisdictional differential layer directly, instead of
fetching and parsing the raw JSON. Reads the committed dataset.json (no network).

Run (stdio transport, for Claude Desktop / MCP clients):
    uvx cbsr-mcp                 # installed from PyPI, nothing to clone
    python mcp_server.py         # from a source checkout, after: pip install "mcp[cli]"

Or register in an MCP client config (see MCP_SERVER.md).

Every record returned carries its source.primary, pinpoint, confidence, dates and
version — the same provenance fields a human sees. No data is synthesised here;
the server only filters and reshapes the published dataset.
"""
from __future__ import annotations
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json
import pathlib
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "The 'mcp' package is required. Install it with:  pip install \"mcp[cli]\""
    ) from e

def _load_dataset() -> dict:
    """
    Locate dataset.json in both supported contexts, with no network call.

      1. Installed wheel  -> package data at cbsr_mcp/data/dataset.json
      2. Source checkout  -> the repo-root dataset.json that build.py compiles

    Order matters: an installed package must resolve its OWN pinned dataset and
    never silently pick up a stray dataset.json from the working directory.
    """
    try:
        from importlib.resources import files

        packaged = files("cbsr_mcp").joinpath("data").joinpath("dataset.json")
        if packaged.is_file():
            return json.loads(packaged.read_text(encoding="utf-8"))
    except (ImportError, ModuleNotFoundError, FileNotFoundError, TypeError):
        pass

    here = pathlib.Path(__file__).resolve()
    for base in here.parents:
        candidate = base / "dataset.json"
        if candidate.is_file():
            return json.loads(candidate.read_text(encoding="utf-8"))

    raise SystemExit(
        "dataset.json not found.\n"
        "  installed -> reinstall the package (the dataset ships inside the wheel)\n"
        "  source    -> run `python build.py` first to compile dataset.json"
    )


DATA = _load_dataset()
RECORDS: list[dict] = DATA.get("records", [])
CORRIDORS: list[dict] = DATA.get("corridors", [])

# 15-dimension spec (key -> human description). Mirrors the schema / taxonomy.md.
DIMENSIONS: dict[str, str] = {
    "regulatory_authority": "Authority and statutory basis",
    "issuer_pathway": "Issuer eligibility / licensing pathway (constraint C1)",
    "reserve_backing": "Reserve composition and backing (constraint C2)",
    "capital_requirements": "Issuer capital requirements (constraint C2)",
    "permitted_activity_yield": "Permitted-activity / yield boundary — SPINE 1 (constraint C3)",
    "securities_classification": "Securities classification boundary — SPINE 2 (constraint C4)",
    "bank_nonbank_routing": "Bank / non-bank status and routing prohibitions (constraint C5)",
    "redemption": "Redemption mechanics",
    "custody": "Custody of client assets / reserves (constraint C2 facet)",
    "aml_kyc": "AML / KYC framework",
    "cross_border_data": "Cross-border payment and data sovereignty (constraint C6)",
    "monetary_sovereignty": "Monetary sovereignty / non-domestic-currency caps (constraint C7)",
    "disclosure_reporting": "Disclosure, reporting, supervisory coordination (constraint C8)",
    "distribution": "Distribution and offering restrictions",
    "implementation_status": "Implementation maturity and timeline",
}
JURISDICTIONS: dict[str, str] = {
    "US": "United States", "HK": "Hong Kong", "EU": "European Union",
    "UK": "United Kingdom", "SG": "Singapore", "CN": "Mainland China",
    "BR": "Brazil", "CH": "Switzerland", "AE": "United Arab Emirates",
    "TW": "Taiwan", "JP": "Japan", "KR": "South Korea",
}

mcp = FastMCP("cross-border-stablecoin-register")


def _summary(r: dict) -> dict:
    """A compact, provenance-bearing view of a record (use get_record for the full object)."""
    src = r.get("source", {}) or {}
    return {
        "id": r.get("id"),
        "jurisdiction": r.get("jurisdiction"),
        "dimension": r.get("dimension"),
        "constraint_ref": r.get("constraint_ref"),
        "requirement_summary": r.get("requirement_summary"),
        "source": {"primary": src.get("primary"), "pinpoint": src.get("pinpoint"), "url": src.get("url") or None},
        "status": r.get("status"),
        "effective_date": r.get("effective_date"),
        "confidence": r.get("confidence"),
        "claim_class": r.get("claim_class"),
        "evidence_tier": r.get("evidence_tier", "unset"),
        "binding_status": r.get("binding_status"),
        "last_reviewed": r.get("last_reviewed"),
        "version_added": r.get("version_added"),
    }


@mcp.tool()
def about() -> dict:
    """Register metadata: name, version, record count, license, DOI, and the verification rule."""
    return {
        "name": DATA.get("name"),
        "version": DATA.get("version"),
        "generated": DATA.get("generated"),
        "record_count": DATA.get("record_count"),
        "corridor_count": len(CORRIDORS),
        "citable_count": DATA.get("citable_subset", {}).get("count", 0),
        "doi": "10.5281/zenodo.20730358",
        "license": {"data": "CC-BY-4.0", "code": "Apache-2.0"},
        "spines": ["permitted_activity_yield", "securities_classification"],
        "evidence_model": {
            "axes": {
                "claim_class": "kind of claim — tier1_legal (proposition of law) vs tier2_operational (market/operational fact)",
                "evidence_tier": "provenance strength — resolution_text vs mixed vs firm_summary",
                "status": "force — in_force vs transitional/proposed/consultation",
                "binding_status": "binding status of the cited instrument — in_force_enacted vs made_not_commenced / finalized_policy_pending / pending_proposal / prohibition / no_regime; caps citability (resolution_text requires in_force_enacted)",
            },
            "citable_subset": "tier1_legal AND in_force AND resolution_text — see the citable_law() tool",
        },
        "temporal": {
            "date_aware_compose": "compose_corridor(origin, destination, as_of=ISO_DATE) evaluates as of a date",
            "event_calendar": f"{len(EVENT_CALENDAR.get('events', []))} dated/contingent tier1_legal events — see event_calendar() and corridor_timeline()",
        },
        "substrate": {
            "constraint_substrate": f"{COMPUTED_SUBSTRATE.get('coverage', {}).get('cells_populated', 0)}/96 C1-C8 poles populated — see constraint_substrate()",
            "deep_compose": "compose_via_substrate(origin, destination) derives feasibility through the interaction-set rules; indeterminate where poles are unset",
        },
        "tool_count": 33,
        "verification_rule": (
            "A record is verified only when it has no open markers AND a human has checked "
            "every source.primary and pinpoint against the instrument itself. Citations are "
            "never machine-generated. Some records are transcribed from the maintainer's "
            "Compliance Matrix and pending final primary-source verification (source.url empty)."
        ),
    }


@mcp.tool()
def list_jurisdictions() -> list[dict]:
    """List jurisdictions covered, with full name and record count."""
    counts: dict[str, int] = {}
    for r in RECORDS:
        counts[r["jurisdiction"]] = counts.get(r["jurisdiction"], 0) + 1
    return [
        {"code": code, "name": JURISDICTIONS.get(code, code), "records": counts.get(code, 0)}
        for code in sorted(counts, key=lambda c: -counts[c])
    ]


@mcp.tool()
def list_dimensions() -> list[dict]:
    """List the 15 dimensions with descriptions and how many records each has."""
    counts: dict[str, int] = {}
    for r in RECORDS:
        counts[r["dimension"]] = counts.get(r["dimension"], 0) + 1
    return [
        {"key": k, "description": v, "records": counts.get(k, 0),
         "spine": k in ("permitted_activity_yield", "securities_classification")}
        for k, v in DIMENSIONS.items()
    ]


@mcp.tool()
def get_record(record_id: str) -> dict:
    """Return the full record (all fields including requirement_structured and interpretation_note) by its id."""
    for r in RECORDS:
        if r.get("id") == record_id:
            return r
    return {"error": f"No record with id '{record_id}'.",
            "hint": "Use query() or search() to find record ids."}


@mcp.tool()
def query(
    jurisdiction: Optional[str] = None,
    dimension: Optional[str] = None,
    status: Optional[str] = None,
    confidence: Optional[str] = None,
    constraint_ref: Optional[str] = None,
) -> dict:
    """
    Typed filter over the register. All arguments optional and combined with AND.

    Args:
        jurisdiction: e.g. 'US', 'HK', 'EU', 'UK', 'SG', 'CN'.
        dimension: one of the 15 dimension keys (see list_dimensions).
        status: 'in_force' | 'transitional' | 'proposed' | 'consultation'.
        confidence: 'high' | 'medium' | 'low'.
        constraint_ref: e.g. 'C1'..'C8' (or composite like 'C3xC4').
    Returns a count and the matching record summaries.
    """
    j = jurisdiction.upper() if jurisdiction else None
    out = []
    for r in RECORDS:
        if j and r.get("jurisdiction") != j:
            continue
        if dimension and r.get("dimension") != dimension:
            continue
        if status and r.get("status") != status:
            continue
        if confidence and r.get("confidence") != confidence:
            continue
        if constraint_ref and (r.get("constraint_ref") or "") != constraint_ref:
            continue
        out.append(_summary(r))
    return {"count": len(out), "filters": {
        "jurisdiction": j, "dimension": dimension, "status": status,
        "confidence": confidence, "constraint_ref": constraint_ref}, "records": out}


@mcp.tool()
def compare_dimension(dimension: str) -> dict:
    """
    Compare all jurisdictions on a single dimension — the core differential view.
    e.g. compare_dimension('monetary_sovereignty') returns the EU cap vs HK restriction
    vs CN prohibition spectrum, each with its source.
    """
    if dimension not in DIMENSIONS:
        return {"error": f"Unknown dimension '{dimension}'.",
                "valid_dimensions": list(DIMENSIONS.keys())}
    rows = [_summary(r) for r in RECORDS if r.get("dimension") == dimension]
    rows.sort(key=lambda x: x["jurisdiction"])
    return {"dimension": dimension, "description": DIMENSIONS[dimension],
            "jurisdiction_count": len(rows), "records": rows}


@mcp.tool()
def jurisdiction_profile(jurisdiction: str) -> dict:
    """Return all records for one jurisdiction, ordered by the dimension framework."""
    j = jurisdiction.upper()
    if j not in JURISDICTIONS:
        return {"error": f"Unknown jurisdiction '{jurisdiction}'.",
                "valid_jurisdictions": list(JURISDICTIONS.keys())}
    dim_order = list(DIMENSIONS.keys())
    rows = [r for r in RECORDS if r.get("jurisdiction") == j]
    rows.sort(key=lambda r: dim_order.index(r["dimension"]) if r["dimension"] in dim_order else 99)
    return {"jurisdiction": j, "name": JURISDICTIONS[j],
            "record_count": len(rows), "records": [_summary(r) for r in rows]}


@mcp.tool()
def search(keyword: str) -> dict:
    """Keyword search across jurisdiction, dimension, authority, requirement summary, source, and tags."""
    term = (keyword or "").strip().lower()
    if not term:
        return {"error": "Empty keyword."}
    out = []
    for r in RECORDS:
        hay = " ".join([
            r.get("jurisdiction", ""), r.get("dimension", ""), r.get("authority", ""),
            r.get("requirement_summary", ""), r.get("instrument_label_local", ""),
            (r.get("source", {}) or {}).get("primary", ""),
            (r.get("source", {}) or {}).get("pinpoint", ""),
            " ".join(r.get("tags", []) or []), r.get("constraint_ref", "") or "",
        ]).lower()
        if term in hay:
            out.append(_summary(r))
    return {"keyword": keyword, "count": len(out), "records": out}


@mcp.tool()
def get_corridor(corridor_id: Optional[str] = None) -> dict:
    """
    Return corridor model(s) — what clears and what breaks at each regulatory boundary
    along a cross-border flow. Omit corridor_id to list all corridors.
    """
    if corridor_id is None:
        return {"count": len(CORRIDORS),
                "corridors": [{"corridor_id": c.get("corridor_id"), "name": c.get("name")} for c in CORRIDORS]}
    for c in CORRIDORS:
        if c.get("corridor_id") == corridor_id:
            return c
    return {"error": f"No corridor with id '{corridor_id}'.",
            "available": [c.get("corridor_id") for c in CORRIDORS]}


@mcp.tool()
def coverage() -> dict:
    """
    Coverage matrix: for each jurisdiction × dimension, whether a record exists ('verified')
    or not ('planned'). Useful for an agent to know where data is and is not available.
    """
    present = {(r["jurisdiction"], r["dimension"]) for r in RECORDS}
    jur = sorted({r["jurisdiction"] for r in RECORDS})
    grid = {}
    for jcode in jur:
        grid[jcode] = {dim: ("verified" if (jcode, dim) in present else "planned")
                       for dim in DIMENSIONS}
    return {"jurisdictions": jur, "dimensions": list(DIMENSIONS.keys()),
            "verified_cells": len(present), "grid": grid}


# ---------------------------------------------------------------------------
# Analysis layer — the Cross-Border Stablecoin Architecture paper's payload,
# encoded as queryable data (compatibility matrix, interaction sets, patterns,
# open questions). Present in dataset.json from v0.5.0.
# ---------------------------------------------------------------------------
ANALYSIS: dict = DATA.get("analysis", {})


@mcp.tool()
def compatibility(jurisdiction: Optional[str] = None,
                  other: Optional[str] = None,
                  category: Optional[str] = None) -> dict:
    """
    Query the §5.14 pairwise compatibility matrix (all 66 jurisdiction pairs from the
    Architecture working paper). Each pair carries a category (I dual-authorization /
    I/II hybrid / II partnership / III composition-problem-unresolved), the operative
    interaction sets (A-F), a Category-III axis where applicable (prohibition /
    pre_regime / counterparty_conditional), and a binding-constraint note.

    Args:
        jurisdiction: filter to pairs involving this code (e.g., 'HK').
        other: with `jurisdiction`, return the single pair (e.g., jurisdiction='HK', other='CN').
        category: filter by 'I' | 'I/II' | 'II' | 'III'.
    """
    comp = ANALYSIS.get("compatibility")
    if not comp:
        return {"error": "analysis layer not present in dataset.json (run scripts/build_analysis.py then build.py)"}
    pairs = comp.get("pairs", [])
    j = jurisdiction.upper() if jurisdiction else None
    o = other.upper() if other else None
    if j and o:
        key = "-".join(sorted([j, o]))
        hit = next((p for p in pairs if p["pair"] == key), None)
        return hit or {"error": f"no pair {key}"}
    out = pairs
    if j:
        out = [p for p in out if j in p["jurisdictions"]]
    if category:
        out = [p for p in out if p["category"] == category]
    return {"categories": comp.get("categories"), "category_iii_axes": comp.get("category_iii_axes"),
            "summary_observation": comp.get("summary_observation"),
            "count": len(out), "pairs": out}


@mcp.tool()
def interaction_sets() -> dict:
    """
    The six constraint-interaction sets (A-F) from Architecture §2.9 — the constraint pairs
    through which joint binding generates composition problems, each with its mechanism and a
    worked example. These are referenced per pair by compatibility().
    """
    return ANALYSIS.get("interaction_sets") or {"error": "analysis layer not present"}


@mcp.tool()
def architectural_patterns() -> dict:
    """
    The Architecture paper's architectural patterns: the PRC three-pattern typology (§3.3 —
    direct subsidiary licensing / partnership distribution / separated-entity), the portable
    three-layer routing architecture (§4/§6 — Layer 1 compliant issuer, Layer 2 user-directed
    routing, Layer 3 yield-bearing fund), the §4.4 five-factor operational test, and the six
    design principles.
    """
    return ANALYSIS.get("architectural_patterns") or {"error": "analysis layer not present"}


@mcp.tool()
def open_questions() -> dict:
    """
    The §7 open regulatory questions (7.1–7.5) whose resolution will determine which architectural
    options become operationally viable, each preserved with its conditional-status flag.
    """
    return ANALYSIS.get("open_questions") or {"error": "analysis layer not present"}


# ---------------------------------------------------------------------------
# Computed layer (the compose() preview) + verification queue. Present from v0.6.0.
# These are the first *computing* tools (not just retrieval): they derive a pair's
# feasibility from the per-jurisdiction signal table and the Atlas algorithm, and
# expose the computed-vs-authored diff.
# ---------------------------------------------------------------------------
COMPUTED: dict = ANALYSIS.get("computed", {})
EVENT_CALENDAR: dict = ANALYSIS.get("event_calendar", {})
COMPUTED_TIMELINE: dict = ANALYSIS.get("computed_timeline", {})
SUBSTRATE: dict = ANALYSIS.get("constraint_substrate", {})
COMPUTED_SUBSTRATE: dict = ANALYSIS.get("computed_substrate", {})
VERIFICATION_WORKLIST: dict = ANALYSIS.get("verification_worklist", {})
STAKEHOLDER_DB: dict = ANALYSIS.get("stakeholder_database", {})
COMPUTED_STAKEHOLDER_PROFILES: dict = ANALYSIS.get("computed_stakeholder_profiles", {})
COMPUTED_CORRIDOR_SKELETONS: dict = ANALYSIS.get("computed_corridor_skeletons", {})
_SUB_SEVERITY = {"blocked": 4, "III": 3, "II": 2, "I": 1, "pre_regime": 0}
_GATE_CLASS = {"open": "I", "open_capped": "I", "comparability": "II", "channel": "II",
               "usage_channel": "II", "fx_counterparty": "II", "transition": "T",
               "pre_regime": "pre_regime", "prohibition": "blocked"}


def _signals_as_of(date_str: Optional[str]) -> dict:
    """Copy the base signal table and apply every scheduled/in_force event effective on/before date_str.

    Contingent events (no firm date) are never applied here. Mirrors scripts/compose.signals_as_of so
    the MCP date-aware compose() matches the build artifact.
    """
    import copy
    base = copy.deepcopy(COMPUTED.get("jurisdiction_signals", {}))
    if not date_str:
        return base
    dated = [e for e in EVENT_CALENDAR.get("events", [])
             if e.get("status") in ("scheduled", "in_force") and e.get("effective_date")]
    for e in sorted(dated, key=lambda e: e["effective_date"]):
        if e["effective_date"] <= date_str:
            for eff in e.get("effect", []):
                j, fld = e.get("jurisdiction"), eff.get("field")
                if j in base and fld:
                    base[j][fld] = eff.get("to")
    return base


def _compose_directed(origin: str, dest: str, signals: Optional[dict] = None) -> dict:
    sig = signals if signals is not None else COMPUTED.get("jurisdiction_signals", {})
    so, sd = sig.get(origin), sig.get(dest)
    if not so or not sd:
        return {"error": f"unknown jurisdiction(s): {origin}/{dest}"}
    if not so.get("exportable_token", True):
        axis = "prohibition" if so.get("regime_status") == "prohibition" else "pre_regime"
        return {"class": "III", "rule": f"origin_drag:{axis}",
                "explain": f"{origin} has no exportable, comprehensively authorizable private token "
                           f"({so.get('basis')}); lawful options are partnership/coordination, not direct issuance.",
                "origin_override": so.get("egress_override", False)}
    cls = _GATE_CLASS.get(sd.get("inbound_gate"), "?")
    return {"class": cls, "rule": f"destination_gate:{sd.get('inbound_gate')}",
            "explain": f"At the destination, {dest} applies an inbound gate of type "
                       f"'{sd.get('inbound_gate')}' ({sd.get('basis')}); origin {origin} has an exportable token.",
            "origin_override": so.get("egress_override", False)}


@mcp.tool()
def compose_corridor(origin: str, destination: str, as_of: Optional[str] = None) -> dict:
    """
    COMPUTE the directed feasibility of an origin->destination corridor from the per-jurisdiction
    signal table and the Corridor Atlas algorithm (origin drag, then destination-determined inbound
    class) — not a lookup. Pass `as_of` (an ISO date, e.g. '2027-06-01') to evaluate the corridor as of
    that date: every scheduled/in_force regulatory event effective by then is applied first, so the same
    edge can read Category III/T today and Category I after a regime is operative. Returns the computed
    class, the rule that fired, the operative §5.14 interaction sets, and (if an authored corridor
    exists) the computed-vs-authored comparison.
    """
    o, d = origin.upper(), destination.upper()
    if not COMPUTED:
        return {"error": "computed layer not present (run scripts/compose.py then build.py)"}
    signals = _signals_as_of(as_of) if as_of else None
    res = _compose_directed(o, d, signals)
    if "error" in res:
        return res
    # operative interaction sets from the undirected §5.14 pair
    comp = ANALYSIS.get("compatibility", {})
    row = next((p for p in comp.get("pairs", []) if p["pair"] == "-".join(sorted([o, d]))), {})
    # authored directed corridor, if one exists
    authored = next((e for e in COMPUTED.get("directed_edges", {}).get("edges", [])
                     if e["edge"] == f"{o}->{d}"), None)
    out = {"edge": f"{o}->{d}", "as_of": as_of or EVENT_CALENDAR.get("as_of_base", "base"),
           "computed_class": res["class"], "rule": res["rule"],
           "explanation": res["explain"], "origin_override": res["origin_override"],
           "operative_interaction_sets": row.get("interaction_sets"),
           "section_5_14_category": row.get("category"),
           "authored_corridor": authored,
           "note": "computed layer is a preview (Atlas §3.2 rule); not asserted authoritative — see findings_by_cause."}
    if as_of:
        base_res = _compose_directed(o, d)
        out["base_class"] = base_res.get("class")
        out["changed_from_base"] = base_res.get("class") != res["class"]
    return out


@mcp.tool()
def explain_feasibility(origin: str, destination: str) -> dict:
    """
    Explain WHY a corridor falls in its feasibility class: the rule that fired (origin drag vs
    destination gate), the justifying node-record basis for each side's signal, the operative
    interaction sets, and whether the computed class agrees with the authored classification.
    """
    o, d = origin.upper(), destination.upper()
    if not COMPUTED:
        return {"error": "computed layer not present (run scripts/compose.py then build.py)"}
    sig = COMPUTED.get("jurisdiction_signals", {})
    res = _compose_directed(o, d)
    if "error" in res:
        return res
    edge = next((e for e in COMPUTED.get("directed_edges", {}).get("edges", []) if e["edge"] == f"{o}->{d}"), None)
    return {"edge": f"{o}->{d}", "computed_class": res["class"], "rule_fired": res["rule"],
            "why": res["explain"],
            "origin_signal": sig.get(o), "destination_signal": sig.get(d),
            "computed_vs_authored": edge,
            "reduction_note": "The directed class composes origin drag with the destination inbound gate; "
                              "the undirected §5.14 category is a reduction of the two directed classes."}


@mcp.tool()
def verification_report() -> dict:
    """
    The verification queue: which records are confirmed against official primary text and which are
    still pending. Buckets records by evidence_tier (resolution_text / mixed / firm_summary / unset),
    flags the largest backlog (the legacy seven-jurisdiction records with no evidence_tier), and lists
    records that lack a source.url. The view a maintainer uses to drive the next verification pass.
    """
    from collections import defaultdict
    buckets = defaultdict(list)
    no_url = []
    for r in RECORDS:
        tier = r.get("evidence_tier", "unset")
        buckets[tier].append(r["id"])
        if not (r.get("source") or {}).get("url"):
            no_url.append(r["id"])
    legacy = sorted(r["id"] for r in RECORDS
                    if r.get("evidence_tier") is None or r.get("evidence_tier") == "unset")
    return {
        "totals": {k: len(v) for k, v in sorted(buckets.items())},
        "records_with_source_url": len(RECORDS) - len(no_url),
        "records_total": len(RECORDS),
        "backlog_unset_legacy": {"count": len(legacy), "ids": legacy,
                                 "note": "the seven-jurisdiction records that predate the evidence_tier field — the next verification pass"},
        "pending_no_url": {"count": len(no_url), "ids": sorted(no_url)},
        "by_tier": {k: sorted(v) for k, v in sorted(buckets.items())},
        "legend": {"resolution_text": "confirmed against official primary text",
                   "mixed": "core point confirmed; some operational detail pending",
                   "firm_summary": "practitioner-corroborated, pending official-text check",
                   "unset": "predates the evidence_tier field (legacy)"},
    }


@mcp.tool()
def verification_worklist(jurisdiction: Optional[str] = None) -> dict:
    """
    The primary-source verification worklist: for every still-unverified cell, exactly what is missing
    to reach the next evidence tier and the instrument/pinpoint to check against. This scopes the
    verification pass that lights up the constraint substrate and retires the standing liability (every
    compose()/substrate result rests on these unverified cells). Verification is external work and is
    never fabricated; this is the checklist that drives it. Optional jurisdiction filter.
    """
    if not VERIFICATION_WORKLIST:
        return {"error": "verification worklist not present (run scripts/build_worklist.py then build.py)"}
    items = VERIFICATION_WORKLIST.get("items", [])
    if jurisdiction:
        j = jurisdiction.upper()
        items = [it for it in items if it.get("jurisdiction") == j]
    return {"headline": VERIFICATION_WORKLIST.get("headline"),
            "tier_requirements": VERIFICATION_WORKLIST.get("tier_requirements"),
            "count": len(items), "items": items,
            "note": "evidence_tier is enforced by the build: a record may only claim a tier it has the evidence for."}


@mcp.tool()
def citable_law(jurisdiction: Optional[str] = None,
                dimension: Optional[str] = None) -> dict:
    """
    The lawyer-citable subset: only records that are a proposition of law (claim_class=tier1_legal),
    currently in force (status=in_force), AND confirmed against the official statutory/regulatory text
    (evidence_tier=resolution_text). Each row returns the binding instrument, the pinpoint locator, and
    the official URL — everything a citation needs.

    This is the 'show me only what I could cite' view for lawyers and supervisors. Operational/market
    facts (claim_class=tier2_operational) are excluded by KIND even when well-sourced (a confirmed
    product launch is a true fact, not a proposition of law); draft provisions are excluded by status;
    unverified legal points are excluded by tier. The same subset is published as `citable_subset` in
    dataset.json and enforced by the build (a citable record must carry source.url + pinpoint).

    Optional filters narrow to a jurisdiction (e.g. 'CH') and/or a dimension (e.g. 'reserve_backing').
    """
    j = jurisdiction.upper() if jurisdiction else None
    sub = DATA.get("citable_subset", {})
    rows = sub.get("records", [])
    if j:
        rows = [r for r in rows if r.get("jurisdiction") == j]
    if dimension:
        rows = [r for r in rows if r.get("dimension") == dimension]
    return {
        "filter": sub.get("filter", {}),
        "count": len(rows),
        "total_citable": sub.get("count", 0),
        "records": rows,
        "note": ("Each record is citable as current binding law: tier1_legal + in_force + "
                 "resolution_text, with an official source.url and pinpoint. Use get_record(id) "
                 "for the full object, including the secondary corroboration and interpretation note."),
    }


@mcp.tool()
def event_calendar(jurisdiction: Optional[str] = None) -> dict:
    """
    The regulatory event calendar driving date-aware compose(): dated/contingent CHANGES IN LAW that
    move a jurisdiction's signal. 'scheduled' events carry an effective_date (applied by
    compose_corridor(as_of=...)); 'contingent' events are bills with no firm date (surfaced as pending
    transitions, never applied by date); 'in_force' events are already effective. Every event is a
    tier1_legal change backed by tier1_legal records — a market launch is never an event (those live in
    a record's operational_notes). Optional jurisdiction filter.
    """
    if not EVENT_CALENDAR:
        return {"error": "event calendar not present (run scripts/compose.py then build.py)"}
    evs = EVENT_CALENDAR.get("events", [])
    if jurisdiction:
        j = jurisdiction.upper()
        evs = [e for e in evs if e.get("jurisdiction") == j]
    return {"as_of_base": EVENT_CALENDAR.get("as_of_base"), "count": len(evs), "events": evs,
            "status_values": EVENT_CALENDAR.get("status_values"),
            "provenance": COMPUTED_TIMELINE.get("event_provenance", {})}


@mcp.tool()
def corridor_timeline(origin: str, destination: str) -> dict:
    """
    The dated future of a directed corridor: today's class, the scheduled transitions that change it
    (with their effective dates), and any contingent transitions (a bill that, if enacted, would change
    the verdict — shown as 'class_if_enacted', never folded into the dated line). This is how the engine
    answers "blocked/Category T today, Category I after the regime is operative." Computes the timeline
    live for any pair, including pairs without an authored corridor.
    """
    o, d = origin.upper(), destination.upper()
    sig0 = COMPUTED.get("jurisdiction_signals", {})
    if not sig0 or o not in sig0 or d not in sig0:
        return {"error": f"unknown jurisdiction(s) or computed layer absent: {o}/{d}"}
    today = _compose_directed(o, d)
    events = EVENT_CALENDAR.get("events", [])
    affects = lambda e: e.get("jurisdiction") in (o, d) and e.get("effect")
    # cumulative scheduled timeline
    import copy
    running = copy.deepcopy(sig0)
    prev, transitions = today.get("class"), []
    for e in sorted([e for e in events if e.get("status") in ("scheduled", "in_force")
                     and e.get("effective_date") and affects(e)], key=lambda e: e["effective_date"]):
        for eff in e.get("effect", []):
            if e["jurisdiction"] in running and eff.get("field"):
                running[e["jurisdiction"]][eff["field"]] = eff.get("to")
        cls = _compose_directed(o, d, running).get("class")
        transitions.append({"date": e["effective_date"], "precision": e.get("precision"),
                            "status": e["status"], "event_id": e["id"], "title": e.get("title"),
                            "class_before": prev, "class_after": cls, "changed": cls != prev})
        prev = cls
    pending = []
    for e in [e for e in events if e.get("status") == "contingent" and affects(e)]:
        hyp = copy.deepcopy(sig0)
        for eff in e.get("effect", []):
            if e["jurisdiction"] in hyp and eff.get("field"):
                hyp[e["jurisdiction"]][eff["field"]] = eff.get("to")
        cls = _compose_directed(o, d, hyp).get("class")
        pending.append({"event_id": e["id"], "title": e.get("title"), "trigger": e.get("trigger"),
                        "class_if_enacted": cls, "would_change": cls != today.get("class")})
    return {"edge": f"{o}->{d}", "today_class": today.get("class"),
            "scheduled_transitions": transitions, "pending_contingent": pending,
            "next_scheduled_change": next((t for t in transitions if t["changed"]), None)}


def _sub_cell(j, c):
    return SUBSTRATE.get("cells", {}).get(j, {}).get(c)


def _sub_attr(cell, key, default=None):
    return (cell or {}).get("attributes", {}).get(key, default)


@mcp.tool()
def constraint_substrate(jurisdiction: Optional[str] = None, constraint: Optional[str] = None) -> dict:
    """
    The constraint substrate: each (jurisdiction × constraint C1–C8) as a structured POLE from a
    controlled vocabulary, citing the tier1_legal record(s) it is transcribed from. This is the deeper
    layer beneath the single inbound-gate signal — feasibility is composed through these poles via the
    interaction-set rules (see compose_via_substrate). Poles exist only where a tier1_legal record backs
    them; absent cells are unset (coverage is bounded by the verification/cell-authoring backlog).
    Optional jurisdiction and/or constraint (e.g. 'C7') filters.
    """
    if not SUBSTRATE:
        return {"error": "constraint substrate not present (run scripts/substrate.py then build.py)"}
    cells = SUBSTRATE.get("cells", {})
    if jurisdiction:
        j = jurisdiction.upper()
        sub = {j: cells.get(j, {})}
    else:
        sub = cells
    if constraint:
        c = constraint.upper()
        sub = {j: {c: v[c]} for j, v in sub.items() if c in v}
    return {"pole_vocabulary": SUBSTRATE.get("pole_vocabulary"),
            "coverage": COMPUTED_SUBSTRATE.get("coverage"),
            "provenance": COMPUTED_SUBSTRATE.get("substrate_provenance", {}).get("clean"),
            "cells": sub}


@mcp.tool()
def compose_via_substrate(origin: str, destination: str) -> dict:
    """
    DERIVE a directed corridor's feasibility by composing the two jurisdictions' C1–C8 poles through the
    interaction-set rules — the deeper engine behind compose_corridor's single inbound-gate. Returns the
    derived class, the per-set verdicts, and (where definite) the cross-check against the signal-table
    compose(). Returns 'indeterminate' (with the missing poles) where a load-bearing pole is unset — it
    never guesses. This is the constraint-substrate thesis as a running function.
    """
    o, d = origin.upper(), destination.upper()
    if not SUBSTRATE:
        return {"error": "constraint substrate not present (run scripts/substrate.py then build.py)"}
    o1, oC6, oC8 = _sub_cell(o, "C1"), _sub_cell(o, "C6"), _sub_cell(o, "C8")
    d1, d7 = _sub_cell(d, "C1"), _sub_cell(d, "C7")
    missing, verdicts, dclass = [], {}, None
    if o1 is None:
        missing.append(f"{o}.C1")
    elif _sub_attr(o1, "exportable_token", None) is False:
        sig = _compose_directed(o, d).get("class")
        return {"edge": f"{o}->{d}", "substrate_class": "III", "rule": "origin_drag:no_exportable_token",
                "set_verdicts": {"C": "origin_drag"}, "missing_poles": [], "signal_class": sig,
                "agree_with_signal": sig == "III",
                "explain": f"{o} has no exportable, authorizable private token (C1={o1.get('pole')})."}
    if d1 is None:
        missing.append(f"{d}.C1")
    elif d1.get("pole") == "prohibition":
        dclass, verdicts["C"] = "blocked", "dest C1=prohibition (issuance prohibited)"
    elif d1.get("pole") == "no_pathway":
        dclass, verdicts["C"] = "pre_regime", "dest C1=no_pathway (no operative issuance regime yet)"
    elif d7 is not None and d7.get("pole") == "prohibition":
        dclass, verdicts["D"] = "blocked", "dest C7=prohibition"
    elif d7 is None:
        missing.append(f"{d}.C7")
    else:
        p7 = d7.get("pole")
        if p7 == "channelled":
            dclass, verdicts["D"] = "II", "dest C7=channelled (channel determination required)"
        elif p7 == "usage_capped":
            dclass, verdicts["D"] = "I", "dest C7=usage_capped (dual authorization, scale-capped)"
        elif p7 == "open":
            dclass, verdicts["D"] = "I", "dest C7=open (dual authorization available)"
            verdicts["C"] = f"dest C1={d1.get('pole')} (authorizable)"
        else:
            dclass = "I"
    if missing:
        return {"edge": f"{o}->{d}", "substrate_class": "indeterminate", "rule": "missing_load_bearing_poles",
                "set_verdicts": verdicts, "missing_poles": sorted(set(missing)),
                "explain": f"cannot derive from constraints: poles unset for {', '.join(sorted(set(missing)))}."}
    if dclass != "blocked" and d1.get("pole") in ("licence_gated", "closed_set", "host_currency_first", "open"):
        if _sub_attr(oC6, "blocks_supervisory_sharing", False) or (_sub_attr(oC8, "supervisory_sharing", True) is False):
            verdicts["A"] = "origin data-sovereignty blocks supervisory sharing; dest eligibility unsatisfiable"
            if _SUB_SEVERITY["III"] > _SUB_SEVERITY.get(dclass, 0):
                dclass = "III"
    sig = _compose_directed(o, d).get("class")
    return {"edge": f"{o}->{d}", "substrate_class": dclass, "rule": "substrate_interaction_sets",
            "set_verdicts": verdicts, "missing_poles": [], "signal_class": sig,
            "agree_with_signal": dclass == sig,
            "explain": f"derived from constraint poles via interaction sets {sorted(verdicts)}."}


# ---------------------------------------------------------------------------
# Atlas §8 — stakeholder projection. profile_for re-projects an already-derived
# corridor (class + poles + inbound mechanism) through a persona's lens; it adds
# no new legal facts and is preview, bounded by the verification status of the
# cells it reads.
# ---------------------------------------------------------------------------
_SH_IMPLICATION = {
    "C1": {"open": "issuance open", "licence_gated": "issuance is authorization-gated",
           "closed_set": "issuance limited to a defined set of entities",
           "host_currency_first": "host-currency issuance prioritized",
           "no_pathway": "no operative issuance pathway yet", "prohibition": "issuance prohibited"},
    "C2": {"prescribed_hqla": "reserve must be high-quality liquid assets",
           "prescribed_flex": "reserve prescribed with some flexibility", "informational": "reserve disclosure only"},
    "C3": {"permitted": "yield permitted", "prohibited_issuer": "issuer may not pay yield",
           "prohibited_incl_agents": "issuer and agents may not pay yield", "silent": "yield treatment unsettled"},
    "C4": {"payment_instrument": "treated as a payment instrument, not a security",
           "contested_routing": "classification turns on the routing structure",
           "security": "treated as a security / unauthorized offering"},
    "C5": {"bank_only": "bank-only issuance", "bank_and_nonbank": "bank and non-bank issuers admitted",
           "layered_separation": "roles separated by licensed function", "unset": "routing architecture unsettled"},
    "C6": {"open": "no data-localization barrier to supervisory sharing", "transfer_gated": "cross-border transfer is gated",
           "localized": "data localization applies", "restrictive": "data sharing restricted"},
    "C7": {"open": "no usage cap; dual authorization available", "usage_capped": "scale / usage capped",
           "channelled": "foreign tokens admitted only via a determination / channel", "prohibition": "foreign tokens prohibited"},
    "C8": {"coordinated": "supervisory coordination available", "constrained": "supervisory coordination constrained"},
}


@mcp.tool()
def stakeholder_database() -> dict:
    """The Atlas §8 stakeholder catalogue: the actor personas (issuer, distributor, regulators, treasury,
    holder, ...), each with its lens, the C1–C8 constraints that bear on it, and the corridor archetypes
    (RC/SC/TC/DC) it engages. Pair with profile_for() to project a corridor onto a persona."""
    if not STAKEHOLDER_DB:
        return {"error": "stakeholder database not present (run scripts/stakeholders.py then build.py)"}
    return {"archetype_legend": STAKEHOLDER_DB.get("archetype_legend"),
            "stakeholders": STAKEHOLDER_DB.get("stakeholders"), "note": STAKEHOLDER_DB.get("note")}


@mcp.tool()
def profile_for(stakeholder: str, origin: str, destination: str) -> dict:
    """PROJECT a directed corridor onto a stakeholder persona (Atlas §8). Returns the persona's lens, the
    corridor's derived class, a per-constraint reading of the origin/dest poles the persona cares about
    (each citing its backing record), the engaged archetypes and inbound mechanism, and a verification
    caveat. Introduces NO new facts — every line is read from an existing record — so the profile is
    preview, bounded by the verification status of the cells it reads."""
    if not STAKEHOLDER_DB or not SUBSTRATE:
        return {"error": "stakeholder database / substrate not present (run scripts/stakeholders.py + substrate.py then build.py)"}
    s = STAKEHOLDER_DB.get("stakeholders", {}).get(stakeholder)
    if s is None:
        return {"error": f"unknown stakeholder '{stakeholder}'", "known": sorted(STAKEHOLDER_DB.get("stakeholders", {}))}
    o, d = origin.upper(), destination.upper()
    if o not in JURISDICTIONS or d not in JURISDICTIONS:
        return {"error": f"unknown jurisdiction(s): {origin}/{destination}"}
    derived = compose_via_substrate(o, d)
    cls = derived.get("substrate_class")
    id2tier = {r["id"]: r.get("evidence_tier") for r in RECORDS}
    reading, cited = [], []
    for side, j in (("origin", o), ("dest", d)):
        for c in s.get("reads", {}).get(side, []):
            cell = SUBSTRATE.get("cells", {}).get(j, {}).get(c)
            if not cell:
                reading.append({"side": side, "jurisdiction": j, "constraint": c, "pole": None,
                                "implication": "pole unset — indeterminate at the substrate level"})
                continue
            pole = cell.get("pole"); rid = (cell.get("derived_from") or [None])[0]
            reading.append({"side": side, "jurisdiction": j, "constraint": c, "pole": pole,
                            "record": rid, "implication": _SH_IMPLICATION.get(c, {}).get(pole, pole)})
            if rid:
                cited.append(rid)
    corr = next((c for c in CORRIDORS if c.get("origin") == o and c.get("destination") == d), None)
    arche = sorted(set(s.get("archetypes", [])) & set(corr.get("archetypes", []))) if corr else s.get("archetypes")
    cited = sorted(set(cited))
    unver = [r for r in cited if id2tier.get(r) != "resolution_text"]
    return {"edge": f"{o}->{d}", "stakeholder": stakeholder, "label": s.get("label"), "lens": s.get("lens"),
            "corridor_class": cls, "archetypes_engaged": arche,
            "inbound_mechanism": corr.get("inbound_mechanism") if corr else None,
            "reading": reading, "provenance": {"records": cited},
            "verification_status": (f"preview — rests on {len(cited)} cell(s), {len(unver)} not yet verified to "
                                    f"resolution_text; not citable authority until those are verified")}


@mcp.tool()
def edge_coverage() -> dict:
    """Edge-layer coverage: how many directed corridors carry a record. Distinguishes the hand-authored
    RICH corridors (with infrastructure_overlap, bespoke inbound detail, curated archetypes, prose) from
    the COMPUTED SKELETONS (derived fields + provenance) and the still-indeterminate edges (into the UK,
    in transition)."""
    if not COMPUTED_CORRIDOR_SKELETONS:
        return {"error": "edge skeletons not present (run scripts/build_edge_skeletons.py then build.py)"}
    cov = COMPUTED_CORRIDOR_SKELETONS.get("coverage", {})
    return {**cov, "cross_check_clean": COMPUTED_CORRIDOR_SKELETONS.get("cross_check", {}).get("clean"),
            "note": ("rich corridors are the enriched gold tier; skeletons carry only derived fields, with "
                     "infrastructure_overlap and bespoke analysis left as a per-edge enrichment backlog.")}


@mcp.tool()
def corridor_skeleton(origin: str, destination: str) -> dict:
    """Return the corridor record for a directed edge: the hand-authored RICH record if one exists,
    otherwise the COMPUTED SKELETON (derived feasibility class, inbound mechanism test + administrator,
    baseline archetypes, directed interaction sets, and provenance). Skeletons introduce no new facts and
    leave empirical fields (infrastructure_overlap, bespoke detail) explicitly unset."""
    o, d = origin.upper(), destination.upper()
    if o not in JURISDICTIONS or d not in JURISDICTIONS:
        return {"error": f"unknown jurisdiction(s): {origin}/{destination}"}
    rich = next((c for c in CORRIDORS if c.get("origin") == o and c.get("destination") == d), None)
    if rich:
        return {"tier": "authored_rich", **rich}
    for s in COMPUTED_CORRIDOR_SKELETONS.get("skeletons", []):
        if s.get("origin") == o and s.get("destination") == d:
            return s
    return {"edge": f"{o}->{d}", "tier": "none",
            "note": "no record — edge is indeterminate at the substrate level (likely into the UK, in transition)"}


VERIFICATION_LEDGER = (DATA.get("analysis") or {}).get("verification_ledger", {})


@mcp.tool()
def verification_ledger(jurisdiction: Optional[str] = None) -> dict:
    """The external primary-source verification pass (v0.9.5) audit trail.

    Records, per cell, the binding status of the cited instrument, the official URL attached, and the
    tier the disposition applied. The pass's discipline is that citability is capped by binding status,
    NOT by whether the official text was located: resolution_text is applied only where binding_status is
    in_force_enacted AND the proposition was confirmed against official text; made_not_commenced (e.g. UK
    SI 2026/102), finalized_policy_pending (e.g. SG MAS SCS framework), and pending_proposal (e.g. US
    CLARITY/NPRM, BR BCB) cells receive the URL + binding_status but are held at firm_summary; prohibition
    cells (CN) stay unset. Filter by jurisdiction (e.g. 'EU', 'US', 'HK', 'UK', 'SG', 'CN', 'BR')."""
    if not VERIFICATION_LEDGER:
        return {"error": "verification ledger not present in dataset.json (run scripts/apply_verification.py then build.py)"}
    entries = VERIFICATION_LEDGER.get("entries", [])
    if jurisdiction:
        j = jurisdiction.upper()
        entries = [e for e in entries if e.get("jurisdiction") == j]
    from collections import Counter
    bs = Counter(e.get("binding_status") for e in entries)
    promoted = [e["cell"] for e in entries if e.get("applied_tier") == "resolution_text"]
    return {
        "performed_by": VERIFICATION_LEDGER.get("performed_by"),
        "discipline": VERIFICATION_LEDGER.get("discipline"),
        "filter": jurisdiction.upper() if jurisdiction else "all",
        "count": len(entries),
        "binding_status_breakdown": dict(bs),
        "promoted_to_resolution_text": promoted,
        "entries": entries,
    }


COMPUTED_CONVERGENCE: dict = ANALYSIS.get("computed_convergence", {})

# The lawyer-citable test, replicated so per-record "why not citable" can be answered inline.
_CITABLE_AXES = (
    ("claim_class", "tier1_legal", "not a proposition of law (tier1_legal)"),
    ("status", "in_force", "not currently in force"),
    ("evidence_tier", "resolution_text", "not confirmed against the official text (resolution_text)"),
)


def _citable_blocks(r: dict) -> list[list]:
    """Return the axes on which a record fails the tier1_legal + in_force + resolution_text test."""
    blocks = []
    for field, want, why in _CITABLE_AXES:
        if r.get(field) != want:
            blocks.append([field, r.get(field), why])
    return blocks


@mcp.tool()
def events_by_kind(kind: Optional[str] = None) -> dict:
    """
    The regulatory event calendar grouped by trigger_kind — the paper's typology of triggers by the
    KIND OF CERTAINTY each carries (flagship §3), not merely by date. This is the view that separates the
    one trigger kind that moves a dated feasibility horizon (fully-scheduled) from the kinds that do not
    (a dated change that alters accessibility within a live regime; a dated change with an explicitly
    empty class effect; a bill with no commencement date surfaced only as an if-enacted branch; a
    pending enactment that hardens a binding status without moving any class). Use it to answer "which of
    these changes actually moves a corridor's class, and which are dated-but-inert or contingent?"

    Returns the trigger_kind_legend (purpose, per-kind definitions, and the horizon rule), the events
    bucketed by trigger_kind, and a per-kind moves_a_horizon flag. Optional `kind` filter (e.g.
    'fully-scheduled', 'intra-regime-gating', 'dated-empty-effect', 'inbound-recognition',
    'contingent-no-date', 'enacted-not-commenced', 'contingent-not-class-change').
    """
    if not EVENT_CALENDAR:
        return {"error": "event calendar not present (run scripts/compose.py then build.py)"}
    legend = EVENT_CALENDAR.get("trigger_kind_legend", {})
    evs = EVENT_CALENDAR.get("events", [])
    if kind:
        evs = [e for e in evs if e.get("trigger_kind") == kind]
    buckets: dict[str, list] = {}
    for e in evs:
        tk = e.get("trigger_kind", "unclassified")
        buckets.setdefault(tk, []).append({
            "id": e.get("id"), "jurisdiction": e.get("jurisdiction"), "title": e.get("title"),
            "status": e.get("status"), "effective_date": e.get("effective_date"),
            "trigger": e.get("trigger"),
            # a change moves a horizon only if it is fully-scheduled AND carries a non-empty effect
            "moves_a_horizon": e.get("trigger_kind") == "fully-scheduled" and bool(e.get("effect")),
        })
    return {
        "as_of_base": EVENT_CALENDAR.get("as_of_base"),
        "filter": kind or "all",
        "count": len(evs),
        "by_kind": buckets,
        "horizon_rule": legend.get("horizon_rule"),
        "legend": legend,
        "note": ("Only fully-scheduled events with a non-empty effect move a compose() horizon. "
                 "dated-empty-effect, intra-regime-gating, and inbound-recognition events are dated "
                 "but move no feasibility class; contingent kinds have no date and are surfaced only "
                 "as if-enacted branches. This grouping asserts no new facts — trigger_kind is a field "
                 "on each event."),
    }


@mcp.tool()
def convergence(side: Optional[str] = None) -> dict:
    """
    The cross-jurisdiction yield-line convergence view (flagship §4.5): independent legislative systems
    converging on the same functional boundary around stablecoin yield — yield for merely HOLDING the
    instrument is prohibited, while ACTIVITY-LINKED rewards are permitted. This reshapes the existing
    per-jurisdiction permitted_activity_yield records into that cross-jurisdiction line; it asserts NO
    new facts (every field is copied from a record) and it respects the register's citable-purity
    discipline: the two-sided line is asserted at citable depth ONLY where a cell is
    tier1_legal + in_force + resolution_text AND both sides are documented (today: the US alone).

    Returns the finding, the discipline statement, and the jurisdictions tiered by role: the citable
    two-sided `anchor` (US), the `sibling` restriction (SG), the documented `counter_example` (CH, where
    holder yield is permitted-but-constrained), `holder_prohibition_in_force` (EU/HK/JP/AE — the
    prohibited side in force and citable, the permitted side carried as backlog), `draft_would_align`
    (KR/TW — would align if enacted), and `backlog_or_not_applicable`. Optional `side` filter, one of:
    'anchor', 'sibling', 'counter_example', 'holder_prohibition_in_force', 'draft_would_align',
    'backlog_or_not_applicable'.
    """
    if not COMPUTED_CONVERGENCE:
        return {"error": "convergence view not present (run scripts/build_convergence.py then build.py)"}
    c = COMPUTED_CONVERGENCE
    if side:
        block = c.get(side)
        if block is None:
            return {"error": f"unknown side {side!r}",
                    "valid_sides": ["anchor", "sibling", "counter_example",
                                    "holder_prohibition_in_force", "draft_would_align",
                                    "backlog_or_not_applicable"]}
        return {"dimension": c.get("dimension"), "side": side, "records": block,
                "discipline": c.get("discipline"), "provenance": c.get("provenance")}
    return {
        "dimension": c.get("dimension"),
        "finding": c.get("finding"),
        "discipline": c.get("discipline"),
        "method": c.get("method"),
        "anchor": c.get("anchor"),
        "sibling": c.get("sibling"),
        "counter_example": c.get("counter_example"),
        "holder_prohibition_in_force": c.get("holder_prohibition_in_force"),
        "draft_would_align": c.get("draft_would_align"),
        "backlog_or_not_applicable": c.get("backlog_or_not_applicable"),
        "summary_counts": c.get("summary_counts"),
        "provenance": c.get("provenance"),
    }


COMPUTED_FORWARD_VIEW: dict = ANALYSIS.get("computed_forward_view", {})


@mcp.tool()
def forward_view(jurisdiction: Optional[str] = None) -> dict:
    """
    The per-jurisdiction supervisor forward view (Atlas §4.4): the trigger register re-sorted BY
    JURISDICTION rather than by trigger, into the view a supervisory reader actually needs. For a
    jurisdiction it answers: which pending developments will change the corridors INTO and OUT OF my
    jurisdiction, and which counterpart jurisdictions am I most exposed to. Each jurisdiction carries its
    own pending events (flagged class-moving vs accessibility-only), the inbound and outbound directed
    edges that change feasibility class under the pending set (each attributed to the trigger causing it
    and split into own-trigger-driven vs counterpart-driven), the counterpart jurisdictions on the other
    end ranked by exposure, and a one-line supervisor_reading. It asserts NO new facts: every movement is
    read from the corridor-state precompute and every event from the event calendar.

    This is the view §4.4 calls the change that makes the forward map usable to supervisory readers: it
    turns "the EU is low-sensitivity" into the operational statement that the EU's own pending change
    (the MiCA 143(3) expiry) is accessibility-only and moves no class, while separately a set of the EU's
    corridors will reclassify when counterparts enact. Pass `jurisdiction` (e.g. 'EU', 'KR') for one
    jurisdiction; omit it for all twelve plus the reading key.
    """
    if not COMPUTED_FORWARD_VIEW:
        return {"error": "forward view not present (run scripts/build_forward_view.py then build.py)"}
    fv = COMPUTED_FORWARD_VIEW
    per = fv.get("jurisdictions", {})
    if jurisdiction:
        j = jurisdiction.upper()
        if j not in per:
            return {"error": f"unknown jurisdiction {jurisdiction!r}", "valid": sorted(per.keys())}
        return {"as_of_base": fv.get("as_of_base"), "jurisdiction": j,
                "forward": per[j], "reading_key": fv.get("reading_key"),
                "provenance": fv.get("provenance")}
    return {
        "as_of_base": fv.get("as_of_base"),
        "method": fv.get("method"),
        "reading_key": fv.get("reading_key"),
        "jurisdictions": per,
        "provenance": fv.get("provenance"),
    }


@mcp.tool()
def reconciliation(only_divergences: bool = False) -> dict:
    """
    The computed-vs-authored corridor reconciliation: for every undirected jurisdiction pair, the class
    the compose() engine derives from the signal table set against the class a human authored, with an
    agree/disagree flag and, where they differ, the named cause. This is the register auditing its own
    analysis layer — the divergences are not errors to hide but findings: today they are exactly the
    pairs where one side is a regime-in-transition (the UK), which the engine flags as Category T while
    the human authored the eventual steady-state class.

    Returns the agreement ratio, the pairs (each with computed_category, authored_category, agree,
    basis, finding), and findings_by_cause (the divergences grouped by their cause). Set
    `only_divergences=true` to return just the disagreeing pairs.
    """
    pairs = COMPUTED.get("undirected_pairs", {})
    rows = pairs.get("pairs", []) if isinstance(pairs, dict) else []
    if not rows:
        return {"error": "reconciliation not present (run scripts/compose.py then build.py)"}
    fbc = pairs.get("findings_by_cause") or COMPUTED.get("findings_by_cause", {})
    shown = [p for p in rows if not p.get("agree")] if only_divergences else rows
    return {
        "agreement": pairs.get("agreement"),
        "count_total": len(rows),
        "count_divergent": sum(1 for p in rows if not p.get("agree")),
        "filter": "divergences_only" if only_divergences else "all",
        "pairs": shown,
        "findings_by_cause": fbc,
        "note": ("A divergence is a finding, not a defect: the engine flags a regime-in-transition side "
                 "as Category T, while the authored class is the steady state. compose_corridor(as_of=…) "
                 "and corridor_timeline show how such a pair resolves over time."),
    }


@mcp.tool()
def records(
    claim_class: Optional[str] = None,
    evidence_tier: Optional[str] = None,
    status: Optional[str] = None,
    binding_status: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    dimension: Optional[str] = None,
    citable_only: bool = False,
) -> dict:
    """
    The evidence-axis record browser: filter the register along the axes that decide citability —
    claim_class (KIND: tier1_legal vs tier2_operational), evidence_tier (PROVENANCE: resolution_text /
    mixed / firm_summary / unset), status, and binding_status — and get, for every record, whether it is
    lawyer-citable and, if not, exactly which axis blocks it (the "why not citable" x-ray). This is the
    complement to query() (which filters by jurisdiction/dimension/status): use records() to reason about
    the two-axis evidence model and the verification frontier.

    Args (all optional, AND-combined):
        claim_class: 'tier1_legal' | 'tier2_operational'.
        evidence_tier: 'resolution_text' | 'mixed' | 'firm_summary' | 'unset'.
        status: 'in_force' | 'transitional' | 'proposed' | 'consultation'.
        binding_status: e.g. 'in_force_enacted' | 'made_not_commenced' | 'finalized_policy_pending' |
                        'pending_proposal' | 'prohibition'.
        jurisdiction: e.g. 'US'. dimension: one of the 15 dimension keys.
        citable_only: if true, return only records that pass tier1_legal + in_force + resolution_text.
    Returns a count, a breakdown by (claim_class × evidence_tier), and per-record summaries each carrying
    `citable` and `blocks` (the failing axes).
    """
    from collections import Counter
    j = jurisdiction.upper() if jurisdiction else None
    et = "unset"
    out, axis = [], Counter()
    for r in RECORDS:
        if j and r.get("jurisdiction") != j:
            continue
        if dimension and r.get("dimension") != dimension:
            continue
        if claim_class and r.get("claim_class") != claim_class:
            continue
        rt = r.get("evidence_tier") or "unset"
        if evidence_tier and rt != evidence_tier:
            continue
        if status and r.get("status") != status:
            continue
        if binding_status and r.get("binding_status") != binding_status:
            continue
        blocks = _citable_blocks(r)
        is_citable = not blocks
        if citable_only and not is_citable:
            continue
        s = _summary(r)
        s["citable"] = is_citable
        s["blocks"] = blocks
        out.append(s)
        axis[f"{r.get('claim_class')} × {rt}"] += 1
    return {
        "count": len(out),
        "citable_in_result": sum(1 for r in out if r["citable"]),
        "filters": {"claim_class": claim_class, "evidence_tier": evidence_tier, "status": status,
                    "binding_status": binding_status, "jurisdiction": j, "dimension": dimension,
                    "citable_only": citable_only},
        "by_claim_class_x_evidence_tier": dict(sorted(axis.items())),
        "records": out,
        "citable_filter": {"claim_class": "tier1_legal", "status": "in_force",
                           "evidence_tier": "resolution_text"},
        "note": ("`citable` = tier1_legal + in_force + resolution_text; `blocks` lists the axes a record "
                 "fails. Operational facts (tier2_operational) are excluded by kind even when "
                 "well-sourced; draft provisions by status; unverified legal points by tier."),
    }


def main() -> None:
    """Entry point for the `cbsr-mcp` console script and for `python mcp_server.py`."""
    mcp.run()


if __name__ == "__main__":
    main()
