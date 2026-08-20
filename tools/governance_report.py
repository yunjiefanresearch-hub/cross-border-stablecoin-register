#!/usr/bin/env python3
"""Generate deterministic public-interest and governance evidence mappings.

These files are repository self-assessments.  They deliberately separate a
control implemented in this checkout from an external determination, remote
GitHub configuration, independent review, or causal-impact claim.
"""
from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import csv
import io
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
AS_OF = "2026-08-20"
DPG_SOURCE = "https://www.digitalpublicgoods.net/standard"
SDG_SOURCE = "https://sdgs.un.org/goals"
GDC_SOURCE = "https://www.un.org/pact-for-the-future/en/annex-i-global-digital-compact"
DPI_SOURCE = "https://www.dpi-safeguards.org/assessments"


def _write_json(relative: str, payload: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_csv(relative: str, rows: list[dict[str, object]], fields: list[str]) -> None:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stream.getvalue(), encoding="utf-8")


def _dpg() -> list[dict[str, object]]:
    specifications = [
        ("1", "SDG Relevance", "Partial", ["analysis/sdg_mapping.json", "research/claims/claims_ledger.csv"],
         "No causal-impact evaluation or UN/DPGA determination."),
        ("2", "Open Licencing", "Met", ["LICENSE", "LICENSE-DATA", "LICENSE-CODE", "README.md"],
         "Licence notices still require release-by-release verification."),
        ("3", "Clear Ownership", "Partial", ["CITATION.cff", ".github/CODEOWNERS", "GOVERNANCE.md"],
         "CODEOWNERS is committed, but repository-side enforcement requires remote ruleset readback."),
        ("4", "Platform Independence", "Partial", ["pyproject.toml", "constraints/dev.txt", ".github/workflows/build.yml"],
         "Linux local evidence exists; remote Python 3.10-3.13 and Windows evidence remain external gates."),
        ("5", "Documentation", "Partial", ["README.md", "MCP_SERVER.md", "LOCAL_DEPLOY_WINDOWS.md"],
         "Independent usability testing has not been completed."),
        ("6", "Non-PII Data Extraction", "Met", ["PRIVACY.md", "api/records.json", "dataset.json"],
         "The public dataset contains regulatory research; downstream action payloads can contain sensitive data."),
        ("7", "Privacy & Applicable Laws", "Partial", ["PRIVACY.md", "docs/security/THREAT_MODEL.md"],
         "Applicability depends on deployment context and must be assessed by the downstream operator."),
        ("8", "Open Standards & Best Practices", "Partial", ["record.schema.json", "schemas/policy-action.v1.schema.json", "server.json"],
         "External interoperability certification has not been performed."),
        ("9A", "Data Privacy & Security", "Partial", ["SECURITY.md", ".github/workflows/security.yml", "dist/cbsr-0.11.0.cdx.json"],
         "Local controls exist; independent security assessment and remote workflow evidence remain pending."),
        ("9B", "Inappropriate & Illegal Content", "Partial", ["CODE_OF_CONDUCT.md", "GOVERNANCE.md", ".github/ISSUE_TEMPLATE/config.yml"],
         "Moderation operation evidence does not yet exist."),
        ("9C", "Protection from Harassment", "Partial", ["CODE_OF_CONDUCT.md", ".github/ISSUE_TEMPLATE/config.yml"],
         "Enforcement effectiveness has not been independently evaluated."),
    ]
    rows = []
    for indicator, title, status, evidence, limitation in specifications:
        rows.append({
            "indicator": indicator,
            "title": title,
            "status": status,
            "evidence_files": evidence,
            "owner_role": "maintainer",
            "reviewed_date": AS_OF,
            "target_date": "before-v0.11.0-release" if status != "Met" else "continuous",
            "verification_command": "python -m tools.verify",
            "limitations": limitation,
            "interpretation": "Repository evidence is assessed against this indicator without implying certification or external assurance.",
            "next_action": "Close the stated limitation, retain dated evidence, and obtain the applicable independent or remote readback before submission.",
            "official_reference": DPG_SOURCE,
            "external_determination": False,
        })
    return rows


