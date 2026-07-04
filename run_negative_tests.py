#!/usr/bin/env python3
"""run_negative_tests.py — the CBSR negative-test battery (shipped, reproducible).

Invariants prove the gates PASS on good data. These prove the gates BITE on bad data: a validation gate
that never rejects anything is not a gate. Each test copies the register to a throwaway temp directory,
introduces one targeted defect there, runs `build.py`, and asserts the build FAILS. The originals are
never modified. Ten distinct gates are exercised — seven in build.py's main(), three in run_invariants.py
(rebuilt, then asserted to reject):

  1. schema-enum             — an out-of-enum binding_status must be rejected by schema validation
  2. binding-status-cap      — a prohibition cell may not claim evidence_tier=resolution_text
  3. citable-integrity       — a resolution_text cell without source.url must be rejected
  4. citable-purity          — an operational entity in a citation (source.primary) must be rejected
  5. verification-ledger-drift — a binding_status that diverges from the committed ledger must be caught
  6. event-gate              — a contingent time-engine event may not carry an effective_date
  7. readme-counts           — a spelled drift-prone count in README must be rejected
  8. version-consistency     — CITATION.cff (machine-authoritative) out of sync with EXPECT_VERSION (V3)
  9. binding-prose-coherence — an enacted-status cell whose prose calls its own instrument un-enacted (B1)
 10. xref-pre-regime         — a note calling ANOTHER jurisdiction pre-regime while its signal disagrees (X1)

Run from the register root:
    python run_negative_tests.py
Exit code 0 iff all gates bite.
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O passes encoding="utf-8" explicitly throughout.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json, shutil, subprocess, tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parent

def read(p):  return p.read_text(encoding="utf-8")
def write(p, s): p.write_text(s, encoding="utf-8")

def yaml_set(path, mutate):
    """Load a YAML record, mutate the dict in place, write it back (UTF-8)."""
    import yaml
    d = yaml.safe_load(read(path))
    mutate(d)
    write(path, yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=110))

def json_set(path, mutate):
    d = json.loads(read(path))
    mutate(d)
    write(path, json.dumps(d, indent=2, ensure_ascii=False))

def build_fails(root):
    """Run build.py in `root`; return True iff it FAILS (non-zero exit or VALIDATION FAILED)."""
    r = subprocess.run([_sys.executable, "build.py"], cwd=str(root),
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode != 0 or "VALIDATION FAILED" in (r.stdout + r.stderr)

def invariants_fail(root):
    """Rebuild so the injected defect reaches dataset.json, then return True iff run_invariants.py
    REJECTS it (non-zero exit). Used for gates that live in run_invariants rather than build.py's main()."""
    subprocess.run([_sys.executable, "build.py"], cwd=str(root), capture_output=True, text=True, encoding="utf-8")
    r = subprocess.run([_sys.executable, "run_invariants.py"], cwd=str(root),
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode != 0

# --- the six defects ---------------------------------------------------------------------------
def t_schema_enum(root):
    yaml_set(root / "us-pss-reserve_backing-001.yaml",
             lambda d: d.__setitem__("binding_status", "totally_not_a_valid_enum_value"))

def t_binding_cap(root):
    def m(d):
        d["evidence_tier"] = "resolution_text"; d["last_reviewed"] = "2026-06-27"
    yaml_set(root / "cn-prc-monetary_sovereignty-001.yaml", m)  # prohibition cell

def t_citable_integrity(root):
    yaml_set(root / "br-vasp-custody-001.yaml",
             lambda d: (d.get("source") or {}).pop("url", None))  # resolution_text cell loses its url

def t_citable_purity(root):
    yaml_set(root / "hk-frs-redemption-001.yaml",
             lambda d: d.setdefault("source", {}).__setitem__(
                 "primary", "Stablecoins Ordinance; Circle launched USDC via Coinbase"))

def t_ledger_drift(root):
    yaml_set(root / "hk-frs-reserve_backing-001.yaml",
             lambda d: d.__setitem__("binding_status", "pending_proposal"))  # ledger says in_force_enacted

def t_event_gate(root):
    json_set(root / "analysis" / "event_calendar.json",
             lambda d: [e.update({"effective_date": "2026-07-01"})
                        for e in d["events"] if e["id"] == "sg-scs-legislation-enacted"])

def t_readme_counts(root):
    # inject a SPELLED drift-prone count -- the house-style regression path a digit-only gate missed
    p = root / "README.md"
    write(p, read(p) + "\n\nSnapshot: the register currently holds one hundred fifty-two verified records.\n")

def t_version_drift(root):
    # roll CITATION.cff (the machine-authoritative version) back out of sync -- the exact drift class
    # where a "bump the version" edit forgets one pointer; V3 must reject it.
    p = root / "CITATION.cff"
    write(p, read(p).replace('version: "0.9.91"', 'version: "0.9.8"'))

def t_prose_incoherence(root):
    # give an enacted-status cell a requirement_summary that describes its own instrument as un-enacted
    # (the Taiwan "label says enacted, body says draft/bill" class); B1 must reject it.
    yaml_set(root / "tw-frs-capital_requirements-001.yaml",  # made_not_commenced after v0.9.9
             lambda d: d.__setitem__("requirement_summary",
                 "DRAFT: capital to be specified by the FSC. No stablecoin capital regime is in force. "
                 "Draft provisions only. STATUS proposed: not operative law."))

def t_xref_pre_regime(root):
    # inject a stale cross-jurisdiction state reference: call Taiwan (signal=transition, after 30 Jun 2026)
    # pre-regime from another jurisdiction's note -- the exact drift class the earlier KR note carried,
    # which the CI reproducibility gate and B1/B3 both miss; X1 must reject it.
    yaml_set(root / "us-pss-reserve_backing-001.yaml",
             lambda d: d.__setitem__("interpretation_note",
                 "US reserve backing rule. Analytically paired with Taiwan as pre-regime."))

TESTS = [
    ("schema-enum             (out-of-enum binding_status)", t_schema_enum, build_fails),
    ("binding-status-cap      (prohibition -> resolution_text)", t_binding_cap, build_fails),
    ("citable-integrity       (resolution_text without source.url)", t_citable_integrity, build_fails),
    ("citable-purity          (operational entity in source.primary)", t_citable_purity, build_fails),
    ("verification-ledger-drift (binding_status diverges from ledger)", t_ledger_drift, build_fails),
    ("event-gate              (contingent event carrying a date)", t_event_gate, build_fails),
    ("readme-counts           (spelled drift-prone count in README)", t_readme_counts, build_fails),
    ("version-consistency     (CITATION.cff version out of sync)", t_version_drift, invariants_fail),
    ("binding-prose-coherence (enacted cell, un-enacted prose)", t_prose_incoherence, invariants_fail),
    ("xref-pre-regime         (note calls another jurisdiction pre-regime; signal disagrees)", t_xref_pre_regime, invariants_fail),
]

def main():
    work = Path(tempfile.mkdtemp(prefix="cbsr_negtest_"))
    reg = work / "register"
    try:
        shutil.copytree(SRC, reg, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        # sanity: the clean copy must BUILD GREEN before we start breaking it
        clean_ok = not build_fails(reg)
        print("CBSR negative-test battery — validating that the gates BITE\n" + "=" * 64)
        print(("  clean copy builds green: " + ("yes" if clean_ok else "NO (abort)")))
        if not clean_ok:
            print("Cannot run negative tests: the pristine copy does not build."); return 1
        bit = 0
        for name, fn, checker in TESTS:
            # snapshot the whole record set so each test is independent and self-restoring
            snap = {p: read(p) for p in list(reg.glob("*.yaml"))
                    + [reg / "analysis" / "event_calendar.json", reg / "README.md", reg / "CITATION.cff"]}
            fn(reg)
            ok = checker(reg)
            bit += ok
            print(("  " + ("BIT  " if ok else "MISS ") + name))
            for p, s in snap.items():  # restore
                write(p, s)
        print("=" * 64)
        print("RESULT: %d/%d gates bit." % (bit, len(TESTS))
              + ("  All negative tests BITE — the validation gates are live."
                 if bit == len(TESTS) else "  (%d gate(s) DID NOT bite)" % (len(TESTS) - bit)))
        return 0 if bit == len(TESTS) else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)

if __name__ == "__main__":
    _sys.exit(main())
