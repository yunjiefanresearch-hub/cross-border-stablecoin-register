# Baseline reproduction

Date: 2026-08-20  
Scope: user-supplied R3 acceptance audit to the current source snapshot.

The deployment ZIP intentionally excludes `.git`; therefore the reported historical baseline
`c723b9b4ec4dc86d7e13bc79681ba63101feb380` and foundation
`e91fdee15a330f3fc2f003994f3816c7ef827226` cannot be re-resolved from the ZIP. They are labels from the
acceptance record, not hashes this bundle claims to contain.

## Reproduction sequence

```bash
python -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
python -m tools.verify
```

The verifier regenerates committed outputs twice, hashes them, runs the full test and research suite,
builds the wheel twice, clean-installs it outside the repository, exercises all six AgenticFi
capabilities, scans dependencies/licences/secrets and writes machine-readable evidence.

## Baseline and current facts

| Metric | Baseline | Current |
|---|---:|---:|
| Records | 152 | 152 |
| Full ledger rows | 4 targeted leads | 152 |
| AgenticFi scenarios | 10 | 31 |
| MCP server lines | 1,352 | 53 |
| Current records | 0 | 0 |
| Independent second reviews | 0 | 0 |

Engineering delivery expanded materially. Legal currentness did not, and is not represented as having
done so. Complete values and limitations are in `baseline_reproduction.json`.
