#!/usr/bin/env python3
"""migrate_from_v0_9_92.py — deterministic, zero-dependency data migration.

This script is the *executable specification* of exactly what changed in the corridor artifact
between the v0.9.92 tooling release and the current release (v0.10.0). Run it on the v0.9.92
artifact and you get, byte-for-byte, the artifact this repository ships.

It is also the upstream fold-in recipe: the same transforms belong in the register's authored YAML,
its node records, its event calendar, and scripts/build_corridors_directed.py, after which a clean
regeneration reproduces this output and this script becomes a no-op.

What it changes (and only this):

  N1  infrastructure_overlap  string  ->  {"bloc": <enum>, "note": <text|null>}
      * `bloc` is recomputed from the settlement-substrate partition function (ground
        truth), so the two authored US<->HK edges are corrected from an implied "none"
        to their true value "cross-bloc" (US on Project Agora; HK on mBridge + Ensemble).
      * `note` preserves the original free text verbatim, except the two US<->HK edges.

  m1  HK->BR seed edge: schema tag  "corridor/v2-rich" -> "corridor/v3-directed-edge".
  m4  HK->BR seed edge: the inline "... CONFIRM date against SFC source" editorial marker
      is removed from boundary_analysis[0].sources[3] and re-homed in a structured
      `verification_backlog` field.
  m5  HK->BR seed edge: feasibility_class prose leads with the DIRECTED class (Category II).

  N3  "Corridor Atlas v0.2.3" -> "Corridor Atlas v0.2.5" everywhere it appears in edge prose.
  M2  a top-level `register_version` field is stamped into the artifact meta.

  F-TW    the CN/KR->TW edges stop calling Taiwan's VAS Act a "draft" (it is enacted).
  F-EU    the MiCA Art. 58(3) ceiling reads the statutory conjunctive "and", not "or".
  NF-4    the ->TW contingent event is renamed `tw-vas-act-commencement` (enactment happened).
  F-TW-2  the ->TW administrator reads `FSC + CBC (dual approval)`.

  ---- new in v0.10.0: the three P0 corrections the eighth and ninth reviews gated release on ----

  NF-1  DESTINATION-FIRST PRECEDENCE. Every `class_code` is now recomputed by the published rule
        `tools/class_rule.py:class_of` over the published `data/signal_table.json`, instead of the
        artifact's undocumented origin-drag-first rule. Corridor Atlas v0.2.5 s.3.4/s.4.1 is
        destination-first ("Three classes are determined entirely by the destination ... the
        destination sets the class on every edge except the twenty-seven where an origin-side
        issuance gap overrides it"), and its own edge register scores `KR -> PRC` as blocked and
        `TW -> KR` as pre-regime. The artifact scored both as `III`. Four edges move:
            TW->CN, KR->CN :  III -> blocked      (a prohibition is not a "partnership route")
            CN->KR, TW->KR :  III -> pre_regime
        This retires lint m7 by FIXING it, not by excusing it.

  E1 / VB-06 / F-US-1 / E8  THE UNITED STATES IS ENACTED-NOT-COMMENCED.
        GENIUS Act s.20: the Act takes effect on the earlier of 18 months after enactment
        (2027-01-18) or 120 days after the primary federal payment stablecoin regulators issue
        final regulations. At the 2026-06-30 snapshot only PROPOSED rules existed. So the s.18
        comparability gate is not yet available, and the 8 token-holder->US edges move
            II -> T   with a `scheduled_with_cap` trigger at 2027-01-18 (an outer cap, not a
                      gazetted date -- it can fall sooner).
        Their prose is rewritten from "none granted to date" (a MARKET observation doing a
        proposition of law's work -- errata E8) to "the gate is not yet in force".
        This is a SECOND dated horizon, and it is EARLIER than the UK's 2027-10-25.

  NF-3  ORIGIN DRAG READS A LEGAL SIGNAL. `class_of` reads `token_regime` (tier1_legal), never
        `token_in_issue` (tier2_operational). The US and UK stay token-holding origins because
        state trust/money-transmitter regimes and the EMRs 2011 respectively authorize issuance
        TODAY -- a proposition of law, not "USDC exists". Stated, not implied.

  class_basis  every edge now carries, as data, WHICH precedence step decided its class, the
        governing jurisdiction, the claim_class of the deciding signal, the binding_status of the
        instrument, and the instrument itself. The three-axis evidence model finally reaches this
        layer (verifier gate EV1).

  origin_override  Atlas v0.2.5 carries an origin-egress override on every CN-> row (mainland
        capital controls), every SG-> row (MAS DTSP statement) and every KR-> row (Korea FX,
        conditional and dormant). The artifact carried it on ONE edge. Now on all 33 (gate OO1).

Usage:
    python3 tools/migrate_from_v0_9_92.py \
        --in  data/legacy/computed_corridors_directed.v0.9.92.json \
        --out data/computed_corridors_directed.json

    # verify only (no write): confirm an artifact is already in current (v0.10.0) shape
    python3 tools/migrate_from_v0_9_92.py --check data/computed_corridors_directed.json

The transform is idempotent: re-running it on an already-migrated artifact reproduces it.
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
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import class_rule  # the PUBLISHED class function + signal-table loader (zero-dep, in-repo)

REGISTER_VERSION = "0.9.9"          # the register release this corridor layer is cut from
ARTIFACT_REVISION = "0.10.0"        # this repository's revision of the corridor artifact
ARTIFACT_REVISION_DATE = "2026-07-08"
ATLAS_VERSION_OLD = "v0.2.3"
ATLAS_VERSION_NEW = "v0.2.5"

# Settlement-substrate membership (public central-bank project record). Kept identical to
# the verifier's INFRA and the builder's INFRA so all three agree by construction.
INFRA = {
    "agora":    {"US", "EU", "UK", "CH", "JP", "KR"},
    "mbridge":  {"CN", "HK", "AE"},
    "ensemble": {"HK", "SG"},
}
_BLOC_LABEL = {"agora": "Project Agora", "mbridge": "mBridge", "ensemble": "Project Ensemble"}


def bloc_of(o: str, d: str) -> str:
    """The settlement-substrate partition, returning the canonical enum for one directed edge.

    A shared experiment wins over a cross-bloc read; ends on rival blocs (Agora vs mBridge)
    are cross-bloc; anything with at least one end off the experiments is none.
    """
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


def _ends_on(j: str) -> str:
    on = sorted(_BLOC_LABEL[k] for k, v in INFRA.items() if j in v)
    return " + ".join(on) if on else "no shared wholesale-settlement experiment"


def canonical_note(o: str, d: str, bloc: str) -> str:
    """Deterministic gloss for the {bloc, note} object, IDENTICAL to the builder's
    scripts/build_corridors_directed.py:infra_overlap, so a clean upstream regeneration
    reproduces this artifact byte-for-byte. The free-text variants that v0.9.92 carried
    (ten distinct spellings for five blocs) are retired here on purpose: the enum in `bloc`
    is the machine field, and the note is a canonical human gloss, not a second source of truth."""
    if bloc == "cross-bloc":
        return (f"{o} on {_ends_on(o)}; {d} on {_ends_on(d)}. Rival bloc rails, not mutually "
                f"interoperable: no shared production or pilot settlement rail (commercial rails "
                f"subject to both regimes).")
    if bloc == "ensemble":
        # v0.9.94: do not over-assert. The HK-SG tie is an HKMA-Project-Ensemble / MAS-Project-
        # Guardian *alignment*; SG's formal Ensemble membership is a Tier-2 attribution pending
        # primary verification (verification_backlog VB-02). This restores the nuance the v0.9.93
        # canonical note dropped ("Both ends on Project Ensemble", which the third review flagged).
        return ("HKMA Project Ensemble and MAS Project Guardian alignment "
                f"({o} and {d}); SG's formal Project Ensemble membership is a Tier-2 attribution "
                "pending primary verification (verification_backlog VB-02).")
    if bloc in ("agora", "mbridge"):
        return f"Both ends on {_BLOC_LABEL[bloc]} ({o} and {d})."
    return f"{o} on {_ends_on(o)}; {d} on {_ends_on(d)}. At least one end off the shared experiments."


def promote_infra(edge: dict) -> dict:
    """N1: string|null infrastructure_overlap -> {bloc, note}, bloc recomputed from the
    partition (ground truth), note canonicalized to match the builder."""
    o, d = edge["origin"], edge["destination"]
    bloc = bloc_of(o, d)
    return {"bloc": bloc, "note": canonical_note(o, d, bloc)}


def fix_hk_br(edge: dict) -> None:
    """m1/m4/m5 on the HK->BR seed edge, in place."""
    if not (edge["origin"] == "HK" and edge["destination"] == "BR"):
        return
    # m1: migrate the legacy schema tag
    if edge.get("schema") == "corridor/v2-rich":
        edge["schema"] = "corridor/v3-directed-edge"
    # m4: pull the inline CONFIRM marker out of the source prose into a structured backlog field
    moved = []
    ba = edge.get("boundary_analysis") or []
    for bi, block in enumerate(ba):
        srcs = block.get("sources") or []
        for si, s in enumerate(srcs):
            if isinstance(s, str) and "CONFIRM" in s:
                head, _, tail = s.partition(" — CONFIRM")
                srcs[si] = head.strip()
                moved.append({
                    "field": f"boundary_analysis[{bi}].sources[{si}]",
                    "instrument": head.strip(),
                    "open_question": "CONFIRM" + tail if not tail.startswith(" ") else ("CONFIRM" + tail),
                    "status": "open",
                })
    if moved:
        # normalise the open_question text ("CONFIRM date against SFC source")
        for m in moved:
            m["open_question"] = m["open_question"].replace("CONFIRM", "confirm").strip()
        edge.setdefault("verification_backlog", [])
        edge["verification_backlog"].extend(moved)
    # m5: lead the feasibility_class prose with the DIRECTED class_code, not the pair category
    fc = edge.get("feasibility_class", "")
    if edge.get("class_code") == "II" and fc.startswith("Category I/II"):
        edge["feasibility_class"] = (
            "Category II (directed edge: channelled — counterparty-conditional + size-capped; "
            "the undirected HK-BR pair is I/II)"
            + fc[len("Category I/II (dual authorization or partnership) — counterparty-conditional + size-capped"):]
        ) if fc.startswith(
            "Category I/II (dual authorization or partnership) — counterparty-conditional + size-capped"
        ) else ("Category II " + fc[len("Category I/II "):])


def align_atlas_version(node):
    """N3: recursively replace the drifted Atlas version string in every str value, in both the
    prose form ('Corridor Atlas v0.2.3') and the tag form ('from_atlas_v0.2.3')."""
    if isinstance(node, dict):
        return {k: align_atlas_version(v) for k, v in node.items()}
    if isinstance(node, list):
        return [align_atlas_version(v) for v in node]
    if isinstance(node, str):
        return (node
                .replace("Corridor Atlas " + ATLAS_VERSION_OLD, "Corridor Atlas " + ATLAS_VERSION_NEW)
                .replace("from_atlas_" + ATLAS_VERSION_OLD, "from_atlas_" + ATLAS_VERSION_NEW))
    return node


def fix_taiwan_regime_prose(edge: dict) -> None:
    """F-TW (fourth review): the tokenless-origin -> TW edges (CN->TW, KR->TW) carried a stale
    inbound_mechanism.test 'No operative inbound regime (draft VAS Act)', describing Taiwan's
    Virtual Asset Service Act as a DRAFT, while the 9 token-holder -> TW transition edges (correctly)
    describe it as enacted on 2026-06-30. Same artifact, contradictory Taiwan status. The class_code
    (III via origin drag) is correct; only the prose is stale. Align it, so the artifact speaks with
    one voice about Taiwan and the new DG2 gate stays green."""
    if edge["destination"] != "TW":
        return
    im = edge.get("inbound_mechanism")
    if isinstance(im, dict) and isinstance(im.get("test"), str) and "draft VAS Act" in im["test"]:
        im["test"] = ("Virtual Asset Service Act enacted 2026-06-30, not yet commenced; inbound gate "
                      "not reached because the origin has no exportable authorizable token "
                      "(Category III via origin drag)")


def fix_mica_threshold(edge: dict) -> None:
    """F-EU (fourth review): MiCA Art. 23(1) (applied to EMTs mutatis mutandis by Art. 58(3)) sets a
    CONJUNCTIVE ceiling -- the issuer must stop issuing only when transactions are 'higher than
    1 million ... and EUR 200 000 000 respectively'. The US->EU edge prose wrote the two thresholds
    as 'or', which is a directional error (an 'or' cap bites earlier than the statutory 'and'). Align
    to the official text and flag that the EBA operative methodology is still pending (§3.7)."""
    im = edge.get("inbound_mechanism")
    if isinstance(im, dict) and isinstance(im.get("detail"), str):
        im["detail"] = im["detail"].replace(
            "the Article 58(3) ceiling (one million transactions/day or EUR 200m/day)",
            "the Article 58(3) ceiling (one million transactions/day and EUR 200m/day \u2014 both "
            "thresholds, per MiCA Art. 23(1) applied mutatis mutandis; EBA operative methodology pending)")


def fix_taiwan_administrator(edge: dict) -> None:
    """F-TW-2 (eighth review): Taiwan's VAS Act requires issuance approval from BOTH the FSC AND the
    central bank (CBC). The edges into TW wrote 'FSC (CBC consulted)' (transition) or 'FSC (Taiwan)'
    (skeleton), which understate the CBC's role from co-approver to consultee (or omit it). Correct
    to dual approval."""
    if edge["destination"] != "TW":
        return
    im = edge.get("inbound_mechanism")
    if isinstance(im, dict) and isinstance(im.get("administrator"), str):
        if im["administrator"] in ("FSC (CBC consulted)", "FSC (Taiwan)"):
            im["administrator"] = "FSC + CBC (dual approval)"


# ================================================================================================
# v0.10.0 transforms
# ================================================================================================

# Prose the recomputed classes carry. Kept in one place so the artifact speaks with one voice.
CLASS_PROSE = {
    "blocked":    "Blocked at destination (issuance / circulation prohibited)",
    "pre_regime": "Pre-regime (no operative destination regime yet)",
    "III":        "Category III (no direct issuance; partnership / coordination route)",
}
US_T_PROSE = ("Regime-in-transition (destination regime enacted, not yet operative; resolves to "
              "Category II on the earlier of 2027-01-18 or 120 days after final rules)")

US_GATE_TEST = ("GENIUS Act \u00a718 comparability determination + OCC registration; US-held reserves "
                "\u2014 enacted 2025-07-18, gate not yet operative (\u00a720)")
US_GATE_DETAIL = (
    "The \u00a718 pathway (unilateral Treasury comparability determination on SCRC recommendation + OCC "
    "registration + US-held reserves) is NOT YET AVAILABLE: per \u00a720 the Act takes effect on the earlier "
    "of 2027-01-18 (18 months after enactment) or 120 days after the primary federal payment stablecoin "
    "regulators issue final regulations, and at the 2026-06-30 snapshot only proposed rules had issued "
    "(OCC NPRM, FR 2026-03-02, comments closed 2026-05-01; FDIC and FinCEN/OFAC NPRMs 2026-04-10; "
    "Treasury \u00a74(c) NPRM April 2026). Earlier prose read \u2018none granted to date\u2019, which states a "
    "MARKET observation (no determination has been made) where a proposition of law is required (the "
    "gate is not in force) \u2014 the claim-class error Citable by Construction \u00a72.1 exists to prevent.")
US_TOKENLESS_TEST = (
    "GENIUS Act regime enacted 2025-07-18, \u00a718 inbound gate not yet operative (\u00a720); inbound gate not "
    "reached because the origin has no exportable authorizable token (Category III via origin drag)")

ORIGIN_OVERRIDE_ADMIN = {
    "CN": "SAFE / CAC / PBOC",
    "SG": "MAS",
    "KR": "MOEF / Bank of Korea (foreign-exchange controls)",
}


def recompute_class(edge: dict, signals: dict) -> str:
    """NF-1: replace the artifact's origin-drag-first class with the published destination-first
    precedence, derived from data/signal_table.json by tools/class_rule.py. Returns the rule id."""
    o, d = edge["origin"], edge["destination"]
    cls, rule = class_rule.class_of(o, d, signals)
    old = edge.get("class_code")
    edge["class_code"] = cls
    edge["origin_drag"] = (rule == "origin_drag")
    if old != cls:                                   # only rewrite prose where the class moved
        if d == "US" and cls == "T":
            edge["feasibility_class"] = US_T_PROSE
        elif cls in CLASS_PROSE:
            edge["feasibility_class"] = CLASS_PROSE[cls]
        else:                                        # defensive: no other class moves in v0.10.0
            raise AssertionError(f"unexpected class move {o}->{d}: {old} -> {cls}")
    return rule


def add_class_basis(edge: dict, rule: str, signals: dict) -> None:
    """Make the derivation a first-class field: which precedence step fired, on whose signal, of
    what claim_class, resting on an instrument of what binding status. Gate EV1 re-checks it."""
    o, d = edge["origin"], edge["destination"]
    gov = class_rule.governing_jurisdiction(o, d, rule)
    signal = "token_regime" if rule == "origin_drag" else "inbound_gate"
    sig = signals[gov][signal]
    edge["class_basis"] = {
        "rule": rule,
        "governing_jurisdiction": gov,
        "signal": signal,
        "signal_value": sig["value"],
        "claim_class": sig["claim_class"],
        "binding_status": class_rule.binding_status_for(o, d, rule, signals),
        "evidence_tier": sig.get("evidence_tier", "unset"),
        "instrument": sig["instrument"],
        "record_ref": None,
    }


def fix_us_inbound_prose(edge: dict) -> None:
    """E8 / F-US-1: the inbound-US prose let a market observation do a proposition of law's job."""
    if edge["destination"] != "US":
        return
    im = edge.setdefault("inbound_mechanism", {})
    if edge["class_code"] == "T":
        im["test"] = US_GATE_TEST
        im["detail"] = US_GATE_DETAIL
        im["administrator"] = "US Treasury (Stablecoin Certification Review Committee) / OCC"
    else:                                            # the 3 tokenless-origin edges (III)
        im["test"] = US_TOKENLESS_TEST
    note = edge.get("note")
    if isinstance(note, str):
        edge["note"] = (
            note
            .replace("Because no comparability determination has been made to date, the corridor is "
                     "Category II in practice: operable in principle, pending a determination that "
                     "does not yet exist.",
                     "The \u00a718 gate is not yet in force (\u00a720: effective on the earlier of 2027-01-18 or "
                     "final rules + 120 days), so the edge is regime-in-transition today and resolves to "
                     "Category II on commencement. \u2018No determination has been granted\u2019 is a market "
                     "observation; \u2018the gate is not yet available\u2019 is the proposition of law.")
            .replace("Category II for the same reason the euro-into-US corridor is.",
                     "Regime-in-transition for the same reason the euro-into-US corridor is: the \u00a718 gate "
                     "is enacted but not yet operative (\u00a720). It resolves to Category II on commencement.")
            .replace("No comparability determination has been made for any jurisdiction including Japan, "
                     "so the corridor is Category II in this direction too \u2014 but for a different reason "
                     "than inbound: there the channel is the gate, here the comparability determination is.",
                     "The \u00a718 comparability gate is enacted but not yet operative (\u00a720), so the corridor "
                     "is regime-in-transition today and resolves to Category II on commencement \u2014 for a "
                     "different reason than inbound: there the channel is the gate, here the comparability "
                     "determination is.")
        )


