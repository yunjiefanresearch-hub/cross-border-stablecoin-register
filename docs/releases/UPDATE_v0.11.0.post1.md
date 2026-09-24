# CBSR v0.11.0.post1 — 更新版本 / Engineering update

This is a maintainer-authorized **engineering update**, not an OpenSSF Gold release,
independently reviewed security certification, or refreshed legal dataset.
The `.post1` package version preserves the underlying dataset's `0.11.0` identity
and **2026-08-20** snapshot. Old tags and release assets are not replaced.

## Changes

- Unify public evidence counts: **152 records, 46 structural candidates, 0 strictly
  decision-ready records and 40 MCP tools**. Structural candidates are not verified
  current law. The site and Mapper distinguish online retrieval from evidence freshness.
- Repair cross-platform verification, the Windows package build, clean-room wheel
  installation, deterministic generation, and fail-closed policy/input boundaries.
- Pin complete runtime, development and measurement dependency graphs with hashes;
  audit the full graph, upgrade vulnerable build dependencies, and isolate release
  signing/upload privileges from repository-code execution.
- Repair Dependabot labels, Dependency review, and historical workflow security findings.
- Add canonical subprocess coverage measurement, negative tests, source-bound audit
  evidence, and reproducible build provenance for the exact released wheel.

## Installation and verification

Download the `cbsr_mcp-0.11.0.post1-py3-none-any.whl` asset and `SHA256SUMS` from this
release. Verify its SHA-256 before installing it into an isolated Python environment.
The supported verification matrix is Python 3.10–3.13 on Linux and Python 3.12 on
Windows. Use the hash-locked installation instructions in
[`constraints/README.md`](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/blob/v0.11.0.post1/constraints/README.md) from this exact source tag.
Do not interpret this GitHub release as a PyPI publication.

Release assets include the current wheel, SBOM, licence inventory, runtime and complete
development audit results, canonical verification summary, source-bound manifest and
checksums. The release workflow builds and verifies in a read-only job, attests the
same-run wheel separately, then publishes only those staged assets. A successful build
attestation proves build provenance, not an independent human review.

## Limitations and explicit publication exception

The maintainer approved this engineering update after being informed that non-author
human approval and independent security review are **not completed**. This is a
publication-scope exception, not evidence that those reviews occurred. The existing
`delivery/external_gates.json` remains `release_ready: false` for the broader reviewed
research/legal release. No security test, dependency audit or artifact-integrity check
is waived for this update.

Independent legal review, qualitative second coding, scholarly peer review and the
security review remain open. No legal-source freshness dates were advanced. The last
pre-update hosted whole-project coverage measurement was **72.06% statements / 61.38%
branches**, below the Gold thresholds; the current workflow report is authoritative
for this source revision. OpenSSF Passing/Silver/Gold prerequisites and other documented
people, infrastructure and review gaps remain outstanding. No badge is awarded or claimed.

CBSR is decision support only: it does not authorize execution, custody keys or sign
legal decisions. Reverting software does not establish current-law validity.

## Source and rollback

The foundational repair is [Register PR #20](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/pull/20).
Use the release manifest's exact source commit and asset hashes when reporting issues.
The prior `v0.11.0` tag is retained for reproducibility; it lacks the engineering fixes
in this update and should not be described as equally secure. Existing data citation
identifiers and the historical dataset version remain unchanged.
