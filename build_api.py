#!/usr/bin/env python3
"""Emit a static JSON API under ./api/ so anyone can fetch the register without cloning.

Pure static files for GitHub Pages — zero backend, zero database. Every endpoint is a
projection of the already-built dataset.json + the corridor-state precompute; it adds no
facts. This turns "a repository" into "a queryable data service" while keeping all five
guardrails: static only; what-if endpoints carry only the register's own if-then branches
with no probabilities; the citable endpoint carries only human-verified cells; the citable
endpoint never mixes operational facts; everything traces to the public register.

Run after build.py and build_corridor_states.py:  python3 build_api.py
"""

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, pathlib, datetime, shutil

ROOT = pathlib.Path(__file__).resolve().parent
API = ROOT / "api"
DS = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
STATES = json.loads((ROOT / "analysis" / "computed_corridor_states.json").read_text(encoding="utf-8"))
CONV_PATH = ROOT / "analysis" / "computed_convergence.json"
CONV = json.loads(CONV_PATH.read_text(encoding="utf-8")) if CONV_PATH.exists() else {}
SENS_PATH = ROOT / "analysis" / "computed_sensitivity.json"
SENS = json.loads(SENS_PATH.read_text(encoding="utf-8")) if SENS_PATH.exists() else {}
SETT_PATH = ROOT / "analysis" / "computed_settlement.json"
SETT = json.loads(SETT_PATH.read_text(encoding="utf-8")) if SETT_PATH.exists() else {}
FV_PATH = ROOT / "analysis" / "computed_forward_view.json"
FV = json.loads(FV_PATH.read_text(encoding="utf-8")) if FV_PATH.exists() else {}

RECORDS = DS["records"]
J12 = STATES["jurisdictions"]
VERSION = DS.get("version", "")


def _w(relpath, obj):
    p = API / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return relpath


def _envelope(kind, data, extra=None):
    e = {"register": "Cross-Border Stablecoin Register", "version": VERSION,
         "generated": str(datetime.date.today()), "endpoint": kind,
         "guardrail": "static projection of the public register; no facts added here", **(extra or {})}
    e["data"] = data
    return e


