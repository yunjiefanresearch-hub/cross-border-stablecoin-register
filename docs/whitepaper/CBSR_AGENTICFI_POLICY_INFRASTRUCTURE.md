# CBSR AgenticFi Policy Infrastructure: Versioned, Citable and Time-Aware Rules for Autonomous Finance

Institutional technical whitepaper · version 0.11.0 · 2026-08-20

**Status:** research release candidate; external peer review and independent legal review not completed.

**Non-claim:** this document and CBSR outputs are not legal advice, transaction approval or execution authority.

---

## 1. Executive summary

CBSR is versioned policy infrastructure for cross-border stablecoin research and deterministic decision support. It keeps legal force, source provenance, freshness, uncertainty, human review and execution authority separate.

The 2026-08-20 snapshot contains 152 records across twelve jurisdictions. Its decision-ready subset is 0 because currentness and independent second review are incomplete.

### Control implications

- Treat zero decision-ready records as a correct fail-closed result.
- Use receipts for traceability, never as transaction authority.

## 2. The evidence and responsibility gap

Autonomous finance can combine an action request with machine-readable rules faster than institutions can review changing legislation. Speed does not transfer legal responsibility from the operator, principal, regulated firm or adviser to the dataset.

CBSR requires evidence state and mandate scope to travel with every result. It does not decide who may lawfully rely on that result in a particular deployment.

### Control implications

- Assign a named accountable owner for every production use.
- Escalate uncertainty instead of inventing permission.

## 3. Scope and non-claims

The unit of analysis is a jurisdiction–instrument–dimension proposition. Corridor and AgenticFi outputs are derived views and cannot create legal facts absent from source records.

CBSR is not legal advice, a sanctions service, an identity provider, a licensed execution venue, a payment instruction or a guarantee of regulatory acceptance.

### Control implications

- Keep execution_authorized=false at every CBSR boundary.
- Obtain jurisdiction-specific advice before operational reliance.

## 4. Research method and source hierarchy

The method is a complete record census with an explicit source ledger, official-source disposition, pinpoint inventory, temporal fields and review workflow. Official material outranks secondary summaries, while unavailable material remains unavailable.

A cited official URL is not equivalent to completed line-by-line review. Primary review, independent second review and reconciliation are distinct events with distinct identities and dates.

### Control implications

- Never infer a reviewer or checked date.
- Retain claims and methods in machine-readable form.

## 5. CBSR legal-evidence model

Evidence tier, source disposition, binding status, legal status, freshness, review stage and uncertainty are orthogonal fields. A plausible summary cannot silently become current, official and independently reconciled law.

Structural citability is an inventory filter. Decision readiness additionally requires official evidence, current SLA state and reconciled independent review.

### Control implications

- Expose all evidence axes through API and MCP.
- Do not map legacy citable flags to unconditional allow.

## 6. Jurisdictional coverage and empirical findings

Coverage comprises twelve jurisdictions and 15 distinct dimensions. The quantitative dashboard reports every numerator with its denominator, unit and definition.

The baseline source-disposition distribution is {'official': 103, 'unavailable': 49}; freshness is {'stale': 38, 'unknown': 114}. Coverage is not a claim of completeness or legal currency.

### Control implications

- Read jurisdiction dossiers with the record ledger.
- Preserve unavailable and unknown values as measured gaps.

## 7. Legal-event ontology

The ontology distinguishes consultation, proposed, enacted-not-commenced, finalized-policy-pending, operative, prohibited, no-regime and superseded states. Allowed transitions and date rules are versioned.

Every record receives an ontology row. A missing event link records modelling debt; it does not assert that no relevant legal event exists.

### Control implications

- Reject reversed effective intervals.
- Require an explicit event before changing temporal state.

## 8. Temporal and freshness engine

Freshness is computed as of 2026-08-20 using binding-status SLAs. The baseline distribution is {'stale': 38, 'unknown': 114}.

last_reviewed is editorial history and cannot substitute for source_last_checked. Missing dates remain unknown, and expired checks cannot produce unconditional allow.

### Control implications

- Persist source_last_checked and next_review_due in YAML.
- Block high-impact evidence that breaches SLA.

## 9. Domain-pack architecture

Generic policy models are separated from stablecoin-specific dimensions and obligations. The stablecoin domain pack declares its schema, ruleset version, supported categories and default obligation catalogue.

The MCP server is a thin composition root; data, evidence, events, domain packs, tools, serialization and API projection have explicit module boundaries.

### Control implications

- Add future domains as versioned packs.
- Keep shared receipt semantics domain-neutral.

## 10. Deterministic action evaluation

The action schema covers action, authority, conditions, modality, obligations, exceptions, effective window, evidence and uncertainty alongside route, asset, amount and actor. Unknown schemas and malformed inputs fail closed.

Outcomes are allow, allow_with_conditions, review_required, prohibited and insufficient_evidence. Prohibitions and mandate violations precede positive evidence.

### Control implications

- Use table-driven negative scenarios.
- Replay identical input, evidence and version to the identical receipt.

## 11. Agent identity, mandate and human approval

A mandate is versioned and time-bounded. It includes issuer, audit identity, assets, counterparties, amount limit, allowed and prohibited jurisdictions, execution windows and human-review thresholds.

