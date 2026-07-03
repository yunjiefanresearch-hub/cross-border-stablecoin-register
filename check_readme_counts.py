#!/usr/bin/env python3
"""
check_readme_counts — the README<->build drift gate (CBSR).

WHY THIS EXISTS
---------------
README.md is the project's front page. Historically it was the ONE document outside the
validation-gate net, and it drifted: its embedded coverage matrix, its per-jurisdiction depth row,
its citable count, and its "typed tools" count all fell behind the build that generates COVERAGE.md /
dataset.json / MCP_SERVER.md, while its header still claimed the current version. A reference whose
entire thesis is "counts must not drift" cannot ship a front page that silently drifts.

The fix (decided with the maintainer) is structural, not a one-time correction:
  (1) README states NO drift-prone number; every drift-prone quantity lives only in its generated
      source, and README points to it. (Done in README.md.)
  (2) This gate FORBIDS a drift-prone count from being copied back into README -- so the failure mode
      is closed permanently, not just for today. It is integrated into build.py and the shipped
      invariant + negative-test suites, exactly like the data gates.

DESIGN PRINCIPLE -- ban the VOCABULARY AND SHAPE of a coverage assertion, never the bare integer.
A naive gate that blacklists the integers 152 / 46 / 132 would misfire on dates (2026), DOIs
(10.5281/zenodo.20730358), version strings (v0.4.0), Article numbers (58(3)), section refs (section 5.14),
and -- the sharpest trap -- legal-instrument numbers like UK "SI 2026/102". A gate that misfires gets
overridden by frustrated contributors, which is worse than no gate. So this gate matches the *shape of
a drift-prone assertion* (a coverage glyph, a dimension-keyed coverage table, or a labelled
coverage / tool / edge / substrate count, in DIGITS OR SPELLED-OUT WORDS) and carries explicit
carve-outs, verified by a self-test.

COMPLETENESS (v2 -- the three coverage gaps a maintainer stress-test surfaced, now closed):
  (1) SPELLED-OUT numbers are caught, not just digits. The portfolio's house style is spelled
      ("one hundred fifty-two records", "forty-six"), so the most likely regression path -- pasting
      paper prose into README -- went through spelled numbers, which a digit-only gate missed. The
      spelled noun-set deliberately EXCLUDES identity nouns (jurisdictions / dimensions / spines /
      constraints / interaction sets / edge) so the scope sentence ("twelve focus jurisdictions ...
      one-hundred-thirty-two-edge space") is never tripped, and excludes a bare leading "one" so
      rate phrasings ("one worked profile per corridor", "one verified (jurisdiction x ...) fact")
      are never tripped.
  (2) The coverage-noun set includes `poles` and `events` (both appear in the project's version
      history: "58 substrate poles", "time engine 4 -> 6 events").
  (3) Scalar + ratio patterns run on a newline-normalized (offset-preserving) copy, so a count split
      across README's hard line wraps ("152 verified\\nrecords") is caught. Glyph and matrix checks
      stay line-based (they are line phenomena by nature).

STATIC IDENTITY (allowed in README, as prose -- never tripped):
  twelve jurisdictions . fifteen dimensions . two doctrinal spines . eight constraints . six interaction sets
  . seven Atlas section-8 personas . the one-hundred-thirty-two-edge directed space . "one ... per ..." rates.
  These change only on a headline framework release, never silently, and several have no clean scalar
  key in dataset.json, so enforcing them would cost machinery for ~zero benefit. They are deliberately
  OUT of scope. The maintainer's outward claim is the honest, strong one: "README states no number
  that can silently drift; every drift-prone quantity is build-generated, and the build forbids it
  from being restated in README."

VERIFICATION STATUS
  Integrated and run against the register: build.py calls check_readme_counts() in main(); the
  shipped invariant suite asserts README is clean; the shipped negative-test battery proves the gate
  bites (it injects each forbidden shape into a copy of README and asserts the build fails) and that
  the carve-outs are safe. The self-test below (`python check_readme_counts.py`) exercises the same
  matrix standalone, and `python check_readme_counts.py --scan README.md` runs the gate against a
  specific file by hand (exit 0 if clean, 1 if a drift-prone assertion is found), which is the same
  check build.py performs in CI. Run `python build.py && python run_invariants.py &&
  python run_negative_tests.py` in the repo/CI to reconfirm on your runner.
"""

