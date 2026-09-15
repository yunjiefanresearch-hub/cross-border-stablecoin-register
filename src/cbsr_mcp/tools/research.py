"""Evidence, research, stakeholder and reconciliation tools."""
from __future__ import annotations
from typing import Optional
from ..core.catalog import JURISDICTIONS
from ..data.repository import DATA, RECORDS, CORRIDORS, record_summary
from .architecture import (ANALYSIS, COMPUTED, COMPUTED_CORRIDOR_SKELETONS, EVENT_CALENDAR,
    STAKEHOLDER_DB, SUBSTRATE, compose_via_substrate)
from .registry import tool
_summary = record_summary

_SH_IMPLICATION = {
    "C1": {"open": "issuance open", "licence_gated": "issuance is authorization-gated",
           "closed_set": "issuance limited to a defined set of entities",
           "host_currency_first": "host-currency issuance prioritized",
           "no_pathway": "no operative issuance pathway yet", "prohibition": "issuance prohibited"},
    "C2": {"prescribed_hqla": "reserve must be high-quality liquid assets",
           "prescribed_flex": "reserve prescribed with some flexibility", "informational": "reserve disclosure only"},
    "C3": {"permitted": "yield permitted", "prohibited_issuer": "issuer may not pay yield",
           "prohibited_incl_agents": "issuer and agents may not pay yield", "silent": "yield treatment unsettled"},
    "C4": {"payment_instrument": "treated as a payment instrument, not a security",
           "contested_routing": "classification turns on the routing structure",
           "security": "treated as a security / unauthorized offering"},
    "C5": {"bank_only": "bank-only issuance", "bank_and_nonbank": "bank and non-bank issuers admitted",
           "layered_separation": "roles separated by licensed function", "unset": "routing architecture unsettled"},
    "C6": {"open": "no data-localization barrier to supervisory sharing", "transfer_gated": "cross-border transfer is gated",
           "localized": "data localization applies", "restrictive": "data sharing restricted"},
    "C7": {"open": "no usage cap; dual authorization available", "usage_capped": "scale / usage capped",
           "channelled": "foreign tokens admitted only via a determination / channel", "prohibition": "foreign tokens prohibited"},
    "C8": {"coordinated": "supervisory coordination available", "constrained": "supervisory coordination constrained"},
}


@tool
def stakeholder_database() -> dict:
    """The Atlas §8 stakeholder catalogue: the actor personas (issuer, distributor, regulators, treasury,
    holder, ...), each with its lens, the C1–C8 constraints that bear on it, and the corridor archetypes
    (RC/SC/TC/DC) it engages. Pair with profile_for() to project a corridor onto a persona."""
    if not STAKEHOLDER_DB:
        return {"error": "stakeholder database not present (run scripts/stakeholders.py then build.py)"}
    return {"archetype_legend": STAKEHOLDER_DB.get("archetype_legend"),
            "stakeholders": STAKEHOLDER_DB.get("stakeholders"), "note": STAKEHOLDER_DB.get("note")}


