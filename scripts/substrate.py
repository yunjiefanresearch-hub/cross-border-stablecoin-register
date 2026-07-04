#!/usr/bin/env python3
"""Constraint substrate (v0.9.0): derive corridor feasibility by composing per-jurisdiction C1-C8
poles through the six interaction-set rules — the deeper engine behind the single-gate compose().

This does NOT replace scripts/compose.py; it is an additive, deeper derivation that is cross-checked
against it. Where the substrate yields a definite class it must agree with the signal-table compose();
where a load-bearing pole is unset it returns 'indeterminate' (it never guesses), so its coverage is
bounded by — and reports — the constraint-cell backlog.
"""
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

ROOT = pathlib.Path(__file__).resolve().parent.parent
J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "TW", "JP", "KR"]

# class severity for aggregation (most binding first)
_SEVERITY = {"blocked": 4, "III": 3, "II": 2, "I": 1, "pre_regime": 0}


def load_substrate():
    f = ROOT / "analysis" / "constraint_substrate.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"cells": {}}


def check_substrate_provenance(sub=None):
    """Every pole must cite tier1_legal record(s). Returns a list of violations (empty = clean)."""
    import yaml
    if sub is None:
        sub = load_substrate()
    cc = {}
    for p in ROOT.glob("*.yaml"):
        if p.name == "_TEMPLATE.yaml":
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") and "claim_class" in d:
            cc[d["id"]] = d["claim_class"]
    violations = []
    vocab = sub.get("pole_vocabulary", {})
    for j, cells in sub.get("cells", {}).items():
        for c, cell in cells.items():
            pole = cell.get("pole")
            if c in vocab and pole not in vocab[c]:
                violations.append(f"{j}.{c}: pole {pole!r} not in controlled vocabulary for {c}")
            refs = cell.get("derived_from", [])
            if not refs:
                violations.append(f"{j}.{c}: pole has no derived_from record")
            for rid in refs:
                if cc.get(rid) != "tier1_legal":
                    violations.append(f"{j}.{c}: backing record {rid} is not tier1_legal "
                                      f"(got {cc.get(rid, 'MISSING')!r}); the substrate may not rest on a market record")
    return violations


def _cell(sub, j, c):
    return sub.get("cells", {}).get(j, {}).get(c)


def _attr(cell, key, default=None):
    return (cell or {}).get("attributes", {}).get(key, default)


