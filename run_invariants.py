#!/usr/bin/env python3
"""run_invariants.py — the CBSR structural invariant suite (shipped, reproducible).

These are read-only assertions over the built register (dataset.json, the record YAMLs, and the
analysis/*.json computed layers). They are the standing properties the build is supposed to preserve;
unlike build.py's internal gates (which fail the build), this prints an explicit, countable pass/fail
report so "N invariants hold" is a concrete, runnable claim rather than a number in prose.

Run from the register root AFTER a build:
    python build.py && python run_invariants.py
Exit code 0 iff every invariant holds.
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O passes encoding="utf-8" explicitly throughout.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json, glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECT_VERSION = "0.9.9"

def load_json(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

# --- load the built register -------------------------------------------------------------------
# These artifacts are produced by build.py. If they are absent (for instance, this file was copied
# into a portfolio slice without the dataset), fail with a controlled message and a non-zero exit
# rather than an uncaught traceback, the same way run_negative_tests.py aborts when its pristine
# copy will not build. A self-disciplining project should have controlled failure messages too.
_REQUIRED = ["dataset.json", "analysis/verification_ledger.json", "analysis/computed_compatibility.json",
             "analysis/computed_timeline.json", "analysis/computed_substrate.json",
             "analysis/computed_corridor_skeletons.json"]
_missing = [p for p in _REQUIRED if not (ROOT / p).exists()]
if _missing:
    print("Cannot run invariants: the built register was not found in this directory.")
    print("  missing: " + ", ".join(_missing))
    print("  These invariants are read-only assertions over a built register; run from the")
    print("  register root after a build:  python build.py && python run_invariants.py")
    _sys.exit(1)

ds = load_json("dataset.json")
records = [r for r in ds.get("records", []) if isinstance(r, dict) and "id" in r]
byid = {r["id"]: r for r in records}
an = ds.get("analysis", {})
ledger = load_json("analysis/verification_ledger.json")
comp = load_json("analysis/computed_compatibility.json")
timeline = load_json("analysis/computed_timeline.json")
substrate = load_json("analysis/computed_substrate.json")
skeletons = load_json("analysis/computed_corridor_skeletons.json")

BLOCKED = {"prohibition", "no_regime", "pending_proposal", "made_not_commenced", "finalized_policy_pending"}
BINDING_ENUM = {"in_force_enacted", "made_not_commenced", "finalized_policy_pending",
                "pending_proposal", "prohibition", "no_regime"}
TIER_ENUM = {"resolution_text", "mixed", "firm_summary", "unset"}

results = []
def inv(name, cond, detail=""):
    results.append((bool(cond), name, "" if cond else detail))

def src(r):
    return r.get("source") or {}

# === STRUCTURE & AXES ==========================================================================
inv("S1  dataset has 152 records", len(records) == 152, f"got {len(records)}")
inv("S2  every record carries a valid binding_status",
    all(r.get("binding_status") in BINDING_ENUM for r in records),
    str([r["id"] for r in records if r.get("binding_status") not in BINDING_ENUM][:5]))
cc = {}
for r in records: cc[r.get("claim_class")] = cc.get(r.get("claim_class"), 0) + 1
inv("S3  claim_class split is 143 tier1_legal / 9 tier2_operational",
    cc.get("tier1_legal") == 143 and cc.get("tier2_operational") == 9, str(cc))
inv("S4  every record has a valid evidence_tier",
    all((r.get("evidence_tier") or "unset") in TIER_ENUM for r in records))

# === CITABILITY DISCIPLINE =====================================================================
rt = [r for r in records if r.get("evidence_tier") == "resolution_text"]
inv("C1  every resolution_text cell is binding_status=in_force_enacted (the cap)",
    all(r.get("binding_status") == "in_force_enacted" for r in rt),
    str([r["id"] for r in rt if r.get("binding_status") != "in_force_enacted"][:5]))
inv("C2  no blocked-binding cell is resolution_text",
    all(r.get("binding_status") not in BLOCKED for r in rt))
inv("C3  every resolution_text cell has url + pinpoint + last_reviewed",
    all(src(r).get("url") and src(r).get("pinpoint") and r.get("last_reviewed") for r in rt),
    str([r["id"] for r in rt if not (src(r).get("url") and src(r).get("pinpoint") and r.get("last_reviewed"))][:5]))
fs = [r for r in records if r.get("evidence_tier") == "firm_summary"]
inv("C4  every firm_summary cell has source.pinpoint",
    all(src(r).get("pinpoint") for r in fs),
    str([r["id"] for r in fs if not src(r).get("pinpoint")][:5]))
citable = [r for r in records if r.get("claim_class") == "tier1_legal"
           and r.get("status") == "in_force" and r.get("evidence_tier") == "resolution_text"]
inv("C5  citable subset == 46", len(citable) == 46, f"got {len(citable)}")
inv("C6  dataset.citable_subset.count agrees with the recomputed set",
    ds.get("citable_subset", {}).get("count") == len(citable),
    f"dataset={ds.get('citable_subset',{}).get('count')} recomputed={len(citable)}")

# === VERIFICATION LEDGER =======================================================================
inv("L1  ledger schema + version", ledger.get("schema") == "cbsr/verification_ledger"
    and ledger.get("version") == f"v{EXPECT_VERSION}", f"version={ledger.get('version')}")
led_entries = ledger.get("entries", [])
drift = [e for e in led_entries if e.get("id") in byid
         and e.get("binding_status") and byid[e["id"]].get("binding_status") != e["binding_status"]]
inv("L2  no ledger drift (every committed binding_status matches the live record)", not drift,
    str([(e["id"], e.get("binding_status"), byid[e["id"]].get("binding_status")) for e in drift][:5]))

# === ANALYSIS / COMPUTED LAYERS ================================================================
inv("A1  analysis layer present (66 pairs, 6 interaction sets, 5 open questions)",
    len(an.get("compatibility", {}).get("pairs", [])) == 66
    and len(an.get("interaction_sets", {}).get("sets", [])) == 6
    and len(an.get("open_questions", {}).get("questions", [])) == 5,
    f"pairs={len(an.get('compatibility',{}).get('pairs',[]))} "
    f"sets={len(an.get('interaction_sets',{}).get('sets',[]))} "
    f"oq={len(an.get('open_questions',{}).get('questions',[]))}")
inv("A2  substrate 80/96 cells, cross-check clean",
    substrate.get("coverage", {}).get("cells_populated") == 80 and substrate.get("cross_check", {}).get("clean") is True,
    str(substrate.get("coverage", {}).get("cells_populated")))
inv("A3  edge layer 124/132 with a record, cross-check clean",
    skeletons.get("coverage", {}).get("edges_with_a_record") == 124
    and skeletons.get("cross_check", {}).get("clean") is True,
    str(skeletons.get("coverage", {})))
prc = comp.get("pre_regime_crosscheck", {})
inv("A4  pre_regime cross-check is {KR} (TW now enacted-not-commenced), consistent",
    prc.get("consistent") is True
    and sorted(prc.get("from_signals", [])) == ["KR"]
    and sorted(prc.get("from_records", [])) == ["KR"],
    f"signals={prc.get('from_signals')} records={prc.get('from_records')} consistent={prc.get('consistent')}")

# === TIME ENGINE ===============================================================================
events = an.get("event_calendar", {}).get("events", [])
inv("T1  event calendar has 7 events, provenance clean",
    len(events) == 7 and timeline.get("event_provenance", {}).get("clean") is True, f"events={len(events)}")
inv("T2  every event is tier1_legal; contingent events carry no effective_date",
    all(e.get("claim_class") == "tier1_legal" for e in events)
    and all(not e.get("effective_date") for e in events if e.get("status") == "contingent"))
legend_kinds = set((an.get("event_calendar", {}).get("trigger_kind_legend", {}).get("kinds", {})).keys())
inv("T2b every event's trigger_kind is defined in the trigger_kind_legend",
    bool(legend_kinds) and all(e.get("trigger_kind") in legend_kinds for e in events),
    f"kinds={sorted(legend_kinds)} events={sorted({e.get('trigger_kind') for e in events})}")
ot = timeline.get("undirected_agreement_over_time", [])
inv("T3  UK transition caveat: 8 today -> 0 at the 2027-10-25 horizon",
    ot and ot[0]["transition_caveated_pairs"]["count"] == 8
    and ot[-1]["transition_caveated_pairs"]["count"] == 0 and ot[-1]["as_of"] == "2027-10-25",
    f"first={ot[0]['transition_caveated_pairs']['count'] if ot else '?'} "
    f"last={ot[-1]['transition_caveated_pairs']['count'] if ot else '?'}@{ot[-1]['as_of'] if ot else '?'}")
dated = {e["effective_date"] for e in events if e.get("effective_date")}
horizons = {x["as_of"] for x in ot}
inv("T4  compose horizons are exactly the dated events (no contingent date leaked in)",
    horizons <= (dated | {ot[0]["as_of"]}) and all(h in dated or h == ot[0]["as_of"] for h in horizons),
    f"horizons={sorted(horizons)} dated={sorted(dated)}")

# === v0.9.7 NATIVE-LANGUAGE PASS ===============================================================
br_rt = [i for i in byid if i.startswith("br-vasp-") and byid[i].get("evidence_tier") == "resolution_text"]
inv("N1  BR: exactly 10 resolution_text cells, each with url+pinpoint",
    len(br_rt) == 10 and all(src(byid[i]).get("url") and src(byid[i]).get("pinpoint") for i in br_rt),
    f"count={len(br_rt)}")
bry = byid.get("br-vasp-permitted_activity_yield-001", {})
inv("N2  BR yield: in_force_enacted + firm_summary + pass-through unsettled noted",
    bry.get("binding_status") == "in_force_enacted" and bry.get("evidence_tier") == "firm_summary"
    and "pass-through" in (bry.get("interpretation_note") or "").lower())
cn4 = ["cn-prc-monetary_sovereignty-001", "cn-prc-issuer_pathway-001",
       "cn-prc-regulatory_authority-001", "cn-prc-securities_classification-001"]
inv("N3  CN: the 4 directly-addressed cells all cite 银发〔2026〕42号",
    all("银发〔2026〕42号" in json.dumps(byid.get(i, {}), ensure_ascii=False) for i in cn4))
cn_all = [i for i in byid if i.startswith("cn-prc-")]
inv("N4  CN: no cell summary contains 'verbal' or 'remain in force'",
    all("verbal" not in (byid[i].get("requirement_summary") or "")
        and "remain in force" not in (byid[i].get("requirement_summary") or "") for i in cn_all),
    str([i for i in cn_all if "verbal" in (byid[i].get("requirement_summary") or "")][:5]))
inv("N5  CN: every prohibition-binding cell stays prohibition (no re-classification)",
    all(byid[i].get("binding_status") == "prohibition" for i in cn4))
inv("N6  CN C7 carries the written RMB-pegged-stablecoin overseas-issuance ban quote",
    "不得在境外发行挂钩人民币的稳定币" in json.dumps(byid.get("cn-prc-monetary_sovereignty-001", {}), ensure_ascii=False))
krs = byid.get("kr-frs-implementation_status-001", {}).get("requirement_summary", "")
inv("N7  KR: '12 May'/'off the subcommittee' removed; 51% dispute added; DABA cells stay pending_proposal",
    "12 May" not in krs and "off the subcommittee" not in krs
    and ("51%" in krs or "issuer-eligibility" in krs)
    and byid.get("kr-frs-issuer_pathway-001", {}).get("binding_status") == "pending_proposal")
twa = byid.get("tw-frs-aml_kyc-001", {})
inv("N8  TW: aml_kyc resolution_text on the MOJ text; issuer_pathway now made_not_commenced (enacted, not commenced)",
    twa.get("evidence_tier") == "resolution_text" and "law.moj.gov.tw" in (src(twa).get("url") or "")
    and byid.get("tw-frs-issuer_pathway-001", {}).get("binding_status") == "made_not_commenced")
evd = {e["id"]: e for e in events}
inv("N9  KR/TW contingent events note their differing procedural stages",
    "51%" in (evd.get("kr-daba-enacted", {}).get("date_basis") or "")
    and "初審" in (evd.get("tw-vas-act-enacted", {}).get("date_basis") or ""))

# === v0.9.8 SOURCE-LAYER CURRENCY (matrix / architecture / corridor reflect the 42号 reality) ====
corridors = {c.get("corridor_id"): c for c in ds.get("corridors", []) if isinstance(c, dict)}
inv("D1  matrix: the §5.14 PRC prohibition axis cites 银发〔2026〕42号",
    "银发〔2026〕42号" in (an.get("compatibility", {}).get("category_iii_axes", {}).get("prohibition") or ""))
ap_boundary = an.get("architectural_patterns", {}).get("prc_three_pattern_typology", {}).get("boundary") or ""
inv("D2  architecture: the PRC boundary cites 42号 and drops the 'no single explicit prohibition' framing",
    "银发〔2026〕42号" in ap_boundary and "not by any single explicit prohibition" not in ap_boundary)
cn_c1_note = an.get("constraint_substrate", {}).get("cells", {}).get("CN", {}).get("C1", {}).get("note") or ""
inv("D3  substrate: CN C1 note cites 42号 and no longer asserts the 2021 framework is in force",
    "银发〔2026〕42号" in cn_c1_note and "PBOC framework in force" not in cn_c1_note)
hkcn = corridors.get("hk-cn-hkd-cny-blocked", {})
inv("D4  corridor hk-cn: the blocked-destination mechanism cites 42号",
    "银发〔2026〕42号" in json.dumps(hkcn, ensure_ascii=False))
hkbr = corridors.get("hk-br-usd-stablecoin-settlement-001") or corridors.get("hk-br-usd-stablecoin-settlement", {})
inv("D5  corridor hk-br: no empty record_refs remain marked 'forthcoming'/'GAP' for existing records",
    "forthcoming)" not in json.dumps(hkbr, ensure_ascii=False)
    and "GAP: write hk-frs-securities_classification" not in json.dumps(hkbr, ensure_ascii=False))
q72 = next((q for q in an.get("open_questions", {}).get("questions", []) if q.get("id") == "7.2"), {})
inv("D6  open question 7.2 records the Feb-2026 written tightening (42号)",
    "银发〔2026〕42号" in json.dumps(q72, ensure_ascii=False))

# === PORTABILITY (the v0.9.7 engineering fix) ==================================================
py_files = sorted(glob.glob(str(ROOT / "*.py")) + glob.glob(str(ROOT / "scripts" / "*.py")))
def io_calls_have_encoding(text):
    for m in re.finditer(r"\.(read_text|write_text)\(", text):
        i = m.end() - 1; depth = 0; j = i; n = len(text)
        while j < n:
            c = text[j]
            if c in "\"'":
                q = c
                if text[j:j+3] == q*3:
                    k = text.find(q*3, j+3); j = (k+3) if k != -1 else n; continue
                j += 1
                while j < n:
                    if text[j] == "\\": j += 2; continue
                    if text[j] == q: j += 1; break
                    j += 1
                continue
            if c == "(": depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0: break
            j += 1
        if "encoding=" not in text[m.start():j+1]:
            return False
    return True
all_enc = all(io_calls_have_encoding(Path(f).read_text(encoding="utf-8")) for f in py_files)
inv("P1  every read_text/write_text in the shipped scripts passes encoding=\"utf-8\"", all_enc)
all_recfg = all("force UTF-8 for console output" in Path(f).read_text(encoding="utf-8") for f in py_files)
inv("P2  every shipped script has the guarded UTF-8 stdout/stderr reconfigure", all_recfg)

# === VERSION ===================================================================================
build_src = (ROOT / "build.py").read_text(encoding="utf-8")
inv("V1  REGISTER_VERSION == 0.9.9 in build.py", f'REGISTER_VERSION = "{EXPECT_VERSION}"' in build_src)
inv("V2  dataset.register_version == 0.9.9",
    (ds.get("register_version") or ds.get("version")) == EXPECT_VERSION,
    str(ds.get("register_version") or ds.get("version")))

# V3: every version-declaring metadata file must agree with EXPECT_VERSION. This is the gate that would
# have bitten on the CITATION.cff-left-at-0.9.8 drift: the "bump the version pointers" edit is no longer
# guarded only by vigilance. CITATION.cff is the machine-authoritative version (Zenodo/citation tools).
def _ver(path, pattern):
    try:
        m = re.search(pattern, (ROOT / path).read_text(encoding="utf-8"))
        return m.group(1) if m else None
    except Exception:
        return None
_version_sources = {
    "CITATION.cff": _ver("CITATION.cff", r'(?m)^version:\s*"?([0-9]+\.[0-9]+\.[0-9]+)"?'),
    "README.md": _ver("README.md", r'\*\*Status:\*\*\s*v([0-9]+\.[0-9]+\.[0-9]+)'),
    "PACKAGE.md": _ver("PACKAGE.md", r'repository \(v([0-9]+\.[0-9]+\.[0-9]+)\)'),
    "verification_ledger": (ledger.get("version") or "").lstrip("v") or None,
    # the two working papers themselves: the ORIGINAL drift was papers-vs-metadata, so V3 must cover the
    # version string each paper cites for the register ("Register (CBSR, v0.9.9…").
    "paper:methodology": _ver("papers/Citable_by_Construction_Methodology_v0.1.0.md", r'CBSR,\s*v([0-9]+\.[0-9]+\.[0-9]+)'),
    "paper:feasibility": _ver("papers/Cross-Border_Stablecoin_Feasibility_Over_Time_v0.1.0.md", r'CBSR,\s*v([0-9]+\.[0-9]+\.[0-9]+)'),
}
_bad_ver = {k: v for k, v in _version_sources.items() if v != EXPECT_VERSION}
inv("V3  all version-declaring artifacts agree with EXPECT_VERSION (CITATION.cff/README/PACKAGE/ledger + both papers)",
    not _bad_ver, f"expected {EXPECT_VERSION}; mismatches: {_bad_ver}")

# B1: no record may describe its OWN instrument as still un-enacted while its binding_status says the
# instrument IS enacted (in_force_enacted / made_not_commenced). This bites on the "label says
# enacted-not-commenced, body still says draft/bill/not-operative-law" contradiction — the Taiwan class
# (both the original issuer_pathway lag and the nine sibling-cell lag). It is a consistency gate, not the
# mere enumeration T2b performs. B1 is a blacklist; because a novel un-enacted phrasing could slip a
# blacklist, B2 adds the POSITIVE companion and B3 the SYMMETRIC pending gate, so coherence is enforced in
# both directions rather than by an ever-growing list of forbidden strings.
_ENACTED_BS = {"in_force_enacted", "made_not_commenced"}
# self-referential "own instrument is un-enacted" phrases. Excludes "if enacted" (a CH cell references a
# FUTURE reform bill) and "not yet in force" (the correct description of a made_not_commenced provision),
# both of which legitimately appear in enacted cells.
_UNENACTED_PHRASES = ["not operative law", "would take effect only on enactment", "remained a bill",
    "still in bill form", "is a draft provision", "are draft provisions", "draft provisions only",
    "pending enactment", "awaiting enactment", "status proposed", "not yet enacted", "a draft member",
    "remains a bill", "still a bill", "in bill form", "draft bill", "the draft act", "is not yet law",
    "has not been enacted", "have not been enacted", "yet to be enacted"]

def _blob(r):
    return ((r.get("requirement_summary") or "") + " " + (r.get("interpretation_note") or "") + " "
            + json.dumps(r.get("source") or {})).lower()

_incoherent = []
for _r in records:
    if _r.get("binding_status") in _ENACTED_BS:
        _s = (_r.get("requirement_summary") or "").lower()
        _hit = [p for p in _UNENACTED_PHRASES if p in _s]
        if _hit:
            _incoherent.append((_r["id"], _hit[0]))
inv("B1  no enacted-status cell describes its own instrument as un-enacted in its summary (blacklist)",
    not _incoherent, str(_incoherent[:5]))

# B2 (positive companion to B1): every made_not_commenced cell must AFFIRMATIVELY signal the
# enacted-but-not-commenced status somewhere in its text (summary/note/source). A blacklist can be evaded
# by novel wording; this cannot — an enacted-not-commenced cell that fails to say so is caught regardless
# of which words it uses. (Applies to made_not_commenced only; an in_force_enacted cell need not narrate
# commencement, and requiring a keyword there would false-positive on plainly-stated in-force requirements.)
_MNC_MARKERS = ["enacted", "commence", "made not commenced", "not yet operative", "not yet in force",
    "awaiting", "takes effect on", "third reading", "gazetted", "operative on", "subsidiary legislation",
    "not commenced", "2027-10-25", "2027", "made not"]
_mnc_silent = [r["id"] for r in records if r.get("binding_status") == "made_not_commenced"
               and not any(m in _blob(r) for m in _MNC_MARKERS)]
inv("B2  every made_not_commenced cell affirmatively signals enacted-not-commenced (positive companion to B1)",
    not _mnc_silent, str(_mnc_silent[:5]))

# B3 (symmetric to B1, pending direction): every pending_proposal cell must signal its pending / not-yet-in-
# force nature somewhere in its text, so a pending cell cannot read as though its instrument were already in
# force (e.g. citing only an in-force tool without naming the pending delegated legislation). This is the
# mirror of the Taiwan class in the other direction; the UK's delegated cells pass it because they name the
# draft SI / consultation their pending status rests on.
_PENDING_MARKERS = ["draft", "pending", "not in force", "not yet", "proposed", "bill", "awaiting", "would ",
    "if enacted", "consultation", "not operative", "forthcoming", "npr", "rulemaking", "to be ", "yet to",
    "anticipat", "implementing", "delegated"]
_pending_silent = [r["id"] for r in records if r.get("binding_status") == "pending_proposal"
                   and not any(m in _blob(r) for m in _PENDING_MARKERS)]
inv("B3  every pending_proposal cell signals its pending / not-yet-in-force nature (symmetric to B1)",
    not _pending_silent, str(_pending_silent[:5]))

# Sen1: the corridor-sensitivity layer (§4, load-bearing forward map) must reproduce the paper's headline
# edge-reclassification counts from the corridor states, and assert no new facts. This gates the layer the
# same way the other computed products are gated: it reproduces the authored ordering where they agree, and
# records the one breadth-vs-paper divergence (TW fan-in 9 > UK 8) as a finding rather than silently.
try:
    _sens = load_json("analysis/computed_sensitivity.json")
    _byj = {r["jurisdiction"]: r for r in _sens.get("ordering", [])}
    _ins = {r["jurisdiction"]: r for r in _sens.get("insensitive", [])}
    _sens_ok = (
        _byj.get("KR", {}).get("edges_reclassified") == 20 and _byj.get("KR", {}).get("fan_in") == 9
        and _byj.get("KR", {}).get("fan_out") == 11
        and _byj.get("UK", {}).get("edges_reclassified") == 8
        and _byj.get("TW", {}).get("fan_in") == 9
        and _ins.get("CN", {}).get("reason") == "prohibition"  # the paper's insensitive pole is listed explicitly
        and _sens.get("disagreement_as_finding") is not None
        and _sens.get("provenance", {}).get("asserts_new_facts") is False)
    inv("Sen1 sensitivity layer reproduces §4 (KR=20 [9in/11out], UK=8, TW fan-in=9; CN insensitive/prohibition); no new facts",
        _sens_ok, f"KR={_byj.get('KR',{}).get('edges_reclassified')} UK={_byj.get('UK',{}).get('edges_reclassified')} TW_in={_byj.get('TW',{}).get('fan_in')} CN={_ins.get('CN',{}).get('reason')}")
except Exception as _e:
    inv("Sen1 corridor-sensitivity layer present and reproduces §4 headline", False, repr(_e))

# Set1: the settlement-substrate bloc layer (§5.2) must be well-formed and, crucially, carry the paper's
# own tier discipline: it is Tier-2 OPERATIONAL enrichment, not a proposition of law. This gate keeps the
# §5.2 structural reading from ever being mistaken for tier1_legal, records the BIS-withdrawal correction,
# and checks every corridor is classified.
try:
    _sett = load_json("analysis/computed_settlement.json")
    _sett_ok = (
        _sett.get("claim_class") == "tier2_operational"
        and len(_sett.get("edges", [])) == 66
        and sum(_sett.get("counts", {}).values()) == 66
        and _sett.get("experiments", {}).get("mbridge", {}).get("bis_led") is False
        and _sett.get("experiments", {}).get("mbridge", {}).get("bis_withdrew") == "2024-10-31"
        and _sett.get("experiments", {}).get("agora", {}).get("bis_led") is True
        and _sett.get("provenance", {}).get("asserts_new_facts") is False)
    inv("Set1 settlement-substrate bloc layer well-formed, Tier-2, 66 edges classified, §5.2 correction recorded",
        _sett_ok, f"tier={_sett.get('claim_class')} edges={len(_sett.get('edges', []))} counts_sum={sum(_sett.get('counts', {}).values())}")
except Exception as _e:
    inv("Set1 settlement-substrate bloc layer present (§5.2)", False, repr(_e))

# === README DRIFT GATE =========================================================================
try:
    from check_readme_counts import check_readme_counts as _crc
    _readme = (ROOT / "README.md").read_text(encoding="utf-8")
    _readme_errs = _crc(_readme)
    inv("R1  README.md states no drift-prone coverage/tool/edge count (digits or spelled)",
        not _readme_errs, " | ".join(_readme_errs))
except Exception as _e:
    inv("R1  README.md drift gate available", False, repr(_e))

# === report ====================================================================================
passed = sum(1 for ok, _, _ in results if ok)
total = len(results)
print("CBSR invariant suite — v%s\n" % EXPECT_VERSION + "=" * 60)
for ok, name, detail in results:
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   -> " + detail) if detail else ""))
print("=" * 60)
print("RESULT: %d/%d invariants hold." % (passed, total)
      + ("" if passed == total else "  (%d FAILED)" % (total - passed)))
_sys.exit(0 if passed == total else 1)
