"""Core register discovery and query tools."""
from __future__ import annotations
from typing import Optional
from ..core.catalog import DIMENSIONS, JURISDICTIONS
from ..data.repository import DATA, RECORDS, CORRIDORS, record_summary
from .registry import count as tool_count, tool
ANALYSIS = DATA.get("analysis", {})
EVENT_CALENDAR = ANALYSIS.get("event_calendar", {})
COMPUTED_SUBSTRATE = ANALYSIS.get("computed_substrate", {})
_summary = record_summary


@tool
def about() -> dict:
    """Register metadata: name, version, record count, license, DOI, and the verification rule."""
    return {
        "name": DATA.get("name"),
        "version": DATA.get("version"),
        "generated": DATA.get("generated"),
        "record_count": DATA.get("record_count"),
        "corridor_count": len(CORRIDORS),
        "citable_count": DATA.get("decision_ready_citable_subset", {}).get("count", 0),
        "structural_citable_candidates": DATA.get("citable_subset", {}).get("count", 0),
        "doi": "10.5281/zenodo.20730358",
        "license": {"data": "CC-BY-4.0", "code": "Apache-2.0"},
        "spines": ["permitted_activity_yield", "securities_classification"],
        "evidence_model": {
            "axes": {
                "claim_class": "kind of claim — tier1_legal (proposition of law) vs tier2_operational (market/operational fact)",
                "evidence_tier": "provenance strength — resolution_text vs mixed vs firm_summary vs unverified",
                "status": "force — in_force vs transitional/proposed/consultation",
                "binding_status": "binding status of the cited instrument — in_force_enacted vs made_not_commenced / finalized_policy_pending / pending_proposal / prohibition / no_regime; caps citability (resolution_text requires in_force_enacted)",
                "source_disposition": "source availability/type — official, secondary, unavailable or not_applicable",
                "legal_status": "separate temporal legal state; never inferred as source disposition",
            },
            "citable_subset": "tier1_legal + in_force + resolution_text + official + current + independently reconciled",
        },
        "temporal": {
            "date_aware_compose": "compose_corridor(origin, destination, as_of=ISO_DATE) evaluates as of a date",
            "event_calendar": f"{len(EVENT_CALENDAR.get('events', []))} dated/contingent tier1_legal events — see event_calendar() and corridor_timeline()",
        },
        "substrate": {
            "constraint_substrate": f"{COMPUTED_SUBSTRATE.get('coverage', {}).get('cells_populated', 0)}/96 C1-C8 poles populated — see constraint_substrate()",
            "deep_compose": "compose_via_substrate(origin, destination) derives feasibility through the interaction-set rules; indeterminate where poles are unset",
        },
        "tool_count": tool_count(),
        "review_coverage": DATA.get("review_coverage", {}),
        "verification_rule": (
            "A record is verified only when it has no open markers AND a human has checked "
            "every source.primary and pinpoint against the instrument itself. Citations are "
            "never machine-generated. Some records are transcribed from the maintainer's "
            "Compliance Matrix and pending final primary-source verification (source.url empty)."
        ),
    }


@tool
def list_jurisdictions() -> list[dict]:
    """List jurisdictions covered, with full name and record count."""
    counts: dict[str, int] = {}
    for r in RECORDS:
        counts[r["jurisdiction"]] = counts.get(r["jurisdiction"], 0) + 1
    return [
        {"code": code, "name": JURISDICTIONS.get(code, code), "records": counts.get(code, 0)}
        for code in sorted(counts, key=lambda c: -counts[c])
    ]


@tool
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


@tool
def get_record(record_id: str) -> dict:
    """Return the full record (all fields including requirement_structured and interpretation_note) by its id."""
    for r in RECORDS:
        if r.get("id") == record_id:
            return r
    return {"error": f"No record with id '{record_id}'.",
            "hint": "Use query() or search() to find record ids."}


@tool
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


@tool
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


@tool
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


@tool
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


@tool
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


@tool
def coverage() -> dict:
    """
    Coverage matrix: for each jurisdiction × dimension, whether a record exists ('verified')
    or not ('planned'). Useful for an agent to know where data is and is not available.
    """
    present = {(r["jurisdiction"], r["dimension"]) for r in RECORDS}
    jur = sorted({r["jurisdiction"] for r in RECORDS})
    grid = {}
    for jcode in jur:
        grid[jcode] = {dim: ("recorded" if (jcode, dim) in present else "planned")
                       for dim in DIMENSIONS}
    review_grid = {}
    for jcode in jur:
        review_grid[jcode] = {}
        for dim in DIMENSIONS:
            rows = [r for r in RECORDS if r["jurisdiction"] == jcode and r["dimension"] == dim]
            if not rows:
                review_grid[jcode][dim] = "not_recorded"
            elif any(r.get("review_stage") == "reconciled" and
                     (r.get("freshness") or {}).get("review_status") == "current" for r in rows):
                review_grid[jcode][dim] = "current_reconciled"
            elif any((r.get("freshness") or {}).get("review_status") == "stale" for r in rows):
                review_grid[jcode][dim] = "stale"
            else:
                review_grid[jcode][dim] = "review_incomplete"
    return {"jurisdictions": jur, "dimensions": list(DIMENSIONS.keys()),
            "recorded_cells": len(present), "inventory_grid": grid, "review_grid": review_grid,
            "note": "record presence is not legal verification; review_grid is the decision-use gate"}
