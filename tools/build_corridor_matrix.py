#!/usr/bin/env python3
"""build_corridor_matrix.py  —  make the full 12x12 directed corridor graph legible.

Reads analysis/computed_corridors_directed.json (the 132-edge layer) and writes three views
into out/ that turn "every jurisdiction bridges to every other" from a claim into something a
reader can SEE and a spreadsheet can consume:

  1. out/corridor_matrix.md          a 12x12 grid: row = origin, col = destination, cell = class
  2. out/corridor_matrix.csv         the same grid as CSV (origin rows x destination columns)
  3. out/corridor_per_jurisdiction.md the supervisor view: for each jurisdiction, its outbound
                                      and inbound edges grouped by class, with counterpart lists

Zero third-party dependencies (json, csv, pathlib, sys only). No pip install.

Usage:  python3 tools/build_corridor_matrix.py [path/to/computed_corridors_directed.json]
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

import sys, json, csv, pathlib
from collections import defaultdict, Counter

__version__ = "0.10.0"

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DEFAULT = ROOT / "analysis" / "computed_corridors_directed.json"
OUT = ROOT / "out"

J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "JP", "TW", "KR"]
NAME = {"US": "United States", "EU": "European Union", "UK": "United Kingdom",
        "SG": "Singapore", "HK": "Hong Kong", "CN": "Mainland China", "BR": "Brazil",
        "CH": "Switzerland", "AE": "United Arab Emirates", "JP": "Japan",
        "TW": "Taiwan", "KR": "South Korea"}
# short cell codes for the grid (kept ASCII-wide-safe for Markdown alignment)
CELL = {"I": "I", "II": "II", "III": "III", "T": "T", "blocked": "BLK", "pre_regime": "PRE"}
LEGEND = [
    ("I",   "Category I — dual authorization available (each end separately authorizable)"),
    ("II",  "Category II — equivalence / recognition / channel determination required"),
    ("III", "Category III — composition unresolved (origin has no exportable authorizable token)"),
    ("T",   "Regime-in-transition — destination regime adopted but not yet operative"),
    ("BLK", "Blocked — destination issuance prohibition"),
    ("PRE", "Pre-regime — destination has no issuance pathway yet"),
    ("—",   "no self-edge (a jurisdiction is not a corridor with itself)"),
]


def load(path):
    doc = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    by_pair = {(e["origin"], e["destination"]): e for e in doc["edges"]}
    return doc, by_pair


def write_matrix_md(doc, by_pair, src: pathlib.Path = None):
    dist = Counter(e["class_code"] for e in doc["edges"])
    lines = []
    lines.append("# Directed corridor matrix — all 12 x 11 = 132 ordered pairs\n")
    src_name = (src or DEFAULT).name
    lines.append(f"_Generated from `{src_name}` (schema `{doc.get('schema')}`, "
                 f"generated {doc.get('generated')})._\n")
    lines.append("Every jurisdiction bridges to every other: **all 132 ordered pairs carry a "
                 "directed-edge record.** Read a row as \"value leaving this origin\"; read a column "
                 "as \"value entering this destination.\"\n")
    lines.append("Each cell is **derived, not authored**: `tools/class_rule.py` applies the Corridor "
                 "Atlas v0.2.5 **destination-first precedence** to `data/signal_table.json` —\n")
    lines.append("> destination prohibition **>** destination pre-regime **>** origin drag **>** "
                 "destination in transition **>** the destination's operative gate type\n")
    lines.append("`tools/recompute_classes.py --trace` reproduces every cell and prints which "
                 "precedence step decided it (`out/derivation_trace.md`).\n")
    # header
    header = "| origin \\ dest |" + "|".join(f" **{d}** " for d in J12) + "|"
    sep = "|---|" + "|".join([":---:"] * len(J12)) + "|"
    lines.append(header)
    lines.append(sep)
    for o in J12:
        row = [f"| **{o}** |"]
        for d in J12:
            if o == d:
                row.append(" — |")
            else:
                e = by_pair.get((o, d))
                row.append(f" {CELL.get(e['class_code'], '?')} |")
        lines.append("".join(row))
    lines.append("")
    # legend
    lines.append("## Legend\n")
    for code, desc in LEGEND:
        lines.append(f"- **{code}** — {desc}")
    lines.append("")
    # distribution
    lines.append("## Class distribution (of 132)\n")
    lines.append("| class | count | what it means for the operator |")
    lines.append("|---|---:|---|")
    meaning = {
        "I": "operable now, dual authorization, no equivalence step",
        "II": "operable now, but only through a recognition / comparability / channel determination",
        "III": "not a clean issuance corridor — origin lacks an exportable token; partnership/coordination only",
        "T": "pathway defined but not yet open (destination regime adopted, awaiting commencement)",
        "blocked": "destination prohibits foreign stablecoin circulation",
        "pre_regime": "destination has no issuance-authorization regime to receive into yet",
    }
    for code in ["I", "II", "III", "T", "blocked", "pre_regime"]:
        lines.append(f"| {CELL[code]} | {dist.get(code,0)} | {meaning[code]} |")
    lines.append(f"| **total** | **{sum(dist.values())}** | |")
    lines.append("")
    lines.append("> **Reading the matrix honestly.** A complete graph does not mean every pair is "
                 "operable today. The register's value is that it says *which* pairs are open (I), "
                 "channelled (II), unresolved (III), pending (T), blocked (BLK), or pre-regime (PRE) "
                 "— and *why*. The blocked column (into CN), the pre-regime column (into KR), and the "
                 "III cells (out of CN/TW/KR) are facts of law, not gaps in coverage.\n")
    lines.append("> **Two columns are wholly `T`.** Into the **UK** (regime made, commencing "
                 "2027-10-25) and into the **US** (GENIUS Act enacted 2025-07-18, effective on the "
                 "earlier of 2027-01-18 or final rules + 120 days — §20). The US was coded `II` "
                 "through v0.9.99, i.e. as a live inbound gate, which is the error the register's own "
                 "`VB-06` identified and v0.10.0 corrected. There are **two** dated horizons, and the "
                 "US one comes first.\n")
    lines.append("> **Four cells look like exceptions and are not.** `TW→CN` and `KR→CN` are **BLK**, "
                 "and `CN→KR` and `TW→KR` are **PRE**, even though all four leave a tokenless origin. "
                 "A destination prohibition and a destination pre-regime absence rank *above* origin "
                 "drag: no origin-side token, present or future, completes a corridor into a "
                 "jurisdiction that bans the instrument or has nothing to receive it. Those four read "
                 "`III` — *\"partnership / coordination route\"* — through v0.9.99.\n")
    (OUT / "corridor_matrix.md").write_text("\n".join(lines), encoding="utf-8")


def write_matrix_csv(by_pair):
    with (OUT / "corridor_matrix.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["origin\\dest"] + J12)
        for o in J12:
            row = [o]
            for d in J12:
                row.append("" if o == d else by_pair[(o, d)]["class_code"])
            w.writerow(row)


def write_per_jurisdiction(doc, by_pair):
    outbound = defaultdict(list)   # origin -> list of edges
    inbound = defaultdict(list)    # destination -> list of edges
    for e in doc["edges"]:
        outbound[e["origin"]].append(e)
        inbound[e["destination"]].append(e)

    def group(edges, key_end):
        g = defaultdict(list)
        for e in edges:
            g[e["class_code"]].append(e[key_end])
        return g

    lines = ["# Per-jurisdiction corridor view (the supervisor's cut)\n"]
    lines.append("For each of the twelve jurisdictions: the corridors **out of** it (its edges as "
                 "origin) and **into** it (its edges as destination), grouped by feasibility class. "
                 "This is the same 132 edges as the matrix, re-sorted to answer a supervisor's "
                 "question — *which corridors touch my jurisdiction, and to/from whom* — rather than "
                 "the analyst's *what is moving across the whole space*.\n")
    order = ["I", "II", "III", "T", "blocked", "pre_regime"]
    for j in J12:
        lines.append(f"## {j} — {NAME[j]}\n")
        out_g = group(outbound[j], "destination")
        in_g = group(inbound[j], "origin")
        lines.append(f"**Outbound** ({len(outbound[j])} edges — value leaving {j}):")
        for c in order:
            if out_g.get(c):
                lines.append(f"- **{CELL[c]}** → {', '.join(sorted(out_g[c]))}")
        lines.append("")
        lines.append(f"**Inbound** ({len(inbound[j])} edges — value entering {j}):")
        for c in order:
            if in_g.get(c):
                lines.append(f"- **{CELL[c]}** ← {', '.join(sorted(in_g[c]))}")
        lines.append("")
    (OUT / "corridor_per_jurisdiction.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv):
    path = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT
    OUT.mkdir(exist_ok=True)
    doc, by_pair = load(path)
    write_matrix_md(doc, by_pair, path)
    write_matrix_csv(by_pair)
    write_per_jurisdiction(doc, by_pair)
    dist = Counter(e["class_code"] for e in doc["edges"])
    print(f"wrote out/corridor_matrix.md, out/corridor_matrix.csv, out/corridor_per_jurisdiction.md")
    print(f"  {len(doc['edges'])} edges | class distribution: {dict(sorted(dist.items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