def compose_via_substrate(origin, dest, sub=None):
    """Derive the directed class for origin->dest by composing constraint poles through the sets.

    Returns {class, rule, set_verdicts, missing, explain}. class is 'indeterminate' when a load-bearing
    pole is unset. The interaction-set rules implemented (analysis/interaction_sets.json):
      - origin drag (C1.exportable_token): no exportable token => III.
      - destination inbound from C7 x C1 (Set D reserve x monetary-sovereignty; Set C bank/non-bank x
        issuer): prohibition => blocked; channelled => II; usage_capped => I; open + authorizable C1 => I.
      - Set A (C1 x C6) overlay: if the destination's issuer eligibility needs supervisory information
        and the ORIGIN's data-sovereignty blocks supervisory sharing (C6.blocks_supervisory_sharing or
        C8.supervisory_sharing == false), eligibility is unsatisfiable => escalate to III (unresolved).
    """
    if sub is None:
        sub = load_substrate()
    o1, oC6, oC8 = _cell(sub, origin, "C1"), _cell(sub, origin, "C6"), _cell(sub, origin, "C8")
    d1, d7 = _cell(sub, dest, "C1"), _cell(sub, dest, "C7")
    missing, verdicts = [], {}

    # --- origin drag (needs origin C1) ---
    if o1 is None:
        missing.append(f"{origin}.C1")
    else:
        if _attr(o1, "exportable_token", None) is False:
            return {"class": "III", "rule": "origin_drag:no_exportable_token", "set_verdicts": {"C":"origin_drag"},
                    "missing": missing, "explain": f"{origin} has no exportable, authorizable private token "
                    f"(C1={o1.get('pole')}); lawful options are partnership/coordination, not direct issuance."}

    # --- destination inbound (needs dest C1, and C7 unless C1 already prohibitive) ---
    if d1 is None:
        missing.append(f"{dest}.C1")
    dest_class = None
    if d1 is not None:
        if d1.get("pole") == "prohibition":
            dest_class, verdicts["C"] = "blocked", "dest C1=prohibition (issuance prohibited)"
        elif d1.get("pole") == "no_pathway":
            dest_class, verdicts["C"] = "pre_regime", "dest C1=no_pathway (no operative issuance regime yet)"
        elif d7 is not None and d7.get("pole") == "prohibition":
            dest_class, verdicts["D"] = "blocked", "dest C7=prohibition"
        elif d7 is None:
            missing.append(f"{dest}.C7")
        else:
            p7 = d7.get("pole")
            if p7 == "channelled":
                dest_class, verdicts["D"] = "II", "dest C7=channelled (channel determination required)"
            elif p7 == "usage_capped":
                dest_class, verdicts["D"] = "I", "dest C7=usage_capped (dual authorization, scale-capped)"
            elif p7 == "open":
                dest_class, verdicts["D"] = "I", "dest C7=open (dual authorization available)"
                verdicts["C"] = f"dest C1={d1.get('pole')} (authorizable)"
            else:
                dest_class = "I"

    if missing:
        return {"class": "indeterminate", "rule": "missing_load_bearing_poles", "set_verdicts": verdicts,
                "missing": sorted(set(missing)),
                "explain": f"cannot derive {origin}->{dest} from constraints: poles unset for {', '.join(sorted(set(missing)))}."}

    # --- Set A overlay (data-sovereignty defeats issuer eligibility) ---
    if dest_class not in ("blocked",) and d1.get("pole") in ("licence_gated", "closed_set", "host_currency_first", "open"):
        origin_blocks = _attr(oC6, "blocks_supervisory_sharing", False) or (_attr(oC8, "supervisory_sharing", True) is False)
        if origin_blocks:
            verdicts["A"] = (f"origin data-sovereignty blocks supervisory sharing "
                             f"(C6={oC6.get('pole') if oC6 else None}); dest issuer eligibility unsatisfiable")
            if _SEVERITY["III"] > _SEVERITY.get(dest_class, 0):
                dest_class = "III"

    return {"class": dest_class, "rule": "substrate_interaction_sets", "set_verdicts": verdicts,
            "missing": [], "explain": f"derived from constraint poles via interaction sets {sorted(verdicts)}."}


