# Methodology

This register is an expert artifact, not a scrape. Its value is the judgment in the data —
how sources are weighed and how ambiguity is resolved — made transparent and reproducible.

## Source hierarchy
1. **Primary** — statute, regulation, central-bank/regulator resolution or circular, official gazette.
   Every record's `source.primary` cites a primary instrument with a pinpoint.
2. **Regulator guidance** — supervisory guidelines, FAQs, consultation papers (as `secondary`).
3. **Secondary analysis** — law-firm client alerts, academic analysis. Used only to locate or
   interpret primary sources, never as the sole basis for a classification.

## Verification rule
A record is **verified** only when (a) it contains no `<VERIFY …>` markers and (b) a human has
checked every `source.primary` and `pinpoint` against the instrument itself. AI tools are **not**
used to generate or fill citations — a single fabricated source is fatal to a reference of this kind.
The build pipeline flags any record still containing `<VERIFY` as a **draft** and excludes it from
verified coverage counts.

## Status values
- `in_force` — effective and binding now.
- `transitional` — in force but under a transitional/grace regime.
- `proposed` — published draft / bill not yet enacted.
- `consultation` — open consultation, text may change.

## Confidence
`high | medium | low` — the maintainer's confidence in the classification given source clarity and
settledness of the regime. Moving targets (e.g. pending bills, open rulemakings) carry `medium`/`low`.

## Coverage states (rendered in COVERAGE.md)
- ✅ **verified** — at least one verified record for that (jurisdiction × dimension) cell.
- ✍️ **draft** — a record exists but still contains `<VERIFY` markers.
- ⬜ **planned vX.Y** — scheduled in `roadmap.yaml`, not yet drafted.

## Versioning
Semantic versioning. Each tagged release is archived to Zenodo for a citable DOI. The changelog
records what regulatory facts changed between versions (the register doubles as a regulatory-diff log).
