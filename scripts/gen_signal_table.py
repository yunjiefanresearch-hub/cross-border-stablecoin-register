#!/usr/bin/env python3
"""gen_signal_table.py — emit analysis/signal_table.json from the curated signal VALUES plus the
register's own 152 node records.

WHY THIS SCRIPT EXISTS (v0.10.0)
--------------------------------
The corridor audit published `signal_table.json` with `record_ref: null` on every signal, because the
152 node records were not shipped with it (critical finding C1; corridor-layer face VB-11). Its own
note is explicit: *"Fabricating locators was declined: the citation firewall (Citable by Construction
§4.3) forbids a tool from generating or inferring a citation, and a null is honest where a
plausible-looking locator would not be."*

In the register the node records ARE published. So the locator can be supplied instead of fabricated,
and VB-11 closes. This script is how: it reads

  * `analysis/signal_table.source.json` — the hand-curated signal VALUES, vendored verbatim from the
    audit. Their independence is the whole proof: they were written from the primary instruments and
    they OVERTURN the pre-v0.10.0 artifact on 12 of 132 edges. This script never edits a value.
  * the register's node records (`<jur>-<code>-<dimension>-001.yaml`), for the locator.

and emits `analysis/signal_table.json`, in which every signal carries a `record_ref` into a real,
existing, `tier1_legal` node record — or an explicit, reasoned `record_ref_gap` where no record
carries the instrument the signal rests on.

DISAGREEMENT IS A FINDING, NOT A SILENT FIX
-------------------------------------------
Binding the signals to the records surfaces genuine disagreements between the two layers — the same
computed-versus-authored posture the methodology paper prescribes (Citable by Construction §5.2).
Two kinds arise, and both are emitted as data under `record_binding_findings`, never reconciled by
overwriting one layer with the other:

  D1  `binding_status_divergence` — the signal and the record it cites disagree about the binding
      status of the instrument. Every instance is required to carry a `reason`. The load-bearing one
      is the United States: `us-pss-monetary_sovereignty-001` codes the GENIUS Act as
      `in_force_enacted` (the Act *is* enacted, 2025-07-18), while the signal codes the §18 inbound
      GATE, whose effective date §20 sets at the earlier of 2027-01-18 or final-rules + 120 days.
      Act-enacted is not section-operative. That distinction is exactly errata E1 / VB-06, and it is
      what moves the 8 inbound-US edges from `II` to `T`.

  D2  `instrument_divergence` — the record is the right dimension but rests on a different
      instrument from the one the signal names (US and UK `token_regime`: the signal rests on state
      trust/money-transmitter regimes and the Electronic Money Regulations 2011 respectively, which
      the register does not carry as records; the node records carry the *new* comprehensive regimes).
      Such a `record_ref` is tagged `match: related_dimension`, never `same_instrument`, so no reader
      can mistake it for a pinpoint citation to the instrument the class actually rests on. VB-09
      stays open, and now says so in the data.

GATES OVER THE OUTPUT (re-checked by run_invariants.py SG1–SG4)
---------------------------------------------------------------
  SG1  every class-driving signal (`token_regime`, `inbound_gate`) carries a `record_ref` that
       resolves to an existing node record whose `claim_class == tier1_legal`.
  SG2  a `record_ref` at `match: same_instrument` whose `record_binding_status` differs from the
       signal's `binding_status` must declare a `divergence` reason.
  SG3  `token_in_issue` (tier2_operational) carries no `record_ref` — a market fact is never given a
       legal locator.
  SG4  the vendored source's sha256 is stamped, so a silent edit to the curated values is detectable.

Plus the audit's own SIG1/SIG2/SIG3 (tools/class_rule.py:check_signal_provenance), run here.

Zero dependencies beyond PyYAML (already a register requirement).

Runs in the build sequence AFTER build_edge_skeletons.py and BEFORE build_corridors_directed.py.
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

import datetime
import hashlib
import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
_sys.path.insert(0, str(ROOT / "tools"))
import class_rule  # noqa: E402  (the published rule + its SIG1/SIG2/SIG3 gates)

REGISTER_VERSION = "0.10.0"

SRC = ROOT / "analysis" / "signal_table.source.json"
DST = ROOT / "analysis" / "signal_table.json"

# The node-record family that carries each jurisdiction's instruments.
FAMILY = {"US": "us-pss", "EU": "eu-emt", "UK": "uk-frs", "SG": "sg-scs", "HK": "hk-frs",
          "CN": "cn-prc", "BR": "br-vasp", "CH": "ch-frs", "AE": "ae-pt", "JP": "jp-epi",
          "TW": "tw-frs", "KR": "kr-frs"}

# ------------------------------------------------------------------------------------------------
# The curated signal -> node-record map.
#
# `dimension` names the register dimension whose record carries the instrument. `match` is a
# JUDGMENT, authored once and reviewed, about whether that record rests on the SAME instrument the
# signal names (`same_instrument`) or merely covers the same dimension under a different instrument
# (`related_dimension`). Nothing is inferred; nothing is fabricated. A `None` dimension means no
# record carries the instrument, and `gap` states why.
# ------------------------------------------------------------------------------------------------
DIM = {"token_regime": "issuer_pathway",
       "inbound_gate": "monetary_sovereignty",
       "egress_override": "cross_border_data",   # overridden per-jurisdiction below
       "yield_line": "permitted_activity_yield"}

# Per-(jurisdiction, signal) overrides of dimension and/or match, with the reason.
OVERRIDES = {
    # --- token_regime -----------------------------------------------------------------------
    ("US", "token_regime"): dict(match="related_dimension", backlog_ref="VB-09", note=(
        "The signal rests on the state trust-company / money-transmitter regimes (e.g. NYDFS 23 NYCRR "
        "Part 200) that authorize USD payment-stablecoin issuance today. The register carries no record "
        "for those state regimes; `us-pss-issuer_pathway-001` records the FEDERAL GENIUS Act layer, "
        "whose §3 issuance prohibition bites only from the §20 effective date. Same dimension, different "
        "instrument. Whether a state-authorized issuer is an 'exportable, comprehensively authorizable "
        "token' for Atlas purposes is the open question in VB-09; if the answer is no, all 11 outbound-US "
        "edges fall to Category III.")),
    ("UK", "token_regime"): dict(match="related_dimension", backlog_ref="VB-09", note=(
        "The signal rests on the Electronic Money Regulations 2011 (SI 2011/99), under which GBP e-money "
        "issuance is authorizable today. `uk-frs-issuer_pathway-001` records the NEW comprehensive regime "
        "(SI 2026/102), which is made-not-commenced and does not remove the existing pathway. Same "
        "dimension, different instrument.")),
    ("SG", "token_regime"): dict(match="same_instrument", note=(
        "The record bundles the in-force Payment Services Act 2019 baseline with the finalized-policy "
        "Single-Currency Stablecoin framework and is coded by the SCS layer (finalized_policy_pending). "
        "The signal is coded by the PSA baseline, which is what determines the class. Divergence declared.")),
    ("SG", "inbound_gate"): dict(match="same_instrument", note=(
        "Same bundling as SG.token_regime: the class rests on the in-force PSA 2019 baseline, the record "
        "is coded by the pending SCS layer.")),
    ("CN", "token_regime"): dict(match="same_instrument", note=(
        "Vocabulary divergence only: the register's binding_status enum carries `prohibition` as a "
        "first-class value; the curated signal writes `in_force_enacted` of the prohibiting instrument "
        "(银发〔2026〕42号, in force 2026-02-06). Same instrument, same fact, two encodings.")),
    ("CN", "inbound_gate"): dict(match="same_instrument", note="As CN.token_regime: `prohibition` vs `in_force_enacted` of the prohibiting instrument."),
    ("CN", "yield_line"): dict(match="related_dimension", note=(
        "The signal value is `n_a` (a prohibition leaves no yield question to answer). The record rests "
        "on the 2017 token-fundraising notice, not on 42号.")),
    ("KR", "token_regime"): dict(match="same_instrument", note=(
        "Vocabulary divergence: the register codes the draft Digital Asset Basic Act as "
        "`pending_proposal` (there IS a bill); the signal codes the absence of an operative issuance "
        "regime as `no_regime` (there is nothing in force to authorize under). Same instruments, "
        "different question asked of them.")),
    ("KR", "inbound_gate"): dict(match="same_instrument", note="As KR.token_regime: `pending_proposal` (the bill exists) vs `no_regime` (nothing operative)."),
    ("TW", "inbound_gate"): dict(match="related_dimension", backlog_ref="VB-R1", note=(
        "`tw-frs-monetary_sovereignty-001` still cites the 'draft Virtual Asset Service Act'. The Act was "
        "passed at third reading on 2026-06-30 and is enacted, not draft. The signal is correct and the "
        "record's source prose is stale — the node-record face of finding F-TW. Recorded here rather than "
        "silently corrected: a legal record is edited by a verification pass, not by a build script.")),
    ("US", "inbound_gate"): dict(match="same_instrument", backlog_ref="VB-06", note=(
        "`us-pss-monetary_sovereignty-001` cites the GENIUS Act, pinpoint 'Foreign payment stablecoin "
        "issuers — comparability determination and registration' — the same §18 gate the signal names. "
        "The record codes the ACT as in_force_enacted (it is: enacted 2025-07-18); the signal codes the "
        "GATE, which §20 makes effective on the earlier of 2027-01-18 or final-rules + 120 days. "
        "Act-enacted is not section-operative. This is errata E1 / VB-06, and it is the divergence that "
        "moves the 8 inbound-US edges from II to T.")),
    ("US", "yield_line"): dict(match="same_instrument", backlog_ref="VB-06", note=(
        "Same §20 effective-date distinction as US.inbound_gate: the record codes the Act, the signal "
        "codes §4(a)(11)'s operative bite.")),
    ("UK", "yield_line"): dict(match="related_dimension", note=(
        "`uk-frs-permitted_activity_yield-001` is coded `pending_proposal` (SI 2026/102 is silent on "
        "yield; the Bank of England Nov 2025 materials are a consultation). The signal codes the "
        "made-not-commenced regime's restriction. Different instruments within one dimension.")),
    # --- egress_override --------------------------------------------------------------------
    # `cross_border_data` is a DATA-protection dimension; only where the egress override is ACTIVE does
    # the register carry a record that speaks to the export restriction the signal names.
    ("CN", "egress_override"): dict(dimension="cross_border_data", match="related_dimension", note=(
        "The record carries PIPL / DSL / CAC — the cross-border DATA half of the override. The mainland "
        "capital-flow half (SAFE) is not separately recorded. Partial locator, declared as such.")),
    ("SG", "egress_override"): dict(dimension="distribution", match="related_dimension", note=(
        "`sg-scs-distribution-001` carries the PSA 2019 / MAS SCS distribution perimeter. The signal "
        "rests on the MAS Digital Token Service Provider statement (June 2025), which the register does "
        "not carry as a separate record. Nearest dimension, different instrument.")),
    ("KR", "egress_override"): dict(dimension="monetary_sovereignty", match="same_instrument", note=(
        "`kr-frs-monetary_sovereignty-001` cites the Foreign Exchange Transactions Act — the instrument "
        "the conditional, dormant Korea-FX override rests on.")),
}

# A `none`-valued egress override is the ABSENCE of an instrument. There is nothing to cite, and a
# locator would be a fabrication. Stated, with a reason, rather than left as a bare null.
EGRESS_NONE_GAP = ("An absence of an export/egress restriction is not an instrument and has no "
                   "locator. The register carries no record asserting the absence; the Atlas's silence "
                   "on the origin's row is the basis. Citation firewall (Citable by Construction §4.3): "
                   "a null is honest where a plausible-looking locator would not be.")

# `yield_line` values the audit left unverified: the record exists but does not yet support the signal.
YIELD_UNVERIFIED_NOTE = ("The signal value is `unverified`: the register carries the record, but its "
                         "yield cell is in the verification backlog and is not asserted as drawing the "
                         "US/SG line (Feasibility §4.5 states exactly this).")


def load_records() -> dict:
    """{(jurisdiction, dimension): record_dict} for the 152 node records."""
    out = {}
    for f in sorted(ROOT.glob("*.yaml")):
        if f.name in ("_TEMPLATE.yaml", "roadmap.yaml"):
            continue
        try:
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") and d.get("dimension") and d.get("jurisdiction"):
            out[(d["jurisdiction"], d["dimension"])] = d
    return out


def build_record_ref(j: str, name: str, sig: dict, records: dict, findings: list):
    """Return (record_ref | None, record_ref_gap | None). Never fabricates a locator."""
    if name == "token_in_issue":                       # SG3: a market fact gets no legal locator
        return None, {"reason": "tier2_operational: a market fact carries no legal locator (SIG1/SG3)."}

    ov = OVERRIDES.get((j, name), {})
    if name == "egress_override" and sig["value"] == "none":
        return None, {"reason": EGRESS_NONE_GAP}

    dim = ov.get("dimension", DIM[name])
    rec = records.get((j, dim))
    if rec is None:
        raise SystemExit(f"[SG1] no node record for {j}.{dim} (signal {j}.{name}) — refusing to emit a "
                         f"signal table with an unresolvable record_ref")
    if rec.get("claim_class") != "tier1_legal":
        raise SystemExit(f"[SG1] {rec['id']} is {rec.get('claim_class')!r}; a class-driving signal may "
                         f"only rest on a tier1_legal record (Citable by Construction §4.2)")

    match = ov.get("match", "same_instrument")
    ref = {
        "record_id": rec["id"],
        "dimension": dim,
        "match": match,
        "record_binding_status": rec.get("binding_status"),
        "record_evidence_tier": rec.get("evidence_tier"),
        "record_claim_class": rec["claim_class"],
    }
    if ov.get("backlog_ref"):
        ref["backlog_ref"] = ov["backlog_ref"]
    if ov.get("note"):
        ref["note"] = ov["note"]
    if name == "yield_line" and sig["value"] == "unverified":
        ref["note"] = YIELD_UNVERIFIED_NOTE
        ref["match"] = "related_dimension"

    sb, rb = sig.get("binding_status"), rec.get("binding_status")
    if sb is not None and sb != rb:
        kind = "D1_binding_status_divergence" if ref["match"] == "same_instrument" else "D2_instrument_divergence"
        if ref["match"] == "same_instrument" and not ov.get("note"):
            # SG2: an undeclared same-instrument divergence is a build failure, not a silent field.
            raise SystemExit(f"[SG2] {j}.{name}: signal binding_status {sb!r} != record {rec['id']} "
                             f"{rb!r} at match=same_instrument, and no divergence reason is declared")
        ref["divergence"] = ov.get("note")
        findings.append({
            "kind": kind, "jurisdiction": j, "signal": name, "record_id": rec["id"],
            "signal_binding_status": sb, "record_binding_status": rb,
            "class_driving": name in class_rule.CLASS_DRIVING_SIGNALS,
            "reason": ov.get("note"),
            "backlog_ref": ov.get("backlog_ref"),
        })
    elif ref["match"] == "related_dimension":
        findings.append({
            "kind": "D2_instrument_divergence", "jurisdiction": j, "signal": name,
            "record_id": rec["id"], "signal_binding_status": sb, "record_binding_status": rb,
            "class_driving": name in class_rule.CLASS_DRIVING_SIGNALS,
            "reason": ov.get("note") or f"the record covers {dim} under a different instrument",
            "backlog_ref": ov.get("backlog_ref"),
        })
    return ref, None


def main() -> int:
    src_bytes = SRC.read_bytes()
    src = json.loads(src_bytes.decode("utf-8"))
    records = load_records()
    findings: list = []

    signals = json.loads(json.dumps(src["signals"]))       # deep copy; values never mutated
    n_ref = n_gap = 0
    for j in class_rule.J12:
        for name, sig in signals[j].items():
            if not isinstance(sig, dict):
                continue
            ref, gap = build_record_ref(j, name, sig, records, findings)
            sig["record_ref"] = ref
            if gap:
                sig["record_ref_gap"] = gap
                n_gap += 1
            else:
                n_ref += 1

    out = {
        "schema": "cbsr-analysis/signal_table",
        "version": "0.10.0",
        "generated": str(datetime.date.today()),
        "register_version": REGISTER_VERSION,
        "as_of": src["as_of"],
        "what_this_is": (
            "The per-jurisdiction signals from which every one of the 132 directed corridor classes is "
            "derived by the published rule tools/class_rule.py:class_of. GENERATED — do not edit. The "
            "signal VALUES are curated in analysis/signal_table.source.json; scripts/gen_signal_table.py "
            "joins them to the register's 152 node records and populates `record_ref`, which closes the "
            "corridor-layer face of finding C1 (backlog VB-11)."),
        "independence_note": src["independence_note"],
        "record_ref_status": (
            f"POPULATED on {n_ref} of {n_ref + n_gap} signals, from the register's own node records; "
            f"{n_gap} carry an explicit, reasoned `record_ref_gap` instead of a fabricated locator "
            f"(citation firewall, Citable by Construction §4.3). VB-11 is closed for this register: the "
            f"152 node records ARE published here, so the locator is supplied rather than declined. A "
            f"`record_ref` is tagged `match: same_instrument` only where the record rests on the very "
            f"instrument the signal names; otherwise `related_dimension`, and the difference is emitted "
            f"under `record_binding_findings` rather than smoothed over."),
        "source_of_record": {
            "path": "analysis/signal_table.source.json",
            "sha256": hashlib.sha256(src_bytes).hexdigest(),
            "note": ("SG4: the curated values are hashed so a silent edit is detectable. The values were "
                     "written from the primary instruments and CONTRADICT the pre-v0.10.0 corridor "
                     "artifact on 12 of 132 edges; a signal table that agreed with the artifact by "
                     "construction would prove nothing."),
        },
        "axes": src["axes"],
        "gates_over_this_file": {
            **src["gates_over_this_file"],
            "SG1": "every class-driving signal's record_ref resolves to an existing tier1_legal node record.",
            "SG2": "a same_instrument record_ref whose record_binding_status differs from the signal's must declare a divergence reason.",
            "SG3": "token_in_issue (tier2_operational) carries no record_ref.",
            "SG4": "the curated source's sha256 is stamped, so an unreviewed edit to the values is detectable.",
        },
        "class_rule": src["class_rule"],
        "record_binding_findings": {
            "posture": ("Disagreement between the signal layer and the node-record layer is surfaced as a "
                        "finding, never resolved by overwriting either layer (Citable by Construction "
                        "§5.2). D1 = the two layers disagree on the binding status of the SAME instrument "
                        "(the load-bearing case is US §18: Act-enacted vs section-operative — errata E1 / "
                        "VB-06). D2 = the record covers the dimension under a DIFFERENT instrument (US and "
                        "UK token_regime — VB-09 stays open)."),
            "count": len(findings),
            "class_driving_count": sum(1 for f in findings if f["class_driving"]),
            "findings": findings,
        },
        "signals": signals,
        "settlement_blocs": src["settlement_blocs"],
    }

    DST.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Re-run the audit's own gates over what we just wrote.
    doc = class_rule.load(DST)
    problems = class_rule.check_signal_provenance(doc) + class_rule.check_gate_values(doc)
    if problems:
        print("[FAIL] signal-table gates violated:")
        for p in problems:
            print("   -", p)
        return 1

    from collections import Counter
    dist = Counter(c for c, _ in class_rule.all_classes(doc["signals"]).values())
    print(f"wrote analysis/signal_table.json — {n_ref} signals bound to node records, {n_gap} reasoned gap(s)")
    print(f"  record-binding findings: {len(findings)} ({out['record_binding_findings']['class_driving_count']} on class-driving signals)")
    print(f"  SIG1/SIG2/SIG3 + SG1–SG4: CLEAN")
    print(f"  class_rule derives {sum(dist.values())} edges; distribution {dict(sorted(dist.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
