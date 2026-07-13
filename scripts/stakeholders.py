#!/usr/bin/env python3
"""Atlas §8 stakeholder projection. profile_for(stakeholder, origin, dest) re-projects the already-derived
corridor class + substrate poles + inbound mechanism through a persona's lens. It adds no new legal facts:
every line it shows is read from an existing record, every profile cites its backing tier1_legal records,
and the profile inherits the verification status of the cells it reads (preview until verified). Emits
analysis/computed_stakeholder_profiles.json (worked profiles for the authored corridors x all personas)."""
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

DB = json.loads((ROOT / "analysis" / "stakeholder_database.json").read_text(encoding="utf-8"))
SUB = json.loads((ROOT / "analysis" / "constraint_substrate.json").read_text(encoding="utf-8"))

# short, persona-neutral implication of each (constraint, pole) — purely a re-reading of the pole
IMPLICATION = {
    "C1": {"open": "issuance open", "licence_gated": "issuance is authorization-gated",
           "closed_set": "issuance limited to a defined set of entities",
           "host_currency_first": "host-currency issuance prioritized",
           "no_pathway": "no operative issuance pathway yet", "prohibition": "issuance prohibited"},
    "C2": {"prescribed_hqla": "reserve must be high-quality liquid assets",
           "prescribed_flex": "reserve prescribed with some flexibility",
           "informational": "reserve disclosure only"},
    "C3": {"permitted": "yield permitted", "prohibited_issuer": "issuer may not pay yield",
           "prohibited_incl_agents": "issuer and agents may not pay yield",
           "silent": "yield treatment unsettled"},
    "C4": {"payment_instrument": "treated as a payment instrument, not a security",
           "contested_routing": "classification turns on the routing structure",
           "security": "treated as a security / unauthorized offering"},
    "C5": {"bank_only": "bank-only issuance", "bank_and_nonbank": "bank and non-bank issuers admitted",
           "layered_separation": "roles separated by licensed function", "unset": "routing architecture unsettled"},
    "C6": {"open": "no data-localization barrier to supervisory sharing",
           "transfer_gated": "cross-border transfer is gated", "localized": "data localization applies",
           "restrictive": "data sharing restricted"},
    "C7": {"open": "no usage cap; dual authorization available", "usage_capped": "scale / usage capped",
           "channelled": "foreign tokens admitted only via a determination / channel",
           "prohibition": "foreign tokens prohibited"},
    "C8": {"coordinated": "supervisory coordination available", "constrained": "supervisory coordination constrained"},
}
CONSTRAINT_NAME = {"C1": "issuer eligibility", "C2": "reserve/capital", "C3": "yield", "C4": "securities classification",
                   "C5": "bank/non-bank routing", "C6": "cross-border/data", "C7": "monetary sovereignty",
                   "C8": "disclosure/supervisory"}


def _records():
    return json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))["records"]


def _corridor_record(o, d, ds):
    for c in ds.get("corridors", []):
        if c.get("origin") == o and c.get("destination") == d:
            return c
    return None


def _pole_reading(j, c):
    """Return (pole, record_id, implication) for jurisdiction j, constraint c — or None if unset."""
    cell = SUB.get("cells", {}).get(j, {}).get(c)
    if not cell:
        return None
    pole = cell.get("pole")
    rid = (cell.get("derived_from") or [None])[0]
    impl = IMPLICATION.get(c, {}).get(pole, pole)
    return {"side_constraint": c, "constraint_name": CONSTRAINT_NAME.get(c), "pole": pole,
            "record": rid, "implication": impl}


def profile_for(stakeholder: str, origin: str, dest: str, ds=None):
    import substrate as SUBM
    import compose as SIG
    s = DB["stakeholders"].get(stakeholder)
    if s is None:
        return {"error": f"unknown stakeholder '{stakeholder}'", "known": sorted(DB["stakeholders"])}
    o, d = origin.upper(), dest.upper()
    ds = ds or json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))

    derived = SUBM.compose_via_substrate(o, d, SUB)
    cls = derived.get("class")
    sig = SIG.compose_directed(o, d).get("class")

    reading, cited = [], []
    for side, j in (("origin", o), ("dest", d)):
        for c in s["reads"].get(side, []):
            r = _pole_reading(j, c)
            if r is None:
                reading.append({"side": side, "jurisdiction": j, "side_constraint": c,
                                "constraint_name": CONSTRAINT_NAME.get(c), "pole": None,
                                "implication": "pole unset — indeterminate at the substrate level"})
            else:
                reading.append({"side": side, "jurisdiction": j, **r})
                if r["record"]:
                    cited.append(r["record"])

    corr = _corridor_record(o, d, ds)
    archetypes_engaged = sorted(set(s["archetypes"]) & set(corr.get("archetypes", []))) if corr else s["archetypes"]
    inbound = corr.get("inbound_mechanism") if corr else None

    # verification status: how many cited cells are NOT yet citable (resolution_text)
    id2tier = {r["id"]: r.get("evidence_tier") for r in ds["records"]}
    id2class = {r["id"]: r["claim_class"] for r in ds["records"]}
    cited = sorted(set(cited))
    unverified = [rid for rid in cited if id2tier.get(rid) != "resolution_text"]
    nontier1 = [rid for rid in cited if id2class.get(rid) != "tier1_legal"]

    # a persona-specific headline built from the class + the most salient pole the persona reads
    caveat = ""
    if cls in (None, "indeterminate"):
        caveat = " (corridor class is indeterminate at the substrate level — in transition; see the time engine)"
    headline = _headline(stakeholder, o, d, cls if cls else "indeterminate", reading) + caveat

    return {
        "edge": f"{o}->{d}", "stakeholder": stakeholder, "label": s["label"], "lens": s["lens"],
        "corridor_class": cls if cls else "indeterminate", "signal_class": sig,
        "agree_with_signal": (cls == sig) if (cls and cls != "indeterminate") else None,
        "archetypes_engaged": archetypes_engaged,
        "inbound_mechanism": inbound,
        "headline": headline,
        "reading": reading,
        "provenance": {"records": cited, "all_tier1_legal": not nontier1, "nontier1": nontier1},
        "verification_status": (f"preview — rests on {len(cited)} cell(s), {len(unverified)} not yet verified "
                                f"to resolution_text; profile is not citable authority until those are verified"),
    }


