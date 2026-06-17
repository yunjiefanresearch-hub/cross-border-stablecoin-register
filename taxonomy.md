# Controlled vocabulary

## Jurisdictions
`HK` Hong Kong · `TW` Taiwan · `BR` Brazil · `US` United States ·
`EU` European Union · `UK` United Kingdom · `SG` Singapore · `CN` mainland China

**Coverage reorientation (v0.2.0-dev).** The author's written substrate — the Compliance
Matrix v0.9.3 and the Cross-Border Stablecoin Architecture working paper — covers
**US, EU, UK, SG, HK, CN** in verified depth. The register's focus set is aligned to that
substrate:
- **Anchor:** US (CLARITY §404 / GENIUS Act — the doctrinal anchor).
- **Focus (verified substrate exists):** HK, EU, UK, SG, CN.
- **Corridor-only:** BR (appears in the HK→BR corridor via BCB resolutions; not yet covered
  in the per-jurisdiction matrix — flagged for primary-source verification).
- **Parked (no written substrate yet):** TW.

## instrument_type (normalized) ↔ instrument_label_local (verbatim)
- `fiat_referenced_stablecoin` — HK "specified stablecoin" / FRS; general FRS
- `payment_stablecoin` — US "payment stablecoin" (GENIUS Act / CLARITY)
- `e_money_token` / `asset_referenced_token` — EU MiCA EMT / ART
- `tokenized_mmf` — 1940-Act registered tokenised money market fund (routing target)
- `tokenized_security` — tokenised security under local securities law
- `other`
The dual field is the built-in concordance: one normalized type, each regime's own label.

## dimensions (15) — aligned to the eight-constraint framework

The register's dimension set is the union of (a) the ten Compliance-Matrix dimensions and
(b) the eight constraints of *Cross-Border Stablecoin Architecture* (§2.1–§2.8). The
`constraint_ref` field on each record links back to the constraint vocabulary.

| Dimension | Constraint | Notes |
|---|---|---|
| `regulatory_authority` | — | authority + statutory basis |
| `issuer_pathway` | C1 Issuer Eligibility | |
| `reserve_backing` | C2 (reserve half) | **split** from former `reserve_capital` |
| `capital_requirements` | C2 (capital half) | **split** from former `reserve_capital` |
| **`permitted_activity_yield`** | **C3 Yield Prohibition** | **spine 1** — the bona-fide-activity / yield line |
| **`securities_classification`** | **C4 Securities Classification** | **spine 2 (new)** — Reves/Howey; routing-into-funds line |
| `bank_nonbank_routing` | C5 Bank/Non-Bank & Routing | **new** — who may route; layer separation |
| `redemption` | — | |
| `custody` | C2 (custody facet) | |
| `aml_kyc` | — | |
| `cross_border_data` | C6 Cross-Border Payment & Data | |
| `monetary_sovereignty` | **C7 Monetary Sovereignty / Reserve-Currency Asymmetry** | **new** — non-domestic-currency usage caps |
| `disclosure_reporting` | C8 Disclosure, Reporting, Supervisory Coordination | **new** — attestation/audit/reporting |
| `distribution` | — | |
| `implementation_status` | — | maturity stage / timeline |

**Two spines.** The original register had one spine (`permitted_activity_yield`). The written
corpus makes clear there is a *second* spine, `securities_classification`: two stand-alone
papers (*When Wallets Become Brokers*; *Reves' Fourth Factor and Stablecoin Routing*) turn on
it, and §4 of the Architecture paper composes C3×C4 directly. It is promoted to spine status.

## status
`in_force` · `transitional` · `proposed` · `consultation`

## confidence
`high` · `medium` · `low`

## interpretive_flag
Carries the Matrix's `[⚠ interpretive question]` construct as structured data:
`{ tension, resolution_channel }`. These are research instruments, not legal advice.
