# OpenSSF Best Practices Gold readiness

Status: evidence inventory and remediation plan; criteria reviewed 10 September 2026,
hosted evidence updated 15 September 2026.

This document is **not a certificate, an independent assessment, or an award of an
OpenSSF badge**. The OpenSSF Best Practices program describes its process as voluntary
self-certification: a project explains how it meets each criterion, and those statements
remain open to verification and correction. This repository matrix is deliberately more
conservative than a self-assessment form and makes no Passing, Silver, or Gold claim.

Gold is cumulative. The official Gold prerequisite is an achieved Silver badge, and the
official Silver prerequisite is an achieved Passing badge. Neither the complete Passing
questionnaire nor the complete Silver questionnaire was verified in this review. A badge
image, workflow declaration, policy file, or local green test is not a substitute for
completing those prerequisites and providing truthful evidence in BadgeApp.

## Official basis

The English criteria are authoritative. This inventory was checked against both the concise
and detailed/rationale views:

- [Passing criteria](https://www.bestpractices.dev/en/criteria/0) and
  [Passing details](https://www.bestpractices.dev/en/criteria/0?details=true&rationale=true)
- [Silver criteria](https://www.bestpractices.dev/en/criteria/1) and
  [Silver details](https://www.bestpractices.dev/en/criteria/1?details=true&rationale=true)
- [Gold criteria](https://www.bestpractices.dev/en/criteria/2) and
  [Gold details](https://www.bestpractices.dev/en/criteria/2?details=true&rationale=true)
- [Criteria discussion, including why the program uses self-certification](https://www.bestpractices.dev/en/criteria_discussion)

The official pages control if this file becomes stale. `MUST` and `MUST NOT` items must be
met; `SHOULD` items must be met or have an accepted justification in the official process.

## Status vocabulary

- **Candidate evidence** — a repository artefact appears relevant, but this document does
  not assert that BadgeApp has accepted it or that the live control operated.
- **Policy only** — a forward-looking requirement is documented, but historical execution
  has not been proved.
- **Partial** — some evidence exists, but it does not cover the complete criterion.
- **Gap** — the criterion is not demonstrated.
- **Human/external evidence required** — repository contents alone cannot establish it.
- **N/A candidate** — the official criterion permits N/A in a narrow case; a maintainer must
  verify the scope and enter a truthful justification before selecting N/A.

## Complete Gold matrix (23 criteria)

| # | Criterion ID | Current repository evidence | Conservative status | Gap and acceptance evidence |
|---:|---|---|---|---|
| 1 | `achieve_silver` | No achieved Passing or Silver badge was validated for this repair. | **Gap / prerequisite blocked** | Complete and truthfully evidence every [Passing](https://www.bestpractices.dev/en/criteria/0) and [Silver](https://www.bestpractices.dev/en/criteria/1) criterion in the official service; record the actual project URL and status. |
| 2 | `bus_factor` | [GOVERNANCE.md](../../GOVERNANCE.md) identifies one accountable maintainer; [CODEOWNERS](../../.github/CODEOWNERS) names a single account, not two independently capable people. | **Gap; human evidence required** | Name at least two people able to review, merge, handle reports, and release; document access continuity and test that loss of one person does not stop those functions. |
| 3 | `contributors_unassociated` | No reviewed affiliation and contribution ledger establishes this. Git identities alone cannot prove association or independence. | **Gap; human evidence required** | Identify two contributors who made non-trivial contributions in the last year, document their affiliations/conflicts, and explain why each qualifies under the official definition. |
| 4 | `copyright_per_file` | [LICENSING.md](../../LICENSING.md) and the root licence files identify project-wide licensing, but a repository scan found no systematic per-source-file copyright notices. [CONTRIBUTING.md](../../CONTRIBUTING.md) now sets a prospective rule for new files. | **Gap / policy only** | Define the source-file inventory, add an accurate copyright statement to every applicable source file, handle generated/commentless formats explicitly, and verify the inventory in CI. Do not bulk-attribute files without confirming ownership. |
| 5 | `license_per_file` | [LICENSE-CODE](../../LICENSE-CODE), [LICENSE-DATA](../../LICENSE-DATA), and [LICENSING.md](../../LICENSING.md) provide repository-level grants; existing files do not consistently carry SPDX or equivalent notices. | **Gap / policy only** | Apply the correct per-file expression (`Apache-2.0` for code, `CC-BY-4.0` for covered data) after inventory review, document exceptions, and add a CI check. Repository-level licence files remain required but do not replace this Gold item. |
| 6 | `repo_distributed` | The project is maintained in a public Git repository; the README points to its GitHub origin. | **Candidate evidence** | Record the public repository URL and immutable revision in BadgeApp; verify the live repository is the canonical change history. |
| 7 | `small_tasks` | Six public tasks now identify bounded deliverables, acceptance owners and criteria: [US source](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/14), [EU second review](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/15), [UK commencement](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/16), [CN/TW language evidence](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/17), [clean-room reproduction](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/18), and [one integration query](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/19). | **Candidate evidence; maintenance required** | Keep the queue discoverable and current, confirm newcomer suitability, and provide guidance during claims. Legal-source tasks still require qualified human review; issue creation does not establish adoption or independent contribution. |
| 8 | `require_2FA` | No repository file can prove organization enforcement, collaborator enrolment, recovery policy, or protection of private vulnerability reports. | **Gap; external settings evidence required** | Enable organization/repository 2FA requirements, verify every privileged developer and sensitive channel is covered, and retain dated settings/readback evidence without exposing recovery secrets. |
| 9 | `secure_2FA` | No verified record identifies the enrolled factors. | **Gap; private human evidence required** | Require WebAuthn/passkeys, hardware security keys, or TOTP rather than SMS-only authentication, and record a non-sensitive attestation of enforcement. Never publish seeds or recovery codes. |
| 10 | `code_review_standards` | [CONTRIBUTING.md](../../CONTRIBUTING.md), the [PR template](../../.github/pull_request_template.md), and [CODEOWNERS](../../.github/CODEOWNERS) now describe scope, reviewer checks, tests, style, security, generated output, and human approval. | **Policy only / candidate after merge** | Confirm links are public, apply the checklist on real pull requests, and keep it aligned with required checks and release practice. Documentation alone does not prove review happened. |
| 11 | `two_person_review` | CONTRIBUTING adopts a stricter prospective rule for non-trivial changes. No reviewed PR sample, ruleset readback, or historical denominator proves the required threshold. | **Gap / policy only; human evidence required** | Protect the release branch, require a human approval from a non-author, and measure reviewed proposed modifications for each release. Bots, AI systems, and CI are not the second person. A project member may review; cross-organization review is preferable but not required by this criterion. |
| 12 | `build_reproducible` | [`tools/verify.py`](../../tools/verify.py) and package-smoke tooling perform repeated generation and wheel comparison; release artefacts include hashes and provenance inputs. | **Partial** | Publish an independently repeatable build recipe with a fixed toolchain/environment, have another party reproduce the same revision, and compare bit-for-bit artefact hashes. Two builds in one process or one environment are useful but not by themselves complete independent reproduction evidence. |
| 13 | `test_invocation` | [`Makefile`](../../Makefile) provides `make test`; `python -m pytest -q` is the standard quick suite and `python -m tools.verify` is the canonical aggregate gate. | **Candidate evidence** | Verify both documented commands on a clean supported environment and link a successful public run. Do not substitute a hand-picked subset for the release verifier. |
| 14 | `test_continuous_integration` | [Hosted run 34481297430](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34481297430) passed the full canonical verifier on Linux Python 3.10–3.13, Windows Python 3.12 clean-room, and the aggregate required-verification job for repair commit `270a002e8d66bb9971b3638dfcab52f3b2f6d2fd`. | **Hosted execution evidenced; enforcement/cadence review required** | Retain successful exact-commit runs, verify required-check enforcement and normal integration cadence, and investigate failures. A successful run is not itself proof of branch protection or a Gold award. |
| 15 | `test_statement_coverage90` | `.coveragerc`, `constraints/quality.txt`, and `tools/check_gold_coverage.py` define whole-repository Python measurement and a separate runtime diagnostic. The 15 September local combined canonical measurement is 72.07% (6,697/9,292 statements), with the limitations below; the earlier hosted pytest-only baseline was 14.73%. | **Measured below threshold; remediation required** | Publish combined hosted evidence and add effective tests until the whole-project statement threshold passes. Do not claim project-wide Gold from the narrower runtime diagnostic. |
| 16 | `test_branch_coverage80` | The same local combined measurement is 61.44% branches (2,073/3,374), versus the earlier hosted pytest-only 10.50%; no accepted Gold result is asserted here. | **Measured below threshold; remediation required** | Demonstrate the branch threshold over the declared whole-project denominator, publish the exact command/configuration/result, and explain any technically excluded files. Test count and statement coverage cannot substitute for branch coverage. |
| 17 | `crypto_used_network` | [`src/cbsr_mcp/server.py`](../../src/cbsr_mcp/server.py) runs the packaged MCP server over stdio, and [SECURITY.md](../../SECURITY.md) describes an offline decision-support boundary. Documentation also describes optional HTTPS-hosted static API use. | **N/A candidate / scope review required** | Review every supported runtime transport and deployment mode. If the produced software truly performs no network communication, enter a precise N/A justification; otherwise test that insecure protocols are disabled by default and document secure configuration. |
| 18 | `crypto_tls12` | Repository and documentation URLs use HTTPS, but no repository artefact establishes protocol negotiation for every supported host or client. | **N/A candidate or external test required** | Resolve the scope decision from row 17. For every TLS surface, test the deployed endpoint and client policy for TLS 1.2+ and rejection of obsolete SSL/TLS; retain dated results. |
| 19 | `hardened_site` | A HEAD check at approximately 2026-09-10 06:50 UTC found the Register GitHub Pages endpoint returned 200 with `Strict-Transport-Security: max-age=31556952`, but CSP, `nosniff`, and `X-Frame-Options` were absent. The Mapper GitHub Pages endpoint returned 200 with all four headers absent. A local TLS connection to `https://cbsr.io/` failed; that single observation cannot establish global availability or header state. GitHub-hosted repository controls remain relevant but do not cure the Pages/download endpoints. HTML CSP meta markup is not an HTTP response header. | **Gap; live external test required** | Inventory every canonical website, repository, Pages/API, package, and download URL; repeat and retain response captures from a reliable network; then configure an approved hosting/fronting layer capable of all four nonpermissive response headers, or move hosting. Either infrastructure change needs separate authorization. Never add a meta tag and present it as response-header evidence. |
| 20 | `security_review` | [`docs/SECURITY_REVIEW_v0.11.md`](../SECURITY_REVIEW_v0.11.md) records automated results and limitations; [`THREAT_MODEL.md`](THREAT_MODEL.md) defines boundaries; [`EXTERNAL_SECURITY_REVIEW_TEMPLATE.md`](EXTERNAL_SECURITY_REVIEW_TEMPLATE.md) is intentionally blank. None proves that an identified human completed the required review. | **Gap; human evidence required** | An identified human must review a fixed revision, security requirements, trust boundary, findings, and remediation, then sign/date the record. Official Gold permits a project member or independent evaluator; independence is not mandatory. The project's separate release policy may retain a stricter independent-review gate. |
| 21 | `hardening` | [THREAT_MODEL.md](THREAT_MODEL.md), schema validation, fail-closed policy gates, receipt mutation tests, negative tests, least-privilege workflows, and pinned dependencies are relevant application-level controls. | **Partial** | Map hardening mechanisms to every executable/runtime boundary, demonstrate they are enabled in release artefacts, and provide a reviewed justification for any N/A component. Design intent and tests alone do not prove deployed hardening. |
| 22 | `dynamic_analysis` | The pytest and negative suites execute code, but this review found no explicitly designated dynamic-analysis tool, release record, or accepted N/A justification satisfying this separate criterion. | **Gap** | Select an appropriate FLOSS dynamic technique (for example property/fuzz testing of parsers and policy inputs or DAST for an actually deployed surface), make it a recorded major-release step, triage findings, and retain the run evidence. Do not relabel ordinary tests after the fact without a defensible scope. |
| 23 | `dynamic_analysis_enable_assertions` | Tests and validation tools contain assertions and negative cases, but row 22 is not yet established and no evidence shows which assertions were enabled during a qualifying dynamic-analysis run. | **Partial / justification required** | Once dynamic analysis is defined, enable and document applicable assertions/contracts during the run and link results; otherwise provide a specific BadgeApp justification for why additional assertions are not applicable or practical. |

## Reproducible evidence commands

Local evidence from 10 September 2026: the offline repair check completed two
generation passes with unchanged hashes and all 23 local validation stages
(73 process steps total). The Python suite passed 94 tests. This does not include
the canonical verifier's isolated wheel installation or network vulnerability audit.

The pytest-only coverage run at 11:42 UTC measured 876/8641 Python statements
(10.14%) and 174/3102 branches (5.61%) across the repository source inventory.
The runtime-only diagnostic was 787/1315 statements (59.85%) and 151/452 branches
(33.41%). No source file was missing from the inventory. The separate canonical
subprocess suites were not instrumented in this measurement, so this is a
baseline, not the combined suite's final coverage. It does not meet Gold thresholds.

Later that day the complete canonical verifier passed all 77 atomic steps on
Windows with CPython 3.12.14, including 97 pytest cases, two identical wheel builds,
a clean installation, six-tool smoke tests and a live vulnerability audit with no
known vulnerabilities. The local run used a new dedicated temporary directory and
disabled pytest's optional cache after an existing temporary-directory ACL conflict.
The matching summary and transcript are in `artifacts/validation/`; hosted CI and
the human/external Gold criteria still need their own evidence. This supersedes
the earlier local packaging limitation, not the coverage or qualification gaps.

### Published repair follow-up

The latest source-only pytest measurement at 12:48 UTC passed 97 tests and counted
879/8644 statements (10.17%) and 176/3104 branches (5.67%); no Python source files
were missing. Runtime-only diagnostics were 790/1318 statements (59.94%) and
153/454 branches (33.70%). These are still pytest-only measurements, not combined
subprocess-suite coverage, and neither Gold threshold is met.

The subsequent [hosted canonical run](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34481297430)
provides successful Linux and Windows execution evidence for commit
`270a002e8d66bb9971b3638dfcab52f3b2f6d2fd`, whose source tree exactly matches local
commit `7a9dec44db1d09992e83a58eb1d64330a06b37ae`. CodeQL, security gates and the
coverage-report workflow also passed for that repair. Report generation passing
does not mean coverage thresholds passed.

One separate local final rerun passed its first 76 steps but could not resolve the
locked `pydantic-core==2.41.5` distribution during clean installation. That failed
run is retained, not rewritten as a pass. A subsequent official Windows wheel
download and standalone package-smoke retry both succeeded: two identical wheels,
clean installation, all six tool checks, warning-free import and a live audit with
no known vulnerabilities. The wheel SHA-256 was
`4281ccfd70e7ae1fead2bdc126b7009f537b418b41fc8def9bff7c055276d625`.
Only the hosted canonical run establishes a complete successful run for the
published repair; separate local stages must not be spliced into a synthetic pass.

The first hosted Dependency review attempt failed because Dependency Graph was
disabled. The maintainer subsequently reported enabling it, and the
[second workflow attempt](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34481297481/attempts/2)
completed successfully. The success is based on the rerun outcome, not the settings
report alone. No failing security gate was bypassed.

### Supply-chain follow-up (15 September 2026)

The [hosted coverage report for PR head `de5c3ad`](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34864683315)
passed 146 pytest cases. Its full Python source inventory measured 1,355/9,197
statements (14.73%) and 350/3,334 branches (10.50%), with no missing source files.
The narrower runtime diagnostic was 790/1,318 statements (59.94%) and 153/454
branches (33.70%). Both whole-project threshold flags were false. The PR workflow
measures and uploads evidence; its threshold-enforcement step was skipped, so its
successful status does not establish Gold coverage. The default PR checkout tested
the merge candidate, not an independent reproduction of the branch alone.

The same head's [canonical matrix](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34864683363)
passed Linux Python 3.10-3.13 but failed Windows: the root `build.py` dataset generator
shadowed PyPA's build module, leaving no installable wheel. The aggregate check
correctly failed. This follow-up isolates packaging module lookup and explicitly
selects UTF-8, with a regression test and a successful local wheel build/install.
The subsequent [hosted run for `7df6096`](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34926810451)
passed all five platform jobs and the required aggregate, with 78 canonical steps
and 155 pytest tests on Windows. The failed run is not relabelled as a pass.

The current measurement workflow instruments the canonical verifier and its
same-environment subprocesses, combines their data, and binds the report to a
successful same-attempt verification summary and the current source fingerprint.
It retains the whole-project source denominator. Temporary source copies used by
legacy negative tests and the clean-wheel smoke's separate runtime environment
are not covered by this instrumentation; their independent test results remain
separate evidence. Executed lines do not automatically imply effective assertions.
The initial local combined run completed at 09:24 UTC on 15 September with all 79
canonical steps passing, including 172 pytest tests (one third-party parser
deprecation warning), a complete current-Windows-platform audit of 73 locked
packages with zero known vulnerabilities, and two identical clean-install-tested
wheels. The package import/six-tool smoke itself remained warning-free.

Its source fingerprint was
`186014a59b9805c734054ed5c54e182d555eff529bbb2dfad32a71a6b09b6b78`.
The report measured 6,697/9,292 statements (72.07%) and 2,073/3,374 branches
(61.44%), with no missing source files and a valid canonical-summary binding.
Both thresholds remain false. The measurement change accounts for execution
previously omitted; it is not a claim that assertions suddenly improved by the
same amount. These local results do not substitute for the next hosted matrix.

These commands collect evidence; they do **not** award a badge or convert a gap into a met
criterion without review of the result.

```bash
# Standard tests and the canonical aggregate gate
python -m pytest -q
python -m tools.verify

# Whole-repository Python coverage plus a runtime-only diagnostic in one report.
python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt -r constraints/quality-hashes.txt
python -m coverage erase
python -m coverage run --context=canonical tools/verify.py
python -m coverage combine
python -m coverage json --show-contexts
python tools/check_gold_coverage.py --verification-summary artifacts/validation/verify-summary.json

# Smaller pytest-only diagnostic (erase/combine are still required):
python -m coverage erase
python -m coverage run -m pytest -q
python -m coverage combine
python -m coverage json
python tools/check_gold_coverage.py

# Acceptance form: intentionally exits non-zero while either threshold or the
# complete source-file inventory is not satisfied.
python tools/check_gold_coverage.py --enforce

# Inventory candidate per-file notices; review results manually because file
# type, generated status, ownership, and code/data licensing differ.
rg --files-without-match "Copyright" -g "*.py" -g "*.ps1" -g "*.sh" .
rg --files-without-match "SPDX-License-Identifier" -g "*.py" -g "*.ps1" -g "*.sh" .
```

For 2FA, contributor independence, branch protection, review history, live response headers,
and the human security review, collect non-sensitive dated evidence from the responsible
people or hosted service. Never commit private vulnerability details, factor seeds, recovery
codes, credentials, or personal identity documents merely to make a badge answer auditable.

## Claim rule

Do not describe CBSR as OpenSSF Gold-ready, Gold-certified, Gold-compliant, externally
certified, or independently audited while any row above is a gap or prerequisite is
unverified. After remediation, a maintainer must refresh this matrix against the then-current
official English criteria, complete Passing and Silver first, submit truthful evidence through
BadgeApp, and link only the status actually shown by the official project page.