def _headline(stakeholder, o, d, cls, reading):
    by = {(r["side"], r["side_constraint"]): r for r in reading}
    cl = {"I": "broadly feasible (Category I)", "II": "feasible pending a determination (Category II)",
          "III": "not directly feasible; partnership/coordination route (Category III)",
          "blocked": "blocked", "pre_regime": "no operative destination regime yet (pre-regime)",
          "T": "in transition", "indeterminate": "indeterminate"}.get(cls, cls)
    if stakeholder == "issuer":
        oc1 = by.get(("origin", "C1"), {}).get("implication", "?")
        return f"As an {o} issuer, {oc1}; entry into {d} is {cl}."
    if stakeholder == "host_regulator":
        dc7 = by.get(("dest", "C7"), {}).get("implication", "?")
        return f"As the {d} (host) regulator: foreign tokens — {dc7}; the corridor is {cl}."
    if stakeholder == "home_regulator":
        oc6 = by.get(("origin", "C6"), {}).get("implication", "?")
        return f"As the {o} (home) regulator: {oc6}; supervising outbound use into {d}, the corridor is {cl}."
    if stakeholder == "distributor":
        dc5 = by.get(("dest", "C5"), {}).get("implication", "?")
        return f"As a distributor/wallet into {d}: {dc5}; the corridor is {cl}."
    if stakeholder == "corporate_treasury":
        dc7 = by.get(("dest", "C7"), {}).get("implication", "?")
        return f"As a corporate treasury using the {o}->{d} rail: {dc7}; feasibility is {cl}."
    if stakeholder == "token_holder":
        dc4 = by.get(("dest", "C4"), {}).get("implication", "?")
        return f"As an institutional holder in {d}: {dc4}; the corridor is {cl}."
    if stakeholder == "reserve_custodian":
        oc2 = by.get(("origin", "C2"), {}).get("implication", "?")
        return f"As reserve custodian for the {o} issuer: {oc2}; the corridor is {cl}."
    return f"{stakeholder} view of {o}->{d}: {cl}."


def build_stakeholder_projections():
    ds = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
    corridors = [(c["origin"], c["destination"]) for c in ds.get("corridors", [])]
    personas = list(DB["stakeholders"].keys())
    profiles, all_cited, bad_prov = [], set(), []
    for (o, d) in corridors:
        for p in personas:
            pr = profile_for(p, o, d, ds)
            profiles.append(pr)
            all_cited.update(pr["provenance"]["records"])
            if not pr["provenance"]["all_tier1_legal"]:
                bad_prov.append(f"{pr['edge']}/{p}: {pr['provenance']['nontier1']}")
    # provenance cross-check: every cited record exists and is tier1_legal
    ids = {r["id"] for r in ds["records"]}
    missing = sorted(r for r in all_cited if r not in ids)
    out = {
        "schema": "cbsr-analysis/computed_stakeholder_profiles",
        "version": DB["version"], "status": "preview",
        "method": ("profile_for(stakeholder, edge) re-projects the derived corridor class, the substrate poles, "
                   "and the edge inbound mechanism through each Atlas \u00a78 persona. No new legal facts: every "
                   "line is read from an existing record and every profile cites its backing tier1_legal records. "
                   "Profiles are preview and inherit the verification status of the cells they read."),
        "personas": personas,
        "corridors_projected": [f"{o}->{d}" for (o, d) in corridors],
        "provenance": {"records_cited": len(all_cited), "missing_records": missing,
                       "nontier1_profiles": bad_prov, "clean": (not missing and not bad_prov)},
        "profiles": profiles,
    }
    (ROOT / "analysis" / "computed_stakeholder_profiles.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    o = build_stakeholder_projections()
    print("wrote analysis/computed_stakeholder_profiles.json")
    print(f"  {len(o['profiles'])} profiles over {len(o['corridors_projected'])} corridors x {len(o['personas'])} personas")
    print(f"  provenance: {o['provenance']['records_cited']} records cited; clean={o['provenance']['clean']}"
          + ("" if o["provenance"]["clean"] else f" — issues {o['provenance']['missing_records']} {o['provenance']['nontier1_profiles'][:2]}"))
    # show one worked projection
    ex = profile_for("issuer", "US", "EU")
    print(f"  example — issuer US->EU: {ex['headline']}")
    print(f"            cites {ex['provenance']['records']}")
