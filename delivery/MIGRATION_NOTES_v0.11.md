# CBSR 0.11 migration notes

## Required environment

Create a clean environment and install `.[dev]` under `constraints/dev.txt` before running
`python -m tools.verify`. Runtime clients install the built wheel under `constraints/runtime.txt`.

## Data changes

- Review, source-disposition, checked/due, freshness and legal-event fields are persisted in every source YAML.
- `source_disposition` now means official/secondary/unavailable/not_applicable; legal force is separate.
- API and MCP projections expose freshness and review state; legacy structural `citable` is not current-law status.

## Policy changes

- Action, mandate, decision and receipt schemas are versioned at `v1`.
- Mandates now require identity, version, validity, scope and human-review policy.
- Receipts contain the full evidence chain and are hashed but unsigned; execution remains disabled.

Consumers must fail on unknown schema versions and must not map a legacy citable flag to unconditional allow.
