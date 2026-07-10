#!/usr/bin/env python3
"""schema_reference_crosscheck.py  -  is the bundled minimal schema executor TRUSTWORTHY?

THE PROBLEM THIS SOLVES
-----------------------
verify_corridors_directed.py ships its own ~40-line JSON-Schema-subset validator so the corridor
layer can be checked with zero third-party dependencies. That buys portability, but invites a fair
objection: *a home-grown validator that accepts everything is worthless.* "132/132 validate" means
nothing unless the validator can also say no -- and unless it says no to the same things a real
JSON-Schema implementation says no to.

This script answers both halves, in two layers.

  LAYER 1 (always runs, zero dependencies)  --  DISCRIMINATION
      Build an adversarial battery of mutations of real edges (bad enums, illegal tags, missing
      required fields, wrong types, pattern violations, out-of-vocabulary jurisdictions, shape
      swaps). Assert the bundled executor ACCEPTS the pristine edge and REJECTS every mutation.
      A validator that passes this cannot be a rubber stamp.

  LAYER 2 (runs iff `jsonschema` is importable)  --  AGREEMENT
      Re-run the whole corpus and the whole battery through the `jsonschema` reference
      implementation (Draft 2020-12) and assert the two agree on EVERY verdict, so neither is more
      permissive than the other. Also assert the schema is itself a legal Draft 2020-12 schema.

If `jsonschema` is absent, Layer 2 prints a SKIP; the script still exits non-zero on a Layer-1
failure. The zero-dependency guarantee of `tools/` is therefore preserved -- the reference library
is an optional oracle, never a runtime dependency. CI installs it, so Layer 2 runs on every push.

Usage:
    python3 tools/schema_reference_crosscheck.py            # Layer 1 (+ Layer 2 if available)
    pip install jsonschema && python3 tools/schema_reference_crosscheck.py

Exit 0 = the executor discriminates (and, where checkable, agrees with the reference).
Exit 1 = it accepted something it should have rejected, or disagreed with the reference.
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


import copy
import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from verify_corridors_directed import schema_errors  # noqa: E402  (the executor under test)

ARTIFACT = HERE.parent / "analysis" / "computed_corridors_directed.json"
SCHEMA_PATH = HERE / "corridor_directed.schema.json"

PRISTINE = "pristine (must be VALID)"


def build_battery(edge):
    """Return [(label, instance, expected_valid)] for one base edge."""
    cases = [(PRISTINE, copy.deepcopy(edge), True)]

    def m(label, fn):
        e = copy.deepcopy(edge)
        fn(e)
        cases.append((label, e, False))

    m("class_code outside enum",         lambda e: e.__setitem__("class_code", "Category-One"))
    m("schema tag outside enum",         lambda e: e.__setitem__("schema", "corridor/v9"))
    m("direction != const 'directed'",   lambda e: e.__setitem__("direction", "undirected"))
    m("origin outside the twelve",       lambda e: e.__setitem__("origin", "ZZ"))
    m("destination lowercase (enum)",    lambda e: e.__setitem__("destination", "eu"))
    m("compatibility_pair bad pattern",  lambda e: e.__setitem__("compatibility_pair", "usa-eur"))
    m("compatibility_category bad",      lambda e: e.__setitem__("compatibility_category", "IV"))
    m("interaction_sets bad item",       lambda e: e.__setitem__("interaction_sets", ["A", "Z"]))
    m("archetypes bad item",             lambda e: e.__setitem__("archetypes", ["QQ"]))
    m("materialized_from bad",           lambda e: e.__setitem__("materialized_from", "guessed"))
    m("name empty (minLength)",          lambda e: e.__setitem__("name", ""))
    m("corridor_id wrong type",          lambda e: e.__setitem__("corridor_id", 12345))
    m("currencies wrong type",           lambda e: e.__setitem__("currencies", ["USD", "EUR"]))
    m("origin_override bad shape (int)", lambda e: e.__setitem__("origin_override", 42))
    m("inbound_mechanism wrong type",    lambda e: e.__setitem__("inbound_mechanism", "a string"))
    # v0.9.93: infrastructure_overlap is a strict {bloc, note} object -----------------------------
    m("infra_overlap.bloc outside enum", lambda e: e.__setitem__("infrastructure_overlap", {"bloc": "atlantis"}))
    m("infra_overlap missing bloc",      lambda e: e.__setitem__("infrastructure_overlap", {"note": "no bloc"}))
    m("infra_overlap extra property",    lambda e: e.__setitem__("infrastructure_overlap", {"bloc": "none", "zzz": 1}))
    m("infra_overlap legacy string",     lambda e: e.__setitem__("infrastructure_overlap", "Project Agora (free text)"))
    m("evidence_tier outside enum",      lambda e: e.__setitem__("evidence_tier", "vibes"))
    m("valid_as_of bad date pattern",    lambda e: e.__setitem__("valid_as_of", "June 2026"))
    m("confidence outside enum",         lambda e: e.__setitem__("confidence", "certain"))
    m("version_added bad semver",        lambda e: e.__setitem__("version_added", "v5"))
    m("tags item wrong type",            lambda e: e.__setitem__("tags", ["ok", 7]))
    m("missing required 'origin'",       lambda e: e.pop("origin", None))
    m("missing required 'class_code'",   lambda e: e.pop("class_code", None))
    m("missing required 'name'",         lambda e: e.pop("name", None))
    # v0.10.0: class_basis (the three-axis evidence model), typed triggers, structured origin_override
    m("missing required 'class_basis'",  lambda e: e.pop("class_basis", None))
    m("class_basis wrong type",          lambda e: e.__setitem__("class_basis", "origin drag"))
    m("class_basis.rule outside enum",   lambda e: e["class_basis"].__setitem__("rule", "vibes"))
    m("class_basis.signal outside enum", lambda e: e["class_basis"].__setitem__("signal", "token_in_issue"))
    m("class_basis.claim_class bad",     lambda e: e["class_basis"].__setitem__("claim_class", "tier3"))
    m("class_basis.binding_status bad",  lambda e: e["class_basis"].__setitem__("binding_status", "in_force"))
    m("class_basis.signal_value bad",    lambda e: e["class_basis"].__setitem__("signal_value", "open"))
    m("class_basis empty instrument",    lambda e: e["class_basis"].__setitem__("instrument", ""))
    m("class_basis missing 'rule'",      lambda e: e["class_basis"].pop("rule", None))
    m("class_basis extra property",      lambda e: e["class_basis"].__setitem__("hunch", "probably"))
    m("origin_drag as a string",         lambda e: e.__setitem__("origin_drag", "yes"))
    m("origin_override.status bad",      lambda e: e.__setitem__(
        "origin_override", {"flag": "origin-egress override", "status": "maybe", "basis": "x"}))
    m("origin_override missing basis",   lambda e: e.__setitem__(
        "origin_override", {"flag": "origin-egress override", "status": "active"}))
    m("origin_override wrong flag const",lambda e: e.__setitem__(
        "origin_override", {"flag": "egress", "status": "active", "basis": "x"}))
    m("as_of_timeline bad today_class",  lambda e: e.__setitem__("as_of_timeline", {
        "today_class": "II", "as_of_base": "2026-06-30", "scheduled": [], "contingent": []}))
    m("trigger status outside enum",     lambda e: e.__setitem__("as_of_timeline", {
        "today_class": "T", "as_of_base": "2026-06-30", "contingent": [],
        "scheduled": [{"event_id": "x", "status": "maybe-someday", "resolves_to": "I"}]}))
    m("trigger date_kind outside enum",  lambda e: e.__setitem__("as_of_timeline", {
        "today_class": "T", "as_of_base": "2026-06-30", "contingent": [],
        "scheduled": [{"event_id": "x", "status": "scheduled", "resolves_to": "I",
                       "date_kind": "vibes", "effective_date": "2027-10-25"}]}))
    m("trigger resolves_to a non-class", lambda e: e.__setitem__("as_of_timeline", {
        "today_class": "T", "as_of_base": "2026-06-30", "contingent": [],
        "scheduled": [{"event_id": "x", "status": "scheduled", "resolves_to": "blocked"}]}))
    m("trigger extra property",          lambda e: e.__setitem__("as_of_timeline", {
        "today_class": "T", "as_of_base": "2026-06-30", "contingent": [],
        "scheduled": [{"event_id": "x", "status": "scheduled", "resolves_to": "I", "odds": 0.48}]}))
    m("as_of_timeline missing 'scheduled'", lambda e: e.__setitem__("as_of_timeline", {
        "today_class": "T", "as_of_base": "2026-06-30", "contingent": []}))
    return cases


def main():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    doc = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    edges = doc["edges"]

    def bundled_valid(inst):
        return not schema_errors(inst, schema, schema)

    # exercise every shape the corpus actually has: the richest authored edge, the sparsest computed
    # skeleton, a regime-in-transition edge (which carries a typed as_of_timeline), and an edge with
    # a structured origin_override. A battery that only ever mutates one shape proves less.
    bases = [
        next(e for e in edges if e["materialized_from"] == "authored"),
        next(e for e in edges if e["materialized_from"] == "computed_skeleton"),
        next(e for e in edges if e["class_code"] == "T"),
        next(e for e in edges if isinstance(e.get("origin_override"), dict)),
    ]
    battery = [(b["corridor_id"], lbl, inst, exp)
               for b in bases for (lbl, inst, exp) in build_battery(b)]

    print("=" * 82)
    print("schema reference cross-check")
    print("=" * 82)

    # -------------------------------------------------------------------------------------------
    # LAYER 1 -- discrimination (zero dependencies, always runs)
    # -------------------------------------------------------------------------------------------
    l1_fail = []
    for cid, label, inst, expected in battery:
        got = bundled_valid(inst)
        if got != expected:
            verb = "ACCEPTED (should reject)" if got else "REJECTED (should accept)"
            l1_fail.append(f"[{cid}] {label}: {verb}")

    n_mut = sum(1 for _, lbl, _, _ in battery if lbl != PRISTINE)
    n_pri = len(battery) - n_mut
    l1_ok = not l1_fail
    print(f"[{'PASS' if l1_ok else 'FAIL'}] LAYER 1  discrimination: accepts {n_pri}/{n_pri} "
          f"pristine, rejects {n_mut - len(l1_fail)}/{n_mut} adversarial mutations")
    for f in l1_fail[:8]:
        print(f"         -> {f}")
    print("         (a validator that accepted these would be a rubber stamp; this one is not)")

    corpus_bad = [e["corridor_id"] for e in edges if not bundled_valid(e)]
    corpus_ok = not corpus_bad
    print(f"[{'PASS' if corpus_ok else 'FAIL'}] LAYER 1  corpus: bundled executor validates "
          f"{len(edges) - len(corpus_bad)}/{len(edges)} edges")
    for c in corpus_bad[:5]:
        print(f"         -> {c}")

    # -------------------------------------------------------------------------------------------
    # LAYER 2 -- agreement with the reference implementation (optional)
    # -------------------------------------------------------------------------------------------
    print("-" * 82)
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        print("[SKIP] LAYER 2  `jsonschema` not installed -- the reference oracle did not run.")
        print("         tools/ is zero-dependency by design; this layer is an OPTIONAL oracle.")
        print("         Force it with:  pip install jsonschema && "
              "python3 tools/schema_reference_crosscheck.py")
        print("         CI installs it, so Layer 2 runs on every push.")
        print("-" * 82)
        ok = l1_ok and corpus_ok
        print("RESULT: bundled executor DISCRIMINATES (reference agreement unverified in this "
              "environment)." if ok else "RESULT: bundled executor FAILED discrimination.")
        print("=" * 82)
        return 0 if ok else 1

    try:
        Draft202012Validator.check_schema(schema)
        schema_legal, schema_err = True, ""
    except Exception as exc:  # jsonschema.exceptions.SchemaError
        schema_legal, schema_err = False, str(exc).splitlines()[0]
    try:
        import importlib.metadata as _md
        _js_ver = _md.version("jsonschema")
    except Exception:
        _js_ver = "unknown"
    print(f"[{'PASS' if schema_legal else 'FAIL'}] LAYER 2  {SCHEMA_PATH.name} is a legal "
          f"Draft 2020-12 schema (jsonschema {_js_ver})")
    if not schema_legal:
        print(f"         -> {schema_err}")

    ref = Draft202012Validator(schema)

    corpus_disagree = [f"{e['corridor_id']}: bundled={bundled_valid(e)} reference={ref.is_valid(e)}"
                       for e in edges if bundled_valid(e) != ref.is_valid(e)]
    c2_ok = not corpus_disagree
    print(f"[{'PASS' if c2_ok else 'FAIL'}] LAYER 2  corpus: the two implementations agree on all "
          f"{len(edges)} edges")
    for d in corpus_disagree[:5]:
        print(f"         -> {d}")

    mut_disagree = [f"[{cid}] {lbl}: bundled={bundled_valid(inst)} reference={ref.is_valid(inst)}"
                    for cid, lbl, inst, _ in battery if bundled_valid(inst) != ref.is_valid(inst)]
    m2_ok = not mut_disagree
    print(f"[{'PASS' if m2_ok else 'FAIL'}] LAYER 2  mutations: the two agree on all "
          f"{len(battery)} verdicts (neither is more permissive)")
    for d in mut_disagree[:8]:
        print(f"         -> {d}")

    ok = l1_ok and corpus_ok and schema_legal and c2_ok and m2_ok
    print("-" * 82)
    print("RESULT: the bundled minimal executor is INDISTINGUISHABLE from the reference "
          "implementation on this schema." if ok else
          "RESULT: the bundled executor is NOT equivalent to the reference implementation.")
    print("=" * 82)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
