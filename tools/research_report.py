#!/usr/bin/env python3
"""Generate the record-level research ledger, baseline and jurisdiction dossiers.

These outputs are an auditable research work product, not an automatic legal opinion. They
preserve missing sources and reviewer gaps instead of filling them with synthetic claims.
"""

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
import io
import json
import pathlib
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
RECORDS = DATA.get("records", [])


def _counts(field: str, rows: list[dict]) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field) or "unset") for row in rows).items()))


def _clean(value, limit: int | None = None) -> str:
    text = str(value or "").replace("|", "\\|").replace("\n", " ").strip()
    return text if limit is None or len(text) <= limit else text[: limit - 1].rstrip() + "…"


def _ledger_row(record: dict) -> dict:
    source = record.get("source") or {}
    freshness = record.get("freshness") or {}
    return {
        "record_id": record.get("id"),
        "jurisdiction": record.get("jurisdiction"),
        "dimension": record.get("dimension"),
        "claim_class": record.get("claim_class"),
        "requirement_summary": record.get("requirement_summary"),
        "official_or_named_source": source.get("primary"),
        "source_url": source.get("url"),
        "pinpoint": source.get("pinpoint"),
        "source_disposition": record.get("source_disposition"),
        "source_check_status": record.get("source_check_status"),
        "source_last_checked": record.get("source_last_checked"),
        "next_review_due": record.get("next_review_due"),
        "review_status": freshness.get("review_status") or record.get("review_status"),
        "days_overdue": freshness.get("days_overdue"),
        "reviewer": record.get("reviewer"),
        "second_reviewer": record.get("second_reviewer"),
        "review_stage": record.get("review_stage"),
        "reconciliation_status": record.get("reconciliation_status"),
        "review_disagreement": record.get("review_disagreement"),
        "evidence_tier": record.get("evidence_tier"),
        "binding_status": record.get("binding_status"),
        "legal_status": record.get("legal_status"),
        "effective_from": record.get("effective_from"),
        "effective_until": record.get("effective_until"),
        "event_id": record.get("event_id"),
        "uncertainty": record.get("uncertainty"),
        "decision_ready": bool(
            freshness.get("review_status") == "current"
            and record.get("review_stage") == "reconciled"
            and record.get("source_disposition") == "official"
        ),
    }


