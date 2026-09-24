# Dependency and release integrity

This control record addresses the PR #20 Scorecard feedback. It is not an OpenSSF
Gold award, a promise of a perfect Scorecard score, or evidence that a release ran.
The authorized `v0.11.0.post1` request is an engineering update to the software
package; it does not advance the `0.11.0` legal-data snapshot or certify legal
currentness, independent review, or Gold status.

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
| `verify-wheel` | `contents: read` | Checkout without persisted credentials; install the locked graph, run the canonical verifier, then invoke the fail-closed release preparer. Upload only its `artifacts/release` directory. |
| `attest-wheel` | `contents: read`, `id-token: write`, `attestations: write` | Download that same-run directory and attest the exact wheel filename emitted by the preparer. No checkout or repository-code execution. |
| `publish-release-assets` | `contents: write` | Only after both verification and attestation: either create the explicitly requested release on the trusted `main` request-file push, or upload the same-run assets to the matching published-release event. No checkout, dependency installation or repository-code execution. |

The publication push trigger is limited to `main` and the single
`delivery/release-request.json` path. Other pushes do not start this workflow. The
preparer accepts only a current PEP 440 post-release request, binds the current source
fingerprint, canonical summary, two reproducible wheel builds, current lock digests
and live vulnerability-audit evidence, and stages only the current-version wheel,
SBOM/license inventory, package-smoke and audit evidence, manifest and checksums.
The notes remain outside `assets/` so they become the release body rather than a
downloadable asset.

On the trusted push, the publisher first asks the GitHub ref API to create
`refs/tags/$RELEASE_TAG` at the exact `${{ github.sha }}` supplied through
`RELEASE_COMMIT`. Ref creation is atomic and is neither forced nor updated: an
existing tag fails the job. `gh release create --verify-tag` then refuses to create
from an absent tag. An existing release also fails normally rather than being edited.
If tag creation succeeds but later release creation fails, the tag is deliberately
left in place for explicit maintainer reconciliation and disclosure; the workflow
does not hide the partial result by deleting or moving it.

On a published-release event, the workflow rebuilds and re-verifies the declared
version and then uses `gh release upload` for the event tag. Neither publication path
uses `--clobber`, so an existing same-name asset fails rather than being replaced.
Manual dispatch verifies and attests but cannot enter the publisher job. Immutable
artifacts are scoped to the same workflow run. No personal access token is introduced.
The release-boundary gate rejects broader triggers, extra permissions, publication
without both predecessor jobs, checkout or repository-code execution in privileged
jobs, and every publisher shell command outside this fixed allowlist.

## Why the publisher retains `contents: write`

GitHub's release and Git-ref APIs require Contents write permission; see the
[release-asset upload API](https://docs.github.com/en/rest/releases/assets#upload-a-release-asset)
and [create-a-reference API](https://docs.github.com/en/rest/git/refs#create-a-reference).
Scorecard v5.5.0's
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