@tool
def profile_for(stakeholder: str, origin: str, destination: str) -> dict:
    """PROJECT a directed corridor onto a stakeholder persona (Atlas §8). Returns the persona's lens, the
    corridor's derived class, a per-constraint reading of the origin/dest poles the persona cares about
    (each citing its backing record), the engaged archetypes and inbound mechanism, and a verification
    caveat. Introduces NO new facts — every line is read from an existing record — so the profile is
    preview, bounded by the verification status of the cells it reads."""
    if not STAKEHOLDER_DB or not SUBSTRATE:
        return {"error": "stakeholder database / substrate not present (run scripts/stakeholders.py + substrate.py then build.py)"}
    s = STAKEHOLDER_DB.get("stakeholders", {}).get(stakeholder)
    if s is None:
        return {"error": f"unknown stakeholder '{stakeholder}'", "known": sorted(STAKEHOLDER_DB.get("stakeholders", {}))}
    o, d = origin.upper(), destination.upper()
    if o not in JURISDICTIONS or d not in JURISDICTIONS:
        return {"error": f"unknown jurisdiction(s): {origin}/{destination}"}
    derived = compose_via_substrate(o, d)
    cls = derived.get("substrate_class")
    id2tier = {r["id"]: r.get("evidence_tier") for r in RECORDS}
    reading, cited = [], []
    for side, j in (("origin", o), ("dest", d)):
        for c in s.get("reads", {}).get(side, []):
            cell = SUBSTRATE.get("cells", {}).get(j, {}).get(c)
            if not cell:
                reading.append({"side": side, "jurisdiction": j, "constraint": c, "pole": None,
                                "implication": "pole unset — indeterminate at the substrate level"})
                continue
            pole = cell.get("pole"); rid = (cell.get("derived_from") or [None])[0]
            reading.append({"side": side, "jurisdiction": j, "constraint": c, "pole": pole,
                            "record": rid, "implication": _SH_IMPLICATION.get(c, {}).get(pole, pole)})
            if rid:
                cited.append(rid)
    corr = next((c for c in CORRIDORS if c.get("origin") == o and c.get("destination") == d), None)
    arche = sorted(set(s.get("archetypes", [])) & set(corr.get("archetypes", []))) if corr else s.get("archetypes")
    cited = sorted(set(cited))
    unver = [r for r in cited if id2tier.get(r) != "resolution_text"]
    return {"edge": f"{o}->{d}", "stakeholder": stakeholder, "label": s.get("label"), "lens": s.get("lens"),
            "corridor_class": cls, "archetypes_engaged": arche,
            "inbound_mechanism": corr.get("inbound_mechanism") if corr else None,
            "reading": reading, "provenance": {"records": cited},
            "verification_status": (f"preview — rests on {len(cited)} cell(s), {len(unver)} not yet verified to "
                                    f"resolution_text; not citable authority until those are verified")}


@tool
def edge_coverage() -> dict:
    """Edge-layer coverage: how many directed corridors carry a record. Distinguishes the hand-authored
    RICH corridors (with infrastructure_overlap, bespoke inbound detail, curated archetypes, prose) from
    the COMPUTED SKELETONS (derived fields + provenance) and the still-indeterminate edges (into the UK,
    in transition)."""
    if not COMPUTED_CORRIDOR_SKELETONS:
        return {"error": "edge skeletons not present (run scripts/build_edge_skeletons.py then build.py)"}
    cov = COMPUTED_CORRIDOR_SKELETONS.get("coverage", {})
    return {**cov, "cross_check_clean": COMPUTED_CORRIDOR_SKELETONS.get("cross_check", {}).get("clean"),
            "note": ("rich corridors are the enriched gold tier; skeletons carry only derived fields, with "
                     "infrastructure_overlap and bespoke analysis left as a per-edge enrichment backlog.")}


@tool
def corridor_skeleton(origin: str, destination: str) -> dict:
    """Return the corridor record for a directed edge: the hand-authored RICH record if one exists,
    otherwise the COMPUTED SKELETON (derived feasibility class, inbound mechanism test + administrator,
    baseline archetypes, directed interaction sets, and provenance). Skeletons introduce no new facts and
    leave empirical fields (infrastructure_overlap, bespoke detail) explicitly unset."""
    o, d = origin.upper(), destination.upper()
    if o not in JURISDICTIONS or d not in JURISDICTIONS:
        return {"error": f"unknown jurisdiction(s): {origin}/{destination}"}
    rich = next((c for c in CORRIDORS if c.get("origin") == o and c.get("destination") == d), None)
    if rich:
        return {"tier": "authored_rich", **rich}
    for s in COMPUTED_CORRIDOR_SKELETONS.get("skeletons", []):
        if s.get("origin") == o and s.get("destination") == d:
            return s
    return {"edge": f"{o}->{d}", "tier": "none",
            "note": "no record — edge is indeterminate at the substrate level (likely into the UK, in transition)"}


