#!/usr/bin/env python3
"""Precompute the budgeted corridor-state JSON that the interactive pages consume.

This is a *surfacing* product, not a new analysis. It re-runs the SAME date-aware
compose() the register already ships (scripts/compose.py, mirrored by the MCP
compose_corridor(as_of=...) tool) over a fixed set of key dates and over each
contingent trigger's if-enacted branch, and freezes the results as static JSON so
GitHub Pages can serve the time-slider / what-if browser with zero backend.

Guardrails honoured (Atlas / methodology paper):
  * All output is static JSON — no server, no database.
  * The dated axis applies ONLY the register's own scheduled/in_force events
    (signals_as_of); it never extrapolates or attaches probabilities.
  * The what-if axis applies ONLY the register's own contingent if-then branches,
    each labelled "if-enacted"; it is conditioning, never forecasting. A branch that
    the register's rules leave class-unchanged (e.g. CLARITY, SG enactment — they
    move within-cell fields, not feasibility signals) is reported as class-unchanged,
    not massaged into a movement.
  * asserts_new_facts = false: every cell is a re-derivation of existing tier1_legal
    signals; no proposition of law is added here.

Run after build.py (needs event_calendar.json):  python3 scripts/build_corridor_states.py
"""

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, pathlib, datetime, importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Import the register's own compose engine so this precompute is byte-for-byte the
# same derivation as the shipped MCP tool — never a re-implementation.
_spec = importlib.util.spec_from_file_location("cbsr_compose", ROOT / "scripts" / "compose.py")
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

J12 = C.J12
BASE_DATE = "2026-06-30"          # the register's as_of_base (Atlas time engine): the 30 Jun 2026 dateline
SIGNAL_FIELDS = {"regime_status", "inbound_gate", "exportable_token", "egress_override"}


def _events():
    events, meta = C.load_events()
    return events, meta


def _matrix(signals):
    """Full 12x12 directed matrix + 66-pair undirected reduction under one signal state."""
    directed = {}
    for o in J12:
        row = {}
        for d in J12:
            if o == d:
                row[d] = None
                continue
            r = C.compose_directed(o, d, signals)
            row[d] = {"class": r["class"], "rule": r["rule"], "origin_override": r.get("origin_override", False)}
        directed[o] = row
    undirected = {}
    caveated = 0
    for i, o in enumerate(J12):
        for d in J12[i + 1:]:
            cat, why = C.reduce_undirected(o, d, signals)
            undirected[f"{o}-{d}"] = {"category": cat, "why": why}
            if "*" in cat:          # I/II* == one side is a regime-in-transition (T)
                caveated += 1
    return directed, undirected, caveated


def _diff(base_directed, new_directed):
    """Which ordered corridors changed class between two matrices."""
    out = []
    for o in J12:
        for d in J12:
            if o == d:
                continue
            b = base_directed[o][d]["class"]
            n = new_directed[o][d]["class"]
            if b != n:
                out.append({"corridor": f"{o}->{d}", "from": b, "to": n})
    return out


