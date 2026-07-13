#!/usr/bin/env python3
"""Build analysis/verification_worklist.json (v0.9.2): turn the 'unset evidence_tier' liability into a
precise, per-cell, machine-readable worklist for the primary-source verification pass.

This does NOT verify anything (verification requires the official text, which is external work and must
never be fabricated). It inventories, for every unverified record, exactly what is missing to reach the
next evidence tier and what instrument/pinpoint to check against — so the external pass is scoped, not
guessed. Run before build.py; build.py validates and embeds the artifact.
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
import collections

ROOT = pathlib.Path(__file__).resolve().parent.parent

# what each tier needs that 'unset' lacks (necessary conditions; see build.check_evidence_tier_requirements)
_TIER_NEEDS = {
    "firm_summary": ["practitioner/law-firm corroboration of the load-bearing point"],
    "mixed": ["source.url (official-text pointer)", "confirmation of the core point against the text at source.pinpoint"],
    "resolution_text": ["source.url (official-text pointer)",
                         "confirmation against the official statutory/normative text at source.pinpoint",
                         "last_reviewed (date of the text check)"],
}


def build_worklist():
    import yaml
    items, by_juris, by_constraint = [], collections.Counter(), collections.Counter()
    total_tier1_unset = 0
    for f in sorted(ROOT.glob("*.yaml")):
        if f.name == "_TEMPLATE.yaml":
            continue
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(d, dict) or not d.get("id"):
            continue
        if d.get("evidence_tier"):
            continue  # already tiered
        src = d.get("source") or {}
        is_legal = d.get("claim_class") == "tier1_legal"
        if is_legal:
            total_tier1_unset += 1
            by_juris[d.get("jurisdiction")] += 1
            if d.get("constraint_ref"):
                by_constraint[d["constraint_ref"]] += 1
        has_url = bool(src.get("url"))
        # the gap to each tier given what the record already has
        missing = {}
        for tier, needs in _TIER_NEEDS.items():
            gap = []
            for n in needs:
                if n.startswith("source.url") and has_url:
                    continue
                if n.startswith("last_reviewed") and d.get("last_reviewed"):
                    continue
                gap.append(n)
            missing[tier] = gap
        items.append({
            "id": d["id"], "jurisdiction": d.get("jurisdiction"), "constraint_ref": d.get("constraint_ref"),
            "dimension": d.get("dimension"), "claim_class": d.get("claim_class"), "status": d.get("status"),
            "instrument": src.get("primary"), "pinpoint": src.get("pinpoint"), "has_url": has_url,
            "missing_for": missing,
            "recommended_next_tier": ("resolution_text" if is_legal else "firm_summary"),
        })

    out = {
        "schema": "cbsr-analysis/verification_worklist",
        "version": "0.9.4",
        "status": "preview",
        "note": ("Per-cell gap analysis for the primary-source verification pass. Verification itself is "
                 "external work (confirming each claim against the official text) and is never fabricated; "
                 "this artifact scopes that work. The liability it tracks is the same one stated since "
                 "v0.7: every compose()/substrate result rests on these still-unverified cells, and the "
                 "constraint substrate stays dark for a corridor until the relevant cells are verified."),
        "headline": {
            "tier1_legal_unverified": total_tier1_unset,
            "all_unverified_lack_url": all(not it["has_url"] for it in items if it["claim_class"] == "tier1_legal"),
            "by_jurisdiction": dict(sorted(by_juris.items(), key=lambda kv: (-kv[1], kv[0]))),
            "by_constraint": dict(sorted(by_constraint.items())),
        },
        "tier_requirements": _TIER_NEEDS,
        "items": items,
    }
    (ROOT / "analysis" / "verification_worklist.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    o = build_worklist()
    print("wrote analysis/verification_worklist.json")
    h = o["headline"]
    print(f"  tier1_legal cells unverified: {h['tier1_legal_unverified']} "
          f"(all lacking source.url: {h['all_unverified_lack_url']})")
    print(f"  by jurisdiction: {h['by_jurisdiction']}")
    print(f"  by constraint:   {h['by_constraint']}")
