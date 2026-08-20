# Archival and persistent-identifier plan

No DOI, archive deposit or Software Heritage snapshot is created by this repository build.

1. Freeze a verified source revision and record its Git SHA, dataset version and canonical verifier summary.
2. Create the signed release only after all release hard gates close; attach ZIP, wheel, SBOM, licence inventory, provenance and SHA256SUMS.
3. Request a Software Heritage save for the public repository and retain the resulting SWHID after readback.
4. Deposit the same immutable artifacts with an authorized archival service and reserve/mint a DOI only with maintainer approval.
5. Update `CITATION.cff` and release metadata with the actual DOI/SWHID; never insert placeholders presented as issued identifiers.
6. Test that the archive resolves and that checksums match before announcing persistence.

Historic identifiers are immutable. Corrections create a new version and link supersession; they never overwrite the archived object.