def build():
    events, meta = _events()

    # ---- dated axis: base + every scheduled/in_force effective_date ----------
    dated = sorted({e["effective_date"] for e in events
                    if e.get("status") in ("scheduled", "in_force") and e.get("effective_date")})
    key_dates = sorted(set([BASE_DATE] + dated))

    # base matrix (nothing applied beyond today's live law)
    base_signals = C.signals_as_of(BASE_DATE, events)
    base_directed, _, _ = _matrix(base_signals)

    date_states = []
    for dt in key_dates:
        S = C.signals_as_of(dt, events)
        directed, undirected, caveated = _matrix(S)
        # which dated events are active (effective) as of this date, and which of them actually move a class
        active_events = []
        for e in events:
            if e.get("status") in ("scheduled", "in_force") and e.get("effective_date") and e["effective_date"] <= dt:
                moves = bool(e.get("effect")) and any(eff.get("field") in SIGNAL_FIELDS for eff in e.get("effect", []))
                active_events.append({"event_id": e["id"], "title": e.get("title"),
                                      "effective_date": e["effective_date"],
                                      "trigger_kind": e.get("trigger_kind"),
                                      "moves_a_class": moves})
        date_states.append({
            "as_of": dt,
            "is_base": dt == BASE_DATE,
            "directed": directed,
            "undirected": undirected,
            "transition_caveated_pairs": caveated,
            "active_events": active_events,
            "changes_vs_base": _diff(base_directed, directed),
        })

    # ---- what-if axis: each contingent trigger as an isolated if-enacted branch ----
    import copy
    whatif = []
    for e in events:
        if e.get("status") != "contingent":
            continue
        hyp = copy.deepcopy(C.SIGNALS)
        touches_signal = False
        for eff in e.get("effect", []):
            fld = eff.get("field")
            if e["jurisdiction"] in hyp and fld in SIGNAL_FIELDS:
                hyp[e["jurisdiction"]][fld] = eff.get("to")
                touches_signal = True
        directed, undirected, caveated = _matrix(hyp)
        changed = _diff(base_directed, directed)
        whatif.append({
            "trigger_id": e["id"],
            "title": e.get("title"),
            "jurisdiction": e.get("jurisdiction"),
            "trigger_kind": e.get("trigger_kind"),
            "trigger_condition": e.get("trigger"),
            "basis": e.get("basis"),
            # honest register logic: a branch may leave every class unchanged
            "changes_any_class": bool(changed),
            "class_movements": changed,
            "note": ("This trigger's register-recorded effects move a feasibility signal; "
                     "the corridors below re-derive accordingly."
                     if touches_signal else
                     "The register records this trigger's effects on within-cell fields "
                     "(binding_status / status / labels), NOT on a feasibility signal — so the "
                     "register's own rules leave every corridor class unchanged. Shown as-is "
                     "(conditioning, not forecasting)."),
            "directed": directed,
            "undirected": undirected,
            "transition_caveated_pairs": caveated,
        })

    trigger_kind_legend = meta.get("trigger_kind_legend", {})

    # ---- engine payload: lets any client replicate compose_directed() exactly ----
    # (so the interactive page runs the register's OWN algorithm over its OWN signals
    #  for every date x toggle combination — never a re-implementation, never frozen
    #  deltas that would compose incorrectly when two movers touch one corridor.)
    dated_payload = [{
        "id": e["id"], "jurisdiction": e["jurisdiction"], "title": e.get("title"),
        "effective_date": e["effective_date"], "trigger_kind": e.get("trigger_kind"),
        "effects": [{"field": eff.get("field"), "to": eff.get("to")}
                    for eff in e.get("effect", []) if eff.get("field") in SIGNAL_FIELDS],
        "moves_a_class": bool(e.get("effect")) and any(eff.get("field") in SIGNAL_FIELDS for eff in e.get("effect", [])),
    } for e in events if e.get("status") in ("scheduled", "in_force") and e.get("effective_date")]
    contingent_payload = [{
        "id": e["id"], "jurisdiction": e["jurisdiction"], "title": e.get("title"),
        "trigger_kind": e.get("trigger_kind"), "trigger": e.get("trigger"), "basis": e.get("basis"),
        "effects": [{"field": eff.get("field"), "to": eff.get("to")}
                    for eff in e.get("effect", []) if eff.get("field") in SIGNAL_FIELDS],
        "recorded_effects_all": [eff.get("field") for eff in e.get("effect", [])],
        "touches_signal": any(eff.get("field") in SIGNAL_FIELDS for eff in e.get("effect", [])),
    } for e in events if e.get("status") == "contingent"]
    engine = {
        "algorithm": "Atlas §3.2: origin-drag first (a non-exportable origin -> Category III), else the "
                     "destination's inbound-gate class. Identical to scripts/compose.py compose_directed().",
        "signal_fields": sorted(SIGNAL_FIELDS),
        "gate_class": C.GATE_CLASS,
        "signals_base": {j: {"regime_status": C.SIGNALS[j]["regime_status"],
                             "inbound_gate": C.SIGNALS[j]["inbound_gate"],
                             "exportable_token": C.SIGNALS[j]["exportable_token"],
                             "egress_override": C.SIGNALS[j]["egress_override"],
                             "basis": C.SIGNALS[j]["basis"]} for j in J12},
        "dated_events": dated_payload,
        "contingent_triggers": contingent_payload,
    }


    out = {
        "schema": "cbsr-analysis/computed_corridor_states",
        "version": meta.get("version", ""),
        "generated": str(datetime.date.today()),
        "as_of_base": BASE_DATE,
        "jurisdictions": J12,
        "provenance": {
            "asserts_new_facts": False,
            "derivation": ("Re-runs the register's own compose() (scripts/compose.py; "
                           "MCP compose_corridor(as_of=...)) over the key dates and over each "
                           "contingent trigger's if-enacted branch. Every class is a re-derivation "
                           "of existing tier1_legal signals; no new proposition of law is asserted."),
            "dated_axis": ("signals_as_of(date): applies every scheduled/in_force event with "
                           "effective_date <= date, then re-runs the Atlas algorithm. No probabilities."),
            "whatif_axis": ("Each contingent trigger applied in isolation to today's base as an "
                            "if-enacted branch. Labelled conditioning, never forecasting."),
            "source": "analysis/event_calendar.json + scripts/compose.py",
        },
        "trigger_kind_legend": trigger_kind_legend,
        "engine": engine,
        "key_dates": key_dates,
        "date_states": date_states,
        "whatif_branches": whatif,
    }
    dest = ROOT / "analysis" / "computed_corridor_states.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    movers = [d["as_of"] for d in date_states if d["changes_vs_base"]]
    wi_movers = [w["trigger_id"] for w in whatif if w["changes_any_class"]]
    print(f"wrote {dest.relative_to(ROOT)}")
    print(f"  key dates: {len(key_dates)}  ({', '.join(key_dates)})")
    print(f"  dated states that move >=1 corridor vs base: {movers or 'none'}")
    print(f"  contingent branches: {len(whatif)}  (move >=1 class: {wi_movers or 'none'})")
    return out


if __name__ == "__main__":
    build()
