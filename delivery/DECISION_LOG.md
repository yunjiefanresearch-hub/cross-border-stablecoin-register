# Architecture and delivery decision log

| ID | Decision | Status | Rationale |
|---|---|---|---|
| D-001 | Use one canonical verifier | accepted | CI, docs and platform scripts call `python -m tools.verify`; duplicated orchestration is forbidden. |
| D-002 | Fail closed on evidence | accepted | Stale, proposed, superseded, conflicting or unreviewed evidence cannot yield unconditional allow. |
| D-003 | Separate source availability from legal force | accepted | `source_disposition` and `binding_status` are independent fields. |
| D-004 | Persist review metadata in YAML | accepted | Derived outputs never invent reviewer identity or checked dates. |
| D-005 | Require a real independent second reviewer | accepted | No automation or maintainer self-review is counted as independent. |
| D-006 | Use domain-neutral policy schemas plus stablecoin pack | accepted | General action/mandate/decision/receipt schemas are separated from domain obligations. |
| D-007 | Receipts remain unsigned and non-executing | accepted | Hashing detects mutation; it does not authenticate a signer or authorize funds movement. |
| D-008 | Treat pilots as controlled evaluations | accepted | Pilot fixtures demonstrate mechanics and do not promote source records to current law. |
| D-009 | Treat DPG/SDG/GDC/DPI as design mappings | accepted | No certification, endorsement, causal impact or external determination is claimed. |
| D-010 | Keep deployment ZIP free of Git history | accepted | PR/commit lineage is delivered as a plan, not fabricated as completed history. |
| D-011 | Block release on external assurance | accepted | Remote GitHub, Windows, legal, security and peer-review gates remain explicit. |
| D-012 | Do not publish while PyPI is absent | accepted | Source/wheel deployment remains canonical until an authorized, verified publication occurs. |