def fix_destination_first_prose(edge: dict) -> None:
    """NF-1 prose: the four reclassified edges must not keep Category-III language."""
    o, d = edge["origin"], edge["destination"]
    if d == "CN" and edge["class_code"] == "blocked" and o in ("TW", "KR"):
        im = edge.setdefault("inbound_mechanism", {})
        im["test"] = "Issuance and circulation prohibited"
        im["administrator"] = "PBOC / CAC"
        im["detail"] = ("A destination prohibition dominates the origin\u2019s issuance gap: no "
                        "partnership or coordination route exists into a jurisdiction that bans the "
                        "instrument. \u94f6\u53d1\u30142026\u301542\u53f7, in force 2026-02-06.")
    if d == "KR" and edge["class_code"] == "pre_regime" and o in ("CN", "TW"):
        im = edge.setdefault("inbound_mechanism", {})
        im["test"] = "No operative inbound regime (draft DABA)"
        im["administrator"] = "FSC (Korea)"
        im["detail"] = ("A destination with no authorizable issuance pathway dominates the origin\u2019s "
                        "issuance gap: there is nothing to receive into, whatever the origin holds.")


def set_timeline(edge: dict, signals: dict) -> None:
    """Every `T` edge carries a dated (or explicitly undated) trigger; nothing else does.

    Extends the two-slot `scheduled`/`contingent` schema with the trigger typology the Feasibility
    paper claims but the artifact could not express: `date_kind` distinguishes a GAZETTED
    commencement (UK, 2027-10-25) from an OUTER CAP (US, <= 2027-01-18, may fall sooner) from an
    UNGAZETTED enactment awaiting commencement (TW). Gate TL2 enforces the T <-> timeline biconditional.
    """
    d = edge["destination"]
    if edge["class_code"] != "T":
        edge.pop("as_of_timeline", None)
        return
    gate = signals[d]["inbound_gate"]
    base = {"today_class": "T", "as_of_base": "2026-06-30", "scheduled": [], "contingent": []}
    if d == "UK":
        base["scheduled"] = [{
            "event_id": "uk-systemic-regime-operative",
            "effective_date": "2027-10-25",
            "date_kind": "gazetted",
            "status": "scheduled",
            "resolves_to": gate["resolves_to"],
            "basis": gate["instrument"],
        }]
    elif d == "US":
        base["scheduled"] = [{
            "event_id": "us-genius-act-effective",
            "effective_date": "2027-01-18",
            "date_kind": "outer_cap",
            "status": "scheduled_with_cap",
            "resolves_to": gate["resolves_to"],
            "basis": gate["instrument"],
        }]
    elif d == "TW":
        base["contingent"] = [{
            "event_id": "tw-vas-act-commencement",
            "effective_date": None,
            "date_kind": "ungazetted",
            "status": "contingent",
            "resolves_to": gate["resolves_to"],
            "basis": gate["instrument"],
        }]
    else:
        raise AssertionError(f"a T edge into {d} has no modelled trigger")
    edge["as_of_timeline"] = base


