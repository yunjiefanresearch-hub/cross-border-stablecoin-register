#!/usr/bin/env python3
"""build_forward_view.py — the per-jurisdiction supervisor forward view (Atlas §4.4).

The sensitivity layer (build_sensitivity.py) re-sorts the trigger register BY TRIGGER: "which corridors
does each pending change in law move." A supervisor asks the mirror question, organized BY JURISDICTION:
"which pending developments will change the corridors INTO and OUT OF my jurisdiction, and which
counterpart jurisdictions am I most exposed to." §4.4 of the forward-feasibility paper calls this the
single change that would make the forward map directly usable by the supervisory readership, and notes it
requires no new data, only the re-sort the register already supports.

This builder produces exactly that re-sort. For each of the twelve jurisdictions X it emits:
  - own_pending_events   : the events acting IN X (from the event calendar), each flagged for whether it
                           moves any feasibility class or only changes accessibility within a live regime;
  - inbound_reclassified : directed edges terminating in X that change class under the pending set,
                           each with the counterpart origin, the from/to class, and the trigger causing it;
  - outbound_reclassified: directed edges originating in X that change class, same detail;
  - counterpart_exposure : the counterpart jurisdictions on the other end of X's reclassified edges,
                           ranked by how many of X's edges they are involved in;
  - supervisor_reading   : the operationally useful one-line statement §4.4 asks for (and, for a
                           jurisdiction whose only pending change is an intra-regime gating one, the
                           explicit "no class flip pending, but accessibility changes" reading §4.4/§6 want).

It asserts NO new facts: every movement is read from analysis/computed_corridor_states.json (itself a
re-derivation of the signal compose()) and every event from analysis/event_calendar.json. Run after
scripts/build_corridor_states.py and before build_api.py:

    python scripts/build_corridor_states.py && python scripts/build_forward_view.py
"""
from __future__ import annotations
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any locale.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES = json.loads((ROOT / "analysis" / "computed_corridor_states.json").read_text(encoding="utf-8"))
CAL = json.loads((ROOT / "analysis" / "event_calendar.json").read_text(encoding="utf-8"))

J12 = STATES["jurisdictions"]
BASE = STATES.get("as_of_base")

# trigger kinds that change WHO/WHAT can reach the market inside an unchanged class (accessibility),
# as opposed to moving a corridor between classes. §3.10 / §6.
_GATING_KINDS = {"intra-regime-gating", "dated-empty-effect", "inbound-recognition",
                 "contingent-not-class-change", "parameterization"}


def _movements():
    """Yield (corridor 'O->D', from, to, trigger_id, trigger_jurisdiction, timing) for every pending
    class movement, whether dated (a non-base date_state's changes_vs_base) or contingent (a what-if
    branch's class_movements). Dated movements are attributed to the active event whose effective_date
    equals the date_state's as_of (the change that caused them)."""
    out = []
    # (1) dated changes — attributed to the event commencing on that date
    for st in STATES.get("date_states", []):
        if st.get("is_base"):
            continue
        as_of = st.get("as_of")
        causing = [e for e in st.get("active_events", []) if e.get("effective_date") == as_of]
        for m in st.get("changes_vs_base", []):
            for ev in (causing or [{"event_id": None, "trigger_kind": None}]):
                out.append((m["corridor"], m.get("from"), m.get("to"),
                            ev.get("event_id"), _event_jur(ev.get("event_id")),
                            f"scheduled {as_of}"))
    # (2) contingent branches — the "if enacted" reclassifications
    for w in STATES.get("whatif_branches", []):
        for m in w.get("class_movements", []):
            out.append((m["corridor"], m.get("from"), m.get("to"),
                        w.get("trigger_id"), w.get("jurisdiction"), "contingent (if enacted)"))
    return out


_EVENT_BY_ID = {e["id"]: e for e in CAL.get("events", [])}


def _event_jur(eid):
    return (_EVENT_BY_ID.get(eid) or {}).get("jurisdiction")


def _event_moves_class(eid):
    """True iff this event id appears as the cause of at least one class movement."""
    for _c, _f, _t, tid, _j, _timing in _MOVES:
        if tid == eid:
            return True
    return False


_MOVES = None


