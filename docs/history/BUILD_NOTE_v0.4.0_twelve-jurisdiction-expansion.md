# Build Note — v0.4.0: The twelve-jurisdiction expansion

**Date:** 2026-06-27 · **Maintainer:** Yunjie Fan · **Scope:** focus set 7 → 12 jurisdictions
(Switzerland, the UAE, Taiwan, Japan, South Korea added); 56 new records → **117 records across
12 jurisdictions**; schema `jurisdiction` enum extended to CH/AE/JP/KR.

This note answers the question that drove the build: *the underlying research has been revised —
the Compliance Matrix is now v0.9.6 and the Architecture paper is now v3 covering twelve
jurisdictions — so what does the register need to do to come back to parity with its own
substrate?* The short answer: **add the five jurisdictions the substrate now carries, faithfully,
with the same provenance discipline as every prior load, and preserve the draft-versus-in-force
distinction the new entries hinge on.** The long answer follows.

---

## 1. What changed in the substrate

The register is downstream of three companion works. All three were revised:

| Companion | Was | Now | What it supplies the register |
|---|---|---|---|
| Multi-Jurisdiction Stablecoin Compliance Matrix | v0.9.3 (6–7 jurisdictions) | **v0.9.6** (12 jurisdictions) | The **node-level data substrate** — every new record's `secondary` provenance cites this. |
| Cross-Border Stablecoin Architecture | "six-jurisdiction" working paper | **v3 — Eight Constraints, Twelve Jurisdictions, Three Architectural Patterns** | The C1–C8 vocabulary (`constraint_ref`) and the §5 narrative posture per jurisdiction. |
| Cross-Border Digital-Finance Corridor Atlas | — | **v0.2.3** (132 directed edges) | The directed-edge companion; informs the v0.5.0 corridor-layer roadmap, not yet loaded as records. |

The gap this version closes: the register sat at **7 focus jurisdictions** (US, EU, UK, SG, HK, CN,
BR) with Taiwan a parked window, while the substrate had moved to **12**. Five jurisdictions —
**Switzerland, the United Arab Emirates, Taiwan, Japan, South Korea** — had verified Matrix entries
with **no home in the register.**

---

## 2. The five additions, and the one analytical reason each earns its place

Each new jurisdiction contributes a *distinct* data point that the prior seven did not represent —
which is exactly why a depth-first register wants them:

| New | Code | The distinctive data point it adds |
|---|---|---|
| **Switzerland** | `CH` | **Regulation without a statute.** The whole non-bank market runs through one textual aperture (the bank-guarantee exemption, Banking Ordinance Art. 5(3)(f)). On the **yield spine (C3)** it is the clearest *permission-cluster anchor*: holder yield is permitted, but the guarantee must cover principal **plus interest** — the opposite pole to the EU/HK/US prohibition. AML is the strictest in the survey (identify *every* holder, including intermediate holders). |
| **United Arab Emirates** | `AE` | **Federal-vs-free-zone split + a monetary-sovereignty *channel* restriction (C7).** Foreign tokens are excluded from general onshore payments (reserved to CBUAE Dirham Payment Tokens) — a *usage-channel* restriction, **not** an aggregate cap. ADGM's promotion-based yield line is the survey's closest non-US analogue to GENIUS "solely." |
| **Taiwan** | `TW` | **A regime under construction.** AML registration is in force; the Virtual Asset Service Act issuance regime is a **draft bill** (peg NTD-vs-USD undecided). Promoted here from a forthcoming window to a full jurisdiction, with the draft layer carried as `status: proposed`. |
| **Japan** | `JP` | **Closed issuer trichotomy + channelled admission (C7).** Electronic Payment Instruments may be issued only by banks, funds-transfer providers, or trust banks; foreign tokens are admitted via a registered EPIESP holding reserves in Japan. Live: JPYC (Oct 2025), USDC via SBI VC Trade (Mar 2025). |
| **South Korea** | `KR` | **Pre-regime, paired with Taiwan.** VAUPA (user-protection/AML) in force; the Digital Asset Basic Act issuance regime pending, with the BOK-vs-FSC eligibility-and-sovereignty fight the item stalling it. Draft FX-means-of-payment classification echoes Brazil's câmbio reclassification (by effect). |