def set_origin_override(edge: dict, signals: dict) -> None:
    """Atlas v0.2.5 s.3.3 + its edge register: CN (mainland capital controls) and SG (MAS DTSP)
    carry an ACTIVE origin-egress override on every outbound row; KR carries a CONDITIONAL, DORMANT
    one (Korea FX -- dormant because there is no exportable won token for it to bite on). The
    artifact carried the flag on exactly one edge (SG->HK) and no gate checked it. Gate OO1 does."""
    o = edge["origin"]
    ov = signals[o]["egress_override"]
    if ov["value"] == "none":
        edge.pop("origin_override", None)
        return
    prior = edge.get("origin_override")
    detail = prior.get("detail") if isinstance(prior, dict) else None
    edge["origin_override"] = {
        "flag": "origin-egress override",
        "status": ov["value"],                       # active | conditional_dormant
        "basis": ov["instrument"],
        "administrator": ORIGIN_OVERRIDE_ADMIN[o],
        "detail": detail,
    }


def update_meta(doc: dict, signals: dict) -> None:
    from collections import Counter
    dist = Counter(e["class_code"] for e in doc["edges"])
    doc["coverage"]["class_distribution"] = dict(sorted(dist.items()))
    doc["coverage"]["timeline_edges"] = sum(1 for e in doc["edges"] if "as_of_timeline" in e)
    doc["note"] = (
        "Directed-edge interaction_sets are the Atlas per-direction refinement and may differ from "
        "the undirected \u00a75.14 pair; only the compatibility_category is a hard cross-layer "
        "relationship and is enforced. From v0.10.0 every class_code is DERIVED, not authored: "
        "tools/class_rule.py:class_of applies the Corridor Atlas v0.2.5 destination-first precedence "
        "(prohibition > no-regime > origin-drag > in-transition > operative gate type) to "
        "data/signal_table.json, and tools/recompute_classes.py re-derives all 132 and diffs them "
        "against this artifact. `materialized_from` is a PRODUCTION-provenance partition (9 authored "
        "+ 106 skeleton + 17 event-calendar transition edges) and is orthogonal to class: 25 edges "
        "now carry an as_of_timeline, not 17.")
    doc["provenance"] = {
        "clean": True,
        "basis": ("Every class_code is recomputed from data/signal_table.json by the published rule "
                  "tools/class_rule.py:class_of. The rule reads exactly two signals -- the "
                  "destination's `inbound_gate` and the origin's `token_regime` -- both "
                  "claim_class=tier1_legal, and never reads `token_in_issue` (tier2_operational). "
                  "The signal-provenance guarantee is enforced by SIG1 and demonstrated empirically "
                  "by `recompute_classes.py --prove-tier2-inert`, which flips every market signal and "
                  "asserts no class moves. Each edge's class_basis records which precedence step "
                  "decided it, on whose signal, resting on which instrument, at what binding_status."),
        "class_rule": "destination-first precedence (Corridor Atlas v0.2.5 \u00a73.4/\u00a74.1)",
        "signal_table": "data/signal_table.json",
    }