VERIFICATION_LEDGER = (DATA.get("analysis") or {}).get("verification_ledger", {})


@tool
def verification_ledger(jurisdiction: Optional[str] = None) -> dict:
    """The external primary-source verification pass (v0.9.5) audit trail.

    Records, per cell, the binding status of the cited instrument, the official URL attached, and the
    tier the disposition applied. The pass's discipline is that citability is capped by binding status,
    NOT by whether the official text was located: resolution_text is applied only where binding_status is
    in_force_enacted AND the proposition was confirmed against official text; made_not_commenced (e.g. UK
    SI 2026/102), finalized_policy_pending (e.g. SG MAS SCS framework), and pending_proposal (e.g. US
    CLARITY/NPRM, BR BCB) cells receive the URL + binding_status but are held at firm_summary; prohibition
    cells (CN) remain unverified. Filter by jurisdiction (e.g. 'EU', 'US', 'HK', 'UK', 'SG', 'CN', 'BR')."""
    if not VERIFICATION_LEDGER:
        return {"error": "verification ledger not present in dataset.json (run scripts/apply_verification.py then build.py)"}
    entries = VERIFICATION_LEDGER.get("entries", [])
    if jurisdiction:
        j = jurisdiction.upper()
        entries = [e for e in entries if e.get("jurisdiction") == j]
    from collections import Counter
    bs = Counter(e.get("binding_status") for e in entries)
    promoted = [e["cell"] for e in entries if e.get("applied_tier") == "resolution_text"]
    return {
        "performed_by": VERIFICATION_LEDGER.get("performed_by"),
        "discipline": VERIFICATION_LEDGER.get("discipline"),
        "filter": jurisdiction.upper() if jurisdiction else "all",
        "count": len(entries),
        "binding_status_breakdown": dict(bs),
        "promoted_to_resolution_text": promoted,
        "entries": entries,
    }


COMPUTED_CONVERGENCE: dict = ANALYSIS.get("computed_convergence", {})

# The lawyer-citable test, replicated so per-record "why not citable" can be answered inline.
_CITABLE_AXES = (
    ("claim_class", "tier1_legal", "not a proposition of law (tier1_legal)"),
    ("status", "in_force", "not currently in force"),
    ("evidence_tier", "resolution_text", "not confirmed against the official text (resolution_text)"),
)


def _citable_blocks(r: dict) -> list[list]:
    """Return every structural, source, freshness or independent-review gate that fails."""
    blocks = []
    for field, want, why in _CITABLE_AXES:
        if r.get(field) != want:
            blocks.append([field, r.get(field), why])
    freshness = r.get("freshness") or {}
    if r.get("source_disposition") != "official":
        blocks.append(["source_disposition", r.get("source_disposition"), "source is not classified as official"])
    if freshness.get("review_status") != "current":
        blocks.append(["review_status", freshness.get("review_status"), "source check is not current"])
    if r.get("review_stage") != "reconciled":
        blocks.append(["review_stage", r.get("review_stage"), "independent second review is not reconciled"])
    return blocks


