#!/usr/bin/env python3
"""build_settlement.py — the settlement-substrate bloc layer (Atlas §5.2, Tier-2 enrichment).

The flagship §5.2 correction is not "Ensemble is not BIS" but the checkable structural claim that the
wholesale settlement substrate is split along geopolitical bloc lines: open within a bloc, closed across
blocs. This layer encodes that structure — the three experiments with their true operators, and each of
the twelve jurisdictions' bloc membership — transcribed from §5.2 and the public membership of each
experiment, then computes the per-edge `infrastructure_overlap` the paper asks for: for every directed
corridor, whether both ends sit on the same bloc-internal substrate, on opposite blocs, or off the shared
experiments entirely (with Hong Kong's Ensemble bridging position marked separately).

EVIDENCE TIER. §5.1/§5.2/§5.4 state plainly that the settlement-substrate reading rests on softer evidence
than §3 — the public central-bank project literature, forward-looking as to interaction with the private
issuance layer — and that `infrastructure_overlap` is a Tier-2 OPERATIONAL enrichment attribute, not a
proposition of law. This layer is emitted with claim_class=tier2_operational accordingly, and NO
feasibility-class conclusion in §§3-4 depends on it. It is structural context, not citable legal fact.
"""
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
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "TW", "JP", "KR"]

# --- transcribed from §5.2 + the public membership of each experiment --------------------------
EXPERIMENTS = {
    "agora": {
        "name": "Project Agorá",
        "lead": "Bank for International Settlements",
        "bloc": "Agorá-participant (dollar-routing)",
        "settlement_currency_orientation": "dollar-routing (tokenized-correspondent; keeps value in the dollar-centred correspondent structure)",
        "bis_led": True,
        "participants_note": "BIS together with seven Agorá-participant central banks (a dollar-routing, G7-anchored but not G7-only group: the Agorá members among the twelve are the United States, the euro area, the United Kingdom, Japan, Korea, and Switzerland) and 40+ private financial institutions",
        "focus_members": ["US", "EU", "UK", "JP", "KR", "CH"],  # of the twelve; the 7th (Bank of Mexico) is out of scope
    },
    "mbridge": {
        "name": "mBridge",
        "lead": "People's Bank of China, Hong Kong Monetary Authority, and the central banks of Thailand, the United Arab Emirates, and Saudi Arabia",
        "bloc": "PRC-and-Gulf",
        "settlement_currency_orientation": "dollar-bypass (settles across monetary areas without the dollar leg; majority of settlement volume reported in digital yuan)",
        "bis_led": False,
        "bis_withdrew": "2024-10-31",
        "participants_note": "no BIS and no Western central bank among operators since the BIS withdrawal on 31 Oct 2024",
        "focus_members": ["CN", "AE", "HK"],  # HKMA is an mBridge operator
    },
    "ensemble": {
        "name": "Project Ensemble",
        "lead": "Hong Kong Monetary Authority",
        "bloc": "bridge",
        "launched": "2024-03",
        "bis_led": False,
        "role": "sits in the bridging position between the two blocs (not a BIS project)",
        "focus_members": ["HK"],
    },
}

# per-jurisdiction bloc membership (the substrate a jurisdiction's wholesale rail belongs to)
BLOC = {
    "US": "agora", "EU": "agora", "UK": "agora", "JP": "agora", "KR": "agora", "CH": "agora",
    "CN": "mbridge", "AE": "mbridge",
    "HK": "bridge",   # HKMA both operates mBridge and leads the bridging Ensemble
    "BR": "none", "SG": "none", "TW": "none",
}


