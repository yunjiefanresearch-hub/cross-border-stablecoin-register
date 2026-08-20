# OpenSSF readiness checklist

This is a local readiness inventory, not an OpenSSF badge, score or external assessment.

| Control | Repository evidence | External evidence still required |
|---|---|---|
| Maintained build | `tools/verify.py`, `constraints/` | Successful required remote checks |
| Code review | `CODEOWNERS`, PR template | Ruleset readback and actual review record |
| Vulnerability disclosure | `SECURITY.md` | Private reporting enabled and response evidence |
| Dependency management | constraints and dependency-refresh workflow | Dependabot/dependency-review run readback |
| Static analysis | CodeQL workflow | Successful CodeQL run and reviewed findings |
| Secret protection | local secret scan and security workflow | GitHub secret scanning/push protection readback |
| SBOM and provenance | CycloneDX generator and provenance workflow | Signed release attestation readback |
| Security review | external-review template | Independent reviewer attestation |

Run `python -m tools.verify`; then complete the remote and human evidence columns before making a readiness claim.
