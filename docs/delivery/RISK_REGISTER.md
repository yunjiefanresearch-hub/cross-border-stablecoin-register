# Risk register

| ID | Severity | Risk | Status | Owner | Mitigation / evidence |
|---|---|---|---|---|---|
| R-001 | critical | Regulatory propositions are stale or unknown | open | legal-review-lead | Complete official-source line review, checked dates and temporal validation for 152 rows. Evidence: `freshness current=0; stale=38; unknown=114` |
| R-002 | critical | Independent second legal review absent | open | independent-legal-reviewer | Perform blind second review and reconcile every disagreement. Evidence: `second reviewer=0/152; decision-ready=0/152` |
| R-003 | high | 49 records have no official source URL | open | legal-research-lead | Locate official source or document secondary/unavailable disposition with rationale. Evidence: `research/source_ledger_2026-08-20.csv` |
| R-004 | high | 132 legal-event relationships are not first-class linked events | open | legal-data-editor | Research enactment/commencement/supersession events and validate dates. Evidence: `analysis/legal_event_ontology.json` |
| R-005 | high | Receipts are hashed but unsigned | accepted-for-research | security-owner | Integrate an identity provider and signing service before production reliance. Evidence: `signing_state=unsigned; execution_authorized=false` |
| R-006 | high | GitHub ruleset and CI have not been remotely read back | open-external | repository-admin | Run workflows, retain artifacts, configure required checks/reviews, then query settings. Evidence: `delivery/REMOTE_GITHUB_RUNBOOK.md` |
| R-007 | high | Windows 11 clean-room evidence is external | open-external | release-manager | Run setup_windows.ps1 -Recreate and retain transcript or green windows-latest artifact. Evidence: `docs/validation/PLATFORM_EVIDENCE.md` |
| R-008 | high | Independent security review absent | open-external | independent-security-reviewer | Complete scoped review and signed disposition template. Evidence: `docs/security/EXTERNAL_SECURITY_REVIEW_TEMPLATE.md` |
| R-009 | medium | Qualitative second coder and inter-coder agreement absent | open-external | independent-researcher | Complete the second-coder worksheet and reconciliation; calculate agreement. Evidence: `research/qualitative/SECOND_CODER_WORKSHEET.csv` |
| R-010 | medium | External whitepaper peer review absent | open-external | independent-peer-reviewer | Complete peer-review template, disposition claims and publish revision notes. Evidence: `docs/whitepaper/PEER_REVIEW_TEMPLATE.md` |
| R-011 | medium | Source action pins use version tags | open | security-owner | Review and pin GitHub Actions to full commit SHAs under a documented update process. Evidence: `.github/workflows/` |
| R-012 | medium | MCP/host privacy is deployment-specific | open-external | deployment-operator | Complete DPIA, retention, access, deletion, logging and transfer controls. Evidence: `PRIVACY.md` |

Open external risks cannot be closed by source-code assertions. Every row is reviewed on 2026-08-20 and targeted before production release.
