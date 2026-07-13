# Build note — v0.9.6: time-engine forward events + verification follow-through

## Why this release exists

v0.9.5 landed the external primary-source verification and the `binding_status` axis. Reviewing that work
from a regulatory and research standpoint surfaced one concrete, actionable gap and two small ones. v0.9.6
closes them. Nothing here changes a current legal conclusion; it makes the register react correctly to two
changes of law that are visibly imminent, and reconciles two labels.

## The actionable gap: two closest-to-flipping events were not in the calendar

The register built a date-aware `compose()` and an event calendar precisely so that a cell can flip when
the law behind it changes. After v0.9.5 the two regimes nearest to flipping the `binding_status` of their
cells were not represented:

1. **US CLARITY Act** (H.R. 3633). Reported to the Senate on 1 Jun 2026 and placed on the Senate
   Legislative Calendar as Calendar No. 423. The Senate Banking Committee advanced its substitute 15-9 on
   14 May 2026. 2026 passage is roughly even (prediction markets near 48 percent in late June, down from
   about 74 percent a month earlier), and the practical floor window runs to the August recess.
2. **Singapore SCS implementing legislation**. The MAS Single-Currency Stablecoin framework was finalised
   15 Aug 2023; MAS announced at the Nov 2025 Singapore FinTech Festival that it was ready to begin
   drafting, with the framework expected to take effect mid-2026.

Both are now contingent `if enacted` events in `analysis/event_calendar.json`, each carrying the cells it
flips:

- `us-clarity-act-enacted` flips `us-pss-bank_nonbank_routing-001` from `pending_proposal` to
  `in_force_enacted`, and turns on the CLARITY Sec. 404 intermediary-yield and market-structure overlays
  carried as pending on the US yield, securities, and issuer cells.
- `sg-scs-legislation-enacted` flips the eight `sg-scs-*` requirement cells from
  `finalized_policy_pending` / `transitional` to `in_force_enacted` / `in_force`.

Because both are contingent (no fixed date), they move no `compose(as_of)` horizon yet. They are the
standing machinery: when a commencement date is fixed, the date is added, the status becomes `scheduled`,
and `compose(as_of >= that date)` flips the dependent cells automatically. The time engine now holds 6
events (UK, JP scheduled; TW, KR, US CLARITY, SG SCS contingent).

## The two small items

- **EU C7 instrument label.** The v0.9.5 pass corrected the pinpoint to Art. 58(3), but the
  `requirement_summary` and `source.primary` still read bare "Article 23". All three fields now read
  Art. 58(3) (which applies the Art. 23 means-of-exchange thresholds mutatis mutandis to non-EU-currency
  EMTs). Internally consistent, and matching the SIGNALS basis and corridor records.
- **US C3 yield cell, live development.** The Senate Banking CLARITY substitute carries the
  Tillis-Alsobrooks stablecoin-yield compromise: yield for merely holding a stablecoin balance is
  prohibited, but stablecoin rewards and activity-linked incentives are allowed. That is the
  intermediary-layer (Sec. 404) extension of the GENIUS issuer-level prohibition, and it supports the
  cell's standing position that user-initiated, activity-linked routing falls outside the holding
  prohibition. Recorded in the cell's interpretation, verified against current primary sources, flagged as
  not-yet-law, and cross-referenced to the contingent event.

## What is deliberately unchanged

The 27 still-`unset` `tier1_legal` cells remain the honest residual: the CN prohibition cells (no positive
rule to cite) and the original-language cells (CN, KR, TW, BR) that need a native-language official-text
line-read. The EU reserve RTS pinpoint (the 60/30 deposit figures live in the MiCA Level-2 RTS) is still
unresolved, so that cell correctly stays below `resolution_text`. And `compose()` still rests on the
hand-curated signal table; the verification grounded the tier1 cells in official URLs but did not remove
that dependency. These are the remaining external-work-gated frontiers, not defects.

## Verification

Full pipeline green offline (builtin validator). Time engine reports 6 events, provenance clean, and the
UK transition caveat still resolves 8 to 0 at the 2027-10-25 horizon (the two contingent events move no
dated horizon). `binding_status` gate and ledger cross-check still enforced; negative tests still bite.
Offline fresh-extract reproduces all metrics.
