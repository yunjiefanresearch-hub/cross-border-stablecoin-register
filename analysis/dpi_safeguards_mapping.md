# Universal DPI Safeguards self-assessment

This is not an official safeguards assessment. It records repository controls and residual deployment gaps.

| ID | Requirement | Status | Evidence | Residual limitation |
|---|---|---|---|---|
| F1 | Do no harm | Partial | `src/cbsr_mcp/policy.py`, `GOVERNANCE.md` | Deployment-specific assessment and independent review remain pending. |
| F2 | Do not discriminate | Partial | `CODE_OF_CONDUCT.md`, `analysis/sdg_mapping.json` | Deployment-specific assessment and independent review remain pending. |
| F3 | Do not exclude | Partial | `README.md`, `analysis/sdg_mapping.json` | Deployment-specific assessment and independent review remain pending. |
| F4 | Reinforce transparency and accountability | Met | `src/cbsr_mcp/receipts.py`, `research/claims/claims_ledger.csv` | No external DPI safeguard assessment. |
| F5 | Uphold the rule of law | Partial | `research/source_ledger_2026-08-20.csv`, `record.schema.json` | Deployment-specific assessment and independent review remain pending. |
| F6 | Promote autonomy and agency | Partial | `src/cbsr_mcp/core/models.py`, `PRIVACY.md` | Deployment-specific assessment and independent review remain pending. |
| F7 | Foster community engagement | Partial | `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/data-source.yml` | Deployment-specific assessment and independent review remain pending. |
| F8 | Ensure effective remedy and redress | Partial | `SECURITY.md`, `.github/ISSUE_TEMPLATE/regulatory-correction.yml` | Deployment-specific assessment and independent review remain pending. |
| F9 | Focus on future sustainability | Partial | `constraints/dev.txt`, `delivery/RISK_REGISTER.md` | Deployment-specific assessment and independent review remain pending. |
| O1 | Leverage market dynamics | Partial | `LICENSE`, `GOVERNANCE.md` | Deployment-specific assessment and independent review remain pending. |
| O2 | Evolve with evidence | Met | `analysis/freshness_report.json`, `tools/verify.py` | No external DPI safeguard assessment. |
| O3 | Ensure data privacy by design | Partial | `PRIVACY.md`, `schemas/policy-action.v1.schema.json` | Deployment-specific assessment and independent review remain pending. |
| O4 | Assure data security by design | Partial | `SECURITY.md`, `.github/workflows/codeql.yml` | Deployment-specific assessment and independent review remain pending. |
| O5 | Ensure data protection during use | Partial | `PRIVACY.md`, `docs/security/THREAT_MODEL.md` | Deployment-specific assessment and independent review remain pending. |
| O6 | Respond to gender, ability or age | Partial | `CODE_OF_CONDUCT.md`, `analysis/sdg_mapping.json` | Deployment-specific assessment and independent review remain pending. |
| O7 | Practice inclusive governance | Partial | `GOVERNANCE.md`, `CONTRIBUTING.md` | Deployment-specific assessment and independent review remain pending. |
| O8 | Sustain financial viability | Partial | `GOVERNANCE.md`, `delivery/RISK_REGISTER.md` | Deployment-specific assessment and independent review remain pending. |
| O9 | Build and share open assets | Met | `LICENSE`, `LICENSE-DATA`, `LICENSE-CODE`, `schemas/domain-pack.v1.schema.json` | No external DPI safeguard assessment. |

## Risk linkage

| Risk | Linked principles | Residual risk |
|---|---|---|
| Privacy vulnerability | O3, O5 | not independently assessed |
| Digital insecurity | O4 | not independently assessed |
| Physical insecurity | F1, O4 | not independently assessed |
| Lack of recourse | F8 | not independently assessed |
| Discrimination | F2, O6 | not independently assessed |
| Unequal access | F3, O6 | not independently assessed |
| Exclusion | F3, F7 | not independently assessed |
| Disempowerment | F6 | not independently assessed |
| Digital distrust | F4, F7 | not independently assessed |
| Weak rule of law | F5 | not independently assessed |
| Weak institutions | F4, O7 | not independently assessed |
| Technical shortcomings | O2, O4 | not independently assessed |
| Unsustainability | F9, O8 | not independently assessed |

Official reference: https://www.dpi-safeguards.org/assessments
