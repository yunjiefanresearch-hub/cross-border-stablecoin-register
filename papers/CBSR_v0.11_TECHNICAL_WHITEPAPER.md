# Cross-Border Stablecoin Register v0.11 — superseded working draft

> The institutional, claims-traceable whitepaper is
> [`docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md`](../docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md).
> This file is retained only as a historical working draft and must not be cited as the current paper.

## Evidence-aware infrastructure for deterministic cross-border decision support

### Abstract

The Cross-Border Stablecoin Register (CBSR) is a versioned, machine-readable comparative-regulation
dataset and an offline Model Context Protocol server. Version 0.11 separates four questions that are
often collapsed in regulatory technology: what kind of claim a record makes, how strong its source is,
whether the cited instrument is legally operative, and whether the source review is fresh enough for a
decision. The release adds deterministic freshness classification, a mandate-aware AgenticFi policy core,
tamper-evident unsigned receipts, six decision-support MCP capabilities, reproducible builds, and a single
verification command. It does not claim that all 152 records have received a new legal review. Instead,
stale and unfinished research becomes a machine-visible reason to stop or escalate.

### 1. Problem

A flat compliance table is a poor control surface for an autonomous or semi-autonomous financial agent.
The table may cite a bill as though it were law, treat promulgation as commencement, blend a regulator's
policy statement with statutory text, or preserve a correct proposition after its source review has aged
past a reasonable service level. These are not cosmetic data issues. They can invert an action decision.

CBSR models regulation at the jurisdiction × instrument × dimension level and retains a source URL,
pinpoint, claim class, evidence tier, force status, review date and version. Its directed corridor layer
recognises that an origin-to-destination path may not have the same result in reverse. Version 0.11 adds a
final control: a valid, source-bearing record is not automatically decision-current.

### 2. Evidence model

The model has four independent axes.

1. **Claim class** separates propositions of law from operational facts such as a licence award or product
   launch. An official register may prove an operational fact without turning that fact into a rule.
2. **Evidence tier** records whether the proposition was confirmed against official resolution text,
   practitioner material, or a mixture. It measures provenance, not force.
3. **Binding status** distinguishes operative enactments, enacted-but-not-commenced material, final policy
   awaiting implementation, pending proposals, prohibitions and no-regime cases.
4. **Freshness** derives `current`, `due_for_review`, `stale` or `unknown` from a source-check date, an
   explicit as-of date and a published SLA. It is computed rather than trusted as a label.

The existing citable subset remains the intersection of legal claim, in-force status and official
resolution text. Freshness is shown alongside that subset. A stale citation may remain historically
citable, but it cannot support an unconditional action decision until rechecked.

### 3. Deterministic build and review discipline

`CBSR_BUILD_DATE` controls the release metadata; v0.11 defaults to the fixed release date rather than the
machine clock. Identical sources therefore generate identical timestamps. The canonical command,
`python -m tools.verify`, performs two complete rebuilds of the analysis, corridor, API, pages, site and
research layers and compares their hashes. It then executes identifier checks, MCP surface
synchronization, structural invariants, fault-injection tests, schema cross-checks and AgenticFi unit
tests; builds the wheel twice; clean-installs it outside the repository; invokes all six capabilities
with warnings treated as errors; and emits SBOM, licence and strict vulnerability evidence. Each
successful step prints an immediate `RECHECK OK` marker. A failure stops the sequence and prevents later
work from being represented as green.

CI is configured to run the same complete dependency locks and canonical verifier on Python 3.10,
3.11, 3.12 and 3.13. A workflow declaration is not a successful-run claim. Scheduled metrics collection is
read-only and uploads an artifact; it cannot commit directly to the default branch. Version 0.11 also
bounds MCP below major version 2 because the original unconstrained requirement installed an incompatible
API while the source still imported the MCP 1.x `FastMCP` path.

### 4. Freshness policy

Fast-moving proposals and no-regime observations use a seven-day review SLA. Enacted-but-not-commenced and
final-policy-pending material uses fourteen days. Operative enactments and prohibitions use thirty days.
The policy adds a seven-day `due_for_review` grace window before a record becomes `stale`. These numbers are
operational review intervals, not predictions about legal change.

