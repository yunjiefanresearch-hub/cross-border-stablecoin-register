import json

import pytest

from tools import check_gold_coverage as gold
from tools.check_gold_coverage import metrics


def sample(statements, lines, branches, covered):
    return {"sample.py": {"summary": dict(num_statements=statements, covered_lines=lines,
        num_branches=branches, covered_branches=covered)}}


def test_gold_thresholds_are_separate_and_not_rounded_up():
    assert metrics(sample(100, 90, 100, 80))["thresholds_met"]
    assert not metrics(sample(10000, 8999, 100, 100))["thresholds_met"]
    assert not metrics(sample(100, 100, 10000, 7999))["thresholds_met"]


def test_empty_scope_cannot_claim_gold_coverage():
    assert not metrics({})["thresholds_met"]
    assert not metrics(sample(1, 1, 0, 0))["thresholds_met"]


def test_metrics_weight_by_statements_not_file_average():
    files = sample(100, 90, 100, 80)
    files["uncovered.py"] = sample(900, 0, 900, 0)["sample.py"]
    actual = metrics(files)
    assert actual["statement_percent"] == 9
    assert actual["branch_percent"] == 8
    assert not actual["thresholds_met"]


def summary_file(tmp_path, **changes):
    document = {"schema": "cbsr/verification-summary/v2", "status": "passed",
                "source_fingerprint_sha256": "a" * 64}
    document.update(changes)
    path = tmp_path / "verify-summary.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    return path


def canonical_files():
    return {"tools/verify.py": {"contexts": {"1": ["canonical"]}}}


def test_valid_current_canonical_binding(tmp_path, monkeypatch):
    monkeypatch.setattr(gold, "current_source_fingerprint", lambda: "a" * 64)
    binding = gold.verification_binding(summary_file(tmp_path), canonical_files())
    assert binding["valid"]
    assert binding["errors"] == []


@pytest.mark.parametrize("change", [{"schema": "old"}, {"status": "failed"},
                                     {"source_fingerprint_sha256": "b" * 64}])
def test_invalid_or_stale_summary_never_qualifies(tmp_path, monkeypatch, change):
    monkeypatch.setattr(gold, "current_source_fingerprint", lambda: "a" * 64)
    assert not gold.verification_binding(summary_file(tmp_path, **change), canonical_files())["valid"]


@pytest.mark.parametrize("payload", ["not json", "[]"])
def test_malformed_summary_is_failure_evidence(tmp_path, monkeypatch, payload):
    monkeypatch.setattr(gold, "current_source_fingerprint", lambda: "a" * 64)
    path = tmp_path / "bad.json"
    path.write_text(payload, encoding="utf-8")
    assert not gold.verification_binding(path, canonical_files())["valid"]


def test_missing_summary_and_unmeasured_canonical_are_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(gold, "current_source_fingerprint", lambda: "a" * 64)
    assert not gold.verification_binding(tmp_path / "missing.json", canonical_files())["valid"]
    assert not gold.verification_binding(summary_file(tmp_path), {})["valid"]


def test_failed_binding_makes_report_fail_even_above_threshold(tmp_path, monkeypatch):
    monkeypatch.setattr(gold, "current_source_fingerprint", lambda: "a" * 64)
    monkeypatch.setattr(gold.subprocess, "check_output", lambda *args, **kwargs: "sample.py\n")
    coverage = {"meta": {"branch_coverage": True, "version": "fixture"},
                "files": sample(100, 100, 100, 100)}
    source = tmp_path / "coverage.json"
    target = tmp_path / "gold.json"
    source.write_text(json.dumps(coverage), encoding="utf-8")
    assert gold.main(["--input", str(source), "--output", str(target),
                      "--verification-summary", str(summary_file(tmp_path, status="failed"))]) == 1
    report = json.loads(target.read_text(encoding="utf-8"))
    assert not report["coverage_thresholds_met"]
    assert not report["gold_badge_awarded"]


def test_legacy_report_keeps_uncovered_files_and_enforcement(tmp_path, monkeypatch):
    monkeypatch.setattr(gold.subprocess, "check_output", lambda *args, **kwargs: "sample.py\n")
    source = tmp_path / "coverage.json"
    target = tmp_path / "gold.json"
    source.write_text(json.dumps({"meta": {"branch_coverage": True, "version": "fixture"},
                                  "files": sample(100, 1, 100, 0)}), encoding="utf-8")
    args = ["--input", str(source), "--output", str(target)]
    assert gold.main(args) == 0
    assert gold.main(args + ["--enforce"]) == 1
    assert json.loads(target.read_text(encoding="utf-8"))["measurement_mode"] == "pytest_only"
    monkeypatch.setattr(gold.subprocess, "check_output", lambda *args, **kwargs: "sample.py\nunmeasured.py\n")
    assert gold.main(args) == 1
