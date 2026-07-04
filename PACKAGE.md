# CBSR — package manifest

This archive is the **full Cross-Border Stablecoin Register repository (v0.9.9)**,
not a thin slice, with the two working papers and the three governance documents
included. It contains the YAML records, the schemas, the build, the analysis
layer, the MCP server, and the verification harness, so the register can be
built and queried, not just read.

## What runs, and what it produces

From the archive root, with Python 3:

```
python build.py             # validates records, builds dataset.json, COVERAGE.md, records.md
python run_invariants.py    # read-only structural invariants over the built register
python run_negative_tests.py# fault-injection battery proving each build gate bites
python check_readme_counts.py --scan README.md   # the README drift gate, standalone
```

These were run on this exact archive immediately before packaging:

- `build.py` exits 0: 152 records valid, citable subset (tier1_legal + in_force +
  resolution_text) = 46.
- `run_invariants.py` exits 0: 49/49 invariants hold, including R1 (the README
  states no drift-prone count).
- `run_negative_tests.py` exits 0: 10/10 gates bite, including the README-counts
  gate, whose injected defect is a *spelled* count.
- `check_readme_counts.py` runs standalone: self-test passes; `--scan README.md`
  reports clean.

Because the data is present, the earlier limitation of the slice (the three
data-dependent scripts could not actually run) no longer applies: a reviewer can
reproduce the 152-record build, the 49 invariants, and the 10 negative tests
directly from this archive.

## One caveat on the validator path

`build.py` validates against `record.schema.json` using a built-in fallback
validator (a structural subset of JSON Schema Draft 2020-12), because the
packaging environment had `PyYAML` but not the `jsonschema` library and could not
install it offline. Every gate bit under the fallback. To exercise the full
Draft-2020-12 path as well, run on a machine with `jsonschema` installed; the
build prints which backend it used.

## MiCA §3.10 correction in this revision

The flagship paper's §3.10 (the intra-regime gating example) previously described
the MiCA Article 143(3) transitional window as expiring uniformly across all
twenty-seven Member States on 1 July 2026. That was wrong, and is corrected here,
verified against ESMA's own statement and the official Article 143(3)
grandfathering list: 1 July 2026 is the **outer cap**, the longest window any
Member State could grant; most States set shorter windows and closed earlier
(Germany and Ireland at twelve months, end of 2025; Finland, Latvia, Lithuania,
Hungary, the Netherlands, Poland, and Slovenia at six months, mid-2025; Sweden at
nine months, late 2025; France, Malta, and Luxembourg run the full window). What
binds a given corridor is the earliest deadline among the Member States it
touches, not the cap. The conditional flag and the summary-table cell were
updated to match.

## A note on dates (one day ahead at packaging)

Packaged 30 June 2026. §3.10 treats the 1 July 2026 outer cap as a future outer
limit, which is correct for a 30 June snapshot but leads it by a single day. The
national windows beneath the cap are mostly already closed and are written in the
past tense. If this is published on or after 1 July 2026, flip the outer-cap
phrasing to the past tense, the same way the Taiwan and Japan dated items are
handled. The other fast-changing facts (the Taiwan third reading, the 1 June 2026
Japan date, the BIS exit from mBridge) should likewise be re-checked against
primary sources at publication time.

## References

The external citations in both papers were verified against their primary records
(Springer, ACM, Oxford Academic, the W3C technical-reports index, the OASIS
standards registry, and the AEA) and carry their DOI or standard identifier with
confirmed volume, pages, and date. One residual is marked as such in the flagship:
regulatory horizon-scanning and scenario analysis are practitioner traditions with
no single canonical citation, named as traditions with a venue-appropriate source
to be selected.

## What is NOT in this archive

- The three substantive companion working papers referenced by the flagship's
  header, the *Multi-Jurisdiction Stablecoin Compliance Matrix* (v0.9.7), the
  *Cross-Border Stablecoin Architecture* (v0.2.8), and the *Cross-Border
  Digital-Finance Corridor Atlas* (v0.2.5), are prose write-ups that are not part
  of this repository and were not available to include. The data they rest on is
  here (the records, `COVERAGE.md`, and the `analysis/` layer), but the papers
  themselves are separate; add them and run the same membrane scan over them.

## Residuals to resolve in your environment

- Cross-references resolve within this archive: README and the governance
  documents reference `METHODOLOGY.md`, `CONTRIBUTING.md`, `ROADMAP.md`,
  `CHANGELOG.md`, `MCP_SERVER.md`, `COVERAGE.md`, `_TEMPLATE.yaml`, and each other,
  and all are present, so there are no dangling links in this package. (They would
  dangle only if the papers-and-governance subset were published on its own.)
- The commit history and issue tracker cannot be scanned from an archive; run
  `git log -p --all | grep -niwE '<your confidential term list>'` and an issues/PR
  search on the live repository, using the same whole-word vocabulary the membrane
  scan uses (kept out of this file deliberately, so the published repository
  carries no trace of it). Early pre-membrane traces are most likely to hide there.
- Resolved (was cosmetic, pre-existing): the V1/V2 label strings in
  `run_invariants.py` now track `EXPECT_VERSION` and read "0.9.9", matching the
  logic they check; the earlier "0.9.7" label / mismatched-logic wording is gone.

## Membrane

Every text file in this archive (records, schemas, scripts, analysis JSON, build
notes, papers, governance, 239 files in all) was scanned for the confidential
commercial vocabulary with a whole-word matcher confirmed live by a planted
canary: zero hits. The PDFs derive from the same scanned Markdown sources.
