# Build note — v0.9.3: offline reproducibility, and the Atlas §8 stakeholder projection

*Authored 2026-06-27. Responds to a review of v0.9.2 and ships the highest-leverage feature short of the
verification pass.*

## Part 1 — the reproducibility fix (a real nit, honestly fixed)

The review caught a genuine reproducibility gap. `build.py` hard-imported `jsonschema`
(`from jsonschema import Draft202012Validator`), but the validator **shim lives outside the package by
design** — at `/home/claude/work/shim`, so it never ships — precisely so it can't be mistaken for part of
the dataset. The sandbox has no network and can't `pip install`. Net effect: an offline third party
trying to reproduce the green build had to hand-roll a validator, exactly as the reviewer did. Not a
dataset defect (`jsonschema` is a declared dependency in `requirements.txt`), but a real friction on the
question that matters — *can someone else actually run this?*

The honest fix is graceful degradation, not vendoring a copy of someone else's library:

```python
try:
    from jsonschema import Draft202012Validator as _ExtValidator
    VALIDATOR_BACKEND = "jsonschema (full Draft 2020-12)"
except Exception:
    _ExtValidator = None
    VALIDATOR_BACKEND = "builtin fallback (offline; structural subset of Draft 2020-12)"
```

When `jsonschema` is importable, the build uses it for full Draft 2020-12 validation. When it isn't, the
build falls back to a small, dependency-free `_FallbackValidator` that implements exactly the keywords
this repo's two schemas use: `type`, `required`, `enum`, `const`, `properties`, `additionalProperties`,
`items`, `allOf`, and `if/then/else` (the corridor schema's one conditional). The build now prints
**`schema validation backend: …`** so a reader knows which path ran. Verified three ways: (1) with the
shim on `PYTHONPATH`, the full backend runs and the build is green; (2) with no shim, the builtin
fallback runs and the build is **identically** green (152 records, 80/96, 9/9, worklist 57); (3) the
fallback still **catches** a bad enum (`status: not_a_real_status`) and an unexpected field
(`additionalProperties:false`). A fresh offline extract now reproduces the green build with no network and
no hand-written validator.

This is the biggest practical step toward "someone else can run this," but it is worth being clear about
what it does *not* fix: it makes the **build** reproducible offline; it does not make the **claims**
verified. That still needs the primary-source pass (Part 3).

## Part 2 — the Atlas §8 stakeholder projection (the near-zero-fact-cost multiplier)

The review correctly identified the stakeholder projection as the highest-leverage feature short of the
verification pass: it was designed in the source documents, and it costs almost no new facts because it is
a *re-projection* of facts the register already derives. v0.9.3 builds it.

**The Stakeholder Database** (`analysis/stakeholder_database.json`) is a controlled catalogue of seven
actor personas — `issuer`, `distributor` (wallet/PSP), `reserve_custodian`, `home_regulator`,
`host_regulator`, `corporate_treasury`, `token_holder`. Each persona declares: a *lens* (the question it
brings to a corridor), the C1–C8 constraints it reads on the origin and on the destination, and the
corridor archetypes (RC Regulatory · SC Stablecoin-Settlement · TC Tokenized-Asset · DC Digital-Financial)
it engages. The personas are the register's operationalization of the §8 concept; the persona list is
itself flagged as subject to confirmation against the §8 source text (the same verification discipline
applied everywhere else).

**The projection** `profile_for(stakeholder, origin, dest)` (`scripts/stakeholders.py`) takes a persona
and a directed edge and returns: the persona's lens; the corridor's **already-derived class** (from
`compose_via_substrate`); a **per-constraint reading** of the origin/dest poles the persona cares about,
where each line is the plain-language implication of a pole *and cites the record that pole rests on*; the
**archetypes engaged** (intersection of the persona's archetypes with the corridor's); the edge's
**inbound mechanism**; and a **verification caveat**. It emits 63 worked profiles — the 9 authored
corridors × 7 personas.

The discipline that makes this honest rather than a generator of plausible text:

- **No new facts.** Every line a profile shows is read from an existing record. The projection composes
  and re-reads; it never asserts anything the constraint layer didn't already contain.
- **Provenance-gated.** Every profile carries the list of `tier1_legal` records it cites, and the build
  **fails** (`stakeholder profiles: provenance not clean …`) if any profile cites a record that is
  missing or not `tier1_legal`. Verified with a negative test.
- **Preview, and it says so.** A profile inherits the verification status of the cells it reads;
  `profile_for` reports how many of the cited cells are not yet verified to `resolution_text`, so a
  profile is explicitly *not* citable authority until the underlying cells are. The projection multiplies
  the register's usefulness without multiplying its claims.

**Surfaced everywhere the other engines are:** MCP gains `stakeholder_database` and `profile_for`
(**23 → 25 tools**), and the site gains a stakeholder-lens panel — pick a corridor, see all seven
personas' projections side by side, each with its reading and its preview caveat.

## Part 3 — what is (still, honestly) left

The review's framing holds exactly. Three things still bound "maximization," in priority order:

1. **The verification backlog (57 cells).** Most substrate inputs are `firm_summary` (transcribed from the
   three documents and practitioner summaries, not confirmed against official text), so every engine
   output — `compose()`, the substrate, and now the stakeholder profiles — is **preview, not citable
   authority**. Only a networked, primary-source pass clears this, and the build environment can't do it.
   This is the real wall between an impressive computable preview and citable regulatory infrastructure.
2. **The rich corridor-edge records (9 of 132).** The edge layer is now *computed-complete but
   rich-record-sparse*: 124/132 directed classes are derivable, but only 9 corridors carry the full Atlas
   model (`inbound_mechanism`, `administrator`, `archetypes`, `infrastructure_overlap`). Authoring the
   other 123 as first-class records is the next within-corpus build.
3. **§8 confirmation.** The stakeholder personas and their constraint mappings are the register's reading
   of §8 and should be checked against the source text — low fact cost, but not zero.

v0.9.3 closed the reproducibility gap and shipped the §8 projection. The substrate's coverage is still the
inverse of the verification backlog; the projection re-reads that coverage for each actor without adding
to the claim surface.