import re

# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, the coverage glyphs printed
# by the self-test) renders on any locale (e.g. Windows GBK/cp1252). This module does no file I/O of
# its own (it takes README text as a string), so there is nothing else to encode.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ---- dimension abbreviations that, clustered in a markdown table row, signal a coverage matrix ------
_DIM_ABBREVS = {
    "Auth", "Issu", "Resv", "Cap", "Yield", "Sec", "Rout", "Redm",
    "Cust", "AML", "XB", "MonSov", "Disc", "Dist", "Impl",
}

# ---- coverage nouns: the head-nouns a DIGIT count attaches to (includes poles, events) --------------
_COVERAGE_NOUN = (r"records?|corridors?|categor(?:y|ies)|edges?|cells?|pairs?|skeletons?|"
                  r"profiles?|gates?|invariants?|tools?|poles?|events?")

# ---- coverage nouns for SPELLED numbers: identical BUT WITHOUT `edges?` -----------------------------
# (the only spelled "...-edge..." string in legitimate use is the identity "one-hundred-thirty-two-edge";
#  a spelled edge COUNT never occurs, so dropping edges here removes the sole identity false-positive.)
_COVERAGE_NOUN_SPELLED = (r"records?|corridors?|categor(?:y|ies)|cells?|pairs?|skeletons?|"
                          r"profiles?|gates?|invariants?|tools?|poles?|events?")

# adjectives that may sit between the number and the coverage noun
_ADJ = r"(?:verified|substrate|authored|computed|directed|total|distinct|typed|citable)"

# ---- spelled-out English number words ---------------------------------------------------------------
_NW = (r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
       r"sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|"
       r"hundred|thousand)")
# A spelled number that can introduce a COUNT: a compound (>=2 number words), OR a single cardinal/ten
# from two..ninety. A bare leading "one" and a bare "hundred"/"thousand" are excluded so that
# "one ... per ..." rates and singular-identity phrasings are never treated as counts.
_NW_SINGLE = (r"(?:two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
              r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
              r"eighty|ninety)")
_SPELLED_NUM = r"(?:" + _NW + r"(?:[\s-]+(?:and[\s-]+)?" + _NW + r")+|" + _NW_SINGLE + r")"

# ---- labelled scalar counts in DIGITS (shape: <int> [adj] <coverage-noun>, or the named labels) -----
_LABELLED_PATTERNS = [
    (re.compile(r"\b\d+\s+(?:verified\s+)?records\b", re.I),
     "a record count ('N records')"),
    (re.compile(r"\b\d+\s+citable\b", re.I),
     "a citable count ('N citable')"),
    (re.compile(r"\bcitable\b[^.\n]{0,40}?\b\d+\b", re.I),
     "a citable-subset count ('citable ... N')"),
    (re.compile(r"Per-jurisdiction\s+depth\s*:", re.I),
     "the per-jurisdiction depth row"),
    (re.compile(r"\b(?:resolution_text|firm_summary|mixed|unset)\s+\d+\b", re.I),
     "an evidence-tier count ('resolution_text N')"),
    (re.compile(r"\b\d+\s+(?:typed\s+)?tools?\b", re.I),
     "a tool count ('N typed tools')"),
    (re.compile(r"\b\d+\s+(?:authored\s+|computed\s+|directed\s+)?(?:" + _COVERAGE_NOUN +
                r")\s+\w*(?:reproduc|deriv|verif|populat|cover)", re.I),
     "a coverage count ('N corridors reproduced', 'N cells populated', ...)"),
    (re.compile(r"\b\d+\s+(?:substrate\s+)?poles?\b", re.I),
     "a substrate-pole count ('N poles')"),
    (re.compile(r"\b\d+\s+events?\b", re.I),
     "an event count ('N events')"),
    (re.compile(r"\b\d+\s+invariants?\b", re.I),
     "an invariant count ('N invariants')"),
    (re.compile(r"\b\d+\s+negative\s+tests?\b", re.I),
     "a negative-test count ('N negative tests')"),
    (re.compile(r"\b\d+(?:\s*/\s*\d+)?\s+gates?\s+bit\b", re.I),
     "a gate-bite count ('N/M gates bit')"),
]

