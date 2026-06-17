# Controlled vocabulary

## Jurisdictions
`HK` Hong Kong · `TW` Taiwan · `BR` Brazil · `US` United States ·
`EU` European Union · `UK` United Kingdom · `SG` Singapore · `CN` mainland China
(Focus: HK, TW, BR. Anchor: US. Backfill: EU, UK, SG, CN.)

## instrument_type (normalized) ↔ instrument_label_local (verbatim)
- `fiat_referenced_stablecoin` — HK "specified stablecoin", general FRS
- `payment_stablecoin` — US "payment stablecoin" (GENIUS Act / CLARITY)
- `e_money_token` / `asset_referenced_token` — EU MiCA EMT / ART
- `tokenized_mmf` — 1940-Act registered tokenised money market fund (e.g. routing target)
- `tokenized_security` — tokenised security under local securities law
- `other`
The dual field is the built-in concordance: one normalized type, each regime's own label.

## dimensions (10)
`regulatory_authority` · `issuer_pathway` · `reserve_capital` ·
**`permitted_activity_yield`** (spine — the bona-fide-activity / yield line) ·
`redemption` · `custody` · `aml_kyc` · `cross_border_data` ·
`distribution` · `implementation_status`

## status
`in_force` · `transitional` · `proposed` · `consultation`

## confidence
`high` · `medium` · `low`
