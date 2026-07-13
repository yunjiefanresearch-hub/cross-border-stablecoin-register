# Licensing

The register is dual-licensed so the **data stays citable** (attribution required) and the
**tooling stays permissively reusable**.

| What | License | File |
|---|---|---|
| **Data** — every `*.yaml` record, the corridor files, the compiled `dataset.json`, the generated `COVERAGE.md` / `records.md` tables, `analysis/`, `api/` | **CC-BY-4.0** | [`LICENSE`](LICENSE) |
| **Code** — `build*.py`, `scripts/`, `tools/`, `run_*.py`, `src/cbsr_mcp/`, `mcp_server.py` | **Apache-2.0** | [`LICENSE-CODE`](LICENSE-CODE) |

Attribution for the data is satisfied by citing the DOI in [`CITATION.cff`](CITATION.cff).

## Why the root `LICENSE` file holds the data license

GitHub detects a repository's license by matching the **root `LICENSE`** file against the verbatim
text of a known license. Through v0.10.1 that file held a *custom summary* of the dual-license
arrangement rather than any license's legal code, so GitHub's own badge read
**"Unknown and 2 other licenses found"** — on a project whose entire pitch is that it is open,
citable and safe to reuse. A compliance reader evaluating whether they may build on the register
saw the word *Unknown*.

The register's headline artefact is the **data**, so the root `LICENSE` now carries the verbatim
CC-BY-4.0 legal code and GitHub reports `CC-BY-4.0`. The code license keeps its own verbatim file,
and this page is the human-readable map. Nothing about the actual grant of rights changed.
