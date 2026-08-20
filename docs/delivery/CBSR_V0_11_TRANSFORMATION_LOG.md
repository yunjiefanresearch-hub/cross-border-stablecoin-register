# CBSR v0.11 transformation log

Snapshot date: 2026-08-20.

Each task is closed only at the stated evidence boundary. PASS_WITH_LIMITATION is not release approval; BLOCKED is an explicit stop.

| Task ID | Work package | Files | Sources | Commands | Result | Independent review | Negative test | Unresolved risks | Status |
|---|---|---|---|---|---|---|---|---|---|
| T-001 | Canonical reproducible delivery | tools/verify.py; constraints/; .github/workflows/build.yml | constraints/dev.txt | python -m tools.verify | Local canonical verifier and package contract implemented | Remote Python/Windows evidence pending | Legacy and directed negative suites | GitHub/Windows readback | PASS_WITH_LIMITATION |
| T-002 | Evidence and temporal schema | record.schema.json; 152 source YAML; api/records.json | official/source inventory in source ledger | python tools/migrate_review_fields.py --check | Persisted review/source/freshness/event fields and public projections | No independent second legal review | Schema/date/reviewer contradiction gates | 0 decision-ready; incomplete event links | PASS_WITH_LIMITATION |
| T-003 | Modular policy architecture | src/cbsr_mcp/; schemas/; docs/architecture/ | versioned schema contracts | python -m pytest -q | Thin server, compatibility aliases, typed models and stablecoin pack | Module and backward-compatibility tests | Malformed/unknown-schema tests | External integration certification absent | PASS |
| T-004 | AgenticFi evaluation and pilots | research/agenticfi_evaluation.json; research/pilots/ | controlled evidence fixtures | python tools/verify_agenticfi_delivery.py | 31 scenarios, receipt mutations, enterprise payment and green-asset settlement pilots | Production identity/signing review pending | Mutation, prohibited, stale, conflict and malformed cases | No execution or production validation | PASS_WITH_LIMITATION |
| T-005 | Mixed-method research and whitepaper | research/quantitative/; research/qualitative/; research/claims/; docs/whitepaper/ | 152-record census and source inventory | python tools/verify_research_delivery.py | Dashboard, coded cases, claims ledger and exact 28-section paper | Independent coding/legal/peer review pending | Missing-data and no-overclaim gates | Human research assurance open | PASS_WITH_LIMITATION |
| T-006 | Governance and security | DPG_STANDARD.md; analysis/sdg_mapping.json; SECURITY.md; docs/governance/ | official DPG/UN/GDC/DPI references | python tools/verify_governance_delivery.py | Complete self-assessment matrices, safe-harbour, archival/FAIR and readiness plans | External security/governance determinations pending | Secret/workflow/evidence-path gates | Remote ruleset and security readback | PASS_WITH_LIMITATION |
| T-007 | Release contract | docs/delivery/; delivery/external_gates.json | all preceding generated evidence | python tools/verify_delivery.py | Exact delivery paths, seven-category scorecard, migration/rollback and remote runbook | No remote PR stack or signed release | Manifest hashes and release_ready=false gate | All external gates remain blocking | BLOCKED |

Repository work is complete only within the listed local evidence boundary. Legal, peer, security, GitHub and Windows evidence is not converted into a software assertion.
