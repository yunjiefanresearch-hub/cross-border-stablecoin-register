# CHARTER

**Cross-Border Stablecoin Register (CBSR)**
Maintainer: Yunjie Fan, independent research on cross-jurisdictional digital-asset regulation
Status: v0.1.0 · June 2026 · governs the register and its derived layers
Companion documents: [`GOVERNANCE.md`](GOVERNANCE.md) · [`DISCLOSURE.md`](DISCLOSURE.md) · [`METHODOLOGY.md`](METHODOLOGY.md)

---

## Why this charter exists

The register is a living, versioned, machine-readable reference of how jurisdictions regulate
stablecoins. A living reference is under continuous pressure: to expand its coverage, to stay current
with fast-moving law, to be maximally useful to the people and the software that consume it. Those
pressures are healthy, but each of them, pursued without discipline, would erode one of the properties
that make the register trustworthy in the first place: that it does not over-claim, that it does not
predict, that it does not let breadth outrun verification, and that its independence is not for sale.

This charter states, in one place, the commitments the project keeps so that the pressures of growth
never quietly compromise the things that make the work worth citing. The commitments are not
aspirations; most are enforced by the build and the governance described in the companion documents,
and where a commitment is enforced, this charter points to the mechanism. The charter is itself
versioned: it does not change silently, and any change is recorded in the changelog with its rationale
(see *Amendment*, below).

The commitments are written for a reference whose primary reader is increasingly software (retrieval
pipelines, language-model agents, automated compliance tools) that will treat whatever the register
asserts as fact. That is the setting in which discipline matters most, because a machine does not read
a caveat.

---

## The commitments

### 1. No claim beyond its evidence

The register never presents a market fact as law, a draft provision as binding, or an unverified
transcription as confirmed. Every record carries three orthogonal axes: the *kind* of claim
(`claim_class`: a proposition of law versus a market/operational fact), its *provenance strength*
(`evidence_tier`: confirmed against the official text, partly, or practitioner-corroborated), and the
*binding status* of the instrument it rests on (`binding_status`: enacted-and-in-force,
made-not-commenced, finalized-policy-pending, a pending proposal, a prohibition, or no regime). A claim
is shown for exactly what it is on each axis, and the subset a lawyer may cite as current binding law is
the strict intersection of the three. *Enforced:* the build refuses a record that asserts official-text
confirmation without a locator to that text, and refuses to treat a located-but-not-commenced instrument
as current law.

### 2. No fabricated citations

No tool, and no language model used to assist authoring, generates or infers a citation. Every
pinpoint is verified by a human against the primary instrument. The register's structure records *what
kind of thing a source establishes* and *how well it is known*; it never manufactures the source. This
discipline grows more important, not less, as drafting is assisted by models that will produce a fluent
and plausible citation that does not exist if they are permitted to. *Enforced:* a record cannot reach
the citable subset without a human-verified locator to the official instrument, and that locator may
carry only the legal instrument, never a product launch, an admission, or a named commercial
counterparty.

### 3. No prediction

The register conditions; it does not forecast. Where the analysis touches a development not yet resolved
(a bill not yet enacted, a regime adopted but not yet operative, an instrument whose operative
methodology is not yet finalized), it states what *would* change *if* the development occurs, and
preserves a conditional-status flag at that point. It does not assert which bills will pass, when
contingent enactments will occur, or how an open question will resolve. A change in law is the only
thing allowed to move a feasibility conclusion, and a contingent change is surfaced as an "if enacted"
branch that is never applied by date. *Enforced:* the time engine applies scheduled changes only by
their gazetted dates and never applies a contingent change by any date.

### 4. Depth before breadth

The project does not expand the jurisdiction set or the dimension set faster than it can verify it.
Coverage that outruns verification is *declared as backlog*, not hidden behind a coverage figure: a
record transcribed but not yet confirmed against the official text is marked as such, appears in the
verification queue, and is excluded from the citable subset until it is confirmed. A hundredth
jurisdiction claimed without verification is worth less, for a reference consumed by software, than a
covered jurisdiction verified and citable. *Enforced:* an evidence tier is earned, not asserted (the
build enforces the necessary provenance for each tier), and the per-cell worklist records exactly what
is missing for every unverified record.

### 5. The computed layer is a preview, never an authority