def _write_source_ledger(research: pathlib.Path) -> list[dict]:
    rows = [_ledger_row(record) for record in sorted(RECORDS, key=lambda item: item["id"])]
    ledger = {
        "schema": "cbsr/source-ledger/v2",
        "dataset_version": DATA.get("version"),
        "as_of": DATA.get("generated"),
        "review_scope": "complete 152-record inventory and review-state ledger",
        "legal_review_claim": (
            "No claim of a new 152-record legal review is made. A row is checked only where a committed "
            "record-level verification identifies the same URL; second review remains independently attestable."
        ),
        "promotion_rule": (
            "Decision-ready requires an official source, current source check, named primary reviewer, "
            "independent second reviewer and reconciled disposition."
        ),
        "counts": {
            "records": len(rows),
            "source_disposition": dict(sorted(Counter(row["source_disposition"] for row in rows).items())),
            "review_status": dict(sorted(Counter(row["review_status"] for row in rows).items())),
            "review_stage": dict(sorted(Counter(row["review_stage"] for row in rows).items())),
            "primary_reviewer_present": sum(bool(row["reviewer"]) for row in rows),
            "second_reviewer_present": sum(bool(row["second_reviewer"]) for row in rows),
            "decision_ready": sum(row["decision_ready"] for row in rows),
        },
        "records": rows,
    }
    (research / "source_ledger_2026-08-20.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    (research / "source_ledger_2026-08-20.csv").write_text(buffer.getvalue(), encoding="utf-8")
    return rows


def _write_baseline(research: pathlib.Path) -> dict:
    report = {
        "schema": "cbsr/quantitative-baseline/v2",
        "dataset_version": DATA.get("version"),
        "as_of": DATA.get("generated"),
        "records": len(RECORDS),
        "jurisdictions": len({row.get("jurisdiction") for row in RECORDS}),
        "by_jurisdiction": _counts("jurisdiction", RECORDS),
        "by_status": _counts("status", RECORDS),
        "by_legal_status": _counts("legal_status", RECORDS),
        "by_binding_status": _counts("binding_status", RECORDS),
        "by_evidence_tier": _counts("evidence_tier", RECORDS),
        "by_claim_class": _counts("claim_class", RECORDS),
        "by_source_disposition": _counts("source_disposition", RECORDS),
        "by_review_stage": _counts("review_stage", RECORDS),
        "by_freshness": dict(sorted(Counter(
            (row.get("freshness") or {}).get("review_status", "unknown") for row in RECORDS
        ).items())),
        "structural_citable_candidates": DATA.get("citable_subset", {}).get("count", 0),
        "decision_ready_citable": DATA.get("decision_ready_citable_subset", {}).get("count", 0),
        "limitations": [
            "Counts describe the committed snapshot; they do not prove that a legal proposition remains current.",
            "last_reviewed is not treated as evidence that a source URL was opened.",
            "No independent second reviewer is inferred from tool or model execution.",
            "No inferential causal claim or population estimate is made.",
        ],
    }
    (research / "quantitative_baseline.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    lines = [
        "# Quantitative baseline", "",
        f"Dataset **v{report['dataset_version']}**, deterministic as-of **{report['as_of']}**.", "",
        f"The census contains **{report['records']} records** across **{report['jurisdictions']} jurisdictions**. "
        f"There are **{report['structural_citable_candidates']} structural citable candidates** and "
        f"**{report['decision_ready_citable']} decision-ready citable records** after freshness and independent-review gates.", "",
        "## Distribution", "", "| Axis | Counts |", "|---|---|",
        f"| Legal status | `{json.dumps(report['by_legal_status'], ensure_ascii=False)}` |",
        f"| Binding status | `{json.dumps(report['by_binding_status'], ensure_ascii=False)}` |",
        f"| Evidence tier | `{json.dumps(report['by_evidence_tier'], ensure_ascii=False)}` |",
        f"| Source disposition | `{json.dumps(report['by_source_disposition'], ensure_ascii=False)}` |",
        f"| Review stage | `{json.dumps(report['by_review_stage'], ensure_ascii=False)}` |",
        f"| Freshness | `{json.dumps(report['by_freshness'], ensure_ascii=False)}` |", "",
        "## Interpretation", "",
        "This is a census of the committed register, not a quality score. Source availability, freshness and "
        "two-person review are separate denominators. An item can be structurally well formed and still be "
        "ineligible for a legal or AgenticFi decision.", "",
        "## Limitations", "", *[f"- {item}" for item in report["limitations"]], "",
    ]
    (research / "QUANTITATIVE_BASELINE.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def _write_dossiers(research: pathlib.Path, report: dict) -> None:
    dossiers = research / "jurisdictions"
    dossiers.mkdir(parents=True, exist_ok=True)
    events = (DATA.get("analysis") or {}).get("event_calendar", {}).get("events", [])
    for code in sorted(report["by_jurisdiction"]):
        rows = sorted((row for row in RECORDS if row.get("jurisdiction") == code), key=lambda item: item["dimension"])
        fresh = Counter((row.get("freshness") or {}).get("review_status", "unknown") for row in rows)
        domains = Counter()
        for row in rows:
            url = (row.get("source") or {}).get("url")
            if url:
                domains[urlparse(url).hostname or "unknown"] += 1
        jurisdiction_events = [event for event in events if event.get("jurisdiction") == code]
        body = [
            f"# {code} jurisdiction evidence dossier", "",
            f"Snapshot: CBSR v{DATA.get('version')} as of {DATA.get('generated')}. This is a record-level "
            "evidence dossier and review queue, not an independent legal opinion.", "",
            "## Research posture", "",
            f"- Record population: {len(rows)}",
            f"- Legal status: `{json.dumps(_counts('legal_status', rows), ensure_ascii=False)}`",
            f"- Evidence tier: `{json.dumps(_counts('evidence_tier', rows), ensure_ascii=False)}`",
            f"- Source disposition: `{json.dumps(_counts('source_disposition', rows), ensure_ascii=False)}`",
            f"- Freshness: `{json.dumps(dict(sorted(fresh.items())), ensure_ascii=False)}`",
            f"- Review stage: `{json.dumps(_counts('review_stage', rows), ensure_ascii=False)}`",
            f"- Named second reviewer: {sum(bool(row.get('second_reviewer')) for row in rows)}/{len(rows)}", "",
            "## Official source families", "",
        ]
        if domains:
            body.extend(f"- `{domain}` — {count} record(s)" for domain, count in sorted(domains.items()))
        else:
            body.append("- No source URL is committed; every row remains in the acquisition queue.")
        thematic_sections = [
            ("Institutional and supervisory boundary", {"regulatory_authority", "securities_classification", "monetary_sovereignty"}),
            ("Authorisation and licensing perimeter", {"issuer_pathway", "distribution", "bank_nonbank_routing"}),
            ("Reserve, safeguarding and redemption", {"reserve_backing", "redemption", "capital_requirements"}),
            ("Cross-border and data conditions", {"cross_border_data", "monetary_sovereignty"}),
            ("AML, KYC and financial-crime controls", {"aml_kyc"}),
            ("Enforcement and implementation posture", {"regulatory_authority", "implementation_status", "disclosure_reporting"}),
        ]
        for heading, dimensions in thematic_sections:
            body.extend(["", f"## {heading}", ""])
            selected = [row for row in rows if row.get("dimension") in dimensions]
            if not selected:
                body.append(
                    "No dedicated record is present for this theme. The absence is a documented scope gap, "
                    "not a legal conclusion."
                )
                continue
            for row in selected:
                body.extend([
                    f"### `{row['id']}` — `{row['dimension']}`", "",
                    _clean(row.get("requirement_summary")), "",
                    f"- Institutional/legal state: `{row.get('legal_status')}` / `{row.get('binding_status')}`.",
                    f"- Evidence and uncertainty: `{row.get('evidence_tier')}` / `{row.get('uncertainty')}`.",
                    f"- Decision-use gate: `{(row.get('freshness') or {}).get('review_status')}` / "
                    f"`{row.get('review_stage')}`.", "",
                ])
        body.extend([
            "", "## Line-by-line record matrix", "",
            "| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |",
            "|---|---|---|---|---|---|",
        ])
        for row in rows:
            source = row.get("source") or {}
            url = source.get("url")
            source_cell = f"[{_clean(source.get('primary'), 70)}]({url})" if url else _clean(source.get("primary"), 70)
            pinpoint = _clean(source.get("pinpoint"), 110) or "pinpoint missing"
            freshness = row.get("freshness") or {}
            body.append(
                f"| `{row['id']}` | `{row['dimension']}` | `{row.get('legal_status')}` / `{row.get('binding_status')}` | "
                f"`{row.get('evidence_tier')}`; `{row.get('uncertainty')}` uncertainty | {source_cell}<br>{pinpoint} | "
                f"`{freshness.get('review_status')}`; `{row.get('review_stage')}` |"
            )
        body.extend(["", "## Record-level propositions and unresolved work", ""])
        for row in rows:
            source = row.get("source") or {}
            gaps = []
            if not source.get("url"):
                gaps.append("official URL acquisition")
            if not source.get("pinpoint"):
                gaps.append("pinpoint mapping")
            if (row.get("freshness") or {}).get("review_status") != "current":
                gaps.append("freshness recheck")
            if not row.get("second_reviewer"):
                gaps.append("independent second review")
            if row.get("reconciliation_status") not in {"agreed", "resolved"}:
                gaps.append("reconciliation")
            body.extend([
                f"### `{row['id']}`", "",
                _clean(row.get("requirement_summary")), "",
                f"- Source disposition: `{row.get('source_disposition')}`; check status: `{row.get('source_check_status')}`.",
                f"- Temporal state: `{row.get('legal_status')}`; effective from `{row.get('effective_from')}`; "
                f"event `{row.get('event_id')}`.",
                f"- Open gate(s): {', '.join(gaps) if gaps else 'none'}.", "",
            ])
        body.extend(["## Legal-event relationships", ""])
        if jurisdiction_events:
            for event in jurisdiction_events:
                body.extend([
                    f"### `{event.get('id')}` — {event.get('title')}", "",
                    f"- Status: `{event.get('status')}`; effective date: `{event.get('effective_date')}`; "
                    f"trigger kind: `{event.get('trigger_kind')}`.",
                    f"- Linked records: {', '.join(f'`{item}`' for item in event.get('records', [])) or 'none'}.",
                    f"- Internal basis: {_clean(event.get('basis'))}", "",
                ])
        else:
            body.extend(["No first-class event is mapped for this jurisdiction. This is an ontology gap, not proof of no legal change.", ""])
        body.extend([
            "## Independent review and reconciliation protocol", "",
            "1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.",
            "2. A different, identified legal reviewer repeats the check without seeing the first disposition.",
            "3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.",
            "4. A resolved row records the rationale and never overwrites the superseded reading silently.",
            "5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.", "",
            "## Release gate", "",
            "This dossier cannot be labelled complete legal research until every row has an official-source disposition, "
            "a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible "
            "in the ledger rather than being converted into a confidence score.", "",
            "## Bibliography", "",
        ])
        bibliography = []
        for row in rows:
            source = row.get("source") or {}
            if source.get("url"):
                bibliography.append((str(source.get("primary") or row.get("instrument_label_local") or row["id"]), str(source["url"]), str(source.get("pinpoint") or "pinpoint pending")))
        if bibliography:
            for index, (title, url, pinpoint) in enumerate(sorted(set(bibliography)), start=1):
                body.append(f"{index}. [{_clean(title, 140)}]({url}) — {_clean(pinpoint, 180)}.")
        else:
            body.append("No URL-bearing source is committed. Bibliographic acquisition remains a release gate.")
        body.extend([
            "", "Bibliography entries reproduce committed source metadata. Inclusion is not a representation that "
            "the source was re-opened during this generation run.", "",
        ])
        (dossiers / f"{code}.md").write_text("\n".join(body), encoding="utf-8")


def main() -> int:
    research = ROOT / "research"
    research.mkdir(parents=True, exist_ok=True)
    rows = _write_source_ledger(research)
    report = _write_baseline(research)
    _write_dossiers(research, report)
    if len(rows) != 152:
        raise SystemExit(f"expected 152 ledger rows, wrote {len(rows)}")
    print("wrote 152-row JSON/CSV source ledger, quantitative baseline and 12 evidence dossiers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
