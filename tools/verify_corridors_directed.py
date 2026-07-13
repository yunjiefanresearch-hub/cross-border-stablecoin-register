#!/usr/bin/env python3
"""verify_corridors_directed.py  -  standalone, zero-dependency verifier for the
directed-132 corridor layer (data/computed_corridors_directed.json).

WHY THIS EXISTS
---------------
The register's own build (build.py / run_invariants.py) can only run against the FULL
register tree (the 152 node records, analysis/compatibility.json, the skeleton and event
files, schema.json, and the upstream builders). That tree is NOT shipped in this repo.
This verifier re-checks everything about the corridor layer that can be checked from the
artifact ALONE - so a reviewer who only has the JSON still gets a green light without
reconstructing the whole register.

Standard library only (json, re, pathlib, sys, argparse, collections). No pip install.

INTEGRITY NOTES (what "verify" does and does NOT mean here)
  * SCHEMA is EXECUTED, not narrated. A minimal JSON-Schema-subset validator (below) runs
    tools/corridor_directed.schema.json against every edge. The verifier and the shipped
    schema therefore agree by construction. tools/schema_reference_crosscheck.py proves
    the minimal executor agrees with the independent `jsonschema` reference implementation.
  * SCHEMA is a GATE. If any edge is structurally invalid, the structural checks below are
    NOT attempted: they index required fields, and running them on invalid records would
    crash rather than report. A schema failure prints a clean FAIL and exits 1.
  * DC4 is RECOMPUTED where the artifact permits, and ATTESTED (clearly labelled) where it
    does not:
      DC4a  pair-key canonicality      - recomputed from the 132 edges (no external input)
      DC4b  inter-direction agreement  - recomputed from the 132 edges (no external input)
      DC4c  artifact self-attestation  - the artifact's own cross_check.clean flag. This is
            NOT an independent check: fully re-deriving each pair's category from first
            principles needs analysis/compatibility.json, which is not in this repo. DC4a
            and DC4b independently corroborate the flag as far as the edges allow.
  * The verifier checks the CORRIDOR LAYER's internal coherence. It cannot and does not
    confirm that any jurisdictional fact is a correct statement of law. Only primary-source
    verification does that (Citable by Construction, §6.1: the gates are defenses, not a cure).

HARD CHECKS (a FAIL sets exit code 1)
  SCHEMA  every edge validates against tools/corridor_directed.schema.json (executed; gate)
  DC1     the layer covers all 132 = 12x11 ordered pairs (no missing / no extra)
  DC3     provenance partitions the 132 (9 authored + 106 skeleton + 17 transition). NOTE:
          `materialized_from` is a PRODUCTION-provenance partition and is orthogonal to class --
          25 edges carry an as_of_timeline, not 17. TL2 checks the class<->timeline relation.
  DC4a    compatibility_pair equals the canonical alphabetical key of {origin,destination}
  DC4b    both directed edges of each unordered pair declare the same compatibility_category
  DC4c    the artifact's own category self-check block is clean (self-attested; see note)
  OD1     DESTINATION-FIRST PRECEDENCE (v0.10.0, was origin-drag-first): for a tokenless origin
          (CN/TW/KR) the class equals the destination's own class where that class is `blocked` or
          `pre_regime` (a prohibition and a pre-regime absence are terminal facts no origin token
          could overcome), and III otherwise; and every III edge originates in CN/TW/KR. Derived
          from the artifact, not asserted: the destination's class is read off its token-holder
          inbound edges, whose homogeneity DG1 independently guarantees. Through v0.9.99 OD1
          encoded origin-drag-first as an AXIOM and therefore could not flag the rule it enforced --
          the structural reason the eighth review's NF-1 was invisible to its own gates
  CD1     the class distribution reconciles exactly to the Corridor Atlas baseline
          (32 I / 32 II / 27 III / 8 T / 11 blocked / 22 pre-regime) via two declared deltas, both
          of which are FACT updates (a jurisdiction's binding status moved), not rule changes:
          (a) Taiwan enacted 2026-06-30, (b) the United States is enacted-not-commenced (GENIUS s.20)
  IB1     infrastructure_overlap.bloc on ALL 132 edges equals the bloc-partition function
          (Agora / mBridge / Ensemble / cross-bloc / none). v0.9.93: authored edges are NO
          LONGER exempt, and the check reads the structured `bloc` enum, not a prose prefix,
          closing the gap that hid the US<->HK cross-bloc edges through v0.9.92
  DG1     destination-class homogeneity (semantic; v0.9.95): all edges into a destination FROM
          token-holding origins share one class_code. Closes the distribution-conserving
          permutation the fourth review's probe exposed -- a class swap that keeps the CD1
          histogram constant must break per-destination homogeneity, and DG1 catches it
  DG2     destination regime-status consistency (semantic; v0.9.95): no destination may be
          described as both regime-absent (draft / no operative regime) and regime-present
          (enacted / in force) across its inbound edges. Closes the stale-copy drift that had
          CN/KR->TW calling Taiwan a "draft" while token-holder->TW edges called it enacted
  CF1     confirmed-fact anchor (semantic GROUND-TRUTH; v0.9.98): a few destination classes are
          pinned to the primary-source-CONFIRMED items in docs/verification_backlog.json (CN is
          'blocked' per VB-04; TW is 'T' per VB-R1). DG1/DG2 are internal-CONSISTENCY gates, and a
          self-consistent permutation of two equal-in-degree destinations with every prose field
          rewritten passes them all (the seventh review demonstrated a green artifact claiming China
          has no prohibition and Korea has one it does not). No internal check can catch a coherent
          lie; only an anchor to a fact verified outside the artifact can. CF1 is that anchor -- and
          it is deliberately PARTIAL (confirmed facts only). Full coverage is the upstream
          signal_table recompute (docs/PROPOSAL_signal_table.md)
  TL1     timeline coherence (semantic; v0.9.99): a `contingent` as_of_timeline event (one whose
          enactment has not happened, per Feasibility §2.1) must not be NAMED after a completed act
          (enacted/passed/signed/...). Closes the eighth review's NF-4: the 9 ->TW edges had a
          contingent 'tw-vas-act-enacted' while Taiwan's enactment is confirmed (VB-R1); the pending
          fact is commencement, and the event is now 'tw-vas-act-commencement'

NON-FATAL LINTS (surfaced as WARN; promoted to FAIL only under --strict)
  m1      an authored edge still carries the legacy 'corridor/v2-rich' schema tag (HK->BR seed)
  m4      an unresolved verification marker (CONFIRM/TODO/FIXME/TBD/XXX) is embedded in edge
          prose. The honest-residual discipline says the backlog belongs in queryable fields,
          not in inline editorial comments inside an authoritative artifact.
  m5      feasibility_class prose does not lead with the edge's own directed class_code
          (the HK->BR edge reads 'Category I/II', which is the UNDIRECTED pair category)
  m6      an edge carries a key the schema does not declare (forward-compatible, but worth
          knowing: it means the corpus grew a field the schema has not caught up with)
  m7      a Category III edge whose inbound_mechanism asserts an issuance PROHIBITION (NF-1, P0):
          III means "partnership / coordination route", which contradicts a ban. This is the
          origin-drag-first (artifact) vs destination-first (Atlas §3.9) rule conflict; it fires on
          TW->CN and KR->CN. Because it is unresolved (reconcile UPSTREAM -- docs/PAPER_ERRATA.md
          NF-1), `--strict` is RED on the shipped artifact BY DESIGN: a real P0 is surfaced, not
          hidden. `--strict` was green through v0.9.98; it turns red in v0.9.99 for this reason

Usage:
    python3 tools/verify_corridors_directed.py [ARTIFACT] [--strict] [--json]

    ARTIFACT   path to computed_corridors_directed.json (default: ../data/ next to tools/)
    --strict   treat every non-fatal lint as a failure (release gate)
    --json     emit a machine-readable report on stdout instead of the human report

Exit code 0 if every hard check passes (and, under --strict, no lint fired); 1 otherwise;
2 if the artifact or schema could not be read at all.
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
import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

__version__ = "0.10.0"

# --- portability: UTF-8 console on any locale ---------------------------------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover - Python < 3.7 or an exotic stream
    pass

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT = HERE.parent / "analysis" / "computed_corridors_directed.json"
SCHEMA_PATH = HERE / "corridor_directed.schema.json"

# --- the register's own topology constants (must match build_corridors_directed.py) -------------
J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "JP", "TW", "KR"]
TOKENLESS = {"CN", "TW", "KR"}  # no exportable authorizable token
INFRA = {
    "agora": {"US", "EU", "UK", "CH", "JP", "KR"},
    "mbridge": {"CN", "HK", "AE"},
    "ensemble": {"HK", "SG"},
}
# Tier-2 (operational) enrichment, not law. agora/mbridge member sets were externally verified;
# ensemble={HK, SG} treats the HKMA-Ensemble / MAS-Guardian alignment as a shared bloc, but SG's
# formal Ensemble membership is pending primary verification (see docs/verification_backlog.json VB-02).
PROVENANCE = {"authored", "computed_skeleton", "computed_transition"}
ATLAS_BASELINE = {"I": 32, "II": 32, "III": 27, "T": 8, "blocked": 11, "pre_regime": 22}

# fields the structural checks index directly; SCHEMA guarantees their presence before we run
STRUCTURAL_FIELDS = ("origin", "destination", "class_code", "compatibility_pair",
                     "compatibility_category", "materialized_from")

# m4: editorial markers that must not survive into an authoritative artifact
MARKER_RE = re.compile(r"\b(CONFIRM|TODO|FIXME|TBD|XXX)\b")


# ================================================================================================
# Minimal JSON-Schema-subset validator (stdlib only). Supports exactly the constructs used by
# tools/corridor_directed.schema.json: $ref (local), type (incl. list of types), enum, const,
# required, properties, additionalProperties (bool), pattern, minLength, items, anyOf.
# Returns a list of human-readable error strings ([] means the instance is valid).
#
# tools/schema_reference_crosscheck.py asserts that this executor agrees, edge for edge and
# mutation for mutation, with the `jsonschema` reference implementation.
# ================================================================================================
_JSON_TYPE = {
    "object": dict, "array": list, "string": str, "boolean": bool,
    "number": (int, float), "integer": int, "null": type(None),
}


def _type_ok(inst, t):
    if t == "integer":
        return isinstance(inst, int) and not isinstance(inst, bool)
    if t == "number":
        return isinstance(inst, (int, float)) and not isinstance(inst, bool)
    if t == "boolean":
        return isinstance(inst, bool)
    py = _JSON_TYPE.get(t)
    return isinstance(inst, py) if py is not None else True


def _resolve(ref, root):
    """Only local refs of the form '#/a/b/c'."""
    node = root
    for part in ref.lstrip("#/").split("/"):
        node = node[part]
    return node


def schema_errors(inst, schema, root, path="$"):
    errs = []
    if "$ref" in schema:
        return schema_errors(inst, _resolve(schema["$ref"], root), root, path)
    if "anyOf" in schema:
        if not any(not schema_errors(inst, sub, root, path) for sub in schema["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
        # anyOf is authoritative for this node in our schema; skip sibling keyword checks
        return errs
    if "const" in schema and inst != schema["const"]:
        errs.append(f"{path}: {inst!r} != const {schema['const']!r}")
    if "enum" in schema and inst not in schema["enum"]:
        errs.append(f"{path}: {inst!r} not in enum {schema['enum']}")
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(_type_ok(inst, t) for t in types):
            errs.append(f"{path}: type {type(inst).__name__} not in {types}")
    if isinstance(inst, str):
        if "minLength" in schema and len(inst) < schema["minLength"]:
            errs.append(f"{path}: shorter than minLength {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], inst):
            errs.append(f"{path}: {inst!r} fails pattern {schema['pattern']}")
    if isinstance(inst, list) and "items" in schema:
        for i, el in enumerate(inst):
            errs += schema_errors(el, schema["items"], root, f"{path}[{i}]")
    if isinstance(inst, dict):
        for req in schema.get("required", []):
            if req not in inst:
                errs.append(f"{path}: missing required '{req}'")
        props = schema.get("properties", {})
        for k, v in inst.items():
            if k in props:
                errs += schema_errors(v, props[k], root, f"{path}.{k}")
            elif schema.get("additionalProperties", True) is False:
                errs.append(f"{path}: additional property '{k}' not allowed")
    return errs


# ================================================================================================
# Domain helpers
# ================================================================================================
def infra_overlap(o, d):
    """Re-implementation of the builder's bloc-partition rule (ground truth), for independent
    verification. Returns the canonical enum: agora / mbridge / ensemble / cross-bloc / none."""
    om = {k for k, v in INFRA.items() if o in v}
    dm = {k for k, v in INFRA.items() if d in v}
    shared = om & dm
    if "ensemble" in shared:
        return "ensemble"
    if "mbridge" in shared:
        return "mbridge"
    if "agora" in shared:
        return "agora"
    if ("agora" in om and "mbridge" in dm) or ("mbridge" in om and "agora" in dm):
        return "cross-bloc"
    return "none"


def infra_bloc(io):
    """Read the edge's structured infrastructure_overlap.bloc enum (v0.9.93 shape).

    No prose parsing: the enum is authoritative. SCHEMA has already guaranteed the object shape
    and the enum membership before IB1 runs, so a missing/typo'd bloc fails SCHEMA, not IB1.
    A defensive fallback ('__unstructured__') is returned for a bare string only so a stale
    v0.9.92 artifact produces a clear IB1 mismatch rather than a crash."""
    if isinstance(io, dict):
        return io.get("bloc")
    return "__unstructured__"


def walk_strings(node, path=""):
    """Yield (json_path, string) for every string anywhere inside an edge."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node