Two of these — the **UAE channel restriction** and the **Japan channelled-admission** model —
extend the `monetary_sovereignty` (C7) comparison from a three-point spectrum (EU cap / HK
restriction / PRC prohibition) to a **five-archetype** spectrum.

---

## 3. How the records were built (and the provenance discipline preserved)

- **Transcription, not generation.** Records were transcribed from the Matrix v0.9.6 jurisdictional
  entries (cross-referenced with Architecture v3 §5). No citation is machine-generated; each
  `source.primary` + `pinpoint` is the Matrix's, cited as `secondary`. `source.url` is left empty
  pending the verification pass.
- **`evidence_tier: firm_summary` across all 56.** The Matrix's own added entries carry a tiered
  verification note (Tier 1 well-corroborated / 1b confirmed-against-text / 2 corrections / 3 open).
  Because the register builder did **not** read the official primary instruments in this pass, the
  honest tier is `firm_summary` — identical to the v0.3.x Brazil convention.
- **Draft-law is flagged, not laundered.** For TW and KR, only the in-force layer (AML / user
  protection) is `status: in_force`; every draft issuance/reserve/capital/yield/redemption/
  monetary-sovereignty/distribution provision is `status: proposed` with the `draft_provision` tag.
  The build still renders these ✅ in `COVERAGE.md` (a sourced record with no `<VERIFY` marker), so
  the draft nuance lives in `status` / `evidence_tier` / `tags`, and the interpretation note says so
  explicitly.
- **Confidence is conservative.** `high` for well-corroborated in-force facts; `medium` for nuanced
  or contested points; `low` for figures that diverge across sources (e.g., KR minimum capital).
- **Interpretive flags carried over.** The Matrix's `[⚠ interpretive question]` constructs are
  encoded as structured `interpretive_flag: {tension, resolution_channel}` on the CH (CISA / holder
  ID), AE (yield asymmetry / channel), TW (draft alignment / peg), JP (intermediary yield), and KR
  (draft alignment / sovereignty contest) records.

---

## 4. Pipeline changes

| File | Change |
|---|---|
| `record.schema.json` | `jurisdiction` enum 8 → 12 (added CH, AE, JP, KR; TW already present). Additive/backward-compatible. |
| `roadmap.yaml` | `focus_jurisdictions` now the full twelve; `backfill_jurisdictions` cleared; planned cells re-scheduled (`⬜0.4.x`). |
| `_build_v0_4_0.py` + `_build_v0_4_0_part2.py` | The builder for this load (kept for provenance, like `_backfill_v0_3_0.py`). |
| `mcp_server.py` | `JURISDICTIONS` map extended to twelve. |
| `build.py` | `REGISTER_VERSION` → 0.4.0; regenerates `dataset.json` / `COVERAGE.md` / `records.md`. |
| `build_site.py` → `index.html` | `JURS` array extended to twelve (BR/TW de-flagged as forthcoming); headline and roadmap cards updated; stats auto-fill (12 jurisdictions, 117 records). |
| `README.md` · `ROADMAP.md` · `taxonomy.md` · `CHANGELOG.md` · `CITATION.cff` | Synced to the 117-record / 12-jurisdiction state. |

> Validation note: as in v0.3.1, `python build.py` was run under a **local `jsonschema`
> validation shim** (the sandbox has no network to `pip install jsonschema`). The shim implements
> Draft 2020-12 type/enum/pattern/required/additionalProperties/minLength/format checks and was
> self-tested against deliberately malformed records before the build. The maintainer should run
> the real `python build.py` (with `jsonschema` installed) as the final gate before tagging.

---

## 5. What this version does *not* do

- It does not read the new jurisdictions' primary instruments against the official text — that is
  the **v0.4.x verification pass** (promote `firm_summary` → `resolution_text`; populate
  clause-level `source.url`).
- It does not load the Corridor Atlas's 132 directed edges. The register keeps its single worked
  corridor; the directed-edge model is the **v0.5.0** roadmap item. Depth before breadth.
- It does not fill `securities_classification`, `custody`, or `disclosure_reporting` for every new
  jurisdiction — only where the Matrix gives clear signal (e.g., Switzerland's CISA C4 cell). The
  remaining cells are scheduled (`⬜0.4.x`) on purpose, visible in `COVERAGE.md`.
