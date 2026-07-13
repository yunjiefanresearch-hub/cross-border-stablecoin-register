#!/usr/bin/env python3
"""recompute_classes.py  -  derive all 132 corridor classes from data/signal_table.json and diff
them against the shipped artifact.

WHAT THIS CLOSES
----------------
Three audit findings shared one root cause: the corridor `class_code`s arrived as a finished column,
and the rule that produced them lived upstream and unpublished.

  F2    the class is a pure function of the destination for 99 of 132 edges -- but *why* each
        destination resolves to its class was opaque.
  F6    the verifier re-implemented the partition from constants HAND-COPIED out of the builder.
        A hand-copy is not an independent check, only a synchronized one.
  NF-1  the rule the artifact actually applied (origin-drag-first) CONTRADICTED the package's own
        published Corridor Atlas (destination-first), and no gate could see it, because OD1 encoded
        the rule as an axiom and CD1 laundered the deviation into a "declared delta".

`docs/PROPOSAL_signal_table.md` designed the fix and then declined to implement it downstream, on
the ground that a table reverse-engineered from the current classes would "bake in the very US=II
classification F1 says is wrong" and offer a false independence. That objection is correct and it
is why this table was written from the PRIMARY-SOURCE LEGAL FACTS instead -- after which it
disagreed with the v0.9.99 artifact on 12 of 132 edges. Those 12 edges were then corrected in the
ARTIFACT, not in the table. A signal table that agrees with the artifact by construction proves
nothing; one that overturns it proves the recompute is real.

WHAT IT CHECKS
--------------
  SIG1  signal-provenance (Citable by Construction s.4.2): every signal `class_of` reads is
        `tier1_legal`; `token_in_issue` is `tier2_operational` and carries no binding_status.
  SIG2  binding-status cap (s.3.1/s.4.2): a signal at `resolution_text` must be `in_force_enacted`.
        This is the gate that keeps the US and UK inbound gates out of the top provenance tier --
        and therefore the gate that PRODUCES the US -> `T` reclassification.
  SIG3  every tier1_legal signal names a non-empty `instrument`.
  PR1   `class_of(origin, destination)` over the table reproduces all 132 `class_code`s, all
        `class_basis.rule`s, and every `as_of_timeline` `resolves_to`, exactly.
  TIER2 INERTNESS  with `--prove-tier2-inert`: flip every `token_in_issue` market signal (and every
        settlement-bloc membership) and assert not one class moves. The signal-provenance guarantee
        is then demonstrated, not merely asserted.

Standard library only. Writes nothing unless `--trace` is given.

Usage:
    python3 tools/recompute_classes.py                    # PR1 + SIG1/2/3
    python3 tools/recompute_classes.py --prove-tier2-inert
    python3 tools/recompute_classes.py --trace            # also write out/derivation_trace.md
    python3 tools/recompute_classes.py --json
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
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import class_rule  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

__version__ = "0.10.0"

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
ARTIFACT = ROOT / "analysis" / "computed_corridors_directed.json"
TABLE = ROOT / "analysis" / "signal_table.json"
OUT = ROOT / "out"

RULE_LABEL = {
    "destination_prohibition":   "1. destination prohibition",
    "destination_no_regime":     "2. destination has no regime",
    "origin_drag":               "3. origin drag (no authorizable token in law)",
    "destination_in_transition": "4. destination regime adopted, not operative",
    "destination_gate":          "5. destination's operative gate type",
}


def recompute(table, artifact):
    """Return (violations, per_edge_rows)."""
    S = table["signals"]
    by_pair = {(e["origin"], e["destination"]): e for e in artifact["edges"]}
    bad, rows = [], []

    for o in class_rule.J12:
        for d in class_rule.J12:
            if o == d:
                continue
            want_cls, want_rule = class_rule.class_of(o, d, S)
            e = by_pair.get((o, d))
            if e is None:
                bad.append(f"PR1 {o}->{d}: edge absent from the artifact")
                continue
            if e["class_code"] != want_cls:
                bad.append(f"PR1 {o}->{d}: artifact says {e['class_code']!r}, the published rule "
                           f"over signal_table.json says {want_cls!r}")
            cb = e.get("class_basis") or {}
            if cb.get("rule") != want_rule:
                bad.append(f"PR1 {o}->{d}: class_basis.rule {cb.get('rule')!r} != {want_rule!r}")
            if cb.get("instrument") != class_rule.instrument_for(o, d, want_rule, S):
                bad.append(f"PR1 {o}->{d}: class_basis.instrument drifted from the signal table")
            tl = e.get("as_of_timeline")
            if want_cls == "T":
                rt = class_rule.resolves_to(d, S)
                events = list((tl or {}).get("scheduled", [])) + list((tl or {}).get("contingent", []))
                for ev in events:
                    if ev.get("resolves_to") != rt:
                        bad.append(f"PR1 {o}->{d}: trigger resolves_to {ev.get('resolves_to')!r} != "
                                   f"the gate's own class {rt!r}")
            rows.append((o, d, want_cls, want_rule, cb.get("governing_jurisdiction"),
                         cb.get("signal"), cb.get("signal_value"), cb.get("binding_status"),
                         cb.get("evidence_tier")))
    return bad, rows


def prove_tier2_inert(table):
    """Flip every tier2_operational input and assert the class function is unmoved.

    This is the empirical form of the signal-provenance guarantee (NF-3). If a class ever moved, a
    market fact would be driving a proposition of law -- the single most consequential error a legal
    reference can make (Citable by Construction s.2.1).
    """
    S = table["signals"]
    base = class_rule.all_classes(S)

    poisoned = copy.deepcopy(table)
    touched = 0
    for j, row in poisoned["signals"].items():
        tii = row.get("token_in_issue")
        if isinstance(tii, dict) and "value" in tii:
            tii["value"] = not bool(tii["value"])
            touched += 1
    # and scramble the (tier2) settlement-bloc memberships for good measure
    poisoned["settlement_blocs"]["agora"] = ["CN"]
    poisoned["settlement_blocs"]["mbridge"] = ["US"]

    after = class_rule.all_classes(poisoned["signals"])
    moved = [f"{o}->{d}: {base[(o, d)][0]} -> {after[(o, d)][0]}"
             for (o, d) in base if base[(o, d)][0] != after[(o, d)][0]]
    return touched, moved


def prove_tier1_live(table):
    """The mirror control: flipping a tier1_legal class-driving signal MUST move classes.
    Without this, 'tier2 is inert' would be satisfied trivially by a class function that reads
    nothing at all."""
    S = table["signals"]
    base = class_rule.all_classes(S)
    poisoned = copy.deepcopy(table)
    poisoned["signals"]["TW"]["token_regime"]["value"] = "authorizable"   # a tier1_legal signal
    after = class_rule.all_classes(poisoned["signals"])
    return [f"{o}->{d}" for (o, d) in base if base[(o, d)][0] != after[(o, d)][0]]


def write_trace(rows, dist):
    OUT.mkdir(exist_ok=True)
    lines = [
        "# Derivation trace — all 132 classes, recomputed from `data/signal_table.json`\n",
        "_Generated by `tools/recompute_classes.py`. Every row is produced by "
        "`tools/class_rule.py:class_of`, which reads exactly two signals — the destination's "
        "`inbound_gate` and the origin's `token_regime`, both `tier1_legal` — and never reads the "
        "`token_in_issue` market fact._\n",
        "The Corridor Atlas v0.2.5 precedence, applied in order:\n",
    ]
    for k in ["destination_prohibition", "destination_no_regime", "origin_drag",
              "destination_in_transition", "destination_gate"]:
        lines.append(f"{RULE_LABEL[k]}")
    lines.append("")
    lines.append(f"Distribution: `{dict(sorted(dist.items()))}` — 132 edges.\n")
    lines.append("| origin | dest | class | deciding rule | governing | signal | value | binding_status | evidence |")
    lines.append("|---|---|:---:|---|:---:|---|---|---|---|")
    for (o, d, c, r, gov, sig, sv, bs, et) in rows:
        lines.append(f"| {o} | {d} | **{c}** | {RULE_LABEL[r]} | {gov} | `{sig}` | `{sv}` | `{bs}` | `{et}` |")
    lines.append("")
    lines.append("> Read the `origin_drag` rows: the class is decided by the **origin**, and the "
                 "instrument named is the origin's issuance regime, not the destination's gate. "
                 "Read the four rows `TW→CN`, `KR→CN`, `CN→KR`, `TW→KR`: they come from tokenless "
                 "origins and are nonetheless **not** Category III, because a destination prohibition "
                 "and a destination pre-regime absence rank above origin drag. Those four edges read "
                 "`III` through v0.9.99 — the eighth review's NF-1.\n")
    (OUT / "derivation_trace.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Recompute all 132 corridor classes from the signal table.")
    ap.add_argument("--artifact", default=str(ARTIFACT))
    ap.add_argument("--table", default=str(TABLE))
    ap.add_argument("--prove-tier2-inert", action="store_true",
                    help="flip every tier2_operational market signal and assert no class moves")
    ap.add_argument("--trace", action="store_true", help="write out/derivation_trace.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    table = class_rule.load(args.table)
    artifact = json.loads(pathlib.Path(args.artifact).read_text(encoding="utf-8"))

    sig_bad = class_rule.check_signal_provenance(table) + class_rule.check_gate_values(table)
    pr1_bad, rows = recompute(table, artifact)
    dist = Counter(r[2] for r in rows)

    tier2_touched, tier2_moved, tier1_moved = 0, [], []
    if args.prove_tier2_inert:
        tier2_touched, tier2_moved = prove_tier2_inert(table)
        tier1_moved = prove_tier1_live(table)

    ok = not sig_bad and not pr1_bad and not tier2_moved and \
        (not args.prove_tier2_inert or bool(tier1_moved))

    if args.json:
        print(json.dumps({
            "tool": "recompute_classes", "tool_version": __version__,
            "signal_table": table["version"], "artifact_revision": artifact.get("artifact_revision"),
            "sig_violations": sig_bad, "pr1_violations": pr1_bad,
            "class_distribution": dict(sorted(dist.items())),
            "tier2_signals_flipped": tier2_touched, "classes_moved_by_tier2": tier2_moved,
            "classes_moved_by_tier1_control": len(tier1_moved),
            "exit_code": 0 if ok else 1,
        }, indent=2, ensure_ascii=False))
        return 0 if ok else 1

    print("=" * 82)
    print(f"recompute_classes v{__version__} — 132 classes derived from data/signal_table.json")
    print("=" * 82)
    print(f"[{'PASS' if not sig_bad else 'FAIL'}] SIG1/SIG2/SIG3  the signal table's own provenance gates")
    for b in sig_bad[:6]:
        print(f"         -> {b}")
    if not sig_bad:
        print("         every class-driving signal is tier1_legal with an instrument; no "
              "resolution_text signal rests on a not-yet-in-force instrument")
    print(f"[{'PASS' if not pr1_bad else 'FAIL'}] PR1  the published rule reproduces all 132 "
          f"class_codes, rules, instruments and resolves_to")
    for b in pr1_bad[:8]:
        print(f"         -> {b}")
    if args.prove_tier2_inert:
        print(f"[{'PASS' if not tier2_moved else 'FAIL'}] TIER2-INERT  flipped {tier2_touched} "
              f"token_in_issue market signals + scrambled the settlement blocs: "
              f"{len(tier2_moved)} classes moved (must be 0)")
        for b in tier2_moved[:5]:
            print(f"         -> {b}")
        print(f"[{'PASS' if tier1_moved else 'FAIL'}] TIER1-LIVE (control)  flipping ONE tier1_legal "
              f"signal (TW token_regime) moves {len(tier1_moved)} classes (must be > 0, else the "
              f"class function reads nothing)")
    print("-" * 82)
    print(f"class distribution: {dict(sorted(dist.items()))}")
    print("guardrail: this proves the artifact's classes FOLLOW from the published signals. It does "
          "not prove a signal is a correct statement of law — only primary-source verification does "
          "(Citable by Construction §6.1).")
    print("=" * 82)

    if args.trace:
        write_trace(rows, dist)
        print("wrote out/derivation_trace.md")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
