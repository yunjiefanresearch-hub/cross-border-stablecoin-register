# Build note — v0.9.7: native-language official-text verification (CN / KR / TW / BR)

## Why this release exists

Every version since v0.9.5 named the same residual: the original-language jurisdictions (China, Korea,
Taiwan, Brazil) needed a line-read against official text in the original language before their in-force
cells could be promoted out of the unverified backlog. An external pass did that spadework against
original-language official and authoritative sources. v0.9.7 applies it.

The discipline is unchanged from the v0.9.5 verification: a cell reaches `resolution_text` only where
`binding_status == in_force_enacted` AND its load-bearing proposition is confirmed against the official text
of the cited instrument. Prohibitions stay prohibition. Before encoding, each material claim was
re-verified against current primary sources, because a legal register must not encode a repeal or a new
prohibition on assumption.

## Brazil: in-force regime confirmed, citable subset 36 → 46

The BCB framework is enacted and in force (2 Feb 2026). The pass confirmed it against the official
Portuguese text, and the official BCB normativo URLs were retrieved. Ten BR cells are promoted to
`resolution_text` with article-level pinpoints:

- reserve_backing — Res BCB 520 Art. 2, III (reserve assets = the fiduciary currency plus public debt
  issued by the same governments) and Arts. 64+ (asset curation; algorithmic-stablecoin prohibition; proof
  of reserves).
- custody — Res 520 patrimonial segregation (client funds in individualised accounts; client virtual
  assets in segregated wallets) and the foreign-custodian conditions.
- capital_requirements — Resolução Conjunta CMN/BCB 14/2025 + Res BCB 517/2025 (R$10.8m to R$37.2m scaled by
  activity).
- issuer_pathway — Lei 14.478/2022 (authorisation required) + Res 519 (process) + Res 520 Art. 4 (three
  SPSAV modalities), Art. 14 (corporate form; ≥3 administrators; head office in Brazil); 30 Oct 2026
  deadline.
- regulatory_authority and securities_classification — Lei 14.478/2022 + Decreto 11.563/2023 (BCB as
  competent authority; CVM jurisdiction preserved over tokens that are securities).
- monetary_sovereignty — Res BCB 521 (virtual-asset services brought into the FX market; monthly reporting
  from 4 May 2026).
- aml_kyc and disclosure_reporting — Res 520 (PLD/FTP; proof of reserves; audits) + Res 521 (FX reporting).
- bank_nonbank_routing — Res 520 Art. 20 (which banks/brokers may also provide intermediation/custody).

**BR C3 yield** leaves `pending_proposal` for `in_force_enacted`: Res 520 (in force) prohibits VASPs from
offering credit and from public fundraising except via share issuance, and restricts client-asset use to
staking / qualified-investor transactions. It is held at `firm_summary`, not `resolution_text`, because the
specific stablecoin yield **pass-through** question (whether a compliant issuer may pass reserve yield to
holders) is still unsettled pending further BCB rulemaking. That is the honest line: the broad rules are
confirmed in force; the narrow sub-question is not yet answered.

## China: a material currency correction

The register cited the 2021 Notice (银发〔2021〕237号). The pass found, and primary sources confirm, that it
was **repealed**: 《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号), eight ministries, in force
6 Feb 2026, states "银发〔2021〕237号同时废止". Two corrections follow:

1. The operative-instrument citation across the CN cells now reads 42号 (with the 2017 ICO Notice policy
   continued and the CSRC 公告〔2026〕1号 RWA ABS-token guidance noted where relevant).
2. CN C7 framed the RMB-pegged-stablecoin prohibition as "PBOC October 2025 verbal guidance". It is now
   **written, in-force law**: 42号 explicitly bans overseas issuance of RMB-pegged stablecoins without
   approval (未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币) and adds an extraterritorial issuance ban on
   PRC-controlled entities. The "verbal guidance" wording is removed from the affected summaries.