Human approval is a condition produced by evaluation, not a signature or approval event. CBSR never records approval that an external control has not supplied.

### Control implications

- Bind production mandates to an authenticated principal.
- Record approval evidence outside the unsigned CBSR receipt.

## 12. Know-your-agent considerations

The audit-identity structure names an agent subject, actor type, principal and session context. It preserves identity assertions without claiming that CBSR authenticated them.

A production know-your-agent programme must cover credential issuance, delegation, revocation, least privilege, model/tool provenance, monitoring and recourse.

### Control implications

- Reject revoked or incomplete agent mandates.
- Separate authentication proof from policy evidence.

## 13. MCP, API and decision receipts

Six AgenticFi capabilities share typed contracts: search evidence, get rule, evaluate action, compare jurisdictions, watch changes and audit decision. Tool metadata is derived from one registry.

Receipts retain action, decision, rule IDs, sources, freshness, assumptions, uncertainty, mandate/audit identity, engine/ruleset versions, requested-as-of time and generation time. Component and receipt digests expose mutation.

### Control implications

- Treat unsigned as integrity-only.
- Retain the fixed non-legal-advice notice in public results.

## 14. Security, privacy and threat model

Threats include evidence substitution, stale-law use, mandate overreach, prompt or tool injection, secret disclosure, dependency compromise, receipt tampering and sensitive action logging.

Controls include canonical serialization, negative tests, secret scanning, dependency audit, SBOM, least-privilege workflows and privacy-minimizing deployment guidance. External security review remains open.

### Control implications

- Keep action payloads out of public telemetry.
- Verify scans and provenance in the actual remote workflow.

## 15. Governance, conflicts and corrections

Regulatory corrections follow a two-person evidence-promotion rule. A primary reviewer and different second reviewer must reconcile disagreements before decision-ready promotion.

Governance templates separate bugs, data-source proposals, regulatory corrections, security reports, releases and dependencies. Remote branch rules and reviewer requirements must be read back from GitHub.

### Control implications

- Never self-certify independent review.
- Retain correction history and supersession links.

## 16. Quantitative findings

The data-quality dashboard covers jurisdiction and dimension coverage, URL and official-source ratios, evidence tiers, freshness, high-impact SLA, missing dates, uncertainty, reviewers, events, supersession, corridor classes and temporal sensitivity.

Results are descriptive census statistics of one repository snapshot. No sampling inference, causal effect or legal-compliance rate is estimated.

### Control implications

- Use CSV/JSON for analysis and Markdown/SVG for inspection.
- Recompute every number through the canonical verifier.

## 17. Qualitative findings

A deterministic first-pass codebook classifies source-acquisition, evidence-tier, freshness, independent-review and event-model gaps. A failure taxonomy links those codes to controls and threats.

The second-coder worksheet is blank by design. Without a qualified independent pass, no intercoder statistic or independently validated theme is reported.

### Control implications

- Keep exploratory findings labelled exploratory.
- Reconcile disagreements before publication claims.

## 18. SDG alignment

Design alignment is mapped to primary targets 9.1, 16.6, 16.10 and 17.18 and secondary targets 8.10 and 16.4. Each row carries evidence, an indicator, claim strength and causal/data limitations.

No UN endorsement, measured development impact or causal attribution is claimed.

### Control implications

- Measure project outputs before impact claims.
- Retain target-specific limitations.

## 19. Global Digital Compact and DPI safeguard alignment

The GDC mapping covers human rights, inclusion, data governance, safety, digital public infrastructure and accountability. The DPI assessment covers F1–F9, O1–O9 and thirteen linked risk groups.

These are repository self-assessments, not official determinations. Deployment-specific human-rights, privacy, inclusion and remedy assessments remain necessary.

### Control implications

- Document residual deployment risk.
- Do not imply institutional endorsement.

## 20. DPG Standard readiness

The DPG matrix covers indicators 1–8 and 9A–9C separately with interpretation, evidence, owner, reviewed date, target date, verification command and next action.

Met means that cited repository evidence exists. It does not mean that the DPGA has assessed, listed or certified CBSR.

### Control implications

- Use the submission-readiness package only after external gates close.
- Preserve external_determination=false.

## 21. Pilot cases

Pilot 1 evaluates a conditioned enterprise US-to-EU stablecoin payment. Pilot 2 evaluates the stablecoin payment leg of a Singapore-to-EU tokenized green-asset delivery-versus-payment request.

Both pilots enumerate actors, assumptions, sources, rules, decision paths, human triggers, receipts, limitations and failure cases. Controlled current/reconciled fixtures test mechanics without promoting committed legal records.

### Control implications

- Do not execute either pilot.
- Obtain separate securities, green-taxonomy, sanctions and identity analysis.

## 22. Tests, evaluation and failure cases

The AgenticFi catalogue contains 31 policy scenarios and 13 receipt mutations, including malformed, unknown-record, superseded, time-bound, prohibited-jurisdiction and conflict paths.

The canonical verifier also exercises legacy and directed negative gates, schemas, research reproduction, package reproducibility, clean-wheel MCP smoke, SBOM and dependency audit.

### Control implications

- Treat each gate as atomic and fail-fast.
- Retain verifier summaries as scoped evidence.

## 23. Adoption and integration model

