# Qualitative thematic analysis

## Method

The current run applies a deterministic primary codebook to all 152 records. It produces a complete coded-case table and a blank second-coder worksheet. No intercoder reliability statistic is reported because an independent human second coding pass has not occurred.

## Themes

### Theme 1: Evidence availability is distinct from legal force

Cases carrying the related primary code: **49**.

A binding-status label cannot substitute for an official source and pinpoint.

### Theme 2: Temporal uncertainty dominates decision readiness

Cases carrying the related primary code: **152**.

Unknown and stale checks must block unconditional allow.

### Theme 3: Independent interpretation is the binding governance gap

Cases carrying the related primary code: **152**.

Automation cannot manufacture an independent reviewer identity.

### Theme 4: Legal change requires explicit event modelling

Cases carrying the related primary code: **132**.

A null event is a modelling gap rather than evidence that no change exists.

## Failure taxonomy and threat linkage

| Failure | Threat | Control |
|---|---|---|
| `source_acquisition_gap` | unsupported or secondary-only legal claim | official-source disposition and fail-closed decision gate |
| `freshness_unknown_or_stale` | obsolete legal state | SLA, next-review date and currentness gate |
| `independent_review_gap` | single-reviewer interpretation bias | blind second review and reconciliation |
| `event_model_gap` | missed commencement or supersession | typed legal-event ontology |
| `receipt_tampering` | post-decision evidence substitution | canonical component and receipt digests |
| `mandate_overreach` | agent acts beyond authority | versioned mandate, jurisdiction/time/amount and human-review gates |

## Independent coding gate

A qualified second coder must complete `SECOND_CODER_WORKSHEET.csv` without copying the primary codes. Agreement, disagreement and reconciliation must then be computed and attested. Until that occurs, qualitative findings are exploratory and cannot be described as independently coded.
