# Dependency and release integrity

This control record addresses the PR #20 Scorecard feedback. It is not an OpenSSF
Gold award, a promise of a perfect Scorecard score, or evidence that a release ran.

## Installation boundary

- Every external GitHub Action is pinned to a complete commit SHA. Version comments
  are explanatory; Dependabot can propose reviewed SHA updates.
- Reviewed Python versions are accompanied by SHA-256 wheel allowlists for the
  documented platform matrix. CI installs with `--require-hashes` and
  `--only-binary=:all:`. See [the lock procedure](../../constraints/README.md).
- The development-only local-wheel helper runs after the complete hashed graph is
  installed. It disables dependency downloads and then runs `pip check`.
- The clean package smoke instead resolves the local wheel and the full hashed
  runtime graph together. Missing pins or hashes fail; source-distribution builds
  cannot fetch unreviewed build dependencies. A locally computed wheel hash protects
  the build-to-install handoff, not the trustworthiness of its source.

The automated suite includes a network-free pip invocation proving an exact wheel
hash is accepted and an altered hash is rejected. Unit tests are not substitutes
for successful clean installations on every supported platform.

## Three-job release boundary

| Job | Permissions | Allowed work |
| --- | --- | --- |
| `verify-wheel` | `contents: read` | Checkout without persisted credentials; install, build, canonical verification, checksums and artifact upload. |
| `attest-wheel` | `contents: read`, `id-token: write`, `attestations: write` | Download the same run's verified wheel and issue build provenance. No checkout or repository-code execution. |
| `publish-release-assets` | `contents: write` | Only after attestation, and only on a published-release event: download the same run's assets and upload them using GitHub CLI. No checkout, dependency installation or repository-code execution. |

Manual dispatch verifies and attests but does not upload to a release. The upload
does not use `--clobber`: existing same-name assets cause failure rather than
replacement. Immutable artifacts are scoped to the same workflow run. No personal
access token is introduced. The release-boundary gate rejects extra permissions or
repository-code execution in privileged jobs.

## Why the publisher retains `contents: write`

GitHub's [release-asset upload API](https://docs.github.com/en/rest/releases/assets#upload-a-release-asset)
requires Contents write permission. Scorecard v5.5.0's
[permission classifier](https://github.com/ossf/scorecard/blob/c395761df6afe1a69e476bc60a013a94bcbc153f/checks/raw/permissions.go#L442-L530)
does not recognize `gh release upload` as an accepted packaging exception.
[Upstream issue #5201](https://github.com/ossf/scorecard/issues/5201) separately
tracks GitHub CLI release detection in the Packaging check.

The prior scan reported `Token-Permissions=9` and emitted both the publisher's
job-level warning and CodeQL's workflow-level write-permission warning. In this
scanner version, a job-level write under explicit read-only workflow defaults can
remain a warning without deducting points; CodeQL's top-level write caused the
deduction. A score of 10 after moving it is not evidence that release write access
disappeared or that GitHub CLI became a recognized packaging exception. Replacing
GitHub CLI with another release action, using a broader secret token, or disabling
SARIF would not remove the underlying permission requirement. Reassess the boundary
whenever the scanner or release design changes.

The [scan for PR head `de5c3ad`](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34864683267)
also reported CodeQL's workflow-level `security-events: write`. This follow-up moves
that necessary SARIF-upload permission into the `analyze` job and disables checkout
credential persistence. A repository-wide regression gate now requires explicit
read-only workflow defaults. Job-scoped write permissions still require review;
moving a permission does not eliminate the capability of the job that needs it.

## Development dependencies are also security-sensitive

The [subsequent scan for `7df6096`](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34926810428)
reported no pinned-dependency or token-permission finding, but still identified 24
OSV vulnerability records affecting `pypdf==6.10.0` and `pytest==8.4.2`. These are
development dependencies, absent from the clean runtime audit. They are not dismissed
as old scan results: the official records include
[pypdf resource-exhaustion fixes](https://osv.dev/vulnerability/GHSA-jm82-fx9c-mx94)
and [pytest temporary-directory handling](https://osv.dev/vulnerability/PYSEC-2026-1845).

The reviewed repair uses `pypdf==6.18.1` and `pytest==9.1.1`, with regenerated official
wheel hashes and dependency closure checks. The canonical verifier now also invokes
`tools/audit_locked_dependencies.py` over the full development and quality locks
(including runtime transitives), with current-platform marker evaluation and strict
failure handling. Each platform run retains the audit output and exact lock digests.
There is no ignore list or offline pass for this additional live audit; the runtime
package smoke remains a separate, clean-environment test. An unavailable vulnerability
service is a verification failure, not a clean result.

Human review, required-check enforcement, independently reproduced releases and
all other [Gold gaps](OPENSSF_GOLD.md) remain separate acceptance requirements.