# ---- labelled scalar counts SPELLED OUT (same shapes, spelled numbers, identity nouns excluded) -----
_SPELLED_PATTERNS = [
    (re.compile(r"\b(?:" + _SPELLED_NUM + r")(?:[\s-]+" + _ADJ + r")?[\s-]+(?:" +
                _COVERAGE_NOUN_SPELLED + r")\b", re.I),
     "a spelled-out coverage/tool count ('forty-six records', 'six events', ...)"),
    (re.compile(r"\b(?:" + _SPELLED_NUM + r")[\s-]+citable\b", re.I),
     "a spelled citable count ('forty-six citable')"),
]

# ---- ratio counts (shape: A/B <coverage-noun>) with the SI-number / year carve-out -----------------
_RATIO = re.compile(r"\b(\d+)\s*/\s*(\d+)\b(?P<tail>[^.\n]{0,24})", re.I)
_RATIO_TAIL_NOUN = re.compile(r"\b(?:" + _COVERAGE_NOUN + r")\b", re.I)

# ---- coverage glyphs --------------------------------------------------------------------------------
_GLYPHS = ("\u2705", "\u2b1c")  # check, white-square


def _looks_like_year(n: int) -> bool:
    return 1900 <= n <= 2100


def check_readme_counts(readme_text, *, filename="README.md"):
    """Return a list of error strings: drift-prone coverage assertions found in README.

    Matches assertion SHAPE (glyph / matrix-row / labelled count in digits or words / coverage ratio),
    not bare integers. Carve-outs (verified by _self_test): dates, DOIs, version strings, Article
    numbers, section references, spelled identity constants, "one ... per ..." rates, and legal-
    instrument numbers such as 'SI 2026/102' do NOT trip the gate.
    """
    errors = []
    lines = readme_text.splitlines()

    # 1) coverage glyphs anywhere (line phenomenon)
    for i, line in enumerate(lines, 1):
        for g in _GLYPHS:
            if g in line:
                errors.append(f"{filename}:{i}: contains a coverage glyph ({g!r}) -- coverage glyphs "
                              f"belong in COVERAGE.md, not in README prose")
                break

    # 2) a coverage-matrix-shaped table row: a markdown table row holding >=3 dimension abbreviations
    for i, line in enumerate(lines, 1):
        if "|" not in line:
            continue
        cells = {c.strip().strip("*`") for c in line.split("|")}
        hits = cells & _DIM_ABBREVS
        if len(hits) >= 3:
            errors.append(f"{filename}:{i}: looks like a coverage matrix (table row keyed by dimension "
                          f"abbreviations {sorted(hits)}) -- the matrix is generated into COVERAGE.md")

    # 3+4) labelled scalar counts (digits AND spelled) + coverage ratios, on a newline-normalized,
    #      OFFSET-PRESERVING copy so a count split across hard line wraps is still caught. Replacing
    #      '\n' (one char) with ' ' (one char) preserves every offset, so we can map a match back to
    #      its original line by counting newlines before its start offset.
    norm = readme_text.replace("\n", " ")

    def line_of(off):
        return readme_text.count("\n", 0, off) + 1

    for pat, what in (_LABELLED_PATTERNS + _SPELLED_PATTERNS):
        for m in pat.finditer(norm):
            errors.append(f"{filename}:{line_of(m.start())}: states {what} -- {m.group(0).strip()!r}; "
                          f"drift-prone counts are generated (COVERAGE.md / dataset.json / "
                          f"MCP_SERVER.md), not restated in README")

    for m in _RATIO.finditer(norm):
        a, b = int(m.group(1)), int(m.group(2))
        tail = m.group("tail")
        if not _RATIO_TAIL_NOUN.search(tail):
            continue                      # no coverage noun after the ratio -> not a coverage ratio
        if a > b:
            continue                      # 'SI 2026/102 cells': numerator > denominator -> instrument no.
        if _looks_like_year(a) or b >= 1000:
            continue                      # year numerator, or implausibly large denominator -> not coverage
        errors.append(f"{filename}:{line_of(m.start())}: states a coverage ratio "
                      f"({m.group(1)}/{m.group(2)}{tail.rstrip()!r}) -- corridor/edge/cell coverage is "
                      f"generated into dataset.json, not restated in README")

    return errors


