# Remote GitHub completion runbook

Committed workflow and policy files do not prove GitHub is configured or has run them.

1. Push the five review branches in `PR_STACK_PLAN.md` to the authorized repository.
2. Create Draft PRs and record exact URLs and head/base SHAs.
3. Run `CBSR canonical verification`; require the stable `required-verification` check.
4. Retain all four Python logs, the Windows transcript, verification JSON, wheel, SBOM, licences and audit.
5. Enable a default-branch ruleset: pull request required, two approvals for regulatory changes,
   CODEOWNERS review, required conversation resolution, no force push/deletion and required signed commits
   if the organization's signing policy supports it.
6. Enable private vulnerability reporting, secret scanning/push protection, Dependabot alerts and CodeQL.
7. Query or inspect the saved settings and write the actual evidence URLs/JSON into the release record.
8. Publish only after legal, peer and security attestations are complete; attach checksums and provenance.

Do not paste a personal access token into this repository, an issue, a log or chat transcript.