Where the register *derives* a conclusion, composing a cross-border feasibility from two jurisdictions'
positions through a rule engine, the derived conclusion ships as a labelled preview, not as asserted
truth. The rule engine is a check on the hand-authored analysis and a way to surface drift, not a
replacement oracle. A disagreement between the computed and the authored layer is surfaced as a
*finding*, not silently overwritten in favour of either side, because the disagreement is exactly the
research-valuable signal the reconciliation exists to expose. *Enforced:* the computed layer is derived
only from propositions of law (a signal resting on a market fact fails the build), and cross-layer
integrity is checked on every build so that a derived artifact cannot be merged stale or in
contradiction with the facts it should follow from.

### 6. Independence is not for sale

The project takes no compensation (direct, contingent, or otherwise) tied to the regulatory matters it
analyzes, and enters no advisory, consulting, employment, or other compensated relationship with any
party having a financial interest in those matters. The register's data is openly licensed and may be
reused, including commercially; but any such commercial use is *downstream and at arm's length*, and it
never flows back into the data or the analysis. There are no sponsored records, no pay-to-verify, and no
arrangement under which a party's interest could shape what the register says. This is the firewall that
protects the register's evidentiary value, and it is the single commitment on which all the others
depend: a reference whose independence could be purchased could not be trusted on any of the rest. The
firewall is stated as a standing policy in [`DISCLOSURE.md`](DISCLOSURE.md) and as a structural boundary
in [`GOVERNANCE.md`](GOVERNANCE.md).

### 7. No endorsement, in either direction

The register's data is licensed for reuse with attribution, but attribution may never be presented in a
way that suggests the project endorses a user or a use. Equally, the project itself endorses no product,
issuer, jurisdiction, or outcome. The register is a reference; it is cited, not allied with.

### 8. No advocacy in the reference layer

The reference layer (the records, the schemas, and the descriptive working papers) describes the
constraint structure of the law as it is in force and pending. It does not argue for or against any
regulatory outcome. Where the maintainer holds and expresses a policy position, that position lives in
separately-labelled advocacy work and is identified as such; it never enters the register or the
descriptive papers. A reader of the register learns what the law requires, permits, and prohibits, and
what would change under a pending development, not what the maintainer thinks the law should be.

### 9. Honest residuals are published, not buried

The backlog of not-yet-verified records, the known modelling differences between the computed and the
authored layers, the dependence of every derived conclusion on the hand-curated signal table beneath it,
and the open questions whose resolution would change a conclusion are all first-class, queryable, and
declared. The project states plainly, wherever its headline counts appear, that its enforcement gates
are *defenses against misuse, not a cure for ignorance*: only a primary-source verification pass
confirms a claim, and the gates do not retire that liability. The boundary of what the register has
verified is part of the published record, not a thing to be discovered by a careful reader.

### 10. Stable identifiers and reproducible builds

The project commits to citable stability and reproducibility. Each tagged release is archived for a
persistent identifier, and a citation resolves to a specific version; the canonical name and the legacy
repository slug are retained deliberately so that inbound references, the archival identifier, and the
published schema identifier stay stable rather than breaking for cosmetic gain. Every record validates
against a published schema; the validation, the structural invariants, and the negative tests that prove
the gates bite run in continuous integration on every change, so that an invalid record, a stale derived
artifact, or a broken gate cannot be merged.

---

## What this charter is not

This charter governs the *discipline* of the register. It is not legal advice and creates no
relationship with any reader; that boundary is stated in [`DISCLOSURE.md`](DISCLOSURE.md). It is not the
operational manual for how records are proposed, verified, and released; that is
[`GOVERNANCE.md`](GOVERNANCE.md). And it is not the sourcing-and-verification rule itself, which is
[`METHODOLOGY.md`](METHODOLOGY.md). It is the statement of what the project commits to and refuses, as a
matter of research integrity, so that the reasons behind the mechanisms in those documents are explicit.

## Amendment

This charter is versioned and changes only deliberately. A change to any commitment is made by an
explicit revision, recorded in the changelog with its rationale, and reflected in the charter's version
line. The charter does not change silently, and a reader can compare any two versions to see precisely
what changed and why. Where a commitment is enforced by the build or the governance, weakening the
commitment requires weakening the mechanism, which is itself a visible, reviewable change.

---

*Maintainer & signatory:* **Yunjie Fan** · ORCID 0009-0005-6762-084X · SSRN Author ID 11463068
*This charter governs CBSR v0.9.8 and forward, from charter v0.1.0 (June 2026).*
