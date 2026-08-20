# Independent legal review protocol

This protocol is the remaining human gate for the 152-record research ledger. Running code, an AI model,
or a second automated pass does not satisfy independence.

## Reviewer requirements

The second reviewer must be a different identified person from the primary reviewer and competent to
review the relevant jurisdiction and language. The reviewer records name or stable organization ID,
review date and conflicts of interest outside the source YAML; the public record may use a stable reviewer
identifier where publishing a name would be inappropriate.

## Record procedure

1. Open the committed source URL. If unavailable, locate the official instrument and record its stable URL.
2. Confirm that `source.primary` identifies the correct instrument and version.
3. Confirm the operative proposition in `requirement_summary` against the exact `source.pinpoint`.
4. Confirm enactment, commencement, transition and supersession dates separately.
5. Classify the URL as `official`, `secondary`, `unavailable` or `not_applicable`.
6. Record `source_last_checked`; derive `next_review_due` under the committed SLA.
7. Record the independent disposition without copying the first reviewer's conclusion.
8. If both readings agree, set `reconciliation_status: agreed` and `review_stage: reconciled`.
9. If they differ, preserve both readings in `review_disagreement`, set
   `review_stage: reconciliation_required`, and do not promote the row.
10. After resolution, record the reason, set `reconciliation_status: resolved`, and rerun
    `python -m tools.verify`.

## Promotion rule

Only a row with an official source, a current source check, an exact pinpoint, distinct primary and second
reviewers, and an agreed or resolved reconciliation may enter `decision_ready_citable_subset`. Structural
schema validity and `resolution_text` alone are insufficient.

## Required output

The reviewer updates the source YAML, the JSON/CSV ledger and the relevant jurisdiction dossier through the
normal generation pipeline. A signed external attestation may be retained privately; the repository must at
minimum preserve the stable reviewer identifiers and reconciliation state needed for audit.
