#!/usr/bin/env python3
"""
apply_verification.py — land the external primary-source verification pass (v0.9.5) onto the register.

The external artifact (web retrieval against official sources, 2026-06-27) located the official instrument
+ URL for each original-seven-jurisdiction cell and reported, per cell, whether the proposition is
confirmed against the official text AND the BINDING STATUS of the instrument it rests on.

DISCIPLINE (the deep-review correction): the verification's own central finding is that a blanket
promotion to resolution_text is WRONG. Citability is capped by binding status, independent of whether
the text was located:

  in_force_enacted          -> resolution_text-eligible (enacted statute, in force now)
  made_not_commenced        -> NOT in-force law (UK SI 2026/102, commences 2027-10-25)      -> firm_summary
  finalized_policy_pending  -> finalized policy, not enacted (SG MAS SCS framework)         -> firm_summary
  pending_proposal          -> bill / NPRM / consultation (US CLARITY, OCC NPRM, BR BCB)     -> firm_summary
  prohibition / no_regime   -> no positive permitted-activity rule to confirm (CN)           -> stays unset

So this promotes ONLY in_force_enacted cells confirmed against official text (EU MiCA, US GENIUS
statutory parts, HK Cap. 656), attaches the official URL + a `verification` block, and records
binding_status on every record (explicit dispositions below, status-based fallback elsewhere). It NEVER
fabricates a URL or a confirmation. Idempotent; patches YAML in place; emits the ledger audit trail.
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import json, datetime, collections, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERIFIED_ON = "2026-06-27"
VERIFIED_BY = "external review (web retrieval against official sources)"
SENT = "\n\n[v0.9.5 verification] "

CLUSTERS = {
 "EU": {"instrument":"MiCA — Regulation (EU) 2023/1114","binding_status":"in_force_enacted",
        "official_url":"https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng",
        "note":"Fully applicable 30 Dec 2024; Titles III/IV (ARTs/EMTs) from 30 Jun 2024."},
 "US": {"instrument":"GENIUS Act (Pub. L., signed 18 Jul 2025); OCC/FDIC NPRMs + CLARITY Act (H.R.3633) pending",
        "binding_status":"mixed","official_url":"https://www.congress.gov/bill/119th-congress/senate-bill/1582/text",
        "note":"GENIUS enacted and in force; the OCC/FDIC NPRMs and CLARITY Act are pending and NOT law."},
 "UK": {"instrument":"FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; FCA CP25/14, CP25/15",
        "binding_status":"made_not_commenced","official_url":"https://www.legislation.gov.uk/uksi/2026/102/contents/made",
        "note":"SI 2026/102 made 4 Feb 2026; FULL COMMENCEMENT 25 Oct 2027. Not in-force law yet."},
 "HK": {"instrument":"Stablecoins Ordinance (Cap. 656) + HKMA Guidelines","binding_status":"in_force_enacted",
        "official_url":"https://www.elegislation.gov.hk/hk/cap656",
        "note":"Gazetted commencement 1 Aug 2025; s.8(1) licensing offence in force."},
 "SG": {"instrument":"Payment Services Act 2019 (enacted) + MAS Single-Currency Stablecoin Framework (finalized policy, pending legislation)",
        "binding_status":"split","official_url":"https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework",
        "note":"PS Act 2019 (DPT licensing, AML/travel-rule) in force; SCS-specific framework is finalized MAS policy still awaiting implementing legislation (expected mid-2026)."},
 "CN": {"instrument":"94 Notice (2017); 24 Sep 2021 Notice; PIPL; DSL; CAC 2024 Provisions","binding_status":"prohibition",
        "official_url":None,
        "note":"Prohibition/data statutes in force, but they establish a PROHIBITION; no affirmative permitted-issuer rule to confirm. Original-language text not line-verified."},
 "BR": {"instrument":"Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); BCB rulemaking pending","binding_status":"in_force_enacted",
        "official_url":"https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm",
        "note":"Lei 14.478 enacted framework law; specific yield/operational rules rest on not-yet-issued BCB rulemaking. Original-language text not line-verified."},
 "TW": {"instrument":"VASP AML registration (in force 30 Nov 2024); Virtual Asset Service Act (bill)","binding_status":"split",
        "official_url":None,"note":"AML registration in force; VAS Act is a draft bill. Original-language text not line-verified."},
 "KR": {"instrument":"Virtual Asset User Protection Act (in force 19 Jul 2024); Digital Asset Basic Act (bill)","binding_status":"split",
        "official_url":None,"note":"VAUPA in force; DABA is a draft bill. Original-language text not line-verified."},
}
EUR=CLUSTERS["EU"]["official_url"]; USC=CLUSTERS["US"]["official_url"]
USR="https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation"
UKS=CLUSTERS["UK"]["official_url"]; HKC=CLUSTERS["HK"]["official_url"]
SGM=CLUSTERS["SG"]["official_url"]; BRL=CLUSTERS["BR"]["official_url"]

D = collections.OrderedDict()

# ---- EU ----
D["eu-emt-permitted_activity_yield-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",url=EUR,
  pinpoint="Art. 50 (no interest paid to EMT holders)",verdict="confirmed",
  note="Confirmed against the official MiCA text: Art. 50 prohibits interest to EMT holders.")
D["eu-emt-monetary_sovereignty-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",url=EUR,
  primary="Regulation (EU) 2023/1114 (MiCA), Art. 58(3) (applying the Art. 23 means-of-exchange thresholds to non-EU-currency EMTs)",
  summary=("For a non-EU-currency EMT, MiCA caps usage as a means of exchange at EUR 200 million per day or "
           "1 million transactions per day (the Article 23 thresholds, applied to significant EMTs via Article "
           "58(3)), measured on a quarterly-average basis. The cap applies only to use as a means of exchange "
           "within a single currency area, not to store-of-value use or to trading on crypto-asset venues. A "
           "separate reporting obligation triggers at EUR 100 million in issuance value globally. This is the "
           "canonical quantitative monetary-sovereignty cap and the clearest instance of Constraint 7."),
  pinpoint="Art. 58(3) (applying Art. 23 mutatis mutandis to non-EU-currency EMTs)",verdict="confirmed_with_refinement",
  note=("LABEL RECONCILED: the operative pinpoint, the requirement summary, and source.primary now all read "
        "Art. 58(3) (which applies the Art. 23 thresholds mutatis mutandis to non-EU-currency EMTs); the "
        "summary and primary previously read bare 'Article 23'. SIGNALS and the corridor records already cite "
        "Art. 58(3), so this reconciles the cell across all three fields."))
D["eu-emt-regulatory_authority-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",url=EUR,
  pinpoint="Titles III/IV; EBA/ESMA/NCA supervisory architecture",verdict="confirmed",
  note="Confirmed: MiCA Titles III/IV and the EBA/ESMA/NCA architecture.")
D["eu-emt-reserve_backing-001"]=dict(binding_status="in_force_enacted",tier="firm_summary",url=EUR,
  pinpoint="reserve composition set in MiCA + Level-2 RTS; deposit-% pinpoint pending RTS line-read",verdict="not_line_verified",
  note="HELD at firm_summary: MiCA is in force, but the deposit-percentage figures (EMT >=60% / ART >=30% bank deposits) are set in the Level-2 RTS and were NOT line-verified against the article text in this pass.")

# ---- US (GENIUS enacted; NPRM/CLARITY pending) ----
D["us-pss-permitted_activity_yield-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",status="in_force",url=USR,
  pinpoint="GENIUS Act Sec. 4(a)(11) (no interest/yield in connection with holding, use, or retention)",verdict="confirmed",
  note=("Confirmed: the Federal Register implementation notice quotes Sec. 4(a)(11) verbatim and matches the cell "
        "pinpoint. GENIUS is enacted and in force (status corrected proposed->in_force). LIVE DEVELOPMENT "
        "(Jun 2026): the Senate Banking Committee's CLARITY substitute (advanced 15-9 on 14 May 2026; placed on "
        "the Senate Legislative Calendar as Calendar No. 423 on 1 Jun 2026) carries the Tillis-Alsobrooks "
        "stablecoin-yield compromise, which prohibits digital-asset service providers from offering interest or "
        "yield for merely holding a stablecoin balance but allows stablecoin rewards and activity-linked "
        "incentives. That is the intermediary-layer (CLARITY Sec. 404) extension of the GENIUS issuer-level "
        "prohibition, and it supports this cell's standing position that user-initiated, activity-linked routing "
        "falls outside the holding prohibition. It is not yet law: the bill still needs Senate floor passage, "
        "reconciliation with the Senate Agriculture and House versions, and signature (see the contingent "
        "us-clarity-act-enacted event in the time engine)."))
D["us-pss-securities_classification-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",status="in_force",url=USC,
  pinpoint="GENIUS Act securities carve-out (amending the '33/'34 Acts and ICA40 for permitted payment stablecoins)",verdict="confirmed_carveout",
  flag="CLARITY market-structure overlay is pending (H.R.3633, House-passed) and is NOT part of this citable carve-out.",
  note="Confirmed: GENIUS carves permitted-issuer payment stablecoins out of the securities laws (enacted). The Reves analysis is common-law backdrop; the CLARITY provisions are a pending bill, excluded. Status corrected proposed->in_force.")
D["us-pss-reserve_backing-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",status="in_force",url=USC,
  primary="GENIUS Act Sec. 4(a)(1) (1:1 fair-value reserve backing)",
  pinpoint="GENIUS Act Sec. 4(a)(1) (1:1 fair-value backing of outstanding payment stablecoins)",
  summary="1:1 backing of outstanding payment stablecoins at fair value is required by the enacted GENIUS Act (Sec. 4(a)(1)). The detailed list of PERMISSIBLE reserve assets is set by the OCC NPRM (proposed 12 CFR Sec. 15.11(b)) and is NOT yet final — that composition is a pending overlay, not part of the in-force statutory proposition.",
  verdict="confirmed_statute_only",
  flag="Permissible-asset composition (proposed 12 CFR Sec. 15.11(b)) is an OCC NPRM (pending), not final law.",
  note="SPLIT per verification: the citable proposition is the enacted 1:1 backing (Sec. 4(a)(1)); the 12 CFR Sec. 15.11(b) permissible-asset detail is an OCC NPRM (proposed), moved out of the citation into a flagged pending overlay. Status corrected proposed->in_force for the 1:1.")
D["us-pss-issuer_pathway-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",url=USC,
  pinpoint="GENIUS Act Sec. 3-4 (permitted payment stablecoin issuers: IDI subsidiaries; OCC-qualified non-banks; certified state regimes)",verdict="confirmed_genius_part",
  flag="CLARITY Act Sec. 404 covered-party definition is a House-passed bill (H.R.3633), NOT law; excluded from the citable proposition.",
  note="Confirmed: GENIUS issuer eligibility (Sec. 3-4) is enacted. The cell's CLARITY Sec. 404 reference is a pending House bill, flagged out of the citable proposition.")
D["us-pss-capital_requirements-001"]=dict(binding_status="pending_proposal",tier="firm_summary",url=USR,
  pinpoint="capital left to OCC/FDIC rulemaking; figures from the OCC/FDIC NPRM (proposed)",verdict="rests_on_proposed_rule",
  note="HELD below resolution_text: GENIUS leaves capital to rulemaking; the figures (min greater of $5m or chartering amount) come from the OCC/FDIC NPRM (proposed), not final law.")
D["us-pss-bank_nonbank_routing-001"]=dict(binding_status="pending_proposal",tier="firm_summary",
  pinpoint="CLARITY Act Sec. 404 covered-party definition (H.R.3633, House-passed, not enacted)",verdict="rests_on_pending_bill",
  note="HELD below resolution_text: bank/non-bank routing rests on the CLARITY Act, a House-passed bill, not enacted law.")
D["us-pss-monetary_sovereignty-001"]=dict(binding_status="in_force_enacted",
  note="GENIUS framework (no non-USD usage cap); binding status recorded; not separately line-verified in this pass.")
D["us-pss-cross_border_data-001"]=dict(binding_status="in_force_enacted",
  note="US data/AML framework in force; binding status recorded; not separately line-verified.")
D["us-pss-disclosure_reporting-001"]=dict(binding_status="in_force_enacted",
  note="GENIUS disclosure/reporting framework; binding status recorded; not separately line-verified.")

# ---- UK (SI 2026/102 made-not-commenced; FCA rules pending) -> none reaches resolution_text ----
D["uk-frs-issuer_pathway-001"]=dict(binding_status="made_not_commenced",tier="firm_summary",status="transitional",url=UKS,
  pinpoint="reg 9M(2) (issuing a qualifying stablecoin; all three limbs) vs HMT policy note (any one limb)",verdict="confirmed_instrument_interpretive_tension_real",
  note="HELD below resolution_text: SI 2026/102 reg 9M is real and confirmed and the three-limbs-vs-one-limb tension is genuine, BUT the regime is NOT yet operative — full commencement 25 Oct 2027. Made law, not yet in force. Status corrected in_force->transitional.")
D["uk-frs-regulatory_authority-001"]=dict(binding_status="made_not_commenced",tier="firm_summary",status="transitional",url=UKS,
  pinpoint="FCA/BoE supervisory architecture under FSMA 2000 (as amended by SI 2026/102)",verdict="made_not_in_force",
  note="HELD below resolution_text: the supervisory architecture is established by SI 2026/102, which is made but commences 25 Oct 2027. Backing record for the scheduled UK commencement event.")
D["uk-frs-reserve_backing-001"]=dict(binding_status="made_not_commenced",url=UKS,
  note="Reserve/backing under SI 2026/102 + FCA rules; made-not-commenced (operative 2027-10-25); held below resolution_text.")
D["uk-frs-custody-001"]=dict(binding_status="made_not_commenced",url=UKS,
  note="Custody under SI 2026/102 + FCA rules; made-not-commenced; held below resolution_text.")
D["uk-frs-redemption-001"]=dict(binding_status="made_not_commenced",url=UKS,
  note="Redemption rules; made-not-commenced (operative 2027-10-25); held below resolution_text.")
D["uk-frs-capital_requirements-001"]=dict(binding_status="pending_proposal",
  note="Prudential/capital detail rests on FCA CP25/14 / CP25/15 consultations (final rules expected summer 2026); pending.")
D["uk-frs-permitted_activity_yield-001"]=dict(binding_status="pending_proposal",
  note="Yield/distribution treatment rests on FCA consultation; pending.")
D["uk-frs-distribution-001"]=dict(binding_status="pending_proposal",
  note="Distribution rules rest on FCA consultation; pending.")
D["uk-frs-cross_border_data-001"]=dict(binding_status="made_not_commenced",url=UKS,
  note="Cross-border/data under the FSMA 2026 perimeter; made-not-commenced.")
D["uk-frs-aml_kyc-001"]=dict(binding_status="in_force_enacted",
  note="MLRs 2017 AML baseline IS in force (distinct from the not-yet-commenced FSMA 2026 stablecoin regime); binding status recorded.")
D["uk-frs-securities_classification-001"]=dict(binding_status="made_not_commenced",
  note="Securities/RAO treatment under the FSMA 2026 perimeter; made-not-commenced.")
D["uk-frs-bank_nonbank_routing-001"]=dict(binding_status="made_not_commenced",
  note="Bank/non-bank routing under the FSMA 2026 perimeter; made-not-commenced.")
D["uk-frs-monetary_sovereignty-001"]=dict(binding_status="made_not_commenced",
  note="Monetary-sovereignty treatment under the FSMA 2026 perimeter; made-not-commenced (the time engine owns the 2027-10-25 flip).")

# ---- HK (Cap. 656 in force, enacted) -> statutory cells the verification confirmed -> resolution_text ----
def hk(pin, note=None, flag=None, verdict="confirmed", tier="resolution_text"):
    e=dict(binding_status="in_force_enacted",tier=tier,url=HKC,pinpoint=pin,verdict=verdict)
    if note: e["note"]=note
    if flag: e["flag"]=flag
    return e
D["hk-frs-permitted_activity_yield-001"]=hk("Sch. 2 s.15 (no interest on issued stablecoins)",
  note="Confirmed against the Ordinance: Sch. 2 s.15 prohibits interest on issued stablecoins.")
D["hk-frs-reserve_backing-001"]=hk("100% backing; same-currency reserve with HKD/USD exception; segregation/trust",
  note="Confirmed: statutory 100% backing + trust/segregation; the HKD-can-be-USD exception is confirmed.",
  flag="Granular eligible-asset list is in the HKMA Guideline (guidance), not the Ordinance.")
D["hk-frs-redemption-001"]=hk("par redemption within 1 business day",note="Confirmed: par redemption within one business day.")
D["hk-frs-capital_requirements-001"]=hk("HK$25m paid-up capital (statutory)",
  note="Confirmed for the statutory HK$25m paid-up minimum. The HK$3m liquid-asset and 12-month-opex figures are HKMA Guideline detail (guidance).",
  flag="HK$3m liquid-asset + 12-month-opex requirements are HKMA Guideline detail (guidance), not the Ordinance.")
D["hk-frs-monetary_sovereignty-001"]=hk("offshore HKD-referencing issuance is licensable; non-HKD FRS offering limited",
  note="Confirmed: offshore HKD-referencing issuance is licensable; non-HKD FRS offering is limited.")
D["hk-frs-issuer_pathway-001"]=hk("licensable regulated activities; s.8(1) licensing offence",
  note="Confirmed: the licensable-activities perimeter and the s.8(1) licensing offence.")
D["hk-frs-regulatory_authority-001"]=hk("HKMA as the licensing/supervisory authority",note="Confirmed: HKMA authority under the Ordinance.")
D["hk-frs-distribution-001"]=hk("permitted-offeror closed loop; HK$5m / 7-year offence",
  note="Confirmed: the permitted-offeror closed loop and the HK$5m / 7-year distribution offence.")
D["hk-frs-aml_kyc-001"]=dict(binding_status="in_force_enacted",tier="firm_summary",url=HKC,
  pinpoint="AMLO + Ordinance AML obligations on licensees",
  note="PROMOTED to firm_summary: HK AML obligations rest on the AMLO + the Ordinance (in force); not separately line-verified to the AML pinpoint in this pass.")
D["hk-frs-cross_border_data-001"]=dict(binding_status="in_force_enacted",tier="firm_summary",url=HKC,
  pinpoint="PDPO (Cap. 486) data obligations; HKMA outsourcing/data guidance",
  note="PROMOTED to firm_summary: HK data obligations rest on the PDPO (in force); not separately line-verified.")
D["hk-frs-securities_classification-001"]=dict(binding_status="in_force_enacted",
  note="HK securities classification (SFO backdrop); binding status recorded; remains firm_summary.")
D["hk-frs-bank_nonbank_routing-001"]=dict(binding_status="in_force_enacted",
  note="HK bank/non-bank routing under the Ordinance; binding status recorded; remains firm_summary.")
D["hk-frs-disclosure_reporting-001"]=dict(binding_status="in_force_enacted",
  note="HK disclosure/reporting under the Ordinance + HKMA Guideline; binding status recorded; remains firm_summary.")

# ---- SG (PS Act baseline in force; SCS-specific cells = finalized policy pending) ----
# CAREFUL: do NOT set issuer_pathway to 'proposed' (would mis-flip SG to pre_regime). PS Act DPT is the
# in-force baseline; only the SCS-SPECIFIC requirement cells become finalized_policy_pending.
D["sg-scs-aml_kyc-001"]=dict(binding_status="in_force_enacted",tier="firm_summary",
  pinpoint="PS Act 2019 DPT licensing; MAS Notices PSN02/PSN03 (AML/CFT, travel rule)",verdict="confirmed_in_force_baseline",
  note="PROMOTED to firm_summary: the PS Act 2019 DPT AML baseline IS in force (resolution_text-eligible per the verification), held at firm_summary pending capture of the official PS Act text URL.")
D["sg-scs-regulatory_authority-001"]=dict(binding_status="in_force_enacted",tier="firm_summary",
  pinpoint="MAS authority under the Payment Services Act 2019",verdict="confirmed_in_force_baseline",
  note="PROMOTED to firm_summary: MAS authority under the PS Act 2019 is in force; held at firm_summary pending capture of the official PS Act text URL.")
def sg_scs(pin):
    return dict(binding_status="finalized_policy_pending",tier="firm_summary",status="transitional",url=SGM,
      pinpoint=pin,verdict="rests_on_finalized_policy_not_statute",
      note="HELD below resolution_text and status corrected to transitional: an SCS-FRAMEWORK requirement (finalized MAS policy, 15 Aug 2023) whose implementing legislation is still being drafted (expected mid-2026) — finalized policy, not enacted statute.")
D["sg-scs-reserve_backing-001"]=sg_scs("SCS framework: 100% reserve in low-risk assets")
D["sg-scs-redemption-001"]=sg_scs("SCS framework: redemption at par within 5 business days")
D["sg-scs-permitted_activity_yield-001"]=sg_scs("SCS framework: no lending/staking by SCS issuers; SGD/G10 label scope")
D["sg-scs-securities_classification-001"]=sg_scs("SCS framework: 'MAS-regulated stablecoin' label vs DPT classification")
D["sg-scs-capital_requirements-001"]=sg_scs("SCS framework: base capital and liquid-asset requirements")
D["sg-scs-distribution-001"]=sg_scs("SCS framework: label/disclosure on distribution")
D["sg-scs-monetary_sovereignty-001"]=dict(binding_status="finalized_policy_pending",tier="firm_summary",status="transitional",url=SGM,
  pinpoint="SCS framework: SGD/G10 label scope; foreign-pegged tokens treated as ordinary DPTs",verdict="rests_on_finalized_policy_not_statute",
  flag="The no-aggregate-cap posture follows from in-force PS Act DPT treatment; the SCS SGD/G10 LABEL scope is finalized-policy-pending.",
  note="Status corrected to transitional: the SGD/G10 SCS-label scope is part of the finalized-policy-pending SCS framework. The underlying 'foreign-pegged tokens circulate as ordinary DPTs / no aggregate cap' posture is PS-Act baseline (in force), noted in the flag.")
D["sg-scs-issuer_pathway-001"]=dict(binding_status="finalized_policy_pending",
  note="The SCS issuer scope is finalized-policy-pending, BUT the operative DPT licensing pathway under the PS Act 2019 is in force (status left transitional, NOT proposed — SG is a live regime, not pre-regime).")
D["sg-scs-implementation_status-001"]=dict(binding_status="finalized_policy_pending",
  note="SCS framework implementation pending legislation (expected mid-2026); operational record.")
D["sg-scs-cross_border_data-001"]=dict(binding_status="in_force_enacted",
  note="SG cross-border data (PDPA) baseline in force; binding status recorded.")
D["sg-scs-bank_nonbank_routing-001"]=dict(binding_status="in_force_enacted",
  note="SG bank/non-bank routing under the PS Act baseline; binding status recorded.")

# ---- CN (prohibition / absence of affirmative regime) -> stays unset ----
for cell,bs in [("issuer_pathway","prohibition"),("regulatory_authority","prohibition"),
                ("capital_requirements","prohibition"),("reserve_backing","prohibition"),
                ("permitted_activity_yield","prohibition"),("securities_classification","prohibition"),
                ("distribution","prohibition"),("monetary_sovereignty","prohibition"),
                ("bank_nonbank_routing","prohibition"),("cross_border_data","in_force_enacted"),
                ("aml_kyc","in_force_enacted"),("implementation_status","no_regime")]:
    nid=f"cn-prc-{cell}-001"
    if bs=="prohibition":
        D[nid]=dict(binding_status="prohibition",
          note="Prohibition/absence-of-regime cell: the 2017/2021 Notices establish a prohibition; there is no affirmative permitted-activity rule to confirm, so this stays unset (not promotable to resolution_text as a positive proposition).")
    elif bs=="in_force_enacted":
        D[nid]=dict(binding_status="in_force_enacted",
          note="PIPL/DSL/CAC data regime is in force, but the specific outbound-transfer thresholds were NOT line-verified against original-language official text in this pass; kept unset.")
    else:
        D[nid]=dict(binding_status="no_regime",note="No affirmative issuance regime exists in the PRC (operational/absence record).")

# ---- BR (Lei 14.478 enacted framework; yield rests on pending BCB rulemaking) ----
D["br-vasp-permitted_activity_yield-001"]=dict(binding_status="pending_proposal",tier="firm_summary",url=BRL,
  pinpoint="Lei 14.478/2022 framework; specific yield treatment pending BCB implementing rules",verdict="pending_bcb_rulemaking",
  note="PROMOTED to firm_summary with pending_proposal binding: yield treatment rests on not-yet-issued BCB implementing rules, so it stays below resolution_text.")
for cell in ["aml_kyc","regulatory_authority","issuer_pathway","capital_requirements","custody",
             "reserve_backing","securities_classification","cross_border_data","monetary_sovereignty",
             "disclosure_reporting","bank_nonbank_routing"]:
    D[f"br-vasp-{cell}-001"]=dict(binding_status="in_force_enacted",
      note="Lei 14.478/2022 is enacted framework law (binding status recorded); original-language text not line-verified in this pass, so the cell stays firm_summary.")

# ---- TW / KR draft issuer regimes -> pending_proposal (in-force AML/user-protection layer left as verified) ----
D["tw-frs-issuer_pathway-001"]=dict(binding_status="made_not_commenced",
  note="The TW issuer regime rests on the Virtual Asset Service Act, enacted at third reading 30 Jun 2026 but not commenced; status transitional, binding made_not_commenced. The in-force AML-registration layer is recorded separately.")
D["kr-frs-issuer_pathway-001"]=dict(binding_status="pending_proposal",
  note="The KR issuer regime rests on the draft Digital Asset Basic Act (a bill); kept proposed. The in-force VAUPA layer is recorded separately.")

# ====================================================================================================
# v0.9.7 NATIVE-LANGUAGE VERIFICATION PASS (CN Chinese, KR Korean, TW Chinese, BR Portuguese)
# External review against original-language official/authoritative text, 2026-06-27. Applied with the
# same discipline: resolution_text only where binding_status==in_force_enacted AND the proposition is
# confirmed against the official text of the cited instrument; prohibitions stay prohibition.
# ====================================================================================================
NATIVE_ON = "2026-06-27"
# Official BCB normativo URLs (verified to resolve; pattern confirmed in published academic citations)
BCB519="https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=519"
BCB520="https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520"
BCB521="https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=521"
BCB517="https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=517"
CSRC42="https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml"

# Re-point the BR and CN clusters now that the original-language pass has confirmed them.
CLUSTERS["BR"].update(
  instrument="Lei 14.478/2022 + Res BCB 519/520/521 (in force 2 Feb 2026) + Res Conjunta CMN/BCB 14/2025 + Res BCB 517/2025 + Decreto 11.563/2023",
  binding_status="in_force_enacted", official_url=BCB520,
  note="Confirmed against original-language official text (BCB normativos + Lei 14.478). Enacted and in force 2 Feb 2026; Res 521 FX reporting from 4 May 2026.")
CLUSTERS["CN"].update(
  instrument="《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, eff. 6 Feb 2026; repealed 银发〔2021〕237号) + 2017 ICO Notice (94公告) + CSRC 公告〔2026〕1号",
  binding_status="prohibition", official_url=CSRC42,
  note="Confirmed against csrc.gov.cn original-language official text. 42号 (6 Feb 2026) repealed the 2021 Notice and continues the total-prohibition stance, adding a written overseas RMB-pegged-stablecoin issuance ban and RWA rules.")

# ---- BR: in-force BCB regime, confirmed against original-language official text -> resolution_text ----
def br(pin, url=BCB520, summary=None):
    e=dict(binding_status="in_force_enacted",tier="resolution_text",status="in_force",url=url,pinpoint=pin,
           verdict="confirmed_against_official_text")
    if summary: e["summary"]=summary
    e["note"]=("NATIVE-LANGUAGE VERIFICATION (Portuguese): confirmed against the official BCB text. The "
               "Lei 14.478/2022 framework as implemented by Res BCB 519/520/521 (in force 2 Feb 2026) is "
               "enacted law, so this cell is promoted to resolution_text.")
    return e
D["br-vasp-reserve_backing-001"]=br(
  "Res BCB 520/2025 Art. 2, III (reserve assets of a fiat-referenced token = the fiduciary currency and public debt issued by the same governments); Arts. 64+ (asset curation; algorithmic-stablecoin prohibition; proof of reserves)",
  summary=("For a fiat-referenced virtual asset (stablecoin), Res BCB 520/2025 defines the reserve assets as the "
           "fiduciary currency plus public debt issued by the same governments that issue those currencies (Art. 2, III), "
           "requires proof of reserves, and prohibits algorithmic reserve control with public disclosure of the criteria "
           "(Arts. 64+). In force 2 Feb 2026."))
D["br-vasp-custody-001"]=br(
  "Res BCB 520/2025 (patrimonial segregation: client funds in individualised payment/deposit accounts; client virtual assets in segregated wallets; foreign-custodian conditions — home-country authorisation/supervision, Brazil representative, enforceable guarantees, formal segregation of Brazilian clients' assets)")
D["br-vasp-capital_requirements-001"]=br(
  "Resolução Conjunta CMN/BCB nº 14/2025 + Res BCB nº 517/2025 (both 3 Nov 2025): minimum capital R$10,800,000 to R$37,200,000 scaled by the set of activities performed",
  url=BCB517)
D["br-vasp-issuer_pathway-001"]=br(
  "Lei 14.478/2022 (BCB authorisation required to provide virtual-asset services); Res BCB 519/2025 (authorisation process); Res BCB 520/2025 Art. 4 (three SPSAV modalities: intermediária, custodiante, corretora), Art. 14 (sociedade limitada/anônima; ≥3 administrators; head office in Brazil); authorisation deadline 30 Oct 2026 (270 days)",
  url=BCB519)
D["br-vasp-regulatory_authority-001"]=br(
  "Lei 14.478/2022 arts. 2-9; Decreto 11.563/2023 (BCB designated competent authority for virtual-asset services; CVM retains jurisdiction over tokens that are securities)",
  url=BRL)
D["br-vasp-securities_classification-001"]=br(
  "Lei 14.478/2022; Decreto 11.563/2023 (BCB over payment/VASP activity; CVM jurisdiction preserved over tokens with securities characteristics)",
  url=BRL)
D["br-vasp-monetary_sovereignty-001"]=br(
  "Res BCB 521/2025 (amends Res 277/278/279 of 31 Dec 2022): virtual-asset services brought into the FX market — international payments/transfers, stablecoin trades, and payment of expenses abroad treated as câmbio operations; monthly reporting to the BCB from 4 May 2026",
  url=BCB521)
D["br-vasp-aml_kyc-001"]=br(
  "Res BCB 520/2025 (PLD/FTP obligations on SPSAVs; ≥3 responsible administrators including AML/CFT; GAFI Recs 15-16 alignment); Lei 14.478/2022")
D["br-vasp-disclosure_reporting-001"]=br(
  "Res BCB 520/2025 (proof of reserves; periodic audits; transparent information flows); Res BCB 521/2025 (monthly FX-operations reporting from 4 May 2026)")
D["br-vasp-bank_nonbank_routing-001"]=br(
  "Res BCB 520/2025 Art. 20 (besides SPSAVs, only commercial/exchange/investment/multiple banks, Caixa, CTVM/DTVM and FX brokers may provide intermediation/custody, with restrictions); Art. 4 (SPSAV modalities)")
# BR C3 yield: the broad yield-relevant rules are now IN FORCE (Res 520), so this leaves pending_proposal;
# but the specific stablecoin yield pass-through is still unsettled, so it is held at firm_summary.
D["br-vasp-permitted_activity_yield-001"]=dict(binding_status="in_force_enacted",tier="firm_summary",status="in_force",url=BCB520,
  pinpoint="Res BCB 520/2025 (VASPs may not offer credit to clients or raise funds from the public except via share issuance; client virtual assets may not be used for proprietary operations except staking and qualified/professional-investor transactions)",
  note=("NATIVE-LANGUAGE VERIFICATION (Portuguese): binding_status corrected pending_proposal -> in_force_enacted. "
        "Res BCB 520/2025 (in force 2 Feb 2026) confirmed against official text: it prohibits credit offering and "
        "public fundraising except by share issuance and restricts client-asset use to staking / qualified-investor "
        "transactions. Held at firm_summary because the specific stablecoin yield PASS-THROUGH question (whether a "
        "compliant issuer may pass reserve yield to holders) remains unsettled pending further BCB rulemaking."))

# ---- CN: prohibition CONFIRMED; the cited 2021 Notice was REPEALED by 银发〔2026〕42号 (provenance + currency fix) ----
# Substance unchanged (CN stays the prohibition pole). Update the operative-instrument citation; the
# RMB-stablecoin ban is now WRITTEN in-force law, not verbal guidance. Cells stay below resolution_text
# (a prohibition has no positive permitted-activity rule to cite), now at firm_summary on the written text.
D["cn-prc-monetary_sovereignty-001"]=dict(binding_status="prohibition",tier="firm_summary",status="in_force",url=CSRC42,
  primary="《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, eff. 6 Feb 2026; repealed 银发〔2021〕237号); 2017 ICO Notice (94公告)",
  pinpoint="银发〔2026〕42号 — 未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币 (no entity, domestic or overseas, may issue RMB-pegged stablecoins overseas without approval); 境内主体及其控制的境外主体不得在境外发行虚拟货币 (PRC-controlled entities may not issue virtual currencies abroad); RWA tokenisation restrictions",
  summary=("Mainland China occupies the prohibitive pole of the monetary-sovereignty constraint. The eight-ministry "
           "Notice 银发〔2026〕42号 (in force 6 Feb 2026) reaffirms that virtual currencies have no legal-tender status "
           "and adds an explicit WRITTEN prohibition on overseas issuance of RMB-pegged stablecoins without lawful "
           "approval (未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币), plus an extraterritorial ban on PRC-controlled "
           "entities issuing virtual currencies abroad and restrictions on RWA tokenisation."),
  note=("NATIVE-LANGUAGE VERIFICATION (Chinese) — MATERIAL CURRENCY FIX: the previously cited basis ('PBOC October "
        "2025 verbal guidance') is replaced. The RMB-pegged-stablecoin prohibition is now WRITTEN, in-force law: "
        "银发〔2026〕42号 (6 Feb 2026), confirmed against the csrc.gov.cn official text, which also explicitly repealed "
        "the 2021 Notice (银发〔2021〕237号同时废止). Substance unchanged: CN remains the prohibition pole; this is a "
        "provenance + currency correction, not a re-classification."))
D["cn-prc-issuer_pathway-001"]=dict(binding_status="prohibition",tier="firm_summary",status="in_force",url=CSRC42,
  primary="《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026; repealed 银发〔2021〕237号); 2017 ICO Notice (94公告)",
  pinpoint="银发〔2026〕42号 (virtual-currency-related business activities in the PRC are illegal financial activities, strictly prohibited; the prohibited act is upgraded from '代币发行融资' (token-offering financing, 2021) to '发行虚拟货币' (issuing virtual currency), now reaching non-fundraising / airdrop / utility issuance)",
  summary=("There is no domestic stablecoin issuance pathway. The 2017 ICO Notice (94公告) policy continues, and the "
           "2026 Notice (银发〔2026〕42号, which repealed the 2021 Notice) treats token issuance and virtual-currency "
           "business activity as prohibited, upgrading the banned act from token-offering financing to issuing virtual "
           "currency. The live regulatory questions for PRC-connected groups therefore concern the indirect pathway "
           "through Hong Kong and the cross-border data, capital, and disclosure constraints that condition it, not a "
           "domestic licence. The behavioural boundary observed in 2025 tracks a private/state distinction: private "
           "internet groups (Ant, JD) applied for HK licences and then withdrew in October 2025; state-linked banks "
           "expressed interest and paused; and no PRC-affiliated applicant received a licence in the April 2026 first round."),
  note=("NATIVE-LANGUAGE VERIFICATION (Chinese): operative-instrument citation updated to 银发〔2026〕42号, which "
        "repealed the 2021 Notice and broadened the issuance prohibition. No domestic issuance pathway exists; "
        "CN stays the prohibition pole."))
D["cn-prc-regulatory_authority-001"]=dict(binding_status="prohibition",tier="firm_summary",status="in_force",url=CSRC42,
  primary="《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026); issuing bodies: PBOC, NDRC, MIIT, MPS, SAMR, NFRA, CSRC, SAFE, with 中央网信办/最高法/最高检",
  pinpoint="银发〔2026〕42号 (a coordinated multi-agency prohibition perimeter; eight ministries plus the cyberspace administration and the two supreme judicial organs)",
  summary=("No single stablecoin regulator exists because there is no lawful domestic issuance pathway; instead, a "
           "coordinated multi-agency prohibition perimeter governs. The eight-ministry Notice 银发〔2026〕42号 (in force "
           "6 Feb 2026), issued jointly with the Cyberspace Administration and the two supreme judicial organs, sets the "
           "perimeter: the People's Bank of China (PBOC) leads, with the NDRC, MIIT, MPS, SAMR, NFRA, CSRC, and SAFE. The "
           "2026 Notice put the prohibition on private RMB-pegged stablecoin issuance into writing, formalising the "
           "stance PBOC had signalled to PRC tech groups in 2025. The CAC governs ICP, deep-synthesis/generative-AI "
           "content, and cross-border data flows; the CSRC governs A-share issuer disclosure and has directed brokerages "
           "to pause Hong Kong tokenisation activity; MIIT and SAFE supply supporting telecoms/ICP and outbound-capital measures."),
  note="NATIVE-LANGUAGE VERIFICATION (Chinese): citation updated to the in-force 银发〔2026〕42号 (repealing 银发〔2021〕237号).")
D["cn-prc-distribution-001"]=dict(binding_status="prohibition",url=CSRC42,
  summary=("All cryptocurrency promotion, offering, and trading is prohibited within PRC territory, so there is no "
           "domestic distribution channel. For PRC-connected groups operating via Hong Kong, the indirect pathway "
           "carries three independent layers of constraint: (i) A-share listing rules (a Hong Kong subsidiary's "
           "stablecoin activities are subject to related-party-transaction disclosure, results consolidate into the "
           "listed parent under the Accounting Standards for Business Enterprises, and the CSRC may require special "
           "disclosure or pre-notification); (ii) SAFE outbound-capital control (capital injections into the HK "
           "subsidiary, profit repatriation, and intra-group financing are subject to SAFE registration and quota "
           "limits); and (iii) PBOC/CAC supervisory posture: the 2026 Notice (银发〔2026〕42号, in force 6 Feb 2026) now "
           "puts in writing the prohibition on private RMB-pegged stablecoin issuance, replacing the unpublished 2025 "
           "signalling and adding an explicit extraterritorial issuance ban."),
  note="NATIVE-LANGUAGE VERIFICATION (Chinese): the unpublished 2025 PBOC/CAC signalling is now written law (银发〔2026〕42号).")
D["cn-prc-securities_classification-001"]=dict(binding_status="prohibition",tier="firm_summary",status="in_force",url=CSRC42,
  primary="《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号); CSRC 公告〔2026〕1号《关于境内资产境外发行资产支持证券代币的监管指引》",
  pinpoint="银发〔2026〕42号 (token issuance treated as illegal public fundraising / illegal financial activity); CSRC 公告〔2026〕1号 (RWA asset-backed-securities-token guidance: filing system + negative list for onshore-asset offshore ABS-token issuance)",
  note="NATIVE-LANGUAGE VERIFICATION (Chinese): added the CSRC 公告〔2026〕1号 RWA ABS-token guidance issued alongside 42号; citation updated.")

# ---- KR: confirmed accurate; soften the over-precise procedural claim; add the 51% issuer-eligibility dispute ----
D["kr-frs-implementation_status-001"]=dict(binding_status="in_force_enacted",
  summary=("Phase-1 in force, Phase-2 pending. Milestones: Virtual Asset User Protection Act in force (19 Jul 2024); "
           "a Digital Asset Basic Act plus three stablecoin-specific bills before the National Assembly Political "
           "Affairs Committee (정무위) — as of late Apr 2026 they remained in the subcommittee (소위), with a "
           "full-committee session around mid-May 2026; a second-half-2026 passage goal described as uncertain, "
           "delayed by the won-stablecoin issuer-eligibility (51%) dispute (the Bank of Korea favouring a "
           "bank-majority consortium) and the June 2026 local elections / committee reconstitution."),
  note=("NATIVE-LANGUAGE VERIFICATION (Korean): the in-force VAUPA layer and the pending DABA bills are accurately "
        "represented. The earlier 'off the subcommittee agenda (12 May 2026)' wording is softened: sources show the "
        "bills remained in the subcommittee in late Apr 2026, so the exact procedural status was not clearly borne out. "
        "Overall characterisation (pending, H2 2026 goal, uncertain) is confirmed."))

# ---- TW: confirmed accurate and current (3 Jun 2026 first review captured); record the native-lang confirmation ----
D["tw-frs-issuer_pathway-001"]=dict(binding_status="made_not_commenced",
  note=("The TW issuer regime rests on the Virtual Asset Service Act (虛擬資產服務法), enacted at third reading 30 Jun 2026 "
        "and moved from proposed to transitional (binding made_not_commenced). NATIVE-LANGUAGE VERIFICATION (Chinese): "
        "confirmed against official FSC text: the Legislative Yuan Finance "
        "Committee completed the article-by-article first review (初審) on 3 Jun 2026 and resolved to send it to the "
        "plenary (no caucus negotiation); third reading followed on 30 Jun 2026. The stablecoin provisions match "
        "the register (FSC permission + prior central-bank consent; issuer = share company; min capital set by FSC; "
        "par issuance/redemption; no interest; reserves at domestic FIs, segregated). Procedurally ahead of "
        "KR's DABA (still in subcommittee). The in-force VASP-AML registration layer is recorded separately."))
D["tw-frs-aml_kyc-001"]=dict(binding_status="in_force_enacted",tier="resolution_text",status="in_force",
  url="https://law.moj.gov.tw/",
  pinpoint="Money Laundering Control Act (洗錢防制法) Art. 6 (amended 31 Jul 2024); VASP registration regime in force 30 Nov 2024 (non-registration: up to 2 yr + NT$5m individuals / NT$50m entities); VASPs classified into 5 types",
  verdict="confirmed_against_official_text",
  note=("NATIVE-LANGUAGE VERIFICATION (Chinese): confirmed against the official FSC text — the Money Laundering "
        "Control Act Art. 6 amendment and the VASP registration regime (in force 30 Nov 2024) are enacted and in force, "
        "so this cell is confirmed at resolution_text."))


# ----------------------------------------------------------------------------------------------------
import yaml

def fallback_binding(status, tier):
    if status in ("proposed","consultation"): return "pending_proposal"
    if status == "transitional": return "made_not_commenced"
    return "in_force_enacted"  # in_force, any tier

def set_note(d, note):
    base = (d.get("interpretation_note") or "").split(SENT)[0].rstrip()
    d["interpretation_note"] = (base + SENT + note) if base else note

def add_tags(d, tags):
    cur = d.get("tags") or []
    for t in tags:
        if t not in cur: cur.append(t)
    d["tags"] = cur

def apply():
    changed = 0; ledger = []
    # 1) explicit dispositions
    for cid, disp in D.items():
        f = ROOT / f"{cid}.yaml"
        if not f.exists():
            print("  !! missing record:", cid); continue
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        d["binding_status"] = disp["binding_status"]
        if "status" in disp: d["status"] = disp["status"]
        src = d.setdefault("source", {})
        if disp.get("url"): src["url"] = disp["url"]
        if disp.get("primary"): src["primary"] = disp["primary"]
        if disp.get("pinpoint"): src["pinpoint"] = disp["pinpoint"]
        if disp.get("summary"): d["requirement_summary"] = disp["summary"]
        if "tier" in disp:
            d["evidence_tier"] = disp["tier"]
            if disp["tier"] == "resolution_text":
                d["last_reviewed"] = VERIFIED_ON
        # verification block (only where the external review reached a verdict on the proposition)
        if disp.get("verdict"):
            tier = disp.get("tier", d.get("evidence_tier"))
            method = "official_text" if tier in ("resolution_text", "mixed") else "practitioner_corroboration"
            against = {"instrument": CLUSTERS[d["jurisdiction"]]["instrument"]}
            if src.get("url"): against["url"] = src["url"]
            if src.get("pinpoint"): against["pinpoint"] = src["pinpoint"]
            d["verification"] = {"verified_by": VERIFIED_BY, "verified_on": VERIFIED_ON,
                                 "method": method, "against": against}
        else:
            # idempotency: a disposition that no longer asserts a verdict must not leave a stale
            # verification block behind (its against.url/pinpoint would diverge from the new source).
            d.pop("verification", None)
        _note = disp.get("note", "")
        if disp.get("flag"):
            _note = (("CAVEAT: " + disp["flag"] + " ") + _note).strip()
        if _note: set_note(d, _note)
        tags = ["v0.9.5_verification", f"binding_{disp['binding_status']}"]
        if disp.get("tier") == "resolution_text": tags.append("resolution_text_verified")
        elif "tier" in disp: tags.append("verification_reviewed")
        add_tags(d, tags)
        f.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
        changed += 1
        ledger.append({"cell": cid, "jurisdiction": d["jurisdiction"],
                       "instrument": CLUSTERS[d["jurisdiction"]]["instrument"],
                       "binding_status": disp["binding_status"],
                       "official_url": src.get("url"), "pinpoint": src.get("pinpoint"),
                       "verdict": disp.get("verdict", "binding_status_recorded"),
                       "applied_tier": d.get("evidence_tier", "unset"),
                       "status_after": d.get("status"), "note": disp.get("note", "")})
    # 2) fallback binding_status for every other record (full-coverage of the new axis)
    fb = 0
    for f in sorted(ROOT.glob("*.yaml")):
        if f.name.startswith("_"): continue
        d = yaml.safe_load(f.read_text(encoding="utf-8"))
        if not isinstance(d, dict) or "id" not in d: continue
        if "binding_status" in d: continue
        d["binding_status"] = fallback_binding(d.get("status"), d.get("evidence_tier"))
        add_tags(d, [f"binding_{d['binding_status']}"])
        f.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
        fb += 1
    # 3) emit the ledger audit trail
    out = {"schema": "cbsr/verification_ledger", "version": "v0.9.9",
           "performed_by": f"{VERIFIED_BY}, {VERIFIED_ON}",
           "discipline": ("Citability is capped by the binding status of the cited instrument, independent of "
                          "whether the official text was located. resolution_text is applied ONLY where "
                          "binding_status==in_force_enacted AND the proposition was confirmed against official "
                          "text. made_not_commenced / finalized_policy_pending / pending_proposal cells receive "
                          "the official URL + binding_status but are held at firm_summary; prohibition cells stay unset."),
           "buckets": {k: CLUSTERS[k]["binding_status"] for k in CLUSTERS},
           "clusters": CLUSTERS,
           "entries": ledger}
    (ROOT / "analysis" / "verification_ledger.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    return changed, fb, ledger

if __name__ == "__main__":
    n, fb, ledger = apply()
    import collections as C
    bs = C.Counter(e["binding_status"] for e in ledger)
    rt = sum(1 for e in ledger if e["applied_tier"] == "resolution_text")
    print(f"applied {n} explicit dispositions + {fb} fallback binding_status assignments")
    print(f"  ledger binding_status: {dict(bs)}")
    print(f"  promoted to resolution_text this pass: {rt}")
    print(f"  wrote analysis/verification_ledger.json ({len(ledger)} entries)")