Adopters consume a pinned wheel or source checkout, a versioned dataset and explicit policy schemas. Integration begins in read-only decision-support mode with no funds movement.

Progression requires authenticated mandates, jurisdictional counsel, data-protection analysis, incident response, observability, approval evidence and rollback testing.

### Control implications

- Start with shadow decisions and compare outcomes.
- Pin dataset, engine, ruleset and constraints together.

## 24. Limitations

The binding limitation is legal currentness: official-source acquisition, complete primary review, independent second review and event linkage remain incomplete. No software change can manufacture those human facts.

Other limitations include jurisdiction selection, translation, prior-author coding, controlled-fixture realism, unsigned receipts, absent production identity and no remote ruleset/Windows readback in this ZIP.

### Control implications

- Keep release_ready=false while hard gates remain open.
- Report limitations next to every score.

## 25. Three-year roadmap

Year one closes official-source, high-impact currentness, event and two-person review gaps while validating remote CI, Windows, security and governance controls. Year two adds independently reviewed domain packs and authenticated/signed receipts in controlled pilots.

Year three evaluates institutional adoption, interoperability, redress, longitudinal freshness and measurable public-interest outcomes. Each phase remains conditional on evidence and governance approval.

### Control implications

- Fund recurring legal maintenance, not only software delivery.
- Publish roadmap progress with denominators and evidence.

## 26. Conclusion

CBSR shows that policy automation can become more conservative as uncertainty rises. Missing evidence, stale review, conflicting interpretations and mandate ambiguity are explicit states, not prompts to guess.

The engineering package is designed to reproduce locally. Legal, security, peer-review and repository-control assurance remains a human and external responsibility.

### Control implications

- Preserve the fail-closed boundary.
- Release only after the documented external gates close.

## 27. Primary-source bibliography

This is a deduplicated inventory of source citations in the register. Inclusion does not imply a completed currentness or independent-review check.

