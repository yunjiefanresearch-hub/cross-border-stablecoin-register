#!/usr/bin/env python3
"""Twelve-jurisdiction expansion (v0.4.0): add Switzerland (CH), the United Arab
Emirates (AE), Taiwan (TW), Japan (JP), and South Korea (KR) — promoting the focus
set from 7 to 12 jurisdictions.

Source of truth: the maintainer's revised research substrate —
  * Multi-Jurisdiction Stablecoin Compliance Matrix v0.9.6 (June 2026)  [the node-level data substrate]
  * Cross-Border Stablecoin Architecture v3 (Twelve Jurisdictions, June 2026) [§2 constraints, §5 survey]
  * Cross-Border Digital-Finance Corridor Atlas v0.2.3 (June 2026) [directed-edge companion]

NO citation is machine-generated: each record's primary instrument + pinpoint is transcribed
from the Matrix v0.9.6 entry, which is cited as secondary provenance. source.url is left empty
(or set to a known official URL where one is unambiguous) and every record joins the same
primary-source verification queue as the v0.2.0/v0.3.0 records. Per the Matrix's own tiered
verification note for the added entries, evidence_tier is set to firm_summary and draft-law
provisions are flagged with status: proposed (NOT in force).

Run:  python3 _build_v0_4_0.py     (writes one <id>.yaml per record into the repo root)
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

ROOT = pathlib.Path(__file__).resolve().parent
REVIEWED = "2026-06-27"
VER = "0.4.0"
MATRIX = "Fan, Multi-Jurisdiction Stablecoin Compliance Matrix v0.9.6 (June 2026)"
ARCH = "Fan, Cross-Border Stablecoin Architecture v3 (Twelve Jurisdictions, June 2026)"

KEY_ORDER = ["id", "jurisdiction", "authority", "instrument_type", "instrument_label_local",
             "dimension", "constraint_ref", "requirement_summary", "requirement_structured",
             "status", "effective_date", "source", "secondary", "interpretation_note",
             "interpretive_flag", "confidence", "evidence_tier",
             "last_reviewed", "version_added", "tags"]


def rec(**k):
    # impose stable key order for readable YAML; drop None values (optional fields omitted, not null)
    return {key: k[key] for key in KEY_ORDER if key in k and k[key] is not None}


R = []

# =====================================================================================
# SWITZERLAND (ch-frs) — regulation WITHOUT a stablecoin statute; FINMA Guidance 06/2024.
# All in force. The whole non-bank market runs through the bank-guarantee aperture
# (Banking Ordinance Art. 5(3)(f)); yield is permitted but the guarantee must cover it.
# =====================================================================================
CH = dict(jurisdiction="CH", instrument_type="fiat_referenced_stablecoin",
          instrument_label_local="stablecoin (Banking Act; bank-guarantee or licensed-institution pathway)")
CH_TAGS = ["europe", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion"]

R.append(rec(**CH, id="ch-frs-regulatory_authority-001", authority="FINMA (primary); SNB (systemic FMIs)",
  dimension="regulatory_authority",
  requirement_summary="Switzerland has no bespoke stablecoin statute: stablecoins are regulated by applying existing financial law — the Banking Act and Banking Ordinance (notably Banking Ordinance Art. 5(3)(f), which removes guaranteed funds from the deposit definition), the DLT Act and the Financial Market Infrastructure Act (FinMIA), the Collective Investment Schemes Act (CISA), and the Anti-Money Laundering Act (AMLA). FINMA Guidance 06/2024 sets out FINMA's supervisory position on stablecoins, including AML treatment and the conditions of the bank-guarantee exemption. FINMA is the primary supervisor; the SNB oversees systemic financial market infrastructures.",
  requirement_structured={"approach": "no bespoke statute; regulation by application of existing law",
    "primary_supervisor": "FINMA", "systemic_fmi_oversight": "SNB",
    "instruments": ["Banking Act + Banking Ordinance (Art. 5(3)(f))", "DLT Act", "FinMIA", "CISA", "AMLA", "FINMA Guidance 06/2024"]},
  status="in_force", effective_date=None,
  source={"primary": "Banking Act and Banking Ordinance; FINMA Guidance 06/2024 (Stablecoins)",
    "pinpoint": "FINMA as primary stablecoin supervisor; SNB for systemic FMIs; no bespoke statute", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Statutory Framework / Regulators)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Switzerland is the survey's clearest 'regulation-by-application' regime: the analytical work is done by the bank-guarantee aperture and FINMA guidance rather than a dedicated statute.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-issuer_pathway-001", authority="FINMA", dimension="issuer_pathway", constraint_ref="C1",
  requirement_summary="Two issuer pathways. Pathway 1 (licensed institution): an issuer holding a banking licence, or a FinTech licence under Art. 1b of the Banking Act, may issue stablecoins as a licensed institution. Pathway 2 (bank default-guarantee exemption): a non-bank issuer avoids the deposit-taking prohibition by securing a default guarantee (Bankengarantie) from a Swiss bank covering the deposited funds; under Banking Ordinance Art. 5(3)(f) funds covered by such a guarantee are not deposits, so the issuer is not engaged in unauthorized deposit-taking. The entire non-bank issuance market runs through this single textual aperture.",
  requirement_structured={"pathway_1": "banking licence or FinTech licence (Banking Act Art. 1b)",
    "pathway_2": "non-bank issuer under a Swiss bank default guarantee (Bankengarantie); BankO Art. 5(3)(f) excludes guaranteed funds from 'deposit'",
    "market_structure": "entire non-bank market runs through the bank-guarantee exemption"},
  status="in_force", effective_date=None,
  source={"primary": "Banking Act Art. 1b (FinTech licence); Banking Ordinance Art. 5(3)(f) (deposit exclusion); FINMA Guidance 06/2024",
    "pinpoint": "Issuer pathways — licensed-institution vs bank-guarantee exemption (BankO Art. 5(3)(f))", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Issuer Pathways and Eligibility)"},
             {"citation": ARCH + ", §2.1 (Constraint 1: Issuer Eligibility)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The bank-guarantee pathway is the structural hallmark of the Swiss regime and the single point through which the whole non-bank market is configured.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-reserve_backing-001", authority="FINMA", dimension="reserve_backing", constraint_ref="C2",
  requirement_summary="There is no statutory reserve schedule (no mandated asset list or percentages). Under the bank-guarantee pathway the protective mechanism is the guarantee, not a prescribed reserve portfolio: the guarantee must cover the principal plus interest of the deposited funds. If the arrangement is structured so that assets are held for the account of holders (rather than as a claim against the issuer), collective investment scheme (CIS) rules under CISA may apply.",
  requirement_structured={"statutory_reserve_schedule": "none",
    "protective_mechanism": "bank default guarantee covering principal + interest",
    "cis_risk": "CISA may apply if assets are held for the account of holders"},
  status="in_force", effective_date=None,
  source={"primary": "Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024; Collective Investment Schemes Act (CISA)",
    "pinpoint": "Reserve/backing — no statutory schedule; guarantee covers principal + interest; CISA characterization risk", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Reserve and Backing Requirements)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Switzerland is the survey's principal counter-example to a prescribed-reserve-portfolio model: the guarantee, not an asset schedule, performs the protective function (Matrix Tier 2 correction).",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-capital_requirements-001", authority="FINMA", dimension="capital_requirements", constraint_ref="C2",
  requirement_summary="For licensed-institution pathways, capital requirements apply per the Banking Act / FinTech-licence framework. For the bank-guarantee pathway there is no separate stablecoin capital schedule; the guarantee performs the protective function in place of a prescribed capital buffer.",
  requirement_structured={"licensed_institution": "capital per Banking Act / FinTech-licence framework",
    "bank_guarantee_pathway": "no separate stablecoin capital schedule; guarantee performs the protective function"},
  status="in_force", effective_date=None,
  source={"primary": "Banking Act / FinTech-licence framework; FINMA Guidance 06/2024",
    "pinpoint": "Capital — per licence for licensed institutions; no separate schedule under the guarantee pathway", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Capital Requirements)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-permitted_activity_yield-001", authority="FINMA",
  dimension="permitted_activity_yield", constraint_ref="C3",
  requirement_summary="Paying yield to holders is NOT prohibited — Switzerland is the clearest survey example of a regime where holder yield is permitted but structurally constrained. Under the bank-guarantee pathway the guarantee must cover any interest earned, so the cost of offering yield is the cost of guaranteeing it; the protective mechanism scales with the yield offered. This contrasts sharply with the prohibition cluster (EU Art. 50; HK Sched. 2 s.15; US GENIUS Act § 4(a)(11)).",
  requirement_structured={"holder_yield": "permitted (not prohibited)",
    "constraint": "bank guarantee must cover principal + interest; cost of yield = cost of guaranteeing it",
    "contrast": "prohibition cluster: EU / HK / US"},
  status="in_force", effective_date=None,
  source={"primary": "FINMA Guidance 06/2024; Banking Ordinance Art. 5(3)(f)",
    "pinpoint": "Yield permitted; bank guarantee must cover interest (structural constraint, not prohibition)", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Yield and Interest Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. This is the permission-cluster anchor on the C3 spine: it shows the yield boundary is drawn by guarantee economics in Switzerland, not by a flat ban.",
  interpretive_flag={"tension": "Whether holding assets for the account of holders to generate yield tips the arrangement into collective-investment-scheme (CIS) territory under CISA.",
    "resolution_channel": "FINMA characterization guidance / supervisory practice on CISA scope."},
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER,
  tags=CH_TAGS + ["spine"]))

R.append(rec(**CH, id="ch-frs-securities_classification-001", authority="FINMA",
  dimension="securities_classification", constraint_ref="C4",
  requirement_summary="If a stablecoin arrangement is structured so that assets are held for the account of holders (rather than as a contractual claim against the issuer), collective-investment-scheme rules under the Collective Investment Schemes Act (CISA) may apply. The operative characterization question is whether holding assets for holders to generate yield converts the arrangement into a CIS — the Swiss analogue to the securities-classification spine.",
  requirement_structured={"test": "are assets held for the account of holders, or as a claim against the issuer?",
    "if_for_holders": "potential CIS under CISA", "spine_analogue": "CISA characterization is the C4 boundary in Switzerland"},
  status="in_force", effective_date=None,
  source={"primary": "Collective Investment Schemes Act (CISA); FINMA Guidance 06/2024",
    "pinpoint": "CISA characterization where assets are held for the account of holders", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Reserve and Backing; Yield and Interest Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The CISA boundary is the C4 instance for Switzerland: it governs whether a yield-bearing or assets-for-holders structure leaves the payment-instrument frame for collective-investment regulation.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER,
  tags=CH_TAGS + ["spine"]))

R.append(rec(**CH, id="ch-frs-redemption-001", authority="FINMA", dimension="redemption",
  requirement_summary="Redemption is a payment claim against the issuer (or, on issuer default, against the guaranteeing bank). There is no statutory at-par redemption mandate; the claim is contractual, backed by the guarantee. Stablecoin holders are not deposit-insured — the bank guarantee, not deposit insurance, is the protection.",
  requirement_structured={"redemption": "contractual payment claim vs issuer; vs guaranteeing bank on issuer default",
    "statutory_par_mandate": "none", "deposit_insurance": "no (guarantee, not insurance, is the protection)"},
  status="in_force", effective_date=None,
  source={"primary": "Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024",
    "pinpoint": "Redemption — contractual claim vs issuer / guaranteeing bank; no statutory par mandate; not deposit-insured", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Redemption Mechanics)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Contrast the at-par mandates of HK (1 business day), SG (5 business days), and the EU (par at any time): Switzerland has no statutory par mandate.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-aml_kyc-001", authority="FINMA", dimension="aml_kyc",
  requirement_summary="FINMA Guidance 06/2024 imposes the strictest AML posture in the survey: the issuer must identify every holder, including intermediate holders, treating each as a customer, and anonymous transfers are prohibited. Full AMLA obligations apply and the FATF travel rule applies.",
  requirement_structured={"holder_identification": "every holder, including intermediate holders, treated as a customer",
    "anonymous_transfers": "prohibited", "regime": "full AMLA + FATF travel rule"},
  status="in_force", effective_date=None,
  source={"primary": "FINMA Guidance 06/2024; Anti-Money Laundering Act (AMLA)",
    "pinpoint": "AML — identify every holder incl. intermediate holders; anonymous transfers prohibited", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (AML / KYC Framework)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The identify-every-holder rule is the strictest AML posture in the survey and the binding practical constraint on Swiss-issued-token composability and transferability.",
  interpretive_flag={"tension": "The requirement to identify every holder (including intermediate holders) materially constrains transferability and composability, because each holder in a transfer chain is treated as an issuer customer; how this applies to composable/DeFi contexts is unsettled.",
    "resolution_channel": "FINMA guidance updates on holder identification in composable contexts."},
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-cross_border_data-001", authority="FINMA / FDPIC",
  dimension="cross_border_data", constraint_ref="C6",
  requirement_summary="The Swiss Federal Act on Data Protection (FADP) applies (revised FADP in force September 2023). Cross-border data transfer requires adequate protection in the recipient state or appropriate safeguards. Switzerland maintains adequacy recognition with the EU.",
  requirement_structured={"statute": "Federal Act on Data Protection (revised FADP, in force Sep 2023)",
    "transfer_rule": "adequate protection in recipient state or appropriate safeguards",
    "eu_adequacy": "maintained"},
  status="in_force", effective_date="2023-09-01",
  source={"primary": "Federal Act on Data Protection (revised FADP, in force Sep 2023)",
    "pinpoint": "Cross-border transfer — adequacy or safeguards; EU adequacy maintained", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Cross-Border Data Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Unlike the PRC PIPL/DSL regime, the FADP's EU-adequacy footing eases cross-border data flows on Swiss-anchored corridors.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-monetary_sovereignty-001", authority="FINMA / SNB",
  dimension="monetary_sovereignty", constraint_ref="C7",
  requirement_summary="There is no monetary-sovereignty usage cap: foreign-currency stablecoins are not restricted by volume or channel. The practical constraints are the bank-guarantee structure and the AML holder-identification requirement, not distribution caps. Switzerland thus sits at the permissive end of the C7 spectrum, in contrast to the EU's Article 23 quantitative cap, the UAE's onshore channel restriction, and the PRC prohibition.",
  requirement_structured={"usage_cap": "none", "foreign_currency_tokens": "unrestricted by volume or channel",
    "practical_constraints": "bank-guarantee structure + AML holder identification",
    "c7_position": "permissive end (no cap)"},
  status="in_force", effective_date=None,
  source={"primary": "FINMA Guidance 06/2024 (no usage cap); Banking Act framework",
    "pinpoint": "Monetary sovereignty — no usage cap; foreign-currency tokens unrestricted", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Distribution and Offering Restrictions)"},
             {"citation": ARCH + ", §2.7 / §5 (Constraint 7: Monetary Sovereignty)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The absence of a C7 cap is itself the data point: Switzerland regulates the issuer (via guarantee + AML), not the currency-of-denomination of the token.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-distribution-001", authority="FINMA", dimension="distribution",
  requirement_summary="There is no monetary-sovereignty usage cap and no distribution-volume restriction; foreign-currency stablecoins are not channel-restricted. The bank-guarantee structure and the FINMA holder-identification requirement are the practical distribution constraints, not caps.",
  requirement_structured={"distribution_caps": "none", "channel_restriction": "none",
    "practical_constraints": "bank-guarantee structure + holder identification"},
  status="in_force", effective_date=None,
  source={"primary": "FINMA Guidance 06/2024; Banking Act framework",
    "pinpoint": "Distribution — no caps/channel restriction; guarantee + holder-ID are the practical limits", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Distribution and Offering Restrictions)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

R.append(rec(**CH, id="ch-frs-implementation_status-001", authority="FINMA",
  dimension="implementation_status",
  requirement_summary="Guidance-in-force regime. Milestones: FINMA Guidance 06/2024 published (Jul 2024); bank-guarantee and licensed-institution pathways in operation (2024-2025); consultation on a Financial Institutions Act (FinIA) amendment creating a dedicated payment-instrument-institution licence to replace the guarantee workaround closed (6 Feb 2026); six-bank CHF stablecoin sandbox launched (8 Apr 2026). If enacted, the FinIA amendment would replace the guarantee workaround with a purpose-built regime.",
  requirement_structured={"regime_stage": "guidance in force; reform bill in train",
    "milestones": ["FINMA Guidance 06/2024 (Jul 2024)", "FinIA-amendment consultation closed 6 Feb 2026", "6-bank CHF sandbox 8 Apr 2026"],
    "next_milestone": "FinIA-amendment outcome (payment-instrument-institution licence)"},
  status="in_force", effective_date="2024-07-01",
  source={"primary": "FINMA Guidance 06/2024; FinIA-amendment consultation (closed 6 Feb 2026)",
    "pinpoint": "Timeline — guidance Jul 2024; FinIA consultation closed 6 Feb 2026; 6-bank CHF sandbox 8 Apr 2026", "url": ""},
  secondary=[{"citation": MATRIX + ", §Switzerland (Implementation Timeline)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. As of June 2026 a reader should re-verify the FinIA-amendment status, the outcome of the six-bank CHF sandbox, and any FINMA guidance updates.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=CH_TAGS))

# =====================================================================================
# UNITED ARAB EMIRATES (ae-pt) — federal-vs-free-zone split + monetary-sovereignty
# channel restriction. CBUAE PTSR (Circular 2/2024) onshore; VARA/ADGM-FSRA/DIFC-DFSA
# free zones. In force; one-year PTSR transition closed; AED + USD tokens live.
# =====================================================================================
AE = dict(jurisdiction="AE", instrument_type="payment_stablecoin",
          instrument_label_local="Payment Token (Dirham Payment Token / Foreign Payment Token)")
AE_TAGS = ["mideast", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion"]

R.append(rec(**AE, id="ae-pt-regulatory_authority-001",
  authority="CBUAE (onshore); VARA / ADGM-FSRA / DIFC-DFSA (free zones)",
  dimension="regulatory_authority",
  requirement_summary="The UAE operates a federal-versus-free-zone split. Onshore, the Central Bank of the UAE (CBUAE) Payment Token Services Regulation (PTSR, Circular 2/2024) governs payment-token issuance and use. The financial free zones run their own fiat-referenced-token regimes: VARA (Dubai, outside the DIFC); the ADGM Financial Services Regulatory Authority (FSRA) under its Fiat-Referenced Token (FRT) framework; and the DIFC's Dubai Financial Services Authority (DFSA) under its Crypto Token rules.",
  requirement_structured={"split": "federal (onshore) vs financial free zones",
    "onshore": "CBUAE PTSR (Circular 2/2024)",
    "free_zones": ["VARA (Dubai ex-DIFC)", "ADGM-FSRA (FRT framework)", "DIFC-DFSA (Crypto Token rules)"]},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE Payment Token Services Regulation (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks",
    "pinpoint": "Regulators — CBUAE onshore; VARA / ADGM-FSRA / DIFC-DFSA free zones", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Statutory Framework / Regulators)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The four-regulator split is the structural hallmark: onshore and free-zone regimes are distinct perimeters, not a single national regime (Matrix Tier 2 correction).",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-issuer_pathway-001", authority="CBUAE / VARA / FSRA / DFSA",
  dimension="issuer_pathway", constraint_ref="C1",
  requirement_summary="Onshore, a Dirham Payment Token (DPT) may be issued only by a CBUAE-licensed, UAE-incorporated entity; a Foreign Payment Token (FPT) is a registered foreign issuer's token that may be used only to purchase virtual assets or derivatives, not for general payments. Banks may issue payment tokens through a subsidiary. Free-zone issuers operate under the VARA/FSRA/DFSA frameworks but cannot issue AED tokens — AED issuance is reserved to the CBUAE regime.",
  requirement_structured={"dpt_onshore": "CBUAE-licensed, UAE-incorporated entity",
    "fpt_onshore": "registered foreign issuer; usable only for VA/derivative purchases",
    "banks": "may issue via a subsidiary", "free_zone": "VARA/FSRA/DFSA frameworks; cannot issue AED tokens"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks",
    "pinpoint": "Issuer pathways — DPT (CBUAE-licensed); FPT (foreign, VA/derivative-only); bank subsidiary; free-zone cannot issue AED", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Issuer Pathways and Eligibility)"},
             {"citation": ARCH + ", §2.1 (Constraint 1: Issuer Eligibility)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The AED-issuance carve-out (free zones cannot issue AED) is the constraint that ties issuer eligibility to the monetary-sovereignty channel restriction (see ae-pt-monetary_sovereignty-001).",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-reserve_backing-001", authority="CBUAE / free-zone regulators",
  dimension="reserve_backing", constraint_ref="C2",
  requirement_summary="Onshore: 100% backing, segregated in UAE banks. The bank-subsidiary option requires at least 50% cash plus UAE government bonds / CBUAE monetary bills. Free-zone frameworks impose their own reserve requirements (e.g., the ADGM FRT framework requires high-quality liquid reserves).",
  requirement_structured={"onshore": "100% backing, segregated in UAE banks",
    "bank_subsidiary": ">=50% cash + UAE government bonds / CBUAE monetary bills",
    "free_zone": "own reserve requirements (ADGM FRT: high-quality liquid reserves)"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024); ADGM FRT framework",
    "pinpoint": "Reserve/backing — 100% segregated in UAE banks; bank-subsidiary >=50% cash + UAE govt bonds/CBUAE bills", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Reserve and Backing Requirements)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-capital_requirements-001", authority="CBUAE / free-zone regulators",
  dimension="capital_requirements", constraint_ref="C2",
  requirement_summary="Onshore, capital requirements are as specified by the CBUAE PTSR. Free-zone issuers face capital requirements per the relevant VARA/FSRA/DFSA framework. The specific figures differ by perimeter.",
  requirement_structured={"onshore": "per CBUAE PTSR", "free_zone": "per VARA/FSRA/DFSA framework"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks",
    "pinpoint": "Capital — per CBUAE PTSR onshore; per free-zone framework", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Capital Requirements)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-permitted_activity_yield-001", authority="CBUAE / ADGM-FSRA",
  dimension="permitted_activity_yield", constraint_ref="C3",
  requirement_summary="Issuer-paid yield is prohibited onshore (CBUAE). ADGM permits the issuer to earn reserve income but bans the promotion of the token as an investment or savings product. The operative line in ADGM is promotion, not the earning of reserve income — an approach that resembles the US 'solely in connection with holding' analysis more than a flat prohibition.",
  requirement_structured={"onshore_cbuae": "issuer-paid yield prohibited",
    "adgm": "reserve income permitted; promotion as investment/savings product banned",
    "operative_line_adgm": "promotion, not the earning of income"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework",
    "pinpoint": "Yield — prohibited onshore; ADGM permits reserve income but bans investment/savings promotion", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Yield and Interest Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The onshore/ADGM split is the C3 data point for the UAE: ADGM's promotion-based line is the survey's closest non-US analogue to the GENIUS Act 'solely' construction.",
  interpretive_flag={"tension": "The UAE's split produces a yield asymmetry: onshore prohibits issuer-paid yield while ADGM permits reserve income but bans investment/savings promotion; the operative ADGM line is promotion, not the earning of income.",
    "resolution_channel": "CBUAE / ADGM-FSRA supervisory practice; any onshore-vs-free-zone harmonization."},
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER,
  tags=AE_TAGS + ["spine"]))

R.append(rec(**AE, id="ae-pt-redemption-001", authority="CBUAE / ADGM-FSRA",
  dimension="redemption",
  requirement_summary="Onshore (CBUAE): redemption at par, no later than the next business day. ADGM: redemption at par within T+2. Free-zone frameworks specify their own redemption timelines.",
  requirement_structured={"onshore_cbuae": "at par, <= next business day", "adgm": "at par within T+2",
    "free_zone": "per framework"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework",
    "pinpoint": "Redemption — CBUAE par <= next business day; ADGM par within T+2", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Redemption Mechanics)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-aml_kyc-001", authority="CBUAE / VARA / FSRA / DFSA",
  dimension="aml_kyc",
  requirement_summary="Federal AML/CFT law applies across onshore and free zones, the FATF travel rule applies, and each regulator (CBUAE, VARA, FSRA, DFSA) imposes AML/CFT obligations within its perimeter.",
  requirement_structured={"federal_aml_cft": "applies onshore and across free zones",
    "travel_rule": "applies", "per_regulator": "CBUAE / VARA / FSRA / DFSA each within its perimeter"},
  status="in_force", effective_date=None,
  source={"primary": "UAE federal AML/CFT law; CBUAE / VARA / FSRA / DFSA AML rules",
    "pinpoint": "AML — federal AML/CFT + FATF travel rule; per-regulator obligations", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (AML / KYC Framework)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-cross_border_data-001", authority="CBUAE / DIFC / ADGM",
  dimension="cross_border_data", constraint_ref="C6",
  requirement_summary="The Federal Personal Data Protection Law (PDPL) applies onshore. The DIFC and ADGM have their own data-protection regimes (DIFC Data Protection Law; ADGM Data Protection Regulations). Cross-border data-transfer rules vary by zone.",
  requirement_structured={"onshore": "Federal Personal Data Protection Law (PDPL)",
    "difc": "DIFC Data Protection Law", "adgm": "ADGM Data Protection Regulations",
    "transfer_rules": "vary by zone"},
  status="in_force", effective_date=None,
  source={"primary": "Federal Personal Data Protection Law (PDPL); DIFC Data Protection Law; ADGM Data Protection Regulations",
    "pinpoint": "Cross-border data — PDPL onshore; DIFC/ADGM own regimes; transfer rules vary by zone", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Cross-Border Data Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-monetary_sovereignty-001", authority="CBUAE",
  dimension="monetary_sovereignty", constraint_ref="C7",
  requirement_summary="The CBUAE PTSR imposes a channel restriction grounded in monetary sovereignty: no merchant may accept a virtual asset as payment for goods or services unless it is a Dirham Payment Token from a CBUAE-licensed issuer. Foreign payment tokens may be accepted only to buy virtual assets or derivatives, not for general onshore payments. This is a usage-channel restriction, not an aggregate cap — there is no volume ceiling, but foreign tokens are excluded from the general-payments channel, which is reserved for CBUAE-licensed Dirham Payment Tokens.",
  requirement_structured={"mechanism": "usage channel restriction (not an aggregate cap)",
    "rule": "general onshore payments reserved to CBUAE-licensed Dirham Payment Tokens",
    "foreign_tokens": "usable only to buy virtual assets or derivatives, not general payments",
    "contrast": "EU Art. 23 quantitative cap vs UAE channel restriction"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE Payment Token Services Regulation (Circular 2/2024)",
    "pinpoint": "Channel restriction — merchants may accept only CBUAE-licensed Dirham Payment Tokens for goods/services; foreign tokens VA/derivative-only", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Distribution and Offering Restrictions)"},
             {"citation": ARCH + ", §2.7 / §5 (Constraint 7: Monetary Sovereignty)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The UAE channel restriction is a distinct C7 mechanism: it caps the use case (general payments) rather than the volume, reserving the merchant-acceptance channel for AED tokens (Matrix Tier 2 correction: channel restriction, not aggregate cap).",
  interpretive_flag={"tension": "Whether free-zone USD tokens can be used in onshore commerce through any compliant structure, given the channel restriction reserving general payments to CBUAE-licensed Dirham Payment Tokens.",
    "resolution_channel": "CBUAE enforcement practice; any CBUAE/free-zone harmonization."},
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-distribution-001", authority="CBUAE / free-zone regulators",
  dimension="distribution", constraint_ref="C8",
  requirement_summary="The CBUAE channel restriction is the distribution-side constraint: foreign payment tokens are excluded from the general-payments channel and may be accepted only to buy virtual assets or derivatives. Free-zone issuers cannot issue AED tokens and are carved out of the onshore payment perimeter. There is no aggregate volume cap.",
  requirement_structured={"channel_restriction": "foreign tokens excluded from general payments (VA/derivative purchases only)",
    "free_zone_carve_out": "cannot issue AED tokens; outside onshore payment perimeter",
    "aggregate_cap": "none"},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024)",
    "pinpoint": "Distribution — channel restriction; free-zone issuers carved out of onshore perimeter", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Distribution and Offering Restrictions)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

R.append(rec(**AE, id="ae-pt-implementation_status-001", authority="CBUAE / free-zone regulators",
  dimension="implementation_status",
  requirement_summary="In-force regime. Milestones: CBUAE Payment Token Services Regulation (Circular 2/2024) issued (2024); one-year transition period for existing arrangements (2024-2025); transition period closes and AED tokens (AE Coin, Zand AED) go live, with the DFSA recognising USD tokens (USDC, RLUSD) (2025-2026). Multiple AED tokens and DFSA-recognised USD tokens are now live.",
  requirement_structured={"regime_stage": "in force; transition closed",
    "milestones": ["CBUAE PTSR (Circular 2/2024) issued 2024", "one-year transition 2024-2025", "transition closed; AED + USD tokens live 2025-2026"],
    "live_tokens": ["AE Coin", "Zand AED", "USDC (DFSA-recognised)", "RLUSD (DFSA-recognised)"]},
  status="in_force", effective_date=None,
  source={"primary": "CBUAE PTSR (Circular 2/2024); DFSA recognition of USD tokens",
    "pinpoint": "Timeline — PTSR 2024; one-year transition closed; AED + DFSA-recognised USD tokens live", "url": ""},
  secondary=[{"citation": MATRIX + ", §United Arab Emirates (Implementation Timeline)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. As of June 2026 a reader should re-verify channel-restriction enforcement and new AED/USD token launches.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=AE_TAGS))

# =====================================================================================
# TAIWAN (tw-frs) — pre-comprehensive-regime: AML registration in force (30 Nov 2024);
# the Virtual Asset Service Act (issuance licensing) is a DRAFT bill (committee first
# review 3 Jun 2026). All issuance/reserve/yield/redemption provisions are PROPOSED.
# =====================================================================================
TW = dict(jurisdiction="TW", instrument_type="fiat_referenced_stablecoin",
          instrument_label_local="virtual asset / draft stablecoin (Virtual Asset Service Act)")
TW_TAGS = ["apac", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion"]
TW_DRAFT = ["apac", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion", "draft_provision"]

R.append(rec(**TW, id="tw-frs-regulatory_authority-001",
  authority="FSC (primary; consults the CBC)", dimension="regulatory_authority",
  requirement_summary="Two layers, only one in force. In force: AML registration under the amended Money Laundering Control Act and the VASP Registration Regulations (effective 30 November 2024). Draft (not in force): the Virtual Asset Service Act, a comprehensive bill that would create FSC licensing for virtual-asset services including stablecoin issuance, with mandatory central-bank consultation; committee first review completed 3 June 2026. The FSC is the primary regulator and consults the Central Bank of the Republic of China (Taiwan) (CBC) on stablecoin matters.",
  requirement_structured={"in_force_layer": "AML registration (amended Money Laundering Control Act + VASP Registration Regulations, 30 Nov 2024)",
    "draft_layer": "Virtual Asset Service Act (FSC licensing; committee first review 3 Jun 2026; not in force)",
    "primary_regulator": "FSC", "central_bank_role": "CBC consulted (onshore-NTD posture is the live question)"},
  status="in_force", effective_date="2024-11-30",
  source={"primary": "Money Laundering Control Act (as amended) + VASP Registration Regulations (in force 30 Nov 2024); draft Virtual Asset Service Act",
    "pinpoint": "Regulators — FSC primary (consults CBC); AML registration in force; comprehensive act in committee", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Statutory Framework / Regulators)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Only the AML-registration layer is operative law; the issuance regime is draft. This entry is a regime-under-construction snapshot — the most likely in the survey to be overtaken by events.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_TAGS))

R.append(rec(**TW, id="tw-frs-issuer_pathway-001", authority="FSC (would administer)",
  dimension="issuer_pathway", constraint_ref="C1",
  requirement_summary="No stablecoin issuer is licensed yet (no licensing regime is in force). DRAFT: the Virtual Asset Service Act would require an FSC licence for stablecoin issuance, available to a share company (corporation limited by shares), with banks expected to lead initial issuance. These are draft provisions, not operative law.",
  requirement_structured={"in_force": "no licensing regime; no issuer licensed",
    "draft": "FSC licence; share company; banks to lead initially",
    "status_note": "draft provisions only — not operative"},
  status="proposed", effective_date=None,
  source={"primary": "Draft Virtual Asset Service Act (committee first review 3 Jun 2026)",
    "pinpoint": "Issuer pathway (draft) — FSC licence; share company; banks lead; NOT in force", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Issuer Pathways and Eligibility)"},
             {"citation": ARCH + ", §2.1 (Constraint 1: Issuer Eligibility)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: the issuance-licensing provisions are draft, not operative (Matrix CONDITIONAL-STATUS flag). The only in-force layer is AML registration (see tw-frs-aml_kyc-001).",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_DRAFT))

R.append(rec(**TW, id="tw-frs-reserve_backing-001", authority="FSC (would administer)",
  dimension="reserve_backing", constraint_ref="C2",
  requirement_summary="DRAFT: full reserves held at domestic financial institutions, segregated from the issuer's own property. No reserve regime is in force (AML registration does not impose reserve requirements). Draft provisions only.",
  requirement_structured={"in_force": "none", "draft": "full reserves at domestic financial institutions, segregated from issuer property"},
  status="proposed", effective_date=None,
  source={"primary": "Draft Virtual Asset Service Act",
    "pinpoint": "Reserve/backing (draft) — full reserves at domestic FIs, segregated; NOT in force", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Reserve and Backing Requirements)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_DRAFT))

R.append(rec(**TW, id="tw-frs-capital_requirements-001", authority="FSC (would administer)",
  dimension="capital_requirements", constraint_ref="C2",
  requirement_summary="DRAFT: capital requirements to be specified by the FSC under the Virtual Asset Service Act. No stablecoin capital regime is in force.",
  requirement_structured={"in_force": "none", "draft": "FSC to specify under the Virtual Asset Service Act"},
  status="proposed", effective_date=None,
  source={"primary": "Draft Virtual Asset Service Act",
    "pinpoint": "Capital (draft) — FSC to specify; NOT in force", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Capital Requirements)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
  confidence="low", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_DRAFT))

R.append(rec(**TW, id="tw-frs-permitted_activity_yield-001", authority="FSC (would administer)",
  dimension="permitted_activity_yield", constraint_ref="C3",
  requirement_summary="DRAFT: the bill prohibits paying interest or other returns to holders. No yield regime is in force. The draft yield prohibition would align Taiwan with the prohibition cluster (EU, Hong Kong) rather than the permission cluster (Switzerland, Brazil), but this is a draft provision, not operative law.",
  requirement_structured={"in_force": "none", "draft": "prohibition on interest or other returns to holders",
    "would_align_with": "prohibition cluster (EU, HK)"},
  status="proposed", effective_date=None,
  source={"primary": "Draft Virtual Asset Service Act",
    "pinpoint": "Yield (draft) — prohibition on interest/other returns; NOT in force", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Yield and Interest Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law. On the C3 spine, Taiwan is a draft member of the prohibition cluster.",
  interpretive_flag={"tension": "Taiwan's draft yield prohibition aligns it with the prohibition cluster (EU, HK) rather than the permission cluster (Switzerland, Brazil), but whether it survives to enactment, and in what form, is open.",
    "resolution_channel": "Enactment of the Virtual Asset Service Act and its final text."},
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER,
  tags=TW_DRAFT + ["spine"]))

R.append(rec(**TW, id="tw-frs-redemption-001", authority="FSC (would administer)",
  dimension="redemption",
  requirement_summary="DRAFT: par issuance and redemption. No redemption regime is in force. Draft provisions only.",
  requirement_structured={"in_force": "none", "draft": "par issuance and redemption"},
  status="proposed", effective_date=None,
  source={"primary": "Draft Virtual Asset Service Act",
    "pinpoint": "Redemption (draft) — par issuance and redemption; NOT in force", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Redemption Mechanics)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
  confidence="low", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_DRAFT))

R.append(rec(**TW, id="tw-frs-aml_kyc-001", authority="FSC",
  dimension="aml_kyc",
  requirement_summary="IN FORCE: AML registration under the amended Money Laundering Control Act and the VASP Registration Regulations (since 30 November 2024), requiring virtual-asset service providers to register and comply with AML/CFT obligations; the FATF travel rule applies. This is the only operative layer of the Taiwan regime.",
  requirement_structured={"in_force": "AML registration (amended Money Laundering Control Act + VASP Registration Regulations, 30 Nov 2024)",
    "travel_rule": "applies", "note": "the only operative layer of the Taiwan regime"},
  status="in_force", effective_date="2024-11-30",
  source={"primary": "Money Laundering Control Act (as amended) + VASP Registration Regulations (in force 30 Nov 2024)",
    "pinpoint": "AML — VASP registration since 30 Nov 2024; FATF travel rule (the only in-force layer)", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (AML / KYC Framework)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. This is the anchor in-force record for Taiwan: AML registration is the only operative obligation pending enactment of the Virtual Asset Service Act.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_TAGS))

R.append(rec(**TW, id="tw-frs-cross_border_data-001", authority="FSC / PDPA competent authority",
  dimension="cross_border_data", constraint_ref="C6",
  requirement_summary="The Personal Data Protection Act (PDPA) applies. Cross-border data transfer is subject to the PDPA and to competent-authority restrictions.",
  requirement_structured={"statute": "Personal Data Protection Act (PDPA)",
    "transfer_rule": "subject to PDPA + competent-authority restrictions"},
  status="in_force", effective_date=None,
  source={"primary": "Personal Data Protection Act (PDPA)",
    "pinpoint": "Cross-border data — PDPA + competent-authority restrictions", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Cross-Border Data Treatment)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_TAGS))

R.append(rec(**TW, id="tw-frs-monetary_sovereignty-001", authority="CBC (central bank)",
  dimension="monetary_sovereignty", constraint_ref="C7",
  requirement_summary="No stablecoin-specific monetary-sovereignty regime is in force. The backdrop is the central bank's control of the NTD and the offshore-NTD posture; the peg currency for a future Taiwan stablecoin (NTD vs USD) is officially undecided. A NTD-pegged stablecoin engages the central bank's monetary-sovereignty concerns directly; a USD-pegged stablecoin engages offshore-NTD and capital-flow concerns. The choice is the central monetary-sovereignty question for Taiwan.",
  requirement_structured={"in_force_cap": "none", "backdrop": "CBC control of NTD; offshore-NTD posture",
    "peg_currency": "officially undecided (NTD vs USD)",
    "ntd_peg": "engages monetary-sovereignty concerns directly",
    "usd_peg": "engages offshore-NTD and capital-flow concerns"},
  status="proposed", effective_date=None,
  source={"primary": "CBC public statements; draft Virtual Asset Service Act",
    "pinpoint": "Monetary sovereignty — peg currency undecided (NTD vs USD); NTD offshore controls are the backdrop", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Distribution and Offering Restrictions)"},
             {"citation": ARCH + ", §5 (Taiwan — monetary-sovereignty posture)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: there is no in-force C7 cap; the peg-currency decision is the defining open issue (Matrix interpretive flag).",
  interpretive_flag={"tension": "The peg-currency question (NTD vs USD) is the defining open issue: a NTD peg engages the central bank's monetary-sovereignty concerns; a USD peg engages offshore-NTD and capital-flow concerns.",
    "resolution_channel": "Enactment of the Virtual Asset Service Act and the central bank's ultimate posture."},
  confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_DRAFT))

R.append(rec(**TW, id="tw-frs-distribution-001", authority="FSC (would administer)",
  dimension="distribution",
  requirement_summary="No stablecoin-specific distribution regime is in force. Draft provisions on offering would take effect only on enactment of the Virtual Asset Service Act. The backdrop is the central bank's control of the NTD and the offshore-NTD posture.",
  requirement_structured={"in_force": "none", "draft": "offering provisions effective only on VASA enactment"},
  status="proposed", effective_date=None,
  source={"primary": "Draft Virtual Asset Service Act",
    "pinpoint": "Distribution (draft) — offering provisions on VASA enactment; NOT in force", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Distribution and Offering Restrictions)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
  confidence="low", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_DRAFT))

R.append(rec(**TW, id="tw-frs-implementation_status-001", authority="FSC / CBC",
  dimension="implementation_status",
  requirement_summary="Pre-comprehensive-regime (a regime under construction). Milestones: AML registration regime in force (30 November 2024); Virtual Asset Service Act drafting and legislative process (2025-2026); committee first review of the Virtual Asset Service Act completed (3 June 2026); further readings and enactment pending with no date certain. No licensed stablecoin issuers yet; peg currency officially undecided.",
  requirement_structured={"regime_stage": "pre-comprehensive (regime under construction)",
    "milestones": ["AML registration in force 30 Nov 2024", "VASA committee first review 3 Jun 2026", "further readings + enactment pending (no date)"],
    "issuers": "none licensed", "peg_currency": "undecided"},
  status="in_force", effective_date="2024-11-30",
  source={"primary": "VASP Registration Regulations (30 Nov 2024); draft Virtual Asset Service Act (committee first review 3 Jun 2026)",
    "pinpoint": "Timeline — AML reg in force 30 Nov 2024; VASA first review 3 Jun 2026; enactment pending", "url": ""},
  secondary=[{"citation": MATRIX + ", §Taiwan (Implementation Timeline)"}],
  interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Status records the in-force AML maturity stage; the comprehensive regime is draft. This is the survey's most volatile entry — re-verify legislative progress and the peg decision after mid-2026.",
  confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=TW_TAGS))

# (Japan + South Korea appended in part 2)
if __name__ == "__main__":
    import _build_v0_4_0_part2 as p2  # noqa: F401  (extends R)
    p2.extend(R, rec, dict(REVIEWED=REVIEWED, VER=VER, MATRIX=MATRIX, ARCH=ARCH))
    written = 0
    for r in R:
        path = ROOT / f"{r['id']}.yaml"
        path.write_text(yaml.dump(r, sort_keys=False, allow_unicode=True,
                                  default_flow_style=False, width=100), encoding="utf-8")
        written += 1
    print(f"wrote {written} records ({len([r for r in R if r['jurisdiction']=='CH'])} CH, "
          f"{len([r for r in R if r['jurisdiction']=='AE'])} AE, "
          f"{len([r for r in R if r['jurisdiction']=='TW'])} TW, "
          f"{len([r for r in R if r['jurisdiction']=='JP'])} JP, "
          f"{len([r for r in R if r['jurisdiction']=='KR'])} KR)")
