#!/usr/bin/env python3
"""regen_forward_sensitivity.py — bring the forward/sensitivity layer into line with the corrected
directed-corridor layer, from REGISTER-INTERNAL DATA ONLY (no frontend/JSX dependency).

Background
  v0.10.0's directed-corridor layer already scored the eight inbound-US edges as regime-in-transition
  (T, resolving to Category II when the GENIUS §18 foreign-issuer comparability gate commences — dated
  outer cap 2027-01-18), but three derived files still framed the US as already-live and left it out of
  the sensitivity ordering. v0.10.1 corrected that. The original v0.10.1 regeneration sourced the
  corrected transition set from the mapper JSX's COMPUTE.corridors — a backwards dependency that made the
  register non-reproducible from its own scripts (CI's `git diff --exit-code` would revert it).

  This script removes that coupling. The corrected forward transition set is now frozen as a first-class,
  version-controlled register input at analysis/forward_transition_set.json (proven edge-for-edge
  identical to the register's own directed-corridor layer, 132/132). This step reads that frozen set,
  re-derives the per-jurisdiction sensitivity edge counts, cross-checks them two independent ways, and
  writes the corrected computed_sensitivity.json / computed_forward_view.json (+ their api projections).

  It asserts NO new legal facts. It exits non-zero if any cross-check fails, so it is a build GATE, not a
  silent overwrite.

Run in the pipeline AFTER scripts/build_forward_view.py (which produces the pre-correction, date-state
form from the not-yet-regenerated computed_corridor_states.json engine — the v0.10.2 follow-up):
    python scripts/build_forward_view.py && python scripts/regen_forward_sensitivity.py
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
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANA = ROOT / "analysis"
API = ROOT / "api"

# The register version this regeneration targets. Kept in one place; the pipeline's build.py owns the
# authoritative REGISTER_VERSION and the invariant suite's V3 gate enforces cross-artifact agreement.
NEWV = "0.10.1"


def rj(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def wj(p: Path, o) -> None:
    with p.open("w", encoding="utf-8") as f:
        json.dump(o, f, ensure_ascii=False, indent=2)
        f.write("\n")


def die(msg: str) -> None:
    print("  FAIL  " + msg)
    raise SystemExit(1)


def main() -> None:
    tset_path = ANA / "forward_transition_set.json"
    if not tset_path.exists():
        die(f"missing frozen transition set: {tset_path.relative_to(ROOT)} "
            "(this is a required, version-controlled register input)")
    tset = rj(tset_path)
    OWNER = tset["owner_of_event"]
    moves = list(tset.get("scheduled", [])) + list(tset.get("contingent", []))
    directed = rj(ANA / "computed_corridors_directed.json")
    edgemap = {(e["origin"], e["destination"]): e for e in directed["edges"]}

    # --- Cross-check 1: every SCHEDULED move matches the register's own edge as_of_timeline ----------
    sched_mismatch = []
    for mv in tset.get("scheduled", []):
        o, d = mv["edge"].split("->")
        e = edgemap.get((o, d), {})
        tl = e.get("as_of_timeline") or {}
        ok = any(s.get("event_id") == mv["event_id"] and s.get("resolves_to") == mv["to"]
                 for s in tl.get("scheduled", []))
        if not ok:
            sched_mismatch.append((mv["edge"], mv["event_id"], mv["to"]))
    if sched_mismatch:
        die(f"{len(sched_mismatch)} scheduled transition(s) do not match the directed layer's "
            f"as_of_timeline: {sched_mismatch[:5]}")

    # --- Cross-check 2: recomputed per-jurisdiction fan counts equal the frozen ordering ------------
    recompute = defaultdict(lambda: {"fan_in": 0, "fan_out": 0})
    for mv in moves:
        owner = OWNER.get(mv["event_id"])
        if not owner:
            continue
        o, d = mv["edge"].split("->")
        if d == owner:
            recompute[owner]["fan_in"] += 1
        if o == owner:
            recompute[owner]["fan_out"] += 1
    for k in recompute:
        recompute[k]["edges"] = recompute[k]["fan_in"] + recompute[k]["fan_out"]

    frozen_order = {o["jurisdiction"]: o for o in tset["sensitivity_payload"]["ordering"]}
    mismatch = []
    for j, o in frozen_order.items():
        r = recompute.get(j, {})
        if (r.get("edges") != o.get("edges_reclassified")
                or r.get("fan_in") != o.get("fan_in")
                or r.get("fan_out") != o.get("fan_out")):
            mismatch.append((j, dict(r), {k: o.get(k) for k in ("edges_reclassified", "fan_in", "fan_out")}))
    if mismatch:
        die(f"recomputed sensitivity counts disagree with the frozen ordering: {mismatch}")

    # --- Write computed_forward_view.json ----------------------------------------------------------
    fwd = rj(ANA / "computed_forward_view.json")
    fwd["version"] = "v" + NEWV
    fwd["generated"] = tset.get("generated", "2026-07-09") + "T00:00:00Z"
    fwd.setdefault("provenance", {})["regenerated"] = (
        "v%s: forward view re-derived from the register's own frozen forward transition set "
        "(analysis/forward_transition_set.json); US carries its own class-moving trigger "
        "(us-genius-act-effective, §18 comparability-gate commencement, dated outer cap 2027-01-18) on "
        "8 inbound edges. Self-contained: no frontend dependency." % NEWV)
    fwd["provenance"]["asserts_new_facts"] = False
    fwd["jurisdictions"] = _forward_from_payload(tset["forward_payload"])
    wj(ANA / "computed_forward_view.json", fwd)

    api_fwd = rj(API / "forward.json")
    api_fwd["version"] = NEWV
    api_fwd["generated"] = tset.get("generated", "2026-07-09")
    api_fwd["data"] = fwd
    wj(API / "forward.json", api_fwd)

    # --- Write computed_sensitivity.json -----------------------------------------------------------
    sens = rj(ANA / "computed_sensitivity.json")
    ms = tset["sensitivity_payload"]
    sens["version"] = "v" + NEWV
    sens["generated"] = tset.get("generated", "2026-07-09")
    sens["finding"] = ms.get("finding", sens.get("finding"))
    sens["ranking_criteria"] = ms.get("ranking_criteria", sens.get("ranking_criteria"))
    sens["ordering"] = ms["ordering"]
    sens["insensitive"] = ms["insensitive"]
    if "two_orderings" in ms:
        sens["two_orderings"] = ms["two_orderings"]
    if "disagreement" in ms:
        sens["disagreement_as_finding"] = ms["disagreement"]
    sens.setdefault("provenance", {})["regenerated"] = (
        "v%s: recomputed from the register's own frozen forward transition set. US moves from the "
        "insensitive set to an 8-edge class-mover via us-genius-act-effective (§18 gate commencement); "
        "KR fan counts and TW both-directions counts re-derived under destination-first precedence. "
        "Cross-checked two ways (scheduled==as_of_timeline; recomputed counts==ordering)." % NEWV)
    sens["provenance"]["asserts_new_facts"] = False
    wj(ANA / "computed_sensitivity.json", sens)

    api_sens = rj(API / "sensitivity.json")
    api_sens["version"] = NEWV
    api_sens["generated"] = tset.get("generated", "2026-07-09")
    api_sens["data"] = sens
    wj(API / "sensitivity.json", api_sens)

    order_str = " / ".join(f"{o['jurisdiction']} {o['edges_reclassified']}" for o in ms["ordering"])
    insens_str = ", ".join(i.get("jurisdiction") for i in ms["insensitive"])
    print("regen_forward_sensitivity: OK (register-internal, no JSX)")
    print(f"  scheduled moves {len(tset.get('scheduled', []))} match as_of_timeline; "
          f"recomputed counts match ordering")
    print(f"  ordering {order_str}; insensitive {{{insens_str}}}")
    print("  wrote computed_forward_view.json, computed_sensitivity.json, api/forward.json, api/sensitivity.json")


def _forward_from_payload(mf: dict) -> dict:
    """Transcode the frozen forward payload into the computed_forward_view jurisdictions schema."""
    EVKEYS = ("event_id", "title", "trigger_kind", "status", "effective_date",
              "moves_class", "accessibility_only")
    out = {}
    for J, b in mf.items():
        out[J] = {
            "jurisdiction": J,
            "own_pending_events": [{k: ev.get(k) for k in EVKEYS} for ev in b.get("events", [])],
            "summary": b.get("summary", {}),
            "inbound_reclassified": b.get("inbound", []),
            "outbound_reclassified": b.get("outbound", []),
            "counterpart_exposure": b.get("exposure", []),
            "supervisor_reading": b.get("reading", ""),
        }
    return out


if __name__ == "__main__":
    main()
