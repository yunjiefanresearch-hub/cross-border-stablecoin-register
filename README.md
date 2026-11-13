# Cross-Border Stablecoin Register (CBSR)

An open, versioned register of how twelve jurisdictions regulate stablecoins: the United States, the European Union, the United Kingdom, Singapore, Hong Kong, mainland China, Brazil, Switzerland, the United Arab Emirates, Taiwan, Japan and South Korea. Maintained by Yunjie Fan as independent research. Website: [cbsr.site](https://cbsr.site).

The register is a research reference. For legal decisions, check the cited source and its date with a qualified adviser.

## What a record contains

Each record is one proposition about one jurisdiction, instrument and dimension. It keeps the following information in separate fields.

- **Kind of claim** (`claim_class`): a rule of law (`tier1_legal`) or a market or operational fact (`tier2_operational`).
- **Strength of the source** (`evidence_tier`): confirmed against the official text (`resolution_text`), core point confirmed (`mixed`), resting on practitioner analysis (`firm_summary`), or `unverified`.
- **Binding status**: for example in force, enacted but not yet in force, or proposed; the full list of values is in [METHODOLOGY.md](METHODOLOGY.md).
- **Source**: the instrument and pinpoint, with a URL where one has been recorded.
- **Source check and review state**: the date of the last check against the source, marked unknown where none has been recorded, and the review the record has had.

## Current state

**Status:** v0.11.0 (data snapshot generated 20 August 2026).

- [Coverage](COVERAGE.md) reports the evidence tiers, populated source URLs and the records that meet the structural test for citable law.
- [Snapshot metadata](api/meta.json) reports the official-source field separately from the evidence tiers and lists the record, corridor and MCP tool totals.
- [Source-check report](analysis/freshness_report.json) records current, stale and missing checks. No record has a current source check or an independently attested second review, so the decision-ready subset is empty.
- [Corridor analysis](COVERAGE.md#computed-layer-preview) uses 30 June 2026 as the reference date. It reports a feasibility class or an indeterminate result for each directed corridor, and shows where the rule engine reproduces the hand-worked corridors and jurisdiction-pair categories. The two differences are EU–UK and UK–US.
The [v0.11.0.post1 engineering update](docs/releases/UPDATE_v0.11.0.post1.md) uses the same data snapshot.

## Use

- [Download the dataset](dataset.json) or read the [dataset guide](https://cbsr.site/data/). The analysis layer is under `analysis`.
- [Query the dataset with typed MCP tools](MCP_SERVER.md). In v0.11.0, `citable_law()` returns an empty result.
- [Explore the CBSR mapper](https://github.com/yunjiefanresearch-hub/cbsr-mapper).
- [Find open tasks](docs/OPEN_TASKS.md) or read the [contribution guide](CONTRIBUTING.md).

Use the hash-locked development dependencies to verify a checkout.

```bash
python -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
.venv/bin/python -m tools.verify
```

On Windows, use [the Windows setup guide](LOCAL_DEPLOY_WINDOWS.md). The [development constraints](constraints/README.md) list supported environments.

## Cite

Fan, Y. (2026). *Cross-Border Stablecoin Register* (v0.11.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.22021736

Cite the version you used and record its source commit when reproducing a result. See [CITATION.cff](CITATION.cff) for citation metadata and [the release archive guide](docs/VERSIONS.md#citing) for version DOIs.

## Licences

Data under CC BY 4.0, code under Apache-2.0; see [LICENSING.md](LICENSING.md).

## How it is made

The code was written with AI coding assistants. The maintainer sources the legal records and records each one's review state; see [METHODOLOGY.md](METHODOLOGY.md) and [GOVERNANCE.md](GOVERNANCE.md).

## Maintainer

Yunjie Fan (yunjiefan.research@gmail.com).

The design history of the build is in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and release notes are in [CHANGELOG.md](CHANGELOG.md) and [the build and upgrade notes](docs/history/).
