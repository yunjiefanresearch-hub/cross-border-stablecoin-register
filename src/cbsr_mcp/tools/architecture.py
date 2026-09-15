"""Corridor, substrate and temporal architecture tools."""
from __future__ import annotations
from datetime import date
from typing import Optional
from ..core.catalog import JURISDICTIONS
from ..data.repository import DATA, RECORDS, record_summary
from .registry import tool
_summary = record_summary

ANALYSIS: dict = DATA.get("analysis", {})


@tool
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


@tool
def interaction_sets() -> dict:
    """
    The six constraint-interaction sets (A-F) from Architecture §2.9 — the constraint pairs
    through which joint binding generates composition problems, each with its mechanism and a
    worked example. These are referenced per pair by compatibility().
    """
    return ANALYSIS.get("interaction_sets") or {"error": "analysis layer not present"}


@tool
def architectural_patterns() -> dict:
    """
    The Architecture paper's architectural patterns: the PRC three-pattern typology (§3.3 —
    direct subsidiary licensing / partnership distribution / separated-entity), the portable
    three-layer routing architecture (§4/§6 — Layer 1 compliant issuer, Layer 2 user-directed
    routing, Layer 3 yield-bearing fund), the §4.4 five-factor operational test, and the six
    design principles.
    """
    return ANALYSIS.get("architectural_patterns") or {"error": "analysis layer not present"}


@tool
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
LEGAL_EVENT_ONTOLOGY: dict = ANALYSIS.get("legal_event_ontology", {})
COMPUTED_TIMELINE: dict = ANALYSIS.get("computed_timeline", {})
SUBSTRATE: dict = ANALYSIS.get("constraint_substrate", {})
COMPUTED_SUBSTRATE: dict = ANALYSIS.get("computed_substrate", {})
VERIFICATION_WORKLIST: dict = ANALYSIS.get("verification_worklist", {})
STAKEHOLDER_DB: dict = ANALYSIS.get("stakeholder_database", {})
COMPUTED_STAKEHOLDER_PROFILES: dict = ANALYSIS.get("computed_stakeholder_profiles", {})
COMPUTED_CORRIDOR_SKELETONS: dict = ANALYSIS.get("computed_corridor_skeletons", {})
COMPUTED_CORRIDORS_DIRECTED: dict = ANALYSIS.get("computed_corridors_directed", {})
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


@tool
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
    if as_of is not None:
        try:
            parsed_as_of = date.fromisoformat(as_of)
        except (TypeError, ValueError):
            return {"error": "as_of must be an ISO date (YYYY-MM-DD)"}
        if parsed_as_of.isoformat() != as_of:
            return {"error": "as_of must be an ISO date (YYYY-MM-DD)"}
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
           "note": "computed layer is a preview (Atlas §3.2 rule); not asserted authoritative — see findings_by_cause. The preview reads the inbound gate's TYPE, so where a destination regime is enacted-but-not-commenced it returns the RESOLVED class (e.g. II), not the in-transition class (T). For the published timing-aware reading, call corridor_directed().",
           "authoritative_reading": "corridor_directed"}
    if as_of:
        base_res = _compose_directed(o, d)
        out["base_class"] = base_res.get("class")
        out["changed_from_base"] = base_res.get("class") != res["class"]
    return out


@tool
def corridor_directed(origin: str, destination: str) -> dict:
    """
    The PUBLISHED, timing-aware directed reading of a corridor — the same reading as the register's
    corridor map, /api/corridors_directed/ and the landing page. Returns the directed feasibility class
    and its class_code, the dated as_of_timeline (today's class plus each scheduled resolution and its
    date_kind), and the class_basis (rule, governing jurisdiction, signal, instrument, binding_status,
    evidence_tier) the class rests on.

    PREFER THIS over compose_corridor() for "what does this corridor read today". compose_corridor()
    exposes the Atlas s.3.2 PREVIEW, which reads the inbound gate's TYPE: where a destination regime is
    enacted-but-not-commenced it returns the RESOLVED class (e.g. II) rather than the in-transition
    class (T). This tool asserts no new facts — every field is read from the published directed layer.
    """
    o, d = origin.upper(), destination.upper()
    if o not in JURISDICTIONS or d not in JURISDICTIONS:
        return {"error": f"unknown jurisdiction(s): {origin}/{destination}"}
    edges = COMPUTED_CORRIDORS_DIRECTED.get("edges", [])
    if not edges:
        return {"error": "directed layer not present (run scripts/build_corridors_directed.py, then build.py)"}
    e = next((x for x in edges if x.get("origin") == o and x.get("destination") == d), None)
    if e is None:
        return {"error": f"no directed edge {o}->{d}", "edges_available": len(edges)}
    return {"edge": f"{o}->{d}",
            "class_code": e.get("class_code"),
            "feasibility_class": e.get("feasibility_class"),
            "as_of_timeline": e.get("as_of_timeline"),
            "class_basis": e.get("class_basis"),
            "origin_drag": e.get("origin_drag"),
            "inbound_mechanism": e.get("inbound_mechanism"),
            "evidence_tier": e.get("evidence_tier"),
            "divergence": e.get("divergence"),
            "corridor_id": e.get("corridor_id"),
            "provenance": e.get("materialized_from") or e.get("authored_source_file"),
            "source": e.get("source"),
            "valid_as_of": e.get("valid_as_of"),
            "note": "Published directed layer (timing-aware). compose_corridor() returns the Atlas s.3.2 "
                    "preview and may differ where a destination regime is made_not_commenced."}


