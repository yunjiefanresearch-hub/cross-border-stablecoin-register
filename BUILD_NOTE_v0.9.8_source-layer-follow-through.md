# Build note — v0.9.8: source-layer follow-through (matrix / architecture / corridor carry 42号)

## Why this release exists

v0.9.7 did the original-language verification and corrected the record cells: China's RMB-pegged-stablecoin
prohibition is written, in-force law (银发〔2026〕42号, 6 Feb 2026, repealing the 2021 Notice), Brazil's BCB
regime is in force, and so on. But the register has higher-level hand-authored source layers on top of the
records: the §5.14 pairwise compatibility matrix, the §3.3 architecture typology, the C1–C8 constraint
substrate, and the directed corridor edges. Those layers still described China the old way ("not by any
single explicit prohibition", a generic prohibition axis) and still carried a few empty placeholders.

v0.9.8 propagates the verified facts up into those layers. Nothing here changes a fact or a feasibility
conclusion; it removes the lag between the record layer and the layers built on top of it.

## What changed, and where the source actually lives

A subtlety worth recording: several of these "source" files are themselves generated. The matrix, the
architecture typology, and the open questions are emitted by `build_analysis.py` from in-script dicts, so the
edit has to be made there, not in the generated `analysis/*.json`. The HK→CN corridor is emitted by
`build_corridors.py` from its `C` list. The constraint substrate and the HK→BR corridor are genuinely
hand-authored files. The edits were made at the real source in each case:

- **§5.14 matrix** (`build_analysis.py`): the Category-III PRC prohibition axis cites 银发〔2026〕42号.
- **§3.3 architecture** (`build_analysis.py`): the PRC boundary now records the explicit written prohibition
  (42号) as of Feb 2026, and distinguishes it from what is still genuinely emergent — the
  Direct-Subsidiary-via-Hong-Kong pathway, constrained by the data-sharing pattern rather than a categorical
  exclusion. The old "not by any single explicit prohibition" wording is gone.
- **Constraint substrate** (`analysis/constraint_substrate.json`): CN C1 note cites 42号; no longer says the
  2021 framework is in force.
- **HK→CN blocked corridor** (`build_corridors.py`): the blocked-destination inbound mechanism cites 42号
  (the written issuance prohibition) alongside the PIPL/DSL/CAC/SAFE data and capital rules.
- **Open question §7.2** (`build_analysis.py`): reframed around the Feb-2026 written tightening; 42号 is
  marked as the RESOLVED tightening event, the three relaxation paths are the still-open branch.
- **HK→BR corridor** (`hk-br-usd-stablecoin-settlement.yaml`): four `record_refs` that were empty
  "forthcoming" / "GAP" placeholders are wired to the BR and HK records that now exist after v0.9.7.

## Invariants

Six new source-layer invariants (`run_invariants.py` D1–D6) assert that the matrix, the architecture, the
substrate note, the HK→CN corridor, the HK→BR record_refs, and open question §7.2 each carry the 42号
reality. The suite is now 39 invariants (was 33). The negative-test battery is unchanged at 6 gates.

## Verification

Full pipeline green offline (builtin validator) and under real `jsonschema`. Citable subset still 46; time
engine still 6 events with the UK 8 → 0 horizon at 2027-10-25; substrate pre_regime cross-check still
{TW, KR}; cross-layer category agreement still enforced (9 corridors, 7 declared divergences). 39 invariants
hold; 6 negative-test gates bite. Offline fresh-extract reproduces all metrics, and `python build.py` runs on
a non-UTF-8 console without `-X utf8`.
