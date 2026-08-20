# Contributing

Records are proposed as schema-validated additions to the data files.

1. Create an isolated environment and install the complete committed graph:
   `python -m pip install --constraint constraints/dev.txt pip setuptools wheel`, then
   `python -m pip install --constraint constraints/dev.txt ".[dev]"`.
2. Copy `_TEMPLATE.yaml` to `<id>.yaml`.
3. Fill every field. Cite a **primary** source with a pinpoint; verify it yourself.
4. Run the only aggregate gate: `python -m tools.verify` (or `make verify`). Do not replace it with
   a hand-picked subset of build commands.
5. Review any regenerated diff. The verifier must finish with no committed-output drift and a matching
   second generation pass.
6. Open a PR. Drafts (records with `<VERIFY` markers) are welcome but are merged as drafts (✍️),
   not as verified coverage.

Dependency changes use `python tools/refresh_constraints.py --write`, followed by the same verifier.
They require a passing Linux Python 3.10-3.13 matrix and Windows clean-room job before merge.

The register follows the source hierarchy and verification rule in `METHODOLOGY.md`.