@tool
def events_by_kind(kind: Optional[str] = None) -> dict:
    """
    The regulatory event calendar grouped by trigger_kind — the paper's typology of triggers by the
    KIND OF CERTAINTY each carries (flagship §3), not merely by date. This is the view that separates the
    one trigger kind that moves a dated feasibility horizon (fully-scheduled) from the kinds that do not
    (a dated change that alters accessibility within a live regime; a dated change with an explicitly
    empty class effect; a bill with no commencement date surfaced only as an if-enacted branch; a
    pending enactment that hardens a binding status without moving any class). Use it to answer "which of
    these changes actually moves a corridor's class, and which are dated-but-inert or contingent?"

    Returns the trigger_kind_legend (purpose, per-kind definitions, and the horizon rule), the events
    bucketed by trigger_kind, and a per-kind moves_a_horizon flag. Optional `kind` filter (e.g.
    'fully-scheduled', 'intra-regime-gating', 'dated-empty-effect', 'inbound-recognition',
    'contingent-no-date', 'enacted-not-commenced', 'contingent-not-class-change').
    """
    if not EVENT_CALENDAR:
        return {"error": "event calendar not present (run scripts/compose.py then build.py)"}
    legend = EVENT_CALENDAR.get("trigger_kind_legend", {})
    evs = EVENT_CALENDAR.get("events", [])
    if kind:
        evs = [e for e in evs if e.get("trigger_kind") == kind]
    buckets: dict[str, list] = {}
    for e in evs:
        tk = e.get("trigger_kind", "unclassified")
        buckets.setdefault(tk, []).append({
            "id": e.get("id"), "jurisdiction": e.get("jurisdiction"), "title": e.get("title"),
            "status": e.get("status"), "effective_date": e.get("effective_date"),
            "trigger": e.get("trigger"),
            # a change moves a horizon only if it is fully-scheduled AND carries a non-empty effect
            "moves_a_horizon": e.get("trigger_kind") == "fully-scheduled" and bool(e.get("effect")),
        })
    return {
        "as_of_base": EVENT_CALENDAR.get("as_of_base"),
        "filter": kind or "all",
        "count": len(evs),
        "by_kind": buckets,
        "horizon_rule": legend.get("horizon_rule"),
        "legend": legend,
        "note": ("Only fully-scheduled events with a non-empty effect move a compose() horizon. "
                 "dated-empty-effect, intra-regime-gating, and inbound-recognition events are dated "
                 "but move no feasibility class; contingent kinds have no date and are surfaced only "
                 "as if-enacted branches. This grouping asserts no new facts — trigger_kind is a field "
                 "on each event."),
    }


@tool
def convergence(side: Optional[str] = None) -> dict:
    """
    The cross-jurisdiction yield-line convergence view (flagship §4.5): independent legislative systems
    converging on the same functional boundary around stablecoin yield — yield for merely HOLDING the
    instrument is prohibited, while ACTIVITY-LINKED rewards are permitted. This reshapes the existing
    per-jurisdiction permitted_activity_yield records into that cross-jurisdiction line; it asserts NO
    new facts (every field is copied from a record) and it respects the register's citable-purity
    discipline: the two-sided line is asserted at citable depth ONLY where a cell is
    tier1_legal + in_force + resolution_text AND both sides are documented (today: the US alone).

    Returns the finding, the discipline statement, and the jurisdictions tiered by role: the citable
    two-sided `anchor` (US), the `sibling` restriction (SG), the documented `counter_example` (CH, where
    holder yield is permitted-but-constrained), `holder_prohibition_in_force` (EU/HK/JP/AE — the
    prohibited side in force and citable, the permitted side carried as backlog), `draft_would_align`
    (KR/TW — would align if enacted), and `backlog_or_not_applicable`. Optional `side` filter, one of:
    'anchor', 'sibling', 'counter_example', 'holder_prohibition_in_force', 'draft_would_align',
    'backlog_or_not_applicable'.
    """
    if not COMPUTED_CONVERGENCE:
        return {"error": "convergence view not present (run scripts/build_convergence.py then build.py)"}
    c = COMPUTED_CONVERGENCE
    if side:
        block = c.get(side)
        if block is None:
            return {"error": f"unknown side {side!r}",
                    "valid_sides": ["anchor", "sibling", "counter_example",
                                    "holder_prohibition_in_force", "draft_would_align",
                                    "backlog_or_not_applicable"]}
        return {"dimension": c.get("dimension"), "side": side, "records": block,
                "discipline": c.get("discipline"), "provenance": c.get("provenance")}
    return {
        "dimension": c.get("dimension"),
        "finding": c.get("finding"),
        "discipline": c.get("discipline"),
        "method": c.get("method"),
        "anchor": c.get("anchor"),
        "sibling": c.get("sibling"),
        "counter_example": c.get("counter_example"),
        "holder_prohibition_in_force": c.get("holder_prohibition_in_force"),
        "draft_would_align": c.get("draft_would_align"),
        "backlog_or_not_applicable": c.get("backlog_or_not_applicable"),
        "summary_counts": c.get("summary_counts"),
        "provenance": c.get("provenance"),
    }


