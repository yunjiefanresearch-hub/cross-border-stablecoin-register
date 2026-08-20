# ADR 0001: Modular MCP and policy boundaries

Status: accepted for v0.11 transformation foundation.

## Context

The previous MCP server combined data loading, public serialization, domain rules, decision receipts,
forty tool implementations and FastMCP startup in one 1,352-line module. This made metadata drift and
cross-domain coupling likely, and kept action, mandate and result payloads as unversioned dictionaries.

## Decision

- `core/` owns versioned, domain-neutral typed inputs, decisions and public errors.
- `data/` owns offline snapshot loading and compact record projections.
- `evidence/` and `events/` own review/freshness and legal-time semantics.
- `domain_packs/stablecoin/` owns stablecoin dimensions, obligations and ruleset version.
- `serialization/` owns canonical JSON and digests.
- `api/` owns static/public record projections.
- `tools/` owns bounded MCP tool families and the single runtime metadata registry.
- `server.py` is a composition root only; it creates FastMCP and binds the registry.

Public decisions use `cbsr/policy-decision/v1` and always expose rule IDs, source URLs, assumptions,
obligations, conflict details, engine version and ruleset version. Compatibility mappings are parsed at
the boundary and are not passed through the core as arbitrary dictionaries.

## Consequences

The public surface remains forty tools, but the count and manifest are registry-derived. Tool families
can be tested without importing FastMCP. A domain pack can evolve independently of the generic mandate
and receipt model. The decision engine remains offline and cannot authorize or execute a transaction.
