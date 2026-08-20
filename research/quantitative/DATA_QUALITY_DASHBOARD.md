# Data-quality dashboard

Extraction date: **2026-08-20**. Unit: one jurisdiction–instrument–dimension record; corridor rows use ordered pairs.

All missing fields remain missing. No checked date, reviewer, source or legal state is imputed. Controlled pilot fixtures are excluded.

| Metric | Value / denominator | Unit | Definition |
|---|---:|---|---|
| `records` | 152 / 152 | records | compiled record count |
| `jurisdictions` | 12 / 12 | jurisdictions | jurisdictions represented |
| `dimensions` | 15 / 15 | dimensions | distinct dimensions represented |
| `records_with_source_url` | 103 / 152 | records | non-empty cited source URL; not a review claim |
| `official_source_disposition` | 103 / 152 | records | source classified as official |
| `primary_text_resolution` | 48 / 152 | records | resolution_text evidence tier |
| `structural_citable_candidates` | 46 / 152 | records | structural candidate only, not current-law ready |
| `decision_ready_citable` | 0 / 152 | records | official, current and independently reconciled |
| `freshness_current` | 0 / 152 | records | current under binding-status SLA |
| `freshness_stale` | 38 / 152 | records | source check beyond SLA |
| `high_impact_current_reconciled` | 0 / 50 | records | high-impact SLA hard gate |
| `missing_source_checked_date` | 114 / 152 | records | null source_last_checked |
| `missing_effective_from` | 100 / 152 | records | null effective_from; may be inapplicable or a gap |
| `invalid_date_relationships` | 0 / 152 | records | ontology date-rule failures |
| `uncertainty_high_or_unknown` | 90 / 152 | records | persisted uncertainty classification |
| `primary_reviewer_coverage` | 41 / 152 | records | named primary reviewer |
| `independent_second_reviewer_coverage` | 0 / 152 | records | different named second reviewer |
| `first_class_event_coverage` | 20 / 152 | records | record linked to event ontology |
| `superseded_records` | 0 / 152 | records | explicit superseded legal status |
| `directed_corridors` | 132 / 132 | corridors | class distribution {"I": 32, "II": 24, "III": 29, "T": 25, "blocked": 11, "pre_regime": 11} |
| `temporally_sensitive_class_moves` | 55 / 132 | edge movements | own-event inbound and outbound class movements; not unique edges |

## Method and limitations

Inclusion: all compiled records and directed corridors. Missing-data policy: retain explicit null/unavailable values. Principal biases are jurisdiction selection, unequal official-source access, translation, non-independent prior coding and the 2026-08-20 temporal cut-off. These are descriptive census statistics, not causal or population estimates.
