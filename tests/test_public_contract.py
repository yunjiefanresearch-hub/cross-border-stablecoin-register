"""Public projections must preserve the distinction between candidates and usable evidence."""

import json
import hashlib
from pathlib import Path
import re

from cbsr_mcp.tools import architecture, research
from cbsr_mcp.tools.registry import metadata

ROOT = Path(__file__).resolve().parent.parent


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def test_api_headlines_are_derived_from_their_actual_collections():
    dataset = read_json("dataset.json")
    envelope = read_json("api/meta.json")
    meta = envelope["data"]
    assert envelope["generated"] == str(dataset["generated"])
    assert meta["record_count"] == len(dataset["records"])
    assert meta["mcp_tool_count"] == len(metadata())
    assert meta["authored_corridors"] == len(dataset["corridors"])
    assert meta["directed_corridors"] == len(read_json("analysis/computed_corridors_directed.json")["edges"])
    assert meta["citable_count"] == dataset["decision_ready_citable_subset"]["count"]
    assert meta["structural_citable_candidates"] == dataset["citable_subset"]["count"]


def test_console_and_mcp_agree_on_every_citable_record_and_failed_gate():
    html = (ROOT / "console.html").read_text(encoding="utf-8")
    payload = json.loads(re.search(r'<script[^>]*id="embedded-data"[^>]*>(.*?)</script>', html, re.S).group(1))
    dataset = read_json("dataset.json")
    strict_ids = {row["id"] for row in dataset["decision_ready_citable_subset"]["records"]}
    assert {row["id"] for row in payload["records"] if row["citable"]} == strict_ids
    assert payload["citable_count"] == architecture.citable_law()["count"]
    assert payload["structural_candidate_count"] == dataset["citable_subset"]["count"]
    source_records = {row["id"]: row for row in dataset["records"]}
    for row in payload["records"]:
        expected = {block[0] for block in research._citable_blocks(source_records[row["id"]])}
        assert {block[0] for block in row["blocks"]} == expected
        assert row["citable"] == (not expected)


def test_missing_review_evidence_cannot_be_promoted_by_a_structural_match():
    structural = {
        "claim_class": "tier1_legal", "status": "in_force", "evidence_tier": "resolution_text",
        "source_disposition": "official", "freshness": {"review_status": "current"},
        "review_stage": "primary_reviewed_second_pending",
    }
    assert [item[0] for item in research._citable_blocks(structural)] == ["review_stage"]
    structural["review_stage"] = "reconciled"
    structural["freshness"]["review_status"] = "stale"
    assert [item[0] for item in research._citable_blocks(structural)] == ["review_status"]


def test_published_manifests_have_portable_order_and_real_byte_hashes():
    for relative in ("research/research_manifest.json", "delivery/delivery_manifest.json"):
        manifest = read_json(relative)
        paths = [row["path"] for row in manifest["files"]]
        assert paths == sorted(paths)
        assert len(paths) == len(set(paths)) == manifest["file_count"]
        for row in manifest["files"]:
            data = (ROOT / row["path"]).read_bytes()
            assert len(data) == row["bytes"], row["path"]
            assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
            if Path(row["path"]).suffix in {".json", ".md", ".csv", ".svg"}:
                assert b"\r" not in data, row["path"]