1. Act on Reporting and Use of Specific Financial Transaction Information; Virtual Asset User Protection Act. AML — Travel Rule + VASP registration for stablecoin-to-fiat conversion for third parties. https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=261099
2. Banking Act / FinTech-licence framework; FINMA Guidance 06/2024. Capital — per licence for licensed institutions; no separate schedule under the guarantee pathway. https://www.fedlex.admin.ch/eli/cc/1934/121/de
3. Banking Act Art. 1b (FinTech licence); Banking Ordinance Art. 5(3)(f) (deposit exclusion); FINMA Guidance 06/2024. Issuer pathways — licensed-institution vs bank-guarantee exemption (BankO Art. 5(3)(f)). https://www.fedlex.admin.ch/eli/cc/2014/273/de
4. Banking Act and Banking Ordinance; FINMA Guidance 06/2024 (Stablecoins). FINMA as primary stablecoin supervisor; SNB for systemic FMIs; no bespoke statute. https://www.fedlex.admin.ch/eli/cc/1934/121/de
5. Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024. Redemption — contractual claim vs issuer / guaranteeing bank; no statutory par mandate; not deposit-insured. https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/
6. Banking Ordinance Art. 5(3)(f); FINMA Guidance 06/2024; Collective Investment Schemes Act (CISA). Reserve/backing — no statutory schedule; guarantee covers principal + interest; CISA characterization risk. https://www.fedlex.admin.ch/eli/cc/2014/273/de
7. CBUAE PTSR (Circular 2/2024). Distribution — channel restriction; free-zone issuers carved out of onshore perimeter. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
8. CBUAE PTSR (Circular 2/2024); ADGM FRT framework. Reserve/backing — 100% segregated in UAE banks; bank-subsidiary >=50% cash + UAE govt bonds/CBUAE bills. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
9. CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework. Redemption — CBUAE par <= next business day; ADGM par within T+2. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
10. CBUAE PTSR (Circular 2/2024); ADGM-FSRA FRT framework. Yield — prohibited onshore; ADGM permits reserve income but bans investment/savings promotion. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
11. CBUAE PTSR (Circular 2/2024); DFSA recognition of USD tokens. Timeline — PTSR 2024; one-year transition closed; AED + DFSA-recognised USD tokens live. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
12. CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks. Capital — per CBUAE PTSR onshore; per free-zone framework. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
13. CBUAE PTSR (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks. Issuer pathways — DPT (CBUAE-licensed); FPT (foreign, VA/derivative-only); bank subsidiary; free-zone cannot issue AED. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
14. CBUAE Payment Token Services Regulation (Circular 2/2024). Channel restriction — merchants may accept only CBUAE-licensed Dirham Payment Tokens for goods/services; foreign tokens VA/derivative-only. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
15. CBUAE Payment Token Services Regulation (Circular 2/2024); VARA / ADGM-FSRA / DIFC-DFSA frameworks. Regulators — CBUAE onshore; VARA / ADGM-FSRA / DIFC-DFSA free zones. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
16. Collective Investment Schemes Act (CISA); FINMA Guidance 06/2024. CISA characterization where assets are held for the account of holders. https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/
17. Draft Digital Asset Basic Act. Capital (draft) — minimum equity to be set on enactment; figures provisional; NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
18. Draft Digital Asset Basic Act. Redemption (draft) — par issuance and redemption; NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
19. Draft Digital Asset Basic Act. Reserve/backing (draft) — >100% reserves in safe assets, bank/custodian-held, segregated; NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
20. Draft Digital Asset Basic Act (Value-Stabilised Assets Act track). Yield (draft) — prohibition on interest/discounts to holders; NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
21. Draft Digital Asset Basic Act; Foreign Exchange Transactions Act. Distribution (draft) — foreign issuers local branch/subsidiary + FSC licence; brokered exchange trading; NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
22. Draft Digital Asset Basic Act; Foreign Exchange Transactions Act. Monetary sovereignty (draft) — cross-border won stablecoins as FX means of payment; NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
23. FCA PS26/10; Bank of England June 2026 systemic-stablecoin policy statement and draft Code. FCA PS26/10 Summary and Ch. 2-3; exact capital-rule mapping pending. https://www.fca.org.uk/publication/policy/ps26-10.pdf
24. FINMA Guidance 06/2024 (no usage cap); Banking Act framework. Monetary sovereignty — no usage cap; foreign-currency tokens unrestricted. https://www.fedlex.admin.ch/eli/cc/2014/273/de
25. FINMA Guidance 06/2024; Anti-Money Laundering Act (AMLA). AML — identify every holder incl. intermediate holders; anonymous transfers prohibited. https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/
26. FINMA Guidance 06/2024; Banking Act framework. Distribution — no caps/channel restriction; guarantee + holder-ID are the practical limits. https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/
27. FINMA Guidance 06/2024; Banking Ordinance Art. 5(3)(f). Yield permitted; bank guarantee must cover interest (structural constraint, not prohibition). https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/
28. FINMA Guidance 06/2024; FinIA-amendment consultation (closed 6 Feb 2026). Timeline — guidance Jul 2024; FinIA consultation closed 6 Feb 2026; 6-bank CHF sandbox 8 Apr 2026. https://www.finma.ch/en/news/2024/07/20240726-m-am-06-24-stablecoins/
29. FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102. Redemption — issuer-controlled; backing-asset trust structure. https://www.legislation.gov.uk/uksi/2026/102/contents/made
30. FSMA 2000 (Cryptoassets) Regulations 2026, SI 2026/102; FCA CP25/14. Custody — 24-hour rule; safeguarding licence for regulated custodians. https://www.legislation.gov.uk/uksi/2026/102/contents/made
31. Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102. 1:1 backing; CIS/AIF carve-out for backing assets. https://www.legislation.gov.uk/uksi/2026/102/contents/made
32. Financial Services and Markets Act 2000 (Cryptoassets) Regulations 2026, SI 2026/102. FCA/BoE supervisory architecture under FSMA 2000 (as amended by SI 2026/102). https://www.legislation.gov.uk/uksi/2026/102/contents/made
33. GENIUS Act Sec. 4(a)(1) (1:1 fair-value reserve backing). GENIUS Act Sec. 4(a)(1) (1:1 fair-value backing of outstanding payment stablecoins). https://www.congress.gov/bill/119th-congress/senate-bill/1582/text
34. GENIUS Act capital provisions; OCC/FDIC NPRM (de novo capital; operational backstop; liquidation trigger). capital left to OCC/FDIC rulemaking; figures from the OCC/FDIC NPRM (proposed). https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation
35. GENIUS Act §4(a)(11); OCC NPRM §15.10(c)(4) / anti-evasion §15.10(c)(6); FDIC NPRM §350.3(b)(4); CLARITY Act (H.R. 3633) §404(c)(1) (Tillis-Alsobrooks text, 1 May 2026; affirmed final 5 May 2026). GENIUS Act Sec. 4(a)(11) (no interest/yield in connection with holding, use, or retention). https://www.federalregister.gov/documents/2025/09/19/2025-18226/genius-act-implementation
36. Guiding and Establishing National Innovation for U.S. Stablecoins Act (GENIUS Act). GENIUS Act Sec. 3-4 (permitted payment stablecoin issuers: IDI subsidiaries; OCC-qualified non-banks; certified state regimes). https://www.congress.gov/bill/119th-congress/senate-bill/1582/text
37. HKMA AML/CFT Guideline for licensed stablecoin issuers (under Cap. 656). AMLO + Ordinance AML obligations on licensees. https://www.elegislation.gov.hk/hk/cap656
38. Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); BCB implementing rulemaking. Res BCB 520/2025 (VASPs may not offer credit to clients or raise funds from the public except via share issuance; client virtual assets may not be used for proprietary operations except staking and qualified/professional-investor transactions). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520
39. Lei 14.478/2022 (Marco Legal dos Ativos Virtuais); Decreto 11.563/2023 (BCB as VASP authority; CVM carve-out for securities tokens). Lei 14.478/2022 arts. 2-9; Decreto 11.563/2023 (BCB designated competent authority for virtual-asset services; CVM retains jurisdiction over tokens that are securities). https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm
40. Lei 14.478/2022 + Decreto 11.563/2023 (CVM carve-out); CVM Parecer de Orientação 40; Resolução CVM 175 (investment funds). Lei 14.478/2022; Decreto 11.563/2023 (BCB over payment/VASP activity; CVM jurisdiction preserved over tokens with securities characteristics). https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14478.htm
41. Lei 14.478/2022; BCB regulations. Res BCB 520/2025 Art. 20 (besides SPSAVs, only commercial/exchange/investment/multiple banks, Caixa, CTVM/DTVM and FX brokers may provide intermediation/custody, with restrictions); Art. 4 (SPSAV modalities). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520
42. MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023). SCS framework: 100% reserve in low-risk assets. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
43. MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023). SCS framework: redemption at par within 5 business days. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
44. MAS Single-Currency Stablecoin Regulatory Framework (15 Aug 2023); FSMA Part 9 (DTSP). SCS framework: base capital and liquid-asset requirements. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
45. MAS Single-Currency Stablecoin framework (Aug 2023) — issuer activity restrictions. SCS framework: no lending/staking by SCS issuers; SGD/G10 label scope. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
46. MAS Stablecoin Regulatory Framework; Payment Services Act 2019. SCS framework: SGD/G10 label scope; foreign-pegged tokens treated as ordinary DPTs. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
47. Money Laundering Control Act (as amended) + VASP Registration Regulations (in force 30 Nov 2024). Money Laundering Control Act (洗錢防制法) Art. 6 (amended 31 Jul 2024); VASP registration regime in force 30 Nov 2024 (non-registration: up to 2 yr + NT$5m individuals / NT$50m entities); VASPs classified into 5 types. https://law.moj.gov.tw/
48. Money Laundering Control Act and VASP Registration Regulations; Virtual Asset Service Act, Presidential Gazette No. 7872. AML registration in force; VAS Act Arts. 2, 7-9; promulgated 22 Jul 2026, commencement mapping pending. https://www.president.gov.tw/File/Doc/69812613-22f1-4288-940e-c40903b232e1
49. PRC prohibition on cryptocurrency promotion/offering/trading within territory; CSRC A-share disclosure rules; SAFE outbound-capital controls; PBOC/CAC October 2025 guidance. Domestic distribution prohibited; three indirect-pathway constraint layers (A-share / SAFE / PBOC-CAC). https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml
50. Payment Services Act (2022 amendment); FSA AML framework. AML — FATF travel rule operative; intermediary cold storage / trust segregation / liability-sharing. https://laws.e-gov.go.jp/
51. Payment Services Act (Electronic Payment Instruments regime). Distribution — foreign tokens handled via a registered EPIESP holding JP reserves equal to customer holdings; foreign issuer may not issue/redeem/solicit to JP users. https://laws.e-gov.go.jp/
52. Payment Services Act (Electronic Payment Instruments regime). Issuer pathway — closed trichotomy (bank / funds-transfer / trust); intermediation via registered EPIESP. https://laws.e-gov.go.jp/
53. Payment Services Act (Electronic Payment Instruments regime). Monetary sovereignty — no cap; foreign tokens admitted via registered EPIESP holding JP reserves. https://laws.e-gov.go.jp/
54. Payment Services Act (Electronic Payment Instruments regime). Redemption — at par on demand; funds-transfer-type JPY 1,000,000 per-transfer cap. https://laws.e-gov.go.jp/
55. Payment Services Act (Electronic Payment Instruments regime). Yield — holders not remunerated; issuer earns reserve interest. https://laws.e-gov.go.jp/
56. Payment Services Act (Electronic Payment Instruments regime, in force 1 Jun 2023) as amended by Act No. 66 of 2025. Regulators — FSA single supervisor; Local Finance Bureaus by delegation. https://laws.e-gov.go.jp/
57. Payment Services Act 2019 / MAS Single-Currency Stablecoin Regulatory Framework. SCS framework: label/disclosure on distribution. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
58. Payment Services Act commencement + FSA registrations (JPYC; USDC via SBI VC Trade). Timeline — EPI 1 Jun 2023; USDC Mar 2025; Act 66/2025 Jun 2025; JPYC 27 Oct 2025; megabank trust token by FY2026. https://laws.e-gov.go.jp/
59. Payment Services Act; Act No. 66 of 2025 (trust-type backing relaxation). Reserve/backing — full backing baseline; trust-type up to 50% short-term low-risk assets (Act 66/2025). https://laws.e-gov.go.jp/
60. Payment Services Act; FSA framework (by entity type). Capital — by entity type (banking / funds-transfer / trust); no separate aggregate cap. https://laws.e-gov.go.jp/
61. Personal Data (Privacy) Ordinance (PDPO); s.33 (cross-border transfer, not yet commenced). PDPO (Cap. 486) data obligations; HKMA outsourcing/data guidance. https://www.elegislation.gov.hk/hk/cap656
62. Presidential Gazette No. 7872 (Virtual Asset Service Act); CBC policy materials require separate mapping. Monetary sovereignty: framework enacted, operative cap and peg-currency decision pending (not commenced). https://www.president.gov.tw/File/Doc/69812613-22f1-4288-940e-c40903b232e1
63. Regulation (EU) 2023/1114 (MiCA). Titles III/IV; EBA/ESMA/NCA supervisory architecture. https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng
64. Regulation (EU) 2023/1114 (MiCA), Art. 58(3) (applying the Art. 23 means-of-exchange thresholds to non-EU-currency EMTs). Art. 58(3) (applying Art. 23 mutatis mutandis to non-EU-currency EMTs). https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng
65. Regulation (EU) 2023/1114 (MiCA), Article 50. Art. 50 (no interest paid to EMT holders). https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng
66. Regulation (EU) 2023/1114 (MiCA), reserve composition provisions. reserve composition set in MiCA + Level-2 RTS; deposit-% pinpoint pending RTS line-read. https://eur-lex.europa.eu/eli/reg/2023/1114/oj/eng
67. Res BCB 519/2025 (authorisation regime); Res BCB 520/2025 Art. 4 (provider modalities). Lei 14.478/2022 (BCB authorisation required to provide virtual-asset services); Res BCB 519/2025 (authorisation process); Res BCB 520/2025 Art. 4 (three SPSAV modalities: intermediária, custodiante, corretora), Art. 14 (sociedade limitada/anônima; ≥3 administrators; head office in Brazil); authorisation deadline 30 Oct 2026 (270 days). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=519
68. Res BCB 520/2025 (proof-of-reserves + biennial independent audit + published reports); Res BCB 521/2025 Art. 82-A (monthly BCB reporting); IN BCB 701 (22 Jan 2026). Res BCB 520/2025 (proof of reserves; periodic audits; transparent information flows); Res BCB 521/2025 (monthly FX-operations reporting from 4 May 2026). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520
69. Res BCB 520/2025 Art. 44 (Travel Rule) + Art. 89 (two-stage phase-in: domestic by Feb 2027, international by 2 Feb 2028) + Art. 88 (authorisation adjustment period — 270-day adequação; internal controls / cybersecurity / Law 13.810/2019); Res BCB 521/2025 (KYT / self-hosted wallets). Res BCB 520/2025 (PLD/FTP obligations on SPSAVs; ≥3 responsible administrators including AML/CFT; GAFI Recs 15-16 alignment); Lei 14.478/2022. https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520
70. Res BCB 520/2025 — patrimonial segregation (segregação patrimonial). Res BCB 520/2025 (patrimonial segregation: client funds in individualised payment/deposit accounts; client virtual assets in segregated wallets; foreign-custodian conditions — home-country authorisation/supervision, Brazil representative, enforceable guarantees, formal segregation of Brazilian clients' assets). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520
71. Res BCB 520/2025 — stablecoin definition + asset-curation / listing-policy rules. Res BCB 520/2025 Art. 2, III (reserve assets of a fiat-referenced token = the fiduciary currency and public debt issued by the same governments); Arts. 64+ (asset curation; algorithmic-stablecoin prohibition; proof of reserves). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=520
72. Res BCB 521/2025 (FX reclassification + caps); Res BCB 561/2026 (eFX exclusion); Lei 14.286/2021. Res BCB 521/2025 (amends Res 277/278/279 of 31 Dec 2022): virtual-asset services brought into the FX market — international payments/transfers, stablecoin trades, and payment of expenses abroad treated as câmbio operations; monthly reporting to the BCB from 4 May 2026. https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=521
73. Res BCB 521/2025 (virtual assets in the FX market); Lei 14.286/2021 (Foreign Exchange Law). Res BCB 521 — per-operation caps (USD 100k SPSAV / USD 500k FX-FI when counterparty not FX-authorised); amends the Res 277/278/279 FX trio, inserting Art. 76-A into Res 277/2022 as the câmbio-inclusion hook (legal base: Lei 14.286/2021). https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=521
74. Resolução Conjunta CMN/BCB nº 14/2025; Res BCB 517/2025 (both 3 Nov 2025) — SPSAV minimum-capital methodology. Resolução Conjunta CMN/BCB nº 14/2025 + Res BCB nº 517/2025 (both 3 Nov 2025): minimum capital R$10,800,000 to R$37,200,000 scaled by the set of activities performed. https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolução BCB&numero=517
75. Reves v. Ernst & Young, 494 U.S. 56 (1990); SEC v. W.J. Howey Co., 328 U.S. 293 (1946); Investment Company Act of 1940 (registered MMFs); CLARITY Act market-structure provisions (pending). GENIUS Act securities carve-out (amending the '33/'34 Acts and ICA40 for permitted payment stablecoins). https://www.congress.gov/bill/119th-congress/senate-bill/1582/text
76. SI 2026/102, Art. 9M(2); FSMA s.418 (as amended); HM Treasury policy note. reg 9M(2) (issuing a qualifying stablecoin; all three limbs) vs HMT policy note (any one limb). https://www.legislation.gov.uk/uksi/2026/102/contents/made
77. SI 2026/102; FCA PS26/10; Bank of England June 2026 policy statement/draft Code; Bank/FCA joint approach. Joint approach, Introduction and Table C; FCA PS26/10 Summary; commencement 25 Oct 2027. https://www.bankofengland.co.uk/paper/2026/boe-and-fcas-approach-to-joint-regulation-of-systemic-stablecoin-issuers
78. SI 2026/102; FCA PS26/10; Bank of England June 2026 systemic policy/draft Code. Holder-yield/remuneration mapping pending; do not infer from reserve remuneration. https://www.fca.org.uk/publication/policy/ps26-10.pdf
79. Securities and Futures Act (SFA); MAS substance-over-form classification. SCS framework: 'MAS-regulated stablecoin' label vs DPT classification. https://www.mas.gov.sg/news/media-releases/2023/mas-finalises-stablecoin-regulatory-framework
80. Stablecoins Ordinance (Cap. 656) — HKD-referencing perimeter + non-HKD FRS professional-investor restriction. offshore HKD-referencing issuance is licensable; non-HKD FRS offering limited. https://www.elegislation.gov.hk/hk/cap656
81. Stablecoins Ordinance (Cap. 656), Schedule 2, s.15 (Non-interest bearing). Sch. 2 s.15 (no interest on issued stablecoins). https://www.elegislation.gov.hk/hk/cap656
82. Stablecoins Ordinance (Cap. 656), capital requirements. HK$25m paid-up capital (statutory). https://www.elegislation.gov.hk/hk/cap656
83. Stablecoins Ordinance (Cap. 656), in force 1 Aug 2025. HKMA as the licensing/supervisory authority. https://www.elegislation.gov.hk/hk/cap656
84. Stablecoins Ordinance (Cap. 656), licensing provisions. licensable regulated activities; s.8(1) licensing offence. https://www.elegislation.gov.hk/hk/cap656
85. Stablecoins Ordinance (Cap. 656), offering / distribution restrictions and offence provisions. permitted-offeror closed loop; HK$5m / 7-year offence. https://www.elegislation.gov.hk/hk/cap656
86. Stablecoins Ordinance (Cap. 656), redemption requirements. par redemption within 1 business day. https://www.elegislation.gov.hk/hk/cap656
87. Stablecoins Ordinance (Cap. 656), reserve / backing requirements. 100% backing; same-currency reserve with HKD/USD exception; segregation/trust. https://www.elegislation.gov.hk/hk/cap656
88. UAE federal AML/CFT law; CBUAE / VARA / FSRA / DFSA AML rules. AML — federal AML/CFT + FATF travel rule; per-regulator obligations. https://rulebook.centralbank.ae/en/rulebook/payment-token-services-regulation
89. UK GDPR (Data Protection Act 2018). Cross-border transfer — adequacy / IDTA / UK Addendum to EU SCCs. https://www.legislation.gov.uk/uksi/2026/102/contents/made
90. VASP Registration Regulations (30 Nov 2024); Virtual Asset Service Act, Presidential Gazette No. 7872. Gazette No. 7872, pp. 2-22; promulgation 22 Jul 2026. Commencement/subordinate-rule mapping pending. https://www.president.gov.tw/File/Doc/69812613-22f1-4288-940e-c40903b232e1
91. Virtual Asset Service Act (enacted at third reading 30 Jun 2026, not commenced). Capital: FSC to specify (enacted, not commenced; figures pending FSC subsidiary legislation). https://english.ey.gov.tw/
92. Virtual Asset Service Act (enacted at third reading 30 Jun 2026, not commenced). Distribution: offering provisions take effect on commencement (enacted, not commenced; pending FSC subsidiary legislation). https://english.ey.gov.tw/
93. Virtual Asset Service Act (enacted at third reading 30 Jun 2026, not commenced). Redemption: par issuance and redemption (enacted, not commenced; pending FSC subsidiary legislation). https://english.ey.gov.tw/
94. Virtual Asset Service Act (enacted at third reading 30 Jun 2026, not commenced). Reserve/backing: full reserves at domestic FIs, segregated (enacted, not commenced; pending FSC subsidiary legislation). https://english.ey.gov.tw/
95. Virtual Asset Service Act (enacted at third reading 30 Jun 2026, not commenced). Yield: prohibition on interest/other returns to holders (enacted, not commenced; operative on commencement). https://english.ey.gov.tw/
96. Virtual Asset Service Act, passed at third reading 30 Jun 2026 (committee first review 3 Jun 2026). Issuer pathway: FSC licence; share company; banks lead. Enacted at third reading, not yet commenced (awaiting subsidiary legislation). https://www.president.gov.tw/File/Doc/69812613-22f1-4288-940e-c40903b232e1
97. Virtual Asset User Protection Act (current law); draft Digital Asset Basic Act. Issuer pathway — won-issuance effectively prohibited; future eligibility contested (BOK vs FSC); NOT in force. https://opinion.lawmaking.go.kr/gcom/nsmLmSts/out/2210736/detailRP
98. Virtual Asset User Protection Act (in force 19 Jul 2024); draft Digital Asset Basic Act. Regulators — FSC would administer issuance; BOK consultative; VAUPA in force, DABA pending. https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=261099
99. Virtual Asset User Protection Act (in force 19 Jul 2024); draft Digital Asset Basic Act. Timeline — VAUPA in force 19 Jul 2024; DABA pending (off subcommittee 12 May 2026; H2 2026 goal, uncertain). https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=261099
100. 《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号); CSRC 公告〔2026〕1号《关于境内资产境外发行资产支持证券代币的监管指引》. 银发〔2026〕42号 (token issuance treated as illegal public fundraising / illegal financial activity); CSRC 公告〔2026〕1号 (RWA asset-backed-securities-token guidance: filing system + negative list for onshore-asset offshore ABS-token issuance). https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml
101. 《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026); issuing bodies: PBOC, NDRC, MIIT, MPS, SAMR, NFRA, CSRC, SAFE, with 中央网信办/最高法/最高检. 银发〔2026〕42号 (a coordinated multi-agency prohibition perimeter; eight ministries plus the cyberspace administration and the two supreme judicial organs). https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml
102. 《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026; repealed 银发〔2021〕237号); 2017 ICO Notice (94公告). 银发〔2026〕42号 (virtual-currency-related business activities in the PRC are illegal financial activities, strictly prohibited; the prohibited act is upgraded from '代币发行融资' (token-offering financing, 2021) to '发行虚拟货币' (issuing virtual currency), now reaching non-fundraising / airdrop / utility issuance). https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml
103. 《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, eff. 6 Feb 2026; repealed 银发〔2021〕237号); 2017 ICO Notice (94公告). 银发〔2026〕42号 — 未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币 (no entity, domestic or overseas, may issue RMB-pegged stablecoins overseas without approval); 境内主体及其控制的境外主体不得在境外发行虚拟货币 (PRC-controlled entities may not issue virtual currencies abroad); RWA tokenisation restrictions. https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml

