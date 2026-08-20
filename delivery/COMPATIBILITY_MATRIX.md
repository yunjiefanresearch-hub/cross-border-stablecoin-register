# Compatibility matrix

| Platform | Python | Status | Evidence boundary |
|---|---|---|---|
| local Linux | 3.10 | `historical_prior_snapshot` | canonical verifier evidence for the recorded source fingerprint only; not evidence for this R5 snapshot or GitHub Actions; `docs/validation/local-linux-matrix.json` |
| local Linux | 3.11 | `historical_prior_snapshot` | canonical verifier evidence for the recorded source fingerprint only; not evidence for this R5 snapshot or GitHub Actions; `docs/validation/local-linux-matrix.json` |
| local Linux | 3.12 | `historical_prior_snapshot` | canonical verifier evidence for the recorded source fingerprint only; not evidence for this R5 snapshot or GitHub Actions; `docs/validation/local-linux-matrix.json` |
| local Linux | 3.13 | `historical_prior_snapshot` | canonical verifier evidence for the recorded source fingerprint only; not evidence for this R5 snapshot or GitHub Actions; `docs/validation/local-linux-matrix.json` |
| GitHub Actions ubuntu-latest | 3.10-3.13 | `unverified_external` | remote matrix and required check; `.github/workflows/build.yml` |
| Windows 11 / windows-latest | 3.12 | `unverified_external` | clean-room PowerShell path; `setup_windows.ps1` |

The retained local matrix belongs to an earlier source fingerprint and is not credited as R5 pass evidence. Workflow declarations are not remote pass evidence. Windows remains unverified until a transcript or Actions artifact is retained.