COMPUTED_FORWARD_VIEW: dict = ANALYSIS.get("computed_forward_view", {})


@tool
def forward_view(jurisdiction: Optional[str] = None) -> dict:
    """
    The per-jurisdiction supervisor forward view (Atlas §4.4): the trigger register re-sorted BY
    JURISDICTION rather than by trigger, into the view a supervisory reader actually needs. For a
    jurisdiction it answers: which pending developments will change the corridors INTO and OUT OF my
    jurisdiction, and which counterpart jurisdictions am I most exposed to. Each jurisdiction carries its
    own pending events (flagged class-moving vs accessibility-only), the inbound and outbound directed
    edges that change feasibility class under the pending set (each attributed to the trigger causing it
    and split into own-trigger-driven vs counterpart-driven), the counterpart jurisdictions on the other
    end ranked by exposure, and a one-line supervisor_reading. It asserts NO new facts: every movement is
    read from the corridor-state precompute and every event from the event calendar.

    This is the view §4.4 calls the change that makes the forward map usable to supervisory readers: it
    turns "the EU is low-sensitivity" into the operational statement that the EU's own pending change
    (the MiCA 143(3) expiry) is accessibility-only and moves no class, while separately a set of the EU's
    corridors will reclassify when counterparts enact. Pass `jurisdiction` (e.g. 'EU', 'KR') for one
    jurisdiction; omit it for all twelve plus the reading key.
    """
    if not COMPUTED_FORWARD_VIEW:
        return {"error": "forward view not present (run scripts/build_forward_view.py then build.py)"}
    fv = COMPUTED_FORWARD_VIEW
    per = fv.get("jurisdictions", {})
    if jurisdiction:
        j = jurisdiction.upper()
        if j not in per:
            return {"error": f"unknown jurisdiction {jurisdiction!r}", "valid": sorted(per.keys())}
        return {"as_of_base": fv.get("as_of_base"), "jurisdiction": j,
                "forward": per[j], "reading_key": fv.get("reading_key"),
                "provenance": fv.get("provenance")}
    return {
        "as_of_base": fv.get("as_of_base"),
        "method": fv.get("method"),
        "reading_key": fv.get("reading_key"),
        "jurisdictions": per,
        "provenance": fv.get("provenance"),
    }


@tool
def reconciliation(only_divergences: bool = False) -> dict:
    """
    The computed-vs-authored corridor reconciliation: for every undirected jurisdiction pair, the class
    the compose() engine derives from the signal table set against the class a human authored, with an
    agree/disagree flag and, where they differ, the named cause. This is the register auditing its own
    analysis layer — the divergences are not errors to hide but findings: today they are exactly the
    pairs where one side is a regime-in-transition (the UK), which the engine flags as Category T while
    the human authored the eventual steady-state class.

    Returns the agreement ratio, the pairs (each with computed_category, authored_category, agree,
    basis, finding), and findings_by_cause (the divergences grouped by their cause). Set
    `only_divergences=true` to return just the disagreeing pairs.
    """
    pairs = COMPUTED.get("undirected_pairs", {})
    rows = pairs.get("pairs", []) if isinstance(pairs, dict) else []
    if not rows:
        return {"error": "reconciliation not present (run scripts/compose.py then build.py)"}
    fbc = pairs.get("findings_by_cause") or COMPUTED.get("findings_by_cause", {})
    shown = [p for p in rows if not p.get("agree")] if only_divergences else rows
    return {
        "agreement": pairs.get("agreement"),
        "count_total": len(rows),
        "count_divergent": sum(1 for p in rows if not p.get("agree")),
        "filter": "divergences_only" if only_divergences else "all",
        "pairs": shown,
        "findings_by_cause": fbc,
        "note": ("A divergence is a finding, not a defect: the engine flags a regime-in-transition side "
                 "as Category T, while the authored class is the steady state. compose_corridor(as_of=…) "
                 "and corridor_timeline show how such a pair resolves over time."),
    }