def migrate(doc: dict) -> dict:
    signals = class_rule.load()["signals"]

    doc = align_atlas_version(doc)                       # N3 (do first: touches all prose)
    # M2: stamp the register version + this repository's artifact revision into the meta
    out = {}
    for k, v in doc.items():
        out[k] = v
        if k == "generated" and "register_version" not in doc:
            out["register_version"] = REGISTER_VERSION
            out["artifact_revision"] = ARTIFACT_REVISION
            out["artifact_revision_date"] = ARTIFACT_REVISION_DATE
    out.setdefault("register_version", REGISTER_VERSION)
    out["artifact_revision"] = ARTIFACT_REVISION
    out["artifact_revision_date"] = ARTIFACT_REVISION_DATE

    for e in out["edges"]:
        fix_hk_br(e)                                     # m1/m4/m5
        fix_taiwan_regime_prose(e)                       # F-TW  (fourth review)
        fix_mica_threshold(e)                            # F-EU  (fourth review)
        fix_taiwan_administrator(e)                      # F-TW-2 (eighth review)
        e["infrastructure_overlap"] = promote_infra(e)   # N1

        rule = recompute_class(e, signals)               # NF-1 + E1/VB-06 (class, origin_drag, prose)
        add_class_basis(e, rule, signals)                # three-axis model reaches this layer (EV1)
        fix_us_inbound_prose(e)                          # E8 / F-US-1
        fix_destination_first_prose(e)                   # NF-1 prose
        set_timeline(e, signals)                         # NF-4 + scheduled_with_cap (TL1/TL2)
        set_origin_override(e, signals)                  # Atlas origin-override, all 33 (OO1)

    update_meta(out, signals)
    return out


