#!/usr/bin/env python3
"""Expand the corridor layer from the single worked example (hk-br) toward the
directed-edge model of the Cross-Border Digital-Finance Corridor Atlas v0.2.3.

The Atlas treats the corridor — a directed origin->destination edge — as the unit of
analysis (132 directed edges across the twelve jurisdictions). Until v0.5.0 the register
encoded only one corridor, so "corridor layer" was a single example rather than a layer.
This builder transcribes the highest-demand / most structurally-illustrative directed
edges from the Atlas §5 deep-dives, each carrying the Atlas attributes:

  feasibility_class · compatibility_category (link to Architecture §5.14) · currencies ·
  archetypes (RC/SC/TC/DC) · operative interaction sets (A-F) · infrastructure overlap ·
  inbound mechanism + administrator · origin-override flag · note.

build.py passes any YAML with a `corridor_id` through into dataset.json["corridors"].
The deeply-verified hk-br-usd-stablecoin-settlement corridor is kept as the anchor and is
NOT regenerated here. Directional pairs are kept distinct (US->EU and EU->US are two
edges) because the inbound gate differs by direction — the Atlas's core thesis.

Source: Fan, Cross-Border Digital-Finance Corridor Atlas v0.2.3 (June 2026), §5;
        Cross-Border Stablecoin Architecture v3 (Twelve Jurisdictions), §5.14.
Run:  python3 scripts/build_corridors.py
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
ATLAS = "Fan, Cross-Border Digital-Finance Corridor Atlas v0.2.3 (June 2026)"
ARCH = "Fan, Cross-Border Stablecoin Architecture v3 (Twelve Jurisdictions, June 2026)"
ARCHETYPES = {"RC": "Regulatory Corridor", "SC": "Stablecoin Settlement Corridor",
              "TC": "Tokenized-Asset Corridor", "DC": "Digital-Financial Corridor"}

KEY_ORDER = ["corridor_id", "name", "schema", "origin", "destination", "direction",
             "currencies", "feasibility_class", "compatibility_category", "compatibility_pair",
             "divergence", "archetypes", "interaction_sets", "infrastructure_overlap", "inbound_mechanism",
             "origin_override", "note", "source", "valid_as_of", "evidence_tier", "version_added", "tags"]


def corr(**k):
    return {key: k[key] for key in KEY_ORDER if key in k and k[key] is not None}


SEC18 = {"test": "GENIUS Act §18 comparability determination",
         "detail": "Unilateral Treasury comparability determination (on SCRC recommendation) + OCC registration + US-held reserves; none granted to date.",
         "administrator": "US Treasury (Stablecoin Certification Review Committee) / OCC"}
JP_CHANNEL = {"test": "Japan Electronic Payment Instruments inbound channel-determination",
              "detail": "Foreign token circulates only via a registered EPIESP holding reserves in Japan equal to customer holdings, with the foreign issuer not issuing/redeeming/soliciting to Japanese users (recognition + registration, not mutual recognition).",
              "administrator": "FSA / Local Finance Bureaus"}

C = []

C.append(corr(
    corridor_id="us-eu-usd-eur-settlement", name="United States -> European Union (USD->EUR settlement)",
    schema="corridor/v3-directed-edge", origin="US", destination="EU", direction="directed",
    currencies="USD -> EUR", feasibility_class="Category I (dual authorization available) — scale-capped",
    compatibility_category="I/II", compatibility_pair="EU-US",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "C", "D"],
    infrastructure_overlap="Project Agora (shared Western wholesale-settlement experimental path)",
    inbound_mechanism={"test": "MiCA EMT authorization wall + Article 58(3) means-of-exchange cap",
                       "detail": "A non-EUR token faces enhanced reporting and, once significant and used as a means of exchange, the Article 58(3) ceiling (one million transactions/day or EUR 200m/day). A EUR sister EMT via a MiCA-authorized issuer avoids the cap.",
                       "administrator": "EBA / national competent authorities"},
    origin_override=None,
    note="Demand is high and the corridor is operable, but the binding question is scale, not permission. A dollar token can be distributed via a MiCA-authorized issuer, yet once significant and used as a means of exchange it meets the Article 58(3) ceiling; the uncapped route is a euro sister token (Circle's euro authorization is the working example). An unauthorized dollar token cannot be lawfully distributed at all (the Tether delisting lesson).",
    source={"primary": ATLAS + ", §5.1 (United States -> European Union)",
            "secondary": ARCH + ", §5.14 (EU x US: Category I/II hybrid; interaction sets B, D)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer"]))

C.append(corr(
    corridor_id="eu-us-eur-usd-settlement", name="European Union -> United States (EUR->USD settlement)",
    schema="corridor/v3-directed-edge", origin="EU", destination="US", direction="directed",
    currencies="EUR -> USD", feasibility_class="Category II (comparability determination required)",
    compatibility_category="I/II", compatibility_pair="EU-US",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "C", "D"],
    infrastructure_overlap="Project Agora (shared Western wholesale-settlement experimental path)",
    inbound_mechanism=SEC18, origin_override=None,
    note="The asymmetric mirror of the dollar-into-Europe corridor, gated differently. A MiCA-authorized euro issuer does not thereby gain US access; entry turns on a §18 Treasury comparability determination, OCC registration, and US-held reserves. Because no comparability determination has been made to date, the corridor is Category II in practice: operable in principle, pending a determination that does not yet exist. The asymmetry is structural — the comparability gate is unilateral with no MiCA counterpart.",
    source={"primary": ATLAS + ", §5.2 (European Union -> United States)",
            "secondary": ARCH + ", §5.14 (EU x US: Category I/II hybrid)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer", "directional_asymmetry"]))

C.append(corr(
    corridor_id="us-hk-usd-hkd-settlement", name="United States -> Hong Kong SAR (USD->HKD settlement)",
    schema="corridor/v3-directed-edge", origin="US", destination="HK", direction="directed",
    currencies="USD -> HKD", feasibility_class="Category I (dual authorization available)",
    compatibility_category="I/II", compatibility_pair="HK-US",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "C", "D"],
    infrastructure_overlap="No shared production or pilot settlement rail; commercial rails subject to both regimes",
    inbound_mechanism={"test": "HKMA fiat-referenced-stablecoin licence",
                       "detail": "Licence required to issue in Hong Kong or to issue an HKD-referenced token anywhere; the first cohort is HKD-only and bank-led, so a non-HKD or crypto-native issuer needs a later licence or a partnership with a licensed issuer.",
                       "administrator": "HKMA"},
    origin_override=None,
    note="A dollar issuer seeking Hong Kong distribution confronts a first cohort that is HKD-only and bank-led. There is no general inbound recognition of a foreign dollar token for payment use; the operator needs a later HKMA licence for a non-HKD product (timing not public) or a partnership with a licensed HK issuer. The regulatory corridor is the gating archetype; the settlement corridor is contingent on it.",
    source={"primary": ATLAS + ", §5.3 (United States -> Hong Kong SAR)",
            "secondary": ARCH + ", §5.14 (US x HK: Category I/II hybrid; interaction sets A, C)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer"]))

C.append(corr(
    corridor_id="hk-us-hkd-usd-settlement", name="Hong Kong SAR -> United States (HKD->USD settlement)",
    schema="corridor/v3-directed-edge", origin="HK", destination="US", direction="directed",
    currencies="HKD -> USD", feasibility_class="Category II (comparability determination required)",
    compatibility_category="I/II", compatibility_pair="HK-US",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "C"],
    infrastructure_overlap="No shared production or pilot settlement rail; commercial rails subject to both regimes",
    inbound_mechanism=SEC18, origin_override=None,
    note="In the reverse direction an HKD-referenced token entering the US meets the same §18 comparability gate as any other foreign token. The Hong Kong extraterritorial rule is not the binding constraint here; the US inbound gate is. Category II for the same reason the euro-into-US corridor is.",
    source={"primary": ATLAS + ", §5.4 (Hong Kong SAR -> United States)",
            "secondary": ARCH + ", §5.14 (US x HK: Category I/II hybrid)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer", "directional_asymmetry"]))

C.append(corr(
    corridor_id="sg-hk-sgd-hkd-settlement", name="Singapore -> Hong Kong SAR (SGD->HKD settlement)",
    schema="corridor/v3-directed-edge", origin="SG", destination="HK", direction="directed",
    currencies="SGD -> HKD", feasibility_class="Category I (dual authorization available)",
    compatibility_category="I/II", compatibility_pair="HK-SG",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "D"],
    infrastructure_overlap="Project Ensemble + Project Guardian alignment (Hong Kong and Singapore)",
    inbound_mechanism={"test": "HKMA fiat-referenced-stablecoin licence",
                       "detail": "Licence required to issue in Hong Kong or to issue an HKD-referenced token; the first cohort is HKD-only and bank-led, so a non-HKD or crypto-native issuer needs a later licence or partnership.",
                       "administrator": "HKMA"},
    origin_override={"flag": "origin-egress override",
                     "detail": "The June 2025 MAS Digital Token Service Provider statement constrains unlicensed Singapore-based operations serving offshore customers, so the origin co-governs an otherwise destination-gated edge.",
                     "administrator": "MAS"},
    note="The most institutionally supported corridor in the Atlas: MAS and HKMA have a banking-supervision MoU and align Project Guardian with Project Ensemble, so the tokenized-asset and digital-financial archetypes are unusually live. Even so, a MAS-regulated single-currency stablecoin must be issued in Singapore and an HKD product still requires an HKMA licence, so dual authorization remains the baseline despite the cooperation.",
    source={"primary": ATLAS + ", §5.5 (Singapore -> Hong Kong SAR)",
            "secondary": ARCH + ", §5.14 (SG x HK: Category I/II hybrid; interaction sets A, F)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer", "origin_override"]))

C.append(corr(
    corridor_id="hk-cn-hkd-cny-blocked", name="Hong Kong SAR -> Mainland China (HKD->CNY/CNH, blocked)",
    schema="corridor/v3-directed-edge", origin="HK", destination="CN", direction="directed",
    currencies="HKD -> CNY/CNH", feasibility_class="Blocked at destination (issuance prohibition)",
    compatibility_category="III", compatibility_pair="CN-HK",
    archetypes=["RC", "DC"], interaction_sets=["A", "D", "F"],
    infrastructure_overlap="mBridge (shared multi-central-bank-digital-currency axis)",
    inbound_mechanism={"test": "Destination prohibition",
                       "detail": "No foreign stablecoin may circulate as a payment instrument in the mainland and no mainland entity may issue one. The prohibition is written, in-force law: 银发〔2026〕42号 (eight-ministry Notice, in force 6 Feb 2026; it repealed the 2021 Notice 银发〔2021〕237号) bars unauthorised overseas issuance of RMB-pegged stablecoins (未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币) and PRC-controlled entities issuing virtual currencies abroad. PRC cross-border data and capital rules (PIPL, DSL, CAC Cross-Border Provisions, SAFE) govern any data or capital leg.",
                       "administrator": "PBOC / CAC / SAFE"},
    origin_override=None,
    note="The mirror corridor is blocked at the destination. No foreign stablecoin, including an HKD-referenced one, may circulate in the mainland as a payment instrument. Only the regulatory and digital-financial archetypes are meaningful, and only at the level of data and capital flows. The contrast with the (also Category III) PRC->HK direction is the clearest single illustration of why corridors must be directed.",
    source={"primary": ATLAS + ", §5.8 (Hong Kong SAR -> Mainland China)",
            "secondary": ARCH + ", §5.14 (HK x CN: Category III, prohibition axis — highest-stakes pair)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer", "blocked", "category_iii"]))

C.append(corr(
    corridor_id="us-jp-usd-jpy-settlement", name="United States -> Japan (USD->JPY settlement)",
    schema="corridor/v3-directed-edge", origin="US", destination="JP", direction="directed",
    currencies="USD -> JPY", feasibility_class="Category II (channel determination required)",
    compatibility_category="I/II", compatibility_pair="JP-US",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "C"],
    infrastructure_overlap="Project Agora (shared Western wholesale-settlement experimental path)",
    inbound_mechanism=JP_CHANNEL, origin_override=None,
    note="A dollar issuer reaching into Japan does not meet automatic dual authorization; it meets a channel. A foreign-issued stablecoin circulates only via a registered EPIESP holding reserves in Japan equal to customer holdings, while the foreign issuer does not issue/redeem/solicit to Japanese users. The working example is USDC, admitted via SBI VC Trade (March 2025). Because the gating step is a recognition + registration channel-determination rather than mutual recognition, the corridor is Category II — the same class as entry into the US or the UAE — even though Japan is a fully live regime.",
    source={"primary": ATLAS + ", §5.18 (United States -> Japan)",
            "secondary": ARCH + ", §5.14 (US x JP: Category I/II hybrid; interaction sets A, C, E, F)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer"]))

C.append(corr(
    corridor_id="jp-us-jpy-usd-settlement", name="Japan -> United States (JPY->USD settlement)",
    schema="corridor/v3-directed-edge", origin="JP", destination="US", direction="directed",
    currencies="JPY -> USD", feasibility_class="Category II (comparability determination required)",
    compatibility_category="I/II", compatibility_pair="JP-US",
    archetypes=["RC", "SC", "TC", "DC"], interaction_sets=["A", "C"],
    infrastructure_overlap="Project Agora (shared Western wholesale-settlement experimental path)",
    inbound_mechanism=SEC18, origin_override=None,
    note="The asymmetric mirror. A yen Electronic Payment Instrument (issued by a bank, registered funds-transfer provider, or trust bank) is freely exportable, but entering the US it meets the §18 comparability gate. No comparability determination has been made for any jurisdiction including Japan, so the corridor is Category II in this direction too — but for a different reason than inbound: there the channel is the gate, here the comparability determination is.",
    source={"primary": ATLAS + ", §5.19 (Japan -> United States)",
            "secondary": ARCH + ", §5.14 (US x JP: Category I/II hybrid)"},
    valid_as_of="2026-06", evidence_tier="firm_summary", version_added="0.5.0",
    tags=["corridor", "directed_edge", "from_atlas_v0.2.3", "v0.5.0_corridor_layer", "directional_asymmetry"]))

if __name__ == "__main__":
    import re, sys
    # Reconcile each directed edge against the §5.14 matrix row it links to, so the
    # cross-layer relationship is DECLARED in the data (not left as a silent contradiction).
    # The compatibility object is imported directly from build_analysis (no file dependency).
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from build_analysis import compatibility as COMPAT
        COMP = {p["pair"]: p for p in COMPAT["pairs"]}
    except Exception as e:                       # pragma: no cover
        COMP = {}
        print(f"  (warning: could not import compatibility matrix for divergence reconciliation: {e})")

    DIVERGENCES = 0
    for c in C:
        pair = c.get("compatibility_pair")
        row = COMP.get(pair) if pair else None
        if row:
            # category MUST agree across layers — fail loudly here if a typo ever breaks it
            if c.get("compatibility_category") != row.get("category"):
                raise SystemExit(f"category mismatch {c['corridor_id']}: edge "
                                 f"{c.get('compatibility_category')!r} vs §5.14 {pair} {row.get('category')!r}")
            edge_sets = c.get("interaction_sets") or []
            pair_sets = row.get("interaction_sets") or []
            if sorted(edge_sets) != sorted(pair_sets):
                c["divergence"] = {
                    "kind": "interaction_sets",
                    "against_pair": pair,
                    "pair_interaction_sets": pair_sets,
                    "edge_interaction_sets": edge_sets,
                    "reason": ("Directed-edge operative interaction sets (Corridor Atlas v0.2.3 §5, read at "
                               "the destination inbound gate for THIS direction) differ from the undirected "
                               "pairwise sets (Architecture §5.14). The Atlas generalizes the §5.12/§5.14 "
                               "undirected pairs into directed edges and re-derives the operative interaction "
                               "sets per direction; the compatibility CATEGORY agrees, the interaction-set "
                               "list may differ by direction. This divergence is declared, not silent."),
                }
                DIVERGENCES += 1
        # sanitize secondary citations that list an interaction-set tail (prevents a citation
        # from appearing to contradict this edge's own interaction_sets field)
        src = c.get("source") or {}
        sec = src.get("secondary")
        if isinstance(sec, str):
            sec = re.sub(r";?\s*interaction sets [A-F](,\s*[A-F])*\)",
                         " — undirected §5.14 pair; see this edge's `divergence` field)", sec)
            src["secondary"] = sec
        # re-impose key order now that divergence may have been added
        for k in list(c.keys()):
            pass
        ordered = {key: c[key] for key in KEY_ORDER if key in c}
        c.clear(); c.update(ordered)

    written = 0
    for c in C:
        (ROOT / f"{c['corridor_id']}.yaml").write_text(
            yaml.dump(c, sort_keys=False, allow_unicode=True, default_flow_style=False, width=100), encoding="utf-8")
        written += 1
    print(f"wrote {written} directed corridor records (+ the hk-br anchor already present = {written + 1} total)")
    print(f"  declared cross-layer divergences (directed edge vs §5.14 undirected pair): {DIVERGENCES}")
    print("  edges:", ", ".join(c["corridor_id"] for c in C))