def _sdg() -> list[dict[str, object]]:
    # Target text follows the UN target wording; alignment remains a project
    # design hypothesis and is not an impact result.
    specifications = [
        ("primary", "9.1", "Develop quality, reliable, sustainable and resilient infrastructure, including regional and transborder infrastructure, to support economic development and human well-being, with a focus on affordable and equitable access for all.", "Open, reproducible cross-border policy infrastructure may reduce regulatory-information friction."),
        ("secondary", "8.10", "Strengthen the capacity of domestic financial institutions to encourage and expand access to banking, insurance and financial services for all.", "Structured policy evidence may support responsible financial-service design; no access outcome is measured."),
        ("secondary", "16.4", "By 2030, significantly reduce illicit financial and arms flows, strengthen the recovery and return of stolen assets and combat all forms of organized crime.", "AML/KYC and prohibition evidence can be preserved in decision receipts; no illicit-flow reduction is attributed."),
        ("primary", "16.6", "Develop effective, accountable and transparent institutions at all levels.", "Pinpointed evidence, deterministic rules and auditable receipts support transparency and accountability."),
        ("primary", "16.10", "Ensure public access to information and protect fundamental freedoms, in accordance with national legislation and international agreements.", "Open licensing and machine-readable public regulatory sources support information access."),
        ("primary", "17.18", "By 2020, enhance capacity-building support to developing countries, including for least developed countries and small island developing States, to increase significantly the availability of high-quality, timely and reliable data disaggregated by income, gender, age, race, ethnicity, migratory status, disability, geographic location and other characteristics relevant in national contexts.", "CBSR targets timely, source-traceable jurisdictional data; it does not currently collect the listed population disaggregations."),
    ]
    rows = []
    for priority, target, official_text, alignment in specifications:
        rows.append({
            "priority": priority,
            "sdg": target.split(".", 1)[0],
            "target": target,
            "official_target_text": official_text,
            "alignment": alignment,
            "evidence": ["dataset.json", "research/claims/claims_ledger.csv", "research/quantitative/jurisdiction_metrics.csv"],
            "measurement_status": "not_evaluated",
            "causal_claim": False,
            "measurable_project_indicator": {
                "metric": f"documented evidence rows aligned to SDG target {target}",
                "baseline": 0,
                "current": 1,
                "unit": "repository mapping rows",
                "outcome_measurement": "not_evaluated",
            },
            "claim_strength": "design_alignment_only",
            "causal_limitation": "Repository controls cannot establish that CBSR caused progress on this SDG target.",
            "data_limitation": "The project measures repository outputs only; no beneficiary, institutional-outcome or population data are collected.",
            "owner_role": "maintainer",
            "reviewed_date": AS_OF,
            "target_date": "before-impact-claim",
            "verification_command": "python tools/verify_governance_delivery.py",
            "official_reference": f"{SDG_SOURCE}/goal{target.split('.', 1)[0]}",
        })
    return rows


def _gdc() -> list[dict[str, object]]:
    specifications = [
        ("human-rights", "Anchor digital cooperation in international law and human rights", ["PRIVACY.md", "CODE_OF_CONDUCT.md"], "Partial", "A deployment-specific human-rights impact assessment is not complete."),
        ("digital-inclusion", "Close digital divides and advance an inclusive digital economy", ["README.md", "DPG_STANDARD.md"], "Partial", "Accessibility and user outcome testing remain pending."),
        ("data-governance", "Advance responsible, equitable and interoperable data governance", ["record.schema.json", "PRIVACY.md", "research/research_manifest.json"], "Partial", "No external governance assessment has been completed."),
        ("safe-secure", "Advance a safe and secure digital space", ["SECURITY.md", "docs/security/THREAT_MODEL.md", ".github/workflows/security.yml"], "Partial", "Independent security review and remote workflow evidence remain pending."),
        ("digital-public-infrastructure", "Develop safe, inclusive and interoperable digital public infrastructure", ["analysis/dpi_safeguards_mapping.json", "schemas/domain-pack.v1.schema.json"], "Partial", "CBSR is a policy-data component, not a national DPI deployment."),
        ("accountability", "Promote transparency, accountability and human oversight", ["GOVERNANCE.md", "src/cbsr_mcp/receipts.py", "research/agenticfi_evaluation.json"], "Partial", "Receipts are unsigned and never authorize execution."),
    ]
    return [{
        "commitment_id": identifier,
        "commitment": commitment,
        "status": status,
        "evidence_files": evidence,
        "owner_role": "maintainer",
        "reviewed_date": AS_OF,
        "target_date": "before-v0.11.0-release",
        "verification_command": "python -m tools.verify",
        "limitations": limitation,
        "official_reference": GDC_SOURCE,
        "external_determination": False,
    } for identifier, commitment, evidence, status, limitation in specifications]


