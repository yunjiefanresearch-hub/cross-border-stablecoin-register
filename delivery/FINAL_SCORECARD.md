# CBSR v0.11 scorecard

Scores measure the present snapshot. They are not averaged because engineering cannot offset a legal-currentness hard stop.

| Category | Score | Numerator / denominator | Evidence | Failing criteria | Remediation | Confidence |
|---|---:|---|---|---|---|---|
| A. Runnable and reproducible | **94/100** | 94 / 100 | `tools/verify.py`, `constraints/`, `dist/package-smoke.json` | Hosted Python/Windows and required-check readback remain external. | Run and retain the remote matrix and Windows transcript. | high |
| B. Regulatory truth | **25/100** | 0 decision-ready; 0 second-reviewed / 152 records | `analysis/freshness_report.json`, `research/source_ledger_2026-08-20.csv` | Official line review, currentness, second review and event linkage remain incomplete. | Complete the 152-row legal workflow with two real reviewers and reconciliation. | high |
| C. Architecture | **97/100** | 7 module boundaries + 1 domain pack / target architecture | `src/cbsr_mcp/`, `schemas/`, `docs/architecture/` | Only the stablecoin domain pack is production-shaped; downstream interoperability is not externally certified. | Add reviewed packs without weakening generic contracts. | high |
| D. AgenticFi capability | **96/100** | 31 scenarios; 2 pilots / 18+ scenarios; 2 pilots | `research/agenticfi_evaluation.json`, `research/pilots/` | Identity/signing and production execution integration are deliberately absent. | Complete authenticated controlled-environment validation and external security review. | high |
| E. Research quality | **78/100** | 152 coded cases; 12 dossiers; 157+ claims / independently reviewed mixed-method study | `research/quantitative/`, `research/qualitative/`, `research/claims/`, `docs/whitepaper/` | Independent second coding, legal review and scholarly peer review are incomplete. | Complete independent coding/reconciliation and peer-review dispositions. | high |
| F. Governance/security/public interest | **82/100** | 11 DPG + 6 SDG + 18 DPI rows / external controls and review | `analysis/dpg_evidence_matrix.json`, `SECURITY.md`, `.github/workflows/` | Remote security settings/ruleset, independent review and external determinations are unverified. | Read back remote controls and close independent security/governance reviews. | medium-high |
| G. Release/documentation | **86/100** | formal local delivery set / signed, reviewed remote release | `docs/delivery/`, `delivery/external_gates.json` | No five-PR stack, signed release, DOI/archive deposit or remote metadata readback. | Execute the authorized remote runbook only after all hard gates close. | high |

Release-ready decision: **No**. The software fails closed correctly, but the external and human evidence needed for a release claim is incomplete.
