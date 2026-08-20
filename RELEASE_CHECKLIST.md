# v0.11 release checklist

## Automated gates

- [x] `python -m tools.verify` (local Linux Python 3.12 release run)
- [x] Local Linux Python 3.10, 3.11, 3.12 and 3.13 canonical verifier runs
- [ ] GitHub Actions Python 3.10, 3.11, 3.12 and 3.13 jobs green
- [ ] Windows 11 clean-room job or physical-host transcript green
- [x] Wheel installed and six MCP capabilities invoked from an empty repository-external directory
- [x] Two wheel builds byte-identical across the local Python matrix
- [x] CycloneDX SBOM generated
- [x] Vulnerability and licence scans generated; zero known vulnerabilities in the resolved runtime
- [x] Source ZIP checksum generated and independently verified; retain the `.zip.sha256` sidecar

## Evidence gates

- [ ] All 152 records opened against official sources
- [ ] Enactment, commencement and proposal overlays mapped separately
- [ ] Freshness date changed only after an actual source read
- [ ] Independent second reviewer and disagreement log complete
- [ ] Taiwan, US, UK and HK research leads mapped to exact record pinpoints

## Repository and external gates

- [ ] Branch protection/ruleset verified on GitHub
- [ ] CODEOWNERS test review completed
- [ ] Draft PR reviewed; no direct merge
- [ ] No release, tag, PyPI, DOI or DPGA action until all applicable gates are approved
