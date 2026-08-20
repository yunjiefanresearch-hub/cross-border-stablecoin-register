# DPG submission-readiness package

Status: **not submitted; external determination not requested**.

This package assembles repository evidence only. It must not be sent to DPGA until legal, security, governance, remote-CI and accessibility gates are closed by their named owners.

## Evidence index

- Indicator matrix: `analysis/dpg_evidence_matrix.json` and CSV.
- Licensing: `LICENSE`, `LICENSE-CODE`, `LICENSE-DATA`.
- Ownership and governance: `GOVERNANCE.md`, `CITATION.cff`, `.github/CODEOWNERS`.
- Privacy and security: `PRIVACY.md`, `SECURITY.md`, `docs/security/THREAT_MODEL.md`.
- Public-interest mappings: `analysis/sdg_mapping.json`, `analysis/gdc_mapping.json`, `analysis/dpi_safeguards_mapping.json`.
- Reproducibility: `tools/verify.py`, constraints, SBOM, package-smoke and compatibility evidence.

## Submission hard gates

1. Replace every Partial row with dated closure evidence or retain a justified limitation.
2. Complete independent legal, security, accessibility and scholarly review.
3. Retain actual GitHub Actions, ruleset, Windows and provenance readback.
4. Obtain maintainer approval for an external submission; no automation may submit it.
5. Record the submitted revision, date, recipient and response without rewriting repository history.