# =====================================================================================================
# INTEGRATION (this is what was actually applied to the register; reproduce on your runner)
# =====================================================================================================
#
# (a) build.py -- in main(), after `errors += check_verification_ledger(recs, analysis)` and before the
#     `if errors:` block, read the README from the repo root and run the gate:
#
#         readme_path = ROOT / "README.md"
#         if readme_path.exists():
#             errors += check_readme_counts(readme_path.read_text(encoding="utf-8"))
#
#     (Paste the patterns + check_readme_counts() into build.py next to check_citable_purity(), or
#     `from check_readme_counts import check_readme_counts` if you ship this as a module.)
#
# (b) run_invariants.py -- one read-only invariant in the suite:
#
#         from check_readme_counts import check_readme_counts
#         _readme = (ROOT / "README.md").read_text(encoding="utf-8")
#         inv("R1  README.md states no drift-prone coverage/tool/edge count (digits or spelled)",
#             not check_readme_counts(_readme),
#             " | ".join(check_readme_counts(_readme)))
#
# (c) run_negative_tests.py -- a 7th gate, proving the README gate BITES (and carve-outs are safe):
#
#         def neg_readme_counts_gate_bites(tmp):
#             readme = SRC / "README.md"
#             assert not check_readme_counts(read(readme)), "real README should pass the counts gate"
#             injections = [
#                 "\nSnapshot: 152 verified records across the focus set.\n",      # digit scalar
#                 "\nCitable subset is forty-six records today.\n",                # SPELLED scalar
#                 "\nThe time engine holds six events.\n",                         # SPELLED + 'events' noun
#                 "\nPer-jurisdiction depth: CH 12, US 9, EU 8.\n",                # depth row
#                 "\nThe register wraps the dataset in 23 typed tools.\n",         # tool count (the real drift)
#                 "\nThe substrate derives 124/132 directed edges.\n",            # coverage ratio
#                 "\nThe register holds 152 verified\nrecords.\n",                 # CROSS-LINE scalar
#                 "\n| US | check | white |\n".replace("check","\u2705").replace("white","\u2b1c"),  # glyphs
#                 "\n| Juris | Auth | Issu | Resv | Yield |\n",                    # dimension-keyed matrix header
#             ]
#             for inj in injections:
#                 assert check_readme_counts(read(readme) + inj), f"gate failed to bite on: {inj!r}"
#             carveouts = (
#                 "UK SI 2026/102 cells; DOI 10.5281/zenodo.20730358; MiCA Article 58(3); v0.4.0; "
#                 "twelve jurisdictions, fifteen dimensions, two doctrinal spines, eight constraints, "
#                 "six interaction sets, seven Atlas personas, the one-hundred-thirty-two-edge space; "
#                 "one worked profile per authored corridor; each record is one verified fact; "
#                 "not a '200-country' tracker."
#             )
#             assert not check_readme_counts(carveouts), "carve-outs wrongly tripped the counts gate"
#
#     Wire it into the runner's gate list exactly as the existing six are wired.
# =====================================================================================================