def build():
    global _MOVES
    _MOVES = _movements()

    per = {}
    for X in J12:
        own = []
        for e in CAL.get("events", []):
            if e.get("jurisdiction") != X:
                continue
            moves = _event_moves_class(e["id"])
            own.append({
                "event_id": e["id"],
                "title": e.get("title"),
                "trigger_kind": e.get("trigger_kind"),
                "status": e.get("status"),
                "effective_date": e.get("effective_date"),
                "moves_class": moves,
                "accessibility_only": (not moves) and e.get("trigger_kind") in _GATING_KINDS,
            })

        inbound, outbound = [], []
        for corridor, frm, to, tid, tjur, timing in _MOVES:
            o, _, d = corridor.partition("->")
            if d == X:
                inbound.append({"counterpart": o, "from": frm, "to": to,
                                "via_trigger": tid, "trigger_jurisdiction": tjur, "timing": timing})
            elif o == X:
                outbound.append({"counterpart": d, "from": frm, "to": to,
                                 "via_trigger": tid, "trigger_jurisdiction": tjur, "timing": timing})

        # counterpart exposure: rank the other ends of X's reclassified edges
        exposure = {}
        for e in inbound:
            exposure.setdefault(e["counterpart"], {"inbound": 0, "outbound": 0})["inbound"] += 1
        for e in outbound:
            exposure.setdefault(e["counterpart"], {"inbound": 0, "outbound": 0})["outbound"] += 1
        exposure_ranked = sorted(
            ({"counterpart": k, "edges_affected": v["inbound"] + v["outbound"],
              "inbound": v["inbound"], "outbound": v["outbound"]} for k, v in exposure.items()),
            key=lambda r: (-r["edges_affected"], r["counterpart"]))

        per[X] = {
            "jurisdiction": X,
            "own_pending_events": own,
            "summary": {
                "own_driven_inbound": sum(1 for e in inbound if e["trigger_jurisdiction"] == X),
                "own_driven_outbound": sum(1 for e in outbound if e["trigger_jurisdiction"] == X),
                "counterpart_driven_inbound": sum(1 for e in inbound if e["trigger_jurisdiction"] != X),
                "counterpart_driven_outbound": sum(1 for e in outbound if e["trigger_jurisdiction"] != X),
                "accessibility_only_own_events": sum(1 for e in own if e["accessibility_only"]),
            },
            "inbound_reclassified": sorted(inbound, key=lambda r: (r["counterpart"], r["via_trigger"] or "")),
            "outbound_reclassified": sorted(outbound, key=lambda r: (r["counterpart"], r["via_trigger"] or "")),
            "counterpart_exposure": exposure_ranked,
            "supervisor_reading": _reading(X, own, inbound, outbound, exposure_ranked),
        }

    obj = {
        "schema": "cbsr-analysis/computed_forward_view",
        "version": CAL.get("version", STATES.get("version")),
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of_base": BASE,
        "method": ("Per-jurisdiction re-sort of the trigger register (Atlas §4.4). For each jurisdiction it "
                   "lists its own pending events (flagged class-moving vs accessibility-only), the inbound and "
                   "outbound directed edges that change feasibility class under the pending set (each attributed "
                   "to the trigger causing it), and the counterpart jurisdictions on the other end ranked by "
                   "exposure. Movements are read from computed_corridor_states.json; events from the event "
                   "calendar. No new facts are asserted."),
        "reading_key": {
            "class_moving": "an inbound/outbound edge that changes feasibility class under a pending trigger",
            "accessibility_only": ("a pending event in this jurisdiction that changes who may operate or which "
                                   "tokens are admissible WITHIN a live regime, without moving any class "
                                   "(intra-regime gating, a control case, a recognition pathway, or an in-force "
                                   "parameterization) — §3.10/§6: a low class-sensitivity position must be read as "
                                   "'no class flip pending', not 'nothing happening'"),
        },
        "provenance": {
            "asserts_new_facts": False,
            "derived_from": ["analysis/computed_corridor_states.json", "analysis/event_calendar.json"],
        },
        "jurisdictions": per,
    }
    (ROOT / "analysis" / "computed_forward_view.json").write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return obj


def _reading(X, own, inbound, outbound, exposure):
    # split X's reclassified edges by WHAT causes them: X's own pending trigger vs a counterpart's.
    own_in = [e for e in inbound if e["trigger_jurisdiction"] == X]
    own_out = [e for e in outbound if e["trigger_jurisdiction"] == X]
    cp_in = [e for e in inbound if e["trigger_jurisdiction"] != X]
    cp_out = [e for e in outbound if e["trigger_jurisdiction"] != X]
    own_gating = [e for e in own if e["accessibility_only"]]
    cp_exposure = sorted(
        ({"counterpart": c, "n": sum(1 for e in cp_in + cp_out if e["counterpart"] == c)}
         for c in {e["counterpart"] for e in cp_in + cp_out}),
        key=lambda r: (-r["n"], r["counterpart"]))

    parts = []
    # (a) X's OWN pending trigger
    if own_in or own_out:
        parts.append(f"{X}'s own pending trigger reclassifies {len(own_in)} inbound and {len(own_out)} "
                     f"outbound corridor(s) (a both-directions change at a pre-regime origin)."
                     if (own_in and own_out) else
                     f"{X}'s own pending trigger reclassifies {len(own_in)} inbound and {len(own_out)} "
                     f"outbound corridor(s).")
    elif own_gating:
        kinds = ", ".join(sorted({e["trigger_kind"] for e in own_gating}))
        parts.append(f"{X}'s own pending change is accessibility-only ({kinds}): it changes who may operate "
                     f"and which tokens are admissible within the live regime, without moving any feasibility "
                     f"class. Read {X}'s low class-sensitivity position as 'no class flip pending', not as "
                     f"'nothing happening' (§3.10/§6).")
    else:
        parts.append(f"{X} has no class-moving or accessibility-changing pending event of its own.")

    # (b) counterpart-driven changes to X's corridors
    if cp_in or cp_out:
        top = ", ".join(f"{r['counterpart']} ({r['n']})" for r in cp_exposure[:3])
        parts.append(f"Separately, {len(cp_in)} inbound and {len(cp_out)} outbound corridor(s) of {X} will "
                     f"reclassify when counterparts enact; most exposed counterpart(s): {top}.")
    elif not (own_in or own_out):
        parts.append("No counterpart's pending trigger reclassifies any corridor touching " + X + ".")
    return " ".join(parts)


if __name__ == "__main__":
    o = build()
    per = o["jurisdictions"]
    print("wrote analysis/computed_forward_view.json")
    print(f"  jurisdictions: {len(per)} | asserts_new_facts={o['provenance']['asserts_new_facts']}")
    for X in ("KR", "EU", "US", "TW"):
        v = per[X]
        print(f"  {X}: in={len(v['inbound_reclassified'])} out={len(v['outbound_reclassified'])} "
              f"own_events={len(v['own_pending_events'])} "
              f"top_counterpart={(v['counterpart_exposure'][0]['counterpart'] if v['counterpart_exposure'] else '-')}")
    print("  EU reading:", per["EU"]["supervisor_reading"][:160])