@tool
def records(
    claim_class: Optional[str] = None,
    evidence_tier: Optional[str] = None,
    status: Optional[str] = None,
    binding_status: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    dimension: Optional[str] = None,
    citable_only: bool = False,
) -> dict:
    """
    The evidence-axis record browser: filter the register along the axes that decide citability —
    claim_class (KIND: tier1_legal vs tier2_operational), evidence_tier (PROVENANCE: resolution_text /
    mixed / firm_summary / unverified), status, and binding_status — and get, for every record, whether it is
    lawyer-citable and, if not, exactly which axis blocks it (the "why not citable" x-ray). This is the
    complement to query() (which filters by jurisdiction/dimension/status): use records() to reason about
    the two-axis evidence model and the verification frontier.

    Args (all optional, AND-combined):
        claim_class: 'tier1_legal' | 'tier2_operational'.
        evidence_tier: 'resolution_text' | 'mixed' | 'firm_summary' | 'unverified'.
        status: 'in_force' | 'transitional' | 'proposed' | 'consultation'.
        binding_status: e.g. 'in_force_enacted' | 'made_not_commenced' | 'finalized_policy_pending' |
                        'pending_proposal' | 'prohibition'.
        jurisdiction: e.g. 'US'. dimension: one of the 15 dimension keys.
        citable_only: if true, also require official/current/independently reconciled review evidence.
    Returns a count, a breakdown by (claim_class × evidence_tier), and per-record summaries each carrying
    `citable` and `blocks` (the failing axes).
    """
    from collections import Counter
    j = jurisdiction.upper() if jurisdiction else None
    out, axis = [], Counter()
    for r in RECORDS:
        if j and r.get("jurisdiction") != j:
            continue
        if dimension and r.get("dimension") != dimension:
            continue
        if claim_class and r.get("claim_class") != claim_class:
            continue
        rt = r.get("evidence_tier") or "unverified"
        if evidence_tier and rt != evidence_tier:
            continue
        if status and r.get("status") != status:
            continue
        if binding_status and r.get("binding_status") != binding_status:
            continue
        blocks = _citable_blocks(r)
        is_citable = not blocks
        if citable_only and not is_citable:
            continue
        s = _summary(r)
        s["citable"] = is_citable
        s["blocks"] = blocks
        out.append(s)
        axis[f"{r.get('claim_class')} × {rt}"] += 1
    return {
        "count": len(out),
        "citable_in_result": sum(1 for r in out if r["citable"]),
        "filters": {"claim_class": claim_class, "evidence_tier": evidence_tier, "status": status,
                    "binding_status": binding_status, "jurisdiction": j, "dimension": dimension,
                    "citable_only": citable_only},
        "by_claim_class_x_evidence_tier": dict(sorted(axis.items())),
        "records": out,
        "citable_filter": {"claim_class": "tier1_legal", "status": "in_force",
                           "evidence_tier": "resolution_text", "source_disposition": "official",
                           "review_status": "current", "review_stage": "reconciled"},
        "note": ("`citable` requires structural legal evidence plus official/current/reconciled review; `blocks` lists every axis a record "
                 "fails. Operational facts (tier2_operational) are excluded by kind even when "
                 "well-sourced; draft provisions by status; unverified legal points by tier."),
    }
