#!/usr/bin/env python3
"""Edge-layer densification (v0.9.4). The 9 hand-authored corridor records are the ENRICHED gold tier
(they carry infrastructure_overlap, bespoke inbound detail, curated archetypes, prose). For every OTHER
derivable directed edge this emits a COMPUTED SKELETON: the structurally-derivable fields only —
feasibility class (from the substrate), inbound mechanism test + administrator (re-projected from the
destination's C1/C7 record), a baseline archetype set, the directed interaction sets, and provenance.

It introduces no new facts: the inbound test/administrator are re-read from existing records, the class is
the already-cross-checked substrate class, and the genuinely EMPIRICAL fields (infrastructure_overlap,
bespoke detail, curated archetypes, prose) are left explicitly UNSET as a per-edge enrichment backlog.
Emits analysis/computed_corridor_skeletons.json."""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "TW", "JP", "KR"]

# Per-destination inbound mechanism (test, administrator) — a re-projection of each regime's C1/C7 record.
DEST_MECHANISM = {
    "US": ("GENIUS Act §18 comparability determination + OCC registration; US-held reserves", "US Treasury (SCRC) / OCC"),
    "EU": ("MiCA authorization; significant-EMT scale caps (Art. 23)", "EBA / ESMA / national competent authorities"),
    "UK": ("FSMA 2026 regime — in transition (systemic regime pending)", "FCA / Bank of England"),
    "SG": ("MAS single-currency-stablecoin recognition; foreign-pegged tokens treated as DPTs", "MAS"),
    "HK": ("HKMA stablecoin licensing", "HKMA"),
    "CN": ("Issuance and circulation prohibited", "PBOC / CAC"),
    "BR": ("BCB VASP / FX-counterparty channel", "Banco Central do Brasil"),
    "CH": ("FINMA authorization (banking / DLT framework)", "FINMA"),
    "AE": ("CBUAE Payment Token Services licensing (usage channel)", "CBUAE"),
    "TW": ("No operative inbound regime (draft VAS Act)", "FSC (Taiwan)"),
    "JP": ("PSA Electronic Payment Instruments channel (registered EPIESP)", "FSA (Japan)"),
    "KR": ("No operative inbound regime (draft DABA)", "FSC (Korea)"),
}
CLASS_LABEL = {
    "I": "Category I (dual authorization available)",
    "II": "Category II (determination / channel required)",
    "III": "Category III (no direct issuance; partnership / coordination route)",
    "blocked": "Blocked at destination (issuance / circulation prohibited)",
    "pre_regime": "Pre-regime (no operative destination regime yet)",
}
# baseline archetype rule (derived; the enriched records may curate these)
def _archetypes(cls):
    if cls in ("I", "II"):
        return ["RC", "SC", "TC", "DC"]
    if cls in ("III", "blocked"):
        return ["RC", "DC"]
    if cls == "pre_regime":
        return ["RC"]
    return ["RC"]


def _cellmap(ds):
    m = {}
    for r in ds["records"]:
        c = r.get("constraint_ref")
        if c:
            m[f"{r['jurisdiction']}.{c}"] = r["id"]
    return m


