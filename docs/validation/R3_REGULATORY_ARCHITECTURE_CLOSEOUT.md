# R3 regulatory-data and architecture closeout

> **Archived snapshot — superseded by R5.** Every number, hash and pass count in this
> file describes the earlier R3 source fingerprint only. It must not be used as evidence
> for the current tree. Use `artifacts/validation/verify-summary.json`,
> `docs/delivery/CBSR_V0_11_SCORECARD.md` and `analysis/freshness_report.json` for R5.

Date: 2026-08-20  
Release candidate: CBSR 0.11.0  
Scope: engineering remediation of the review-data model, research inventory, API/MCP
projections, legal-event ontology and MCP package architecture.

## Executive decision

The engineering acceptance criteria in this scope are implemented and locally verified.
Regulatory currentness is **not** certified: no new independent second legal review occurred,
52 records still have no source URL, and no record currently satisfies the complete
official + current + independently reconciled decision-ready gate. The system now reports
those gaps explicitly and prevents them from being promoted to unconditional policy output.

## Acceptance map

| Requirement | Result | Evidence |
|---|---|---|
| 152-row research ledger | Passed | JSON and CSV contain one unique row per record, with source, pinpoint, dates, review stage, reviewers, disposition, legal state, event link and uncertainty |
| Persist review fields in source YAML | Passed | 152/152 records validate; `migrate_review_fields.py --check` is a no-op |
| Correct source disposition taxonomy | Passed | `official=100`, `unavailable=52`; legal force is stored separately as `legal_status`/`binding_status` |
| Freshness truthfulness | Passed | `current=0`, `stale=38`, `unknown=114`; missing check dates are not silently converted to stale or current |
| Independent second-review gate | Passed as a control; human work pending | 0/152 second reviews and 0/152 decision-ready records are reported; no synthetic reviewer was inserted |
| 12 jurisdiction dossiers | Passed as evidence dossiers | 12 generated dossiers contain a line-by-line record matrix (125-176 lines each); they expressly do not claim a new legal opinion |
| Legal-event ontology | Passed as an inventory | All 152 records have an ontology row; 20 are linked to first-class events, 132 are explicit modelling gaps, 0 internal validation errors |
| Review fields in API/MCP | Passed | `api/records.json`, `api/review.json`, evidence tools, watch tools and citable tools expose freshness, source checks, due dates and review status |
| Thin server and module boundaries | Passed | `server.py` is 48 lines; logic is split across core, data, evidence, events, domain packs, tools, serialization and API modules |
| Stablecoin domain pack | Passed | Versioned stablecoin pack supplies policy dimensions, ruleset version and default obligations |
| Versioned typed policy schema | Passed | Typed action, mandate, evidence, conflict and decision models plus JSON schemas |
| Dynamic tool metadata | Passed | 40 tools are registered from one registry and synchronized to `mcp.json`; no hard-coded public tool count |
| Complete public decision structure | Passed | Results include rule IDs, source URLs, assumptions, obligations, conflicts, engine/ruleset versions and execution authorization |
| Canonical verification | Passed locally | 59 atomic steps, immediate rechecks, 59/59 invariants, 21 tests, two deterministic generations, reproducible wheel, clean install, external smoke, SBOM, licences and strict dependency audit |

## Measured state

- Records: 152.
- Official source URLs: 100; unavailable source URLs: 52.
- Evidence tiers: 27 remain `unverified`.
- Primary-review traces: 41; independent second-review traces: 0.
- Review stage: 41 primary-reviewed/second-pending; 111 unreviewed.
- Freshness: 0 current, 0 due, 38 stale, 114 unknown.
- High-impact SLA: 0/50 current and reconciled; 50/50 incomplete or breached.
- Structural citable candidates: 46; decision-ready citable records: 0.
- Legal-event coverage: 20 linked, 132 explicit gaps, 0 internal ontology errors.
- MCP tools: 40, derived from the registry.
- Runtime verification in this closeout environment: CPython 3.12.13.
- Closeout wheel SHA-256:
  `9a8f3075007827f7842e4f56ac15874aa47cfda1efabee9148300184ac8bee7f`.

## Honest scorecard

| Dimension | Score | Why it is not higher |
|---|---:|---|
| Review-data engineering | 96/100 | Complete persisted model and projections; 132 event links remain unmodelled pending legal research |
| MCP/package architecture | 97/100 | Clean boundaries, typed public models and registry; further domain packs and broader integration tests remain future work |
| Regulatory truth/currentness | 35/100 | No current records, no independent second review, 52 missing URLs and 27 unverified evidence tiers |
| Local reproducibility (3.12) | 100/100 | The expanded 59-step verifier passed with deterministic builds and clean package smoke |
| Cross-platform release evidence | 60/100 | Earlier foundation matrix exists, but the R3 source tree still needs fresh GitHub 3.10-3.13 and Windows 11 evidence |

These scores deliberately separate software correctness from legal-currentness. Averaging them
into a single marketing number would hide the principal release risk.

## Human completion gates

1. A named primary legal reviewer checks every proposition against the cited official source,
   records a pinpoint and source-check date, and resolves the 52 unavailable-source rows.
2. A different, independent legal reviewer records a disposition without seeing or copying a
   fabricated identity. Differences are reconciled and attested using the committed protocol.
3. The 27 `unverified` evidence tiers are promoted only when the source supports the promotion.
4. The 132 event-model gaps are researched; event IDs and dates are added only where primary
   evidence supports them.
5. The 50 high-impact records are completed within their SLA before any public currentness claim.
6. Run the current source tree on GitHub-hosted Python 3.10-3.13 and Windows 11; retain artifacts
   and configure the branch ruleset before release.

Until those gates are complete, `allow` remains unavailable where evidence is not current and
independently reconciled. This is the intended fail-closed behavior, not a release defect.
