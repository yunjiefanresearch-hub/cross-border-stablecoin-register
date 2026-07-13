#!/usr/bin/env python3
"""Build the ANALYSIS LAYER — the queryable encoding of the Cross-Border Stablecoin
Architecture v3 working paper's analytical payload.

Until v0.5.0 the register encoded the Compliance Matrix *node* layer at high fidelity
but left the Architecture paper's actual contribution — the composition-problem
apparatus — living only in PDF prose. This builder lifts four artifacts into
structured, schema-validated, machine-queryable JSON:

  analysis/interaction_sets.json      — the six constraint-interaction sets (§2.9, A–F)
  analysis/architectural_patterns.json — the PRC three-pattern typology (§3.3),
                                         the three-layer routing architecture (§4/§6),
                                         the §4.4 five-factor operational test,
                                         and the six design principles
  analysis/compatibility.json         — the §5.14 pairwise compatibility matrix
                                         (all 66 unordered jurisdiction pairs)
  analysis/open_questions.json        — the §7 open questions with conditional-status flags

build.py reads these (validating against analysis.schema.json) and folds them into
dataset.json under an `analysis` key, so a single fetch of dataset.json delivers both
the node layer and the analysis layer. The standalone files remain for direct access.

Source: Fan, Cross-Border Stablecoin Architecture v3 (Twelve Jurisdictions), June 2026.
Run:  python3 scripts/build_analysis.py
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis"
OUT.mkdir(exist_ok=True)
SRC = "Fan, Cross-Border Stablecoin Architecture v3 (Twelve Jurisdictions, June 2026)"
J12 = ["US", "EU", "UK", "SG", "HK", "CN", "BR", "CH", "AE", "TW", "JP", "KR"]

# ---------------------------------------------------------------------------
# 1. The six interaction sets (§2.9)
# ---------------------------------------------------------------------------
interaction_sets = {
    "schema": "cbsr-analysis/interaction_sets",
    "source": SRC + ", §2.9 (Constraint Interactions)",
    "note": ("The six interaction sets identify the constraint pairs through which joint "
             "binding generates composition problems. They are not exhaustive; they are the "
             "sets that generate the architectural composition problems analyzed in §3, §4, §6."),
    "sets": [
        {"id": "A", "name": "Issuer Eligibility x Cross-Border Payment and Data Sovereignty",
         "constraints": "C1xC6",
         "mechanism": ("Issuer eligibility depends in part on the entity's ability to comply with the "
                       "host jurisdiction's disclosure, reporting, and supervisory information-sharing "
                       "obligations. Where the entity's controlling person is subject to data-sovereignty "
                       "constraints in another jurisdiction that limit supervisory information-sharing with "
                       "the host supervisor, issuer eligibility may not be satisfiable even if the entity "
                       "formally meets the licensing criteria."),
         "worked_example": "The PRC-Hong Kong interaction analyzed in §3 (Pattern A constraint)."},
        {"id": "B", "name": "Yield Prohibition x Securities Classification",
         "constraints": "C3xC4",
         "mechanism": ("The yield prohibition operates against the issuer, its affiliates, and (under CLARITY "
                       "§404 as reported) its authorized agents; the securities-classification boundary operates "
                       "against the routing arrangement connecting the non-yielding stablecoin to a yield-bearing "
                       "instrument. Whether a routing arrangement falls within §404 turns on whether the routing "
                       "entity functions as an authorized agent paying yield in connection with the stablecoin "
                       "holding, or as a user-directed broker executing instructions to convert one asset into "
                       "another."),
         "worked_example": "The §4 yield-separation analysis (Reves four-factor; the three-layer routing architecture)."},
        {"id": "C", "name": "Bank/Non-Bank Status x Issuer Eligibility",
         "constraints": "C5xC1",
         "mechanism": ("Issuer eligibility in many jurisdictions depends on bank or non-bank status (GENIUS "
                       "creates separate bank/non-bank paths; MiCA separates credit institutions and EMIs). The "
                       "architectural choice between bank and non-bank configuration in each jurisdiction must be "
                       "made jointly across jurisdictions, because the cross-jurisdictional operation must compose "
                       "with the choices made in each."),
         "worked_example": "US x UK and US x Switzerland configuration choices in §5.14."},
        {"id": "D", "name": "Reserve Composition x Monetary Sovereignty",
         "constraints": "C2xC7",
         "mechanism": ("Reserves of a stablecoin denominated in a reference currency are typically held in that "
                       "currency at custodians supervised by that currency's monetary authority, so cross-border "
                       "circulation volume generates reserve-asset demand and potential monetary-policy effects in "
                       "the issuing jurisdiction. The Article 58(3) cap is the operative regulatory response; the "
                       "Bank of England systemic proposals address the analog."),
         "worked_example": "US x EU (Article 58(3) cap on USD-referenced EMT scale)."},
        {"id": "E", "name": "Securities Classification x Cross-Border Payment",
         "constraints": "C4xC6",
         "mechanism": ("A routing arrangement that converts a non-security payment stablecoin into a security "
                       "tokenized investment fund crosses the securities-classification boundary at the point of "
                       "routing. Where the arrangement spans multiple jurisdictions (e.g., a GENIUS stablecoin "
                       "routed to an EU UCITS fund), the cross-border payment instruction must satisfy the "
                       "disclosure and routing requirements of both jurisdictions' securities laws."),
         "worked_example": "Cross-border Layer 1 -> Layer 3 routing in §6 (US x JP, EU x JP edges)."},
        {"id": "F", "name": "Disclosure and Supervisory Coordination x All Other Constraints",
         "constraints": "C8xC1-7",
         "mechanism": ("A second-order constraint: satisfying it requires the operator to satisfy every other "
                       "constraint in a manner the relevant supervisors can verify through available disclosure and "
                       "reporting mechanisms. Where supervisory coordination is underdeveloped, the burden of "
                       "demonstrating compliance falls on the operator and may itself become binding on the "
                       "operational pattern available."),
         "worked_example": "Every Category III pair (the PRC-touching and pre-regime axes in §5.14)."},
    ],
}

# ---------------------------------------------------------------------------
# 2. Architectural patterns (§3.3 PRC typology; §4/§6 routing; §4.4 test; §6.1 principles)
# ---------------------------------------------------------------------------
architectural_patterns = {
    "schema": "cbsr-analysis/architectural_patterns",
    "source": SRC + ", §3.3, §4, §6",
    "prc_three_pattern_typology": {
        "source": SRC + ", §3.3 (Three Architectural Patterns)",
        "boundary": ("The cross-border PRC boundary is the practical consequence of the joint operation of "
                     "Constraints 1 (issuer eligibility) and 6 (cross-border payment and data sovereignty) "
                     "(Interaction Set A). As of Feb 2026 it is also anchored by an explicit written prohibition: "
                     "银发〔2026〕42号 (eight-ministry Notice, in force 6 Feb 2026; it repealed the 2021 Notice "
                     "银发〔2021〕237号) bars unauthorised overseas issuance of RMB-pegged stablecoins "
                     "(未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币) and PRC-controlled entities issuing virtual "
                     "currencies abroad, and restricts onshore RWA tokenisation (with CSRC 公告〔2026〕1号 guidance on "
                     "offshore ABS-token issuance). What remains emergent (rather than categorically prohibited) is the "
                     "Direct-Subsidiary-via-Hong-Kong pathway: the public record (absence of PRC-connected entities from "
                     "the April 2026 HKMA first cohort; the Oct 2025 Ant/JD application withdrawals; the absence of "
                     "state-owned bank affiliates despite Sep 2025 activity; the Oct 2025 CSRC tokenization guidance) "
                     "shows it constrained by the data-sharing pattern, not by a categorical exclusion under the "
                     "Stablecoins Ordinance."),
        "patterns": [
            {"id": "A", "name": "Direct Subsidiary Licensing", "status": "currently_constrained",
             "description": ("A PRC-connected group seeks FRS issuance through a wholly-owned Hong Kong subsidiary "
                             "licensed under the Stablecoins Ordinance. Architecturally simplest and commercially "
                             "most efficient (preserves equity control), and formally available (the Ordinance does "
                             "not categorically exclude PRC-connected applicants)."),
             "binding_constraint": ("Interaction Set A: PRC cross-border data law (PIPL, DSL, the March 2024 CAC "
                                     "Cross-Border Provisions) limits the subsidiary's ability to share supervisory "
                                     "data with the HKMA and offshore counterparties as the supervisor expects."),
             "viability_conditions": ["PRC modifies the cross-border data framework to permit supervisor-to-supervisor "
                                       "information-sharing with the HKMA on acceptable terms, OR",
                                       "the HKMA modifies its posture toward PRC-connected applicants."]},
            {"id": "B", "name": "Partnership Distribution", "status": "operationally_implemented",
             "description": ("The PRC-connected group does not seek direct issuance; it partners with an already-"
                             "licensed third-party issuer as a distribution partner. The group holds no reserves and "
                             "has none of the issuer's disclosure/reporting obligations; it provides distribution "
                             "access through existing commercial relationships and payment infrastructure."),
             "public_anchor": ("The July 2025 Ant International announcement of a Circle USDC integration into Ant "
                               "International's cross-border payment infrastructure; deployment in any jurisdiction is "
                               "contingent on Circle's regulatory standing there."),
             "limitation": ("Does not give the group equity-based participation in issuance economics: the reserve "
                            "yield accrues to the partner issuer, not the group. Adequate where the commercial interest "
                            "is payment-infrastructure value; unsatisfactory where it is reserve-yield capture.")},
            {"id": "C", "name": "Separated-Entity Architecture", "status": "constraint_derived_analytical_option",
             "description": ("An analytical option suggested by the constraint framework but not confirmed by any "
                             "public deployed example. Asks whether the four PRC-side constraints admit any "
                             "configuration in which a licensable front-office entity is operationally connected to a "
                             "PRC-side counterparty without yielding consolidation, control attribution, or excess "
                             "cross-border data/capital flows. Specified at the level of the constraints, not any "
                             "particular configuration."),
             "four_prc_constraints": [
                 "Accounting consolidation under the Accounting Standards for Business Enterprises (control = multi-factor).",
                 "Related-party transaction disclosure under CSRC rules (material transactions).",
                 "Outbound capital movement approval/registration under the SAFE framework (above thresholds).",
                 "Data flows under PIPL, DSL, and the March 2024 CAC Cross-Border Provisions."],
             "viability_conditions": ["HKMA posture toward formally-compliant-but-operationally-connected applicants (unknown);",
                                       "PRC posture toward outbound service/technology-cooperation arrangements (unknown);",
                                       "commercial viability vs Pattern B given greater operational complexity (uncertain)."]},
        ],
        "selection_logic": ("Pattern B is adequate and currently implementable where the objective is payment-"
                            "infrastructure integration without equity participation. Pattern C is the analytical "
                            "option where the objective is reserve-yield capture and the operator accepts regulatory "
                            "uncertainty. Pattern A becomes viable only if the boundary changes. Hybrid/per-jurisdiction "
                            "selection is possible (e.g., Pattern B for the EU via a MiCA partner, Pattern A for the UK "
                            "via direct SI 2026/102 authorization)."),
    },
    "three_layer_routing_architecture": {
        "source": SRC + ", §4, §6 (Routing Architecture Design)",
        "summary": ("A portable architecture separating yield-bearing tokenized cash management from payment-"
                    "stablecoin functionality, anchored in the SEC's 24 Feb 2026 §6(c) relief for the WisdomTree "
                    "Treasury MMF Digital Fund (WTGXX) and the Ant International-Circle example."),
        "layers": [
            {"layer": 1, "name": "Compliant payment stablecoin",
             "description": "A non-yield-bearing payment stablecoin compliant with the local stablecoin regime (GENIUS / MiCA EMT / SI 2026/102 / MAS-SCS / HK Stablecoins Ordinance)."},
            {"layer": 2, "name": "User-authorized routing",
             "description": "A routing function providing user-directed conversion between Layers 1 and 3, with audit-trail capability. Its regulatory status is broker-dealer (or broker-dealer-plus-authorized-agent)."},
            {"layer": 3, "name": "Yield-bearing tokenized cash management",
             "description": "Shares of a registered investment company (or non-US equivalent: UCITS / AIF) whose portfolio generates yield; a distinct ownership position held by the user."},
        ],
        "routing_layer_functions": [
            "Provide the user interface for the conversion election (affirmative election per conversion; disclose distinct ownership).",
            "Execute the conversion at the user's elected timing (transmit instruction to counterparties; settle).",
            "Record each conversion in the audit trail.",
            "Execute the reverse conversion (redeem Layer 3 shares; acquire Layer 1 balances).",
            "Distribute the Layer 3 yield to the user as a Layer 3 holder (not in connection with the Layer 1 balance).",
            "Report tax and regulatory information to the user, tax authorities, and supervisors.",
        ],
        "operational_test_section_4_4": {
            "purpose": ("The five factors that determine whether a routing arrangement falls on the permitted side "
                        "of the §404 boundary (the boundary is functional: it depends on the operational facts)."),
            "factors": [
                {"factor": 1, "name": "Direction of the Conversion",
                 "test": "User-directed, not issuer- or intermediary-directed; affirmative election per conversion, capable of being withheld; no intermediary discretion. Automated sweeps without per-conversion election fail."},
                {"factor": 2, "name": "Disclosure of the Distinct Ownership Position",
                 "test": "The intermediary must disclose, and the user must understand, that the investment-company shares are a distinct ownership position (a security) from the stablecoin balance (not a security). Failure if the user is unaware conversion occurred."},
                {"factor": 3, "name": "Timing Independence",
                 "test": "Timing determined by the user, not the intermediary's algorithm or the issuer's instruction; the user can defer indefinitely and withdraw. Conversion triggered by non-overridable automated rules fails."},
                {"factor": 4, "name": "Yield Attribution",
                 "test": "Yield attributed to the user as a Layer 3 holder and paid by the investment company / its transfer agent; not paid by the stablecoin issuer, an affiliate, or an intermediary acting as the issuer's authorized agent. Accounting/operational separation must be clear."},
                {"factor": 5, "name": "Audit Trail",
                 "test": "Each conversion records the user's election, time, amount, price, parties, and resulting positions; available to the user, supervisors, and (on dispute) counsel. The audit trail is the evidentiary mechanism for the functional boundary."},
            ],
        },
        "design_principles": [
            {"principle": 1, "name": "Separation of payment and yield functions at the protocol level",
             "derivation": "C3 (yield prohibition) x C4 (securities classification)",
             "statement": "The separation between Layer 1 (non-yielding) and Layer 3 (yield-bearing security) must be substantive, not nominal: distinct legal instruments, authorization, accounting, and disclosure."},
            {"principle": 2, "name": "User-directed routing between layers",
             "derivation": "§4.4 Factor 1 (direction) + Factor 3 (timing)",
             "statement": "The Layer 1 <-> Layer 3 connection must be user-initiated and user-controlled, distinguishing the pattern from issuer-side yield arrangements within the §404 prohibition."},
            {"principle": 3, "name": "Audit trail integrity",
             "derivation": "C8 (disclosure/coordination) + §4.4 Factor 5",
             "statement": "Each routing event generates a verifiable record (election, time, amount, price, parties, positions) — the evidentiary mechanism establishing the user-directed character to supervisors and courts."},
            {"principle": 4, "name": "Per-jurisdiction authorization of each layer",
             "derivation": "C1 (issuer eligibility) + C5 (bank/non-bank) operating cross-jurisdictionally",
             "statement": "Each layer must be authorized in each operating jurisdiction under the applicable regime (Layer 1 stablecoin regime; Layer 3 funds regime; Layer 2 securities/intermediary regime). The pattern is one; the authorizations are multiple."},
            {"principle": 5, "name": "Cross-jurisdictional portability of the pattern",
             "derivation": "§4.6 cross-jurisdictional compatibility analysis",
             "statement": "The design principles apply analogously in each receiving jurisdiction; only the specific authorizations differ. The architectural pattern is not intrinsically US-specific."},
            {"principle": 6, "name": "Configurability against open regulatory developments",
             "derivation": "§7 open questions",
             "statement": "Architectural elements should be configurable so the operator can respond to the §7.1-§7.4 developments without fundamental redesign."},
        ],
    },
}

# ---------------------------------------------------------------------------
# 3. The §5.14 pairwise compatibility matrix (all 66 unordered pairs)
# ---------------------------------------------------------------------------
# category: "I" | "I/II" | "III"   ;  axis (for III): prohibition | pre_regime | prohibition+pre_regime
# Each entry: (category, [interaction sets], iii_axis or None, short binding note)
PAIRS = {
    "US-EU": ("I/II", ["B", "D"], None, "Issuer eligibility non-coextensive; Article 58(3) cap forces volume limit, EUR sister EMT, or non-MoE routing; §18 comparability is asymmetric (no MiCA reciprocal)."),
    "UK-US": ("I", ["B", "C"], None, "Non-coextensive but bridgeable via dual authorization/partnership; BoE systemic framework parallel; HMT 21 Apr 2026 draft amendment SI addresses FCA/BoE interactions."),
    "SG-US": ("I/II", ["A", "E"], None, "Separate authorization paths; the MAS June 2025 DTSP statement constrains offshore operations targeting Singapore residents."),
    "HK-US": ("I/II", ["A", "C"], None, "HKMA first cohort is HKD-referenced; USD-referenced HK operations need a later licence or partnership with a HK-licensed issuer."),
    "CN-US": ("III", ["A", "F"], "prohibition", "PRC prohibits issuance; §3 patterns apply (Pattern B / constrained A / analytical C); GENIUS applies on the US side, PRC data/capital frameworks on PRC-touching elements."),
    "BR-US": ("I/II", ["A", "D"], None, "GENIUS issuer is not a Brazilian PSAV; Brazil reclassifies the payment leg as câmbio with a per-operation cap binding against non-FX-authorised counterparties; Res 561 closes the retail eFX rail from 1 Oct 2026."),
    "CH-US": ("I/II", ["B", "C"], None, "GENIUS issuer not authorised under the Swiss Banking Act; Swiss leg needs separate authorization, partnership, or a bank-guarantee structure; FINMA holder-identification constrains composability; no CH usage cap."),
    "AE-US": ("I/II", ["A", "C"], None, "GENIUS issuer is not a CBUAE Dirham Payment Token issuer; a USD Foreign Payment Token may be used onshore only to buy a virtual asset/derivative, not for goods/services (channel restriction)."),
    "TW-US": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): the issuer regime is enacted but not operative and there is no exportable token yet, so neither dual authorization nor partnership is available on the TW side and the pair is Category III via origin-drag; only AML registration operative. Distinct from PRC prohibition (not prohibited) and from Korea's pre-regime status (Taiwan has enacted law); inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "JP-US": ("I/II", ["A", "C", "E", "F"], None, "Japan inbound is a channel-determination (EPIESP registration, reserves in Japan, foreign-issuer non-solicitation), so the JP leg requires recognition and registration rather than mutual recognition."),
    "KR-US": ("III", ["A", "C", "D", "F"], "pre_regime", "South Korea pre-regime (DABA un-enacted; won-issuance effectively prohibited); no issuance authorization on the KR side; GENIUS applies on the US side."),
    "EU-UK": ("I", ["C", "D"], None, "Post-Brexit, MiCA and FCA authorizations are non-mutual; dual authorization/partnership required; Article 58(3) cap and the BoE systemic framework address monetary sovereignty through distinct mechanisms."),
    "EU-SG": ("I/II", ["A", "D"], None, "Dual authorization/partnership; MAS DTSP statement and the Article 58(3) cap constrain different sides of the pair."),
    "EU-HK": ("I/II", ["A", "D"], None, "Reference-currency asymmetry: a HKD HKMA-licensed token faces Article 58(3) if marketed to EU residents at scale; a EUR MiCA EMT is not eligible under the current HK cohort posture without a HK licence."),
    "CN-EU": ("III", ["A", "D", "F"], "prohibition", "Same as US x PRC for pattern selection (§3); Article 58(3) applies to any token circulating in the EU through PRC-connected architecture; PIPL/DSL/CAC apply to data flows."),
    "BR-EU": ("I/II", ["A", "D"], None, "A MiCA EMI is not a Brazilian PSAV; câmbio reclassification + per-operation cap on the Brazil leg; a USD EMT additionally faces Article 58(3) in the EU. Two monetary-sovereignty mechanisms on opposite legs."),
    "CH-EU": ("I/II", ["C", "D"], None, "Despite EU-Switzerland data adequacy, MiCA and Swiss authorizations are non-mutual; Article 58(3) cap on the EU leg vs full holder identification on the Swiss leg."),
    "AE-EU": ("I/II", ["A", "D"], None, "Article 58(3) cap in the EU and the Foreign Payment Token channel restriction onshore in the UAE; a EUR MiCA EMT is not acceptable for onshore UAE goods/services payment without separate authorization."),
    "EU-TW": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; MiCA (incl. Article 58(3)) on the EU leg; only AML registration operative on the TW side. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "EU-JP": ("I/II", ["A", "C", "D", "E", "F"], None, "Japan channel-determination inbound; MiCA + Article 58(3) on the EU leg, the PSA EPI regime on the JP leg."),
    "EU-KR": ("III", ["A", "D", "E", "F"], "pre_regime", "South Korea pre-regime; MiCA + Article 58(3) on the EU leg; no issuance authorization on the KR side."),
    "SG-UK": ("I/II", ["A", "C"], None, "FCA and MAS authorizations non-mutual; BoE systemic framework and MAS-SCS on parallel tracks; HMT 21 Apr 2026 draft amendment SI's APAC interaction not yet operationally elaborated."),
    "HK-UK": ("I/II", ["A", "C"], None, "FCA authorization does not confer HKMA authorization; dual authorization/partnership required."),
    "CN-UK": ("III", ["A", "D", "F"], "prohibition", "Same pattern as US x PRC and EU x PRC."),
    "BR-UK": ("I/II", ["A", "D"], None, "FCA authorization does not confer PSAV status; BoE systemic framework on the UK side if systemic; câmbio reclassification + per-operation cap on the Brazil cross-border leg."),
    "CH-UK": ("I/II", ["C", "F"], None, "FCA and Swiss authorizations non-mutual; UK systemic framework and the Swiss bank-guarantee / forthcoming payment-instrument-institution regime on parallel tracks; Swiss holder-identification constrains composability."),
    "AE-UK": ("I/II", ["A", "C"], None, "FCA does not confer CBUAE/free-zone authorization; UAE Foreign Payment Token channel restriction is the onshore inbound asymmetry; DIFC/ADGM provide recognition/licensing outside the onshore perimeter."),
    "TW-UK": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; FCA and BoE frameworks on the UK leg; only AML registration operative on the TW side. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement. (Both are regime-in-transition, but the UK exports an authorizable token and Taiwan does not yet.)"),
    "JP-UK": ("I/II", ["A", "C", "E", "F"], None, "Japan channel-determination inbound; FSMA 2026 conduct + systemic regimes (operative 2027) on the UK leg, the PSA EPI regime on the JP leg."),
    "KR-UK": ("III", ["C", "D", "F"], "pre_regime", "South Korea pre-regime; FSMA 2026 conduct + systemic regimes (operative 2027) on the UK leg; no issuance authorization on the KR side."),
    "HK-SG": ("I/II", ["A", "F"], None, "Dual authorization/partnership; Project Ensemble (HKMA-led) provides an institutional interoperability channel, though it is not part of the stablecoin licensing regime."),
    "CN-SG": ("III", ["A", "F"], "prohibition", "§3 patterns on the PRC side; MAS DTSP framework on the Singapore side; PIPL/DSL/CAC on data flows."),
    "BR-SG": ("I/II", ["A", "D"], None, "An MAS-SCS issuer is not a Brazilian PSAV; MAS DTSP statement constrains offshore Singapore-resident-targeting operations; câmbio reclassification + per-operation cap on the Brazil leg."),
    "CH-SG": ("I/II", ["C", "F"], None, "MAS and Swiss authorizations non-mutual; both permit major-reference-currency stablecoins without a usage cap; the binding constraints are the Swiss holder-identification requirement and the MAS DTSP perimeter."),
    "AE-SG": ("I/II", ["A", "C"], None, "MAS and CBUAE/free-zone authorizations non-mutual; UAE channel restriction applies onshore; both host significant tokenization and free-zone/sandbox activity, providing partnership pathways."),
    "SG-TW": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; MAS-SCS + DTSP perimeter on the Singapore leg; only AML registration operative on the TW side. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "JP-SG": ("I/II", ["A", "C", "E", "F"], None, "Japan channel-determination inbound; MAS single-currency framework + DTSP perimeter on the Singapore leg, the PSA EPI regime on the JP leg."),
    "KR-SG": ("III", ["D", "F"], "pre_regime", "South Korea pre-regime; MAS single-currency framework + DTSP perimeter on the Singapore leg; no issuance authorization on the KR side."),
    "CN-HK": ("III", ["A", "F"], "prohibition", "The most analytically loaded pair (highest stakes): geographic proximity and commercial integration create the strongest demand while the PRC data/capital frameworks plus the HKMA first-cohort posture create the most restrictive constraint set. §3 patterns are the operative options."),
    "BR-HK": ("I/II", ["A", "D"], None, "An HKMA FRS licensee is not a Brazilian PSAV; the HKMA first cohort is HKD-referenced; a HKD token entering Brazil as payment crosses the câmbio reclassification and per-operation cap."),
    "CH-HK": ("I/II", ["C", "F"], None, "HKMA and Swiss authorizations non-mutual; the HKD-only first-cohort posture and the Swiss holder-identification requirement are operative; neither imposes a MiCA-style aggregate cap."),
    "AE-HK": ("I/II", ["A", "F"], None, "HKMA and CBUAE/free-zone authorizations non-mutual; both participate in distinct wholesale-settlement initiatives (HK's Project Ensemble; the UAE's mBridge participation); HKD/AED issuance under domestic central-bank perimeters."),
    "HK-TW": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; HKMA FRS regime on the Hong Kong leg; only AML registration operative on the TW side; an additional cross-strait political dimension the public record does not resolve. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "HK-JP": ("I/II", ["A", "C", "E", "F"], None, "Japan channel-determination inbound; Stablecoins Ordinance + HKD-only first cohort on the Hong Kong leg, the PSA EPI regime on the JP leg."),
    "HK-KR": ("III", ["A", "D", "F"], "pre_regime", "South Korea pre-regime; Stablecoins Ordinance + HKD-only first cohort on the Hong Kong leg; no issuance authorization on the KR side."),
    "BR-CN": ("III", ["A", "F"], "prohibition", "PRC prohibition axis (§3 patterns on the PRC side); licensed-PSAV regime + câmbio reclassification on the Brazil side; PRC data/capital frameworks on PRC-touching elements."),
    "CH-CN": ("III", ["A", "F"], "prohibition", "PRC prohibition axis; the Swiss regime on the Swiss leg; PIPL/DSL/CAC on data flows."),
    "AE-CN": ("III", ["A", "F"], "prohibition", "PRC prohibition axis; UAE PTSR + free-zone regimes on the UAE leg; CBUAE and Hong Kong both participate in the mBridge platform, a wholesale-settlement channel distinct from private stablecoin issuance."),
    "CN-TW": ("III", ["A", "F"], "prohibition+enacted_not_commenced", "Combines PRC prohibition with Taiwan's enacted-but-not-commenced status (VAS Act third reading 30 Jun 2026, awaiting subsidiary legislation): no direct issuance architecture on either side, and the cross-strait political relationship further removes this pair from the resolvable set. Category III on both axes, but for different reasons: PRC prohibits issuance, while Taiwan has enacted law not yet operative and no exportable token yet."),
    "CN-JP": ("III", ["A", "C", "E", "F"], "prohibition", "PRC prohibits issuance and does not permit a foreign stablecoin to circulate as a payment instrument; the PSA EPI regime applies on the JP leg. Prohibition Category III, distinct from pre-regime."),
    "CN-KR": ("III", ["D", "F"], "prohibition", "PRC prohibition axis; only the VAUPA is operative on the South Korea leg. Prohibition Category III, distinct from pre-regime."),
    "BR-CH": ("I/II", ["C", "D"], None, "Brazilian PSAV and Swiss authorizations non-mutual; câmbio reclassification on the Brazil leg, holder-identification on the Swiss leg; neither imposes a MiCA-style aggregate cap."),
    "AE-BR": ("I/II", ["A", "D"], None, "Non-mutual authorizations; câmbio reclassification + per-operation cap on the Brazil leg, the UAE Foreign Payment Token channel restriction onshore; both are channel/counterparty monetary-sovereignty mechanisms, not aggregate caps."),
    "BR-TW": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; Brazilian licensed-PSAV regime + câmbio reclassification on the Brazil leg; only AML registration operative on the TW side. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "BR-JP": ("I/II", ["A", "C", "D", "E", "F"], None, "Japan channel-determination inbound; the BCB câmbio channel (licensed VASP) on the Brazil leg, the PSA EPI regime on the JP leg."),
    "BR-KR": ("III", ["D", "F"], "pre_regime", "South Korea pre-regime; the BCB câmbio channel (licensed VASP) on the Brazil leg; no issuance authorization on the KR side."),
    "AE-CH": ("I/II", ["C", "F"], None, "Swiss and CBUAE/free-zone authorizations non-mutual; the Swiss holder-identification requirement and the UAE usage-channel restriction are operative; neither imposes an aggregate usage cap."),
    "CH-TW": ("III", ["C", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; the Swiss regime on the Swiss leg; only AML registration operative on the TW side. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "CH-JP": ("I/II", ["A", "C", "E", "F"], None, "Japan channel-determination inbound; the Swiss banking/FinTech licence regime on the Switzerland leg, the PSA EPI regime on the JP leg."),
    "CH-KR": ("III", ["D", "F"], "pre_regime", "South Korea pre-regime; the Swiss banking/FinTech licence regime on the Switzerland leg; no issuance authorization on the KR side."),
    "AE-TW": ("III", ["A", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; UAE PTSR + free-zone regimes on the UAE leg; only AML registration operative on the TW side. Inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "AE-JP": ("I/II", ["A", "C", "D", "E", "F"], None, "Japan channel-determination inbound; CBUAE PTSR + free-zone regimes on the UAE leg, the PSA EPI regime on the JP leg."),
    "AE-KR": ("III", ["A", "D", "F"], "pre_regime", "South Korea pre-regime; CBUAE PTSR + free-zone regimes on the UAE leg; no issuance authorization on the KR side."),
    "JP-TW": ("III", ["A", "C", "E", "F"], "enacted_not_commenced", "Taiwan enacted-but-not-commenced (VAS Act third reading 30 Jun 2026; awaiting FSC subsidiary legislation, no gazetted commencement): no exportable token yet, so the TW leg drags the pair to Category III; the PSA EPI regime on the JP leg. Category III via origin-drag, distinct from the mainland prohibition; inbound-to-Taiwan edges are held at Category T and resolve to a channelled Category II on commencement."),
    "KR-TW": ("III", ["D", "F"], "pre_regime+enacted_not_commenced", "Korea is pre-regime (DABA un-enacted) and Taiwan is enacted-but-not-commenced (VAS Act third reading 30 Jun 2026, awaiting subsidiary legislation): neither leg has an exportable token, so the pair is Category III on both sides, but for different reasons: Korea has no comprehensive regime yet, while Taiwan has enacted law not yet operative. Only the VAUPA on the KR leg and only AML registration on the TW leg."),
    "JP-KR": ("III", ["A", "C", "D", "E", "F"], "pre_regime", "South Korea pre-regime; the PSA EPI regime on the JP leg; no issuance authorization on the KR side."),
}


def _norm_pair(key):
    a, b = key.split("-")
    return "-".join(sorted([a, b]))


compat_pairs = []
for key, (cat, sets, axis, note) in PAIRS.items():
    a, b = sorted(key.split("-"))
    entry = {"pair": f"{a}-{b}", "jurisdictions": [a, b], "category": cat,
             "interaction_sets": sets, "note": note}
    if axis:
        entry["category_iii_axis"] = axis
    compat_pairs.append(entry)
compat_pairs.sort(key=lambda e: e["pair"])

compatibility = {
    "schema": "cbsr-analysis/compatibility",
    "source": SRC + ", §5.14 (Pairwise Compatibility Analysis)",
    "jurisdictions": J12,
    "pair_count": len(compat_pairs),
    "categories": {
        "I": "Dual authorization compatible — operable under a single pattern with separate legal entities holding local authorizations under common control; the §6 routing architecture is portable across the pair.",
        "I/II": "Category I/II hybrid — not operable under dual direct authorization with the operator as issuer in both jurisdictions, but operable through partnership with a locally-authorized issuer in one jurisdiction (Category II), or via dual authorization through separate entities (Category I).",
        "II": "Partnership distribution required — operable only through a partnership arrangement with a locally-authorized issuer.",
        "III": "Composition problem unresolved — the constraints interact in ways the public regulatory record does not currently resolve; configurations may be analytically derivable but their viability depends on regulatory developments not yet completed.",
    },
    "category_iii_axes": {
        "prohibition": "The PRC prohibition axis: issuance is prohibited (now by explicit written law, 银发〔2026〕42号, in force 6 Feb 2026, which repealed the 2021 Notice and bars overseas RMB-pegged-stablecoin issuance and extraterritorial issuance by PRC-controlled entities); the §3.3 three-pattern typology supplies the responsive architectures.",
        "pre_regime": "The South Korea pre-regime axis: issuance is not prohibited but not yet authorizable (the Digital Asset Basic Act remains a bill); partnership and dual-authorization options become available only on enactment. Taiwan left this axis on 30 Jun 2026 when the VAS Act was enacted, moving to the enacted_not_commenced axis.",
        "counterparty_conditional": "The Brazil cross-border leg: the câmbio reclassification and the 1 Oct 2026 closure of the retail eFX rail leave the permitted channel running through a licensed VASP with an FX-authorised counterparty or within the per-operation cap.",
        "enacted_not_commenced": "The Taiwan enacted-but-not-commenced axis: the Virtual Asset Service Act passed third reading on 30 Jun 2026 but awaits FSC subsidiary legislation with no gazetted commencement, so no exportable token exists yet. Origin edges drag to Category III; inbound edges are held at Category T and resolve to a channelled Category II on commencement. Distinct from pre-regime (no regime at all) and from prohibition.",
        "prohibition+enacted_not_commenced": "PRC prohibition combined with Taiwan's enacted-but-not-commenced status: Category III on both legs for different reasons, plus a cross-strait political dimension.",
        "pre_regime+enacted_not_commenced": "Korea pre-regime combined with Taiwan enacted-but-not-commenced: neither leg has an exportable token, so Category III on both sides, for different reasons.",
    },
    "summary_observation": ("No surveyed pair exhibits unilateral authorization recognition permitting a single entity "
                            "to operate as issuer in both jurisdictions under one authorization; Category I (dual "
                            "authorization) and Category II (partnership distribution) are the standard configurations. "
                            "Category III arises along several axes (PRC prohibition; Korea pre-regime; Taiwan "
                            "enacted-but-not-commenced; the "
                            "counterparty-conditional Brazil leg). As of June 2026 there is no cross-border stablecoin "
                            "operation in production crossing any Category III pair through direct subsidiary "
                            "architecture; production solutions are Category II partnership arrangements (Ant "
                            "International + Circle as anchor) or are limited to non-Category-III pairs."),
    "pairs": compat_pairs,
}

# ---------------------------------------------------------------------------
# 4. Open questions (§7) with conditional-status flags
# ---------------------------------------------------------------------------
open_questions = {
    "schema": "cbsr-analysis/open_questions",
    "source": SRC + ", §7 (Implementation and Open Questions)",
    "note": "Sections 7.1-7.4 are the four developments the paper identifies as determining which architectural options become operationally viable; 7.5 is the wholesale-settlement infrastructure-implications question. Each is preserved with its conditional regulatory status.  v0.9.9: each open question now carries a trigger_kind aligning it with the flagship §3 typology (7.3 parameterization §3.7; 7.4 open-compositional §3.8; 7.2 resolved-tightening §3.9; 7.1 and 7.5 open-compositional). These are the non-horizon-moving trigger kinds, carried here rather than in the event calendar because none has a commencement to apply by date.",
    "questions": [
        {"id": "7.1", "title": "Joint NPRM architecture (§404 implementation)",
         "question": "What will the joint Notice of Proposed Rulemaking that CLARITY §404 (as reported) directs the SEC, CFTC, and Treasury to issue within twelve months of enactment actually contain?",
         "affects": "The §4 yield-separation architecture and the permitted/prohibited boundary for routing arrangements.",
         "status": "unresolved", "conditional_flag": "Depends on enactment of CLARITY substantially as reported and on the joint NPRM's actual content (not yet issued).",
         "trigger_kind": "open-compositional",
         "trigger_kind_basis": "§3.8-adjacent: the joint NPRM is information/rulemaking whose resolution feeds the routing and market-structure architecture; contingent on CLARITY enactment, no commencement to apply by date."},
        {"id": "7.2", "title": "People's Republic of China boundary stability",
         "question": "The PRC boundary tightened in writing in Feb 2026 (银发〔2026〕42号). Will it hold at that level, tighten further, or relax?",
         "affects": "The §3.3 three-pattern typology (especially Pattern A viability).",
         "status": "unresolved",
         "material_developments": ["RESOLVED (tightening): 银发〔2026〕42号 (in force 6 Feb 2026) put the prohibition into explicit written law — overseas RMB-pegged-stablecoin issuance banned, extraterritorial issuance by PRC-controlled entities banned, onshore RWA tokenisation restricted (CSRC 公告〔2026〕1号);",
                                    "STILL-OPEN (relaxation paths): PRC modifies the cross-border data framework to facilitate HKMA supervisor-to-supervisor information-sharing;",
                                    "the HKMA announces a second cohort including one or more PRC-connected entities;",
                                    "the PRC publicly authorizes state-owned bank HK affiliates to apply/operate under HK licences."],
         "conditional_flag": "The tightening has occurred (42号). None of the three relaxation developments has occurred as of publication; the §3.3 patterns are configured against the boundary as currently observed.",
         "trigger_kind": "resolved-tightening",
         "trigger_kind_basis": "§3.9: the PRC boundary's Feb-2026 written tightening (银发〔2026〕42号) is settled in the tightening direction while a reversing relaxation stays open."},
        {"id": "7.3", "title": "Operationalization of the Article 58(3) cap",
         "question": "How will the EBA operationalize the Article 58(3) means-of-exchange cap (adopted methodology guidance and Member State competent-authority practice)?",
         "affects": "The §5.14 cross-currency cross-border analysis for USD-referenced stablecoins in the EU.",
         "status": "unresolved", "conditional_flag": "The EBA has not finalized the relevant methodology guidance; thresholds are one million daily transactions or EUR 200m daily value (quarterly average, means-of-exchange use).",
         "trigger_kind": "parameterization",
         "trigger_kind_basis": "§3.7: operationalization of the Article 58(3) means-of-exchange cap — sharpens the operative content of a constraint already in force without moving any class."},
        {"id": "7.4", "title": "HKMA second-cohort composition",
         "question": "What will the composition of the second cohort of HKMA stablecoin licences be (currency coverage; PRC-connected applicants; USD-referenced products)?",
         "affects": "US x HK and EU x HK pair feasibility; PRC boundary stability (§7.2).",
         "status": "unresolved", "conditional_flag": "The HKMA has not announced the second cohort.",
         "trigger_kind": "open-compositional",
         "trigger_kind_basis": "§3.8: the HKMA second-cohort composition is information, not a change in law; its resolution feeds the PRC boundary-stability question (7.2)."},
        {"id": "7.5", "title": "Project Agorá (BIS-led) and Project Ensemble (HKMA-led) implications",
         "question": "How will the wholesale-settlement experiments (Project Agorá, Project Ensemble, mBridge) interact with private stablecoin architectures at the infrastructure layer?",
         "affects": "The Digital-Financial corridor archetype and infrastructure-axis membership across edges.",
         "status": "unresolved", "conditional_flag": "Infrastructure implications are forward-looking; the Corridor Atlas develops the infrastructure layer.",
         "trigger_kind": "open-compositional",
         "trigger_kind_basis": "§5: the wholesale-settlement experiments are an open compositional/infrastructure question feeding the geopolitical-fracture reading; softer evidence tier, not a class-level trigger."},
    ],
}

# ---------------------------------------------------------------------------
# Write the four artifacts
# ---------------------------------------------------------------------------
ARTIFACTS = {
    "interaction_sets.json": interaction_sets,
    "architectural_patterns.json": architectural_patterns,
    "compatibility.json": compatibility,
    "open_questions.json": open_questions,
}
if __name__ == "__main__":
    for name, obj in ARTIFACTS.items():
        (OUT / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    # sanity: all 66 pairs present and well-formed
    assert compatibility["pair_count"] == 66, compatibility["pair_count"]
    seen = {p["pair"] for p in compat_pairs}
    expected = {"-".join(sorted([a, b])) for i, a in enumerate(J12) for b in J12[i + 1:]}
    missing = expected - seen
    assert not missing, f"missing pairs: {sorted(missing)}"
    extra = seen - expected
    assert not extra, f"unexpected pairs: {sorted(extra)}"
    print(f"wrote analysis layer: {len(ARTIFACTS)} files")
    print(f"  interaction_sets: {len(interaction_sets['sets'])}")
    print(f"  architectural_patterns: PRC typology ({len(architectural_patterns['prc_three_pattern_typology']['patterns'])}) + 3-layer routing + 5-factor test + {len(architectural_patterns['three_layer_routing_architecture']['design_principles'])} principles")
    print(f"  compatibility: {compatibility['pair_count']} pairs (all C(12,2) present)")
    print(f"  open_questions: {len(open_questions['questions'])}")
    from collections import Counter
    print("  category distribution:", dict(Counter(p["category"] for p in compat_pairs)))
