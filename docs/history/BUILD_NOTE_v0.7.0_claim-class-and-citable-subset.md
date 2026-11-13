# Build Note — v0.7.0: A second evidence axis, and the lawyer-citable subset

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** promote the Corridor Atlas §7
legal-vs-operational distinction into the schema as a required `claim_class` field; define, expose, and
**enforce** the lawyer-citable subset; make the computed layer rest only on propositions of law.

Through v0.6.0 a record's `evidence_tier` told you *how well-sourced* it was — confirmed against the
official text (`resolution_text`), partly (`mixed`), or practitioner-corroborated (`firm_summary`). But
nothing in the schema told you *what kind of claim* the record made. "Switzerland imposes no C7 usage
cap" (a proposition of law) and "JPYC launched on 27 October 2025" (a market fact) were both just
records, and a confident `resolution_text` tag on the second could be misread as making it *citable
law*. It is not — it is a true, well-sourced fact about the market. v0.7.0 adds the missing axis.

This was sequenced **first** among the three candidate features not because it demos best (the
date-aware engine does) or because it is the deepest idea (the constraint substrate is), but because it
is the one the other two **structurally depend on**: a date-aware `compose(origin, dest, as_of)` and a
constraint-level feasibility engine both have to distinguish a legal fact from an operational one, or
they produce dangerous answers. Its payoff — citable-subset integrity — is also the highest-value
deliverable for the core legal/supervisory audience, and it is fully achievable in one pass without the
shallowness risk that rushing the other two would carry.

---

## 1. The diagnosis

`evidence_tier` is a **provenance** axis (how well do we know it). The thing it was being asked to
also carry — *is this a statement of law or a statement about the market* — is a different, orthogonal
question. The Corridor Atlas §7 already draws exactly this line: **Tier-1** primary-source legal
constraints versus **Tier-2** market-reported operability, and it warns the two must not be read at the
same confidence. The register had collapsed that distinction into prose and the choice of dimension.

The cost was latent but real: there was no honest way to answer the single most valuable question a
lawyer or supervisor asks — *"show me only what I could actually cite as binding law"* — because the
data did not record which claims were law in the first place.

---

## 2. The axis: `claim_class` (orthogonal, required, per-record)

A new **required** field, enum `tier1_legal | tier2_operational`:

- **`tier1_legal`** — a proposition of law: what a binding instrument (statute, regulation, official
  guidance) requires, permits, or prohibits. Citable to the instrument.
- **`tier2_operational`** — a market/operational fact: what is live, who is registered, what launched,
  what rails or liquidity exist. Read as-of-dated.

Three properties make it load-bearing rather than cosmetic:

1. **Orthogonal to the other two axes.** It composes with `status` (in force vs draft) and
   `evidence_tier` (provenance) without collision. A draft statute is `tier1_legal` + `proposed`; a
   confirmed launch is `tier2_operational` + `resolution_text`. The value strings share nothing with
   the `evidence_tier` strings, so the two can never be confused in a filter.
2. **Per-record, not derived.** In today's data the mapping is clean — the `implementation_status`
   dimension is operational, the other fourteen state propositions of law — but the field is stored on
   each record, not inferred from the dimension at read time. That is what lets a future operational
   claim inside a nominally-legal dimension (say, a `monetary_sovereignty` record whose load-bearing
   fact is a market datum) be tagged `tier2_operational` explicitly, instead of silently inheriting
   "legal" from its dimension.
3. **Audited, not assumed.** Every record flagged by a market/media-source heuristic was read by hand:
   `tw-frs-aml_kyc`, `tw-frs-regulatory_authority`, `cn-prc-capital_requirements`,
   `us-pss-securities_classification` all state propositions of law and merely *cite* an announcement
   as corroboration — so all stay `tier1_legal`. No current record is a legal-dimension exception; the
   capability to express one is what matters.

The retag (`scripts/retag_claim_class_v0_7_0.py`) is an idempotent textual YAML edit that preserves the
hand-authored formatting and block scalars, inserts `claim_class` after `confidence`, and appends a
`v0.7.0_claim_class` tag. Result: **108 `tier1_legal` + 9 `tier2_operational` = 117**. Corridors carry
no `claim_class`.

---

## 3. The lawyer-citable subset

The subset a lawyer or supervisor can cite as **current binding law** is the intersection of all three
axes:

```
claim_class == tier1_legal   AND   status == in_force   AND   evidence_tier == resolution_text
```

= **21 records** today. Each is projected to what a citation needs — instrument (`source.primary`),
`pinpoint`, official `url`, `last_reviewed` — and published three ways:

- **`citable_subset` in `dataset.json`** (filter definition + count + projected rows), so consumers
  never re-derive it;
- the **`citable_law(jurisdiction?, dimension?)` MCP tool** (tool count 17 → 18) — the "show me only
  what I could cite" view, with optional filters;
- the **"citable law only" toggle** on the static site, alongside a `claim_class` column and filter,
  citable-`§` markers on the matrix, and claim/tier badges + the official-URL link in the inspector.

The reconciliation is worth stating because it is the whole point. Of the 23 `resolution_text` records,
**21 are `tier1_legal`** (citable) and **2 are `tier2_operational`** (e.g. a confirmed product launch).
Those 2 are *deliberately excluded* from citable law despite being perfectly well-sourced — because
they are facts about the market, not propositions of law. That exclusion is the axis doing its job.

Worked examples: `citable_law('CH')` → **6** (Switzerland is a live, well-verified regime);
`citable_law('TW')` → **1** (only the in-force AML layer; the draft Virtual Asset Service Act is
excluded by `status`, exactly as a lawyer would want).

---

## 4. Enforcement (so the subset cannot drift)

A subset that is only a filter over self-reported tags is not trustworthy. Two build-time gates make it
real:

1. **Citable integrity** (`check_citable_integrity()` in `build.py`): a `tier1_legal` record at
   `resolution_text` or `mixed` *asserts* confirmation against the official text, so it **must** carry a
   `source.url`; at `resolution_text` it **must** also carry a `source.pinpoint`. A citable record
   cannot ship without a locator to the official instrument. *Negative test:* stripping the URL from a
   citable record fails the build with a precise message; restored cleanly.
2. **Signal-provenance discipline** (`check_signal_provenance()` in `scripts/compose.py`, enforced by
   `build.py`): every per-jurisdiction signal the `compose()` engine reads must rest on `tier1_legal`
   records. A signal resting on a `tier2_operational` fact is a build-failing violation. *Negative
   test:* flipping a signal-driving record (`ch-frs-issuer_pathway-001`) to `tier2_operational` makes
   `compose()` report the violation and fails the build; restored cleanly.

Gate (2) is the **inheritance hook**. The computed layer now derives feasibility only from propositions
of law — which is precisely the invariant the v0.8.0 time/event engine and the v0.9.0 constraint
substrate need, stated and enforced one version early so they inherit it for free.

---

## 5. Honesty surfaces

`COVERAGE.md` gains the two-axis count matrix (`claim_class` × `evidence_tier`) and a "citable cells"
block. The MCP record summary now carries `claim_class` and `evidence_tier`; `about()` reports the
evidence model and the citable count. The methodology, taxonomy, the site's methodology card, the "for
agents" note, and the roadmap are all updated for the two-axis model. None of this generates or infers
a citation — `claim_class` records *what kind* of thing a source establishes; the citation firewall is
unchanged.

---

## 6. What is still open (declared, not hidden)

- **47 of the 51 `unset` legacy records are `tier1_legal`.** They are excluded from the citable subset
  only by `evidence_tier` (they predate the field), not by kind — so the next verification pass would
  expand the citable subset directly. This is the v0.9.0 backlog item.
- **No legal-dimension operational exceptions exist yet.** The per-record design anticipates them; none
  is present in the current data.
- **The citable filter is deliberately strict** (`resolution_text` only). A looser "citable with a
  caveat" view (including `mixed`) is intentionally *not* shipped — a lawyer-citable claim should rest
  on the official text, full stop.

---

## 7. Validation

- `build.py`: **117 records valid, 9 corridors, 66 compatibility pairs**; computed layer reproduces
  **9/9** corridors and **64/66** §5.14 categories; **2 findings** under `uk_regime_in_transition`;
  pre-regime cross-check `{KR, TW}` consistent; **signal provenance clean**.
- `claim_class`: **108 `tier1_legal` + 9 `tier2_operational`**; matrix reconciles with the
  evidence-tier totals (`resolution_text` 21 legal + 2 operational = 23; `mixed` 11 + 3 = 14;
  `firm_summary` 29 + 0 = 29; `unset` 47 + 4 = 51).
- **Citable subset = 21**; `citable_law('CH')` = 6, `citable_law('TW')` = 1.
- Both negative tests pass (citable-URL strip; signal-provenance flip), both restored.
- Static site regenerated at v0.7.0; embedded data carries `claim_class`; app JS passes `node --check`.
- Local validation uses a faithful Draft 2020-12 shim (no network in the sandbox); CI uses the real
  `jsonschema` (`requirements.txt`), and the shim is kept outside the package so it never ships.