def leading_category(prose):
    """Extract the 'Category X' token a feasibility_class prose leads with, if any."""
    m = re.match(r"\s*Category\s+([IVX/]+)", prose or "")
    return m.group(1) if m else None


# ================================================================================================
# Main
# ================================================================================================
def run(path: pathlib.Path):
    """Execute all checks. Returns (results, warnings, notes, doc) or raises SystemExit(2)."""
    if not path.exists():
        print(f"FATAL: artifact not found: {path}", file=sys.stderr)
        raise SystemExit(2)
    if not SCHEMA_PATH.exists():
        print(f"FATAL: schema not found: {SCHEMA_PATH}", file=sys.stderr)
        raise SystemExit(2)

    doc = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    edges = doc.get("edges", [])

    results, warnings, notes = [], [], []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    def warn(name, detail=""):
        warnings.append((name, detail))

    def note(name, detail=""):
        notes.append((name, detail))

    # --- SCHEMA (GATE): execute the shipped JSON schema against every edge ----------------------
    nonconforming = []
    for e in edges:
        errs = schema_errors(e, schema, schema)
        if errs:
            nonconforming.append(f"{e.get('corridor_id', '?')}: {errs[0]}")
    check(f"SCHEMA  all {len(edges)} edges validate against {SCHEMA_PATH.name} (executed)",
          not nonconforming, "; ".join(nonconforming[:5]))

    if nonconforming:
        # Fail fast. The structural checks index required fields; running them on structurally
        # invalid records would raise a KeyError traceback instead of reporting a clean FAIL.
        note("SCHEMA is a gate", f"{len(nonconforming)} edge(s) are structurally invalid, so the "
                                 "structural checks (DC*/OD1/CD1/IB1/DG1/DG2/CF1/TL1) were not attempted. Fix the "
                                 "schema violations and re-run.")
        return results, warnings, notes, doc

    # Belt and braces: SCHEMA guarantees the structural fields exist, but assert it explicitly so
    # a future schema relaxation can never silently re-introduce the KeyError crash.
    missing = [f"{e.get('corridor_id', '?')}: {f}" for e in edges
               for f in STRUCTURAL_FIELDS if f not in e]
    if missing:
        check("SCHEMA  structural fields present on every edge", False, "; ".join(missing[:5]))
        return results, warnings, notes, doc

    # --- m1 lint: authored edge(s) still on the legacy schema tag -------------------------------
    stragglers = [f"{e['corridor_id']} ({e['origin']}->{e['destination']})"
                  for e in edges if e.get("schema") != "corridor/v3-directed-edge"]
    if stragglers:
        warn("m1  authored edge(s) still on legacy 'corridor/v2-rich' tag (schema-valid; "
             "migrate for tag-uniformity)", "; ".join(stragglers))

    # --- DC1  coverage: all 132 ordered pairs ---------------------------------------------------
    seen = {(e["origin"], e["destination"]) for e in edges}
    expected = {(o, d) for o in J12 for d in J12 if o != d}
    check("DC1     covers all 132 = 12x11 ordered pairs",
          len(edges) == 132 and seen == expected,
          f"{len(edges)} edges; missing={sorted(expected - seen)[:4]} extra={sorted(seen - expected)[:4]}")

    # --- DC3  provenance partition --------------------------------------------------------------
    prov = Counter(e["materialized_from"] for e in edges)
    check("DC3     provenance partitions 132 (9 authored + 106 skeleton + 17 transition)",
          prov.get("authored") == 9 and prov.get("computed_skeleton") == 106
          and prov.get("computed_transition") == 17,
          dict(prov))
    n_timeline = sum(1 for e in edges if isinstance(e.get("as_of_timeline"), dict))
    note("DC3 partitions PRODUCTION provenance, which is orthogonal to class. From v0.10.0 "
         f"{n_timeline} edges carry an as_of_timeline (the 25 `T` edges: 8 ->UK, 9 ->TW, 8 ->US), "
         "not the 17 the `computed_transition` label counts -- three of the ->US edges are authored "
         "and five are skeletons. TL2 checks the class<->timeline relation; DC3 checks provenance.")

    # --- DC4a (RECOMPUTED)  pair-key canonicality -----------------------------------------------
    badkey = [f"{e['origin']}->{e['destination']}: pair={e['compatibility_pair']!r} "
              f"expected {'-'.join(sorted([e['origin'], e['destination']]))!r}"
              for e in edges
              if e["compatibility_pair"] != "-".join(sorted([e["origin"], e["destination"]]))]
    check("DC4a    [recomputed] compatibility_pair == canonical alphabetical key of {o,d}",
          not badkey, "; ".join(badkey[:4]))

    # --- DC4b (RECOMPUTED)  inter-direction category agreement ----------------------------------
    by_pair = defaultdict(dict)
    for e in edges:
        by_pair[tuple(sorted([e["origin"], e["destination"]]))][(e["origin"], e["destination"])] = \
            e["compatibility_category"]
    disagreeing = [f"{k}: {v}" for k, v in by_pair.items() if len(set(v.values())) > 1]
    check(f"DC4b    [recomputed] both directions of each of {len(by_pair)} pairs share "
          "compatibility_category",
          not disagreeing, "; ".join(disagreeing[:4]))

    # --- DC4c  artifact self cross-check block --------------------------------------------------
    xc = doc.get("cross_check", {})
    check("DC4c    [self-attested] artifact cross_check.clean == true, 0 mismatches",
          xc.get("clean") is True and not xc.get("category_mismatches"),
          str(xc.get("category_mismatches"))[:160])

    # --- DC4d (INDEPENDENT, register-only)  every edge's compatibility_category re-derived from
    # the §5.14 matrix itself, not from the artifact's own flag. In the audit repository this could
    # not run, because analysis/compatibility.json was not shipped (finding C1). In the register it
    # is shipped, so the self-attestation of DC4c is upgraded to an independent re-derivation and the
    # "cannot disagree by construction" objection (finding F6) is retired for this relationship too.
    compat_path = HERE.parent / "analysis" / "compatibility.json"
    if compat_path.exists():
        import json as _json
        pairs = {p_["pair"]: p_ for p_ in _json.loads(compat_path.read_text(encoding="utf-8"))["pairs"]}
        by_set = {frozenset(p_["jurisdictions"]): p_ for p_ in pairs.values()}
        bad = []
        for e in edges:
            row = by_set.get(frozenset({e["origin"], e["destination"]}))
            if row is None:
                bad.append(f"{e['origin']}->{e['destination']}: no §5.14 pair")
            elif e.get("compatibility_category") != row.get("category"):
                bad.append(f"{e['origin']}->{e['destination']}: {e.get('compatibility_category')!r} "
                           f"!= §5.14 {row.get('category')!r}")
            elif e.get("compatibility_pair") != row.get("pair"):
                bad.append(f"{e['origin']}->{e['destination']}: pair key {e.get('compatibility_pair')!r} "
                           f"!= {row.get('pair')!r}")
        check(f"DC4d    [recomputed] all {len(edges)} edges' compatibility_category re-derived from "
              f"analysis/compatibility.json (§5.14)", not bad, "; ".join(bad[:4]))
        note("DC4d upgrades DC4c from a self-attestation to an INDEPENDENT re-derivation: the §5.14 "
             "matrix is read from the register and every edge's category and pair key is recomputed "
             "from it. This is the check the audit repository could not run (finding C1/F6).")
    else:
        note("DC4c is the artifact's own flag, not an independent check. Full per-pair re-derivation "
             "from jurisdiction properties needs analysis/compatibility.json (absent); "
             "DC4a + DC4b recompute everything the 132 edges permit and both pass.")

    # --- OD1  destination-first precedence (v0.10.0; was origin-drag-first) ---------------------
    # Corridor Atlas v0.2.5 s.3.4: "Three classes are determined entirely by the destination. Every
    # edge terminating in Mainland China is Blocked ... Every edge terminating in Taiwan or South Korea
    # is Pre-regime ... (the edges whose origin is Mainland China, Taiwan, or South Korea fall instead
    # to Category III, since the origin has no exportable token)"; s.4.1: "the destination sets the
    # class on every edge except the twenty-seven where an origin-side issuance gap overrides it."
    # Its own edge register scores KR -> PRC as blocked and TW -> KR as pre-regime.
    #
    # So origin drag ranks THIRD, below a destination prohibition and a destination pre-regime: those
    # are terminal facts about the destination that no origin-side token, present or future, could
    # overcome. "Category III" means a partnership or coordination route remains -- which is false
    # into a jurisdiction that bans the instrument.
    #
    # This check DERIVES the destination's class from the artifact (the class its token-holding origins
    # see, whose per-destination homogeneity DG1 independently guarantees) rather than hard-coding
    # {CN: blocked, KR: pre_regime}. It is therefore a check on the RULE, not a restatement of it --
    # which is precisely what OD1 was not, through v0.9.99, and why NF-1 was invisible to it.
    dest_of_tokenholders = {}
    for e in edges:
        if e["origin"] not in TOKENLESS:
            dest_of_tokenholders.setdefault(e["destination"], set()).add(e["class_code"])
    TERMINAL = {"blocked", "pre_regime"}
    od1_bad = []
    for e in edges:
        if e["origin"] not in TOKENLESS:
            continue
        seen = dest_of_tokenholders.get(e["destination"], set())
        # a destination whose own token-holder inbound class is terminal imposes it on everyone;
        # otherwise the origin's issuance gap drags the edge to III
        want = (next(iter(seen)) if len(seen) == 1 and seen <= TERMINAL else "III")
        if e["class_code"] != want:
            od1_bad.append(f"{e['origin']}->{e['destination']}: {e['class_code']} (precedence says {want})")
    III_not_from_tokenless = [f"{e['origin']}->{e['destination']}"
                              for e in edges if e["class_code"] == "III" and e["origin"] not in TOKENLESS]
    check("OD1     destination-first precedence: prohibition/pre-regime > origin drag > transition > gate",
          not od1_bad and not III_not_from_tokenless,
          f"precedence_violations={od1_bad[:4]} III_not_from_tokenless={III_not_from_tokenless[:3]}")

    # --- CD1  distribution reconciles to the Atlas baseline via two declared FACT deltas ---------
    # Through v0.9.99 one of the two "declared deltas" was a RULE REVERSAL (origin drag on the
    # CN/TW/KR mutual edges) laundered into the same ledger as a genuine fact update. Both deltas are
    # now fact updates -- a jurisdiction's binding status moved -- and the rule is the Atlas's own.
    dist = Counter(e["class_code"] for e in edges)
    exp = dict(ATLAS_BASELINE)
    # (a) FACT: Taiwan enacted its Virtual Asset Service Act at third reading on 2026-06-30 (VB-R1).
    #     The 9 token-holder edges into TW move pre_regime -> T ...
    exp["pre_regime"] -= 9
    exp["T"] += 9
    #     ... and because TW is no longer a pre-regime destination, the two tokenless-origin edges
    #     into it (CN->TW, KR->TW) are no longer held there by the destination and fall to III.
    exp["pre_regime"] -= 2
    exp["III"] += 2
    # (b) FACT: the United States is enacted-not-commenced. GENIUS s.20 sets the effective date at the
    #     earlier of 2027-01-18 or final rules + 120 days; at the 2026-06-30 snapshot only proposed
    #     rules existed, so the s.18 inbound gate is not yet available. The 8 token-holder edges into
    #     the US move II -> T (VB-06 / errata E1 / F-US-1).
    exp["II"] -= 8
    exp["T"] += 8
    check("CD1     class distribution reconciles to Atlas baseline via 2 declared FACT deltas",
          dict(dist) == exp, f"got={dict(dist)} expected={exp}")
    note("CD1's deltas are fact updates, not rule changes (v0.10.0). Baseline "
         f"{ATLAS_BASELINE} + (Taiwan enacted) + (US enacted-not-commenced) = {exp}.")

    # --- IB1  infrastructure_overlap.bloc on ALL 132 edges (authored no longer exempt) ---------
    # v0.9.93: infrastructure_overlap is a structured {bloc, note} object and IB1 reads the
    # `bloc` enum directly on every edge. Through v0.9.92 IB1 checked only computed edges and
    # bucketed a free-text string by prose prefix; that exempted the two authored US<->HK edges,
    # whose prose ("No shared production or pilot settlement rail...") bucketed to "none" while
    # the partition says "cross-bloc" (US on Agora, HK on mBridge). The exemption hid the error.
    # Now bloc is authoritative and checked everywhere, so the same error cannot recur silently.
    infra_mismatch = []
    for e in edges:
        want = infra_overlap(e["origin"], e["destination"])
        got = infra_bloc(e.get("infrastructure_overlap"))
        if want != got:
            infra_mismatch.append(
                f"{e['origin']}->{e['destination']} [{e['materialized_from']}]: want {want}, got {got}")
    check("IB1     infrastructure_overlap.bloc matches partition on ALL 132 (authored included)",
          not infra_mismatch, "; ".join(infra_mismatch[:5]))

    # --- DG1  destination-class homogeneity (semantic gate; v0.9.95) ----------------------------
    # The corridor class is read at the destination gate with origin drag applied first, so for a
    # token-holding origin the class is a function of the destination. This gate enforces that: all
    # edges into a given destination FROM token-holding origins must share one class_code. It closes
    # the "distribution-conserving permutation" hole the fourth review's probe exposed -- e.g. reading
    # US->CN as Category I while the other token-holder->CN edges stay 'blocked' preserves the CD1
    # histogram but is caught here, because a permutation that keeps the class counts equal must break
    # per-destination homogeneity. (Tokenless origins are excluded: their edges are III by origin drag
    # regardless of destination, which is exactly what OD1 enforces.)
    dest_classes = {}
    for e in edges:
        if e["origin"] in TOKENLESS:
            continue
        dest_classes.setdefault(e["destination"], {}).setdefault(e["class_code"], []).append(e["origin"])
    dg1_bad = []
    for dest, codes in sorted(dest_classes.items()):
        if len(codes) > 1:
            detail = "; ".join(f"{c}<-{sorted(os)}" for c, os in sorted(codes.items()))
            dg1_bad.append(f"->{dest}: {detail}")
    check("DG1     destination-class homogeneity: token-holder->D edges share one class_code",
          not dg1_bad, " | ".join(dg1_bad[:5]))

    # --- DG2  destination regime-status consistency (semantic gate; v0.9.95) --------------------
    # Every edge terminating in destination D describes D's inbound regime in inbound_mechanism.test.
    # Those descriptions must not contradict each other on D's regime EXISTENCE. This catches the
    # stale-copy drift the fourth review found: CN->TW / KR->TW read "No operative inbound regime
    # (draft VAS Act)" while the 9 token-holder->TW edges read "enacted 2026-06-30" -- the same
    # artifact asserting Taiwan is both a draft and enacted. A destination may not carry both a
    # regime-absent phrase and a regime-present phrase. Absent patterns are tested FIRST, so a phrase
    # like "No operative inbound regime" is read as absent (regime negated), not present.
    ABSENT_RE = re.compile(r"\b(draft|no operative|not yet (?:enacted|adopted)|remains a bill|"
                           r"pre-regime|no (?:issuance )?regime)\b", re.I)
    PRESENT_RE = re.compile(r"\b(enacted|in force|operative|commenc|adopted)\b", re.I)

    def regime_polarity(t):
        if ABSENT_RE.search(t):     # tested first: "no operative regime" is ABSENT, not present
            return "absent"
        if PRESENT_RE.search(t):
            return "present"
        return "neutral"

    dg2_bad = []
    for dest in sorted({e["destination"] for e in edges}):
        tests = [e.get("inbound_mechanism", {}).get("test") or "" for e in edges
                 if e["destination"] == dest]
        pol = {regime_polarity(t) for t in tests}
        if "absent" in pol and "present" in pol:
            ex_absent = next(t for t in tests if regime_polarity(t) == "absent")
            ex_present = next(t for t in tests if regime_polarity(t) == "present")
            dg2_bad.append(f"->{dest}: '{ex_absent[:36]}...' vs '{ex_present[:36]}...'")
    check("DG2     destination regime-status consistency: no D described as both absent and present",
          not dg2_bad, " | ".join(dg2_bad[:5]))

    # --- CF1  confirmed-fact anchor (semantic ground-truth gate; v0.9.98) -----------------------
    # DG1/DG2 are INTERNAL-CONSISTENCY gates: a *self-consistent* permutation of two destinations
    # with equal token-holder in-degree, with every prose field rewritten to match, passes all of
    # SCHEMA/DC*/OD1/CD1/IB1/DG1/DG2 (the seventh review demonstrated exactly this: a green artifact
    # asserting Mainland China has no prohibition and South Korea has one it does not). No amount of
    # internal coherence can catch a coherent lie -- only an anchor to a fact verified OUTSIDE the
    # artifact can. CF1 is that anchor: it pins a small number of destination classifications to the
    # primary-source-CONFIRMED items in docs/verification_backlog.json. It is deliberately PARTIAL
    # (it covers only the confirmed facts, not all 132 edges); full coverage is the upstream
    # signal_table recompute in docs/PROPOSAL_signal_table.md. Because the threat model is a poisoned
    # ARTIFACT (the tools are trusted), the anchors live in the trusted verifier, sourced to backlog
    # IDs; they are ground truth, not builder logic (so they do not deepen finding F6 -- they are the
    # independent check F6 asks for).
    CONFIRMED_FACT_ANCHORS = [
        # (jurisdiction, expected class for token-holder-origin inbound edges, backlog id, basis)
        ("CN", "blocked", "VB-04", "PRC 银发〔2026〕42号 issuance prohibition, in force 2026-02-06, "
                                   "confirmed vs the PBoC 条法司 primary page"),
        ("TW", "T",       "VB-R1", "Taiwan Virtual Asset Service Act enacted 2026-06-30, not "
                                   "commenced (regime-in-transition), confirmed vs the enacted text"),
        ("US", "T",       "VB-06", "GENIUS Act §20: effective on the earlier of 2027-01-18 (18 months "
                                   "after enactment) or 120 days after final rules; at the 2026-06-30 "
                                   "snapshot only proposed rules existed (OCC/FDIC/FinCEN-OFAC/Treasury "
                                   "NPRMs), so the §18 inbound gate was not yet available. Confirmed "
                                   "against Congress.gov, the Federal Register and OCC Bulletin 2026-3 "
                                   "by reviews 5, 8 and 9; the artifact was corrected in v0.10.0"),
    ]
    cf1_bad = []
    for juris, want_class, vb_id, basis in CONFIRMED_FACT_ANCHORS:
        got = {e["class_code"] for e in edges
               if e["destination"] == juris and e["origin"] not in TOKENLESS}
        if got != {want_class}:
            cf1_bad.append(f"->{juris} should be {{{want_class}}} ({vb_id}) but token-holder edges are {sorted(got)}")
    check("CF1     confirmed-fact anchor: destination class honours primary-source-verified facts",
          not cf1_bad, " | ".join(cf1_bad))

    # --- TL1  timeline event-kind coherence (semantic; v0.9.99) ---------------------------------
    # Feasibility Over Time §2.1: a `contingent` trigger is one whose enactment HAS NOT HAPPENED and
    # carries no firm date. So a contingent event must not be NAMED after a completed event. The
    # eighth review found the 9 token-holder->TW edges carrying a contingent event `tw-vas-act-enacted`
    # -- but Taiwan's enactment has happened (VB-R1 confirmed); the pending fact is COMMENCEMENT. A
    # machine reading `status=contingent, event_id=*-enacted` would infer the Act is unpassed,
    # contradicting the same edge's inbound_mechanism and DG2. TL1 forbids a contingent event whose
    # id names a completed act (enacted/passed/signed/adopted/promulgated/gazetted/commenced).
    DONE_VERB = re.compile(r"(enacted|passed|signed|adopted|promulgated|gazetted|in[-_]force)", re.I)
    tl1_bad = []
    for e in edges:
        tl = e.get("as_of_timeline")
        if not isinstance(tl, dict):
            continue
        for ev in list(tl.get("contingent", [])) + list(tl.get("scheduled", [])):
            if ev.get("status") != "contingent":
                continue                      # a SCHEDULED event may name a completed act
            eid = ev.get("event_id") or ""
            if DONE_VERB.search(eid):
                tl1_bad.append(f"{e['origin']}->{e['destination']}: contingent event '{eid}' names a completed act")
    check("TL1     timeline coherence: a contingent event is not named after a completed act",
          not tl1_bad, " | ".join(tl1_bad[:5]))

    # --- TL2  class <-> timeline biconditional, and the trigger typology (v0.10.0) ---------------
    # A `T` edge WITHOUT a timeline is the exact shape of the US error: an enacted-not-commenced
    # destination coded as if it were live, with nothing dated to say otherwise. A non-`T` edge WITH a
    # timeline is the mirror. Both are now build failures. TL2 also enforces the trigger typology the
    # Feasibility paper claims and the pre-v0.10.0 schema could not express (eighth review NF-5):
    # `scheduled` (a gazetted day), `scheduled_with_cap` (an earlier-of upper bound that may fall
    # sooner -- GENIUS s.20), `contingent` (enacted, no gazetted commencement -- Taiwan).
    tl2_bad = []
    resolves_by_dest = defaultdict(set)
    for e in edges:
        has = isinstance(e.get("as_of_timeline"), dict)
        is_T = e["class_code"] == "T"
        if is_T != has:
            tl2_bad.append(f"{e['origin']}->{e['destination']}: class={e['class_code']} but "
                           f"as_of_timeline {'present' if has else 'absent'}")
            continue
        if not has:
            continue
        tl = e["as_of_timeline"]
        events = list(tl.get("scheduled", [])) + list(tl.get("contingent", []))
        if tl.get("today_class") != "T":
            tl2_bad.append(f"{e['origin']}->{e['destination']}: today_class != 'T'")
        if not events:
            tl2_bad.append(f"{e['origin']}->{e['destination']}: a T edge with no trigger event")
        for ev in events:
            st, dk, dt = ev.get("status"), ev.get("date_kind"), ev.get("effective_date")
            if st == "scheduled" and not (dt and dk == "gazetted"):
                tl2_bad.append(f"{e['origin']}->{e['destination']}: `scheduled` needs a gazetted date")
            if st == "scheduled_with_cap" and not (dt and dk == "outer_cap"):
                tl2_bad.append(f"{e['origin']}->{e['destination']}: `scheduled_with_cap` needs "
                               f"effective_date + date_kind='outer_cap' (the cap may fall sooner)")
            if st == "contingent" and dt is not None:
                tl2_bad.append(f"{e['origin']}->{e['destination']}: a contingent trigger carries no "
                               f"date -- it 'moves no horizon until a date is fixed' (Feasibility s.2.1)")
            resolves_by_dest[e["destination"]].add(ev.get("resolves_to"))
    for d, rs in sorted(resolves_by_dest.items()):
        if len(rs) > 1:
            tl2_bad.append(f"->{d}: inbound triggers disagree on resolves_to {sorted(map(str, rs))}")
    check("TL2     class T <-> as_of_timeline, and every trigger is a typed change in law",
          not tl2_bad, " | ".join(tl2_bad[:5]))

    # --- EV1  evidence-model integrity: the three-axis model, enforced at this layer (v0.10.0) ---
    # Citable by Construction s.4.2's SIGNAL-PROVENANCE gate: "a derived conclusion may rest only on
    # propositions of law, never on a market fact." Through v0.9.99 that gate did not exist here --
    # `claim_class` and `binding_status` were not even schema fields, so the lawyer-citable
    # intersection was UNDEFINED rather than empty. Now every edge states, as data, which precedence
    # step decided it, on whose signal, resting on which instrument at what binding status; EV1
    # re-derives all of that from the edge itself and rejects any inconsistency.
    RULE_TO_CLASS = {
        "destination_prohibition":   "blocked",
        "destination_no_regime":     "pre_regime",
        "origin_drag":               "III",
        "destination_in_transition": "T",
    }
    RULE_TO_BINDING = {
        "destination_prohibition":   {"in_force_enacted"},   # a ban must itself be in force to bind
        "destination_no_regime":     {"no_regime"},
        "destination_in_transition": {"made_not_commenced"},
        "destination_gate":          {"in_force_enacted"},   # a gate must be in force to be a gate
        # origin drag: the origin's token_regime instrument may be an IN-FORCE prohibition (CN), a
        # made-not-commenced statute (TW), or nothing at all (KR). What matters is the signal's
        # EFFECT (`signal_value`), not the instrument's binding status -- see below.
        "origin_drag":               {"in_force_enacted", "made_not_commenced", "no_regime",
                                      "pending_proposal", "finalized_policy_pending"},
    }
    # The signal's legal EFFECT must imply the class. This is the check that distinguishes
    # "the instrument is in force" from "the instrument permits issuance": Mainland China's
    # 银发〔2026〕42号 is in_force_enacted AND prohibited, and only the second fact drags the edge.
    RULE_TO_SIGNAL_VALUE = {
        "destination_prohibition":   {"prohibited"},
        "destination_no_regime":     {"none"},
        "origin_drag":               {"prohibited", "not_commenced", "none"},   # never "authorizable"
        "destination_in_transition": {"authorization", "channel", "comparability"},
        "destination_gate":          {"authorization", "channel", "comparability"},
    }
    GATE_VALUE_TO_CLASS = {"authorization": "I", "channel": "II", "comparability": "II"}
    ev1_bad = []
    for e in edges:
        cb = e.get("class_basis")
        if not isinstance(cb, dict):
            ev1_bad.append(f"{e['origin']}->{e['destination']}: no class_basis")
            continue
        rule, cc = cb.get("rule"), e["class_code"]
        if rule in RULE_TO_CLASS and cc != RULE_TO_CLASS[rule]:
            ev1_bad.append(f"{e['origin']}->{e['destination']}: rule={rule} implies "
                           f"{RULE_TO_CLASS[rule]}, class_code={cc}")
        if rule == "destination_gate" and cc not in ("I", "II"):
            ev1_bad.append(f"{e['origin']}->{e['destination']}: rule=destination_gate but class={cc}")
        want_gov = e["origin"] if rule == "origin_drag" else e["destination"]
        if cb.get("governing_jurisdiction") != want_gov:
            ev1_bad.append(f"{e['origin']}->{e['destination']}: governing_jurisdiction "
                           f"{cb.get('governing_jurisdiction')} != {want_gov}")
        want_sig = "token_regime" if rule == "origin_drag" else "inbound_gate"
        if cb.get("signal") != want_sig:
            ev1_bad.append(f"{e['origin']}->{e['destination']}: signal {cb.get('signal')} != {want_sig}")
        if cb.get("claim_class") != "tier1_legal":
            ev1_bad.append(f"{e['origin']}->{e['destination']}: SIGNAL-PROVENANCE VIOLATION -- a "
                           f"class-driving signal is {cb.get('claim_class')!r}, not tier1_legal")
        if rule in RULE_TO_BINDING and cb.get("binding_status") not in RULE_TO_BINDING[rule]:
            ev1_bad.append(f"{e['origin']}->{e['destination']}: binding_status "
                           f"{cb.get('binding_status')!r} inconsistent with rule {rule!r}")
        sv = cb.get("signal_value")
        if rule in RULE_TO_SIGNAL_VALUE and sv not in RULE_TO_SIGNAL_VALUE[rule]:
            ev1_bad.append(f"{e['origin']}->{e['destination']}: signal_value {sv!r} cannot produce "
                           f"rule {rule!r}")
        if rule == "destination_gate" and GATE_VALUE_TO_CLASS.get(sv) != cc:
            ev1_bad.append(f"{e['origin']}->{e['destination']}: an in-force {sv!r} gate is "
                           f"Category {GATE_VALUE_TO_CLASS.get(sv)}, not {cc}")
        if not (cb.get("instrument") or "").strip():
            ev1_bad.append(f"{e['origin']}->{e['destination']}: class_basis has no instrument")
        if bool(e.get("origin_drag")) != (rule == "origin_drag"):
            ev1_bad.append(f"{e['origin']}->{e['destination']}: origin_drag={e.get('origin_drag')!r} "
                           f"disagrees with class_basis.rule={rule!r}")
    check("EV1     evidence model: class_basis implies class_code; every class-driving signal is tier1_legal",
          not ev1_bad, " | ".join(ev1_bad[:5]))

    # --- OO1  origin-override completeness (v0.10.0) ---------------------------------------------
    # Atlas v0.2.5's edge register carries "[origin-egress override (mainland capital controls)]" on
    # all 11 CN-> rows, "[origin-egress override (Singapore DTSP)]" on all 11 SG-> rows, and
    # "[conditional origin-egress override (Korea FX, dormant)]" on all 11 KR-> rows. The artifact
    # carried the flag on exactly ONE edge (SG->HK) and no gate checked it -- so a signal Feasibility
    # s.2.1 lists among the five that drive the class was ~99% absent from the data.
    OVERRIDE_ORIGINS = {"CN": "active", "SG": "active", "KR": "conditional_dormant"}
    oo1_bad = []
    for e in edges:
        ov = e.get("origin_override")
        want = OVERRIDE_ORIGINS.get(e["origin"])
        if want is None:
            if ov is not None:
                oo1_bad.append(f"{e['origin']}->{e['destination']}: unexpected origin_override")
        elif not isinstance(ov, dict):
            oo1_bad.append(f"{e['origin']}->{e['destination']}: missing origin_override (Atlas says {want})")
        elif ov.get("status") != want:
            oo1_bad.append(f"{e['origin']}->{e['destination']}: origin_override.status "
                           f"{ov.get('status')!r} != {want!r}")
    check("OO1     origin-egress override present on exactly the 33 CN/SG/KR outbound edges",
          not oo1_bad, " | ".join(oo1_bad[:5]))

    # --- m4 lint: unresolved editorial markers inside the artifact -------------------------------
    marker_hits = []
    for e in edges:
        for jpath, s in walk_strings(e):
            m = MARKER_RE.search(s)
            if m:
                marker_hits.append(f"{e['corridor_id']}{jpath}: {m.group(1)} -> {s[:70]}...")
    if marker_hits:
        warn(f"m4  {len(marker_hits)} unresolved verification marker(s) embedded in edge prose "
             "(honest-residual: move to a structured verification-backlog field, or resolve)",
             " | ".join(marker_hits[:3]))

    # --- m5 lint: prose category vs directed class_code -----------------------------------------
    prose_mismatch = []
    for e in edges:
        lead = leading_category(e["feasibility_class"])
        if lead is None:
            continue  # 'Regime-in-transition (...)', 'Blocked at destination (...)', 'Pre-regime (...)'
        if lead != e["class_code"]:
            prose_mismatch.append(
                f"{e['origin']}->{e['destination']} ({e['corridor_id']}): prose leads "
                f"'Category {lead}' but class_code={e['class_code']!r} "
                f"(compatibility_category={e['compatibility_category']!r})")
    if prose_mismatch:
        warn(f"m5  {len(prose_mismatch)} edge(s) whose feasibility_class prose does not lead with "
             "their own DIRECTED class_code (the undirected pair category leaked into the prose)",
             " | ".join(prose_mismatch[:3]))

    # --- m6 lint: keys the schema does not declare ------------------------------------------------
    declared = set(schema.get("properties", {}))
    undeclared = Counter(k for e in edges for k in e if k not in declared)
    if undeclared:
        warn(f"m6  {len(undeclared)} key(s) present in the corpus but not declared by the schema "
             "(additionalProperties is true by design; declare them so the schema documents the corpus)",
             ", ".join(f"{k} x{c}" for k, c in undeclared.most_common(8)))

    # --- m7 lint: Category III edge whose own prose asserts an issuance PROHIBITION (v0.9.99) -----
    # The eighth review's NF-1 (P0). The artifact's origin-drag-first rule (a tokenless origin drags
    # every one of its edges to Category III) CONTRADICTS the published Corridor Atlas v0.2.5 and
    # Feasibility Over Time §3.9, which are destination-first ("EVERY edge terminating in Mainland
    # China is blocked, regardless of origin"; "27 edges are Category III"). The artifact has III=33,
    # and the excess sits on the six tokenless<->tokenless edges. The sharpest symptom: TW->CN and
    # KR->CN are class III ("partnership / coordination route") while their own inbound_mechanism.test
    # says "Issuance and circulation prohibited" -- one edge asserting both a workaround exists and
    # that issuance is banned, in the OPTIMISTIC direction. This is a genuine RULE conflict (which of
    # origin-drag-first / destination-first is canonical) that must be reconciled UPSTREAM (see
    # docs/PAPER_ERRATA.md NF-1); it is deliberately implemented and cascades through OD1/CD1, so it is
    # not silently reclassified here. m7 makes the contradiction mechanically visible instead -- which
    # is why `--strict` is RED on the shipped artifact until the rule is reconciled. That is the
    # honesty discipline working: a real P0 is surfaced, not hidden behind a green badge.
    PROHIB_RE = re.compile(r"prohibit|banned|\bban\b|blocked", re.I)
    m7_hits = []
    for e in edges:
        if e.get("class_code") == "III":
            test = (e.get("inbound_mechanism") or {}).get("test") or ""
            if PROHIB_RE.search(test):
                m7_hits.append(f"{e['origin']}->{e['destination']}: III but test says {test!r}")
    if m7_hits:
        warn(f"m7  {len(m7_hits)} Category III edge(s) whose inbound_mechanism asserts an issuance "
             "PROHIBITION -- III means 'partnership/coordination route', which contradicts a ban "
             "(NF-1). This lint fired on TW->CN and KR->CN through v0.9.99 and turned --strict red; "
             "v0.10.0 FIXED the rule rather than excusing the lint, so it now fires on nothing. The "
             "check remains, and the negative suite still proves it bites.",
             " | ".join(m7_hits[:5]))

    return results, warnings, notes, doc