def _dpi() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    principles = [
        ("F1", "Do no harm"), ("F2", "Do not discriminate"), ("F3", "Do not exclude"),
        ("F4", "Reinforce transparency and accountability"), ("F5", "Uphold the rule of law"),
        ("F6", "Promote autonomy and agency"), ("F7", "Foster community engagement"),
        ("F8", "Ensure effective remedy and redress"), ("F9", "Focus on future sustainability"),
        ("O1", "Leverage market dynamics"), ("O2", "Evolve with evidence"),
        ("O3", "Ensure data privacy by design"), ("O4", "Assure data security by design"),
        ("O5", "Ensure data protection during use"), ("O6", "Respond to gender, ability or age"),
        ("O7", "Practice inclusive governance"), ("O8", "Sustain financial viability"),
        ("O9", "Build and share open assets"),
    ]
    evidence_by_id = {
        "F1": ["src/cbsr_mcp/policy.py", "GOVERNANCE.md"],
        "F2": ["CODE_OF_CONDUCT.md", "analysis/sdg_mapping.json"],
        "F3": ["README.md", "analysis/sdg_mapping.json"],
        "F4": ["src/cbsr_mcp/receipts.py", "research/claims/claims_ledger.csv"],
        "F5": ["research/source_ledger_2026-08-20.csv", "record.schema.json"],
        "F6": ["src/cbsr_mcp/core/models.py", "PRIVACY.md"],
        "F7": ["CONTRIBUTING.md", ".github/ISSUE_TEMPLATE/data-source.yml"],
        "F8": ["SECURITY.md", ".github/ISSUE_TEMPLATE/regulatory-correction.yml"],
        "F9": ["constraints/dev.txt", "delivery/RISK_REGISTER.md"],
        "O1": ["LICENSE", "GOVERNANCE.md"],
        "O2": ["analysis/freshness_report.json", "tools/verify.py"],
        "O3": ["PRIVACY.md", "schemas/policy-action.v1.schema.json"],
        "O4": ["SECURITY.md", ".github/workflows/codeql.yml"],
        "O5": ["PRIVACY.md", "docs/security/THREAT_MODEL.md"],
        "O6": ["CODE_OF_CONDUCT.md", "analysis/sdg_mapping.json"],
        "O7": ["GOVERNANCE.md", "CONTRIBUTING.md"],
        "O8": ["GOVERNANCE.md", "delivery/RISK_REGISTER.md"],
        "O9": ["LICENSE", "LICENSE-DATA", "LICENSE-CODE", "schemas/domain-pack.v1.schema.json"],
    }
    rows = []
    for identifier, title in principles:
        met = identifier in {"F4", "O2", "O9"}
        rows.append({
            "principle_id": identifier,
            "principle": title,
            "status": "Met" if met else "Partial",
            "evidence_files": evidence_by_id[identifier],
            "owner_role": "maintainer",
            "reviewed_date": AS_OF,
            "target_date": "continuous" if met else "before-production-deployment",
            "verification_command": "python -m tools.verify",
            "residual_gap": "No external DPI safeguard assessment." if met else "Deployment-specific assessment and independent review remain pending.",
            "official_reference": DPI_SOURCE,
            "external_determination": False,
        })
    risks = [
        ("privacy-vulnerability", "Privacy vulnerability", ["O3", "O5"]),
        ("digital-insecurity", "Digital insecurity", ["O4"]),
        ("physical-insecurity", "Physical insecurity", ["F1", "O4"]),
        ("lack-of-recourse", "Lack of recourse", ["F8"]),
        ("discrimination", "Discrimination", ["F2", "O6"]),
        ("unequal-access", "Unequal access", ["F3", "O6"]),
        ("exclusion", "Exclusion", ["F3", "F7"]),
        ("disempowerment", "Disempowerment", ["F6"]),
        ("digital-distrust", "Digital distrust", ["F4", "F7"]),
        ("weak-rule-of-law", "Weak rule of law", ["F5"]),
        ("weak-institutions", "Weak institutions", ["F4", "O7"]),
        ("technical-shortcomings", "Technical shortcomings", ["O2", "O4"]),
        ("unsustainability", "Unsustainability", ["F9", "O8"]),
    ]
    risk_rows = [{
        "risk_id": identifier,
        "risk": title,
        "linked_principles": linked,
        "repository_controls": sorted({item for pid in linked for item in evidence_by_id[pid]}),
        "residual_risk": "not independently assessed",
        "owner_role": "maintainer",
        "reviewed_date": AS_OF,
        "target_date": "before-production-deployment",
        "verification_command": "python -m tools.verify",
        "official_reference": DPI_SOURCE,
    } for identifier, title, linked in risks]
    return rows, risk_rows