@tool
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


@tool
def verification_report() -> dict:
    """
    The verification queue: which records are confirmed against official primary text and which are
    still pending. Buckets records by evidence_tier (resolution_text / mixed / firm_summary / unverified),
    flags the explicit unverified backlog, and lists
    records that lack a source.url. The view a maintainer uses to drive the next verification pass.
    """
    from collections import defaultdict
    buckets = defaultdict(list)
    no_url = []
    for r in RECORDS:
        tier = r.get("evidence_tier", "unverified")
        buckets[tier].append(r["id"])
        if not (r.get("source") or {}).get("url"):
            no_url.append(r["id"])
    legacy = sorted(r["id"] for r in RECORDS if r.get("evidence_tier") == "unverified")
    return {
        "totals": {k: len(v) for k, v in sorted(buckets.items())},
        "records_with_source_url": len(RECORDS) - len(no_url),
        "records_total": len(RECORDS),
        "backlog_unverified": {"count": len(legacy), "ids": legacy,
                                "note": "no earned evidence tier is asserted; official-source review remains open"},
        "pending_no_url": {"count": len(no_url), "ids": sorted(no_url)},
        "by_tier": {k: sorted(v) for k, v in sorted(buckets.items())},
        "legend": {"resolution_text": "confirmed against official primary text",
                   "mixed": "core point confirmed; some operational detail pending",
                   "firm_summary": "practitioner-corroborated, pending official-text check",
                   "unverified": "no earned evidence tier is committed"},
    }


@tool
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


@tool
def citable_law(jurisdiction: Optional[str] = None,
                dimension: Optional[str] = None) -> dict:
    """
    Decision-ready citable law: structural legal candidates with official, current, independently reconciled evidence.

    All six gates must pass: claim_class=tier1_legal, status=in_force,
    evidence_tier=resolution_text, source_disposition=official,
    freshness.review_status=current, and review_stage=reconciled. Each record also
    carries its source URL and pinpoint. Freshness is assessed at the dataset's dated
    snapshot, not at the time this offline tool is called.

    This returns `decision_ready_citable_subset` from dataset.json. The legacy
    `citable_subset` contains structural candidates only; its separate count never
    promotes a candidate through the freshness or independent-review gates.

    Optional filters narrow to a jurisdiction (e.g. 'CH') and/or a dimension (e.g. 'reserve_backing').
    """
    j = jurisdiction.upper() if jurisdiction else None
    sub = DATA.get("decision_ready_citable_subset", {})
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
        "structural_candidate_count": DATA.get("citable_subset", {}).get("count", 0),
        "note": ("Decision-ready citable law additionally requires current evidence and an "
                 "independently reconciled second review. Structural candidates remain visible "
                 "separately and are not promoted by this tool."),
    }


@tool
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
    ontology_rows = LEGAL_EVENT_ONTOLOGY.get("records", [])
    if jurisdiction:
        j = jurisdiction.upper()
        evs = [e for e in evs if e.get("jurisdiction") == j]
        ontology_rows = [row for row in ontology_rows if row.get("jurisdiction") == j]
    return {"as_of_base": EVENT_CALENDAR.get("as_of_base"), "count": len(evs), "events": evs,
            "status_values": EVENT_CALENDAR.get("status_values"),
            "ontology": {
                "schema": LEGAL_EVENT_ONTOLOGY.get("schema"),
                "allowed_transitions": LEGAL_EVENT_ONTOLOGY.get("allowed_transitions", {}),
                "coverage": LEGAL_EVENT_ONTOLOGY.get("coverage", {}),
                "records": ontology_rows,
                "limitations": LEGAL_EVENT_ONTOLOGY.get("limitations"),
            },
            "provenance": COMPUTED_TIMELINE.get("event_provenance", {})}


@tool
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
            "next_scheduled_change": next((t for t in transitions if t["changed"]), None),
            "authoritative_reading": "corridor_directed",
            "note": "today_class and the transitions here are computed from the compose() signal table "
                    "and the event calendar. Where a destination regime is enacted-but-not-commenced the "
                    "preview may already report the resolved class, leaving no scheduled change to show; "
                    "corridor_directed() carries the published as_of_timeline for that edge."}


def _sub_cell(j, c):
    return SUBSTRATE.get("cells", {}).get(j, {}).get(c)


def _sub_attr(cell, key, default=None):
    return (cell or {}).get("attributes", {}).get(key, default)


@tool
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


@tool
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