def report_human(path, results, warnings, notes, doc, strict):
    edges = doc.get("edges", [])
    print("=" * 82)
    print(f"CBSR directed-132 corridor verifier v{__version__}  -  {path}")
    rv = doc.get("register_version")
    print(f"artifact: register_version={rv or 'UNSTAMPED (M2)'}  generated={doc.get('generated')}")
    print("=" * 82)
    passed = 0
    for name, ok, detail in results:
        tag = "PASS" if ok else "FAIL"
        line = f"[{tag}] {name}"
        if not ok and detail:
            line += f"\n         -> {detail}"
        print(line)
        passed += ok
    if warnings:
        print("-" * 82)
        for name, detail in warnings:
            print(f"[{'FAIL' if strict else 'WARN'}] {name}")
            if detail:
                print(f"         -> {detail}")
    if notes:
        print("-" * 82)
        for name, detail in notes:
            print(f"[NOTE] {name}")
            if detail:
                print(f"         {detail}")
    print("-" * 82)
    if edges and all(ok for _, ok, _ in results):
        print(f"class distribution: {dict(sorted(Counter(e['class_code'] for e in edges).items()))}")
        print(f"provenance:         {dict(sorted(Counter(e['materialized_from'] for e in edges).items()))}")
    mode = " (--strict: lints are failures)" if strict else ""
    print(f"{passed}/{len(results)} hard checks passed; {len(warnings)} lint(s){mode}")
    print("=" * 82)


