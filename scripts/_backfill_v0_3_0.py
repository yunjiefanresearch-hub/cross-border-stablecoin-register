#!/usr/bin/env python3
"""Backfill records for SG / UK / CN (v0.3.0), transcribed from the author's
Compliance Matrix v0.9.3 (pp.14-28). NO citation is machine-generated: each
record's primary instrument + pinpoint is transcribed from the matrix text,
which is cited as secondary provenance. source.url is left empty and each
record joins the same primary-source verification queue as the v0.2.0 records.
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
REVIEWED = "2026-06-17"
VER = "0.3.0"
MATRIX = "Fan, Compliance Matrix v0.9.3 (18 May 2026)"

def rec(**k):
    # impose stable key order for readable YAML; drop None values (optional fields omitted, not null)
    order = ["id","jurisdiction","authority","instrument_type","instrument_label_local",
             "dimension","constraint_ref","requirement_summary","requirement_structured",
             "status","effective_date","source","secondary","interpretation_note",
             "confidence","last_reviewed","version_added","tags"]
    return {key: k[key] for key in order if key in k and k[key] is not None}

R = []

# ============================== SINGAPORE (sg-scs) ==============================
SG = dict(jurisdiction="SG", instrument_type="fiat_referenced_stablecoin",
          instrument_label_local="single-currency stablecoin (SCS)")

R.append(rec(**SG, id="sg-scs-issuer_pathway-001", authority="MAS", dimension="issuer_pathway", constraint_ref="C1",
  requirement_summary="The MAS Single-Currency Stablecoin (SCS) framework applies only to stablecoins pegged to the Singapore Dollar or any G10 currency and issued in Singapore; tokens pegged to other assets or issued offshore stay under the general Digital Payment Token regime and may not use the 'MAS-regulated stablecoin' label. Non-bank SCS issuers with circulation above S$5 million must hold a Major Payment Institution (MPI) licence; those below are exempt from the framework but cannot use the label. Banks are exempt from the PSA licence requirement and may issue under their banking framework. Issuers must be incorporated in Singapore.",
  requirement_structured={"peg_scope":"SGD or any G10 currency, issued in Singapore","mpi_threshold":"circulation > S$5,000,000 requires MPI licence","below_threshold":"exempt but no 'MAS-regulated' label","banks":"exempt from PSA licence","incorporation":"must be incorporated in Singapore"},
  status="transitional", effective_date="2023-08-15",
  source={"primary":"Payment Services Act 2019 (PSA, amended 2022); MAS Single-Currency Stablecoin Regulatory Framework (finalised 15 Aug 2023)","pinpoint":"SCS framework — peg scope (SGD/G10, Singapore-issued); MPI licence > S$5m; Singapore incorporation","url":""},
  secondary=[{"citation":MATRIX+", pp.18-19 (Singapore — Issuer Pathways and Eligibility)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification (source.url to be filled). The S$5m threshold creates an opt-in regime for small issuers; the MPI + incorporation rules confine the framework to bank-led or institutional issuers in practice.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-securities_classification-001", authority="MAS", dimension="securities_classification", constraint_ref="C4",
  requirement_summary="Token classification follows MAS's substance-over-form test: a token with capital-markets-product characteristics is regulated under the Securities and Futures Act (SFA), not the Payment Services Act, and falls outside the SCS framework entirely. Tokens marketed as offering yield or as investments would likely be classified as securities under the SFA. The destination-product classification analysis governs whether a routing architecture that converts SCS holdings into SFA-regulated capital-markets-product shares is permissible.",
  requirement_structured={"test":"MAS substance-over-form","securities_regulator_statute":"Securities and Futures Act (SFA)","yield_marketed_tokens":"likely securities under SFA, outside SCS","routing_question":"turns on SFA classification of destination product"},
  status="in_force", effective_date=None,
  source={"primary":"Securities and Futures Act (SFA); MAS substance-over-form classification","pinpoint":"SFA classification — capital-markets-product characteristics regulated under SFA, not PSA","url":""},
  secondary=[{"citation":MATRIX+", pp.18-19 (Singapore — Issuer Pathways; Yield and Interest Treatment)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. This is the SG instance of the securities-classification spine (C4): the SFA boundary is what removes yield-bearing or investment-marketed tokens from SCS scope.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill","new_dimension"]))

R.append(rec(**SG, id="sg-scs-reserve_backing-001", authority="MAS", dimension="reserve_backing", constraint_ref="C2",
  requirement_summary="SCS reserves must be 100% backed in cash, cash equivalents, or short-term sovereign debt securities denominated in the pegged currency, valued at daily mark-to-market, segregated from the issuer's own assets, and held with MAS-approved custodians. Reserves are subject to monthly independent attestation and annual external audit, with audit reports publicly disclosed.",
  requirement_structured={"backing":"100% cash / cash equivalents / short-term sovereign debt in pegged currency","valuation":"daily mark-to-market","segregation":"segregated; MAS-approved custodians","assurance":"monthly attestation + annual external audit, publicly disclosed"},
  status="transitional", effective_date="2023-08-15",
  source={"primary":"MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023)","pinpoint":"Reserve and backing requirements — 100% backing; daily MTM; monthly attestation; annual audit","url":""},
  secondary=[{"citation":MATRIX+", p.18 (Singapore — Reserve and Backing Requirements)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. Note the pegged-currency-denomination requirement on reserve assets, which ties reserve composition to the SGD/G10 peg scope.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-capital_requirements-001", authority="MAS", dimension="capital_requirements", constraint_ref="C2",
  requirement_summary="An SCS issuer must hold base capital of at least S$1 million or 50% of annual operating expenses, whichever is higher, plus liquid assets sufficient for an orderly wind-down. DTSP licensees (where granted) face a separate S$250,000 base-capital requirement, a S$10,000 annual licence fee, a Singapore-based compliance officer, and annual penetration testing.",
  requirement_structured={"base_capital":"max(S$1,000,000 ; 50% of annual operating expenses)","wind_down":"liquid assets sufficient for orderly wind-down","dtsp_base_capital":"S$250,000 + S$10,000 annual fee + SG compliance officer + annual pen-test"},
  status="transitional", effective_date="2023-08-15",
  source={"primary":"MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023); FSMA Part 9 (DTSP)","pinpoint":"Capital requirements — base capital S$1m or 50% opex; DTSP S$250k","url":""},
  secondary=[{"citation":MATRIX+", p.19 (Singapore — Capital Requirements)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-redemption-001", authority="MAS", dimension="redemption", constraint_ref=None,
  requirement_summary="SCS holders are entitled to redemption at par value within 5 business days of a valid request, with no unreasonable fees or conditions, and customer assets are held under a statutory trust.",
  requirement_structured={"par_redemption":"at par within 5 business days of valid request","fees":"no unreasonable fees or conditions","trust":"statutory trust of customer assets"},
  status="transitional", effective_date="2023-08-15",
  source={"primary":"MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023)","pinpoint":"Redemption mechanics — par redemption within 5 business days; statutory trust","url":""},
  secondary=[{"citation":MATRIX+", p.18 (Singapore — Redemption Mechanics)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. Contrast HK's 1-business-day par redemption.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-aml_kyc-001", authority="MAS", dimension="aml_kyc", constraint_ref=None,
  requirement_summary="AML/CFT obligations apply under MAS Notice PSN02 (payment services) and Notice PSN03 (digital payment tokens), including the FATF travel rule for digital-payment-token transfers, FATF-aligned KYC, transaction monitoring, and suspicious-transaction reporting.",
  requirement_structured={"notices":["MAS Notice PSN02 (payment services)","MAS Notice PSN03 (digital payment tokens)"],"travel_rule":"applies to DPT transfers","standard":"FATF-aligned KYC, monitoring, STR"},
  status="in_force", effective_date=None,
  source={"primary":"MAS Notice PSN02; MAS Notice PSN03","pinpoint":"AML/CFT — PSN02/PSN03; travel rule for DPT transfers","url":""},
  secondary=[{"citation":MATRIX+", p.19 (Singapore — AML / KYC Framework)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-cross_border_data-001", authority="MAS; PDPC", dimension="cross_border_data", constraint_ref="C6",
  requirement_summary="Cross-border personal-data transfer is governed by the Personal Data Protection Act 2012 (PDPA), which requires reasonable safeguards — consent, contract, certification, or transfer to a jurisdiction with comparable protection. MAS Outsourcing Guidelines and Technology Risk Management Guidelines apply to data hosting.",
  requirement_structured={"statute":"Personal Data Protection Act 2012 (PDPA)","transfer_gates":["consent","contract","certification","comparable-protection jurisdiction"],"data_hosting":"MAS Outsourcing + Technology Risk Management Guidelines"},
  status="in_force", effective_date=None,
  source={"primary":"Personal Data Protection Act 2012 (PDPA); MAS Outsourcing and Technology Risk Management Guidelines","pinpoint":"PDPA cross-border transfer safeguards; MAS data-hosting guidelines","url":""},
  secondary=[{"citation":MATRIX+", p.19 (Singapore — Cross-Border Data Treatment)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. The PDPA gate set is materially lighter than the PRC PIPL/DSL regime.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-distribution-001", authority="MAS", dimension="distribution", constraint_ref="C8",
  requirement_summary="The 'MAS-regulated stablecoin' label is restricted to SCS-framework-compliant issuers; misrepresenting a token as MAS-regulated carries financial penalties or imprisonment and placement on the MAS Investor Alert List. Retail consumer protections prohibit high-risk activities such as lending or staking using stablecoins, and foreign-issued stablecoins remain DPTs under the general regime.",
  requirement_structured={"label_restriction":"'MAS-regulated stablecoin' label limited to SCS-compliant issuers","misrepresentation":"financial penalty / imprisonment; MAS Investor Alert List","retail_protection":"no lending or staking using stablecoins","foreign_tokens":"remain DPTs under general regime"},
  status="in_force", effective_date=None,
  source={"primary":"Payment Services Act 2019 / MAS Single-Currency Stablecoin Regulatory Framework","pinpoint":"Distribution and offering — label restriction; misrepresentation penalties; retail lending/staking prohibition","url":""},
  secondary=[{"citation":MATRIX+", pp.19-20 (Singapore — Distribution and Offering Restrictions)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**SG, id="sg-scs-implementation_status-001", authority="MAS", dimension="implementation_status", constraint_ref=None,
  requirement_summary="The Payment Services Act came into force in January 2020; the SCS framework was finalised on 15 August 2023; the FSMA Part 9 DTSP regime took effect 30 June 2025 with no transitional arrangement; full SCS-framework implementation is targeted for mid-2026.",
  requirement_structured={"psa_in_force":"Jan 2020","scs_finalised":"15 Aug 2023","dtsp_effective":"30 Jun 2025 (no transition)","full_scs_target":"mid-2026"},
  status="transitional", effective_date="2023-08-15",
  source={"primary":"Payment Services Act 2019; MAS SCS framework; FSMA Part 9","pinpoint":"Implementation timeline — PSA 2020; SCS Aug 2023; DTSP Jun 2025; full SCS mid-2026","url":""},
  secondary=[{"citation":MATRIX+", p.20 (Singapore — Implementation Timeline)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="high", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

# ============================== UNITED KINGDOM (uk-frs) ==============================
UK = dict(jurisdiction="UK", instrument_type="fiat_referenced_stablecoin",
          instrument_label_local="UK qualifying stablecoin (UKQS)")

R.append(rec(**UK, id="uk-frs-reserve_backing-001", authority="FCA", dimension="reserve_backing", constraint_ref="C2",
  requirement_summary="SI 2026/102 requires 1:1 backing by a backing-asset pool with annual independent review. Backing assets are carved out from the collective-investment-scheme (CIS) and alternative-investment-fund (AIF) definitions, with the carve-out activated early ahead of full regime commencement; specific backing-asset composition rules are pending final FCA rules.",
  requirement_structured={"backing":"1:1 by backing-asset pool","review":"annual independent review","cis_aif_carveout":"backing assets carved out of CIS/AIF definitions (activated early)","composition":"pending final FCA rules"},
  status="transitional", effective_date="2026-02-01",
  source={"primary":"Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102","pinpoint":"1:1 backing; CIS/AIF carve-out for backing assets","url":""},
  secondary=[{"citation":MATRIX+", pp.14-15 (United Kingdom — Reserve and Backing Requirements)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. The early CIS/AIF carve-out is the closest structural mirror among the six jurisdictions to US 1940-Act treatment of tokenised MMFs (enables 1940-Act-equivalent routing).",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**UK, id="uk-frs-capital_requirements-001", authority="FCA; Bank of England", dimension="capital_requirements", constraint_ref="C2",
  requirement_summary="The prudential regime for qualifying stablecoin issuers sits under FCA Consultation Paper CP25/15, with final requirements pending. The Bank of England separately addresses prudential standards for systemic sterling-denominated stablecoins, with revised proposals published 10 November 2025.",
  requirement_structured={"non_systemic":"FCA CP25/15 prudential regime — final rules pending","systemic":"Bank of England regime for systemic GBP stablecoins (revised proposals 10 Nov 2025)"},
  status="proposed", effective_date=None,
  source={"primary":"FCA Consultation Paper CP25/15; Bank of England systemic stablecoin proposals (10 Nov 2025)","pinpoint":"Prudential regime — FCA CP25/15 (pending); BoE systemic regime","url":""},
  secondary=[{"citation":MATRIX+", p.14 (United Kingdom — Capital Requirements)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. Final FCA prudential requirements are not yet published — confidence is held low/medium accordingly.",
  confidence="low", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**UK, id="uk-frs-redemption-001", authority="FCA", dimension="redemption", constraint_ref=None,
  requirement_summary="Redemption follows an issuer-controlled process within a backing-asset trust structure: third parties holding backing assets do so on trust for the benefit of stablecoin holders. Specific redemption mechanics are pending final FCA rules.",
  requirement_structured={"process":"issuer-controlled","trust":"backing assets held on trust for holders","mechanics":"pending final FCA rules"},
  status="proposed", effective_date=None,
  source={"primary":"FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102","pinpoint":"Redemption — issuer-controlled; backing-asset trust structure","url":""},
  secondary=[{"citation":MATRIX+", p.15 (United Kingdom — Redemption Mechanics)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="low", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**UK, id="uk-frs-custody-001", authority="FCA", dimension="custody", constraint_ref="C2",
  requirement_summary="Any firm holding client crypto-assets for more than 24 hours, or with the ability to override client authority, is a regulated custodian requiring a safeguarding licence. This 24-hour custody rule has significant operational implications for wallet operators with UK user exposure.",
  requirement_structured={"trigger":"holding client crypto-assets > 24 hours, or ability to override client authority","consequence":"regulated custodian; safeguarding licence required","impact":"wallet operators with UK user exposure"},
  status="transitional", effective_date="2026-02-01",
  source={"primary":"FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; FCA CP25/14","pinpoint":"Custody — 24-hour rule; safeguarding licence for regulated custodians","url":""},
  secondary=[{"citation":MATRIX+", p.15 (United Kingdom — Distribution and Offering Restrictions; custody rule)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. This is the first record on the custody dimension; the 24-hour test is the operative custody trigger.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill","new_dimension"]))

R.append(rec(**UK, id="uk-frs-aml_kyc-001", authority="FCA", dimension="aml_kyc", constraint_ref=None,
  requirement_summary="The cryptoassets regime supersedes the previous Money Laundering Regulations registration regime by bringing cryptoasset activities into full FSMA scope, including AML/KYC obligations; the existing Money Laundering Regulations 2017 continue to apply alongside.",
  requirement_structured={"change":"cryptoassets brought into full FSMA scope (AML/KYC)","supersedes":"previous MLR money-laundering registration regime","alongside":"Money Laundering Regulations 2017 still apply"},
  status="transitional", effective_date="2026-02-01",
  source={"primary":"FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; Money Laundering Regulations 2017","pinpoint":"AML/KYC — full FSMA scope; MLR registration regime superseded","url":""},
  secondary=[{"citation":MATRIX+", p.15 (United Kingdom — AML / KYC Framework)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**UK, id="uk-frs-cross_border_data-001", authority="ICO", dimension="cross_border_data", constraint_ref="C6",
  requirement_summary="UK GDPR applies (effectively mirroring EU GDPR post-Brexit). Cross-border data transfers to non-UK jurisdictions require an adequacy decision, an International Data Transfer Agreement (IDTA), or the UK Addendum to the EU Standard Contractual Clauses.",
  requirement_structured={"regime":"UK GDPR (mirrors EU GDPR)","transfer_gates":["adequacy decision","International Data Transfer Agreement (IDTA)","UK Addendum to EU SCCs"]},
  status="in_force", effective_date=None,
  source={"primary":"UK GDPR (Data Protection Act 2018)","pinpoint":"Cross-border transfer — adequacy / IDTA / UK Addendum to EU SCCs","url":""},
  secondary=[{"citation":MATRIX+", p.15 (United Kingdom — Cross-Border Data Treatment)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**UK, id="uk-frs-distribution-001", authority="FCA; HM Treasury", dimension="distribution", constraint_ref="C8",
  requirement_summary="Offshore firms 'involved' in a sale of a cryptoasset to a UK consumer are within territorial scope. UKQS transactions (in UKQS only) are carved out from the financial-promotions regime, except for lending and borrowing arrangements. HM Treasury's 21 April 2026 draft amendment SI signals intent to bring stablecoin payments using UKQS-authorised firms into regulated payment services (consultation closed 22 May 2026).",
  requirement_structured={"territorial":"offshore firms 'involved' in a sale to a UK consumer are in scope","fin_promo_carveout":"UKQS-only transactions carved out, except lending/borrowing","payments_proposal":"HM Treasury 21 Apr 2026 amendment SI — UKQS payments into regulated payment services"},
  status="proposed", effective_date=None,
  source={"primary":"FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; HM Treasury draft amendment SI (21 Apr 2026)","pinpoint":"Distribution — offshore 'involved' test; UKQS financial-promotions carve-out; payments amendment","url":""},
  secondary=[{"citation":MATRIX+", p.15 (United Kingdom — Distribution and Offering Restrictions)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**UK, id="uk-frs-implementation_status-001", authority="FCA; Bank of England; HM Treasury", dimension="implementation_status", constraint_ref=None,
  requirement_summary="SI 2026/102 was published February 2026 and is in force; the Bank of England published revised systemic-stablecoin proposals on 10 November 2025; HM Treasury published a draft amendment SI on 21 April 2026; final FCA policy statements are expected summer 2026, perimeter guidance September 2026, and the full crypto regime takes effect late 2027.",
  requirement_structured={"si_published":"Feb 2026 (in force)","boe_proposals":"10 Nov 2025","hmt_amendment":"21 Apr 2026","fca_final":"summer 2026","perimeter_guidance":"Sep 2026","full_regime":"late 2027"},
  status="transitional", effective_date="2026-02-01",
  source={"primary":"SI 2026/102; FCA CP25/14 & CP25/15; Bank of England proposals; HM Treasury amendment SI","pinpoint":"Implementation timeline — SI in force Feb 2026; FCA final summer 2026; full regime late 2027","url":""},
  secondary=[{"citation":MATRIX+", pp.16-17 (United Kingdom — Implementation Timeline)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. The regime is mid-transition: a published SI but pending final FCA rules.",
  confidence="high", last_reviewed=REVIEWED, version_added=VER, tags=["europe","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

# ============================== MAINLAND CHINA (cn-prc) ==============================
CN = dict(jurisdiction="CN", instrument_type="other")

R.append(rec(**CN, id="cn-prc-reserve_backing-001", authority="PBOC; SAFE; CSRC", instrument_label_local="无境内发行 (no domestic issuance); indirect HK pathway",
  dimension="reserve_backing", constraint_ref="C2",
  requirement_summary="Reserve requirements are not applicable to domestic issuance, which is prohibited. On the indirect pathway through Hong Kong, HKMA reserve requirements apply to the HK-licensed entity; the PRC-connected parent holds no reserve obligation directly under PRC law but faces consolidation treatment under A-share listing rules.",
  requirement_structured={"domestic":"not applicable (issuance prohibited)","indirect_hk":"HKMA reserve rules apply to HK entity","prc_parent":"no direct reserve obligation; A-share consolidation treatment"},
  status="in_force", effective_date=None,
  source={"primary":"PRC prohibition on domestic issuance; HKMA reserve rules apply to HK-licensed entity (indirect pathway)","pinpoint":"Reserve — N/A domestically; indirect HK pathway + A-share consolidation","url":""},
  secondary=[{"citation":MATRIX+", p.25 (Mainland China — Reserve and Backing Requirements)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. Recorded because the 'N/A domestically + indirect HK consolidation' structure is itself the analytically relevant fact for PRC-connected groups.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill","indirect_pathway"]))

R.append(rec(**CN, id="cn-prc-capital_requirements-001", authority="PBOC; SAFE; CSRC", instrument_label_local="无境内发行 (no domestic issuance); indirect HK pathway",
  dimension="capital_requirements", constraint_ref="C2",
  requirement_summary="Capital requirements are not applicable to domestic issuance. On the indirect Hong Kong pathway, the HKMA HK$25 million paid-up share capital applies to the HK-licensed entity; for PRC-listed parents, capital injected into the HK subsidiary is subject to SAFE outbound-investment registration and consolidates into the parent's financial statements under the Accounting Standards for Business Enterprises.",
  requirement_structured={"domestic":"not applicable","indirect_hk_capital":"HKMA HK$25m paid-up on HK entity","safe":"capital injection subject to SAFE outbound-investment registration","consolidation":"into parent statements under Accounting Standards for Business Enterprises"},
  status="in_force", effective_date=None,
  source={"primary":"HKMA capital rules (HK entity); SAFE outbound-investment registration; Accounting Standards for Business Enterprises","pinpoint":"Capital — N/A domestically; indirect HK HK$25m + SAFE registration + consolidation","url":""},
  secondary=[{"citation":MATRIX+", p.25 (Mainland China — Capital Requirements)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. The SAFE outbound-capital and consolidation layers are the operative PRC-law constraints on the indirect pathway.",
  confidence="medium", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill","indirect_pathway"]))

R.append(rec(**CN, id="cn-prc-aml_kyc-001", authority="PBOC", instrument_label_local="反洗钱 (AML)",
  dimension="aml_kyc", constraint_ref=None,
  requirement_summary="The Anti-Money Laundering Law of the PRC and PBOC AML/CFT regulations apply to all financial institutions, and cryptocurrency-related transactions are explicitly subject to AML scrutiny under the 2017 ICO Notice (94 公告) and supporting circulars.",
  requirement_structured={"statute":"Anti-Money Laundering Law of the PRC","regulator_rules":"PBOC AML/CFT regulations (all financial institutions)","crypto":"explicit AML scrutiny under 94 公告 and supporting circulars"},
  status="in_force", effective_date=None,
  source={"primary":"Anti-Money Laundering Law of the PRC; PBOC AML/CFT regulations; 2017 ICO Notice (94 公告)","pinpoint":"AML — PRC AML Law; PBOC AML/CFT; crypto AML scrutiny under 94 公告","url":""},
  secondary=[{"citation":MATRIX+", p.26 (Mainland China — AML / KYC Framework)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification.",
  confidence="high", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

R.append(rec(**CN, id="cn-prc-implementation_status-001", authority="PBOC; CAC; CSRC; SAFE", instrument_label_local="稳定禁止 (stable prohibition)",
  dimension="implementation_status", constraint_ref=None,
  requirement_summary="The regime is a stable prohibition with no scheduled formal rule change. Key milestones: the 2017 ICO ban (94 公告); the Data Security Law (1 Sep 2021); the reaffirmed comprehensive prohibition extended to offshore exchanges (24 Sep 2021); PIPL (1 Nov 2021); the 22 March 2024 cross-border data Provisions; the 2025 Hong Kong application window in which PRC-connected groups (Ant, JD, and state-owned banks) applied or expressed interest; and the 10 April 2026 HK first-license cohort, which excluded all PRC-connected applicants, private and state alike.",
  requirement_structured={"2017":"ICO ban (94 公告)","2021_dsl":"Data Security Law (1 Sep)","2021_prohibition":"comprehensive prohibition reaffirmed (24 Sep)","2021_pipl":"PIPL (1 Nov)","2024":"cross-border data Provisions (22 Mar)","2025":"HK application window; Oct 2025 PBOC/CAC guidance; Ant/JD suspend","2026":"10 Apr HK first cohort excludes all PRC-connected applicants"},
  status="in_force", effective_date="2021-09-24",
  source={"primary":"94 公告 (2017); DSL (2021); PIPL (2021); 2024 cross-border data Provisions; HKMA April 2026 first-license cohort","pinpoint":"Implementation timeline — stable prohibition; 2017-2026 milestones","url":""},
  secondary=[{"citation":MATRIX+", pp.27-28 (Mainland China — Implementation Timeline)"}],
  interpretation_note="Provenance: transcribed from author's Compliance Matrix v0.9.3; pending primary-source verification. The April 2026 cohort's exclusion of both private (Ant, JD) and state-owned (BOCHK, ICBC Asia, BOCom HK, CCB Asia, PetroChina) applicants is the operative evidence of the private/state boundary the PBOC polices.",
  confidence="high", last_reviewed=REVIEWED, version_added=VER, tags=["apac","focus","from_matrix_v0.9.3","v0.3.0_backfill"]))

# ---- emit ----
written = 0
for r in R:
    path = ROOT / (r["id"] + ".yaml")
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(r, f, sort_keys=False, allow_unicode=True, width=100, default_flow_style=False)
    written += 1
print(f"wrote {written} backfill records (SG/UK/CN, v0.3.0)")
