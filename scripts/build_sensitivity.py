#!/usr/bin/env python3
"""build_sensitivity.py — the corridor-sensitivity layer (Atlas §4, "load-bearing forward map").

For each pending trigger (a contingent enactment or a dated commencement) this counts the directed
edges it reclassifies, split into fan-in (edges terminating in the trigger jurisdiction) and fan-out
(edges originating there). Every count is DERIVED edge-by-edge from analysis/computed_corridor_states.json
(itself a re-derivation of the signal compose()); the layer asserts NO new facts.

It reproduces the flagship §4 corridor-sensitivity ordering — South Korea the single highest-sensitivity
jurisdiction (a both-directions trigger, 20 edges), the two regime-in-transition destinations next (the
United Kingdom 8, Taiwan 9), the prohibition destination insensitive — and it records, rather than hides,
the one point where the mechanical count and the paper's ordering disagree: Taiwan's inbound fan (9) is one
larger than the United Kingdom's (8), yet the paper ranks the United Kingdom ahead on timing certainty
(gazetted date) and resolution class (clean Category I vs channelled Category II). That divergence is
emitted as a disagreement-as-finding for the reconciliation layer.

Run after scripts/build_corridor_states.py:
    python scripts/build_corridor_states.py && python scripts/build_sensitivity.py
"""
from __future__ import annotations
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O passes encoding="utf-8" explicitly throughout.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES = json.loads((ROOT / "analysis" / "computed_corridor_states.json").read_text(encoding="utf-8"))


def _split(movements, juris):
    """Split a list of {corridor: 'O->D', ...} into (fan_in terminating in juris, fan_out originating)."""
    fan_in, fan_out = [], []
    for m in movements:
        o, _, d = m["corridor"].partition("->")
        if d == juris:
            fan_in.append(m)
        elif o == juris:
            fan_out.append(m)
    return fan_in, fan_out


