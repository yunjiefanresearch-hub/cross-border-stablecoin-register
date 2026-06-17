# Contributing

Records are proposed as schema-validated additions to `data/`.

1. Copy `data/_TEMPLATE.yaml` to `data/<id>.yaml`.
2. Fill every field. Cite a **primary** source with a pinpoint; verify it yourself.
3. Run `python scripts/build.py` — it must pass schema validation.
4. Open a PR. Drafts (records with `<VERIFY` markers) are welcome but are merged as drafts (✍️),
   not as verified coverage.

The register follows the source hierarchy and verification rule in `METHODOLOGY.md`.