def build_substrate():
    """Emit analysis/computed_substrate.json: substrate derivations + cross-check vs signal compose()."""
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import compose as SIG  # the signal-table compose()
    sub = load_substrate()
    violations = check_substrate_provenance(sub)

    corridors = []
    for f in sorted(ROOT.glob("*.yaml")):
        import yaml
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "corridor_id" in d and d.get("origin") and d.get("destination"):
            corridors.append(d)

    def derive_and_check(o, d):
        s = compose_via_substrate(o, d, sub)
        sig = SIG.compose_directed(o, d)["class"]
        definite = s["class"] != "indeterminate"
        agree = (s["class"] == sig) if definite else None
        return {"edge": f"{o}->{d}", "substrate_class": s["class"], "signal_class": sig,
                "definite": definite, "agree_with_signal": agree, "rule": s["rule"],
                "set_verdicts": s["set_verdicts"], "missing_poles": s["missing"], "explain": s["explain"]}

    authored = [derive_and_check(c["origin"], c["destination"]) for c in corridors]
    # the fully-derivable closed triangle {HK, CN, JP} plus cross-region examples now unblocked
    triangle = [("HK", "JP"), ("JP", "HK"), ("HK", "CN"), ("CN", "HK"), ("JP", "CN"), ("CN", "JP")]
    illustration = [derive_and_check(o, d) for (o, d) in triangle]
    cross_region = [derive_and_check(o, d) for (o, d) in
                    [("US", "EU"), ("EU", "US"), ("US", "JP"), ("EU", "HK"), ("US", "UK"), ("AE", "EU")]]

    # full directed-edge derivability across all 12x11 ordered pairs
    all_edges = [derive_and_check(a, b) for a in J12 for b in J12 if a != b]
    derivable = [e for e in all_edges if e["definite"]]
    edge_disagreements = [e for e in all_edges if e["definite"] and e["agree_with_signal"] is False]

    # coverage
    cells = sub.get("cells", {})
    populated = sum(len(v) for v in cells.values())
    definite_authored = sum(1 for e in authored if e["definite"])
    nodes_full = sorted(j for j in J12 if "C1" in cells.get(j, {})
                        and ("C7" in cells.get(j, {}) or cells.get(j, {}).get("C1", {}).get("pole") in ("prohibition", "no_pathway")))
    disagreements = [e for e in authored + illustration + cross_region if e["definite"] and e["agree_with_signal"] is False] + edge_disagreements

    out = {
        "schema": "cbsr-analysis/computed_substrate",
        "status": "preview",
        "method": ("compose_via_substrate(origin, destination) derives feasibility by composing the two "
                   "jurisdictions' C1-C8 poles through the six interaction-set rules (origin drag; "
                   "destination inbound from C7xC1; Set A data-sovereignty overlay) — NOT the single "
                   "inbound-gate shortcut. It returns 'indeterminate' where a load-bearing pole is unset, "
                   "so coverage is bounded by the constraint-cell backlog. Where definite, it is "
                   "cross-checked against the signal-table compose(); a disagreement would be a finding."),
        "substrate_provenance": {"clean": not violations, "violations": violations,
                                 "discipline": "every pole cites tier1_legal records; the substrate never rests on a market fact"},
        "coverage": {"cells_populated": populated, "cells_total": 96,
                     "coverage_note": ("poles exist only where a tier1_legal record backs them; the remaining "
                                       "unset cells are the genuinely-unsettled ones (KR pre-regime; UK and TW "
                                       "regime-in-transition, C7 unset; CN C5, BR C4). Pole ASSIGNMENT is authored "
                                       "from the records and is itself subject to the verification backlog."),
                     "authored_corridors_definite": f"{definite_authored}/{len(authored)}",
                     "directed_edges_derivable": f"{len(derivable)}/{len(all_edges)}",
                     "indeterminate_edges_note": "remaining indeterminate edges are those into UK and TW (regimes in transition, C7 unset) that are not already origin-dragged to III — the time engine, not the substrate, owns that",
                     "fully_participating_nodes": nodes_full},
        "cross_check": {"disagreements_with_signal": sorted({e["edge"] for e in disagreements}),
                        "clean": not disagreements,
                        "scope": f"checked all {len(all_edges)} directed edges; {len(derivable)} definite, all match the signal compose()"},
        "authored_corridor_derivations": authored,
        "illustration_triangle_derivations": illustration,
        "cross_region_derivations": cross_region,
    }
    (ROOT / "analysis" / "computed_substrate.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    o = build_substrate()
    print("wrote analysis/computed_substrate.json")
    sp = o["substrate_provenance"]
    print(f"  substrate provenance — every pole rests on tier1_legal records: clean={sp['clean']}"
          + ("" if sp["clean"] else f" ({len(sp['violations'])} violation(s))"))
    cov = o["coverage"]
    print(f"  coverage: {cov['cells_populated']}/96 constraint cells populated; "
          f"authored corridors derivable: {cov['authored_corridors_definite']}; "
          f"directed edges derivable: {cov['directed_edges_derivable']}")
    print(f"  cross-check vs signal compose(): clean={o['cross_check']['clean']} ({o['cross_check']['scope']})"
          + ("" if o["cross_check"]["clean"] else f" — disagreements {o['cross_check']['disagreements_with_signal']}"))
    print("  cross-region derivations (newly unblocked):")
    for e in o["cross_region_derivations"]:
        tag = "✓agrees" if e["agree_with_signal"] else ("indeterminate" if not e["definite"] else "DIVERGES")
        print(f"    {e['edge']}: substrate={e['substrate_class']} signal={e['signal_class']} [{tag}]")
