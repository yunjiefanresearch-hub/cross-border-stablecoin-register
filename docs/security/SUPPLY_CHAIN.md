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

The prior scan consequently reported `Token-Permissions=9`. That warning may
remain after this hardening: it is disclosed, not suppressed, and the permission
is confined to the publisher. Replacing GitHub CLI with another release action,
using a broader secret token, or disabling SARIF would not remove the underlying
permission requirement. Reassess this exception whenever the scanner or release
design changes; the actual new scan must be read before reporting its score.

Human review, required-check enforcement, independently reproduced releases and
all other [Gold gaps](OPENSSF_GOLD.md) remain separate acceptance requirements.
