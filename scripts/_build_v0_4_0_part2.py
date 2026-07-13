#!/usr/bin/env python3
"""Part 2 of the v0.4.0 twelve-jurisdiction expansion: Japan (jp-epi) and South
Korea (kr-frs). Imported by _build_v0_4_0.py, which calls extend(R, rec, ctx).

Japan: Electronic Payment Instruments regime IN FORCE (Payment Services Act, 1 Jun
2023) as amended by Act No. 66 of 2025; multiple registered yen tokens live; foreign
tokens admitted through the registered intermediary channel.

South Korea: pre-regime — Virtual Asset User Protection Act IN FORCE (19 Jul 2024,
user-protection/AML only); the Digital Asset Basic Act (issuance regime) is a PENDING
bill. Issuance/reserve/yield/redemption provisions are PROPOSED (draft).
"""
# Portability: force UTF-8 for console output so non-ASCII (CJK, accents, §—·) prints on any
# locale (e.g. Windows GBK/cp1252). File I/O already passes encoding="utf-8" explicitly.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def extend(R, rec, ctx):
    REVIEWED = ctx["REVIEWED"]; VER = ctx["VER"]; MATRIX = ctx["MATRIX"]; ARCH = ctx["ARCH"]

    # =================================================================================
    # JAPAN (jp-epi) — Electronic Payment Instruments; closed issuer trichotomy.
    # =================================================================================
    JP = dict(jurisdiction="JP", instrument_type="fiat_referenced_stablecoin",
              instrument_label_local="Electronic Payment Instrument (EPI)")
    JP_TAGS = ["apac", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion"]

    R.append(rec(**JP, id="jp-epi-regulatory_authority-001", authority="FSA (Financial Services Agency)",
      dimension="regulatory_authority",
      requirement_summary="Fiat-referenced, par-redeemable stablecoins are Electronic Payment Instruments under the Payment Services Act. The 2022 amendment took effect 1 June 2023 and created the category; Act No. 66 of 2025 (in force June 2025, with implementing cabinet orders to follow) relaxed the trust-type backing rule. The FSA is the single supervisor of issuers and intermediaries; Local Finance Bureaus administer funds-transfer and intermediary registrations under FSA delegation.",
      requirement_structured={"category": "Electronic Payment Instrument under the Payment Services Act",
        "created": "2022 amendment, in force 1 Jun 2023", "amended_by": "Act No. 66 of 2025 (in force Jun 2025)",
        "supervisor": "FSA (single)", "delegated_admin": "Local Finance Bureaus"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act (Electronic Payment Instruments regime, in force 1 Jun 2023) as amended by Act No. 66 of 2025",
        "pinpoint": "Regulators — FSA single supervisor; Local Finance Bureaus by delegation", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Statutory Framework / Regulators)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Japan is a mature, live regime: the FSA single-supervisor model and the EPI category are the structural anchors.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-issuer_pathway-001", authority="FSA", dimension="issuer_pathway", constraint_ref="C1",
      requirement_summary="A closed trichotomy: only (a) banks (deposit-type), (b) registered funds-transfer service providers, and (c) trust companies or trust banks (trust-type) may issue Electronic Payment Instruments. Distribution and intermediation require registration as an Electronic Payment Instruments Exchange Service Provider (EPIESP). The issuer trichotomy is the binding eligibility constraint and the structural hallmark of the regime.",
      requirement_structured={"trichotomy": ["banks (deposit-type)", "registered funds-transfer providers", "trust companies / trust banks (trust-type)"],
        "intermediation": "registered Electronic Payment Instruments Exchange Service Provider (EPIESP)",
        "note": "the binding eligibility constraint and structural hallmark"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act (Electronic Payment Instruments regime)",
        "pinpoint": "Issuer pathway — closed trichotomy (bank / funds-transfer / trust); intermediation via registered EPIESP", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Issuer Pathways and Eligibility)"},
                 {"citation": ARCH + ", §2.1 (Constraint 1: Issuer Eligibility — Japan trust-type sub-mode)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Japan's trust-type issuer mode is the constraint sub-type the Architecture paper flags as differing materially in reserve treatment and bankruptcy-remoteness.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-reserve_backing-001", authority="FSA", dimension="reserve_backing", constraint_ref="C2",
      requirement_summary="Full backing is the baseline; funds-transfer and bank types hold liquid backing. For the trust-type, Act No. 66 of 2025 permits up to fifty percent of issuance value to be held in low-risk short-term assets (Japanese or US government bonds with no more than three months remaining maturity, or terminable time deposits). The bond-eligibility detail was the subject of an FSA consultation that ran until 27 February 2026; final standards were pending at that date.",
      requirement_structured={"baseline": "full backing",
        "trust_type_relaxation": "up to 50% in low-risk short-term assets (JGB/US govt bonds <=3 months, or terminable time deposits) under Act No. 66 of 2025",
        "fsa_consultation": "bond-eligibility detail; ran to 27 Feb 2026; final standards pending"},
      status="in_force", effective_date="2025-06-01",
      source={"primary": "Payment Services Act; Act No. 66 of 2025 (trust-type backing relaxation)",
        "pinpoint": "Reserve/backing — full backing baseline; trust-type up to 50% short-term low-risk assets (Act 66/2025)", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Reserve and Backing Requirements)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The Act 66/2025 trust-type relaxation (up to 50% short-term low-risk assets) is the key 2025 change; the bond-eligibility standards were still pending after the 27 Feb 2026 consultation.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-capital_requirements-001", authority="FSA", dimension="capital_requirements", constraint_ref="C2",
      requirement_summary="Capital requirements are set by entity type under the Payment Services Act and the FSA framework (banking, funds-transfer, or trust licensing); there is no separate aggregate stablecoin capital cap.",
      requirement_structured={"basis": "by entity type (banking / funds-transfer / trust licensing)",
        "aggregate_cap": "none"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act; FSA framework (by entity type)",
        "pinpoint": "Capital — by entity type (banking / funds-transfer / trust); no separate aggregate cap", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Capital Requirements)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-permitted_activity_yield-001", authority="FSA",
      dimension="permitted_activity_yield", constraint_ref="C3",
      requirement_summary="Holders are not remunerated: Electronic Payment Instruments are payment instruments, and issuer economics come from reserve interest. A reported secondary-layer lending service (SBI VC Trade, USDC, reported launch March 2026) is a boundary case at the intermediary level rather than issuer-paid yield.",
      requirement_structured={"holder_yield": "prohibited (holders not remunerated)",
        "issuer_economics": "reserve interest",
        "intermediary_boundary_case": "reported SBI VC Trade USDC lending (Mar 2026) — intermediary-level, not issuer-paid yield"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act (Electronic Payment Instruments regime)",
        "pinpoint": "Yield — holders not remunerated; issuer earns reserve interest", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Yield and Interest Treatment)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. On the C3 spine Japan is a prohibition-cluster member at the issuer layer; the SBI VC Trade lending service is the intermediary-layer boundary case (the C3xC5 routing question).",
      interpretive_flag={"tension": "Whether a reported intermediary-layer lending service over an admitted foreign token (SBI VC Trade, USDC) is issuer-paid yield or a separate intermediary product.",
        "resolution_channel": "FSA supervisory treatment of EPIESP-layer lending/yield services."},
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER,
      tags=JP_TAGS + ["spine"]))

    R.append(rec(**JP, id="jp-epi-redemption-001", authority="FSA", dimension="redemption",
      requirement_summary="Redemption is at par on demand. Funds-transfer-type tokens are subject to a 1,000,000 yen per-transfer cap.",
      requirement_structured={"redemption": "at par on demand",
        "funds_transfer_type": "JPY 1,000,000 per-transfer cap"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act (Electronic Payment Instruments regime)",
        "pinpoint": "Redemption — at par on demand; funds-transfer-type JPY 1,000,000 per-transfer cap", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Redemption Mechanics)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The JPY 1m per-transfer cap is specific to the funds-transfer issuer type.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-aml_kyc-001", authority="FSA", dimension="aml_kyc",
      requirement_summary="The FATF Travel Rule is operative (2022 amendment). Intermediaries hold a large share of customer crypto-assets in cold storage, segregate user funds via trust, and enter liability-sharing agreements with issuers.",
      requirement_structured={"travel_rule": "operative (2022 amendment)",
        "intermediary_controls": ["cold storage of a large share of customer crypto-assets", "user-fund segregation via trust", "issuer liability-sharing agreements"]},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act (2022 amendment); FSA AML framework",
        "pinpoint": "AML — FATF travel rule operative; intermediary cold storage / trust segregation / liability-sharing", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (AML / KYC Framework)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-cross_border_data-001", authority="PPC (APPI)",
      dimension="cross_border_data", constraint_ref="C6",
      requirement_summary="The Act on the Protection of Personal Information (APPI) governs personal data and cross-border handling.",
      requirement_structured={"statute": "Act on the Protection of Personal Information (APPI)",
        "scope": "personal data + cross-border handling"},
      status="in_force", effective_date=None,
      source={"primary": "Act on the Protection of Personal Information (APPI)",
        "pinpoint": "Cross-border data — APPI governs personal data and cross-border handling", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Cross-Border Data Treatment)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-monetary_sovereignty-001", authority="FSA",
      dimension="monetary_sovereignty", constraint_ref="C7",
      requirement_summary="There is no aggregate cap. Japan does not prohibit foreign-currency tokens; it admits them through a registered Electronic Payment Instruments Exchange Service Provider (EPIESP) that holds reserves in Japan equal to customers' holdings, provided the foreign issuer does not itself issue, redeem, or solicit to Japanese users. This is an open-but-channelled monetary-sovereignty posture: the currency-of-denomination is not capped, but inbound foreign tokens are routed through a registered domestic intermediary holding local reserves.",
      requirement_structured={"aggregate_cap": "none", "foreign_tokens": "admitted via registered EPIESP holding reserves in Japan",
        "issuer_condition": "foreign issuer must not issue/redeem/solicit to Japanese users directly",
        "posture": "open-but-channelled"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act (Electronic Payment Instruments regime)",
        "pinpoint": "Monetary sovereignty — no cap; foreign tokens admitted via registered EPIESP holding JP reserves", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Distribution and Offering Restrictions)"},
                 {"citation": ARCH + ", §5 (Japan — open-but-channelled posture)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Japan's C7 posture is the 'channelled-admission' model: distinct from the EU cap, the UAE channel restriction, and the PRC prohibition — it admits foreign tokens but only through a registered, locally-reserved intermediary.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-distribution-001", authority="FSA", dimension="distribution",
      requirement_summary="Foreign-issued stablecoins may be handled by a registered EPIESP if it sets aside reserves in Japan equal to customers' holdings and the foreign issuer does not itself issue, redeem, or solicit to Japanese users. USDC was admitted through SBI VC Trade (regulatory approval 4 March 2025; launch 26 March 2025), the working example of the inbound channel.",
      requirement_structured={"inbound_channel": "registered EPIESP with JP reserves equal to customer holdings; foreign issuer not soliciting JP users",
        "working_example": "USDC via SBI VC Trade (approval 4 Mar 2025; launch 26 Mar 2025)"},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act; FSA approval of USDC admission via SBI VC Trade",
        "pinpoint": "Distribution — foreign tokens via registered EPIESP w/ JP reserves; USDC via SBI VC Trade (Mar 2025)", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Distribution and Offering Restrictions)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. The USDC/SBI VC Trade admission is the live proof of the inbound channel that makes Japan an authorizable destination for foreign tokens.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    R.append(rec(**JP, id="jp-epi-implementation_status-001", authority="FSA",
      dimension="implementation_status",
      requirement_summary="Live regime. Milestones: Electronic Payment Instruments regime in force (1 June 2023); USDC admitted via the intermediary channel (March 2025); Act No. 66 of 2025 enacted, relaxing trust-type reserves (June 2025); JPYC Inc. registered as a Type II funds-transfer provider (18 August 2025); JPYC, the first registered yen stablecoin, launched (27 October 2025); a megabank trust-structured stablecoin (MUFG, Mizuho, SMBC via Progmat and Project Pax) targeted by the end of FY2026 (31 March 2027).",
      requirement_structured={"regime_stage": "live",
        "milestones": ["EPI regime in force 1 Jun 2023", "USDC admitted Mar 2025", "Act 66/2025 Jun 2025",
                        "JPYC Inc. registered 18 Aug 2025", "JPYC launched 27 Oct 2025",
                        "megabank trust token targeted by end FY2026 (31 Mar 2027)"]},
      status="in_force", effective_date="2023-06-01",
      source={"primary": "Payment Services Act commencement + FSA registrations (JPYC; USDC via SBI VC Trade)",
        "pinpoint": "Timeline — EPI 1 Jun 2023; USDC Mar 2025; Act 66/2025 Jun 2025; JPYC 27 Oct 2025; megabank trust token by FY2026", "url": ""},
      secondary=[{"citation": MATRIX + ", §Japan (Implementation Timeline)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Japan is the most operationally advanced of the v0.4.0 additions, with multiple live yen tokens and a working inbound channel.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=JP_TAGS))

    # =================================================================================
    # SOUTH KOREA (kr-frs) — pre-regime: VAUPA in force (user-protection/AML only);
    # Digital Asset Basic Act (issuance) is a pending bill. Issuance provisions PROPOSED.
    # =================================================================================
    KR = dict(jurisdiction="KR", instrument_type="fiat_referenced_stablecoin",
              instrument_label_local="won-referenced stablecoin (draft Digital Asset Basic Act)")
    KR_TAGS = ["apac", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion"]
    KR_DRAFT = ["apac", "focus", "from_matrix_v0.9.6", "v0.4.0_expansion", "draft_provision"]

    R.append(rec(**KR, id="kr-frs-regulatory_authority-001",
      authority="FSC (would administer); BOK (consultative)", dimension="regulatory_authority",
      requirement_summary="Two layers, only one in force. In force: the Virtual Asset User Protection Act (VAUPA), a user-protection and market-abuse regime, not an issuance-licensing framework. Pending: the Digital Asset Basic Act, which would create an issuance regime but remained an un-enacted bill as of late June 2026. Under the leading drafts the FSC would administer the issuance regime; the Bank of Korea (BOK) seeks a binding consultative role on monetary-sovereignty and foreign-exchange-stability grounds.",
      requirement_structured={"in_force_layer": "Virtual Asset User Protection Act (user-protection/market-abuse only)",
        "pending_layer": "Digital Asset Basic Act (issuance regime; not enacted)",
        "administrator": "FSC (under leading drafts)", "central_bank_role": "BOK seeks binding consultative role"},
      status="in_force", effective_date="2024-07-19",
      source={"primary": "Virtual Asset User Protection Act (in force 19 Jul 2024); draft Digital Asset Basic Act",
        "pinpoint": "Regulators — FSC would administer issuance; BOK consultative; VAUPA in force, DABA pending", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Statutory Framework / Regulators)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Only the VAUPA user-protection layer is operative; the issuance regime is a pending bill. Analytically paired with Taiwan as pre-regime.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_TAGS))

    R.append(rec(**KR, id="kr-frs-issuer_pathway-001", authority="FSC (would administer)",
      dimension="issuer_pathway", constraint_ref="C1",
      requirement_summary="No stablecoin issuer is licensed; domestic won-stablecoin issuance is effectively prohibited under current law. Future eligibility is contested: the BOK seeks bank-led consortia holding at least fifty-one percent; the FSC favours a more fintech-inclusive model. These are draft provisions, not operative law, and reported minimum-capital figures diverge across drafts (a press-versus-draft discrepancy) and should be treated as provisional.",
      requirement_structured={"in_force": "won-stablecoin issuance effectively prohibited; no issuer licensed",
        "contested_eligibility": "BOK >=51% bank consortium vs FSC fintech-inclusive",
        "figures": "minimum-capital figures diverge across drafts (provisional)"},
      status="proposed", effective_date=None,
      source={"primary": "Virtual Asset User Protection Act (current law); draft Digital Asset Basic Act",
        "pinpoint": "Issuer pathway — won-issuance effectively prohibited; future eligibility contested (BOK vs FSC); NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Issuer Pathways and Eligibility)"},
                 {"citation": ARCH + ", §2.1 (Constraint 1: Issuer Eligibility)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: issuance is effectively prohibited today and the future pathway is contested (the BOK-vs-FSC eligibility fight is the principal item stalling the bill).",
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_DRAFT))

    R.append(rec(**KR, id="kr-frs-reserve_backing-001", authority="FSC (would administer)",
      dimension="reserve_backing", constraint_ref="C2",
      requirement_summary="DRAFT: more than one hundred percent reserves in safe assets, bank- or custodian-held, segregated. No reserve regime is in force. Draft provisions only.",
      requirement_structured={"in_force": "none",
        "draft": ">100% reserves in safe assets, bank/custodian-held, segregated"},
      status="proposed", effective_date=None,
      source={"primary": "Draft Digital Asset Basic Act",
        "pinpoint": "Reserve/backing (draft) — >100% reserves in safe assets, bank/custodian-held, segregated; NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Reserve and Backing Requirements)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_DRAFT))

    R.append(rec(**KR, id="kr-frs-capital_requirements-001", authority="FSC (would administer)",
      dimension="capital_requirements", constraint_ref="C2",
      requirement_summary="DRAFT: minimum equity capital to be set by the enacted statute; reported figures range across drafts and are provisional (a press-versus-draft discrepancy). No stablecoin capital regime is in force.",
      requirement_structured={"in_force": "none",
        "draft": "minimum equity capital to be set by the enacted statute; reported figures provisional"},
      status="proposed", effective_date=None,
      source={"primary": "Draft Digital Asset Basic Act",
        "pinpoint": "Capital (draft) — minimum equity to be set on enactment; figures provisional; NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Capital Requirements)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law; reported minimum-capital figures diverge across drafts and should not be cited as operative.",
      confidence="low", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_DRAFT))

    R.append(rec(**KR, id="kr-frs-permitted_activity_yield-001", authority="FSC (would administer)",
      dimension="permitted_activity_yield", constraint_ref="C3",
      requirement_summary="DRAFT (Value-Stabilised Assets Act track): prohibition on interest or discounts to holders. No yield regime is in force. The draft yield prohibition would align Korea with the United States, the European Union, and Japan, but it is not operative until enactment.",
      requirement_structured={"in_force": "none",
        "draft": "prohibition on interest or discounts to holders (Value-Stabilised Assets Act track)",
        "would_align_with": "US, EU, Japan (prohibition cluster)"},
      status="proposed", effective_date=None,
      source={"primary": "Draft Digital Asset Basic Act (Value-Stabilised Assets Act track)",
        "pinpoint": "Yield (draft) — prohibition on interest/discounts to holders; NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Yield and Interest Treatment)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law. On the C3 spine, Korea is a draft member of the prohibition cluster.",
      interpretive_flag={"tension": "Korea's draft yield prohibition would align it with the United States, the European Union, and Japan, but it is not operative until enactment.",
        "resolution_channel": "Enactment of the Digital Asset Basic Act and its final text."},
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER,
      tags=KR_DRAFT + ["spine"]))

    R.append(rec(**KR, id="kr-frs-redemption-001", authority="FSC (would administer)",
      dimension="redemption",
      requirement_summary="DRAFT: par issuance and redemption. No redemption regime is in force. Draft provisions only.",
      requirement_structured={"in_force": "none", "draft": "par issuance and redemption"},
      status="proposed", effective_date=None,
      source={"primary": "Draft Digital Asset Basic Act",
        "pinpoint": "Redemption (draft) — par issuance and redemption; NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Redemption Mechanics)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
      confidence="low", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_DRAFT))

    R.append(rec(**KR, id="kr-frs-aml_kyc-001", authority="FSC / KoFIU",
      dimension="aml_kyc",
      requirement_summary="IN FORCE: anti-money-laundering and Travel Rule obligations apply through the specified financial transaction information framework. Entities converting stablecoins to fiat for third parties are treated as virtual-asset service providers requiring FSC registration.",
      requirement_structured={"in_force": "AML + Travel Rule via the specified financial transaction information framework",
        "vasp_trigger": "converting stablecoins to fiat for third parties = VASP requiring FSC registration"},
      status="in_force", effective_date=None,
      source={"primary": "Act on Reporting and Use of Specific Financial Transaction Information; Virtual Asset User Protection Act",
        "pinpoint": "AML — Travel Rule + VASP registration for stablecoin-to-fiat conversion for third parties", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (AML / KYC Framework)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. This is an in-force layer alongside VAUPA; the issuance regime remains a pending bill.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_TAGS))

    R.append(rec(**KR, id="kr-frs-cross_border_data-001", authority="PIPC (PIPA)",
      dimension="cross_border_data", constraint_ref="C6",
      requirement_summary="The Personal Information Protection Act (PIPA) governs data, including localisation.",
      requirement_structured={"statute": "Personal Information Protection Act (PIPA)",
        "scope": "data governance including localisation"},
      status="in_force", effective_date=None,
      source={"primary": "Personal Information Protection Act (PIPA)",
        "pinpoint": "Cross-border data — PIPA governs data including localisation", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Cross-Border Data Treatment)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification.",
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_TAGS))

    R.append(rec(**KR, id="kr-frs-monetary_sovereignty-001", authority="BOK / FSC",
      dimension="monetary_sovereignty", constraint_ref="C7",
      requirement_summary="No stablecoin-specific monetary-sovereignty regime is in force. DRAFT: cross-border won stablecoins would be classified as a foreign-exchange means of payment under the Foreign Exchange Transactions Act, engaging the capital-flow management regime. Won FX stability is the backdrop and the monetary-sovereignty contest (the central-bank-approval question) is the defining open issue and the principal item stalling the bill.",
      requirement_structured={"in_force_cap": "none",
        "draft": "cross-border won stablecoins classified as an FX means of payment (Foreign Exchange Transactions Act)",
        "backdrop": "won FX stability; BOK monetary-sovereignty concerns",
        "comparator": "structurally akin to Brazil's FX-reclassification of the cross-border leg"},
      status="proposed", effective_date=None,
      source={"primary": "Draft Digital Asset Basic Act; Foreign Exchange Transactions Act",
        "pinpoint": "Monetary sovereignty (draft) — cross-border won stablecoins as FX means of payment; NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Distribution and Offering Restrictions)"},
                 {"citation": ARCH + ", §5 (South Korea — monetary-sovereignty contest)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: no in-force C7 mechanism. The draft FX-means-of-payment classification echoes Brazil's câmbio reclassification (comparison by effect); the BOK/FSC sovereignty contest is what is stalling enactment.",
      interpretive_flag={"tension": "The monetary-sovereignty contest (won FX stability and the central-bank-approval question) is the defining open issue and the principal item stalling the bill.",
        "resolution_channel": "Enactment of the Digital Asset Basic Act and resolution of the BOK/FSC eligibility-and-consent question."},
      confidence="medium", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_DRAFT))

    R.append(rec(**KR, id="kr-frs-distribution-001", authority="FSC (would administer)",
      dimension="distribution",
      requirement_summary="No stablecoin-specific distribution regime is in force. DRAFT: foreign issuers would establish a local branch or subsidiary and obtain an FSC licence for payment, redemption, or remittance services, with brokered trading permitted on domestic exchanges. Cross-border stablecoins would be classified as a foreign-exchange means of payment under the Foreign Exchange Transactions Act.",
      requirement_structured={"in_force": "none",
        "draft_foreign_issuers": "local branch/subsidiary + FSC licence for payment/redemption/remittance; brokered trading on domestic exchanges",
        "draft_fx_classification": "cross-border stablecoins = FX means of payment"},
      status="proposed", effective_date=None,
      source={"primary": "Draft Digital Asset Basic Act; Foreign Exchange Transactions Act",
        "pinpoint": "Distribution (draft) — foreign issuers local branch/subsidiary + FSC licence; brokered exchange trading; NOT in force", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Distribution and Offering Restrictions)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. STATUS proposed: not operative law.",
      confidence="low", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_DRAFT))

    R.append(rec(**KR, id="kr-frs-implementation_status-001", authority="FSC / BOK",
      dimension="implementation_status",
      requirement_summary="Pre-regime, with a transition trigger on enactment. Milestones: Virtual Asset User Protection Act in force (19 July 2024); a Digital Asset Basic Act introduced (June 2025) with a consolidated version advanced in 2026; the consolidated bill left off the subcommittee agenda (12 May 2026), pushing review past the June local elections; a stated second-half-2026 passage goal described as uncertain, with the National Policy Committee not yet reconstituted after the elections.",
      requirement_structured={"regime_stage": "pre-regime (transition trigger on enactment)",
        "milestones": ["VAUPA in force 19 Jul 2024", "DABA introduced Jun 2025; consolidated 2026",
                        "consolidated bill off subcommittee agenda 12 May 2026", "H2 2026 passage goal (uncertain)"]},
      status="in_force", effective_date="2024-07-19",
      source={"primary": "Virtual Asset User Protection Act (in force 19 Jul 2024); draft Digital Asset Basic Act",
        "pinpoint": "Timeline — VAUPA in force 19 Jul 2024; DABA pending (off subcommittee 12 May 2026; H2 2026 goal, uncertain)", "url": ""},
      secondary=[{"citation": MATRIX + ", §South Korea (Implementation Timeline)"}],
      interpretation_note="Provenance: transcribed from the author's Compliance Matrix v0.9.6; pending primary-source verification. Status records the in-force VAUPA maturity stage; the issuance regime is a pending bill. Re-verify the legislative timeline after the June elections.",
      confidence="high", evidence_tier="firm_summary", last_reviewed=REVIEWED, version_added=VER, tags=KR_TAGS))