def build():
    if API.exists():
        shutil.rmtree(API)
    API.mkdir(parents=True)
    written = []

    # ---- meta ----------------------------------------------------------------
    written.append(_w("meta.json", _envelope("meta", {
        "version": VERSION,
        "record_count": DS.get("record_count", len(RECORDS)),
        "jurisdictions": J12,
        "as_of_base": STATES["as_of_base"],
        "key_dates": STATES["key_dates"],
        "citable_count": DS["citable_subset"]["count"],
        "authored_corridors": len(DS.get("corridors", [])),
    })))

    # ---- records (full + faceted axes) --------------------------------------
    slim = [{"id": r["id"], "jurisdiction": r["jurisdiction"], "dimension": r["dimension"],
             "claim_class": r.get("claim_class"), "evidence_tier": r.get("evidence_tier"),
             "binding_status": r.get("binding_status"), "status": r.get("status"),
             "instrument": (r.get("source") or {}).get("primary") or r.get("instrument_label_local"),
             "pinpoint": (r.get("source") or {}).get("pinpoint"),
             "url": (r.get("source") or {}).get("url")} for r in RECORDS]
    written.append(_w("records.json", _envelope("records", slim,
                     {"axes": ["claim_class", "evidence_tier", "binding_status"]})))

    # per-jurisdiction
    _fvj = (FV.get("jurisdictions") or {})
    for j in J12:
        jr = [s for s in slim if s["jurisdiction"] == j]
        cit = [c for c in DS["citable_subset"]["records"] if c["jurisdiction"] == j]
        sig = STATES["date_states"][0]["directed"].get(j, {})  # this jurisdiction as origin at base
        written.append(_w(f"jurisdictions/{j}.json", _envelope("jurisdiction", {
            "jurisdiction": j, "records": jr, "citable_cells": cit,
            "outbound_classes_at_base": sig,
            "forward": _fvj.get(j, {}),  # §4.4 supervisor forward view: pending events + reclassified edges + counterpart exposure
        })))

    # ---- events + by-kind ----------------------------------------------------
    ev = DS["analysis"]["event_calendar"]
    written.append(_w("events.json", _envelope("events", ev.get("events", []),
                     {"trigger_kind_legend": ev.get("trigger_kind_legend", {})})))
    by_kind = {}
    for e in ev.get("events", []):
        by_kind.setdefault(e.get("trigger_kind", "unclassified"), []).append(e["id"])
    written.append(_w("events/by_kind.json", _envelope("events_by_kind", by_kind,
                     {"trigger_kind_legend": ev.get("trigger_kind_legend", {})})))

    # ---- corridor states (dated + what-if), full and per key date -----------
    written.append(_w("corridor_states.json", _envelope("corridor_states", {
        "key_dates": STATES["key_dates"],
        "date_states": STATES["date_states"],
        "whatif_branches": STATES["whatif_branches"],
        "trigger_kind_legend": STATES["trigger_kind_legend"],
        "provenance": STATES["provenance"],
    })))
    for st in STATES["date_states"]:
        written.append(_w(f"dates/{st['as_of']}.json", _envelope("date_matrix", st)))

    # per-corridor (66 undirected units, each carrying both directed classes,
    # the dated timeline across key dates, and every what-if branch touching it)
    idx = {j: i for i, j in enumerate(J12)}
    for i, o in enumerate(J12):
        for d in J12[i + 1:]:
            key = f"{o}-{d}"
            timeline = []
            for st in STATES["date_states"]:
                timeline.append({"as_of": st["as_of"],
                                 "directed": {f"{o}->{d}": st["directed"][o][d],
                                              f"{d}->{o}": st["directed"][d][o]},
                                 "undirected": st["undirected"].get(key)})
            whatif = []
            for w in STATES["whatif_branches"]:
                moves = [m for m in w["class_movements"]
                         if m["corridor"] in (f"{o}->{d}", f"{d}->{o}")]
                whatif.append({"trigger_id": w["trigger_id"], "trigger_kind": w["trigger_kind"],
                               "changes_this_corridor": bool(moves), "movements": moves,
                               "note": w["note"]})
            written.append(_w(f"corridors/{key}.json", _envelope("corridor", {
                "corridor": key, "timeline": timeline, "whatif": whatif})))

    # ---- convergence ---------------------------------------------------------
    if CONV:
        written.append(_w("convergence.json", _envelope("convergence", CONV)))

    # ---- citable subset (lawyer view; human-verified cells only) ------------
    written.append(_w("citable.json", _envelope("citable", DS["citable_subset"]["records"],
                     {"filter": DS["citable_subset"]["filter"],
                      "count": DS["citable_subset"]["count"],
                      "guardrail": "human-verified propositions of law only; operational facts excluded by construction"})))

    # ---- reconciliation (authored vs computed) ------------------------------
    comp = DS["analysis"]["computed"]
    written.append(_w("reconciliation.json", _envelope("reconciliation", {
        "undirected_pairs": comp["undirected_pairs"]["pairs"],
        "agreement": comp["undirected_pairs"]["agreement"],
        "findings_by_cause": comp["findings_by_cause"],
        "note": "computed layer is a labelled preview; a divergence is a finding, never an authoritative correction",
    })))

    # ---- corridor sensitivity (§4 forward-map ordering; feeds reconciliation) -
    if SENS:
        written.append(_w("sensitivity.json", _envelope("sensitivity", SENS)))

    # ---- settlement substrate (§5.2 bloc partition; Tier-2 enrichment) -------
    if SETT:
        written.append(_w("settlement.json", _envelope("settlement", SETT)))

    # ---- per-jurisdiction supervisor forward view (§4.4 re-sort) -------------
    if FV:
        written.append(_w("forward.json", _envelope("forward_view", FV)))

    # ---- verification worklist (honest residual) ----------------------------
    wl = DS["analysis"]["verification_worklist"]
    written.append(_w("worklist.json", _envelope("verification_worklist", {
        "headline": wl["headline"], "status": wl["status"], "items": wl["items"]})))

    # ---- index (endpoint manifest) ------------------------------------------
    corridor_keys = sorted({f for f in written if f.startswith("corridors/")})
    manifest = {
        "meta": "meta.json",
        "records": "records.json",
        "jurisdictions": {j: f"jurisdictions/{j}.json" for j in J12},
        "events": "events.json",
        "events_by_kind": "events/by_kind.json",
        "corridor_states": "corridor_states.json",
        "dates": {st["as_of"]: f"dates/{st['as_of']}.json" for st in STATES["date_states"]},
        "corridors": corridor_keys,
        "convergence": "convergence.json" if CONV else None,
        "sensitivity": "sensitivity.json" if SENS else None,
        "settlement": "settlement.json" if SETT else None,
        "forward": "forward.json" if FV else None,
        "citable": "citable.json",
        "reconciliation": "reconciliation.json",
        "worklist": "worklist.json",
    }
    _w("index.json", _envelope("index", manifest, {
        "description": ("Static JSON API for the Cross-Border Stablecoin Register. All endpoints "
                        "are projections of the public dataset.json; fetch any file directly."),
        "endpoint_count": len(written) + 1,
    }))

    print(f"wrote api/ — {len(written) + 1} JSON files")
    print(f"  meta, records (+{len(J12)} jurisdictions), events (+by_kind),")
    print(f"  corridor_states (+{len(STATES['date_states'])} dates, +{len(corridor_keys)} corridors),")
    print(f"  convergence, citable ({DS['citable_subset']['count']}), reconciliation, worklist, index")


if __name__ == "__main__":
    build()
