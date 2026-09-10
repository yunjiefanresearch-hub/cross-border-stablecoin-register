# Public evidence repair — September 2026

The 2026-08-20 data snapshot contains 152 records, 46 structural candidates and
0 decision-ready citable records. The code repair does not perform a fresh legal
source review or supply an independent second reviewer. The snapshot date stays fixed.

## Changes to validate

- Canonical CI cache configuration must be valid at workflow parse time.
- Generated research CSVs must have identical bytes on Windows and Linux.
- Register pages, MCP, Mapper and the public site must agree on strict citability.
- The metadata contract distinguishes 9 authored corridors from 132 directed corridors,
  and derives the MCP tool count from the runtime manifest (40 in this snapshot).
- Successful HTTP retrieval means a published snapshot was fetched; it does not
  establish that legal evidence is current. Incompatible responses retain the labelled snapshot.

The requested security target is tracked separately in the
[OpenSSF Gold evidence matrix](security/OPENSSF_GOLD.md). A successful repair build
does not establish Gold qualification. In particular, humans and hosted controls
cannot be replaced by generated reports or AI-authored review attestations.

Use `python -m tools.verify` with the committed development constraints. Its output
is the evidence for the checkout tested. A checked-in workflow file, a security-only
run, or an old local transcript does not prove that the current commit passes.

## Repository settings and release handoff

These are GitHub settings, not properties a source-file change can apply:

| Repository | Description | Homepage | Suggested topics |
| --- | --- | --- | --- |
| cross-border-stablecoin-register | Versioned evidence for cross-border stablecoin regulation: 12 jurisdictions, dated sources, independent-review gates and 40 MCP tools. | https://cbsr.io | stablecoin, regulation, regulatory-technology, legal-data, mcp, open-data |
| cbsr-mapper | Interactive CBSR corridor map with a dated Register snapshot, evidence filters and explicit synchronization status. | https://yunjiefanresearch-hub.github.io/cbsr-mapper/ | stablecoin, visualization, regulatory-technology, react |
| cbsr.io | CBSR public site: evidence, methods, tools and contributor entry points. | https://cbsr.io | stablecoin, research, open-data, mcp |

The Register's Dependency Graph was initially disabled. After the maintainer enabled
it, [Dependency review attempt 2](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/actions/runs/34481297481/attempts/2)
passed for the repair. Keep Dependency Graph enabled and retain this required check.
Verify the old `stablecoin-rail-register` homepage link redirects, then replace the
repository homepage with the canonical destination. Confirm homepage ownership and
availability before changing settings.

The observed v0.11.0 release has no body or attached assets. Before updating it or
publishing a successor, link a successful canonical run for the exact source commit,
state the snapshot's evidence limits, describe changes from the prior version, and
provide installation instructions. Attach the verified wheel, checksum, SBOM,
licence inventory and verification summary produced from that same commit. Do not
reuse an older success report as evidence for repaired source files.

## Claimable contribution queue

Open a task in the [issue tracker](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues)
before changing evidence. The maintainer accepts submissions; an independent second
reviewer accepts source-verification results. An issue claimant is not automatically
a qualified reviewer. Six public issues are now available with `small task` and
`help wanted` labels: [#14](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/14),
[#15](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/15),
[#16](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/16),
[#17](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/17),
[#18](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/18),
and [#19](https://github.com/yunjiefanresearch-hub/cross-border-stablecoin-register/issues/19).
The following small scopes can be claimed independently:

| Task | Deliverable | Acceptance |
| --- | --- | --- |
| Official-source check: US issuer pathway | Open the cited official source; record access date, exact provision and amendment/commencement status. | Source URL and pinpoint verified; freshness changed only for sources actually opened. |
| Official-source check: UK commencement | Reconcile cited made/commenced dates against the official instrument. | Distinguish enacted from operative law; retain uncertainties and source evidence. |
| Independent second review: one EU record | Complete one row of the second-coder worksheet without copying the first review. | Reviewer identities differ; disagreement and reconciliation trail recorded. |
| Chinese-language evidence: one CN or TW record | Supply original-language quotation locator and a concise English gloss. | Official provenance and proposition scope checked by a qualified language reviewer. |
| Clean-room reproduction | Run the canonical verifier in a fresh supported Python environment. | Include commit SHA, interpreter/OS, commands, exit status and machine-readable summary. |
| External integration report | Reproduce one MCP/API/Mapper query against a pinned snapshot. | Publish inputs, version/date, outputs and limitations; distinguish experiment from adoption. |

Stars and forks describe one public channel only. Record external reproductions,
contributions and citations with links and dates; do not invent adoption metrics.
