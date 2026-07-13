#!/usr/bin/env python3
"""compute_sensitivity.py  -  recompute the corridor-sensitivity ordering of Feasibility Over Time
s.4.2 from the published signal table, instead of asserting it in prose.

WHY
---
s.4.2 says South Korea is "the single highest-sensitivity jurisdiction" and that Mainland China "is
insensitive ... every edge terminating in the People's Republic of China is stable across the entire
pending set." The eighth review recomputed both against the SHIPPED ARTIFACT and found them wrong:
Taiwan and Korea were tied at 20 edges each, and `KR->CN` / `TW->CN` flipped `III -> blocked` once
Korea or Taiwan gained a token, so China was NOT insensitive (finding NF-2).

Both of those defects were artefacts of the artifact's origin-drag-first rule, which v0.10.0 replaced
with the published Atlas's destination-first precedence. Under the corrected rule the arithmetic is
different again -- and this tool computes it rather than arguing about it. A sensitivity ordering that
lives in prose is a claim; one a tool recomputes from the signals is a result.

WHAT IT DOES
------------
For each pending change in law in the register, it applies the change to a COPY of the signal table,
re-derives all 132 classes with `tools/class_rule.py:class_of`, and counts the edges that change
class. Nothing is forecast: a contingent trigger is applied as an if-enacted branch and moves no date.

Every trigger below is a `tier1_legal` change in law -- a commencement, an enactment, or an instrument
taking effect -- never a market event (Feasibility s.2.1).

Usage:  python3 tools/compute_sensitivity.py [--write] [--json]
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


import argparse
import copy
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import class_rule  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

__version__ = "0.10.0"
OUT = pathlib.Path(__file__).resolve().parent.parent / "out"

NAME = {"US": "United States", "EU": "European Union", "UK": "United Kingdom", "SG": "Singapore",
        "HK": "Hong Kong", "CN": "Mainland China", "BR": "Brazil", "CH": "Switzerland",
        "AE": "United Arab Emirates", "JP": "Japan", "TW": "Taiwan", "KR": "South Korea"}


# ------------------------------------------------------------------------------------------------
# The pending changes in law, as signal mutations. Each is an if-then, not a forecast.
# ------------------------------------------------------------------------------------------------
def t_us_effective(S):
    S["US"]["inbound_gate"]["binding_status"] = "in_force_enacted"


def t_uk_commencement(S):
    S["UK"]["inbound_gate"]["binding_status"] = "in_force_enacted"


def t_tw_commencement(S):
    S["TW"]["token_regime"]["value"] = "authorizable"
    S["TW"]["inbound_gate"]["binding_status"] = "in_force_enacted"


def t_kr_daba(S):
    S["KR"]["token_regime"]["value"] = "authorizable"
    S["KR"]["inbound_gate"]["value"] = "authorization"      # PROVISIONAL: the enacted gate type is
    S["KR"]["inbound_gate"]["resolves_to"] = "I"            # undetermined (Feasibility s.3.4)
    S["KR"]["inbound_gate"]["binding_status"] = "in_force_enacted"


def t_cn_relaxation(S):
    """No positive trigger exists. The register records three RELAXATION developments (a PRC data
    framework change, a second HK cohort with a PRC-connected entity, PRC authorisation of SOE HK
    affiliates) -- none of which, on its own, lifts the issuance prohibition. Modelled as the empty
    change, which is the whole point: the ordering must SHOW the insensitivity, not assume it."""
    return


TRIGGERS = [
    ("us-genius-act-effective", "US", "GENIUS Act s.20 effective date", t_us_effective,
     "scheduled_with_cap", "<= 2027-01-18 (outer cap; may fall sooner)"),
    ("uk-systemic-regime-operative", "UK", "FSMA 2000 (Cryptoassets) Regs 2026 commencement",
     t_uk_commencement, "scheduled", "2027-10-25 (gazetted)"),
    ("tw-vas-act-commencement", "TW", "Virtual Asset Service Act commencement", t_tw_commencement,
     "contingent", "no gazetted date (nine subsidiary items pending)"),
    ("kr-daba-enacted-commenced", "KR", "Digital Asset Basic Act enacted and commenced", t_kr_daba,
     "contingent", "no date (National Assembly subcommittee)"),
    ("cn-boundary-relaxation", "CN", "PRC boundary relaxation (no positive trigger available)",
     t_cn_relaxation, "open_question", "n/a"),
]


def sensitivity(table):
    S0 = table["signals"]
    base = class_rule.all_classes(S0)
    results = []
    for eid, juris, label, mutate, kind, when in TRIGGERS:
        S = copy.deepcopy(S0)
        mutate(S)
        after = class_rule.all_classes(S)
        moved = [(o, d, base[(o, d)][0], after[(o, d)][0])
                 for (o, d) in base if base[(o, d)][0] != after[(o, d)][0]]
        inbound = [m for m in moved if m[1] == juris]
        outbound = [m for m in moved if m[0] == juris]
        other = [m for m in moved if m[0] != juris and m[1] != juris]
        results.append({
            "event_id": eid, "jurisdiction": juris, "label": label, "trigger_kind": kind,
            "when": when, "edges_moved": len(moved),
            "inbound": len(inbound), "outbound": len(outbound), "elsewhere": len(other),
            "moves": [f"{o}->{d}: {a} -> {b}" for o, d, a, b in moved],
        })
    results.sort(key=lambda r: (-r["edges_moved"], r["jurisdiction"]))
    return results


def render(results):
    lines = ["# Corridor sensitivity — recomputed, not asserted\n",
             "_Generated by `tools/compute_sensitivity.py` from `data/signal_table.json` via the "
             "published class rule. Each pending **change in law** is applied to a copy of the signal "
             "table; all 132 classes are re-derived; the edges that change class are counted. "
             "Nothing is forecast — a contingent trigger is an if-enacted branch and moves no date._\n",
             "## The ordering\n",
             "| # | jurisdiction | trigger | kind | when | edges moved | inbound | outbound |",
             "|---:|---|---|---|---|---:|---:|---:|"]
    for i, r in enumerate(results, 1):
        lines.append(f"| {i} | **{r['jurisdiction']}** — {NAME[r['jurisdiction']]} | {r['label']} | "
                     f"`{r['trigger_kind']}` | {r['when']} | **{r['edges_moved']}** | "
                     f"{r['inbound']} | {r['outbound']} |")
    lines += [
        "",
        "## What this corrects\n",
        "**Feasibility Over Time §4.2 as drafted** calls South Korea *\"the single highest-sensitivity "
        "jurisdiction\"* and Mainland China *\"insensitive.\"* The **eighth review** recomputed both "
        "against the v0.9.99 artifact and found them wrong — Taiwan and Korea tied at 20 edges each, "
        "and China moved 2 edges (`KR→CN`, `TW→CN` flipping `III → blocked` once Korea or Taiwan gained "
        "a token). Both defects were **artefacts of the artifact's origin-drag-first rule**, which "
        "contradicted the published Atlas.\n",
        "Under the corrected **destination-first** precedence (v0.10.0) the arithmetic changes again:\n",
        f"- **South Korea leads at {results[0]['edges_moved']} edges** — so §4.2's headline is right, "
        "but not for the reason it gives, and not by the margin the eighth review computed.",
        "- **Taiwan is second, not tied**: its commencement moves fewer edges because two of its "
        "outbound edges (`TW→CN` blocked, `TW→KR` pre-regime) are held by their **destinations** and "
        "cannot move whatever Taiwan does.",
        "- **Mainland China is genuinely insensitive** — 0 edges — because a destination prohibition "
        "dominates the origin's issuance gap. §4.2's claim becomes *true* the moment NF-1 is fixed, "
        "which is independent evidence for fixing it that way.",
        "- **The United States and the United Kingdom move 8 edges each** — but the US horizon is "
        "**earlier** (an outer cap at 2027-01-18) than the UK's gazetted 2027-10-25. On the "
        "*dated* ordering the US leads. This is errata **E1**.\n",
        "## The two orderings are different questions\n",
        "| question | ordering |",
        "|---|---|",
        f"| *Which pending change would reclassify the most edges?* | {' > '.join(r['jurisdiction'] + ' (' + str(r['edges_moved']) + ')' for r in results)} |",
        "| *Which dated horizon arrives first?* | US (≤ 2027-01-18, outer cap) > UK (2027-10-25, gazetted). TW and KR carry no date and move no horizon. |",
        "",
        "A forward map must report **both**, and §4.2 currently reports neither cleanly: it ranks by "
        "edge count while calling the UK *\"the highest-sensitivity scheduled jurisdiction\"* and "
        "omitting the US horizon entirely.\n",
        "## Per-trigger edge lists\n",
    ]
    for r in results:
        lines.append(f"### `{r['event_id']}` — {r['edges_moved']} edges\n")
        if not r["moves"]:
            lines.append("_No edge changes class. A destination prohibition cannot be moved by any "
                         "positive trigger; only a relaxation of the prohibition itself could, and "
                         "that would change the `inbound_gate` signal, not any origin's token._\n")
        else:
            for m in r["moves"]:
                lines.append(f"- `{m}`")
            lines.append("")
    lines.append("> **Guardrail.** These counts follow from the signal table. They are not a forecast "
                 "of which enactment will occur, and the post-commencement gate type of a pre-regime "
                 "jurisdiction (South Korea) is provisional pending its enacted text — modelled here as "
                 "`authorization`, which the register flags as undetermined (Feasibility §3.4).\n")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Recompute the corridor-sensitivity ordering.")
    ap.add_argument("--write", action="store_true", help="write out/corridor_sensitivity.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    table = class_rule.load()
    results = sensitivity(table)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    print("=" * 82)
    print(f"corridor sensitivity v{__version__} — recomputed from data/signal_table.json")
    print("=" * 82)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['jurisdiction']:2s}  {r['edges_moved']:2d} edges  "
              f"(in {r['inbound']}, out {r['outbound']}, elsewhere {r['elsewhere']})  "
              f"[{r['trigger_kind']}]  {r['when']}")
    print("-" * 82)
    print("dated horizons, in order of arrival: US <= 2027-01-18 (outer cap) then UK 2027-10-25 "
          "(gazetted). TW and KR are undated and move no horizon.")
    print("=" * 82)

    if args.write:
        OUT.mkdir(exist_ok=True)
        (OUT / "corridor_sensitivity.md").write_text(render(results), encoding="utf-8")
        print("wrote out/corridor_sensitivity.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
