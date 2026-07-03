# GOVERNANCE

**Cross-Border Stablecoin Register (CBSR)**
Maintainer: Yunjie Fan, independent research on cross-jurisdictional digital-asset regulation
Status: v0.1.0 · June 2026 · governs the register and its derived layers
Companion documents: [`CHARTER.md`](CHARTER.md) · [`DISCLOSURE.md`](DISCLOSURE.md) · [`METHODOLOGY.md`](METHODOLOGY.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md)

---

## 0. What this document governs

[`CHARTER.md`](CHARTER.md) states *what the project commits to and refuses*. This document states *how
the project is run* so that those commitments hold in practice: who decides what, where the open–closed
boundary falls and why, how a record moves from a proposal to verified coverage, how the verified status
of the data is governed, how releases are cut and cited, how the derived layers are kept honest, and how
the firewall that protects the project's independence is maintained as a matter of structure rather than
of good intentions. [`DISCLOSURE.md`](DISCLOSURE.md) states the independence, conflict-of-interest, and
limitations policy as a standing disclosure; this document is its structural counterpart.

The register is two things that this governance binds together: the *node data* (one verified
`(jurisdiction × instrument × dimension)` fact per record) and the *derived layers* built on top of it
(the corridor edges, the computed feasibility layer, the time engine, the constraint substrate, the
stakeholder projection, and the agent-queryable interface). The descriptive working papers carry their
own scholarly disclosures and are the *analysis*; the register is the *data substrate*; this governance
applies to the register and its derived layers.

---

## 1. Roles and decision rights

**Maintainer.** The project has a single accountable maintainer, who is responsible for the integrity of
the data, the verification standard, the release cadence, and the enforcement of the charter. The
maintainer holds final decision rights over what is merged and what a release contains, exercised within
the constraints this governance imposes (a maintainer cannot, for example, merge a record that fails the
build, because continuous integration will not permit it).

**Contributors.** Anyone may propose a record or a correction. Contributions are made as
schema-validated additions or amendments under the rule in [`METHODOLOGY.md`](METHODOLOGY.md) and the
process in [`CONTRIBUTING.md`](CONTRIBUTING.md). A contributor proposing a record asserts that they have
cited a primary source with a pinpoint and verified it themselves; the maintainer reviews, and the build
enforces the structural conditions independently of either party's assertion.

**Continuous integration.** The build, the structural invariants, and the negative-test suite are a
non-discretionary participant in every decision: they run on every change and every pull request, and a
change that fails any of them cannot be merged regardless of who proposes it. This is deliberate: it
moves the most important guarantees out of the realm of reviewer attention and into the realm of
mechanism.

---

## 2. The open–closed boundary

The defining governance question for an open research commons is where the boundary falls between what is
open and what is reserved, and *why*. The register's boundary is stated here in full, because it is the
structure that lets the project be maximally useful without compromising what makes it trustworthy.

### 2.1 What is open, and under which licence

- **The data is open under CC-BY-4.0.** All records, the corridor file(s), the compiled dataset, and the
  generated coverage and records tables are licensed Creative Commons Attribution 4.0 International.
  Anyone is free to share and to adapt the material for any purpose, *including commercially*, under the
  single condition of attribution (with a link to the licence and an indication of changes), and with the
  standing limitation that attribution may not suggest the project endorses the user or the use.
- **The code is open under Apache-2.0.** The build tooling, the schemas, and the analysis scripts are
  licensed Apache 2.0, a permissive licence that grants use while retaining a patent grant, so that the
  tooling can be built on without exposing contributors or users to patent action.
- **The methodology, taxonomy, and schemas are deliberately open.** These are *standards meant to be
  built on*: the evidence model, the controlled vocabulary, and the record, corridor, and analysis
  schemas are published precisely so that others can adopt them, extend them, and produce interoperable
  references. The project's interest is in the discipline being adopted, not in withholding it.

### 2.2 What "open" does not mean

Open licensing does *not* dissolve the project's quality boundary. Two things are governed tiers, not
casual states:

- **Verification status gates what may be cited as law.** "Open" never means "unverified passes as
  verified." The citable subset (the records a lawyer may cite as current binding law) is a strict,
  enforced intersection of the three evidence axes; a record outside it is openly available but is not,
  and is not represented as, citable current law. The data is free to reuse; the *status* of a claim is
  not negotiable by a reuser.
- **The computed layer is a preview, not an authority.** The derived conclusions are open data, but they
  are labelled previews; reusing them does not convert them into asserted truth, and the project does not
  warrant a computed conclusion where it diverges from the authored analysis (the divergence is published
  as a finding).

### 2.3 The firewall: data flows out, interests do not flow in

The most important property of the boundary is its *direction*. The open data flows *outward* without
restriction: anyone may take it, including for commercial purposes. Commercial and other interests do
*not* flow *inward*: there are no sponsored records, no paid placement, no pay-to-verify, and no
arrangement under which a party's financial interest could shape what the register says or which cells
are verified first. The boundary is therefore one-directional by design.

Stated structurally, the register is the *open infrastructure*; any product, service, or commercial
analysis built on it is a *separate, downstream layer* that consumes the open data without contaminating
it. A downstream user is free to build a closed product on the open register; the register's records and
verification are unaffected by that product's existence, because nothing about the product flows back
into the data. This is the structural form of the charter's commitment that independence is not for sale,
and it is what lets the project license its data for commercial reuse (maximizing the data's usefulness)
without any commercial relationship reaching the data's integrity. The standing-disclosure form of the
same firewall is in [`DISCLOSURE.md`](DISCLOSURE.md).

---

## 3. Contribution governance

A record is proposed, not merely added, and the path from proposal to verified coverage is the same for
the maintainer and for any contributor.

1. **Authoring.** A record is a copy of the record template with every field filled, citing a *primary*
   source with a pinpoint, self-verified by the author. Drafts that still carry verification markers are
   welcome but are merged as *drafts*, not as verified coverage.
2. **Validation.** The build validates the record against the published schema; a record that does not
   validate cannot be merged.
3. **Review and merge.** The maintainer reviews for substance and sourcing; continuous integration runs
   the full suite (schema validation, structural invariants, the negative tests, and the cross-layer
   integrity checks) on the pull request. A change that breaks any gate cannot be merged.
4. **Status.** A merged record carries its three evidence axes and its status; a draft is visibly a
   draft, a verified record is visibly verified, and the difference is in the data, not in prose.

The gates are not advisory. The structural invariants are read-only assertions over the built register
that must all hold, and the negative-test suite deliberately breaks each validation gate on a throwaway
copy to prove the gate *bites* (and then reverts); both run in continuous integration. A contributor
cannot bypass a gate, and neither can the maintainer.

---

## 4. Verification governance

The verified status of the data is the project's central asset, and it is governed explicitly.

- **Tiers are earned, not asserted.** The build enforces the necessary provenance for each evidence tier:
  a record confirmed against the official text must carry a locator, a pinpoint, and a review date; a
  partly-confirmed record must carry a locator and a pinpoint; a practitioner-corroborated record must
  carry a pinpoint. A record cannot claim a tier it lacks the provenance for.
- **Binding status caps citability.** Locating an instrument's official text is not sufficient to make a
  claim citable as current law; the instrument must be enacted and in force. The build refuses to treat a
  made-but-not-commenced, finalized-policy-pending, or pending-proposal instrument as current binding law,
  even where its text has been read. This is what keeps the citable subset honest after verification.
- **External verification is never fabricated.** A promotion to the highest provenance tier requires
  reading the official instrument; it is done by hand and recorded in an audit ledger (for each verified
  cell: the instrument, the binding status, the official locator, the pinpoint, the verdict, and the tier
  applied), and the build cross-checks every record against the ledger to catch drift. Where verification
  has confirmed a regime only at the level of its status, or has not yet reached an original-language
  official-text line-read, the record is held below the highest tier and the gap is declared, not papered
  over.
- **The residual is governed, not hidden.** The backlog of not-yet-verified records is tracked in a
  per-cell worklist (the instrument, the pinpoint, and exactly what is missing for each) and a
  verification queue. It is published as queryable data, and the standing acknowledgment (that the gates
  are defenses and only a primary-source pass retires the liability) is repeated wherever the coverage
  counts appear. A record leaves the backlog only by acquiring the provenance the build requires, and the
  move is recorded.

---

## 5. Release governance

- **Versioning and cadence.** Releases are versioned; the cadence is quarterly diffs plus event patches
  (a patch when a tracked change in law commences or a verification pass lands). The changelog records
  what changed in each release and why.
- **Citable stability.** Each tagged release is archived for a persistent identifier, and a citation
  resolves to a specific version. The canonical name and the legacy repository slug are retained
  deliberately: the slug, the archival identifier, and the published schema identifier are kept stable so
  that inbound references and the schema identity do not break, even though the project is *named* to a
  reader by its canonical name everywhere a name (rather than a stable identifier) appears.
- **The meaning of "verified" in coverage.** A coverage cell marked verified denotes a sourced,
  schema-valid record with no outstanding verification marker and a human-passed pinpoint; it does *not*,
  by itself, denote that the pinpoint has been checked against the official gazette. Provenance is tracked
  separately by the evidence tier, and the coverage view publishes the evidence-tier breakdown so that a
  reader checks the breakdown before relying on any cell as primary authority. The two-axis count matrix
  (claim-kind against provenance) and the citable-cell count are published with every release.

---

## 6. Derived-layer governance

The layers built on the node data are kept honest by the same discipline that governs the data.

- **Cross-layer integrity is enforced.** A corridor edge that points to a pairwise-compatibility row must
  carry a category that matches that row; if its directed interaction sets differ from the undirected
  pair's, it must carry an explicit divergence field explaining why. The build fails otherwise, so a
  derived edge cannot silently contradict the analysis it points to.
- **Derivation rests only on law.** Every signal the composition engine reads must rest on a proposition
  of law; a signal resting on a market fact fails the build. The same invariant governs the time engine
  (every calendar event is a change in law, never a market launch) and the constraint substrate (every
  pole cites the legal record it is transcribed from, and a pole backed by a market record is rejected).
- **Derived artifacts cannot be merged stale.** Continuous integration rebuilds the derived layers and
  fails if a committed artifact is out of date with the data it is derived from, so the published derived
  layer always corresponds to the current records.
- **Indeterminacy is reported, not guessed.** Where a load-bearing input to a derivation is missing, the
  engine returns an explicit indeterminate result naming what is missing, rather than guessing; coverage
  of the derived layers therefore reports its own backlog honestly.

---

## 7. Amendment and continuity

- **Amendment.** This governance is versioned and changes only deliberately, by an explicit revision
  recorded in the changelog with its rationale. Where a governance rule is enforced by the build,
  weakening the rule requires weakening the mechanism, which is a visible, reviewable change.
- **Continuity.** The project's protocols (the verification rule, the gate definitions, the release
  process, the schemas, and the audit ledger) are documented precisely so that the register survives a
  change of maintainer. The guarantees that matter most are encoded in the build and the schemas rather
  than held only in the maintainer's practice, so that a successor inherits the discipline as mechanism,
  not as memory. Contributions are welcomed under the same documented rule, which is the project's hedge
  against single-maintainer fragility.

---

## 8. Relationship to the companion working papers

The descriptive working papers (the Compliance Matrix, the Architecture working paper, the Corridor
Atlas, and the forward-feasibility and methodology papers in this portfolio) are the *analysis*. The
register is the *data substrate* the analysis rests on, and the derived layers expose the analysis as
queryable data alongside the node facts. This governance binds the register and its derived layers; the
working papers carry their own scholarly disclosures, and the independence policy that applies across the
whole portfolio is stated in [`DISCLOSURE.md`](DISCLOSURE.md). Where a paper states a conclusion and the
register carries the data and the derivation behind it, the register is the citable substrate and the
paper is the argument; the governance ensures the substrate is what it claims to be.

---

*Maintainer:* **Yunjie Fan** · ORCID 0009-0005-6762-084X · SSRN Author ID 11463068
*This governance applies to CBSR v0.9.8 and forward, from governance v0.1.0 (June 2026).*