def is_migrated(doc: dict) -> tuple[bool, list]:
    """Structural + semantic staleness check. Everything the migration guarantees is asserted here,
    so `--check` on a shipped artifact is a real gate, not a version-string comparison."""
    problems = []
    signals = class_rule.load()["signals"]

    if "register_version" not in doc:
        problems.append("meta.register_version missing (M2)")
    if doc.get("artifact_revision") != ARTIFACT_REVISION:
        problems.append(f"meta.artifact_revision != {ARTIFACT_REVISION} (v0.10.0)")

    for e in doc.get("edges", []):
        o, d = e["origin"], e["destination"]
        io = e.get("infrastructure_overlap")
        if not (isinstance(io, dict) and "bloc" in io):
            problems.append(f"{o}->{d}: infrastructure_overlap not structured (N1)")
        elif io["bloc"] != bloc_of(o, d):
            problems.append(f"{o}->{d}: bloc {io['bloc']!r} != partition {bloc_of(o, d)!r}")
        if e.get("schema") == "corridor/v2-rich":
            problems.append(f"{o}->{d}: legacy schema tag (m1)")

        want_cls, want_rule = class_rule.class_of(o, d, signals)
        if e.get("class_code") != want_cls:
            problems.append(f"{o}->{d}: class_code {e.get('class_code')!r} != published rule "
                            f"{want_cls!r} (NF-1 / E1)")
        cb = e.get("class_basis")
        if not isinstance(cb, dict) or cb.get("rule") != want_rule:
            problems.append(f"{o}->{d}: class_basis missing or rule != {want_rule!r} (EV1)")
        if (e.get("class_code") == "T") != ("as_of_timeline" in e):
            problems.append(f"{o}->{d}: class T <-> as_of_timeline biconditional broken (TL2)")
        want_ov = signals[o]["egress_override"]["value"] != "none"
        if want_ov != isinstance(e.get("origin_override"), dict):
            problems.append(f"{o}->{d}: origin_override presence != the Atlas rule (OO1)")

    raw = json.dumps(doc, ensure_ascii=False)
    if ("Corridor Atlas " + ATLAS_VERSION_OLD in raw) or ("from_atlas_" + ATLAS_VERSION_OLD in raw):
        problems.append("drifted Atlas version string present (N3)")
    if "CONFIRM" in raw:
        problems.append("unresolved CONFIRM marker present (m4)")
    if "draft VAS Act" in raw:
        problems.append("stale Taiwan 'draft VAS Act' prose present (F-TW)")
    if "one million transactions/day or EUR 200m/day" in raw:
        problems.append("MiCA Art. 58(3) threshold written as 'or' (F-EU)")
    if "tw-vas-act-enacted" in raw:
        problems.append("Taiwan contingent event still named 'tw-vas-act-enacted' (NF-4)")
    if "FSC (CBC consulted)" in raw or '"FSC (Taiwan)"' in raw:
        problems.append("Taiwan administrator understates CBC as consultee/omits it (F-TW-2)")
    if "US-held reserves; none granted to date." in raw:
        problems.append("inbound-US prose still asserts the \u00a718 gate is live-but-unused ('none granted "
                        "to date') \u2014 a market fact doing a proposition of law's job (E8)")
    return (not problems), problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Migrate the corridor artifact v0.9.92 -> v0.10.0.")
    ap.add_argument("--in", dest="src", help="input v0.9.92 artifact")
    ap.add_argument("--out", dest="dst", help="output the current-shape artifact")
    ap.add_argument("--check", dest="check", help="verify an artifact is already in current (v0.10.0) shape")
    args = ap.parse_args()

    if args.check:
        doc = json.loads(pathlib.Path(args.check).read_text(encoding="utf-8"))
        ok, problems = is_migrated(doc)
        if ok:
            print(f"[OK] {args.check} is in current (v0.10.0) shape: structured infra, bloc==partition, "
                  f"register_version + artifact_revision stamped, every class_code equals the published "
                  f"destination-first rule over data/signal_table.json, class_basis present, "
                  f"T<->timeline holds, origin_override matches the Atlas, no drift markers.")
            return 0
        print(f"[STALE] {args.check} is not fully migrated:")
        for p in problems:
            print("   -", p)
        return 1

    if not (args.src and args.dst):
        ap.error("provide --in and --out (or --check)")
    doc = json.loads(pathlib.Path(args.src).read_text(encoding="utf-8"))
    out = migrate(doc)
    ok, problems = is_migrated(out)
    if not ok:
        print("[ERROR] migration did not converge:", file=sys.stderr)
        for p in problems:
            print("   -", p, file=sys.stderr)
        return 2
    pathlib.Path(args.dst).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n",
                                      encoding="utf-8")
    from collections import Counter
    n_cross = sum(1 for e in out["edges"] if e["infrastructure_overlap"]["bloc"] == "cross-bloc")
    dist = dict(sorted(Counter(e["class_code"] for e in out["edges"]).items()))
    print(f"[wrote] {args.dst}")
    print(f"        register_version={out['register_version']}  artifact_revision={out['artifact_revision']}")
    print(f"        {len(out['edges'])} edges; class distribution {dist}")
    print(f"        {n_cross} cross-bloc edges; "
          f"{sum(1 for e in out['edges'] if 'as_of_timeline' in e)} timeline edges; "
          f"{sum(1 for e in out['edges'] if 'origin_override' in e)} origin-override edges")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
