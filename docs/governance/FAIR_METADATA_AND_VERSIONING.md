# FAIR metadata and versioning note

CBSR supports findability and interoperability through stable record IDs, schema IDs, `CITATION.cff`, versioned JSON schemas, machine-readable manifests and explicit licences. Accessibility is supported by open formats and source URLs, but source availability and language remain uneven. Reuse is bounded by provenance, freshness, review and non-legal-advice fields.

Versions follow semantic release identifiers for software and immutable dataset snapshots for citation. Every derived artifact records or inherits the dataset version. Unknown schemas must fail closed. A migration must preserve record IDs, review history and supersession links; rollback restores a complete immutable artifact rather than mixing generated files across versions.

This note is a repository design statement, not a FAIR certification or measured FAIR maturity score.