def build_edge_skeletons():
    import substrate as SUBM
    import compose as SIG
    ds = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
    sub = json.loads((ROOT / "analysis" / "constraint_substrate.json").read_text(encoding="utf-8"))
    cmap = _cellmap(ds)
    id2class = {r["id"]: r["claim_class"] for r in ds["records"]}
    authored = {(c["origin"], c["destination"]) for c in ds.get("corridors", [])}

    skeletons, bad_prov, disagreements = [], [], []
    n_indeterminate = 0
    for o in J12:
        for d in J12:
            if o == d or (o, d) in authored:
                continue
            derived = SUBM.compose_via_substrate(o, d, sub)
            cls = derived.get("class")
            if cls in (None, "indeterminate"):
                n_indeterminate += 1
                continue
            sig = SIG.compose_directed(o, d).get("class")
            if cls != sig:
                disagreements.append(f"{o}->{d}: substrate={cls} signal={sig}")
            test, admin = DEST_MECHANISM.get(d, (None, None))
            # provenance: dest C7 (or C1 for prohibition/pre-regime) + origin C1
            cited = []
            dc7 = cmap.get(f"{d}.C7"); dc1 = cmap.get(f"{d}.C1"); oc1 = cmap.get(f"{o}.C1")
            if cls in ("blocked", "pre_regime"):
                cited += [x for x in (dc1,) if x]
            else:
                cited += [x for x in (dc7, dc1) if x]
            cited += [x for x in (oc1,) if x]
            cited = sorted(set(cited))
            nontier1 = [r for r in cited if id2class.get(r) != "tier1_legal"]
            if nontier1:
                bad_prov.append(f"{o}->{d}: {nontier1}")
            skeletons.append({
                "corridor_id": f"{o.lower()}-{d.lower()}-skeleton",
                "origin": o, "destination": d, "direction": "directed",
                "tier": "computed_skeleton",
                "feasibility_class": CLASS_LABEL.get(cls, cls),
                "class_code": cls,
                "compatibility_pair": "-".join(sorted([o, d])),
                "inbound_mechanism": {"test": test, "administrator": admin, "detail": None},
                "archetypes": _archetypes(cls),
                "interaction_sets": sorted((derived.get("set_verdicts") or {}).keys()),
                "origin_drag": derived.get("rule", "").startswith("origin_drag"),
                "infrastructure_overlap": None,
                "provenance": {"records": cited, "all_tier1_legal": not nontier1},
                "enrichment_status": "computed skeleton — derived fields only",
                "enrichment_backlog": ["infrastructure_overlap", "bespoke_inbound_detail",
                                        "curated_archetypes", "prose_note", "primary_source_verification"],
            })

    out = {
        "schema": "cbsr-analysis/computed_corridor_skeletons",
        "version": "0.9.4", "status": "preview",
        "method": ("For each derivable directed edge without a hand-authored rich corridor record, derive the "
                   "feasibility class (from the substrate), the inbound mechanism test + administrator "
                   "(re-projected from the destination's C1/C7 record), a baseline archetype set, and the "
                   "directed interaction sets. No new facts: empirical fields (infrastructure_overlap, bespoke "
                   "detail, curated archetypes, prose) are left null as a per-edge enrichment backlog. Class is "
                   "cross-checked against the signal compose(); every skeleton cites its backing tier1_legal records."),
        "coverage": {
            "authored_rich_corridors": len(authored),
            "computed_skeletons": len(skeletons),
            "edges_with_a_record": len(authored) + len(skeletons),
            "edges_total": len(J12) * (len(J12) - 1),
            "indeterminate_edges": n_indeterminate,
            "indeterminate_note": "indeterminate edges are those into the UK and Taiwan (inbound gate in transition) that are not origin-dragged — the time engine's domain",
        },
        "cross_check": {"disagreements_with_signal": disagreements, "clean": not disagreements},
        "provenance": {"nontier1_skeletons": bad_prov, "clean": not bad_prov},
        "skeletons": skeletons,
    }
    (ROOT / "analysis" / "computed_corridor_skeletons.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    o = build_edge_skeletons()
    cov = o["coverage"]
    print("wrote analysis/computed_corridor_skeletons.json")
    print(f"  authored rich: {cov['authored_rich_corridors']} | computed skeletons: {cov['computed_skeletons']} | "
          f"edges with a record: {cov['edges_with_a_record']}/{cov['edges_total']} | indeterminate: {cov['indeterminate_edges']}")
    print(f"  cross-check clean={o['cross_check']['clean']}; provenance clean={o['provenance']['clean']}")
    ex = next(s for s in o["skeletons"] if s["origin"] == "EU" and s["destination"] == "JP")
    print(f"  example — EU->JP: {ex['feasibility_class']} | inbound: {ex['inbound_mechanism']['test']} [{ex['inbound_mechanism']['administrator']}] | cites {ex['provenance']['records']}")
