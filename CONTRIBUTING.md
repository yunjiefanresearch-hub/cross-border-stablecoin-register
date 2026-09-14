# Contributing

Records are proposed as schema-validated additions to the data files.

1. Create an isolated environment and install the complete committed graph:
   `python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt`.
2. Copy `_TEMPLATE.yaml` to `<id>.yaml`.
3. Fill every field. Cite a **primary** source with a pinpoint; verify it yourself.
4. Run the only aggregate gate: `python -m tools.verify` (or `make verify`). Do not replace it with
   a hand-picked subset of build commands.
5. Review any regenerated diff. The verifier must finish with no committed-output drift and a matching
   second generation pass.
6. Open a PR. Drafts (records with `<VERIFY` markers) are welcome but are merged as drafts (✍️),
   not as verified coverage.

Dependency changes use `python tools/refresh_constraints.py --write`, then regenerate and review
the wheel hashes as described in `constraints/README.md`, followed by the same verifier.
They require a passing Linux Python 3.10-3.13 matrix and Windows clean-room job before merge.

The register follows the source hierarchy and verification rule in `METHODOLOGY.md`.

## Acceptance policy

This section is prospective project policy. Its presence does not claim that historical
changes received human review, reached a coverage target, or satisfied an OpenSSF badge.

### Scope and change record

- Keep each pull request reviewable and state the intended user-visible outcome, files in
  scope, generated outputs, and residual risks. Do not mix unrelated refactors with a data,
  dependency, security, or release change.
- Link the issue or worklist cell when one exists. A maintainer marking a task `good first
  issue` or `small task` must give it a bounded outcome, expected files, acceptance checks,
  and enough context for a new contributor to finish it.
- Never hand-edit a generated artefact to conceal source drift. Change its source, run
  `python -m tools.verify`, and review the complete regenerated diff.

### Style and warnings

- Python changes follow [PEP 8](https://peps.python.org/pep-0008/), preserve the repository's
  existing type-annotated interfaces, use explicit encodings for text files, and avoid
  broad warning suppressions. New warnings must be fixed or documented as reviewed false
  positives.
- YAML and JSON changes must satisfy their versioned schemas, preserve stable identifiers,
  and remain deterministic under the generator. Markdown uses portable CommonMark-style
  links and must pass the internal-link gate.
- Match nearby structure when no automated formatter covers a file. Manual review is not a
  claim that the Silver automatic-style-enforcement criterion is met; tooling and evidence
  for that criterion must be assessed separately.

### Tests and regressions

- Major new functionality **must** add automated tests that cover its success, rejection,
  and relevant boundary paths. Documentation of the feature and its external interface must
  change with it.
- A bug or security fix **must** add a regression test that fails before the fix and passes
  after it whenever a safe automated reproduction is possible. If it is not possible, the
  pull request must explain why and give a reviewer-verifiable alternative.
- `python -m pytest -q` (or `make test`) is the standard quick test invocation. Before
  acceptance, run the aggregate `python -m tools.verify` (or `make verify`); the quick suite
  is not a substitute for the canonical gate.
- Test count is not coverage. Do not claim the OpenSSF Gold 90% statement or 80% branch
  thresholds until the whole-repository measurement described in
  `docs/security/OPENSSF_GOLD.md` produces and publishes those results. A runtime-only view
  cannot establish project-wide coverage.

### Security requirements

- Preserve the security boundary in `SECURITY.md` and `docs/security/THREAT_MODEL.md`:
  CBSR is decision support, never execution authority; inputs are schema-validated and
  unknown, stale, conflicting, or insufficient evidence fails closed.
- Do not commit credentials, private vulnerability details, personal data, private legal
  files, production decision payloads, 2FA seeds, or recovery codes. Report exploitable
  vulnerabilities through the private process in `SECURITY.md`, not a public issue.
- Dependency changes must use `python tools/refresh_constraints.py --write`, refresh the reviewed
  hash locks following `constraints/README.md`, receive
  dependency/security review, and pass the complete supported-platform verifier.
- A change that introduces a network transport or client must use secure protocols by
  default, support TLS 1.2 or later when TLS is used, disable obsolete/insecure protocols by
  default, document its trust boundary, and add negative configuration tests.
- Changes to parsing, policy decisions, receipts, dependency loading, release provenance,
  hosted surfaces, authentication, or vulnerability handling require an identified human
  security reviewer. Update the threat model when assets, entry points, trust boundaries,
  or residual risks change.
- Before a proposed major production release, run and record an appropriate FLOSS dynamic
  analysis technique in addition to ordinary tests. This policy does not claim that a
  qualifying dynamic-analysis run or human security review has already occurred.

### Human review and release acceptance

Every non-trivial source, data, schema, dependency, workflow, security, release, or public
claim change requires approval before release from at least one identified person other than
the author. The reviewer must determine that the change is worthwhile and free of known
issues that argue against inclusion, and must check:

1. scope, provenance, licensing, and compatibility;
2. code/data style, schema validity, and generated-output determinism;
3. success, rejection, boundary, and regression tests;
4. security impact, secrets/privacy, dependencies, and threat-boundary changes;
5. documentation, changelog, version, API/MCP manifest, and rollback impact; and
6. every disclosed limitation, skipped check, or unresolved external dependency.

Approval must be attributable in the pull request or, for a confidential vulnerability,
in the protected review record. The author cannot approve their own work. Bots, AI tools,
automated checks, and `CODEOWNERS` routing do not count as the other person. If no human
reviewer is available, the change remains unapproved for release; a green CI run does not
waive this requirement.

The pull-request reviewer and the independent second reviewer required to promote legal
evidence are separate roles and attestations. One must not be inferred from the other.
OpenSSF Gold permits a project member to conduct its human security review; it does not
require independence. CBSR may retain the stricter independent-review release condition in
`SECURITY.md`, and this contribution policy does not weaken it.

### Per-file notices for new source

Follow `LICENSING.md`: code is Apache-2.0 and covered register data is CC-BY-4.0. New
hand-written source files whose format permits comments must carry an accurate copyright
statement and the matching SPDX licence expression near the beginning, for example:

```text
Copyright the Cross-Border Stablecoin Register contributors.
SPDX-License-Identifier: Apache-2.0
```

Use `SPDX-License-Identifier: CC-BY-4.0` for covered data source files. If a new file's
classification, ownership, generated status, or comment syntax is unclear, disclose it in
the pull request and obtain a maintainer decision before merge; do not guess. This rule for
new files does not assert that the existing per-file notice backlog is complete.
