#!/usr/bin/env python3
"""class_rule.py  -  the ONE published function that turns per-jurisdiction signals into a
directed corridor class, plus the signal-table loader and its provenance gates.

WHY THIS MODULE EXISTS
----------------------
Through v0.9.99 the corridor artifact arrived as a finished `class_code` column. The rule that
produced it lived upstream and unpublished, which produced three findings at once:

  F2   for the 99 edges from token-holding origins the class is a pure function of the
       destination -- but *why* each destination resolves to its class was opaque.
  F6   the verifier re-implemented the partition from constants HAND-COPIED out of the builder.
       "They cannot disagree by construction" is the problem, not the reassurance.
  NF-1 the rule the artifact actually applied (origin-drag-first) CONTRADICTED the published
       Corridor Atlas v0.2.5 (destination-first), and no gate could see it, because OD1 encoded
       the rule as an axiom and CD1 laundered the deviation into a "declared delta".

v0.10.0 publishes both halves: `data/signal_table.json` (the inputs) and this function (the rule).
`tools/recompute_classes.py` derives all 132 classes from them and diffs against the artifact.

THE PRECEDENCE (Corridor Atlas v0.2.5, s.3.4 / s.4.1 -- quoted in the signal table)
-----------------------------------------------------------------------------------
  1. destination inbound_gate == 'prohibited'                  -> blocked
  2. destination inbound_gate == 'none'                        -> pre_regime
  3. origin token_regime != 'authorizable'                     -> III      (origin drag)
  4. destination inbound_gate.binding_status made_not_commenced-> T
  5. otherwise the operative gate type: authorization -> I, channel|comparability -> II

Steps 1-2 rank ABOVE origin drag because a prohibition and a pre-regime absence are terminal facts
about the destination: no origin-side token, present or future, completes the corridor. Category III
means "the composition is unresolved; partnership or coordination routes remain", which is false
where the destination bans the instrument. Ranking origin drag first (as the artifact did) made
TW->CN and KR->CN read `III` -- "partnership route" -- while their own prose read "Issuance and
circulation prohibited". That is NF-1, in the optimistic direction.

SIGNAL PROVENANCE (Citable by Construction, s.4.2)
--------------------------------------------------
`class_of` reads exactly two signals: `inbound_gate` (destination) and `token_regime` (origin).
Both are `tier1_legal`. It NEVER reads `token_in_issue`, which is a `tier2_operational` market fact.
That is NF-3, and `check_signal_provenance` enforces it -- while `recompute_classes.py --prove-tier2-inert`
demonstrates it empirically by flipping every `token_in_issue` and asserting no class moves.

Standard library only.
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


import json
import pathlib

__version__ = "0.10.0"

HERE = pathlib.Path(__file__).resolve().parent
SIGNAL_TABLE = HERE.parent / "analysis" / "signal_table.json"

J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "JP", "TW", "KR"]

# The only signals the class function is permitted to read. Both must be tier1_legal (SIG1).
CLASS_DRIVING_SIGNALS = ("inbound_gate", "token_regime")

# The gate type -> operative class map, applied only once the gate is in force.
GATE_TO_CLASS = {"authorization": "I", "channel": "II", "comparability": "II"}

VALID_CLASSES = {"I", "II", "III", "T", "blocked", "pre_regime"}


# ------------------------------------------------------------------------------------------------
# The rule
# ------------------------------------------------------------------------------------------------
def class_of(origin: str, destination: str, signals: dict) -> tuple[str, str]:
    """Return (class_code, rule_id) for one directed edge, from the signal table alone.

    rule_id names WHICH precedence step decided the class, so every edge can carry its own
    derivation (`class_basis.rule` in the artifact) and a reader never has to guess.
    """
    if origin == destination:
        raise ValueError("a jurisdiction is not a corridor with itself")

    gate = signals[destination]["inbound_gate"]

    # 1. a destination prohibition dominates everything
    if gate["value"] == "prohibited":
        return "blocked", "destination_prohibition"

    # 2. a destination with no authorizable pathway to receive into
    if gate["value"] == "none":
        return "pre_regime", "destination_no_regime"

    # 3. origin drag -- reads token_regime (tier1_legal), never token_in_issue (tier2). NF-3.
    if signals[origin]["token_regime"]["value"] != "authorizable":
        return "III", "origin_drag"

    # 4. the destination's regime is adopted but not yet operative
    if gate["binding_status"] == "made_not_commenced":
        return "T", "destination_in_transition"

    # 5. the operative gate type
    return GATE_TO_CLASS[gate["value"]], "destination_gate"


def resolves_to(destination: str, signals: dict):
    """The class a `T` edge resolves to once the destination gate commences (None if not a gate)."""
    return signals[destination]["inbound_gate"].get("resolves_to")


def binding_status_for(origin: str, destination: str, rule: str, signals: dict) -> str:
    """The binding status of the instrument THIS edge's class rests on."""
    if rule == "origin_drag":
        return signals[origin]["token_regime"]["binding_status"] or "no_regime"
    return signals[destination]["inbound_gate"]["binding_status"] or "no_regime"