def overlap(a, b):
    """Per-edge infrastructure_overlap: same-bloc / cross-bloc / bridge / off-experiments."""
    ba, bb = BLOC[a], BLOC[b]
    if ba == "none" or bb == "none":
        return "off-experiments", "at least one end is in no named settlement experiment"
    if "bridge" in (ba, bb):
        other = bb if ba == "bridge" else ba
        if other == "mbridge":
            return "same-bloc:mBridge", "Hong Kong operates mBridge alongside this end"
        # other == agora  (or bridge-bridge, impossible with one HK)
        return "bridge", "Hong Kong's Ensemble sits in the bridging position toward the Agorá-participant (dollar-routing) bloc"
    if ba == bb:
        label = "Agorá" if ba == "agora" else "mBridge"
        return f"same-bloc:{label}", f"both ends sit on the {label} bloc-internal substrate"
    return "cross-bloc", "opposite blocs: Agorá (dollar-routing) vs mBridge (dollar-bypass); memberships do not overlap and the rails are not mutually interoperable"


def build():
    edges = []
    counts = {}
    for a, b in combinations(J12, 2):
        cls, why = overlap(a, b)
        edges.append({"pair": f"{a}-{b}", "infrastructure_overlap": cls,
                      "blocs": {a: BLOC[a], b: BLOC[b]}, "basis": why})
        counts[cls] = counts.get(cls, 0) + 1

    out = {
        "schema": "cbsr-analysis/computed_settlement",
        "version": "v0.9.9",
        "generated": date.today().isoformat(),
        "claim_class": "tier2_operational",
        "evidence_tier": "operational_enrichment",
        "method": ("The three wholesale-settlement experiments are recorded with their true operators (the §5.2 "
                   "correction), each of the twelve jurisdictions is assigned to the bloc-internal substrate its "
                   "rail belongs to, and every undirected corridor is then classified by whether its two ends sit "
                   "on the same bloc substrate, on opposite blocs, on the Ensemble bridge, or off the shared "
                   "experiments. The per-edge classification is deterministic given the public memberships."),
        "correction": ("The earlier draft attributed all three experiments to the BIS, which was wrong. Only Project "
                       "Agorá is BIS-led; Project Ensemble is HKMA-led; and mBridge has not been a BIS project since "
                       "the BIS withdrew on 31 Oct 2024, and is now operated by a PRC-and-Gulf group with the majority "
                       "of settlement volume in digital yuan. The true operators are what reveal the bloc structure."),
        "experiments": EXPERIMENTS,
        "bloc_membership": BLOC,
        "edges": edges,
        "counts": counts,
        "finding": ("The settlement substrate is not a single shared open rail but two bloc-internal rails — a "
                    "dollar-routing rail (Project Agorá, the Agorá-participant bloc) and a dollar-bypass rail (mBridge, PRC-and-Gulf) "
                    "— each open to its own members and closed across the divide, with Hong Kong's Project Ensemble "
                    "in the bridging position. The partition is visible at the level of individual corridors."),
        "evidence_note": ("Tier-2, operational-grade structural context, NOT a proposition of law. Per §5.1/§5.4 this "
                          "reading rests on the public central-bank project literature (reliable as to the existence "
                          "and design of the experiments, forward-looking as to their interaction with the private "
                          "issuance layer). No feasibility-class conclusion in §§3-4 depends on this layer; it is "
                          "tracked as a per-edge enrichment attribute, consistent with the register's own tiering."),
        "provenance": {
            "clean": True,
            "asserts_new_facts": False,
            "source": "Feasibility-Over-Time paper §5.2 (the bifurcation, corrected) + the public membership of each experiment",
            "note": "Bloc memberships are transcribed from §5.2 and public central-bank announcements; per-edge overlaps are computed from them.",
        },
    }
    (ROOT / "analysis" / "computed_settlement.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote analysis/computed_settlement.json")
    print(f"  per-edge infrastructure_overlap over 66 corridors: {counts}")
    print(f"  Agorá={EXPERIMENTS['agora']['focus_members']}  mBridge={EXPERIMENTS['mbridge']['focus_members']}  "
          f"bridge=['HK']  off-experiments=['BR', 'SG', 'TW']")


if __name__ == "__main__":
    build()
