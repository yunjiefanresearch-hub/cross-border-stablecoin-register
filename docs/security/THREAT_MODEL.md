# CBSR threat model

Status: repository design review, 20 August 2026. This is not an independent penetration test or legal
assessment.

## Assets and trust boundaries

Protected assets are regulatory evidence and provenance, policy/mandate inputs, deterministic decisions,
receipts, release artifacts and the integrity of the verification pipeline. The trust boundaries are:

1. public sources to source YAML and research ledger;
2. source data to generated API/MCP projections;
3. caller-supplied action and mandate to the policy engine;
4. decision to unsigned receipt and downstream storage;
5. source checkout to dependency graph, CI, wheel and release distribution.

CBSR does not custody funds or keys, sign transactions, authenticate principals, or authorize execution.
Every decision has `execution_authorized: false`.

## Threats, controls and residual risk

| Threat | Repository control | Residual risk / deployment control |
|---|---|---|
| Stale or fabricated law | official-source disposition, persisted freshness, two-person promotion, claims ledger | 0/152 are decision-ready; independent legal review is pending |
| Malformed or unknown evidence | versioned JSON Schemas, unknown-record and negative tests | schemas cannot establish legal truth |
| Mandate bypass | prohibited-jurisdiction, validity, limit, asset, counterparty, time-window and human-review gates | caller identity and authorization require an external identity system |
| Conflicting or superseded rules | explicit conflict and superseded outcomes; fail-closed policy | reconciliation requires qualified human judgment |
| Receipt tampering | canonical JSON and component SHA-256 digests; mutation tests | receipts are unsigned and do not prove origin or non-repudiation |
| Dependency compromise | pinned constraints, reproducible wheel, SBOM, dependency review, pip-audit | registry and CI compromise remain supply-chain risks |
| Secret disclosure | local high-confidence scan, gitleaks workflow, issue guidance | scanning cannot prove absence; rotate any exposed credential |
| Build/release substitution | double build, checksums, provenance workflow | provenance and release signature need remote verification |
| Sensitive action leakage | no default persistence, minimal schema, privacy guidance | MCP clients/logging/hosts remain outside the repository boundary |
| Denial of service | bounded searches and static dataset | hosting resource limits and monitoring are operator responsibilities |

## Review cadence

Review this model on schema, policy, dependency, hosting, trust-boundary or release-process changes. Record
the reviewer, date, finding disposition and follow-up in the risk register. An external reviewer uses
`EXTERNAL_SECURITY_REVIEW_TEMPLATE.md`; absence of that attestation blocks a production-ready claim.