Substance is unchanged: China remains the prohibition pole (Category-III / blocked). This is a provenance
and currency correction, not a re-classification. The prohibition cells stay below `resolution_text` (a
prohibition has no positive permitted-activity rule to cite); the directly-addressed cells move to
`firm_summary` on the written text.

## Korea and Taiwan: procedural accuracy

- KR: the over-precise "off the subcommittee (12 May 2026)" wording is softened. The DABA and three
  stablecoin-specific bills remained in the 정무위 subcommittee in late Apr 2026; passage is targeted for H2
  2026 but uncertain, delayed by the won-stablecoin **51% issuer-eligibility dispute** (the Bank of Korea
  favouring a bank-majority consortium) and the June local elections / committee reconstitution. The cells
  stay `pending_proposal`.
- TW: confirmed current. The VAS Act passed the Legislative Yuan Finance Committee article-by-article first
  review (初審) on 3 Jun 2026 and went to the plenary, not yet through third reading. It is procedurally more
  advanced than KR's DABA. The cells stay `pending_proposal`; the in-force VASP-AML layer
  (`tw-frs-aml_kyc-001`) stays `resolution_text`, confirmed against the MOJ text.

The `kr-daba-enacted` and `tw-vas-act-enacted` contingent events now record their differing procedural
stages.

## Engineering

`apply_verification.py` is now fully idempotent on the `verification` block. A disposition that no longer
asserts a verdict (for example BR C3 yield, which moved from a verdict-bearing pending note to an in-force
firm_summary) drops any stale block, whose `against.url` would otherwise diverge from the new source. The
verification-consistency gate catches the divergence; a new negative test covers it.

**Cross-platform UTF-8.** A local run on Windows surfaced that `python build.py` failed with
`UnicodeDecodeError` on a Chinese-locale console: the scripts read files using the platform default codec
(GBK on that machine), which cannot decode the CJK and Portuguese text. Every `read_text()` / `write_text()`
across the build scripts now passes `encoding="utf-8"` explicitly, and each script reconfigures stdout/stderr
to UTF-8 (guarded, so it is a no-op where unsupported). The full pipeline, build, and site now run end to end
under a strict pure-ASCII locale (stricter than GBK), with the CJK/Portuguese text preserved in the outputs.
`python build.py` no longer needs the `-X utf8` workaround.

## What remains

The honest residual is now smaller. The CN prohibition cells stay `unset`/`firm_summary` (no positive rule
to cite). The EU reserve RTS pinpoint (the 60/30 deposit figures in the MiCA Level-2 RTS) is still
unresolved, so that cell correctly stays below `resolution_text`. And `compose()` still rests on the
hand-curated signal table. These are the remaining frontiers.

## Verification

Full pipeline green offline (builtin validator). Citable subset 46. Time engine 6 events, provenance clean,
UK transition caveat still 8 → 0 at the 2027-10-25 horizon. Substrate pre_regime cross-check still {TW, KR}.
33 invariants and a 6-test negative battery pass, both shipped as runnable scripts (`run_invariants.py` prints `33/33 invariants hold`; `run_negative_tests.py` prints `6/6 gates bit`, breaking each gate on a throwaway copy so the originals are never touched). Offline fresh-extract reproduces all metrics.

## Reproducible verification scripts (new in v0.9.7)

The invariant suite and the negative-test battery used to ship as prose claims ("N invariants pass"). They are now two shipped, runnable scripts so the counts are concrete and anyone can re-check them:

- `python run_invariants.py` -> read-only assertions over the built register; prints a per-check PASS/FAIL report and `RESULT: 33/33 invariants hold`. (Earlier notes quoted 11 or 18; that was an ad-hoc count in prose. The shipped suite is 33 checks, covering the binding_status cap, citable integrity/purity, the verification ledger, the analysis/substrate/edge layers, the time engine, the v0.9.7 native-language pass, the UTF-8 portability fix, and the version stamp.)
- `python run_negative_tests.py` -> proves the six gates BITE; copies the register to a temp directory, introduces one defect per gate, asserts `build.py` fails, and restores. Prints `RESULT: 6/6 gates bit`.