def _self_test():
    """Standalone proof the gate bites AND that the carve-outs are safe. Run: python check_readme_counts.py"""
    bite = {
        "record count (digit)":     "Snapshot: 152 verified records.",
        "record count (spelled)":   "the register holds one hundred fifty-two verified records.",
        "citable count (digit)":    "Citable subset is 46 records.",
        "citable count (spelled)":  "the citable subset is forty-six records.",
        "citable adj (spelled)":    "the build enforces forty-six citable records.",
        "citable bare (spelled)":   "the subset is forty-six citable.",
        "depth row":                "Per-jurisdiction depth: CH 12, US 9, EU 8.",
        "tool count (digit)":       "wraps the dataset in 23 typed tools.",
        "tool count (spelled)":     "wraps the dataset in twenty-three typed tools.",
        "poles (spelled)":          "the substrate carries fifty-eight substrate poles.",
        "events (spelled)":         "the time engine holds six events.",
        "ratio":                    "derives 124/132 directed edges.",
        "tier breakdown":           "resolution_text 48 - mixed 14 - unset 27.",
        "glyph":                    "| US | \u2705 | \u2b1c |",
        "matrix header":            "| Juris | Auth | Issu | Resv | Yield |",
        "corridors reproduced":     "reproduces 9 corridors derived from first principles.",
        "invariants":               "run_invariants.py -> 33 invariants hold.",
        "gates bit (numbered)":     "run_negative_tests.py -> 6/6 gates bit.",
        "cross-line scalar":        "the register holds 152 verified\nrecords.",
    }
    for name, text in bite.items():
        errs = check_readme_counts(text, filename="<bite>")
        assert errs, f"FAIL: gate did not bite on {name!r}: {text!r}"

    safe = {
        "UK SI number":     "UK SI 2026/102 cells stay below resolution_text; commences 2027-10-25.",
        "DOI":              "Cite the DOI 10.5281/zenodo.20730358 of the version you used.",
        "Article number":   "MiCA Article 58(3) applies the Art. 23 thresholds mutatis mutandis.",
        "section ref":      "see section 5.14 and 7.1-7.5 for the open questions.",
        "version":          "v0.4.0 is the twelve-jurisdiction expansion; status v0.9.8.",
        "200-country":      "not another broad, shallow '200-country' tracker.",
        "spelled scope":    "twelve jurisdictions, fifteen dimensions, two doctrinal spines, eight constraints, six interaction sets.",
        "spelled edges id": "the one-hundred-thirty-two-edge directed space (twelve jurisdictions).",
        "seven personas":   "the seven Atlas section-8 personas: issuer, distributor, custodian, ...",
        "one-per rate":     "one worked profile per authored corridor x persona.",
        "one verified fact":"each record is one verified (jurisdiction x instrument x dimension) fact.",
        "SI with /132":     "a hypothetical SI 2031/132 reference cells",   # numerator>denominator -> safe
        "qualitative gates":'run_negative_tests.py -> "every gate bit".',     # numberless -> allowed
        "qualitative inv":  'run_invariants.py -> "all invariants hold".',    # numberless -> allowed
        "three-layer arch": "the three-layer routing architecture with the five-factor operational test.",
    }
    for name, text in safe.items():
        errs = check_readme_counts(text, filename="<safe>")
        assert not errs, f"FAIL: gate wrongly tripped on {name!r}: {text!r} -> {errs}"

    print("check_readme_counts self-test: OK -- bites on all drift-prone shapes (digit, spelled, "
          "cross-line); safe on all carve-outs (SI numbers, DOI, dates, versions, spelled identity, "
          "one-per rates).")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        prog="check_readme_counts",
        description=("README<->build drift gate. With no arguments, runs the self-test. "
                     "With --scan PATH, scans the given file for drift-prone coverage assertions "
                     "and exits non-zero if any are found (the same check build.py runs in CI)."),
    )
    parser.add_argument(
        "--scan", metavar="PATH", default=None,
        help="scan PATH (e.g. README.md) for drift-prone coverage assertions and report them",
    )
    args = parser.parse_args()

    if args.scan is None:
        _self_test()
    else:
        try:
            with open(args.scan, encoding="utf-8") as _fh:
                _text = _fh.read()
        except OSError as _exc:
            print(f"check_readme_counts: cannot read {args.scan!r}: {_exc}", file=sys.stderr)
            sys.exit(2)
        _errs = check_readme_counts(_text, filename=args.scan)
        if _errs:
            print(f"check_readme_counts: {len(_errs)} drift-prone coverage assertion(s) "
                  f"in {args.scan}:")
            for _e in _errs:
                print(f"  {_e}")
            sys.exit(1)
        print(f"check_readme_counts: OK -- {args.scan} contains no drift-prone "
              f"coverage assertions.")
        sys.exit(0)
