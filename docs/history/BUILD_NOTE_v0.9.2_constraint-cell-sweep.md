# Build note — v0.9.2, the constraint-cell sweep (the substrate, lit up)

*Authored 2026-06-27. Companion to the v0.9.0 (substrate) and v0.9.1 (verification harness) notes.*

## Why this was the highest-value keyboard move

At the v0.9.1 checkpoint the only substantive task left was the **external verification pass** — and that
needs live access to primary legal sources this build environment does not have. Faking it (inventing
`resolution_text` cites, URLs, pinpoints) would be worse than useless: it would launder unverified claims
into the citable tier and destroy the firewall the whole register is built around. So that stays undone,
honestly, on the roadmap.

What *could* be done well from the corpus alone was the thing blocking the substrate from paying off.
v0.9.0 shipped the constraint substrate, but it could derive only **1 of 9** authored corridors, because:

- the substrate's **coverage is poles** in `constraint_substrate.json`, a layer distinct from the records;
- most `(jurisdiction × constraint)` cells had **no record at all** (35 of 96 were empty); and
- most poles were therefore unset, so `compose_via_substrate` correctly returned `indeterminate`.

Authoring the missing cells is exactly the kind of work the corpus *does* support — they are propositions
of law, transcribable from the three source documents — and it is what turns the substrate from a
scaffold into something that derives real corridors. So: author the 35 missing cells, author the poles
they unlock, re-derive, and report the new coverage honestly.

## What was authored

**35 records — every C1–C8 cell for all twelve jurisdictions now has a backing record.** The gap matrix
at the start: C5 ×11, C4 ×8, C8 ×7, C7 ×3 (US, UK, SG), C1 ×2 (US, EU), C3 ×2 (CN, BR), C6 ×2 (US, EU).
The high-value ones were the **C1** issuer-eligibility cells for the US (GENIUS Act permitted issuers) and
EU (MiCA Art. 48–49) — both previously unrecorded — and the **C7** monetary-sovereignty cells, because C1
and C7 are the load-bearing poles for the directed-edge derivation.

**Tiering is honest, not inflated.** Each record carries `evidence_tier` only where earned:

- **25 cells `firm_summary`** — established regimes, with instrument + pinpoint, pending the official-text
  check (e.g. US/EU/UK/SG/HK/AE/JP payment-instrument and routing cells, US comparability, EU passporting).
- **10 cells `unset`** — the genuinely unsettled ones: CN's prohibition cells (C3/C4/C5), and TW/KR's
  pre-regime cells (C4/C5/C8), plus BR C3. These enter the verification worklist, which rises **47 → 57**.

Nothing was promoted to `resolution_text`; the **citable subset stays 21**. A `firm_summary` cell is not a
verified cell — it is a practitioner-grade summary that still owes the official-text pass.

**58 substrate poles — coverage 22/96 → 80/96.** Each pole cites the `tier1_legal` record for its cell:
**C1 for all 12**, **C7 for the nine** non-transition/non-pre-regime jurisdictions, **C6 for all 12**
(the Set A data-sovereignty input), and C2/C3/C4/C5/C8 for the established regimes. The **16 unset poles**
are left unset deliberately — TW/KR pre-regime, **UK C7 in transition**, CN C5, BR C4 — so the substrate
returns `indeterminate` there instead of guessing.

## The pole → signal mapping (and why it cross-checks)

The build enforces that every *definite* substrate class equals the signal-table `compose()`. The poles
were authored to reproduce the signal table's inbound classes exactly:

| dest | signal gate | C7 pole (or C1) | dest class |
|------|-------------|-----------------|-----------|
| US | comparability | C7 = `channelled` | II |
| EU | open_capped | C7 = `usage_capped` | I |
| SG, HK, CH | open | C7 = `open` | I |
| BR, AE, JP | fx/usage/channel | C7 = `channelled` | II |
| CN | prohibition | C1 = `prohibition` | blocked |
| TW, KR | pre_regime | C1 = `no_pathway` | pre_regime |
| UK | transition | C7 **unset** | *indeterminate* |

One rule fix was required for this to be faithful: the dest-class derivation previously mapped **both**
`prohibition` and `no_pathway` → `blocked`. But the signal table treats a pre-regime destination (TW/KR)
as `pre_regime`, not `blocked` — only an active prohibition (CN) is `blocked`. Split into
`prohibition → blocked` and `no_pathway → pre_regime` (in both `scripts/substrate.py` and
`mcp_server.py`); the cross-check is clean afterwards.

## Result

- **Authored corridors derivable: 1/9 → 9/9.**
- **Directed edges derivable: 124/132.** The eight indeterminate are the non-prohibited origins *into the
  UK* (US/EU/SG/HK/BR/CH/AE/JP → UK); CN/TW/KR → UK resolve to III by origin drag. UK-as-destination is
  in transition — the **time engine** owns that, not the substrate.
- **Cross-check now exercised across all 132 directed edges** (124 definite, every one agreeing).
  Newly-unblocked cross-region derivations: **US→EU = I, EU→US = II, US→JP = II, EU→HK = I, AE→EU = I.**
- Substrate provenance clean (every pole rests on a `tier1_legal` record). 117 → 152 records; 108 → 143
  `tier1_legal`. All prior negative tests still pass.

## What this does and does not buy

It buys **structure**: the substrate can now derive almost the whole corridor space from constraints, and
the cross-check proves the rules compose those constraints correctly on real poles. It does **not** buy
**citability**: the 57 worklist cells (and the 25 `firm_summary` cells) still owe the official-text pass,
and the authored **pole assignments** are themselves part of that backlog — verifying a cell against the
primary text is what both promotes it to `resolution_text` *and* confirms its pole. The substrate's
coverage is, as ever, the inverse of the verification backlog; v0.9.2 widened the structure that the
verification pass will make load-bearing.

## Reproducibility note

The 35 records and 58 poles were emitted by two one-off generators
(`scripts/_gen_v092_cells.py`, `scripts/_gen_v092_poles.py`) from a single content map, then **removed**:
the records and poles are now first-class files under version control, and the generators depended on a
scratch cell→id map (`/tmp/cellmap.json`) that does not survive a fresh extract. The canonical pipeline
(`build_analysis → build_corridors → compose → substrate → build_worklist → build → build_site`) rebuilds
everything from those first-class files.
