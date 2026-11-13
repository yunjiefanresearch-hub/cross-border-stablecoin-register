# Versions: the collapse of three numbers into one

Before v0.10.0, three different numbers described one object, and the corridor audit's own
`docs/VERSIONS.md` flagged the confusion as something that needed to "collapse":

| Number | What carried it | Value before |
|---|---|---|
| register version | `build.py:REGISTER_VERSION`, `dataset.json`, `CITATION.cff`, `README.md`, `PACKAGE.md`, the verification ledger, both papers | `0.9.91` |
| `register_version` in the corridor artifact | `computed_corridors_directed.json` meta — *"the register release this corridor layer is cut from"* | `0.9.9` |
| `artifact_revision` | the same file — the corridor audit repository's own revision of the artifact | `0.10.0` |

They were never a version *chain*. `v0.10.0` of the audit repository was a downstream revision of a
corridor layer cut from register `v0.9.9`, published while the register itself stood at `v0.9.91`.
Reading "v0.10.0 > v0.9.91" as "newer, therefore replaces" was the natural misreading, and the wrong
one: the audit package shipped 52 files, no node records, no `api/`, no papers, no MCP server. It was
a patch and a set of findings, not a register.

## After v0.10.0

There is **one** number. The register is `0.10.0`. The corridor artifact's `register_version` is
`0.10.0` because it is built from this register by `scripts/build_corridors_directed.py`, in this
repository, on every build. `artifact_revision` is retained at `0.10.0` as the shape identifier that
`tools/migrate_from_v0_9_92.py --check` asserts, and it is now, by construction, the same release.

Agreement is enforced, not maintained by vigilance:

- `V1` — `build.py:REGISTER_VERSION == EXPECT_VERSION`
- `V2` — `dataset.json.register_version == EXPECT_VERSION`
- `V3` — `CITATION.cff` (machine-authoritative for Zenodo), `README.md`, `PACKAGE.md`, the
  verification ledger, and the register version cited by **both papers** all agree
- `L1` — the verification ledger's schema and version
- a negative test rolls `CITATION.cff` out of sync and confirms the build fails

## What keeps its own version

The companion works are different works, not different names for this one, and they keep their own
numbers:

- *Multi-Jurisdiction Stablecoin Compliance Matrix* — v0.9.7
- *Cross-Border Stablecoin Architecture* — v0.2.8
- *Cross-Border Digital-Finance Corridor Atlas* — v0.2.5 (the class rule this register applies is
  the Atlas's §3.4/§4.1 destination-first precedence)
- *Citable by Construction* and *Cross-Border Stablecoin Feasibility Over Time* — v0.1.0 (both cite
  the register as CBSR v0.10.0)

## Citing

Available Zenodo records are listed under the [concept DOI](https://doi.org/10.5281/zenodo.20730358),
which resolves to the latest archived version. Cite a **version DOI** when a claim
depends on a specific state of the data.

- [v0.11.0 data snapshot (20 August 2026)](https://doi.org/10.5281/zenodo.22021736)
- [v0.11.0.post1 engineering update (24 September 2026)](https://doi.org/10.5281/zenodo.22941250)
