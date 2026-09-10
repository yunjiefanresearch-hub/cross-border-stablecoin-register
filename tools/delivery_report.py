#!/usr/bin/env python3
"""Generate deterministic transformation, risk, decision and release evidence."""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import csv
import hashlib
import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "delivery"
DOC_OUT = ROOT / "docs" / "delivery"
AS_OF = "2026-08-20"


def _json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def _write_json(name: str, value: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(rows: list[dict], fields: list[str]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    DOC_OUT.mkdir(parents=True, exist_ok=True)
    quantitative = _json("research/quantitative_baseline.json")
    freshness = _json("analysis/freshness_report.json")
    agentic = _json("research/agenticfi_evaluation.json")
    research_manifest = _json("research/research_manifest.json")
    events = _json("analysis/legal_event_ontology.json")
    event_rows = events.get("records", events.get("events", []))
    linked_events = sum(1 for row in event_rows if row.get("event_id") or row.get("event_ids"))

    baseline_metrics = {
        "records": 152,
        "targeted_legal_leads": 4,
        "source_urls": 100,
        "missing_evidence_tier": 27,
        "current_records": 0,
        "independent_second_reviews": 0,
        "dossier_minimum_lines": 16,
        "agenticfi_scenarios": 10,
        "pytest_tests": 21,
        "mcp_server_lines": 1352,
    }
    current_metrics = {
        "records": quantitative["records"],
        "research_ledger_rows": quantitative["records"],
        "research_manifest_files": research_manifest["file_count"],
        "source_urls": quantitative["by_source_disposition"].get("official", 0),
        "unavailable_sources": quantitative["by_source_disposition"].get("unavailable", 0),
        "unverified_evidence_tiers": quantitative["by_evidence_tier"].get("unverified", 0),
        "current_records": freshness["counts"]["current"],
        "stale_records": freshness["counts"]["stale"],
        "unknown_freshness_records": freshness["counts"]["unknown"],
        "independent_second_reviews": freshness["reviewer_coverage"]["independent_second_reviewer"]["count"],
        "decision_ready_records": quantitative["decision_ready_citable"],
        "agenticfi_scenarios": agentic["scenario_count"],
        "receipt_mutations": agentic["receipt_mutation_count"],
        "agenticfi_pilots": len(agentic["pilots"]),
        "legal_event_rows": len(event_rows),
        "legal_events_linked": linked_events,
        "claims": len(_json("research/claims/claims_ledger.json")["claims"]),
        "dossiers": len(list((ROOT / "research/jurisdictions").glob("*.md"))),
        "whitepaper_lines": len((ROOT / "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md").read_text(encoding="utf-8").splitlines()),
        "mcp_server_lines": len((ROOT / "src/cbsr_mcp/server.py").read_text(encoding="utf-8").splitlines()),
    }
    baseline = {
        "schema": "cbsr/baseline-reproduction/v1",
        "as_of": AS_OF,
        "baseline_source": "user-supplied acceptance audit of the R3 ZIP; Git history is intentionally absent from deployment ZIPs",
        "audit_baseline_sha": "c723b9b4ec4dc86d7e13bc79681ba63101feb380",
        "reported_foundation_sha": "e91fdee15a330f3fc2f003994f3816c7ef827226",
        "sha_availability_in_zip": "not_applicable_no_git_history",
        "baseline_metrics": baseline_metrics,
        "current_metrics": current_metrics,
        "reproduction_commands": [
            "python -m pip install --constraint constraints/dev.txt '.[dev]'",
            "python -m tools.verify",
            "python tools/verify_agenticfi_delivery.py",
            "python tools/verify_research_delivery.py",
            "python tools/verify_governance_delivery.py",
            "python tools/verify_delivery.py",
        ],
        "limitations": [
            "The historical SHAs cannot be re-resolved from a Git-history-free ZIP.",
            "Legal currentness and independent review are not reproduced by code execution.",
            "GitHub and Windows status require external platform evidence.",
        ],
    }
    _write_json("baseline_reproduction.json", baseline)
    baseline_md = f"""# Baseline reproduction

Date: {AS_OF}  
Scope: user-supplied R3 acceptance audit to the current source snapshot.

The deployment ZIP intentionally excludes `.git`; therefore the reported historical baseline
`c723b9b4ec4dc86d7e13bc79681ba63101feb380` and foundation
`e91fdee15a330f3fc2f003994f3816c7ef827226` cannot be re-resolved from the ZIP. They are labels from the
acceptance record, not hashes this bundle claims to contain.

## Reproduction sequence

```bash
python -m pip install --constraint constraints/dev.txt ".[dev]"
python -m tools.verify
```

The verifier regenerates committed outputs twice, hashes them, runs the full test and research suite,
builds the wheel twice, clean-installs it outside the repository, exercises all six AgenticFi
capabilities, scans dependencies/licences/secrets and writes machine-readable evidence.

## Baseline and current facts

| Metric | Baseline | Current |
|---|---:|---:|
| Records | 152 | {current_metrics['records']} |
| Full ledger rows | 4 targeted leads | {current_metrics['research_ledger_rows']} |
| AgenticFi scenarios | 10 | {current_metrics['agenticfi_scenarios']} |
| MCP server lines | 1,352 | {current_metrics['mcp_server_lines']} |
| Current records | 0 | {current_metrics['current_records']} |
| Independent second reviews | 0 | {current_metrics['independent_second_reviews']} |

Engineering delivery expanded materially. Legal currentness did not, and is not represented as having
done so. Complete values and limitations are in `baseline_reproduction.json`.
"""
    (OUT / "BASELINE_REPRODUCTION.md").write_text(baseline_md, encoding="utf-8", newline="\n")

    risks = [
        ("R-001", "critical", "Regulatory propositions are stale or unknown", "open", "legal-review-lead", "Complete official-source line review, checked dates and temporal validation for 152 rows.", "freshness current=0; stale=38; unknown=114"),
        ("R-002", "critical", "Independent second legal review absent", "open", "independent-legal-reviewer", "Perform blind second review and reconcile every disagreement.", "second reviewer=0/152; decision-ready=0/152"),
        ("R-003", "high", f"{current_metrics['unavailable_sources']} records have no official source URL", "open", "legal-research-lead", "Locate official source or document secondary/unavailable disposition with rationale.", "research/source_ledger_2026-08-20.csv"),
        ("R-004", "high", "132 legal-event relationships are not first-class linked events", "open", "legal-data-editor", "Research enactment/commencement/supersession events and validate dates.", "analysis/legal_event_ontology.json"),
        ("R-005", "high", "Receipts are hashed but unsigned", "accepted-for-research", "security-owner", "Integrate an identity provider and signing service before production reliance.", "signing_state=unsigned; execution_authorized=false"),
        ("R-006", "high", "GitHub ruleset and CI have not been remotely read back", "open-external", "repository-admin", "Run workflows, retain artifacts, configure required checks/reviews, then query settings.", "delivery/REMOTE_GITHUB_RUNBOOK.md"),
        ("R-007", "high", "Windows 11 clean-room evidence is external", "open-external", "release-manager", "Run setup_windows.ps1 -Recreate and retain transcript or green windows-latest artifact.", "docs/validation/PLATFORM_EVIDENCE.md"),
        ("R-008", "high", "Independent security review absent", "open-external", "independent-security-reviewer", "Complete scoped review and signed disposition template.", "docs/security/EXTERNAL_SECURITY_REVIEW_TEMPLATE.md"),
        ("R-009", "medium", "Qualitative second coder and inter-coder agreement absent", "open-external", "independent-researcher", "Complete the second-coder worksheet and reconciliation; calculate agreement.", "research/qualitative/SECOND_CODER_WORKSHEET.csv"),
        ("R-010", "medium", "External whitepaper peer review absent", "open-external", "independent-peer-reviewer", "Complete peer-review template, disposition claims and publish revision notes.", "docs/whitepaper/PEER_REVIEW_TEMPLATE.md"),
        ("R-011", "medium", "Source action pins use version tags", "open", "security-owner", "Review and pin GitHub Actions to full commit SHAs under a documented update process.", ".github/workflows/"),
        ("R-012", "medium", "MCP/host privacy is deployment-specific", "open-external", "deployment-operator", "Complete DPIA, retention, access, deletion, logging and transfer controls.", "PRIVACY.md"),
    ]
    risk_rows = [{
        "risk_id": rid, "severity": severity, "risk": risk, "status": status, "owner_role": owner,
        "mitigation": mitigation, "evidence": evidence, "reviewed_date": AS_OF,
        "target_date": "before-production-release", "verification_command": "python -m tools.verify",
    } for rid, severity, risk, status, owner, mitigation, evidence in risks]
    _write_json("risk_register.json", {"schema": "cbsr/risk-register/v1", "as_of": AS_OF, "risks": risk_rows})
    risk_md = ["# Risk register", "", "| ID | Severity | Risk | Status | Owner | Mitigation / evidence |", "|---|---|---|---|---|---|"]
    for row in risk_rows:
        risk_md.append(f"| {row['risk_id']} | {row['severity']} | {row['risk']} | {row['status']} | {row['owner_role']} | {row['mitigation']} Evidence: `{row['evidence']}` |")
    risk_md += ["", "Open external risks cannot be closed by source-code assertions. Every row is reviewed on 2026-08-20 and targeted before production release."]
    (OUT / "RISK_REGISTER.md").write_text("\n".join(risk_md) + "\n", encoding="utf-8", newline="\n")

    decisions = [
        ("D-001", "Use one canonical verifier", "accepted", "CI, docs and platform scripts call `python -m tools.verify`; duplicated orchestration is forbidden."),
        ("D-002", "Fail closed on evidence", "accepted", "Stale, proposed, superseded, conflicting or unreviewed evidence cannot yield unconditional allow."),
        ("D-003", "Separate source availability from legal force", "accepted", "`source_disposition` and `binding_status` are independent fields."),
        ("D-004", "Persist review metadata in YAML", "accepted", "Derived outputs never invent reviewer identity or checked dates."),
        ("D-005", "Require a real independent second reviewer", "accepted", "No automation or maintainer self-review is counted as independent."),
        ("D-006", "Use domain-neutral policy schemas plus stablecoin pack", "accepted", "General action/mandate/decision/receipt schemas are separated from domain obligations."),
        ("D-007", "Receipts remain unsigned and non-executing", "accepted", "Hashing detects mutation; it does not authenticate a signer or authorize funds movement."),
        ("D-008", "Treat pilots as controlled evaluations", "accepted", "Pilot fixtures demonstrate mechanics and do not promote source records to current law."),
        ("D-009", "Treat DPG/SDG/GDC/DPI as design mappings", "accepted", "No certification, endorsement, causal impact or external determination is claimed."),
        ("D-010", "Keep deployment ZIP free of Git history", "accepted", "PR/commit lineage is delivered as a plan, not fabricated as completed history."),
        ("D-011", "Block release on external assurance", "accepted", "Remote GitHub, Windows, legal, security and peer-review gates remain explicit."),
        ("D-012", "Do not publish while PyPI is absent", "accepted", "Source/wheel deployment remains canonical until an authorized, verified publication occurs."),
    ]
    decision_rows = [{"decision_id": did, "decision": title, "status": status, "rationale": rationale, "date": AS_OF, "owner_role": "maintainer"} for did, title, status, rationale in decisions]
    _write_json("decision_log.json", {"schema": "cbsr/decision-log/v1", "as_of": AS_OF, "decisions": decision_rows})
    decision_md = ["# Architecture and delivery decision log", "", "| ID | Decision | Status | Rationale |", "|---|---|---|---|"]
    decision_md += [f"| {row['decision_id']} | {row['decision']} | {row['status']} | {row['rationale']} |" for row in decision_rows]
    (OUT / "DECISION_LOG.md").write_text("\n".join(decision_md) + "\n", encoding="utf-8", newline="\n")

    transformations = [
        ("Verification", "Single canonical verifier with deterministic generation, wheel clean-install, MCP smoke, SBOM, audit, licences and secrets", "implemented-local", "tools/verify.py"),
        ("Review data", "152 source YAML records persist source, temporal and review metadata; API/MCP expose it", "implemented", "record.schema.json; api/records.json"),
        ("Legal research", "152-row ledger and 12 evidence dossiers; official review and second reviewer remain incomplete", "mechanism-complete-human-gate-open", "research/"),
        ("Architecture", "Thin composition root, typed core, data/evidence/events/domain/tools/serialization/API boundaries", "implemented", "src/cbsr_mcp/"),
        ("AgenticFi", "Versioned general schemas, stablecoin pack, mandate gates, complete receipts, 31 scenarios and 2 pilots", "implemented-research-only", "schemas/; research/agenticfi_evaluation.json"),
        ("Research", "Quantitative CSV/JSON/Markdown/SVG, qualitative code table/taxonomy/threats, 157 claims and institutional whitepaper", "implemented-independent-review-open", "research/; docs/whitepaper/"),
        ("Public interest", "DPG 1-9C, exact SDG set, GDC and 18-principle DPI self-assessments", "implemented-self-assessment", "analysis/dpg_evidence_matrix.json"),
        ("Security", "CodeQL/dependency/secret/Scorecard/provenance declarations and local hard gates", "implemented-remote-and-external-gates-open", ".github/workflows/; SECURITY.md"),
        ("Release", "Migration, rollback, risk, decision, compatibility, manifests, scorecard and five-layer review plan", "implemented-not-release-ready", "delivery/"),
    ]
    lines = ["# Transformation log", "", f"Snapshot date: {AS_OF}", "", "| Workstream | Delivered change | Status | Evidence |", "|---|---|---|---|"]
    lines += [f"| {name} | {change} | `{status}` | `{evidence}` |" for name, change, status, evidence in transformations]
    lines += ["", "`implemented` describes repository delivery only. It does not close external legal, security, peer-review, GitHub or Windows assurance gates."]
    (OUT / "TRANSFORMATION_LOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    matrix_source = _json("docs/validation/local-linux-matrix.json")
    matrix_rows = []
    for minor in ("3.10", "3.11", "3.12", "3.13"):
        prior = next((row for row in matrix_source.get("versions", []) if row.get("requested_minor") == minor), None)
        matrix_rows.append({
            "platform": "local Linux", "python": minor,
            "status": "historical_prior_snapshot" if prior else "not_recorded",
            "scope": (
                "canonical verifier evidence for the recorded source fingerprint only; "
                "not evidence for this R5 snapshot or GitHub Actions"
            ),
            "evidence": "docs/validation/local-linux-matrix.json" if prior else "",
        })
    matrix_rows += [
        {"platform": "GitHub Actions ubuntu-latest", "python": "3.10-3.13", "status": "unverified_external", "scope": "remote matrix and required check", "evidence": ".github/workflows/build.yml"},
        {"platform": "Windows 11 / windows-latest", "python": "3.12", "status": "unverified_external", "scope": "clean-room PowerShell path", "evidence": "setup_windows.ps1"},
    ]
    (OUT / "compatibility_matrix.csv").write_bytes(
        _csv(matrix_rows, ["platform", "python", "status", "scope", "evidence"]).encode("utf-8")
    )
    matrix_md = ["# Compatibility matrix", "", "| Platform | Python | Status | Evidence boundary |", "|---|---|---|---|"]
    matrix_md += [f"| {row['platform']} | {row['python']} | `{row['status']}` | {row['scope']}; `{row['evidence']}` |" for row in matrix_rows]
    matrix_md += ["", "The retained local matrix belongs to an earlier source fingerprint and is not credited as R5 pass evidence. Workflow declarations are not remote pass evidence. Windows remains unverified until a transcript or Actions artifact is retained."]
    (OUT / "COMPATIBILITY_MATRIX.md").write_text("\n".join(matrix_md) + "\n", encoding="utf-8", newline="\n")

    score_rows = [
        ("A", "Runnable and reproducible", 94, "94", "100", ["tools/verify.py", "constraints/", "dist/package-smoke.json"], "Hosted Python/Windows and required-check readback remain external.", "Run and retain the remote matrix and Windows transcript.", "high"),
        ("B", "Regulatory truth", 25, "0 decision-ready; 0 second-reviewed", "152 records", ["analysis/freshness_report.json", "research/source_ledger_2026-08-20.csv"], "Official line review, currentness, second review and event linkage remain incomplete.", "Complete the 152-row legal workflow with two real reviewers and reconciliation.", "high"),
        ("C", "Architecture", 97, "7 module boundaries + 1 domain pack", "target architecture", ["src/cbsr_mcp/", "schemas/", "docs/architecture/"], "Only the stablecoin domain pack is production-shaped; downstream interoperability is not externally certified.", "Add reviewed packs without weakening generic contracts.", "high"),
        ("D", "AgenticFi capability", 96, f"{agentic['scenario_count']} scenarios; {len(agentic['pilots'])} pilots", "18+ scenarios; 2 pilots", ["research/agenticfi_evaluation.json", "research/pilots/"], "Identity/signing and production execution integration are deliberately absent.", "Complete authenticated controlled-environment validation and external security review.", "high"),
        ("E", "Research quality", 78, "152 coded cases; 12 dossiers; 157+ claims", "independently reviewed mixed-method study", ["research/quantitative/", "research/qualitative/", "research/claims/", "docs/whitepaper/"], "Independent second coding, legal review and scholarly peer review are incomplete.", "Complete independent coding/reconciliation and peer-review dispositions.", "high"),
        ("F", "Governance/security/public interest", 82, "11 DPG + 6 SDG + 18 DPI rows", "external controls and review", ["analysis/dpg_evidence_matrix.json", "SECURITY.md", ".github/workflows/"], "Remote security settings/ruleset, independent review and external determinations are unverified.", "Read back remote controls and close independent security/governance reviews.", "medium-high"),
        ("G", "Release/documentation", 86, "formal local delivery set", "signed, reviewed remote release", ["docs/delivery/", "delivery/external_gates.json"], "No five-PR stack, signed release, DOI/archive deposit or remote metadata readback.", "Execute the authorized remote runbook only after all hard gates close.", "high"),
    ]
    scorecard = [{
        "category_id": category_id, "category": category, "score": score, "target": 100,
        "numerator": numerator, "denominator": denominator, "evidence_paths": evidence,
        "failing_criteria": failing, "remediation": remediation, "confidence": confidence,
    } for category_id, category, score, numerator, denominator, evidence, failing, remediation, confidence in score_rows]
    _write_json("final_scorecard.json", {
        "schema": "cbsr/final-scorecard/v1", "as_of": AS_OF,
        "scoring_rule": "repository capability and assurance are scored separately; external work is never credited before evidence",
        "scorecard": scorecard,
        "release_ready": False,
        "blocking_reason": "legal currentness, independent review, remote GitHub and Windows assurance gates remain open",
    })
    score_md = ["# CBSR v0.11 scorecard", "", "Scores measure the present snapshot. They are not averaged because engineering cannot offset a legal-currentness hard stop.", "", "| Category | Score | Numerator / denominator | Evidence | Failing criteria | Remediation | Confidence |", "|---|---:|---|---|---|---|---|"]
    score_md += [f"| {row['category_id']}. {row['category']} | **{row['score']}/100** | {row['numerator']} / {row['denominator']} | {', '.join(f'`{item}`' for item in row['evidence_paths'])} | {row['failing_criteria']} | {row['remediation']} | {row['confidence']} |" for row in scorecard]
    score_md += ["", "Release-ready decision: **No**. The software fails closed correctly, but the external and human evidence needed for a release claim is incomplete."]
    (OUT / "FINAL_SCORECARD.md").write_text("\n".join(score_md) + "\n", encoding="utf-8", newline="\n")

    migration = """# CBSR 0.11 migration notes

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
"""
    (OUT / "MIGRATION_NOTES_v0.11.md").write_text(migration, encoding="utf-8", newline="\n")
    rollback = """# CBSR 0.11 rollback notes

1. Stop downstream decision use; retain affected action/receipt hashes and logs without sensitive payloads.
2. Verify the target artifact checksum and restore the prior immutable wheel/ZIP. Do not copy generated outputs selectively.
3. Restore source YAML and regenerate all projections with that version's canonical verifier.
4. Do not downgrade new review fields into a claim of currentness. Preserve the v0.11 research ledger for audit.
5. Revoke or mark incompatible mandates/receipts by schema and engine version; unsigned receipts are not authorization.
6. Record incident, scope, owner, timeline, restored hash and validation evidence. Reopen only after the complete verifier passes.

Rollback cannot reverse an external legal change, data disclosure, credential leak or already-consumed downstream decision.
Those events require the applicable incident, correction and notification procedure.
"""
    (OUT / "ROLLBACK_NOTES_v0.11.md").write_text(rollback, encoding="utf-8", newline="\n")

    pr_plan = """# Five-layer review and Draft PR plan

The deployment ZIP contains no `.git` history. The following is an executable review plan, **not** a
claim that five commits or Draft PRs exist.

| Layer | Branch / commit subject | Scope | Required reviewers | Hard gate |
|---|---|---|---|---|
| A | `agent/cbsr-a-runtime` / `build: canonical reproducible delivery` | constraints, verifier, package, CI | maintainer + security | full local verifier and remote platform matrix |
| B | `agent/cbsr-b-regulatory` / `data: migrate evidence and temporal review model` | 152 YAML, ledgers, dossiers, events | two independent legal reviewers | current/reconciled evidence; no synthetic identity |
| C | `agent/cbsr-c-governance` / `docs: align governance privacy and public interest` | DPG/SDG/GDC/DPI, privacy, templates | governance + privacy | exact matrices and no-overclaim checks |
| D | `agent/cbsr-d-agenticfi` / `feat: add typed policy domain and receipts` | schemas, stablecoin pack, engine, pilots | architecture + security | 31 scenarios, mutation tests, pilot replay |
| E | `agent/cbsr-e-research-release` / `docs: complete research and release evidence` | mixed methods, claims, whitepaper, manifests | independent peer reviewer + release manager | all prior layers green; external gates closed |

Create each branch from the preceding approved layer or split the source snapshot into the five subjects,
push them, create Draft PRs, retain URLs and SHAs, and never merge Layer E while regulatory, security,
GitHub or Windows hard gates remain open.
"""
    (OUT / "PR_STACK_PLAN.md").write_text(pr_plan, encoding="utf-8", newline="\n")

    remote = """# Remote GitHub completion runbook

Committed workflow and policy files do not prove GitHub is configured or has run them.

1. Push the five review branches in `PR_STACK_PLAN.md` to the authorized repository.
2. Create Draft PRs and record exact URLs and head/base SHAs.
3. Run `CBSR canonical verification`; require the stable `required-verification` check.
4. Retain all four Python logs, the Windows transcript, verification JSON, wheel, SBOM, licences and audit.
5. Enable a default-branch ruleset: pull request required, two approvals for regulatory changes,
   CODEOWNERS review, required conversation resolution, no force push/deletion and required signed commits
   if the organization's signing policy supports it.
6. Enable private vulnerability reporting, secret scanning/push protection, Dependabot alerts and CodeQL.
7. Query or inspect the saved settings and write the actual evidence URLs/JSON into the release record.
8. Publish only after legal, peer and security attestations are complete; attach checksums and provenance.

Do not paste a personal access token into this repository, an issue, a log or chat transcript.
"""
    (OUT / "REMOTE_GITHUB_RUNBOOK.md").write_text(remote, encoding="utf-8", newline="\n")

    external = {
        "schema": "cbsr/external-gates/v1", "as_of": AS_OF, "release_ready": False,
        "gates": [
            {"gate": "independent_legal_review", "status": "not_completed", "owner_role": "independent-legal-reviewer"},
            {"gate": "independent_second_qualitative_coding", "status": "not_completed", "owner_role": "independent-researcher"},
            {"gate": "external_whitepaper_peer_review", "status": "not_completed", "owner_role": "independent-peer-reviewer"},
            {"gate": "external_security_review", "status": "not_completed", "owner_role": "independent-security-reviewer"},
            {"gate": "github_actions_and_ruleset_readback", "status": "not_verified", "owner_role": "repository-admin"},
            {"gate": "windows_11_clean_room", "status": "not_verified", "owner_role": "release-manager"},
            {"gate": "signed_release_and_provenance_readback", "status": "not_verified", "owner_role": "release-manager"},
        ],
    }
    _write_json("external_gates.json", external)

    atomic_rows = [
        ("T-001", "Canonical reproducible delivery", "tools/verify.py; constraints/; .github/workflows/build.yml", "constraints/dev.txt", "python -m tools.verify", "Local canonical verifier and package contract implemented", "Remote Python/Windows evidence pending", "Legacy and directed negative suites", "GitHub/Windows readback", "PASS_WITH_LIMITATION"),
        ("T-002", "Evidence and temporal schema", "record.schema.json; 152 source YAML; api/records.json", "official/source inventory in source ledger", "python tools/migrate_review_fields.py --check", "Persisted review/source/freshness/event fields and public projections", "No independent second legal review", "Schema/date/reviewer contradiction gates", "0 decision-ready; incomplete event links", "PASS_WITH_LIMITATION"),
        ("T-003", "Modular policy architecture", "src/cbsr_mcp/; schemas/; docs/architecture/", "versioned schema contracts", "python -m pytest -q", "Thin server, compatibility aliases, typed models and stablecoin pack", "Module and backward-compatibility tests", "Malformed/unknown-schema tests", "External integration certification absent", "PASS"),
        ("T-004", "AgenticFi evaluation and pilots", "research/agenticfi_evaluation.json; research/pilots/", "controlled evidence fixtures", "python tools/verify_agenticfi_delivery.py", "31 scenarios, receipt mutations, enterprise payment and green-asset settlement pilots", "Production identity/signing review pending", "Mutation, prohibited, stale, conflict and malformed cases", "No execution or production validation", "PASS_WITH_LIMITATION"),
        ("T-005", "Mixed-method research and whitepaper", "research/quantitative/; research/qualitative/; research/claims/; docs/whitepaper/", "152-record census and source inventory", "python tools/verify_research_delivery.py", "Dashboard, coded cases, claims ledger and exact 28-section paper", "Independent coding/legal/peer review pending", "Missing-data and no-overclaim gates", "Human research assurance open", "PASS_WITH_LIMITATION"),
        ("T-006", "Governance and security", "DPG_STANDARD.md; analysis/sdg_mapping.json; SECURITY.md; docs/governance/", "official DPG/UN/GDC/DPI references", "python tools/verify_governance_delivery.py", "Complete self-assessment matrices, safe-harbour, archival/FAIR and readiness plans", "External security/governance determinations pending", "Secret/workflow/evidence-path gates", "Remote ruleset and security readback", "PASS_WITH_LIMITATION"),
        ("T-007", "Release contract", "docs/delivery/; delivery/external_gates.json", "all preceding generated evidence", "python tools/verify_delivery.py", "Exact delivery paths, seven-category scorecard, migration/rollback and remote runbook", "No remote PR stack or signed release", "Manifest hashes and release_ready=false gate", "All external gates remain blocking", "BLOCKED"),
    ]
    atomic_md = [
        "# CBSR v0.11 transformation log", "", f"Snapshot date: {AS_OF}.", "",
        "Each task is closed only at the stated evidence boundary. PASS_WITH_LIMITATION is not release approval; BLOCKED is an explicit stop.", "",
        "| Task ID | Work package | Files | Sources | Commands | Result | Independent review | Negative test | Unresolved risks | Status |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    atomic_md += ["| " + " | ".join(row) + " |" for row in atomic_rows]
    atomic_md += ["", "Repository work is complete only within the listed local evidence boundary. Legal, peer, security, GitHub and Windows evidence is not converted into a software assertion.", ""]
    (DOC_OUT / "CBSR_V0_11_TRANSFORMATION_LOG.md").write_text("\n".join(atomic_md), encoding="utf-8", newline="\n")

    copies = {
        "BASELINE_REPRODUCTION.md": OUT / "BASELINE_REPRODUCTION.md",
        "RISK_REGISTER.md": OUT / "RISK_REGISTER.md",
        "DECISION_LOG.md": OUT / "DECISION_LOG.md",
        "COMPATIBILITY_MATRIX.md": OUT / "COMPATIBILITY_MATRIX.md",
        "AGENTICFI_EVALUATION_REPORT.md": ROOT / "research/AGENTICFI_EVALUATION_REPORT.md",
        "CBSR_V0_11_SCORECARD.md": OUT / "FINAL_SCORECARD.md",
    }
    for target_name, source_path in copies.items():
        content = source_path.read_text(encoding="utf-8")
        if target_name == "AGENTICFI_EVALUATION_REPORT.md":
            content = content.replace("(pilots/", "(../../research/pilots/")
        (DOC_OUT / target_name).write_text(content, encoding="utf-8", newline="\n")
    claims = _json("research/claims/claims_ledger.json")
    claims_md = [
        "# Claims ledger delivery contract", "",
        f"Claims: **{claims['claim_count']}**. Independent review: **{claims['independent_review_status']}**.", "",
        "Canonical machine-readable files: `research/claims/claims_ledger.csv` and `research/claims/claims_ledger.json`.", "",
        "Every row contains claim text/type, record/evidence locator, freshness, reviewer, second reviewer, review date, status, strength, allowed use, uncertainty and limitation. Blank reviewer fields remain blank; no automated process may convert them into an independent attestation.", "",
        "Verification: `python tools/verify_research_delivery.py`.", "",
    ]
    (DOC_OUT / "CLAIMS_LEDGER.md").write_text("\n".join(claims_md), encoding="utf-8", newline="\n")
    release_notes = """# CBSR v0.11.0 release notes draft

Status: **draft; not released; not release-ready**.

This candidate adds versioned evidence/review fields, modular MCP policy architecture, deterministic receipts, two controlled AgenticFi pilots, complete local research and governance contracts, reproducible package verification and explicit migration/rollback material. Legacy `cbsr_mcp.server` data symbols remain compatible aliases.

Breaking semantic change: structural citability is not legal currentness. Consumers must use freshness, source disposition, review stage and decision-ready fields and must fail on unknown schema versions.

Known blocking gates: zero decision-ready records, no independent second legal review, incomplete event/source research, no independent coding/peer/security review, no remote GitHub/Windows/ruleset readback and no signed release provenance. Do not publish, tag or announce until `delivery/external_gates.json` is closed with real evidence.
"""
    (DOC_OUT / "RELEASE_NOTES_v0.11.0_DRAFT.md").write_text(release_notes, encoding="utf-8", newline="\n")

    # Manifest covers formal delivery inputs without hashing itself, avoiding a
    # self-referential digest. Package artifacts are verified later by verifier.
    key_paths = [
        "analysis/dpg_evidence_matrix.json", "analysis/sdg_mapping.json", "analysis/gdc_mapping.json",
        "analysis/dpi_safeguards_mapping.json", "research/research_manifest.json",
        "research/agenticfi_evaluation.json", "docs/whitepaper/CBSR_AGENTICFI_POLICY_INFRASTRUCTURE.md",
        "DPG_STANDARD.md", "GOVERNANCE.md", "SECURITY.md", "PRIVACY.md",
    ]
    key_paths += [
        path.relative_to(ROOT).as_posix()
        for path in sorted(
            DOC_OUT.iterdir(), key=lambda item: item.relative_to(ROOT).as_posix()
        )
        if path.is_file()
    ]
    key_paths += [
        path.relative_to(ROOT).as_posix()
        for path in sorted(
            (ROOT / "docs/governance").iterdir(),
            key=lambda item: item.relative_to(ROOT).as_posix(),
        )
        if path.is_file()
    ]
    key_paths += [
        f"delivery/{path.name}"
        for path in sorted(
            OUT.iterdir(), key=lambda item: item.relative_to(ROOT).as_posix()
        )
        if path.is_file() and path.name != "delivery_manifest.json"
    ]
    manifest_rows = []
    for relative in sorted(set(key_paths)):
        path = ROOT / relative
        manifest_rows.append({"path": relative, "bytes": path.stat().st_size, "sha256": _sha(path)})
    _write_json("delivery_manifest.json", {
        "schema": "cbsr/delivery-manifest/v1", "as_of": AS_OF,
        "files": manifest_rows, "file_count": len(manifest_rows),
        "package_evidence": "generated after delivery validation by python -m tools.verify",
        "external_gates": "delivery/external_gates.json",
    })
    print(f"delivery reports generated: {len(risk_rows)} risks, {len(decision_rows)} decisions, {len(manifest_rows)} manifest files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
