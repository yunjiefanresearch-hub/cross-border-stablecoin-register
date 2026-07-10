#!/usr/bin/env python3
# v0.10.0 FOLD-IN COMPLETE. The class rule is no longer re-derived here: this builder imports
# tools/class_rule.py (destination-first precedence, Corridor Atlas v0.2.5 §3.4/§4.1) and reads its
# inputs from analysis/signal_table.json, which scripts/gen_signal_table.py emits from the register's
# own 152 node records. Every class_code below is DERIVED from that table by the published rule; none
# is authored. `tools/migrate_from_v0_9_92.py --check` on this builder's output exits 0, which is the
# signal that the fold-in is complete (the migration script is now a no-op).
"""build_corridors_directed.py — the directed-132 corridor layer (computed).

The register carries the full directed structure split across three shapes: 9 authored
corridors, 106 computed skeletons (analysis/computed_corridor_skeletons.json), and 17
regime-in-transition edges (into UK and TW) held by the time engine. 9 + 106 + 17 = 132.

This builder UNIFIES them into one artifact — analysis/computed_corridors_directed.json —
so every ordered pair of the twelve jurisdictions has a directed-edge record in one place.
It asserts no new facts: authored classes are taken as-authored, skeleton classes as-computed,
and the 17 transition edges are filled from the same compose algorithm + the event calendar.
Each edge's compatibility_category is set from its §5.14 pair so the cross-layer category
relationship holds by construction (build.py and run_invariants.py enforce it).

Runs in the build sequence AFTER build_edge_skeletons.py and BEFORE build.py:
    python3 scripts/build_corridors_directed.py
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
import json, pathlib, datetime
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
_sys.path.insert(0, str(ROOT / "tools"))
import class_rule                    # the ONE published class function + signal-table loader
import migrate_from_v0_9_92 as mig   # the executable specification of the v0.10.0 edge shape

# M2: stamp the register version into the artifact so no consumer has to infer it from a
# filename or an external map. Keep in step with build.py:REGISTER_VERSION on every release.
REGISTER_VERSION = "0.10.1"
mig.REGISTER_VERSION = REGISTER_VERSION   # the artifact's register_version follows the register's
ATLAS_VERSION = "v0.2.5"   # N3: the Corridor Atlas release this layer's prose cites

J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "JP", "TW", "KR"]
TOKEN_HOLDERS = {"US", "EU", "UK", "SG", "HK", "BR", "CH", "AE", "JP"}
TRANSITION_DESTS = {"UK", "TW"}
CCY = {"US": "USD", "EU": "EUR", "UK": "GBP", "SG": "SGD", "HK": "HKD", "CN": "CNY",
       "BR": "BRL", "CH": "CHF", "AE": "AED", "JP": "JPY", "TW": "NTD", "KR": "KRW"}
INFRA = {"agora": {"US", "EU", "UK", "CH", "JP", "KR"},
         "mbridge": {"CN", "HK", "AE"}, "ensemble": {"HK", "SG"}}
# Bloc membership is a Tier-2 (operational) enrichment, not a proposition of law. The `agora` and
# `mbridge` member sets were externally verified by the first two reviews; `ensemble={HK, SG}` treats
# the HKMA-Project-Ensemble / MAS-Project-Guardian alignment as a shared bloc, but SG's *formal*
# Ensemble membership is pending primary verification (verification_backlog VB-02, third review).
_BLOC_LABEL = {"agora": "Project Agora", "mbridge": "mBridge", "ensemble": "Project Ensemble"}


def bloc_of(o, d):
    """The settlement-substrate partition, returning the canonical enum (v0.9.93).

    Identical rule to tools/verify_corridors_directed.py:infra_overlap and the migration
    script's bloc_of, so builder / verifier / migration cannot disagree by construction.
    """
    om = {k for k, v in INFRA.items() if o in v}
    dm = {k for k, v in INFRA.items() if d in v}
    shared = om & dm
    if "ensemble" in shared:
        return "ensemble"
    if "mbridge" in shared:
        return "mbridge"
    if "agora" in shared:
        return "agora"
    if ("agora" in om and "mbridge" in dm) or ("mbridge" in om and "agora" in dm):
        return "cross-bloc"
    return "none"


def _ends_on(j):
    on = sorted(_BLOC_LABEL[k] for k, v in INFRA.items() if j in v)
    return " + ".join(on) if on else "no shared wholesale-settlement experiment"


def infra_overlap(o, d):
    """Structured {bloc, note} (v0.9.93). bloc is the machine-consumable partition enum,
    checked on ALL 132 edges by verifier IB1; note is a deterministic human gloss."""
    bloc = bloc_of(o, d)
    if bloc == "cross-bloc":
        note = (f"{o} on {_ends_on(o)}; {d} on {_ends_on(d)}. Rival bloc rails, not mutually "
                f"interoperable: no shared production or pilot settlement rail (commercial rails "
                f"subject to both regimes).")
    elif bloc == "ensemble":
        # v0.9.94: HK-SG is an HKMA-Ensemble / MAS-Guardian alignment; SG's formal Ensemble
        # membership is a Tier-2 attribution pending primary verification (verification_backlog VB-02).
        note = ("HKMA Project Ensemble and MAS Project Guardian alignment "
                f"({o} and {d}); SG's formal Project Ensemble membership is a Tier-2 attribution "
                "pending primary verification (verification_backlog VB-02).")
    elif bloc in ("agora", "mbridge"):
        note = f"Both ends on {_BLOC_LABEL[bloc]} ({o} and {d})."
    else:
        note = f"{o} on {_ends_on(o)}; {d} on {_ends_on(d)}. At least one end off the shared experiments."
    return {"bloc": bloc, "note": note}


def _load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _authored_class_code(fc: str) -> str:
    s = (fc or "").lower()
    if "blocked" in s:
        return "blocked"
    if "pre-regime" in s or "pre regime" in s:
        return "pre_regime"
    if "transition" in s:
        return "T"
    if "category iii" in s:
        return "III"
    if "category i/ii" in s:
        return "II"
    if "category ii" in s:
        return "II"
    if "category i" in s:
        return "I"
    return "?"


def load_authored():
    out = {}
    for f in sorted(ROOT.glob("*.yaml")):
        if f.name == "_TEMPLATE.yaml":
            continue
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("corridor_id") and d.get("origin") and d.get("destination"):
            out[(d["origin"], d["destination"])] = (f.name, d)
    return out


def edge_timeline(o, d, events):
    tl = {"today_class": "T", "as_of_base": "2026-06-30", "scheduled": [], "contingent": []}
    for e in events:
        if e.get("jurisdiction") != d or not e.get("effect"):
            continue
        if not any(x.get("field") == "regime_status" and x.get("to") == "live" for x in e["effect"]):
            continue
        gate_to = next((x["to"] for x in e["effect"] if x.get("field") == "inbound_gate"), None)
        # N4 (hardening): map the enacted inbound-gate type to a resolved class explicitly.
        # An UNKNOWN gate value must abort, not silently resolve to a clean Category I.
        _GATE_TO_CLASS = {"open": "I", "channel": "II"}
        if gate_to not in _GATE_TO_CLASS:
            raise SystemExit(
                f"[N4] event {e.get('id')} for {d}: inbound_gate transition 'to'={gate_to!r} is "
                f"not one of {sorted(_GATE_TO_CLASS)}. Refusing to default the resolved class to a "
                f"clean Category I. Fix the event calendar entry.")
        resolved = _GATE_TO_CLASS[gate_to]
        row = {"event_id": e["id"], "effective_date": e.get("effective_date"),
               "status": e["status"], "resolves_to": resolved}
        (tl["scheduled"] if e["status"] == "scheduled" and e.get("effective_date") else tl["contingent"]).append(row)
    return tl


def materialize():
    """Return (edges_by_pair dict keyed (o,d), provenance_counts). Consumes register data only."""
    pairs = {p["pair"]: p for p in _load("analysis/compatibility.json")["pairs"]}
    pair_by_set = {frozenset(p["jurisdictions"]): p for p in pairs.values()}
    skeletons = _load("analysis/computed_corridor_skeletons.json")["skeletons"]
    events = _load("analysis/event_calendar.json")["events"]
    authored = load_authored()

    recs, prov = {}, {"authored": 0, "computed_skeleton": 0, "computed_transition": 0}

    # 1) authored win
    for (o, d), (fname, doc) in authored.items():
        r = dict(doc)
        r["materialized_from"] = "authored"
        r["authored_source_file"] = fname
        if not r.get("class_code"):
            r["class_code"] = _authored_class_code(r.get("feasibility_class", ""))
        recs[(o, d)] = r
        prov["authored"] += 1

    # 2) computed skeletons
    for sk in skeletons:
        o, d = sk["origin"], sk["destination"]
        if (o, d) in recs:
            continue
        p = pair_by_set.get(frozenset({o, d}), {})
        recs[(o, d)] = {
            "corridor_id": f"{o.lower()}-{d.lower()}-directed",
            "name": f"{o} -> {d} ({CCY[o]}->{CCY[d]} directed edge)",
            "schema": "corridor/v3-directed-edge", "origin": o, "destination": d,
            "direction": "directed", "currencies": f"{CCY[o]} -> {CCY[d]}",
            "feasibility_class": sk.get("feasibility_class"), "class_code": sk.get("class_code"),
            "compatibility_category": p.get("category"),
            "compatibility_pair": sk.get("compatibility_pair") or p.get("pair"),
            "archetypes": sk.get("archetypes", ["RC", "DC"]),
            "interaction_sets": sk.get("interaction_sets", []),
            "infrastructure_overlap": sk.get("infrastructure_overlap") or infra_overlap(o, d),
            "inbound_mechanism": sk.get("inbound_mechanism", {}),
            "origin_drag": sk.get("origin_drag"),
            "materialized_from": "computed_skeleton",
        }
        prov["computed_skeleton"] += 1

    # 3) transition edges (token-holding origins into UK and TW)
    for d in TRANSITION_DESTS:
        for o in J12:
            if o == d or o not in TOKEN_HOLDERS or (o, d) in recs:
                continue
            p = pair_by_set.get(frozenset({o, d}), {})
            tl = edge_timeline(o, d, events)
            # N4: a transition destination MUST have a scheduled or contingent resolution in the
            # event calendar. Through v0.9.92 a missing entry silently defaulted to a clean
            # Category I ([{"resolves_to": "I"}]); a jurisdiction added to TRANSITION_DESTS without
            # a calendar entry would then be mislabelled I. Abort instead, so the omission is loud.
            _resolutions = tl["scheduled"] or tl["contingent"]
            if not _resolutions:
                raise SystemExit(
                    f"[N4] transition edge {o}->{d}: {d} is in TRANSITION_DESTS but the event "
                    f"calendar has no scheduled or contingent regime-goes-live resolution for it. "
                    f"Refusing to default to a clean Category I. Add a calendar entry for {d} "
                    f"(or remove it from TRANSITION_DESTS).")
            resolves = _resolutions[0]["resolves_to"]
            when = tl["scheduled"][0]["effective_date"] if tl["scheduled"] else "pending (contingent, no gazetted date)"
            recs[(o, d)] = {
                "corridor_id": f"{o.lower()}-{d.lower()}-directed",
                "name": f"{o} -> {d} ({CCY[o]}->{CCY[d]} directed edge)",
                "schema": "corridor/v3-directed-edge", "origin": o, "destination": d,
                "direction": "directed", "currencies": f"{CCY[o]} -> {CCY[d]}",
                "feasibility_class": ("Regime-in-transition (destination regime adopted, not yet "
                                      f"operative; resolves to Category {resolves} at {when})"),
                "class_code": "T", "compatibility_category": p.get("category"),
                "compatibility_pair": p.get("pair"),
                "archetypes": ["RC", "SC", "TC", "DC"], "interaction_sets": p.get("interaction_sets", []),
                "infrastructure_overlap": infra_overlap(o, d),
                "inbound_mechanism": {
                    "test": ("FCA conduct + BoE systemic regime (adopted; operative 2027-10-25)" if d == "UK"
                             else "Virtual Asset Service Act enacted 2026-06-30; FSC-approval inbound gate on commencement"),
                    "administrator": "FCA / Bank of England" if d == "UK" else "FSC (CBC consulted)",
                    "detail": None},
                "as_of_timeline": tl, "materialized_from": "computed_transition",
            }
            prov["computed_transition"] += 1
    return recs, prov, pairs


def build():
    recs, prov, pairs = materialize()
    ordered = [(o, d) for o in J12 for d in J12 if o != d]
    edges = [recs[k] for k in ordered if k in recs]

    # v0.9.93 normalization: guarantee EVERY edge (authored included) carries the structured
    # infrastructure_overlap {bloc, note}, with bloc recomputed from the partition function and
    # a canonical, deterministic note. This authoritatively sets bloc, which is what closes the
    # US<->HK gap that IB1 now checks, and makes the output reproducible (no free-text variance).
    for e in edges:
        e["infrastructure_overlap"] = infra_overlap(e["origin"], e["destination"])

    # self cross-check: every edge's compatibility_category must equal its §5.14 pair category
    mism = []
    for e in edges:
        pr = e.get("compatibility_pair")
        row = pairs.get(pr)
        if row is None:
            mism.append(f"{e['corridor_id']}: pair {pr!r} not in §5.14 matrix")
        elif e.get("compatibility_category") != row.get("category"):
            mism.append(f"{e['corridor_id']}: category {e.get('compatibility_category')!r} != §5.14 {pr} {row.get('category')!r}")

    dist = {}
    for e in edges:
        dist[e.get("class_code")] = dist.get(e.get("class_code"), 0) + 1

    out = {
        "schema": "cbsr-analysis/computed_corridors_directed",
        "generated": str(datetime.date.today()),
        "register_version": REGISTER_VERSION,   # M2: stamped, not inferred
        "source": ("Unifies the register's own layers: authored corridors (root *.yaml), computed "
                   "skeletons (analysis/computed_corridor_skeletons.json), and the event-calendar "
                   "transition edges. No new facts; compatibility_category is taken from the §5.14 matrix."),
        "note": ("Directed-edge interaction_sets are the Atlas per-direction refinement and may differ "
                 "from the undirected §5.14 pair; only the compatibility_category is a hard cross-layer "
                 "relationship and is enforced (build.py check_directed_cross_layer; run_invariants DC*)."),
        "coverage": {
            "edges_total": len(edges), "ordered_pairs_expected": len(ordered),
            "authored": prov["authored"], "computed_skeleton": prov["computed_skeleton"],
            "computed_transition": prov["computed_transition"],
            "class_distribution": dist,
        },
        "provenance": {
            "clean": True,
            "basis": ("authored + tier1_legal-backed skeletons + event-calendar transitions; the directed "
                      "layer inherits the skeletons' signal-provenance (every driving signal is tier1_legal)"),
        },
        "cross_check": {"clean": len(mism) == 0, "category_mismatches": mism},
        "edges": edges,
    }
    # ------------------------------------------------------------------------------------------
    # v0.10.0 fold-in. Everything above assembles the register's own three production shapes into
    # one 132-edge base; everything below DERIVES the analytical content from the signal table, by
    # the published rule, and asserts nothing new.
    #
    #   * every `class_code` is recomputed by tools/class_rule.py:class_of over
    #     analysis/signal_table.json (destination-first precedence), replacing the base shapes'
    #     origin-drag-first classes. Four edges move on precedence (TW/KR -> CN to `blocked`,
    #     CN/TW -> KR to `pre_regime`) and eight move because the US §18 gate is not yet in force
    #     (II -> T; GENIUS Act §20, errata E1 / VB-06).
    #   * every edge gains `class_basis` — which precedence step decided it, on whose signal, at
    #     what claim_class, resting on which instrument at what binding_status — so the three-axis
    #     evidence model reaches the corridor layer.
    #   * `as_of_timeline` becomes a typed trigger (gazetted | outer_cap | ungazetted) on exactly
    #     the `T` edges, and the Atlas's origin-egress override lands on all 33 CN/SG/KR rows.
    #
    # The transforms are the ones tools/migrate_from_v0_9_92.py specifies, imported rather than
    # re-implemented, so builder and migration cannot disagree by construction.
    # ------------------------------------------------------------------------------------------
    out = mig.migrate(out)

    # record_ref propagation — the C1 / VB-11 closure. The migration script hardcodes
    # `record_ref: None` because the audit repository did not ship the node records. The register
    # does, so every edge's class_basis now carries a locator into the very record its class rests
    # on. Nothing is fabricated: the locator is whatever gen_signal_table.py bound to that signal,
    # `match`-tagged, and where no record carries the instrument the ref stays null with its reason.
    # `record_ref` stays what the schema says a locator is: a STRING (the node-record id), or null.
    # Everything a reader needs to weigh that locator -- whether the record rests on the very
    # instrument the class rests on (`match`), the record's own binding_status, and, where the two
    # layers disagree, the declared reason -- goes in the sibling `record_ref_meta`. A locator is
    # never diluted by the metadata that qualifies it (citable purity, Citable by Construction §4.2).
    signals = class_rule.load()["signals"]
    n_ref = 0
    n_same = 0
    for e in out["edges"]:
        cb = e["class_basis"]
        sig = signals[cb["governing_jurisdiction"]][cb["signal"]]
        ref = sig.get("record_ref")
        cb["record_ref"] = ref["record_id"] if ref else None
        if ref:
            cb["record_ref_meta"] = {k: v for k, v in ref.items() if k != "record_id"}
            n_ref += 1
            n_same += ref["match"] == "same_instrument"
        if sig.get("record_ref_gap"):
            cb["record_ref_gap"] = sig["record_ref_gap"]

    out["provenance"]["record_ref"] = (
        f"{n_ref}/{len(out['edges'])} edges carry a class_basis.record_ref into a published node "
        f"record ({n_same} of them at match=same_instrument); backlog VB-11 is closed for this "
        f"register, because the 152 node records ARE shipped here and the locator can be supplied "
        f"rather than declined. `match: related_dimension` marks a locator that is the right dimension "
        f"but a different instrument from the one the class rests on; every such case, and every "
        f"binding-status divergence between the signal and the record it cites, is emitted as a "
        f"finding in analysis/signal_table.json:record_binding_findings rather than reconciled away.")
    out["provenance"]["signal_table"] = "analysis/signal_table.json"

    ok, problems = mig.is_migrated(out)
    if not ok:
        print("[FAIL] the built artifact is not in v0.10.0 shape:", file=_sys.stderr)
        for pb in problems[:10]:
            print("   -", pb, file=_sys.stderr)
        _sys.exit(1)

    edges = out["edges"]
    dist = out["coverage"]["class_distribution"]
    n_tl = out["coverage"]["timeline_edges"]
    n_ov = sum(1 for e in edges if "origin_override" in e)
    n_cb = sum(1 for e in edges if e["infrastructure_overlap"]["bloc"] == "cross-bloc")

    (ROOT / "analysis" / "computed_corridors_directed.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"wrote analysis/computed_corridors_directed.json — {len(edges)} directed edges "
          f"(authored {prov['authored']} + skeleton {prov['computed_skeleton']} + transition {prov['computed_transition']})")
    print(f"  class distribution (derived by class_rule over the signal table): {dist}")
    print(f"  class_basis on {len(edges)}/{len(edges)} edges; record_ref populated on {n_ref} "
          f"({n_same} same_instrument, {n_ref - n_same} related_dimension)")
    print(f"  {n_tl} typed as_of_timeline edges; {n_ov} origin-override edges; {n_cb} cross-bloc edges")
    print(f"  cross-layer category check (self): {'clean ✓' if not mism else f'{len(mism)} MISMATCH'}")
    if mism:
        for m in mism[:5]:
            print("   -", m)
        _sys.exit(1)


if __name__ == "__main__":
    build()