def report_json(path, results, warnings, notes, doc, strict, exit_code):
    edges = doc.get("edges", [])
    payload = {
        "tool": "verify_corridors_directed",
        "tool_version": __version__,
        "artifact": str(path),
        "artifact_generated": doc.get("generated"),
        "artifact_register_version": doc.get("register_version"),
        "artifact_schema": doc.get("schema"),
        "strict": strict,
        "hard_checks": [
            {"id": name.split()[0], "name": name, "passed": ok, "detail": detail or None}
            for name, ok, detail in results
        ],
        "lints": [{"id": name.split()[0], "name": name, "detail": detail or None}
                  for name, detail in warnings],
        "notes": [{"name": n, "detail": d or None} for n, d in notes],
        "hard_checks_passed": sum(ok for _, ok, _ in results),
        "hard_checks_total": len(results),
        "class_distribution": dict(sorted(Counter(e.get("class_code") for e in edges).items())),
        "provenance": dict(sorted(Counter(e.get("materialized_from") for e in edges).items())),
        "guardrail": ("Corridor-layer internal coherence only. This tool does not confirm that any "
                      "jurisdictional fact is a correct statement of law; only primary-source "
                      "verification does. No facts are added or inferred."),
        "exit_code": exit_code,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="verify_corridors_directed.py",
        description="Zero-dependency verifier for the CBSR directed-132 corridor layer.")
    ap.add_argument("artifact", nargs="?", default=str(DEFAULT),
                    help="path to computed_corridors_directed.json")
    ap.add_argument("--strict", action="store_true",
                    help="treat every non-fatal lint (m1/m4/m5/m6/m7) as a failure (release gate)")
    ap.add_argument("--allow-lint", action="append", default=[], metavar="ID",
                    help="under --strict, do NOT promote this lint id to a failure (repeatable). "
                         "For a documented, accepted lint whose fix is upstream, so a NEW lint "
                         "regression still fails the gate while the known one does not block. The "
                         "lint is still printed. No lint currently needs it: --strict is green on "
                         "the shipped artifact from v0.10.0.")
    ap.add_argument("--json", action="store_true",
                    help="emit a machine-readable report instead of the human report")
    args = ap.parse_args(argv)

    path = pathlib.Path(args.artifact)
    results, warnings, notes, doc = run(path)

    allow = set(args.allow_lint)
    blocking_warnings = [w for w in warnings if (w[0].split() or [""])[0] not in allow]
    hard_ok = all(ok for _, ok, _ in results)
    exit_code = 0 if (hard_ok and (not args.strict or not blocking_warnings)) else 1

    if args.json:
        report_json(path, results, warnings, notes, doc, args.strict, exit_code)
    else:
        report_human(path, results, warnings, notes, doc, args.strict)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
