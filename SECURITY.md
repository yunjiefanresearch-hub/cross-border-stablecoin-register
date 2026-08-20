# Security policy

## Supported version

Security fixes target the latest released or release-candidate branch. Historical datasets remain
available for citation but do not receive runtime fixes.

## Reporting

Do not disclose an exploitable vulnerability in a public issue. Use GitHub's private vulnerability
reporting for this repository. Include the affected revision, reproduction steps, impact, and the
smallest safe test case. Never include production credentials, personal data, or private legal files.

## Response expectations and coordinated disclosure

- A maintainer should acknowledge a complete private report within **3 business days** and provide an
  initial severity/triage decision within **7 business days**. These are response targets, not a warranty.
- The reporter and maintainer should agree a disclosure date based on exploitability, affected users,
  patch availability and downstream coordination. The default target is within **90 days**, shortened
  for active exploitation and extended only with a recorded reason.
- A fix is not considered complete until the regression test, dependency/security gates, artifact
  checksums and applicable advisory are verified. Affected versions and mitigations must be explicit.
- If GitHub private vulnerability reporting is unavailable, do not open a public exploit issue. Use the
  maintainer's verified contact channel in `CITATION.cff` only for an initial request; do not email secrets
  or sensitive payloads before agreeing a protected channel.

## Good-faith research safe harbour

The project will not recommend or pursue legal action against good-faith security research that avoids
privacy violations, data destruction, service disruption, social engineering, credential theft and use
of findings beyond what is necessary to demonstrate impact. Researchers should stop after confirming the
minimum evidence, report promptly, keep the issue confidential during coordination and comply with
applicable law. This statement cannot authorize testing of third-party services or data that the project
does not control.

## Trust boundary

CBSR is offline decision support. It does not custody keys, submit transactions, sign receipts, or
authorize execution. `evaluate_action` always returns `execution_authorized: false`. SHA-256 receipts
detect mutation only; they are not signatures and do not prove who made a decision.

Dependencies are pinned in `constraints/`. The canonical verifier builds twice, clean-installs the
wheel outside the checkout, treats import warnings as errors, emits a CycloneDX SBOM and licence
inventory, and requires a clean `pip-audit` result or a dated, lock-bound offline snapshot. CI is
configured for Python 3.10-3.13 and Windows, but only successful remote runs constitute platform
evidence.

## Supply-chain gates

Pull-request workflows declare CodeQL, dependency review, high-confidence secret scanning and OpenSSF
Scorecard checks. Release workflows generate build provenance attestations. `python -m tools.verify`
also validates those declarations and performs the repository-local secret, SBOM, licence and dependency
gates. Version tags in workflow files are upgrade inputs, not proof a workflow ran; branch protection,
required reviews, secret scanning, provenance and signed release state must be read back from GitHub
before a release is labelled ready.

## Release hard stops

A release is blocked by a known unreviewed vulnerability, a detected secret, a failing licence policy,
non-reproducible wheel, invalid receipt mutation test, missing verification summary, or unverified
checksum. An independent security reviewer must complete
`docs/security/EXTERNAL_SECURITY_REVIEW_TEMPLATE.md`. No independent security review is claimed by the
repository as of 20 August 2026.

See `docs/security/THREAT_MODEL.md` for assets, trust boundaries, threats, controls and residual risks.
