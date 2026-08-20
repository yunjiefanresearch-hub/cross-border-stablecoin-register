# A-category reproducibility closeout

Date: 2026-08-20  
Release candidate: CBSR 0.11.0

## Acceptance map

| Requirement | Implementation | Local evidence | Release status |
|---|---|---|---|
| One canonical verifier | CI, README, CONTRIBUTING, Makefile and both Windows scripts call `python -m tools.verify` | Source cross-check; current R3 run on 3.12 plus historical foundation matrix | Implemented |
| Complete verifier | Two full regenerations, committed/hash-diff gate, research reproduction, two wheel builds, repository-external clean install, six-tool smoke, warning-as-error, SBOM, licences and strict vulnerability audit | Current R3: 59/59 steps on 3.12 | Implemented |
| Python 3.10-3.13 | CI matrix plus stable aggregate check | Foundation source passed four local interpreters; current R3 source has only a 3.12 local result | Fresh R3 matrix and GitHub-hosted run pending |
| Complete dependency lock | All runtime and development transitives pinned; interpreter markers cover the 3.10 graph fork; Python support bounded below 3.14 | One lock digest across four clean environments | Implemented |
| Maintainable upgrade path | Direct-window checker rejects prereleases and fully yanked versions; transitive freeze and four-version/Windows review are documented | Yanked `build 1.5.1` was detected and rejected during this closeout | Implemented |
| Windows clean room | Destructive action limited to the project `.venv` behind `-Recreate`; transcript, freeze and JSON evidence captured; workflow calls the same verifier | PowerShell source and workflow validated structurally | Real Windows 11 run pending |
| Setup is a hard prerequisite | Verifier is non-bootstrap and checks every active package against the lock before step 1 | Mismatched and incomplete environments fail in preflight | Implemented |
| MCP/Pydantic warning | MCP 1.29.0, Pydantic 2.12.5 and Pydantic Settings 2.14.2 are locked | Current R3 installed-wheel calls pass under `PYTHONWARNINGS=error` on 3.12; foundation did so on all four local versions | Implemented; fresh R3 matrix pending |

## Final local proof

- The foundation build passed the same 53-step verifier in four clean Linux environments
  (CPython 3.10.20, 3.11.15, 3.12.13 and 3.13.14). That historical evidence is retained in
  `local-linux-matrix.json`; it does **not** certify later source changes by itself.
- The regulatory/architecture closeout build passed the expanded 59-step verifier on
  CPython 3.12.13. It regenerated 280 committed artifacts twice without byte drift.
- The closeout wheel SHA-256 is
  `9a8f3075007827f7842e4f56ac15874aa47cfda1efabee9148300184ac8bee7f`.
- Constraint digest:
  `6970056c0c0b56de1cdc63e21d4cd5fb2ee2e4ca21242d31b2ca628b8ca37a7a`.
- The resolved Python 3.10 runtime received a live strict `pip-audit` with zero known
  vulnerabilities; `dist/pip-audit.json` preserves the report. Because the execution sandbox later
  denied advisory-network calls, final cross-version reruns used the matching 2026-08-20 live snapshot.
  The historical matrix reports label those results as snapshot-backed, not live. A fresh
  3.10-3.13 run is still required for the regulatory/architecture closeout source tree.

## External hard gates before a public release

1. Push the release-candidate branch and run `CBSR canonical verification` on GitHub Actions.
2. Require all four `verify-python-*` jobs, `verify-windows-clean-room-python-3.12` and the stable
   `required-verification` job to be green.
3. Download and retain every workflow artifact. Confirm the live CI `pip-audit` report is clean.
4. If Windows runner evidence is unavailable, run `setup_windows.ps1 -Recreate` on a physical Windows
   11 host and retain `artifacts/validation/windows/`.
5. Configure the default-branch ruleset to require `required-verification`, then verify the protection
   from GitHub. Do not infer protection from the workflow file.

No GitHub-hosted run or physical Windows claim is made by this Linux-built ZIP.
