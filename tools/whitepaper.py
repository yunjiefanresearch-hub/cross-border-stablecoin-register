#!/usr/bin/env python3
"""Build the exact 28-section CBSR institutional whitepaper contract."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import pathlib
from typing import Any


TITLE = "CBSR AgenticFi Policy Infrastructure: Versioned, Citable and Time-Aware Rules for Autonomous Finance"


def _section(number: int, title: str, paragraphs: list[str], controls: list[str]) -> list[str]:
    lines = [f"## {number}. {title}", ""]
    for paragraph in paragraphs:
        lines.extend([paragraph, ""])
    lines.extend(["### Control implications", ""])
    lines.extend(f"- {control}" for control in controls)
    lines.append("")
    return lines


def build_whitepaper(
    root: pathlib.Path,
    records: list[dict[str, Any]],
    data: dict[str, Any],
    claims: list[dict[str, Any]],
    baseline: dict[str, Any],
    report: dict[str, Any],
) -> None:
    """Write a stable, evidence-bounded Markdown source for Markdown and PDF delivery."""
    ready = int((data.get("decision_ready_citable_subset") or {}).get("count", 0))
    dimensions = len({row.get("dimension") for row in records})
    specs = [
        (1, "Executive summary", [
            "CBSR is versioned policy infrastructure for cross-border stablecoin research and deterministic decision support. It keeps legal force, source provenance, freshness, uncertainty, human review and execution authority separate.",
            f"The 2026-08-20 snapshot contains {len(records)} records across twelve jurisdictions. Its decision-ready subset is {ready} because currentness and independent second review are incomplete.",
        ], ["Treat zero decision-ready records as a correct fail-closed result.", "Use receipts for traceability, never as transaction authority."]),
        (2, "The evidence and responsibility gap", [
            "Autonomous finance can combine an action request with machine-readable rules faster than institutions can review changing legislation. Speed does not transfer legal responsibility from the operator, principal, regulated firm or adviser to the dataset.",
            "CBSR requires evidence state and mandate scope to travel with every result. It does not decide who may lawfully rely on that result in a particular deployment.",
        ], ["Assign a named accountable owner for every production use.", "Escalate uncertainty instead of inventing permission."]),
        (3, "Scope and non-claims", [
            "The unit of analysis is a jurisdiction–instrument–dimension proposition. Corridor and AgenticFi outputs are derived views and cannot create legal facts absent from source records.",
            "CBSR is not legal advice, a sanctions service, an identity provider, a licensed execution venue, a payment instruction or a guarantee of regulatory acceptance.",
        ], ["Keep execution_authorized=false at every CBSR boundary.", "Obtain jurisdiction-specific advice before operational reliance."]),
        (4, "Research method and source hierarchy", [
            "The method is a complete record census with an explicit source ledger, official-source disposition, pinpoint inventory, temporal fields and review workflow. Official material outranks secondary summaries, while unavailable material remains unavailable.",
            "A cited official URL is not equivalent to completed line-by-line review. Primary review, independent second review and reconciliation are distinct events with distinct identities and dates.",
        ], ["Never infer a reviewer or checked date.", "Retain claims and methods in machine-readable form."]),
        (5, "CBSR legal-evidence model", [
            "Evidence tier, source disposition, binding status, legal status, freshness, review stage and uncertainty are orthogonal fields. A plausible summary cannot silently become current, official and independently reconciled law.",
            "Structural citability is an inventory filter. Decision readiness additionally requires official evidence, current SLA state and reconciled independent review.",
        ], ["Expose all evidence axes through API and MCP.", "Do not map legacy citable flags to unconditional allow."]),
        (6, "Jurisdictional coverage and empirical findings", [
            f"Coverage comprises twelve jurisdictions and {dimensions} distinct dimensions. The quantitative dashboard reports every numerator with its denominator, unit and definition.",
            f"The baseline source-disposition distribution is {baseline['by_source_disposition']}; freshness is {baseline['by_freshness']}. Coverage is not a claim of completeness or legal currency.",
        ], ["Read jurisdiction dossiers with the record ledger.", "Preserve unavailable and unknown values as measured gaps."]),
        (7, "Legal-event ontology", [
            "The ontology distinguishes consultation, proposed, enacted-not-commenced, finalized-policy-pending, operative, prohibited, no-regime and superseded states. Allowed transitions and date rules are versioned.",
            "Every record receives an ontology row. A missing event link records modelling debt; it does not assert that no relevant legal event exists.",
        ], ["Reject reversed effective intervals.", "Require an explicit event before changing temporal state."]),
        (8, "Temporal and freshness engine", [
            f"Freshness is computed as of 2026-08-20 using binding-status SLAs. The baseline distribution is {baseline['by_freshness']}.",
            "last_reviewed is editorial history and cannot substitute for source_last_checked. Missing dates remain unknown, and expired checks cannot produce unconditional allow.",
        ], ["Persist source_last_checked and next_review_due in YAML.", "Block high-impact evidence that breaches SLA."]),
        (9, "Domain-pack architecture", [
            "Generic policy models are separated from stablecoin-specific dimensions and obligations. The stablecoin domain pack declares its schema, ruleset version, supported categories and default obligation catalogue.",
            "The MCP server is a thin composition root; data, evidence, events, domain packs, tools, serialization and API projection have explicit module boundaries.",
        ], ["Add future domains as versioned packs.", "Keep shared receipt semantics domain-neutral."]),
        (10, "Deterministic action evaluation", [
            "The action schema covers action, authority, conditions, modality, obligations, exceptions, effective window, evidence and uncertainty alongside route, asset, amount and actor. Unknown schemas and malformed inputs fail closed.",
            "Outcomes are allow, allow_with_conditions, review_required, prohibited and insufficient_evidence. Prohibitions and mandate violations precede positive evidence.",
        ], ["Use table-driven negative scenarios.", "Replay identical input, evidence and version to the identical receipt."]),
        (11, "Agent identity, mandate and human approval", [
            "A mandate is versioned and time-bounded. It includes issuer, audit identity, assets, counterparties, amount limit, allowed and prohibited jurisdictions, execution windows and human-review thresholds.",
            "Human approval is a condition produced by evaluation, not a signature or approval event. CBSR never records approval that an external control has not supplied.",
        ], ["Bind production mandates to an authenticated principal.", "Record approval evidence outside the unsigned CBSR receipt."]),
        (12, "Know-your-agent considerations", [
            "The audit-identity structure names an agent subject, actor type, principal and session context. It preserves identity assertions without claiming that CBSR authenticated them.",
            "A production know-your-agent programme must cover credential issuance, delegation, revocation, least privilege, model/tool provenance, monitoring and recourse.",
        ], ["Reject revoked or incomplete agent mandates.", "Separate authentication proof from policy evidence."]),
        (13, "MCP, API and decision receipts", [
            "Six AgenticFi capabilities share typed contracts: search evidence, get rule, evaluate action, compare jurisdictions, watch changes and audit decision. Tool metadata is derived from one registry.",
            "Receipts retain action, decision, rule IDs, sources, freshness, assumptions, uncertainty, mandate/audit identity, engine/ruleset versions, requested-as-of time and generation time. Component and receipt digests expose mutation.",
        ], ["Treat unsigned as integrity-only.", "Retain the fixed non-legal-advice notice in public results."]),
        (14, "Security, privacy and threat model", [
            "Threats include evidence substitution, stale-law use, mandate overreach, prompt or tool injection, secret disclosure, dependency compromise, receipt tampering and sensitive action logging.",
            "Controls include canonical serialization, negative tests, secret scanning, dependency audit, SBOM, least-privilege workflows and privacy-minimizing deployment guidance. External security review remains open.",
        ], ["Keep action payloads out of public telemetry.", "Verify scans and provenance in the actual remote workflow."]),
        (15, "Governance, conflicts and corrections", [
            "Regulatory corrections follow a two-person evidence-promotion rule. A primary reviewer and different second reviewer must reconcile disagreements before decision-ready promotion.",
            "Governance templates separate bugs, data-source proposals, regulatory corrections, security reports, releases and dependencies. Remote branch rules and reviewer requirements must be read back from GitHub.",
        ], ["Never self-certify independent review.", "Retain correction history and supersession links."]),
        (16, "Quantitative findings", [
            "The data-quality dashboard covers jurisdiction and dimension coverage, URL and official-source ratios, evidence tiers, freshness, high-impact SLA, missing dates, uncertainty, reviewers, events, supersession, corridor classes and temporal sensitivity.",
            "Results are descriptive census statistics of one repository snapshot. No sampling inference, causal effect or legal-compliance rate is estimated.",
        ], ["Use CSV/JSON for analysis and Markdown/SVG for inspection.", "Recompute every number through the canonical verifier."]),
        (17, "Qualitative findings", [
            "A deterministic first-pass codebook classifies source-acquisition, evidence-tier, freshness, independent-review and event-model gaps. A failure taxonomy links those codes to controls and threats.",
            "The second-coder worksheet is blank by design. Without a qualified independent pass, no intercoder statistic or independently validated theme is reported.",
        ], ["Keep exploratory findings labelled exploratory.", "Reconcile disagreements before publication claims."]),
        (18, "SDG alignment", [
            "Design alignment is mapped to primary targets 9.1, 16.6, 16.10 and 17.18 and secondary targets 8.10 and 16.4. Each row carries evidence, an indicator, claim strength and causal/data limitations.",
            "No UN endorsement, measured development impact or causal attribution is claimed.",
        ], ["Measure project outputs before impact claims.", "Retain target-specific limitations."]),
        (19, "Global Digital Compact and DPI safeguard alignment", [
            "The GDC mapping covers human rights, inclusion, data governance, safety, digital public infrastructure and accountability. The DPI assessment covers F1–F9, O1–O9 and thirteen linked risk groups.",
            "These are repository self-assessments, not official determinations. Deployment-specific human-rights, privacy, inclusion and remedy assessments remain necessary.",
        ], ["Document residual deployment risk.", "Do not imply institutional endorsement."]),
        (20, "DPG Standard readiness", [
            "The DPG matrix covers indicators 1–8 and 9A–9C separately with interpretation, evidence, owner, reviewed date, target date, verification command and next action.",
            "Met means that cited repository evidence exists. It does not mean that the DPGA has assessed, listed or certified CBSR.",
        ], ["Use the submission-readiness package only after external gates close.", "Preserve external_determination=false."]),
        (21, "Pilot cases", [
            "Pilot 1 evaluates a conditioned enterprise US-to-EU stablecoin payment. Pilot 2 evaluates the stablecoin payment leg of a Singapore-to-EU tokenized green-asset delivery-versus-payment request.",
            "Both pilots enumerate actors, assumptions, sources, rules, decision paths, human triggers, receipts, limitations and failure cases. Controlled current/reconciled fixtures test mechanics without promoting committed legal records.",
        ], ["Do not execute either pilot.", "Obtain separate securities, green-taxonomy, sanctions and identity analysis."]),
        (22, "Tests, evaluation and failure cases", [
            f"The AgenticFi catalogue contains {report['scenario_count']} policy scenarios and {report['receipt_mutation_count']} receipt mutations, including malformed, unknown-record, superseded, time-bound, prohibited-jurisdiction and conflict paths.",
            "The canonical verifier also exercises legacy and directed negative gates, schemas, research reproduction, package reproducibility, clean-wheel MCP smoke, SBOM and dependency audit.",
        ], ["Treat each gate as atomic and fail-fast.", "Retain verifier summaries as scoped evidence."]),
        (23, "Adoption and integration model", [
            "Adopters consume a pinned wheel or source checkout, a versioned dataset and explicit policy schemas. Integration begins in read-only decision-support mode with no funds movement.",
            "Progression requires authenticated mandates, jurisdictional counsel, data-protection analysis, incident response, observability, approval evidence and rollback testing.",
        ], ["Start with shadow decisions and compare outcomes.", "Pin dataset, engine, ruleset and constraints together."]),
        (24, "Limitations", [
            "The binding limitation is legal currentness: official-source acquisition, complete primary review, independent second review and event linkage remain incomplete. No software change can manufacture those human facts.",
            "Other limitations include jurisdiction selection, translation, prior-author coding, controlled-fixture realism, unsigned receipts, absent production identity and no remote ruleset/Windows readback in this ZIP.",
        ], ["Keep release_ready=false while hard gates remain open.", "Report limitations next to every score."]),
        (25, "Three-year roadmap", [
            "Year one closes official-source, high-impact currentness, event and two-person review gaps while validating remote CI, Windows, security and governance controls. Year two adds independently reviewed domain packs and authenticated/signed receipts in controlled pilots.",
            "Year three evaluates institutional adoption, interoperability, redress, longitudinal freshness and measurable public-interest outcomes. Each phase remains conditional on evidence and governance approval.",
        ], ["Fund recurring legal maintenance, not only software delivery.", "Publish roadmap progress with denominators and evidence."]),
        (26, "Conclusion", [
            "CBSR shows that policy automation can become more conservative as uncertainty rises. Missing evidence, stale review, conflicting interpretations and mandate ambiguity are explicit states, not prompts to guess.",
            "The engineering package is designed to reproduce locally. Legal, security, peer-review and repository-control assurance remains a human and external responsibility.",
        ], ["Preserve the fail-closed boundary.", "Release only after the documented external gates close."]),
    ]
    lines = [
        f"# {TITLE}", "", "Institutional technical whitepaper · version 0.11.0 · 2026-08-20", "",
        "**Status:** research release candidate; external peer review and independent legal review not completed.", "",
        "**Non-claim:** this document and CBSR outputs are not legal advice, transaction approval or execution authority.", "", "---", "",
    ]
    for number, title, paragraphs, controls in specs:
        lines.extend(_section(number, title, paragraphs, controls))

    lines.extend(["## 27. Primary-source bibliography", "", "This is a deduplicated inventory of source citations in the register. Inclusion does not imply a completed currentness or independent-review check.", ""])
    bibliography = sorted({
        (str((row.get("source") or {}).get("primary") or row["id"]), str((row.get("source") or {}).get("url")), str((row.get("source") or {}).get("pinpoint") or "pinpoint pending"))
        for row in records if (row.get("source") or {}).get("url")
    })
    for index, (title, url, pinpoint) in enumerate(bibliography, start=1):
        lines.append(f"{index}. {title}. {pinpoint}. {url}")

    lines.extend(["", "## 28. Reproducibility appendix", "", "### Canonical command", "", "```text", "python -m pip install --constraint constraints/dev.txt \".[dev]\"", "python -m tools.verify", "```", "", "The verifier regenerates committed outputs twice, compares hashes, validates schemas and internal links, runs positive and negative tests, builds the wheel twice, installs it outside the repository, smokes all six AgenticFi capabilities, emits an SBOM and runs the dependency audit.", "", "### Claims traceability sample", "", "| Claim | Type | Evidence | Status | Strength | Limitation |", "|---|---|---|---|---|---|"])
    for claim in claims[:24] + claims[-5:]:
        lines.append(f"| `{claim['claim_id']}` | `{claim['claim_type']}` | `{claim['record_ids'] or claim['source_urls']}` | `{claim['status']}` | `{claim['strength']}` | {claim['limitation']} |")
    lines.extend(["", "The complete ledger is `research/claims/claims_ledger.csv` and JSON. Reproduction inputs and hashes are in `research/research_manifest.json`.", "", "### External review record", "", "- Independent legal review: **not completed**.", "- Independent qualitative second coding: **not completed**.", "- External security review: **not completed**.", "- External scholarly peer review: **not completed**.", "- GitHub ruleset and hosted CI readback: **not completed in this local artifact**.", "- Windows 11 clean-room transcript: **not completed in this local artifact**.", "", "These release gates cannot be converted to completed by automated generation.", ""])

    target = root / "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
