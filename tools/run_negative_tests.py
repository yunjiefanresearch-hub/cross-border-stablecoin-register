#!/usr/bin/env python3
"""run_negative_tests.py  -  prove that every gate in verify_corridors_directed.py BITES.

WHY THIS EXISTS
---------------
"Citable by Construction" (Fan, 2026), §4.1:

    A subset defined only by self-reported tags is a promise, not a guarantee. ... the
    model therefore makes the citability discipline real with build-time gates that refuse
    to compile a knowledge base in which the discipline is violated, and it demonstrates
    each gate by a negative test, a deliberate break on a throwaway copy that must make the
    build fail, after which the break is reverted.

The corridor bundle shipped the gates but never shipped the negative tests. A gate that has
never been shown to fail is indistinguishable, to a reader, from a gate that cannot fail.
This suite closes that hole for the corridor layer: for each hard check and each lint it
mutates a THROWAWAY copy of the artifact in a temp directory, runs the verifier as a
subprocess, and asserts that the SPECIFIC targeted check failed -- not merely that "something"
failed, which a test could satisfy for the wrong reason.

Two properties are asserted on every negative case:
  1. the verifier exits non-zero, and
  2. the TARGETED check id appears in the failure set (or, for a lint, in the lint set).

And one regression property, because it was a real defect:
  3. a missing required field produces a clean `SCHEMA ... FAIL`, never a Python traceback.
     (Before v0.9.92 the verifier crashed with `KeyError: 'origin'` before it could report.)

A positive control runs first: the pristine artifact must exit 0 with 16/16 hard checks.

v0.10.0 adds a SECOND suite over the newly-published `data/signal_table.json`: the table's own
provenance gates (SIG1 signal-provenance, SIG2 binding-status cap, SIG3 instrument-present) and PR1
(the published rule reproduces all 132 classes) are each broken on a throwaway copy, and
`tools/recompute_classes.py` must fail. A published signal table whose gates have never been shown
to fail is, again, indistinguishable from a table that cannot fail.

Standard library only. No pip install. Nothing outside a temp directory is ever written.

Usage:
    python3 tools/run_negative_tests.py [-v]
Exit code 0 if every gate bites as specified; 1 otherwise.
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
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

HERE = pathlib.Path(__file__).resolve().parent
VERIFIER = HERE / "verify_corridors_directed.py"
RECOMPUTE = HERE / "recompute_classes.py"
ARTIFACT = HERE.parent / "analysis" / "computed_corridors_directed.json"
SIGNAL_TABLE = HERE.parent / "analysis" / "signal_table.json"


# ------------------------------------------------------------------------------------------------
# harness
# ------------------------------------------------------------------------------------------------
def run_verifier(artifact_path: pathlib.Path, strict: bool = False):
    """Run the verifier as a subprocess. Returns (exit_code, parsed_json_or_None, stderr)."""
    cmd = [sys.executable, str(VERIFIER), str(artifact_path), "--json"]
    if strict:
        cmd.append("--strict")
    p = subprocess.run(cmd, capture_output=True, text=True)
    try:
        payload = json.loads(p.stdout)
    except json.JSONDecodeError:
        payload = None
    return p.returncode, payload, p.stderr


def failed_ids(payload):
    if not payload:
        return set()
    return {c["id"] for c in payload["hard_checks"] if not c["passed"]}


def lint_ids(payload):
    if not payload:
        return set()
    return {l["id"] for l in payload["lints"]}


# ------------------------------------------------------------------------------------------------
# mutations.  Each takes the loaded doc and returns a short description of the break.
# Edges are located dynamically -- no hard-coded indices, so the suite survives a rebuild.
# ------------------------------------------------------------------------------------------------
def _find(doc, pred):
    for e in doc["edges"]:
        if pred(e):
            return e
    raise AssertionError("negative test could not locate a suitable edge")


def mut_schema_bad_enum(doc):
    e = _find(doc, lambda e: e["class_code"] == "I")
    e["class_code"] = "Category-One"
    return f"class_code -> 'Category-One' on {e['origin']}->{e['destination']}"


def mut_schema_bad_tag(doc):
    e = _find(doc, lambda e: e["schema"] == "corridor/v3-directed-edge")
    e["schema"] = "corridor/v9-imaginary"
    return f"schema tag -> 'corridor/v9-imaginary' on {e['origin']}->{e['destination']}"


def mut_schema_missing_required(doc):
    e = _find(doc, lambda e: e["materialized_from"] == "computed_skeleton")
    cid = e["corridor_id"]
    del e["origin"]
    return f"delete required field 'origin' from {cid}"


def mut_schema_bad_jurisdiction(doc):
    e = _find(doc, lambda e: e["destination"] == "EU")
    e["destination"] = "ZZ"
    return f"destination -> 'ZZ' (not in the twelve) on {e['corridor_id']}"


def mut_dc1_drop_edge(doc):
    e = doc["edges"].pop()
    return f"drop the edge {e['origin']}->{e['destination']} (131 remain)"


def mut_dc3_provenance(doc):
    e = _find(doc, lambda e: e["materialized_from"] == "computed_skeleton")
    e["materialized_from"] = "authored"
    return f"relabel one skeleton edge as 'authored' ({e['origin']}->{e['destination']})"


def mut_dc4a_pair_key(doc):
    e = _find(doc, lambda e: e["compatibility_pair"] == "EU-US")
    e["compatibility_pair"] = "US-EU"  # schema-valid pattern, non-canonical order
    return "compatibility_pair 'EU-US' -> 'US-EU' (valid pattern, wrong canonical order)"


def mut_dc4b_direction_disagree(doc):
    e = _find(doc, lambda e: (e["origin"], e["destination"]) == ("US", "EU"))
    e["compatibility_category"] = "III"
    return "US->EU compatibility_category -> 'III' while EU->US keeps its own"


def mut_dc4c_attestation(doc):
    doc["cross_check"]["clean"] = False
    return "artifact cross_check.clean -> false"


def mut_od1_origin_drag(doc):
    e = _find(doc, lambda e: e["origin"] == "CN")
    e["class_code"] = "I"
    return f"CN->{e['destination']} class_code -> 'I' (tokenless origin must be III)"


def mut_cd1_distribution(doc):
    # move one I -> II from a non-tokenless origin: leaves OD1 untouched, breaks only CD1
    e = _find(doc, lambda e: e["class_code"] == "I" and e["origin"] not in {"CN", "TW", "KR"})
    e["class_code"] = "II"
    return f"{e['origin']}->{e['destination']} class_code 'I' -> 'II' (distribution no longer reconciles)"


def mut_ib1_bloc_tag(doc):
    # v0.9.93: infrastructure_overlap is {bloc, note} and IB1 covers ALL edges. Target an
    # AUTHORED cross-bloc edge (US<->HK) and flip its bloc to a wrong value: pre-v0.9.93 IB1
    # exempted authored edges and would have missed this; the new IB1 must catch it.
    e = _find(doc, lambda e: e["materialized_from"] == "authored"
              and isinstance(e.get("infrastructure_overlap"), dict)
              and e["infrastructure_overlap"].get("bloc") == "cross-bloc")
    e["infrastructure_overlap"]["bloc"] = "agora"   # fabricated: US<->HK is cross-bloc, not agora
    return (f"{e['origin']}->{e['destination']} (authored) infrastructure_overlap.bloc "
            f"'cross-bloc' -> 'agora'")


def mut_dg1_permute(doc):
    # v0.9.95: the distribution-conserving permutation the fourth review's probe used. Swap the
    # class_code of two token-holder edges into DIFFERENT destinations, so the class HISTOGRAM is
    # unchanged (CD1 still passes) and both origins are non-tokenless (OD1 still passes) -- only
    # per-destination homogeneity breaks. This is precisely the hole CD1 + OD1 cannot see and DG1
    # exists to close.
    a = _find(doc, lambda e: (e["origin"], e["destination"]) == ("US", "CH"))  # class I
    b = _find(doc, lambda e: (e["origin"], e["destination"]) == ("US", "AE"))  # class II
    a["class_code"], b["class_code"] = b["class_code"], a["class_code"]
    return "histogram-conserving swap: US->CH and US->AE class_codes exchanged (CD1 blind, DG1 catches)"


def mut_dg2_regime_drift(doc):
    # v0.9.95: reintroduce the stale-copy drift the fourth review found -- describe Taiwan as a draft
    # on the CN->TW edge while the token-holder->TW edges say enacted, so the same artifact asserts
    # Taiwan is both a draft and enacted. No hard check other than DG2 sees this.
    e = _find(doc, lambda e: (e["origin"], e["destination"]) == ("CN", "TW"))
    e.setdefault("inbound_mechanism", {})["test"] = "No operative inbound regime (draft VAS Act)"
    return "CN->TW inbound regime described as 'draft' while token-holder->TW edges say 'enacted'"


def mut_cf1_consistent_swap(doc):
    # v0.9.98: the seventh review's finding -- a FULLY self-consistent permutation of two
    # equal-token-holder-in-degree destinations (CN and KR, both 9) with EVERY inbound edge's prose
    # rewritten to match. It conserves the CD1 histogram, keeps each destination homogeneous (DG1),
    # and removes all regime-status contradictions (DG2), so it passes every internal-consistency
    # gate. Only CF1 -- the anchor to primary-source-CONFIRMED facts (CN is 'blocked' per VB-04) --
    # catches that the artifact now claims Mainland China has no prohibition.
    for e in doc["edges"]:
        d = e["destination"]
        if d == "CN":
            if e["class_code"] == "blocked":
                e["class_code"] = "pre_regime"
            e["feasibility_class"] = "Pre-regime at destination (no authorizable issuance pathway yet)"
            if isinstance(e.get("inbound_mechanism"), dict):
                e["inbound_mechanism"]["test"] = "No operative issuance regime yet (pre-regime)"
        elif d == "KR":
            if e["class_code"] == "pre_regime":
                e["class_code"] = "blocked"
            e["feasibility_class"] = "Blocked at destination (issuance prohibition)"
            if isinstance(e.get("inbound_mechanism"), dict):
                e["inbound_mechanism"]["test"] = "Issuance prohibition in force"
    return "self-consistent CN<->KR class swap (histogram/DG1/DG2 all satisfied; only CF1 anchors CN=blocked)"


def mut_tl1_contingent_done(doc):
    # v0.9.99 (NF-4): name a contingent event after a completed act. A contingent trigger is one whose
    # enactment has NOT happened (Feasibility §2.1), so 'tw-vas-act-enacted' on a contingent event
    # (while Taiwan's enactment is confirmed) is incoherent -- TL1 must catch it.
    e = _find(doc, lambda e: isinstance(e.get("as_of_timeline"), dict) and e["as_of_timeline"].get("contingent"))
    e["as_of_timeline"]["contingent"][0]["event_id"] = "tw-vas-act-enacted"
    return f"{e['origin']}->{e['destination']} contingent event renamed to 'tw-vas-act-enacted' (a completed act)"


def mut_od1_precedence(doc):
    # v0.10.0 (NF-1): re-introduce origin-drag-first. Under the published Atlas precedence a
    # destination prohibition dominates the origin's issuance gap, so TW->CN is `blocked`. Coding it
    # `III` says a partnership route exists into a jurisdiction that bans the instrument.
    e = _find(doc, lambda e: (e["origin"], e["destination"]) == ("TW", "CN"))
    e["class_code"] = "III"
    e["feasibility_class"] = "Category III (no direct issuance; partnership / coordination route)"
    e["origin_drag"] = True
    e["class_basis"]["rule"] = "origin_drag"
    e["class_basis"]["governing_jurisdiction"] = "TW"
    e["class_basis"]["signal"] = "token_regime"
    e["class_basis"]["signal_value"] = "not_commenced"
    e["class_basis"]["binding_status"] = "made_not_commenced"
    return "TW->CN reverted to origin-drag-first (III) while its own prose says issuance is prohibited"


def mut_cf1_us_regression(doc):
    # v0.10.0: re-introduce VB-06 exactly as it stood through v0.9.99 -- the 8 token-holder->US edges
    # coded Category II, i.e. an enacted-not-commenced regime treated as a live inbound gate. CF1's
    # US anchor (GENIUS s.20, confirmed against Congress.gov / the Federal Register / OCC Bulletin
    # 2026-3) is the gate that catches it. It was NOT an anchor before v0.10.0, which is why six
    # reviews recorded the symptom without any gate failing.
    for e in doc["edges"]:
        if e["destination"] == "US" and e["origin"] not in {"CN", "TW", "KR"}:
            e["class_code"] = "II"
            e["feasibility_class"] = "Category II (comparability determination required)"
            e.pop("as_of_timeline", None)
            e["class_basis"]["rule"] = "destination_gate"
            e["class_basis"]["binding_status"] = "in_force_enacted"
    return "the 8 inbound-US edges coded Category II again (the pre-v0.10.0 VB-06 error)"


def mut_tl2_missing_timeline(doc):
    # A `T` edge with no timeline is the exact shape of the US error: an enacted-not-commenced
    # destination coded as if it were live, with nothing dated to say otherwise.
    e = _find(doc, lambda e: e["class_code"] == "T" and e["destination"] == "UK")
    del e["as_of_timeline"]
    return f"{e['origin']}->UK is class T but carries no as_of_timeline"


def mut_tl2_dated_contingency(doc):
    # Feasibility s.2.1: "a contingent trigger moves no horizon until a date is fixed."
    e = _find(doc, lambda e: isinstance(e.get("as_of_timeline"), dict) and e["as_of_timeline"]["contingent"])
    e["as_of_timeline"]["contingent"][0]["effective_date"] = "2027-03-01"
    return f"{e['origin']}->{e['destination']} invents a date for a contingent trigger"


def mut_ev1_tier2_signal(doc):
    # The signal-provenance violation (Citable by Construction s.4.2): a derived legal conclusion
    # resting on a market fact. This is NF-3, at the edge level.
    e = _find(doc, lambda e: e["class_basis"]["rule"] == "origin_drag")
    e["class_basis"]["claim_class"] = "tier2_operational"
    return f"{e['origin']}->{e['destination']} class_basis.claim_class -> tier2_operational"


def mut_ev1_rule_class_mismatch(doc):
    e = _find(doc, lambda e: e["class_code"] == "blocked")
    e["class_basis"]["rule"] = "destination_gate"
    e["class_basis"]["signal_value"] = "authorization"
    return f"{e['origin']}->{e['destination']} is `blocked` but class_basis claims an in-force authorization gate"


def mut_oo1_missing_override(doc):
    e = _find(doc, lambda e: e["origin"] == "CN" and isinstance(e.get("origin_override"), dict))
    del e["origin_override"]
    return f"CN->{e['destination']} loses its origin-egress override (Atlas carries it on all 11 CN rows)"


def mut_m7_prohibition_in_III(doc):
    # The lint that turned --strict red through v0.9.99. v0.10.0 fixed the rule rather than excusing
    # the lint, so it fires on nothing -- but it must still bite if the contradiction returns.
    e = _find(doc, lambda e: e["class_code"] == "III" and e["destination"] == "JP")
    e["inbound_mechanism"]["test"] = "Issuance and circulation prohibited"
    return f"{e['origin']}->JP is Category III but its inbound_mechanism asserts a prohibition"


def mut_m4_marker(doc):
    e = _find(doc, lambda e: e["materialized_from"] == "computed_skeleton")
    e["name"] = e["name"] + " TODO check this"
    return f"inject a TODO marker into {e['corridor_id']}.name"


def mut_m5_prose(doc):
    e = _find(doc, lambda e: e["class_code"] == "I"
              and e["feasibility_class"].startswith("Category I "))
    e["feasibility_class"] = "Category III (prose contradicting the directed class_code)"
    return f"{e['origin']}->{e['destination']} prose says 'Category III' but class_code stays 'I'"


def mut_m6_undeclared_key(doc):
    e = _find(doc, lambda e: e["materialized_from"] == "computed_skeleton")
    e["brand_new_enrichment_field"] = "arrived without a schema update"
    return f"add an undeclared key to {e['corridor_id']}"


# (name, mutation, target check id, is_lint, needs_strict)
CASES = [
    ("SCHEMA rejects a class_code outside the enum",        mut_schema_bad_enum,        "SCHEMA", False, False),
    ("SCHEMA rejects an unknown schema tag",                mut_schema_bad_tag,         "SCHEMA", False, False),
    ("SCHEMA rejects a missing required field (no crash)",  mut_schema_missing_required,"SCHEMA", False, False),
    ("SCHEMA rejects a jurisdiction outside the twelve",    mut_schema_bad_jurisdiction,"SCHEMA", False, False),
    ("DC1  catches a missing ordered pair",                 mut_dc1_drop_edge,          "DC1",    False, False),
    ("DC3  catches a corrupted provenance partition",       mut_dc3_provenance,         "DC3",    False, False),
    ("DC4a catches a non-canonical compatibility_pair",     mut_dc4a_pair_key,          "DC4a",   False, False),
    ("DC4b catches two directions disagreeing on category", mut_dc4b_direction_disagree,"DC4b",   False, False),
    ("DC4c catches a flipped self-attestation",             mut_dc4c_attestation,       "DC4c",   False, False),
    ("OD1  catches a tokenless origin escaping Cat. III",   mut_od1_origin_drag,        "OD1",    False, False),
    ("CD1  catches a distribution that stops reconciling",  mut_cd1_distribution,       "CD1",    False, False),
    ("IB1  catches a fabricated settlement-bloc tag",       mut_ib1_bloc_tag,           "IB1",    False, False),
    ("DG1  catches a histogram-conserving class permutation", mut_dg1_permute,          "DG1",    False, False),
    ("DG2  catches a stale contradictory regime description", mut_dg2_regime_drift,     "DG2",    False, False),
    ("CF1  catches a self-consistent swap that fools DG1/DG2", mut_cf1_consistent_swap, "CF1",    False, False),
    ("TL1  catches a contingent event named after a done act",  mut_tl1_contingent_done, "TL1",    False, False),
    ("OD1  catches a return to origin-drag-first (NF-1)",   mut_od1_precedence,         "OD1",    False, False),
    ("CF1  catches the inbound-US Category II regression (VB-06)", mut_cf1_us_regression,"CF1",    False, False),
    ("TL2  catches a T edge with no trigger event",         mut_tl2_missing_timeline,   "TL2",    False, False),
    ("TL2  catches a contingent trigger given an invented date", mut_tl2_dated_contingency,"TL2",  False, False),
    ("EV1  catches a class driven by a tier2 market signal",mut_ev1_tier2_signal,       "EV1",    False, False),
    ("EV1  catches a class_basis rule that contradicts the class", mut_ev1_rule_class_mismatch,"EV1",False,False),
    ("OO1  catches a missing Atlas origin-egress override", mut_oo1_missing_override,   "OO1",    False, False),
    ("m4   catches an unresolved editorial marker",         mut_m4_marker,              "m4",     True,  True),
    ("m5   catches prose contradicting the directed class", mut_m5_prose,               "m5",     True,  True),
    ("m6   catches a key the schema does not declare",      mut_m6_undeclared_key,      "m6",     True,  True),
    ("m7   catches a Category III edge asserting a prohibition", mut_m7_prohibition_in_III, "m7",  True,  True),
]


# ------------------------------------------------------------------------------------------------
# suite 2: the signal table's own gates (v0.10.0).  Broken on a throwaway copy; recompute must fail.
# ------------------------------------------------------------------------------------------------
def run_recompute(table_path: pathlib.Path):
    p = subprocess.run([sys.executable, str(RECOMPUTE), "--table", str(table_path),
                        "--artifact", str(ARTIFACT), "--json"], capture_output=True, text=True)
    try:
        payload = json.loads(p.stdout)
    except json.JSONDecodeError:
        payload = None
    return p.returncode, payload, p.stderr


def sig_mut_tier2_driver(t):
    """NF-3: drive the class from a market fact. The single most consequential error a legal
    reference can make (Citable by Construction s.2.1)."""
    t["signals"]["US"]["token_regime"]["claim_class"] = "tier2_operational"
    return "US.token_regime.claim_class -> tier2_operational (a class-driving signal becomes a market fact)"


def sig_mut_binding_status_cap(t):
    """SIG2: promote a made-not-commenced instrument to the top provenance tier. This is exactly the
    move that produced the US=II error: 'the official text was located and confirmed' treated as
    'this is current binding law' (Citable by Construction s.2.3)."""
    t["signals"]["US"]["inbound_gate"]["evidence_tier"] = "resolution_text"
    return "US.inbound_gate.evidence_tier -> resolution_text while binding_status is made_not_commenced"


def sig_mut_no_instrument(t):
    t["signals"]["CN"]["inbound_gate"]["instrument"] = "  "
    return "CN.inbound_gate loses its instrument (a tier1_legal signal with nothing to cite)"


def sig_mut_pr1_drift(t):
    """PR1: the table and the artifact must never drift. Commence Taiwan in the table only."""
    t["signals"]["TW"]["inbound_gate"]["binding_status"] = "in_force_enacted"
    return "TW.inbound_gate commenced in the table but not in the artifact (silent drift)"


SIGNAL_CASES = [
    ("SIG1 catches a class driven by a tier2_operational signal", sig_mut_tier2_driver, "SIG1"),
    ("SIG2 catches resolution_text on a not-yet-in-force instrument", sig_mut_binding_status_cap, "SIG2"),
    ("SIG3 catches a tier1_legal signal with no instrument",     sig_mut_no_instrument, "SIG3"),
    ("PR1  catches signal-table / artifact drift",               sig_mut_pr1_drift,     "PR1"),
]


def main():
    ap = argparse.ArgumentParser(description="Negative tests: prove every corridor gate bites.")
    ap.add_argument("-v", "--verbose", action="store_true", help="print each mutation's detail")
    args = ap.parse_args()

    if not ARTIFACT.exists():
        print(f"FATAL: artifact not found: {ARTIFACT}", file=sys.stderr)
        return 2

    pristine = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    print("=" * 82)
    print("CBSR corridor gates - negative test suite")
    print("  every gate is broken on a throwaway copy and must make the verifier fail")
    print("=" * 82)

    ok = True

    # --- positive control -----------------------------------------------------------------------
    rc, payload, err = run_verifier(ARTIFACT)
    pos_ok = (rc == 0 and payload and payload["hard_checks_passed"] == payload["hard_checks_total"])
    print(f"[{'PASS' if pos_ok else 'FAIL'}] positive control: pristine artifact exits 0 with "
          f"{payload['hard_checks_passed'] if payload else '?'}/"
          f"{payload['hard_checks_total'] if payload else '?'} hard checks")
    ok &= pos_ok

    print("-" * 82)

    with tempfile.TemporaryDirectory(prefix="cbsr-negtest-") as td:
        tmp = pathlib.Path(td) / "computed_corridors_directed.json"

        for label, mutate, target, is_lint, needs_strict in CASES:
            doc = copy.deepcopy(pristine)          # throwaway copy; the real artifact is never touched
            detail = mutate(doc)
            tmp.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")

            rc, payload, err = run_verifier(tmp, strict=needs_strict)

            bit = (target in (lint_ids(payload) if is_lint else failed_ids(payload)))
            nonzero = rc != 0
            no_crash = "Traceback" not in err
            case_ok = bit and nonzero and no_crash

            print(f"[{'PASS' if case_ok else 'FAIL'}] {label}")
            if args.verbose or not case_ok:
                print(f"         break : {detail}")
                print(f"         result: exit={rc}  targeted={target} caught={bit}  clean={no_crash}")
                if not no_crash:
                    print(f"         STDERR: {err.strip().splitlines()[-1] if err.strip() else ''}")
            ok &= case_ok

            # the break lives only in the temp file; `pristine` is deep-copied every iteration,
            # so the reversion the methodology paper describes is structural, not a cleanup step.

    # --- suite 2: the signal table's own gates ---------------------------------------------------
    print("-" * 82)
    print("signal table (data/signal_table.json) - its gates must bite too")
    print("-" * 82)

    pristine_table = json.loads(SIGNAL_TABLE.read_text(encoding="utf-8"))
    rc, payload, _ = run_recompute(SIGNAL_TABLE)
    pos2 = (rc == 0 and payload and not payload["sig_violations"] and not payload["pr1_violations"])
    print(f"[{'PASS' if pos2 else 'FAIL'}] positive control: the pristine table reproduces all 132 "
          f"classes (PR1) and passes SIG1/SIG2/SIG3")
    ok &= pos2

    with tempfile.TemporaryDirectory(prefix="cbsr-sigtest-") as td:
        tmpt = pathlib.Path(td) / "signal_table.json"
        for label, mutate, target in SIGNAL_CASES:
            t = copy.deepcopy(pristine_table)
            detail = mutate(t)
            tmpt.write_text(json.dumps(t, ensure_ascii=False), encoding="utf-8")
            rc, payload, err = run_recompute(tmpt)
            found = payload and any(target in v for v in
                                    payload["sig_violations"] + payload["pr1_violations"])
            case_ok = bool(found) and rc != 0 and "Traceback" not in err
            print(f"[{'PASS' if case_ok else 'FAIL'}] {label}")
            if args.verbose or not case_ok:
                print(f"         break : {detail}")
                print(f"         result: exit={rc}  targeted={target} caught={bool(found)}")
            ok &= case_ok

    table_unchanged = json.loads(SIGNAL_TABLE.read_text(encoding="utf-8")) == pristine_table
    print(f"[{'PASS' if table_unchanged else 'FAIL'}] the committed signal table was never modified")
    ok &= table_unchanged

    # --- the artifact on disk must be untouched -------------------------------------------------
    unchanged = json.loads(ARTIFACT.read_text(encoding="utf-8")) == pristine
    print("-" * 82)
    print(f"[{'PASS' if unchanged else 'FAIL'}] the committed artifact was never modified")
    ok &= unchanged

    print("-" * 82)
    total = len(CASES) + len(SIGNAL_CASES)
    print(f"{'ALL GATES BITE' if ok else 'SOME GATE DID NOT BITE'} - "
          f"{total} negative cases ({len(CASES)} artifact + {len(SIGNAL_CASES)} signal table) "
          f"+ 2 positive controls + 2 non-mutation assertions")
    print("=" * 82)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
