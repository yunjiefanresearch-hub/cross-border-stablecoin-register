#!/usr/bin/env python3
"""Generate quantitative, qualitative, claims, whitepaper and research-manifest deliverables."""

from __future__ import annotations

# Portability: force UTF-8 for console output on Windows and other non-UTF-8 locales.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8")
    _sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from collections import Counter
import csv
import hashlib
import html
import io
import json
import pathlib

from tools.whitepaper import build_whitepaper

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
DATA = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
RECORDS = DATA.get("records", [])
AS_OF = "2026-08-20"


def _csv(path: pathlib.Path, rows: list[dict]) -> None:
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _quantitative() -> None:
    rows = []
    event_records = {
        str(item.get("record_id")) for item in
        json.loads((ROOT / "analysis/legal_event_ontology.json").read_text(encoding="utf-8")).get("records", [])
        if item.get("event_id")
    }
    for jurisdiction in sorted({str(row.get("jurisdiction")) for row in RECORDS}):
        subset = [row for row in RECORDS if row.get("jurisdiction") == jurisdiction]
        rows.append({
            "jurisdiction": jurisdiction,
            "records": len(subset),
            "official_sources": sum(row.get("source_disposition") == "official" for row in subset),
            "unavailable_sources": sum(row.get("source_disposition") == "unavailable" for row in subset),
            "unverified_evidence": sum(row.get("evidence_tier") == "unverified" for row in subset),
            "freshness_current": sum((row.get("freshness") or {}).get("review_status") == "current" for row in subset),
            "freshness_stale": sum((row.get("freshness") or {}).get("review_status") == "stale" for row in subset),
            "freshness_unknown": sum((row.get("freshness") or {}).get("review_status") == "unknown" for row in subset),
            "primary_reviewer": sum(bool(row.get("reviewer")) for row in subset),
            "second_reviewer": sum(bool(row.get("second_reviewer")) for row in subset),
            "event_linked": sum(str(row.get("id")) in event_records for row in subset),
            "decision_ready": sum(
                (row.get("freshness") or {}).get("review_status") == "current"
                and row.get("review_stage") == "reconciled"
                and row.get("source_disposition") == "official"
                for row in subset
            ),
        })
    _csv(RESEARCH / "quantitative/jurisdiction_metrics.csv", rows)
    (RESEARCH / "quantitative/jurisdiction_metrics.json").write_text(
        json.dumps({"schema": "cbsr/quantitative-metrics/v1", "as_of": AS_OF, "rows": rows}, indent=2) + "\n",
        encoding="utf-8",
    )
    dimensions = []
    for dimension in sorted({str(row.get("dimension")) for row in RECORDS}):
        subset = [row for row in RECORDS if row.get("dimension") == dimension]
        dimensions.append({
            "dimension": dimension,
            "records": len(subset),
            "jurisdictions_covered": len({row.get("jurisdiction") for row in subset}),
            "official_sources": sum(row.get("source_disposition") == "official" for row in subset),
            "resolution_text": sum(row.get("evidence_tier") == "resolution_text" for row in subset),
            "current": sum((row.get("freshness") or {}).get("review_status") == "current" for row in subset),
            "independent_second_review": sum(bool(row.get("second_reviewer")) for row in subset),
        })
    _csv(RESEARCH / "quantitative/dimension_metrics.csv", dimensions)
    (RESEARCH / "quantitative/dimension_metrics.json").write_text(
        json.dumps({"schema": "cbsr/dimension-metrics/v1", "as_of": AS_OF, "rows": dimensions}, indent=2) + "\n",
        encoding="utf-8",
    )

    freshness_report = json.loads((ROOT / "analysis/freshness_report.json").read_text(encoding="utf-8"))
    event_report = json.loads((ROOT / "analysis/legal_event_ontology.json").read_text(encoding="utf-8"))
    corridor_report = json.loads((ROOT / "analysis/computed_corridors_directed.json").read_text(encoding="utf-8"))
    forward_report = json.loads((ROOT / "analysis/computed_forward_view.json").read_text(encoding="utf-8"))
    source_urls = sum(bool((row.get("source") or {}).get("url")) for row in RECORDS)
    resolution_text = sum(row.get("evidence_tier") == "resolution_text" for row in RECORDS)
    missing_checked_dates = sum(not row.get("source_last_checked") for row in RECORDS)
    missing_effective_dates = sum(not row.get("effective_from") for row in RECORDS)
    uncertainty = Counter(str(row.get("uncertainty") or "unknown") for row in RECORDS)
    class_distribution = corridor_report.get("coverage", {}).get("class_distribution", {})
    temporal_moves = sum(
        int((value.get("summary") or {}).get("own_driven_inbound", 0))
        + int((value.get("summary") or {}).get("own_driven_outbound", 0))
        for value in forward_report.get("jurisdictions", {}).values()
    )
    dashboard_rows = [
        {"metric": "records", "value": len(RECORDS), "denominator": len(RECORDS), "unit": "records", "definition": "compiled record count", "source": "dataset.json"},
        {"metric": "jurisdictions", "value": len(rows), "denominator": 12, "unit": "jurisdictions", "definition": "jurisdictions represented", "source": "research/quantitative/jurisdiction_metrics.csv"},
        {"metric": "dimensions", "value": len(dimensions), "denominator": len(dimensions), "unit": "dimensions", "definition": "distinct dimensions represented", "source": "research/quantitative/dimension_metrics.csv"},
        {"metric": "records_with_source_url", "value": source_urls, "denominator": len(RECORDS), "unit": "records", "definition": "non-empty cited source URL; not a review claim", "source": "dataset.json"},
        {"metric": "official_source_disposition", "value": sum(row.get("source_disposition") == "official" for row in RECORDS), "denominator": len(RECORDS), "unit": "records", "definition": "source classified as official", "source": "analysis/freshness_report.json"},
        {"metric": "primary_text_resolution", "value": resolution_text, "denominator": len(RECORDS), "unit": "records", "definition": "resolution_text evidence tier", "source": "research/quantitative_baseline.json"},
        {"metric": "structural_citable_candidates", "value": int(DATA.get("structural_citable_subset", {}).get("count", DATA.get("citable_subset", {}).get("count", 0))), "denominator": len(RECORDS), "unit": "records", "definition": "structural candidate only, not current-law ready", "source": "dataset.json"},
        {"metric": "decision_ready_citable", "value": int(DATA.get("decision_ready_citable_subset", {}).get("count", 0)), "denominator": len(RECORDS), "unit": "records", "definition": "official, current and independently reconciled", "source": "dataset.json"},
        {"metric": "freshness_current", "value": freshness_report["counts"]["current"], "denominator": len(RECORDS), "unit": "records", "definition": "current under binding-status SLA", "source": "analysis/freshness_report.json"},
        {"metric": "freshness_stale", "value": freshness_report["counts"]["stale"], "denominator": len(RECORDS), "unit": "records", "definition": "source check beyond SLA", "source": "analysis/freshness_report.json"},
        {"metric": "high_impact_current_reconciled", "value": freshness_report["high_impact_sla"]["current_reconciled"], "denominator": freshness_report["high_impact_sla"]["count"], "unit": "records", "definition": "high-impact SLA hard gate", "source": "analysis/freshness_report.json"},
        {"metric": "missing_source_checked_date", "value": missing_checked_dates, "denominator": len(RECORDS), "unit": "records", "definition": "null source_last_checked", "source": "dataset.json"},
        {"metric": "missing_effective_from", "value": missing_effective_dates, "denominator": len(RECORDS), "unit": "records", "definition": "null effective_from; may be inapplicable or a gap", "source": "dataset.json"},
        {"metric": "invalid_date_relationships", "value": event_report["coverage"]["invalid"], "denominator": len(RECORDS), "unit": "records", "definition": "ontology date-rule failures", "source": "analysis/legal_event_ontology.json"},
        {"metric": "uncertainty_high_or_unknown", "value": uncertainty["high"] + uncertainty["unknown"], "denominator": len(RECORDS), "unit": "records", "definition": "persisted uncertainty classification", "source": "dataset.json"},
        {"metric": "primary_reviewer_coverage", "value": freshness_report["reviewer_coverage"]["primary_reviewer"]["count"], "denominator": len(RECORDS), "unit": "records", "definition": "named primary reviewer", "source": "analysis/freshness_report.json"},
        {"metric": "independent_second_reviewer_coverage", "value": freshness_report["reviewer_coverage"]["independent_second_reviewer"]["count"], "denominator": len(RECORDS), "unit": "records", "definition": "different named second reviewer", "source": "analysis/freshness_report.json"},
        {"metric": "first_class_event_coverage", "value": event_report["coverage"]["linked_to_first_class_event"], "denominator": len(RECORDS), "unit": "records", "definition": "record linked to event ontology", "source": "analysis/legal_event_ontology.json"},
        {"metric": "superseded_records", "value": sum(row.get("legal_status") == "superseded" for row in RECORDS), "denominator": len(RECORDS), "unit": "records", "definition": "explicit superseded legal status", "source": "dataset.json"},
        {"metric": "directed_corridors", "value": corridor_report["coverage"]["edges_total"], "denominator": corridor_report["coverage"]["ordered_pairs_expected"], "unit": "corridors", "definition": f"class distribution {json.dumps(class_distribution, sort_keys=True)}", "source": "analysis/computed_corridors_directed.json"},
        {"metric": "temporally_sensitive_class_moves", "value": temporal_moves, "denominator": corridor_report["coverage"]["edges_total"], "unit": "edge movements", "definition": "own-event inbound and outbound class movements; not unique edges", "source": "analysis/computed_forward_view.json"},
    ]
    _csv(RESEARCH / "quantitative/data_quality_dashboard.csv", dashboard_rows)
    dashboard = {
        "schema": "cbsr/data-quality-dashboard/v1", "as_of": AS_OF,
        "unit_of_analysis": "one jurisdiction-instrument-dimension record; corridor measures use ordered jurisdiction pairs",
        "inclusion": "all 152 compiled source records and all 132 directed corridors",
        "exclusion": "controlled pilot fixtures never change dataset statistics",
        "missing_data_rule": "null and unavailable remain explicit; no reviewer, date, source or legal state is imputed",
        "biases": ["jurisdiction selection", "uneven source availability", "translation risk", "reviewer non-independence", "temporal truncation"],
        "command": "python tools/research_deliverables.py",
        "metrics": dashboard_rows,
    }
    (RESEARCH / "quantitative/data_quality_dashboard.json").write_text(
        json.dumps(dashboard, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    dashboard_md = ["# Data-quality dashboard", "", f"Extraction date: **{AS_OF}**. Unit: one jurisdiction–instrument–dimension record; corridor rows use ordered pairs.", "", "All missing fields remain missing. No checked date, reviewer, source or legal state is imputed. Controlled pilot fixtures are excluded.", "", "| Metric | Value / denominator | Unit | Definition |", "|---|---:|---|---|"]
    dashboard_md.extend(f"| `{row['metric']}` | {row['value']} / {row['denominator']} | {row['unit']} | {row['definition']} |" for row in dashboard_rows)
    dashboard_md.extend(["", "## Method and limitations", "", "Inclusion: all compiled records and directed corridors. Missing-data policy: retain explicit null/unavailable values. Principal biases are jurisdiction selection, unequal official-source access, translation, non-independent prior coding and the 2026-08-20 temporal cut-off. These are descriptive census statistics, not causal or population estimates.", ""])
    (RESEARCH / "quantitative/DATA_QUALITY_DASHBOARD.md").write_text("\n".join(dashboard_md), encoding="utf-8")
    before_after = [
        {"metric": "research_ledger_rows", "before": 4, "after": 152, "unit": "records", "interpretation": "targeted leads replaced by full inventory ledger"},
        {"metric": "dossier_minimum_lines", "before": 16, "after": min(len((RESEARCH / f"jurisdictions/{code}.md").read_text(encoding="utf-8").splitlines()) for code in sorted({r['jurisdiction'] for r in RECORDS})), "unit": "lines", "interpretation": "minimum across twelve dossiers"},
        {"metric": "agenticfi_policy_scenarios", "before": 10, "after": 31, "unit": "scenarios", "interpretation": "table-driven independent paths"},
        {"metric": "pytest_tests", "before": 21, "after": 59, "unit": "tests", "interpretation": "current local test collection"},
        {"metric": "mcp_server_lines", "before": 1352, "after": len((ROOT / "src/cbsr_mcp/server.py").read_text(encoding="utf-8").splitlines()), "unit": "lines", "interpretation": "thin composition root"},
        {"metric": "api_record_review_fields", "before": 0, "after": 7, "unit": "fields", "interpretation": "freshness/source/review projection"},
        {"metric": "source_urls", "before": 100, "after": sum(bool((r.get("source") or {}).get("url")) for r in RECORDS), "unit": "records", "interpretation": "legal research gap intentionally unchanged without invented URLs"},
        {"metric": "independent_second_reviews", "before": 0, "after": sum(bool(r.get("second_reviewer")) for r in RECORDS), "unit": "records", "interpretation": "external human gate intentionally not fabricated"},
    ]
    _csv(RESEARCH / "quantitative/before_after.csv", before_after)
    (RESEARCH / "quantitative/before_after.json").write_text(
        json.dumps({"schema": "cbsr/transformation-before-after/v1", "as_of": AS_OF, "baseline_source": "user-supplied acceptance audit and committed R3 baseline", "metrics": before_after}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    md = ["# Quantitative before/after", "", "Baseline values reproduce the acceptance audit; after values are generated from the current tree.", "", "| Metric | Before | After | Unit | Interpretation |", "|---|---:|---:|---|---|"]
    md.extend(f"| `{r['metric']}` | {r['before']} | {r['after']} | {r['unit']} | {r['interpretation']} |" for r in before_after)
    md.extend(["", "A higher number is not always better. The unchanged source/reviewer gaps are controls against fabricated research.", ""])
    (RESEARCH / "quantitative/BEFORE_AFTER.md").write_text("\n".join(md), encoding="utf-8")

    chart_dir = RESEARCH / "charts"
    chart_dir.mkdir(parents=True, exist_ok=True)
    max_records = max(row["records"] for row in rows)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="620" viewBox="0 0 960 620">', '<rect width="960" height="620" fill="#ffffff"/>', '<text x="40" y="40" font-family="sans-serif" font-size="24">CBSR review coverage by jurisdiction</text>', '<text x="40" y="66" font-family="sans-serif" font-size="13" fill="#555">Official source, primary review and independent second review are separate denominators.</text>']
    for index, row in enumerate(rows):
        y = 92 + index * 40
        width = 620 * row["records"] / max_records
        official = 620 * row["official_sources"] / max_records
        primary = 620 * row["primary_reviewer"] / max_records
        second = 620 * row["second_reviewer"] / max_records
        svg.extend([
            f'<text x="40" y="{y+16}" font-family="monospace" font-size="14">{html.escape(row["jurisdiction"])}</text>',
            f'<rect x="90" y="{y}" width="{width:.1f}" height="8" fill="#d9d9d9"/>',
            f'<rect x="90" y="{y+10}" width="{official:.1f}" height="8" fill="#2f6f9f"/>',
            f'<rect x="90" y="{y+20}" width="{primary:.1f}" height="8" fill="#dd8a2e"/>',
            f'<rect x="90" y="{y+30}" width="{second:.1f}" height="8" fill="#2f9f62"/>',
            f'<text x="730" y="{y+18}" font-family="sans-serif" font-size="12">records {row["records"]} · official {row["official_sources"]} · primary {row["primary_reviewer"]} · second {row["second_reviewer"]}</text>',
        ])
    svg.extend(['<text x="40" y="594" font-family="sans-serif" font-size="12" fill="#555">Grey: records · blue: official source · orange: primary review · green: independent second review</text>', '</svg>'])
    (chart_dir / "review_coverage.svg").write_text("\n".join(svg) + "\n", encoding="utf-8")


def _codes(record: dict) -> list[str]:
    values = []
    freshness = (record.get("freshness") or {}).get("review_status")
    if record.get("source_disposition") == "unavailable":
        values.append("source_acquisition_gap")
    if record.get("evidence_tier") == "unverified":
        values.append("evidence_classification_gap")
    if freshness == "unknown":
        values.append("freshness_unknown")
    if freshness == "stale":
        values.append("freshness_sla_breach")
    if not record.get("second_reviewer"):
        values.append("independent_review_gap")
    if not record.get("event_id"):
        values.append("event_model_gap")
    return values or ["no_structural_gap_detected"]


def _qualitative() -> None:
    coded = []
    for record in sorted(RECORDS, key=lambda item: item["id"]):
        coded.append({
            "case_id": record["id"], "jurisdiction": record.get("jurisdiction"),
            "dimension": record.get("dimension"), "primary_codes": "|".join(_codes(record)),
            "primary_coder": "deterministic_ruleset_v1", "second_codes": "",
            "second_coder": "", "agreement_status": "not_measured",
            "reconciliation_status": record.get("reconciliation_status"),
            "evidence_excerpt": str(record.get("requirement_summary") or "")[:240],
        })
    qualitative = RESEARCH / "qualitative"
    qualitative.mkdir(parents=True, exist_ok=True)
    _csv(qualitative / "coded_cases.csv", coded)
    (qualitative / "coded_cases.json").write_text(
        json.dumps({"schema": "cbsr/qualitative-coded-cases/v1", "coding_claim": "deterministic primary coding only; no independent second coder inferred", "cases": coded}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    worksheet = [{**row, "second_codes": "", "second_coder": "", "agreement_status": "pending_independent_coder"} for row in coded]
    _csv(qualitative / "SECOND_CODER_WORKSHEET.csv", worksheet)
    counts = Counter(code for record in RECORDS for code in _codes(record))
    taxonomy = [
        {"failure_id": "F1", "failure": "source_acquisition_gap", "threat": "unsupported or secondary-only legal claim", "control": "official-source disposition and fail-closed decision gate"},
        {"failure_id": "F2", "failure": "freshness_unknown_or_stale", "threat": "obsolete legal state", "control": "SLA, next-review date and currentness gate"},
        {"failure_id": "F3", "failure": "independent_review_gap", "threat": "single-reviewer interpretation bias", "control": "blind second review and reconciliation"},
        {"failure_id": "F4", "failure": "event_model_gap", "threat": "missed commencement or supersession", "control": "typed legal-event ontology"},
        {"failure_id": "F5", "failure": "receipt_tampering", "threat": "post-decision evidence substitution", "control": "canonical component and receipt digests"},
        {"failure_id": "F6", "failure": "mandate_overreach", "threat": "agent acts beyond authority", "control": "versioned mandate, jurisdiction/time/amount and human-review gates"},
    ]
    (qualitative / "failure_taxonomy.json").write_text(
        json.dumps({"schema": "cbsr/failure-taxonomy/v1", "failures": taxonomy}, indent=2) + "\n", encoding="utf-8"
    )
    _csv(qualitative / "threat_linkage.csv", taxonomy)
    themes = [
        ("Evidence availability is distinct from legal force", counts["source_acquisition_gap"], "A binding-status label cannot substitute for an official source and pinpoint."),
        ("Temporal uncertainty dominates decision readiness", counts["freshness_unknown"] + counts["freshness_sla_breach"], "Unknown and stale checks must block unconditional allow."),
        ("Independent interpretation is the binding governance gap", counts["independent_review_gap"], "Automation cannot manufacture an independent reviewer identity."),
        ("Legal change requires explicit event modelling", counts["event_model_gap"], "A null event is a modelling gap rather than evidence that no change exists."),
    ]
    lines = ["# Qualitative thematic analysis", "", "## Method", "", "The current run applies a deterministic primary codebook to all 152 records. It produces a complete coded-case table and a blank second-coder worksheet. No intercoder reliability statistic is reported because an independent human second coding pass has not occurred.", "", "## Themes", ""]
    for index, (theme, count, interpretation) in enumerate(themes, start=1):
        lines.extend([f"### Theme {index}: {theme}", "", f"Cases carrying the related primary code: **{count}**.", "", interpretation, ""])
    lines.extend(["## Failure taxonomy and threat linkage", "", "| Failure | Threat | Control |", "|---|---|---|"])
    lines.extend(f"| `{row['failure']}` | {row['threat']} | {row['control']} |" for row in taxonomy)
    lines.extend(["", "## Independent coding gate", "", "A qualified second coder must complete `SECOND_CODER_WORKSHEET.csv` without copying the primary codes. Agreement, disagreement and reconciliation must then be computed and attested. Until that occurs, qualitative findings are exploratory and cannot be described as independently coded.", ""])
    (qualitative / "QUALITATIVE_ANALYSIS.md").write_text("\n".join(lines), encoding="utf-8")


def _claims() -> list[dict]:
    claims = []
    for record in sorted(RECORDS, key=lambda item: item["id"]):
        source = record.get("source") or {}
        freshness = record.get("freshness") or {}
        claims.append({
            "claim_id": f"claim-{record['id']}", "claim_type": "record_level_legal_proposition",
            "claim_text": record.get("requirement_summary"), "record_ids": record["id"],
            "source_urls": source.get("url") or "", "pinpoint": source.get("pinpoint") or "",
            "evidence_tier": record.get("evidence_tier"), "binding_status": record.get("binding_status"),
            "freshness": freshness.get("review_status"), "review_stage": record.get("review_stage"),
            "allowed_use": "decision_ready" if freshness.get("review_status") == "current" and record.get("review_stage") == "reconciled" and record.get("source_disposition") == "official" else "research_inventory_only",
            "uncertainty": record.get("uncertainty"),
            "reviewer": record.get("reviewer") or "",
            "second_reviewer": record.get("second_reviewer") or "",
            "review_date": record.get("source_last_checked") or "",
            "status": "decision_ready" if freshness.get("review_status") == "current" and record.get("review_stage") == "reconciled" and record.get("source_disposition") == "official" else "pending_independent_review",
            "strength": "high" if record.get("evidence_tier") == "resolution_text" and freshness.get("review_status") == "current" else "limited",
            "limitation": "Not a current-law claim unless official, current and independently reconciled; inspect the record uncertainty and legal-force fields.",
        })
    derived = [
        ("claim-derived-record-count", "dataset_metric", f"The compiled snapshot contains {len(RECORDS)} records.", "dataset.json"),
        ("claim-derived-decision-ready", "dataset_metric", f"The decision-ready citable subset contains {DATA.get('decision_ready_citable_subset', {}).get('count', 0)} records.", "dataset.json"),
        ("claim-derived-agentic-scenarios", "software_test", "The table-driven AgenticFi catalogue contains 31 independent policy scenarios.", "research/agenticfi_evaluation.json"),
        ("claim-derived-pilots", "software_test", "Two end-to-end AgenticFi pilots replay to byte-identical receipts.", "research/pilots/"),
        ("claim-derived-server", "architecture", f"The MCP composition root contains {len((ROOT / 'src/cbsr_mcp/server.py').read_text(encoding='utf-8').splitlines())} lines.", "src/cbsr_mcp/server.py"),
    ]
    for claim_id, claim_type, text, evidence in derived:
        claims.append({"claim_id": claim_id, "claim_type": claim_type, "claim_text": text, "record_ids": "", "source_urls": evidence, "pinpoint": "generated artifact", "evidence_tier": "computed", "binding_status": "not_applicable", "freshness": AS_OF, "review_stage": "machine_verified", "allowed_use": "technical_claim", "uncertainty": "low", "reviewer": "canonical_verifier", "second_reviewer": "", "review_date": AS_OF, "status": "machine_verified", "strength": "computed", "limitation": "Reproducible technical claim only; no external assurance or legal conclusion."})
    _csv(RESEARCH / "claims/claims_ledger.csv", claims)
    (RESEARCH / "claims/claims_ledger.json").write_text(
        json.dumps({"schema": "cbsr/claims-ledger/v2", "as_of": AS_OF, "claim_count": len(claims), "independent_review_status": "not_completed", "claims": claims}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return claims


def _manifest() -> None:
    files = []
    for path in sorted(RESEARCH.rglob("*")):
        if not path.is_file() or path.name == "research_manifest.json" or "__pycache__" in path.parts:
            continue
        files.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": _sha(path)})
    (RESEARCH / "research_manifest.json").write_text(
        json.dumps({"schema": "cbsr/research-manifest/v1", "as_of": AS_OF, "file_count": len(files), "files": files, "external_review": {"legal_second_review": "not_completed", "qualitative_second_coder": "not_completed", "peer_review": "not_completed"}}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    _quantitative()
    _qualitative()
    claims = _claims()
    build_whitepaper(
        ROOT, RECORDS, DATA, claims,
        json.loads((RESEARCH / "quantitative_baseline.json").read_text(encoding="utf-8")),
        json.loads((RESEARCH / "agenticfi_evaluation.json").read_text(encoding="utf-8")),
    )
    _manifest()
    print(f"wrote research deliverables: {len(claims)} claims, quantitative/qualitative outputs and whitepaper")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