## 28. Reproducibility appendix

### Canonical command

```text
python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
python -m tools.verify
```

The verifier regenerates committed outputs twice, compares hashes, validates schemas and internal links, runs positive and negative tests, builds the wheel twice, installs it outside the repository, smokes all six AgenticFi capabilities, emits an SBOM and runs the dependency audit.

### Claims traceability sample

| Claim | Type | Evidence | Status | Strength | Limitation |
|---|---|---|---|---|---|
| `claim-ae-pt-aml_kyc-001` | `record_level_legal_proposition` | `ae-pt-aml_kyc-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-bank_nonbank_routing-001` | `record_level_legal_proposition` | `ae-pt-bank_nonbank_routing-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-capital_requirements-001` | `record_level_legal_proposition` | `ae-pt-capital_requirements-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-cross_border_data-001` | `record_level_legal_proposition` | `ae-pt-cross_border_data-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-distribution-001` | `record_level_legal_proposition` | `ae-pt-distribution-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-implementation_status-001` | `record_level_legal_proposition` | `ae-pt-implementation_status-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-issuer_pathway-001` | `record_level_legal_proposition` | `ae-pt-issuer_pathway-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-monetary_sovereignty-001` | `record_level_legal_proposition` | `ae-pt-monetary_sovereignty-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-permitted_activity_yield-001` | `record_level_legal_proposition` | `ae-pt-permitted_activity_yield-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-redemption-001` | `record_level_legal_proposition` | `ae-pt-redemption-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-regulatory_authority-001` | `record_level_legal_proposition` | `ae-pt-regulatory_authority-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-reserve_backing-001` | `record_level_legal_proposition` | `ae-pt-reserve_backing-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-ae-pt-securities_classification-001` | `record_level_legal_proposition` | `ae-pt-securities_classification-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-aml_kyc-001` | `record_level_legal_proposition` | `br-vasp-aml_kyc-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-bank_nonbank_routing-001` | `record_level_legal_proposition` | `br-vasp-bank_nonbank_routing-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-capital_requirements-001` | `record_level_legal_proposition` | `br-vasp-capital_requirements-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-cross_border_data-001` | `record_level_legal_proposition` | `br-vasp-cross_border_data-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-custody-001` | `record_level_legal_proposition` | `br-vasp-custody-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-disclosure_reporting-001` | `record_level_legal_proposition` | `br-vasp-disclosure_reporting-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-issuer_pathway-001` | `record_level_legal_proposition` | `br-vasp-issuer_pathway-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-monetary_sovereignty-001` | `record_level_legal_proposition` | `br-vasp-monetary_sovereignty-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-permitted_activity_yield-001` | `record_level_legal_proposition` | `br-vasp-permitted_activity_yield-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-regulatory_authority-001` | `record_level_legal_proposition` | `br-vasp-regulatory_authority-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-br-vasp-reserve_backing-001` | `record_level_legal_proposition` | `br-vasp-reserve_backing-001` | `pending_independent_review` | `limited` | Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields. |
| `claim-derived-record-count` | `dataset_metric` | `dataset.json` | `machine_verified` | `computed` | Reproducible technical claim only; no external assurance or legal conclusion. |
| `claim-derived-decision-ready` | `dataset_metric` | `dataset.json` | `machine_verified` | `computed` | Reproducible technical claim only; no external assurance or legal conclusion. |
| `claim-derived-agentic-scenarios` | `software_test` | `research/agenticfi_evaluation.json` | `machine_verified` | `computed` | Reproducible technical claim only; no external assurance or legal conclusion. |
| `claim-derived-pilots` | `software_test` | `research/pilots/` | `machine_verified` | `computed` | Reproducible technical claim only; no external assurance or legal conclusion. |
| `claim-derived-server` | `architecture` | `src/cbsr_mcp/server.py` | `machine_verified` | `computed` | Reproducible technical claim only; no external assurance or legal conclusion. |

The complete ledger is `research/claims/claims_ledger.csv` and JSON. Reproduction inputs and hashes are in `research/research_manifest.json`.

### External review record

- Independent legal review: **not completed**.
- Independent qualitative second coding: **not completed**.
- External security review: **not completed**.
- External scholarly peer review: **not completed**.
- GitHub ruleset and hosted CI readback: **not completed in this local artifact**.
- Windows 11 clean-room transcript: **not completed in this local artifact**.

These release gates cannot be converted to completed by automated generation.
