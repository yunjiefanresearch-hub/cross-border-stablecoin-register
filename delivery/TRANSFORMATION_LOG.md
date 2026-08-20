# Transformation log

Snapshot date: 2026-08-20

| Workstream | Delivered change | Status | Evidence |
|---|---|---|---|
| Verification | Single canonical verifier with deterministic generation, wheel clean-install, MCP smoke, SBOM, audit, licences and secrets | `implemented-local` | `tools/verify.py` |
| Review data | 152 source YAML records persist source, temporal and review metadata; API/MCP expose it | `implemented` | `record.schema.json; api/records.json` |
| Legal research | 152-row ledger and 12 evidence dossiers; official review and second reviewer remain incomplete | `mechanism-complete-human-gate-open` | `research/` |
| Architecture | Thin composition root, typed core, data/evidence/events/domain/tools/serialization/API boundaries | `implemented` | `src/cbsr_mcp/` |
| AgenticFi | Versioned general schemas, stablecoin pack, mandate gates, complete receipts, 31 scenarios and 2 pilots | `implemented-research-only` | `schemas/; research/agenticfi_evaluation.json` |
| Research | Quantitative CSV/JSON/Markdown/SVG, qualitative code table/taxonomy/threats, 157 claims and institutional whitepaper | `implemented-independent-review-open` | `research/; docs/whitepaper/` |
| Public interest | DPG 1-9C, exact SDG set, GDC and 18-principle DPI self-assessments | `implemented-self-assessment` | `analysis/dpg_evidence_matrix.json` |
| Security | CodeQL/dependency/secret/Scorecard/provenance declarations and local hard gates | `implemented-remote-and-external-gates-open` | `.github/workflows/; SECURITY.md` |
| Release | Migration, rollback, risk, decision, compatibility, manifests, scorecard and five-layer review plan | `implemented-not-release-ready` | `delivery/` |

`implemented` describes repository delivery only. It does not close external legal, security, peer-review, GitHub or Windows assurance gates.