def _markdown_table(rows: list[dict[str, object]], id_key: str, title_key: str) -> str:
    lines = ["| ID | Requirement | Status | Evidence | Residual limitation |", "|---|---|---|---|---|"]
    for row in rows:
        limitation = row.get("limitations", row.get("residual_gap", ""))
        evidence = ", ".join(f"`{value}`" for value in row["evidence_files"])
        lines.append(f"| {row[id_key]} | {row[title_key]} | {row['status']} | {evidence} | {limitation} |")
    return "\n".join(lines)


def main() -> int:
    dpg = _dpg()
    sdg = _sdg()
    gdc = _gdc()
    dpi, risks = _dpi()
    _write_json("analysis/dpg_evidence_matrix.json", {
        "schema": "cbsr/dpg-evidence-matrix/v2", "as_of": AS_OF,
        "assessment_type": "repository self-assessment; not a DPGA determination",
        "official_reference": DPG_SOURCE, "indicators": dpg,
    })
    _write_csv("analysis/dpg_evidence_matrix.csv", dpg,
               ["indicator", "title", "status", "owner_role", "reviewed_date", "target_date", "verification_command", "interpretation", "next_action", "limitations", "official_reference"])
    _write_json("analysis/sdg_mapping.json", {
        "schema": "cbsr/sdg-alignment/v2", "as_of": AS_OF,
        "claim": "design alignment only; no causal impact, compliance or UN endorsement claim",
        "mappings": sdg,
    })
    _write_json("analysis/gdc_mapping.json", {
        "schema": "cbsr/gdc-alignment/v1", "as_of": AS_OF,
        "assessment_type": "design alignment self-assessment; no UN endorsement", "mappings": gdc,
    })
    _write_json("analysis/dpi_safeguards_mapping.json", {
        "schema": "cbsr/dpi-safeguards/v1", "as_of": AS_OF,
        "assessment_type": "repository self-assessment; not an official DPI safeguards assessment",
        "principles": dpi, "risks": risks,
    })
    dpg_md = """# Digital Public Goods readiness evidence matrix

This is a repository self-assessment against the Digital Public Goods Standard. It is **not** a DPGA determination, DPG certification, submission, or compliance claim. `Met` means the cited repository control exists; it does not convert a repository assertion into external assurance.

""" + _markdown_table(dpg, "indicator", "title") + f"""

Each row is owned by the maintainer, was reviewed on {AS_OF}, and is rechecked by `python -m tools.verify`. Machine-readable owner, date, target, command and limitations are in `analysis/dpg_evidence_matrix.json`.

Official reference: {DPG_SOURCE}
"""
    (ROOT / "DPG_STANDARD.md").write_text(dpg_md, encoding="utf-8")
    gdc_md = "# Global Digital Compact design-alignment mapping\n\nNo UN endorsement or conformance determination is claimed.\n\n" + _markdown_table(gdc, "commitment_id", "commitment") + f"\n\nOfficial reference: {GDC_SOURCE}\n"
    (ROOT / "analysis/gdc_mapping.md").write_text(gdc_md, encoding="utf-8")
    dpi_md = "# Universal DPI Safeguards self-assessment\n\nThis is not an official safeguards assessment. It records repository controls and residual deployment gaps.\n\n" + _markdown_table(dpi, "principle_id", "principle")
    dpi_md += "\n\n## Risk linkage\n\n| Risk | Linked principles | Residual risk |\n|---|---|---|\n"
    for row in risks:
        dpi_md += f"| {row['risk']} | {', '.join(row['linked_principles'])} | {row['residual_risk']} |\n"
    dpi_md += f"\nOfficial reference: {DPI_SOURCE}\n"
    (ROOT / "analysis/dpi_safeguards_mapping.md").write_text(dpi_md, encoding="utf-8")
    governance = ROOT / "docs/governance"
    governance.mkdir(parents=True, exist_ok=True)
    submission = [
        "# DPG submission-readiness package", "",
        "Status: **not submitted; external determination not requested**.", "",
        "This package assembles repository evidence only. It must not be sent to DPGA until legal, security, governance, remote-CI and accessibility gates are closed by their named owners.", "",
        "## Evidence index", "",
        "- Indicator matrix: `analysis/dpg_evidence_matrix.json` and CSV.",
        "- Licensing: `LICENSE`, `LICENSE-CODE`, `LICENSE-DATA`.",
        "- Ownership and governance: `GOVERNANCE.md`, `CITATION.cff`, `.github/CODEOWNERS`.",
        "- Privacy and security: `PRIVACY.md`, `SECURITY.md`, `docs/security/THREAT_MODEL.md`.",
        "- Public-interest mappings: `analysis/sdg_mapping.json`, `analysis/gdc_mapping.json`, `analysis/dpi_safeguards_mapping.json`.",
        "- Reproducibility: `tools/verify.py`, constraints, SBOM, package-smoke and compatibility evidence.", "",
        "## Submission hard gates", "",
        "1. Replace every Partial row with dated closure evidence or retain a justified limitation.",
        "2. Complete independent legal, security, accessibility and scholarly review.",
        "3. Retain actual GitHub Actions, ruleset, Windows and provenance readback.",
        "4. Obtain maintainer approval for an external submission; no automation may submit it.",
        "5. Record the submitted revision, date, recipient and response without rewriting repository history.", "",
    ]
    (governance / "DPG_SUBMISSION_READINESS.md").write_text("\n".join(submission), encoding="utf-8")
    openssf = """# OpenSSF readiness checklist

This is a local readiness inventory, not an OpenSSF badge, score or external assessment.

| Control | Repository evidence | External evidence still required |
|---|---|---|
| Maintained build | `tools/verify.py`, `constraints/` | Successful required remote checks |
| Code review | `CODEOWNERS`, PR template | Ruleset readback and actual review record |
| Vulnerability disclosure | `SECURITY.md` | Private reporting enabled and response evidence |
| Dependency management | constraints and dependency-refresh workflow | Dependabot/dependency-review run readback |
| Static analysis | CodeQL workflow | Successful CodeQL run and reviewed findings |
| Secret protection | local secret scan and security workflow | GitHub secret scanning/push protection readback |
| SBOM and provenance | CycloneDX generator and provenance workflow | Signed release attestation readback |
| Security review | external-review template | Independent reviewer attestation |

Run `python -m tools.verify`; then complete the remote and human evidence columns before making a readiness claim.
"""
    (governance / "OPENSSF_READINESS.md").write_text(openssf, encoding="utf-8")
    archival = """# Archival and persistent-identifier plan

No DOI, archive deposit or Software Heritage snapshot is created by this repository build.

1. Freeze a verified source revision and record its Git SHA, dataset version and canonical verifier summary.
2. Create the signed release only after all release hard gates close; attach ZIP, wheel, SBOM, licence inventory, provenance and SHA256SUMS.
3. Request a Software Heritage save for the public repository and retain the resulting SWHID after readback.
4. Deposit the same immutable artifacts with an authorized archival service and reserve/mint a DOI only with maintainer approval.
5. Update `CITATION.cff` and release metadata with the actual DOI/SWHID; never insert placeholders presented as issued identifiers.
6. Test that the archive resolves and that checksums match before announcing persistence.

Historic identifiers are immutable. Corrections create a new version and link supersession; they never overwrite the archived object.
"""
    (governance / "ARCHIVAL_AND_PERSISTENT_IDENTIFIERS.md").write_text(archival, encoding="utf-8")
    fair = """# FAIR metadata and versioning note

CBSR supports findability and interoperability through stable record IDs, schema IDs, `CITATION.cff`, versioned JSON schemas, machine-readable manifests and explicit licences. Accessibility is supported by open formats and source URLs, but source availability and language remain uneven. Reuse is bounded by provenance, freshness, review and non-legal-advice fields.

Versions follow semantic release identifiers for software and immutable dataset snapshots for citation. Every derived artifact records or inherits the dataset version. Unknown schemas must fail closed. A migration must preserve record IDs, review history and supersession links; rollback restores a complete immutable artifact rather than mixing generated files across versions.

This note is a repository design statement, not a FAIR certification or measured FAIR maturity score.
"""
    (governance / "FAIR_METADATA_AND_VERSIONING.md").write_text(fair, encoding="utf-8")
    print(f"governance mappings generated: {len(dpg)} DPG indicators, {len(sdg)} SDG targets, {len(dpi)} DPI principles, {len(risks)} risks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
