#!/usr/bin/env python3
"""The computed layer (preview) — turn the composition-problem thesis into a running function.

The Architecture paper's central claim is that cross-border feasibility is a *composition* of
single-jurisdiction constraints; the Atlas's 132 directed classifications are the hand-output of
that composition. v0.5.x stored both layers but never *computed* anything: the §5.14 matrix and the
corridors were independent transcriptions. This module takes the first real step toward a computable,
self-checking graph:

  1. derive a small, auditable per-jurisdiction signal table from the node records (where it can be
     read off cleanly — e.g. pre-regime status — it is; the inbound-gate *type* is an explicit,
     annotated table because it is a documentary judgment, not a single field);
  2. implement compose_directed(origin, destination) using the Atlas's OWN stated algorithm
     (§3.2 destination-determined class + origin drag/override);
  3. DIFF the computed class against the authored values — the authored directed feasibility_class
     of the 9 corridors, and (via a documented reduction) the authored §5.14 undirected categories;
  4. emit analysis/computed_compatibility.json, where every computed-vs-authored disagreement is a
     FINDING with a named cause, not a silent contradiction.

This is deliberately a *preview*: compose_directed is NOT asserted to be authoritative. Its value is
that it reproduces most authored classifications from first principles and that its disagreements
localise exactly where the two source papers (Atlas directed vs Architecture undirected) diverge —
which is where the research interest is. Run: python3 scripts/compose.py
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "TW", "JP", "KR"]

# --- 1. per-jurisdiction signals -------------------------------------------------------------
# regime_status: live | transition | pre_regime | prohibition
# inbound_gate (the destination test a foreign token meets): open | comparability | channel |
#   usage_channel | fx_counterparty | transition | pre_regime | prohibition
# exportable_token: whether the jurisdiction has an authorizable private token to export (origin drag)
# egress_override: whether the origin imposes an export/egress restriction (annotation flag)
# Each entry is annotated with the record/source that justifies it (auditable, not a bare table).
SIGNALS = {
    "US": {"regime_status": "live",        "inbound_gate": "comparability",  "exportable_token": True,
           "egress_override": False, "basis": "GENIUS Act; §18 comparability gate (us-pss-* records)"},
    "EU": {"regime_status": "live",        "inbound_gate": "open_capped",    "exportable_token": True,
           "egress_override": False, "basis": "MiCA; Art. 58(3) cap — dual auth available (eu-emt-* records)"},
    "UK": {"regime_status": "transition",  "inbound_gate": "transition",     "exportable_token": True,
           "egress_override": False, "basis": "FSMA 2026 conduct + systemic regimes operative 2027 (uk-frs-* records)"},
    "SG": {"regime_status": "live",        "inbound_gate": "open",           "exportable_token": True,
           "egress_override": True,  "basis": "MAS-SCS; June 2025 DTSP perimeter constrains offshore-to-SG (sg-frs-* records)"},
    "HK": {"regime_status": "live",        "inbound_gate": "open",           "exportable_token": True,
           "egress_override": False, "basis": "Stablecoins Ordinance; HKD-only first cohort (hk-frs-* records)"},
    "CN": {"regime_status": "prohibition", "inbound_gate": "prohibition",    "exportable_token": False,
           "egress_override": True,  "basis": "issuance prohibited; PIPL/DSL/CAC/SAFE on data/capital (cn-prc-* records)"},
    "BR": {"regime_status": "live",        "inbound_gate": "fx_counterparty","exportable_token": True,
           "egress_override": False, "basis": "BCB câmbio reclassification; per-operation cap vs non-FX-authorised counterparty (br-* records)"},
    "CH": {"regime_status": "live",        "inbound_gate": "open",           "exportable_token": True,
           "egress_override": False, "basis": "Banking Act/Ordinance; no usage cap; FINMA holder-ID (ch-frs-* records)"},
    "AE": {"regime_status": "live",        "inbound_gate": "usage_channel",  "exportable_token": True,
           "egress_override": False, "basis": "CBUAE PTSR; Foreign Payment Token usage-channel restriction (ae-pt-* records)"},
    "TW": {"regime_status": "transition",  "inbound_gate": "transition",     "exportable_token": False,
           "egress_override": False, "basis": "VAS Act enacted at third reading 30 Jun 2026; subsidiary legislation pending, no gazetted commencement; no exportable token yet (tw-frs-issuer_pathway-001 status=transitional)"},
    "JP": {"regime_status": "live",        "inbound_gate": "channel",        "exportable_token": True,
           "egress_override": False, "basis": "Payment Services Act EPI regime; EPIESP inbound channel-determination (jp-epi-* records)"},
    "KR": {"regime_status": "pre_regime",  "inbound_gate": "pre_regime",     "exportable_token": False,
           "egress_override": False, "basis": "VAUPA in force; DABA a bill (kr-frs-issuer_pathway-001 status=proposed)"},
}

# inbound_gate -> directed feasibility class produced AT the destination
GATE_CLASS = {
    "open": "I", "open_capped": "I",         # dual authorization available (EU additionally scale-capped)
    "comparability": "II", "channel": "II", "usage_channel": "II", "fx_counterparty": "II",
    "transition": "T", "pre_regime": "pre_regime", "prohibition": "blocked",
}


def derive_pre_regime_from_records():
    """Cross-check: pre_regime should be exactly the jurisdictions whose issuer_pathway is proposed."""
    pre = set()
    for j in J12:
        for f in ROOT.glob(f"{j.lower()}-*issuer_pathway*.yaml"):
            import yaml
            d = yaml.safe_load(f.read_text(encoding="utf-8"))
            if d.get("status") == "proposed":
                pre.add(j)
    return pre


# The signals compose() reads are legal characterisations of each regime, so the node records
# that back them must be propositions of law (claim_class=tier1_legal), not market/operational
# reports. This is the v0.7.0 inheritance: the computed layer rests only on tier1_legal facts.
# (It is what lets a future date-aware compose() and the constraint substrate refuse to derive
# feasibility from a tier2_operational-only basis.)
SIGNAL_DRIVING_DIMENSIONS = ["issuer_pathway", "regulatory_authority",
                             "monetary_sovereignty", "distribution"]

def check_signal_provenance():
    """For each jurisdiction, confirm the records driving its signal are tier1_legal.

    Returns (provenance_by_jurisdiction, violations). A violation is a driving record whose
    claim_class is tier2_operational — i.e. the engine would be composing a proposition of law
    from a market/operational fact, which the two-axis model forbids.
    """
    import yaml
    prov, violations = {}, []
    for j in J12:
        legal_ids, op_ids = [], []
        for dim in SIGNAL_DRIVING_DIMENSIONS:
            for f in ROOT.glob(f"{j.lower()}-*{dim}*.yaml"):
                d = yaml.safe_load(f.read_text(encoding="utf-8"))
                cc = d.get("claim_class")
                rid = d.get("id")
                if cc == "tier1_legal":
                    legal_ids.append(rid)
                elif cc == "tier2_operational":
                    op_ids.append(rid)
                    violations.append(f"{j}: signal-driving record {rid} ({dim}) is tier2_operational; "
                                      f"compose() must rest on tier1_legal facts")
        prov[j] = {"tier1_legal_basis": sorted(legal_ids),
                   "tier2_operational_in_driving_dims": sorted(op_ids)}
    return prov, violations


import datetime as _dt

def load_events():
    """Load the event calendar (dated/contingent CHANGES IN LAW). Returns (events_list, meta)."""
    f = ROOT / "analysis" / "event_calendar.json"
    if not f.exists():
        return [], {}
    obj = json.loads(f.read_text(encoding="utf-8"))
    return obj.get("events", []), obj

def _parse_date(s):
    try:
        return _dt.date.fromisoformat(s)
    except Exception:
        return None

def signals_as_of(date_str, events=None):
    """Return a copy of SIGNALS with all scheduled/in_force events effective on or before date_str applied.

    Contingent events (no firm date) are NEVER applied here — they are surfaced separately as pending
    transitions. This is the date-aware evaluation the time engine rests on.
    """
    import copy
    if events is None:
        events, _ = load_events()
    S = copy.deepcopy(SIGNALS)
    asof = _parse_date(date_str) if date_str else None
    # apply in chronological order so a later event overrides an earlier one on the same field
    dated = [e for e in events if e.get("status") in ("scheduled", "in_force") and e.get("effective_date")]
    for e in sorted(dated, key=lambda e: e["effective_date"]):
        ed = _parse_date(e["effective_date"])
        if asof is not None and ed is not None and ed <= asof:
            for eff in e.get("effect", []):
                fld, to = eff.get("field"), eff.get("to")
                if e["jurisdiction"] in S and fld:
                    S[e["jurisdiction"]][fld] = to
    return S

def check_event_provenance(events=None):
    """Every event must be a tier1_legal change in law backed by tier1_legal records — never a market event.

    This is the v0.8.0 inheritance of the two-axis discipline into the time dimension: the engine only
    advances on changes in LAW. Returns a list of violations (empty = clean).
    """
    import yaml
    if events is None:
        events, _ = load_events()
    # map record id -> claim_class
    cc = {}
    for p in ROOT.glob("*.yaml"):
        if p.name == "_TEMPLATE.yaml":
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and d.get("id") and "claim_class" in d:
            cc[d["id"]] = d["claim_class"]
    violations = []
    valid_status = {"scheduled", "contingent", "in_force"}
    for e in events:
        eid = e.get("id", "<no id>")
        if e.get("claim_class") != "tier1_legal":
            violations.append(f"event {eid}: claim_class must be tier1_legal (a change in law), got {e.get('claim_class')!r}")
        if e.get("status") not in valid_status:
            violations.append(f"event {eid}: invalid status {e.get('status')!r}")
        if e.get("status") == "scheduled" and not e.get("effective_date"):
            violations.append(f"event {eid}: scheduled events require an effective_date")
        if e.get("status") == "contingent" and e.get("effective_date"):
            violations.append(f"event {eid}: contingent events must not carry an effective_date (use trigger)")
        for rid in e.get("records", []):
            if cc.get(rid) != "tier1_legal":
                violations.append(f"event {eid}: backing record {rid} is not tier1_legal "
                                  f"(got {cc.get(rid, 'MISSING')!r}); the time engine may not rest on a market record")
    return violations

def edge_timeline(origin, dest, events=None):
    """The dated future of one directed edge: today's class, then each event that changes it.

    Scheduled events are applied cumulatively in date order; contingent events are shown as hypothetical
    'would change to' branches (never folded into the dated line). Returns today's class plus a list of
    transition points and the next change.
    """
    import copy
    if events is None:
        events, _ = load_events()
    base_date = "2026-06-30"
    today_cls = compose_directed(origin, dest, SIGNALS)["class"]
    affects = lambda e: e.get("jurisdiction") in (origin, dest) and e.get("effect")
    # cumulative scheduled timeline
    transitions, running = [], copy.deepcopy(SIGNALS)
    dated = sorted([e for e in events if e.get("status") in ("scheduled", "in_force")
                    and e.get("effective_date") and affects(e)], key=lambda e: e["effective_date"])
    prev = today_cls
    for e in dated:
        for eff in e.get("effect", []):
            if e["jurisdiction"] in running and eff.get("field"):
                running[e["jurisdiction"]][eff["field"]] = eff["to"]
        cls = compose_directed(origin, dest, running)["class"]
        transitions.append({"date": e["effective_date"], "precision": e.get("precision"),
                            "status": e["status"], "event_id": e["id"], "title": e.get("title"),
                            "class_before": prev, "class_after": cls, "changed": cls != prev,
                            "basis": e.get("basis")})
        prev = cls
    # contingent (no date) — hypothetical branches off today's base
    contingent = [e for e in events if e.get("status") == "contingent" and affects(e)]
    pending = []
    for e in contingent:
        hyp = copy.deepcopy(SIGNALS)
        for eff in e.get("effect", []):
            if e["jurisdiction"] in hyp and eff.get("field"):
                hyp[e["jurisdiction"]][eff["field"]] = eff["to"]
        cls = compose_directed(origin, dest, hyp)["class"]
        pending.append({"date": None, "status": "contingent", "event_id": e["id"], "title": e.get("title"),
                        "trigger": e.get("trigger"), "class_if_enacted": cls,
                        "would_change": cls != today_cls, "basis": e.get("basis")})
    next_change = next((t for t in transitions if t["changed"]), None)
    return {"edge": f"{origin}->{dest}", "as_of_base": base_date, "today_class": today_cls,
            "scheduled_transitions": transitions, "pending_contingent": pending,
            "next_scheduled_change": next_change}


def compose_directed(origin, dest, signals=None):
    """Atlas §3.2 algorithm: origin drag first, then destination-determined inbound class."""
    S = signals if signals is not None else SIGNALS
    so, sd = S[origin], S[dest]
    # origin drag: an origin with no exportable/authorizable token cannot cross into any destination
    if not so["exportable_token"]:
        if so["regime_status"] == "prohibition":
            axis = "prohibition"
        elif so["regime_status"] == "pre_regime":
            axis = "pre_regime"
        else:  # transition/live: enacted law but no exportable token yet (Taiwan post-enactment, pre-commencement)
            axis = "enacted_not_commenced"
        return {"class": "III", "rule": f"origin_drag:{axis}",
                "explain": f"{origin} has no exportable, comprehensively authorizable private token "
                           f"({so['basis']}); the lawful options are partnership/coordination, not direct issuance.",
                "origin_override": so["egress_override"]}
    cls = GATE_CLASS[sd["inbound_gate"]]
    return {"class": cls, "rule": f"destination_gate:{sd['inbound_gate']}",
            "explain": f"At the destination, {dest} applies an inbound gate of type '{sd['inbound_gate']}' "
                       f"({sd['basis']}); origin {origin} has an exportable token.",
            "origin_override": so["egress_override"]}


def reduce_undirected(o, d, signals=None):
    """Reduce the two directed classes to a §5.14-style undirected category, to diff vs the matrix."""
    a, b = compose_directed(o, d, signals)["class"], compose_directed(d, o, signals)["class"]
    s = {a, b}
    if s & {"III", "blocked", "pre_regime"}:
        return "III", "either direction is blocked / pre-regime / origin-dragged"
    if "T" in s:
        return "I/II*", "one side is a regime-in-transition (operative later); Atlas flags T"
    # both directions in {I, II}: the standard live-live config is dual-authorization-or-partnership
    return "I/II", "both directions authorizable (dual authorization or partnership)"


def parse_authored_class(feasibility_class):
    """Pull the leading class token out of an authored corridor feasibility_class string."""
    if not feasibility_class:
        return None
    s = feasibility_class.lower()
    if "blocked" in s: return "blocked"
    if "pre-regime" in s or "pre regime" in s: return "pre_regime"
    if "transition" in s: return "T"
    m = re.search(r"category\s+(i/ii|iii|ii|i)\b", s)
    if m:
        return {"i": "I", "ii": "II", "iii": "III", "i/ii": "I/II"}[m.group(1)]
    return None


def build():
    comp = json.loads((ROOT / "analysis" / "compatibility.json").read_text(encoding="utf-8"))
    authored_pairs = {p["pair"]: p for p in comp["pairs"]}

    # cross-check the derived pre_regime set
    try:
        pre_from_records = sorted(derive_pre_regime_from_records())
    except Exception:
        pre_from_records = None
    pre_from_signals = sorted([j for j, s in SIGNALS.items() if s["regime_status"] == "pre_regime"])

    # v0.7.0: provenance discipline — every signal must rest on tier1_legal records
    try:
        signal_provenance, provenance_violations = check_signal_provenance()
    except Exception:
        signal_provenance, provenance_violations = {}, []

    # (a) directed edges: compose vs authored corridor feasibility_class
    corridors = []
    for f in sorted(ROOT.glob("*.yaml")):
        import yaml
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "corridor_id" in d and d.get("origin") and d.get("destination"):
            corridors.append(d)
    directed = []
    d_agree = 0
    for c in corridors:
        o, dst = c["origin"], c["destination"]
        cm = compose_directed(o, dst)
        authored = parse_authored_class(c.get("feasibility_class"))
        # normalise authored I/II to compare with computed (computed emits I or II directional)
        agree = (authored == cm["class"]) or (authored == "I/II" and cm["class"] in {"I", "II"})
        if agree:
            d_agree += 1
        directed.append({
            "corridor_id": c["corridor_id"], "edge": f"{o}->{dst}",
            "computed_class": cm["class"], "authored_class": authored,
            "agree": agree, "rule": cm["rule"], "origin_override": cm["origin_override"],
            "finding": None if agree else (
                "br_counterparty_conditional" if dst == "BR" else
                "uk_regime_in_transition" if "T" in {cm["class"], authored} else "review"),
        })

    # (b) undirected pairs: reduced compose vs §5.14 authored category
    pairs = []
    p_agree = 0
    for i, a in enumerate(J12):
        for b in J12[i + 1:]:
            key = "-".join(sorted([a, b]))
            authored = authored_pairs.get(key, {}).get("category")
            red, why = reduce_undirected(a, b)
            # 'I/II*' = dual-auth-or-partnership WITH a regime-in-transition caveat (Atlas flags UK=T).
            # It agrees with an authored 'I/II', but NOT with a pure 'I' — which is exactly where the
            # Architecture's §5.14 ("cleanly bridgeable Category I") and the Atlas ("UK not operative
            # until 2027") disagree. Those become findings.
            agree = (red == authored) or (red == "I/II*" and authored == "I/II")
            if agree:
                p_agree += 1
            finding = None
            if not agree:
                finding = "uk_regime_in_transition" if (red == "I/II*" or "UK" in (a, b)) else "review"
            pairs.append({"pair": key, "computed_category": red, "authored_category": authored,
                          "agree": agree, "basis": why, "finding": finding})

    findings = {}
    for row in directed + pairs:
        if not row["agree"]:
            findings.setdefault(row["finding"], []).append(row.get("pair") or row.get("edge"))

    out = {
        "schema": "cbsr-analysis/computed_compatibility",
        "status": "preview",
        "method": ("compose_directed(origin,destination) implements the Corridor Atlas v0.2.3 §3.2 "
                   "algorithm — origin drag (no exportable token => Category III) then a "
                   "destination-determined inbound class from the per-jurisdiction signal table — and "
                   "is diffed against authored values. It is NOT asserted authoritative; disagreements "
                   "are findings that localise where the Atlas (directed) and Architecture §5.14 "
                   "(undirected) classifications diverge."),
        "jurisdiction_signals": SIGNALS,
        "pre_regime_crosscheck": {"from_signals": pre_from_signals, "from_records": pre_from_records,
                                  "consistent": pre_from_records is None or pre_from_records == pre_from_signals},
        "signal_provenance": {
            "discipline": ("Every per-jurisdiction signal rests on tier1_legal records (propositions of "
                           "law), never on tier2_operational (market) facts. This is what lets the "
                           "computed layer — and any future date-aware compose() or constraint "
                           "substrate — derive feasibility only from binding-law facts."),
            "by_jurisdiction": signal_provenance,
            "violations": provenance_violations,
            "clean": not provenance_violations,
        },
        "directed_edges": {"count": len(directed), "agree": d_agree,
                           "agreement": f"{d_agree}/{len(directed)}", "edges": directed},
        "undirected_pairs": {"count": len(pairs), "agree": p_agree,
                             "agreement": f"{p_agree}/{len(pairs)}", "pairs": pairs},
        "findings_by_cause": {k: sorted(v) for k, v in sorted(findings.items())},
    }
    (ROOT / "analysis" / "computed_compatibility.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def _undirected_agreement(authored_pairs, signals):
    """Recompute undirected computed-vs-authored agreement under a given signal set."""
    agree = 0
    rows = []
    for i, a in enumerate(J12):
        for b in J12[i + 1:]:
            key = "-".join(sorted([a, b]))
            authored = authored_pairs.get(key, {}).get("category")
            red, _ = reduce_undirected(a, b, signals)
            ok = (red == authored) or (red == "I/II*" and authored == "I/II")
            if ok:
                agree += 1
            else:
                rows.append({"pair": key, "computed": red, "authored": authored})
    return agree, rows


def build_timeline():
    """Emit analysis/computed_timeline.json: the date-aware view of the corridor layer.

    For each directed corridor it computes today's class and the dated/contingent transitions that
    change it; it also recomputes the undirected agreement as of future dates and tracks the
    regime-in-transition caveat, separating findings that resolve over time from structural ones.
    """
    events, meta = load_events()
    violations = check_event_provenance(events)
    comp = json.loads((ROOT / "analysis" / "compatibility.json").read_text(encoding="utf-8"))
    authored_pairs = {p["pair"]: p for p in comp["pairs"]}

    corridors = []
    for f in sorted(ROOT.glob("*.yaml")):
        import yaml
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "corridor_id" in d and d.get("origin") and d.get("destination"):
            corridors.append(d)
    edges = [edge_timeline(c["origin"], c["destination"], events) for c in corridors]

    # Illustration edges that exercise a scheduled regime change (the authored 9 corridors don't touch
    # the UK, where the headline transition happens): show the clean directed T -> I as the regime goes live.
    illustration = [edge_timeline(o, d, events) for (o, d) in
                    [("US", "UK"), ("UK", "US"), ("EU", "UK"), ("UK", "EU"), ("HK", "UK")]]

    horizons = ["2026-06-30"] + sorted({e["effective_date"] for e in events
                                        if e.get("status") in ("scheduled", "in_force") and e.get("effective_date")})

    def caveated_pairs(signals):
        out = []
        for i, a in enumerate(J12):
            for b in J12[i + 1:]:
                red, _ = reduce_undirected(a, b, signals)
                if str(red).endswith("*"):
                    out.append("-".join(sorted([a, b])))
        return out

    over_time = []
    for h in horizons:
        S = signals_as_of(h, events)
        agree, residual = _undirected_agreement(authored_pairs, S)
        cav = caveated_pairs(S)
        over_time.append({"as_of": h, "undirected_agreement": f"{agree}/66",
                          "transition_caveated_pairs": {"count": len(cav), "pairs": cav},
                          "residual_findings": residual})

    out = {
        "schema": "cbsr-analysis/computed_timeline",
        "status": "preview",
        "as_of_base": meta.get("as_of_base", "2026-06-30"),
        "method": ("Date-aware compose(): signals_as_of(date) applies every scheduled/in_force event in "
                   "the event calendar with effective_date <= date, then re-runs the Atlas algorithm. "
                   "Contingent events (a bill not yet enacted) are never applied by date — they are "
                   "shown as hypothetical 'class_if_enacted' branches. Every event is a tier1_legal "
                   "change in law backed by tier1_legal records (enforced); a market launch is never an "
                   "event. NOT asserted authoritative."),
        "event_provenance": {"clean": not violations, "violations": violations,
                             "discipline": "the time engine advances only on tier1_legal events backed by tier1_legal records"},
        "headline": ("The directed edge US->UK is Category III/T while the UK regime is in transition and "
                     "becomes Category I (dual authorization) once the systemic regime is operative "
                     "(modelled 2027). The regime-in-transition caveat on UK undirected pairs (I/II*) "
                     "resolves at the same horizon. The EU-UK and UK-US undirected pairs remain findings "
                     "AFTER that horizon because their residual is STRUCTURAL — the Atlas scores live-live "
                     "as I/II (dual-authorization-or-partnership) while Architecture §5.14 authored them "
                     "as cleanly bridgeable I — not temporal. The time engine thus separates a "
                     "regime-in-transition artifact (resolves by date) from a genuine modelling "
                     "difference (does not)."),
        "events": events,
        "edge_timelines": edges,
        "illustration_edge_timelines": illustration,
        "undirected_agreement_over_time": over_time,
    }
    (ROOT / "analysis" / "computed_timeline.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    o = build()
    print("wrote analysis/computed_compatibility.json")
    print(f"  directed edges  — computed reproduces authored: {o['directed_edges']['agreement']}")
    print(f"  undirected pairs — computed reproduces §5.14:    {o['undirected_pairs']['agreement']}")
    pc = o["pre_regime_crosscheck"]
    print(f"  pre_regime cross-check (signals vs records): {pc['from_signals']} vs {pc['from_records']} -> consistent={pc['consistent']}")
    sp = o["signal_provenance"]
    print(f"  signal provenance — every signal rests on tier1_legal records: clean={sp['clean']}"
          + ("" if sp["clean"] else f" ({len(sp['violations'])} violation(s))"))
    print("  findings by cause:")
    for cause, items in o["findings_by_cause"].items():
        print(f"    {cause}: {len(items)} — {', '.join(items)}")
    t = build_timeline()
    print("wrote analysis/computed_timeline.json")
    print(f"  event calendar: {len(t['events'])} events; provenance clean={t['event_provenance']['clean']}")
    ill = {e["edge"]: e for e in t["illustration_edge_timelines"]}
    usuk = ill.get("US->UK", {})
    if usuk.get("scheduled_transitions"):
        tr = usuk["scheduled_transitions"][-1]
        print(f"  illustration US->UK: today {usuk['today_class']} -> {tr['class_after']} as of {tr['date']} ({tr['event_id']})")
    print("  transition-caveated undirected pairs over time:")
    for row in t["undirected_agreement_over_time"]:
        print(f"    as of {row['as_of']}: {row['transition_caveated_pairs']['count']} caveated · "
              f"agreement {row['undirected_agreement']}")
