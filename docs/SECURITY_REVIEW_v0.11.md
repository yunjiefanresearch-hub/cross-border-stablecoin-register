# Security review record — v0.11 source bundle

## Automated result

- Scope: wheel installed into a new Python 3.12 virtual environment.
- Runtime compatibility window: `mcp>=1.29,<1.30`; the complete reviewed runtime graph is pinned in
  `constraints/runtime.txt`.
- Import smoke test: package v0.11.0, 152 records, 40 MCP tools.
- Decision smoke test: conservative `review_required`; receipt hash verified.
- Vulnerability audit: `pip-audit 2.10.1`, run 20 August 2026 after updating the clean
  environment's packaging installer to pip 26.2.1; **no known vulnerabilities found**.
- Machine-readable output: `dist/pip-audit.json`.
- Dependency inventory: `dist/cbsr-0.11.0.cdx.json`.
- Licence metadata inventory: `dist/licenses.json`.

## Boundaries

The audit queries known package advisories; it is not a source-code penetration test or an independent
security assessment. Licence metadata may be incomplete or non-SPDX and requires human review before a
public release. GitHub rulesets, secret scanning and hosted-client logging cannot be verified from the ZIP.
