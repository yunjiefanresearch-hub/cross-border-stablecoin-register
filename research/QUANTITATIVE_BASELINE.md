# Quantitative baseline

Dataset **v0.11.0**, deterministic as-of **2026-08-20**.

The census contains **152 records** across **12 jurisdictions**. There are **46 structural citable candidates** and **0 decision-ready citable records** after freshness and independent-review gates.

## Distribution

| Axis | Counts |
|---|---|
| Legal status | `{"consultation": 1, "enacted_not_commenced": 21, "finalized_policy_pending": 9, "no_regime": 1, "operative": 98, "prohibited": 9, "proposed": 13}` |
| Binding status | `{"finalized_policy_pending": 9, "in_force_enacted": 98, "made_not_commenced": 21, "no_regime": 1, "pending_proposal": 14, "prohibition": 9}` |
| Evidence tier | `{"firm_summary": 63, "mixed": 14, "resolution_text": 48, "unverified": 27}` |
| Source disposition | `{"official": 103, "unavailable": 49}` |
| Review stage | `{"primary_reviewed_second_pending": 41, "unreviewed": 111}` |
| Freshness | `{"stale": 38, "unknown": 114}` |

## Interpretation

This is a census of the committed register, not a quality score. Source availability, freshness and two-person review are separate denominators. An item can be structurally well formed and still be ineligible for a legal or AgenticFi decision.

## Limitations

- Counts describe the committed snapshot; they do not prove that a legal proposition remains current.
- last_reviewed is not treated as evidence that a source URL was opened.
- No independent second reviewer is inferred from tool or model execution.
- No inferential causal claim or population estimate is made.