The compiled dataset includes the derived status, next due date, overdue age, source disposition and
uncertainty for every record. A quantitative report publishes the complete distribution. This makes the
research backlog measurable without promoting old records simply because the software build succeeds.

### 5. AgenticFi policy core

The policy core accepts an action, a mandate and explicit applicable evidence. It returns exactly one of:

- `allow`;
- `allow_with_conditions`;
- `review_required`;
- `prohibited`; or
- `insufficient_evidence`.

The evaluator is side-effect free. It does not hold keys, call a chain, transfer value or approve
execution; every result carries `execution_authorized: false`. Mandatory context is checked before legal
reasoning. A revoked or expired mandate, an asset or jurisdiction outside the mandate, a disallowed
counterparty or an amount above the limit produces `prohibited`. A regulatory prohibition cannot be
overridden by a permissive mandate. Missing evidence produces `insufficient_evidence`. Stale, unknown,
proposed, transitional, not-commenced or conflicting evidence produces `review_required`. Only current,
operative evidence can reach `allow`, and mandatory human approval changes that result to
`allow_with_conditions`.

Six MCP tools expose this layer: `search_evidence`, `get_rule`, `evaluate_action`,
`compare_jurisdictions`, `watch_changes` and `audit_decision`. The server remains offline; “watch” means
reviewing changes and freshness in the packaged snapshot, not polling regulators.

### 6. Decision receipts

A receipt contains the dataset version, original action, deterministic decision and explicit
`signing_state: unsigned`. Canonical JSON uses sorted keys and fixed separators before SHA-256 hashing.
Replaying the same inputs produces the same decision and receipt hash. Any mutation changes the computed
digest and is reported by `audit_decision`.

This is an integrity control, not authentication. It does not establish who created or approved a
decision and offers no non-repudiation. A production deployment that needs identity assurance must add a
managed signature system outside CBSR and preserve its own access, retention and key-management controls.

### 7. Research results and boundaries

The quantitative layer is a census of the committed snapshot, not a statistical sample. It reports counts
by jurisdiction, status, binding status, evidence tier, claim class and freshness, together with the
structural citable subset. No causal or population inference is made.

The 20 August 2026 qualitative pilot rechecked four high-priority official-source leads: Taiwan's 22 July
promulgation of the Virtual Asset Service Act, the United States Treasury's 18 August proposed GENIUS Act
rule, the Bank of England/FCA joint systemic-stablecoin approach, and the HKMA licence announcement and
register. The source ledger distinguishes official lead confirmation from record-level mapping. It does
not promote an evidence tier or currentness. The pilot was single-coded, so inter-rater reliability is not
reported. Eight jurisdictions and the full record-by-record pass remain queued.

### 8. Governance and public-interest controls

Security, privacy, conduct, ownership and contribution files define the project's operating boundary.
Evidence promotion requires two reviewers. The DPG matrix is a readiness self-assessment, not a DPGA
determination. SDG mappings state design alignment only and do not claim measured impact. The local server
stores no users or decisions, but downstream clients may log sensitive action payloads; such data must not
enter Git, issues or public CI artifacts.

### 9. Limitations and release gates

Version 0.11 is a runnable decision-support foundation, not a legal-currentness certificate. The full
152-record primary-source review, independent second coding, external security review, live GitHub
ruleset verification and production interoperability tests are not completed by this source bundle. Those
are human and environment-dependent gates. Until they are closed, the software must continue to surface
stale evidence and require review rather than convert uncertainty into permission.

### 10. Reproduction

On Windows, extract the release ZIP, open PowerShell in its root, run
`Set-ExecutionPolicy -Scope Process Bypass`, then `./setup_windows.ps1`. The setup creates an isolated
environment, installs the bounded dependencies and runs the canonical verifier. `./run_mcp.ps1` starts the
stdio server. macOS and Linux users create a virtual environment, install `pip setuptools wheel` and
then `.[dev]` under `constraints/dev.txt`, run `python -m tools.verify`, and finally start
`python mcp_server.py`.
