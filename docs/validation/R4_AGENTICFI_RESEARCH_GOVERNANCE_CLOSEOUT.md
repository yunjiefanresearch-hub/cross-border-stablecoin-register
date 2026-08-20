# R4 AgenticFi, research, governance and delivery closeout

Date: 2026-08-20  
Release candidate: CBSR 0.11.0 R4 local deployment bundle  
Decision: engineering verification passed; legal-currentness and external-assurance release gates remain open.

## Verified repository delivery

| Area | Result | Evidence |
|---|---|---|
| General action-policy schemas | Passed | versioned action, mandate, decision, receipt and domain-pack JSON Schemas |
| Stablecoin domain pack | Passed | version 1.1.0 manifest, validation and obligation catalogue |
| Mandate model | Passed | prohibited jurisdiction, validity, time windows, thresholds, version and audit identity |
| Complete receipt | Passed | rules, URLs, freshness, assumptions, uncertainty, mandate/audit identity, versions, timestamp and component digests |
| AgenticFi scenarios | Passed | 31 table-driven scenarios and 11 receipt mutations |
| Pilots | Passed | two deterministic end-to-end pilots with identical replay and valid receipts |
| Research inventory | Passed as a repository deliverable | 152-row ledger, 12 evidence dossiers, quantitative and qualitative outputs, 157 claims |
| Whitepaper | Passed as a repository deliverable | 455-line institutional paper at the canonical requested path with formal bibliography and claims traceability |
| Public-interest mappings | Passed as self-assessment | DPG 1-9C, six specified SDG targets, GDC and 18 DPI safeguards plus 13 risks |
| Security and supply chain | Passed locally / declarations present | secrets, SBOM, licences, audit, reproducible wheel; CodeQL/dependency/gitleaks/Scorecard/provenance workflows |
| Formal delivery set | Passed | baseline, transformation, risk, decision, compatibility, migration, rollback, PR plan, scorecard and manifests |

## Canonical verifier evidence

- Canonical steps: **73/73 passed** for each local Linux interpreter.
- Invariants: **59/59 passed**.
- Pytest: **59 passed**.
- Generated artifacts: **332**, unchanged after pass 1 and byte-identical after pass 2.
- AgenticFi evaluation: **31 scenarios**, **11 receipt mutations**, **2 reproducible pilots**.
- Research: **152 cases**, **12 dossiers**, **157 claims**, **40 manifest files**.
- Governance: **11 DPG indicators**, **6 SDG targets**, **6 GDC commitments**, **18 DPI principles**, **13 risks**.
- Secret scan: **712 text files**, **5 high-confidence patterns**, no findings.
- Package: two byte-identical wheel builds, clean repository-external install, all six AgenticFi capabilities, warnings treated as errors, valid unsigned receipt and execution disabled.
- Wheel SHA-256: `02bfe7589dfb0f3f7e28240be2c79da73cd86134c668015f8258146c60177d4b`.
- Source fingerprint: `d3193c1c680b3a023455829e005446c54035f7328b69508539e1014fcfc649e9`.

## Real local Linux matrix

| Python | Canonical result | Audit evidence | Wheel |
|---|---|---|---|
| 3.10.20 | 73/73 | lock-bound 2026-08-20 live snapshot | identical |
| 3.11.15 | 73/73 | lock-bound 2026-08-20 live snapshot | identical |
| 3.12.13 | 73/73 | live `pip-audit --strict` | identical |
| 3.13.14 | 73/73 | lock-bound 2026-08-20 live snapshot | identical |

This is current-source local Linux evidence, not a claim that GitHub Actions or Windows ran.

## Legal and external hard stops

- Freshness remains `current=0`, `stale=38`, `unknown=114`.
- Official source disposition remains `official=100`, `unavailable=52`; 27 evidence tiers remain unverified.
- Independent second legal reviewers remain `0/152`; decision-ready records remain `0/152`.
- The second qualitative coder, independent whitepaper peer reviewer and independent security reviewer have not completed attestations.
- GitHub Actions, ruleset/branch protection, Draft PRs, signed release and provenance have not been remotely read back.
- Windows 11/`windows-latest` has not produced a current transcript or artifact.

These are real assurance dependencies, not defects that source code can truthfully mark complete. The R4 bundle is runnable and fail-closed, but it is not labelled legally current, independently reviewed, production-secure or fully release-ready.