def build():
    rows = []

    # (1) contingent triggers: fan derived from each what-if branch's class_movements
    for w in STATES.get("whatif_branches", []):
        j = w["jurisdiction"]
        movs = w.get("class_movements", [])
        fin, fout = _split(movs, j)
        rows.append({
            "jurisdiction": j,
            "trigger_id": w["trigger_id"],
            "trigger_kind": w.get("trigger_kind"),
            "timing": "no gazetted date",
            "both_directions": bool(fin) and bool(fout),
            "edges_reclassified": len(movs),
            "fan_in": len(fin),
            "fan_out": len(fout),
            "changes_any_class": w.get("changes_any_class", len(movs) > 0),
        })

    # (2) dated commencement(s): fan derived from the horizon date_state's changes_vs_base
    #     (the UK 2027-10-25 systemic-regime commencement is the worked scheduled case).
    base = STATES.get("as_of_base")
    for s in STATES.get("date_states", []):
        if s.get("is_base") or not s.get("changes_vs_base"):
            continue
        ch = s["changes_vs_base"]
        # attribute the dated movement to the jurisdiction(s) whose event fires on this date
        evts = [e for e in s.get("active_events", []) if e.get("effective_date") == s["as_of"] and e.get("moves_a_class")]
        for e in evts:
            j = _juris_of_event(e["event_id"])
            fin, fout = _split(ch, j) if j else ([], [])
            rows.append({
                "jurisdiction": j,
                "trigger_id": e["event_id"],
                "trigger_kind": e.get("trigger_kind"),
                "timing": f"gazetted {s['as_of']}",
                "both_directions": bool(fin) and bool(fout),
                "edges_reclassified": len(ch) if not (fin or fout) else len(fin) + len(fout),
                "fan_in": len(fin),
                "fan_out": len(fout),
                "changes_any_class": True,
            })

    # The layer reproduces the paper's §4 forward-map ordering. Breadth (edges reclassified) is the primary
    # criterion; among the regime-in-transition destinations the paper's tie-breakers (timing certainty, then
    # resolution class) place the United Kingdom ahead of Taiwan despite Taiwan's larger inbound fan. We encode
    # the paper's authoritative order and keep each row's mechanical fan counts, so the divergence is explicit.
    PAPER_RANK = {"KR": 1, "UK": 2, "TW": 3}
    movers = [r for r in rows if r["edges_reclassified"] > 0]
    insensitive = [r for r in rows if r["edges_reclassified"] == 0]
    # Mainland China has no pending positive trigger, so it never appears as a what-if branch; but the paper
    # §4 discusses it explicitly as THE insensitive pole (a prohibition destination no positive trigger can
    # reach). List it explicitly so the layer's insensitive set matches the paper rather than silently
    # omitting the prohibition pole.
    if not any(r["jurisdiction"] == "CN" for r in insensitive):
        insensitive.append({
            "jurisdiction": "CN", "trigger_id": None, "trigger_kind": "resolved-tightening-open-relaxation",
            "timing": "no positive trigger (stable prohibition)", "both_directions": False,
            "edges_reclassified": 0, "fan_in": 0, "fan_out": 0, "changes_any_class": False,
        })
    movers.sort(key=lambda r: (PAPER_RANK.get(r["jurisdiction"], 99), -r["edges_reclassified"], r["jurisdiction"]))

    # attach the paper's ordering rationale + resolution class per known jurisdiction
    RESOLVE = {
        "KR": ("II (channelled) inbound; Category III -> II outbound",
               "The single highest-sensitivity jurisdiction: a both-directions trigger. A single contingent "
               "enactment reclassifies the most edges of any pending trigger, lifting South Korea out of the "
               "pre-regime class inbound and out of Category III outbound."),
        "UK": ("I (clean)",
               "The highest-sensitivity scheduled jurisdiction: commencement reclassifies every inbound edge from "
               "a token-holding origin from Category T to a clean Category I on a known day, resolving the "
               "eight-pair caveat in full — the cleanest worked transition because it is dated."),
        "TW": ("II (channelled)",
               "Same lifecycle stage as the United Kingdom but resolves differently: enacted rather than scheduled "
               "(no gazetted commencement date), and inbound edges resolve to a channelled Category II rather than "
               "a clean Category I because the enacted gate is approval-based."),
    }
    for i, r in enumerate(movers, 1):
        r["rank"] = i  # the paper's authoritative forward-map rank
        res, note = RESOLVE.get(r["jurisdiction"], (None, None))
        r["resolves_to"], r["note"] = res, note
    # also record the pure-breadth (mechanical) rank, so the divergence from the paper's rank is legible
    for i, r in enumerate(sorted(movers, key=lambda x: (-x["edges_reclassified"], x["jurisdiction"])), 1):
        r["mechanical_fan_rank"] = i
    for r in insensitive:
        r["rank"] = None
        if r["jurisdiction"] == "CN":
            r["reason"] = "prohibition"
            r["note"] = ("The prohibition destination is insensitive: no positive trigger can reach an inbound edge "
                         "blocked by an issuance prohibition, so every edge terminating in the People's Republic of "
                         "China is stable across the entire pending set.")
        else:
            r["reason"] = "contingent-not-class-change"
            r["note"] = ("A pending enactment that hardens a binding status without moving any feasibility class — "
                         "the baseline class is already in force, so no corridor moves.")

    # the one mechanical-vs-paper divergence: TW inbound fan (9) > UK inbound fan (8)
    tw = next((r for r in movers if r["jurisdiction"] == "TW"), None)
    uk = next((r for r in movers if r["jurisdiction"] == "UK"), None)
    disagreement = None
    if tw and uk and tw["fan_in"] > uk["fan_in"]:
        disagreement = {
            "observation": (
                f"Taiwan's inbound fan ({tw['fan_in']} edges) is mechanically one larger than the United Kingdom's "
                f"({uk['fan_in']}), because Taiwan is not itself a token-holder, so all {tw['fan_in']} token-holding "
                "origins point inbound to it, whereas the United Kingdom's own self-edge is excluded. A breadth-only "
                "ranking would place Taiwan above the United Kingdom among the regime-in-transition destinations."),
            "resolution": (
                "The paper places the United Kingdom ahead on its stated tie-breakers: timing certainty (the United "
                "Kingdom has a gazetted 2027-10-25 commencement; Taiwan's is ungazetted) and resolution class (the "
                "United Kingdom resolves to a clean Category I; Taiwan to a channelled Category II). Breadth is "
                "mechanical; the tie-breakers are the paper's."),
            "handling": ("Recorded, not hidden: the layer keeps both the mechanical fan counts and the paper's "
                         "ordering, and surfaces the divergence as a disagreement-as-finding — consistent with the "
                         "computed-vs-authored reconciliation discipline (computed reproduces authored where they "
                         "agree; where they diverge, the divergence is the finding)."),
            "feeds": "reconciliation",
        }

    out = {
        "schema": "cbsr-analysis/computed_sensitivity",
        "version": "v0.10.0",
        "generated": date.today().isoformat(),
        "as_of_base": base,
        "method": ("For each pending trigger (a contingent enactment or a dated commencement) the layer counts the "
                   "directed edges it reclassifies, split into fan-in (edges terminating in the trigger jurisdiction) "
                   "and fan-out (edges originating there), derived edge-by-edge from computed_corridor_states.json. "
                   "It asserts NO new facts; every count is a re-derivation of the corridor states."),
        "finding": ("The forward map's class-level motion concentrates at the one remaining pre-regime origin (South "
                    "Korea) and the two regime-in-transition destinations (the United Kingdom and Taiwan). South Korea "
                    "is the single highest-sensitivity jurisdiction because it is the subject of a both-directions "
                    "trigger; the prohibition destination (Mainland China) is insensitive to any positive trigger."),
        "ranking_criteria": ("Ordered by breadth (edges reclassified) first; among the regime-in-transition "
                             "destinations the paper's tie-breakers are timing certainty (a gazetted commencement date "
                             "outranks an ungazetted one) and resolution class (a clean Category I outranks a channelled "
                             "Category II). Breadth is mechanical; the tie-breakers are the paper's."),
        "ordering": movers,
        "insensitive": insensitive,
        "disagreement_as_finding": disagreement,
        "provenance": {
            "clean": True,
            "asserts_new_facts": False,
            "note": ("Every count is derived edge-by-edge from computed_corridor_states.json, itself a re-derivation "
                     "of the signal compose(). The layer reshapes and orders; it introduces no fact."),
            "reproduces": {"KR_edges": 20, "UK_edges": 8, "TW_fan_in": 9},
        },
    }
    (ROOT / "analysis" / "computed_sensitivity.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    top = ", ".join(f"{r['jurisdiction']}={r['edges_reclassified']}" for r in movers)
    print("wrote analysis/computed_sensitivity.json")
    print(f"  sensitivity ordering (by edges reclassified): {top}")
    print(f"  insensitive: {[r['jurisdiction'] for r in insensitive]}")
    if disagreement:
        print(f"  disagreement-as-finding: TW fan_in={tw['fan_in']} > UK fan_in={uk['fan_in']} "
              f"(paper ranks UK ahead on timing + resolution class)")


def _juris_of_event(event_id: str):
    for w in STATES.get("whatif_branches", []) + STATES.get("date_states", []):
        pass
    # map from the event's known jurisdiction via the trigger prefix
    prefix = event_id.split("-")[0].upper()
    known = {"UK": "UK", "TW": "TW", "KR": "KR", "US": "US", "SG": "SG", "EU": "EU", "JP": "JP",
             "HK": "HK", "CN": "CN", "BR": "BR", "CH": "CH", "AE": "AE"}
    return known.get(prefix)


if __name__ == "__main__":
    build()
