# Digital Public Goods readiness evidence matrix

This is a repository self-assessment against the Digital Public Goods Standard. It is **not** a DPGA determination, DPG certification, submission, or compliance claim. `Met` means the cited repository control exists; it does not convert a repository assertion into external assurance.

| ID | Requirement | Status | Evidence | Residual limitation |
|---|---|---|---|---|
| 1 | SDG Relevance | Partial | `analysis/sdg_mapping.json`, `research/claims/claims_ledger.csv` | No causal-impact evaluation or UN/DPGA determination. |
| 2 | Open Licencing | Met | `LICENSE`, `LICENSE-DATA`, `LICENSE-CODE`, `README.md` | Licence notices still require release-by-release verification. |
| 3 | Clear Ownership | Partial | `CITATION.cff`, `.github/CODEOWNERS`, `GOVERNANCE.md` | CODEOWNERS is committed, but repository-side enforcement requires remote ruleset readback. |
| 4 | Platform Independence | Partial | `pyproject.toml`, `constraints/dev.txt`, `.github/workflows/build.yml` | Linux local evidence exists; remote Python 3.10-3.13 and Windows evidence remain external gates. |
| 5 | Documentation | Partial | `README.md`, `MCP_SERVER.md`, `LOCAL_DEPLOY_WINDOWS.md` | Independent usability testing has not been completed. |
| 6 | Non-PII Data Extraction | Met | `PRIVACY.md`, `api/records.json`, `dataset.json` | The public dataset contains regulatory research; downstream action payloads can contain sensitive data. |
| 7 | Privacy & Applicable Laws | Partial | `PRIVACY.md`, `docs/security/THREAT_MODEL.md` | Applicability depends on deployment context and must be assessed by the downstream operator. |
| 8 | Open Standards & Best Practices | Partial | `record.schema.json`, `schemas/policy-action.v1.schema.json`, `server.json` | External interoperability certification has not been performed. |
| 9A | Data Privacy & Security | Partial | `SECURITY.md`, `.github/workflows/security.yml`, `dist/cbsr-0.11.0.cdx.json` | Local controls exist; independent security assessment and remote workflow evidence remain pending. |
| 9B | Inappropriate & Illegal Content | Partial | `CODE_OF_CONDUCT.md`, `GOVERNANCE.md`, `.github/ISSUE_TEMPLATE/config.yml` | Moderation operation evidence does not yet exist. |
| 9C | Protection from Harassment | Partial | `CODE_OF_CONDUCT.md`, `.github/ISSUE_TEMPLATE/config.yml` | Enforcement effectiveness has not been independently evaluated. |

Each row is owned by the maintainer, was reviewed on 2026-08-20, and is rechecked by `python -m tools.verify`. Machine-readable owner, date, target, command and limitations are in `analysis/dpg_evidence_matrix.json`.

Official reference: https://www.digitalpublicgoods.net/standard