def governing_jurisdiction(origin: str, destination: str, rule: str) -> str:
    return origin if rule == "origin_drag" else destination


def instrument_for(origin: str, destination: str, rule: str, signals: dict) -> str:
    if rule == "origin_drag":
        return signals[origin]["token_regime"]["instrument"]
    return signals[destination]["inbound_gate"]["instrument"]


def all_classes(signals: dict) -> dict:
    """Derive all 132 (origin, destination) -> (class_code, rule) pairs."""
    return {(o, d): class_of(o, d, signals) for o in J12 for d in J12 if o != d}


# ------------------------------------------------------------------------------------------------
# Loading + the provenance gates over the table itself
# ------------------------------------------------------------------------------------------------
def load(path: pathlib.Path | str = SIGNAL_TABLE) -> dict:
    doc = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if doc.get("schema") != "cbsr-analysis/signal_table":
        raise ValueError(f"not a signal table: {doc.get('schema')!r}")
    missing = [j for j in J12 if j not in doc["signals"]]
    if missing:
        raise ValueError(f"signal table is missing jurisdictions: {missing}")
    return doc


def check_signal_provenance(doc: dict) -> list[str]:
    """SIG1 + SIG2 + SIG3, returned as a list of violations ([] == clean).

    SIG1  signal-provenance: every signal `class_of` reads is tier1_legal, and `token_in_issue`
          is tier2_operational with no binding_status (Citable by Construction s.4.2).
    SIG2  binding-status cap: a signal at evidence_tier == resolution_text must have
          binding_status == in_force_enacted (Citable by Construction s.3.1 / s.4.2). This is the
          gate that keeps the US inbound gate out of the top tier -- and therefore the gate that
          produces the US -> `T` reclassification.
    SIG3  a tier1_legal signal carries a non-empty `instrument`.
    """
    bad = []
    S = doc["signals"]
    for j in J12:
        row = S[j]
        for name in CLASS_DRIVING_SIGNALS:
            sig = row.get(name)
            if sig is None:
                bad.append(f"SIG1 {j}.{name}: class-driving signal absent")
                continue
            if sig.get("claim_class") != "tier1_legal":
                bad.append(f"SIG1 {j}.{name}: class-driving signal is "
                           f"{sig.get('claim_class')!r}, must be tier1_legal")
            if not (sig.get("instrument") or "").strip():
                bad.append(f"SIG3 {j}.{name}: tier1_legal signal has no `instrument`")

        tii = row.get("token_in_issue")
        if tii is not None:
            if tii.get("claim_class") != "tier2_operational":
                bad.append(f"SIG1 {j}.token_in_issue: must be tier2_operational (it is a market fact)")
            if tii.get("binding_status") is not None:
                bad.append(f"SIG1 {j}.token_in_issue: a market fact carries no binding_status")

        for name, sig in row.items():
            if not isinstance(sig, dict):
                continue
            if sig.get("evidence_tier") == "resolution_text" and \
                    sig.get("binding_status") != "in_force_enacted":
                bad.append(f"SIG2 {j}.{name}: evidence_tier=resolution_text requires "
                           f"binding_status=in_force_enacted (got {sig.get('binding_status')!r}) "
                           f"-- an instrument must be IN FORCE, not merely located, to be cited "
                           f"as current binding law")
    return bad


def check_gate_values(doc: dict) -> list[str]:
    """The class function must be total: every gate value it can meet has a mapping."""
    bad = []
    for j, row in doc["signals"].items():
        g = row["inbound_gate"]
        v = g["value"]
        if v not in set(GATE_TO_CLASS) | {"prohibited", "none"}:
            bad.append(f"{j}.inbound_gate.value={v!r} is unknown to class_of")
        if row["token_regime"]["value"] not in {"authorizable", "not_commenced", "prohibited", "none"}:
            bad.append(f"{j}.token_regime.value={row['token_regime']['value']!r} is unknown to class_of")
        rt = g.get("resolves_to")
        if v in GATE_TO_CLASS and rt != GATE_TO_CLASS[v]:
            bad.append(f"{j}.inbound_gate.resolves_to={rt!r} != the gate type's class {GATE_TO_CLASS[v]!r}")
    return bad


if __name__ == "__main__":  # a tiny self-check, so the module is runnable
    doc = load()
    problems = check_signal_provenance(doc) + check_gate_values(doc)
    cls = all_classes(doc["signals"])
    from collections import Counter
    dist = Counter(c for c, _ in cls.values())
    print(f"class_rule v{__version__}: {len(cls)} edges derived; distribution {dict(sorted(dist.items()))}")
    print(f"signal-table gates: {'CLEAN' if not problems else str(len(problems)) + ' VIOLATION(S)'}")
    for p in problems:
        print("  -", p)
    raise SystemExit(1 if problems else 0)
