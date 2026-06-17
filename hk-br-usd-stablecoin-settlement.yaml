# Corridor record — the layer that distinguishes this register from per-jurisdiction trackers.
# Models what clears vs. what breaks at each regulatory boundary along a flow.
corridor_id: hk-br-usd-stablecoin-settlement-001
name: "HK to Brazil — USD stablecoin B2B settlement"
legs: [HK, BR]
flow: "USD-referenced stablecoin used for B2B cross-border settlement, originating HK side, terminating Brazil side"
boundary_analysis:
  - leg: HK
    gate: "<VERIFY: HK perimeter — FRS regime (Cap. 656) where issuance/distribution touches; SFC tokenisation/STO perimeter where settlement touches tokenised funds>"
    clears: "<VERIFY>"
    breaks: "<VERIFY>"
  - leg: BR
    gate: "Brazil FX perimeter. Two diverging rails: (i) eFX rail — BCB Resolution 561 prohibits eFX providers from using stablecoins/crypto to settle with overseas counterparties (effective Oct 1, 2026); (ii) VASP rail — BCB Resolution 521 permits authorised VASPs to use stablecoins for international payments inside the FX market."
    clears: "Authorised-VASP-in-FX channel (Res 521), subject to per-transaction limits (USD 100k pure VASP / USD 500k FX-authorised FI), monthly FX reporting (Annex II-A), custody segregation (Res 520: MPC/HSM, proof-of-reserves, biennial audit)."
    breaks: "eFX back-end stablecoin settlement rail (Res 561) — closing. Algorithmic / non-auditable-reserve stablecoins prohibited."
key_constraint: "A single USD-stablecoin instrument cannot serve both HK and Brazil as one uniform rail: the Brazil side forces the flow through the authorised-VASP-in-FX channel, not the closing eFX rail. This is the binding 'regulatory geography' constraint the corridor must be architected around."
us_doctrinal_link: "Same underlying question as US Sec. 404 bona-fide-activity carve-out: what activity is permitted on the regulated stablecoin rail. US = the anchor instance; see data/us-pss-permitted_activity_yield-001.yaml."
sources:
  - "BCB Resolution 521/2025; BCB Resolution 561 (Apr 30, 2026); BCB Resolution 520/2025 (custody)"
  - "<VERIFY: HK primary sources for the HK leg>"
confidence: medium
last_reviewed: "2026-06-17"
version_added: 0.1.0
