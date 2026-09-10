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
