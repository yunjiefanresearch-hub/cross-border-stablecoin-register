# CN jurisdiction evidence dossier

Snapshot: CBSR v0.11.0 as of 2026-08-20. This is a record-level evidence dossier and review queue, not an independent legal opinion.

## Research posture

- Record population: 12
- Legal status: `{"no_regime": 1, "operative": 2, "prohibited": 9}`
- Evidence tier: `{"firm_summary": 4, "unverified": 8}`
- Source disposition: `{"official": 5, "unavailable": 7}`
- Freshness: `{"unknown": 12}`
- Review stage: `{"unreviewed": 12}`
- Named second reviewer: 0/12

## Official source families

- `www.csrc.gov.cn` — 5 record(s)

## Institutional and supervisory boundary

### `cn-prc-monetary_sovereignty-001` — `monetary_sovereignty`

Mainland China occupies the prohibitive pole of the monetary-sovereignty constraint. The eight-ministry Notice 银发〔2026〕42号 (in force 6 Feb 2026) reaffirms that virtual currencies have no legal-tender status and adds an explicit WRITTEN prohibition on overseas issuance of RMB-pegged stablecoins without lawful approval (未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币), plus an extraterritorial ban on PRC-controlled entities issuing virtual currencies abroad and restrictions on RWA tokenisation.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-regulatory_authority-001` — `regulatory_authority`

No single stablecoin regulator exists because there is no lawful domestic issuance pathway; instead, a coordinated multi-agency prohibition perimeter governs. The eight-ministry Notice 银发〔2026〕42号 (in force 6 Feb 2026), issued jointly with the Cyberspace Administration and the two supreme judicial organs, sets the perimeter: the People's Bank of China (PBOC) leads, with the NDRC, MIIT, MPS, SAMR, NFRA, CSRC, and SAFE. The 2026 Notice put the prohibition on private RMB-pegged stablecoin issuance into writing, formalising the stance PBOC had signalled to PRC tech groups in 2025. The CAC governs ICP, deep-synthesis/generative-AI content, and cross-border data flows; the CSRC governs A-share issuer disclosure and has directed brokerages to pause Hong Kong tokenisation activity; MIIT and SAFE supply supporting telecoms/ICP and outbound-capital measures.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-securities_classification-001` — `securities_classification`

Token issuance and exchange activity have been treated as unauthorized public fundraising / illegal financial activity rather than admitted securities offerings; there is no compliant securities pathway for private tokens.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Authorisation and licensing perimeter

### `cn-prc-bank_nonbank_routing-001` — `bank_nonbank_routing`

With no domestic issuance pathway, there is no bank/non-bank routing architecture for compliant private-token issuance to characterize.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-distribution-001` — `distribution`

All cryptocurrency promotion, offering, and trading is prohibited within PRC territory, so there is no domestic distribution channel. For PRC-connected groups operating via Hong Kong, the indirect pathway carries three independent layers of constraint: (i) A-share listing rules (a Hong Kong subsidiary's stablecoin activities are subject to related-party-transaction disclosure, results consolidate into the listed parent under the Accounting Standards for Business Enterprises, and the CSRC may require special disclosure or pre-notification); (ii) SAFE outbound-capital control (capital injections into the HK subsidiary, profit repatriation, and intra-group financing are subject to SAFE registration and quota limits); and (iii) PBOC/CAC supervisory posture: the 2026 Notice (银发〔2026〕42号, in force 6 Feb 2026) now puts in writing the prohibition on private RMB-pegged stablecoin issuance, replacing the unpublished 2025 signalling and adding an explicit extraterritorial issuance ban.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-issuer_pathway-001` — `issuer_pathway`

There is no domestic stablecoin issuance pathway. The 2017 ICO Notice (94公告) policy continues, and the 2026 Notice (银发〔2026〕42号, which repealed the 2021 Notice) treats token issuance and virtual-currency business activity as prohibited, upgrading the banned act from token-offering financing to issuing virtual currency. The live regulatory questions for PRC-connected groups therefore concern the indirect pathway through Hong Kong and the cross-border data, capital, and disclosure constraints that condition it, not a domestic licence. The behavioural boundary observed in 2025 tracks a private/state distinction: private internet groups (Ant, JD) applied for HK licences and then withdrew in October 2025; state-linked banks expressed interest and paused; and no PRC-affiliated applicant received a licence in the April 2026 first round.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Reserve, safeguarding and redemption

### `cn-prc-capital_requirements-001` — `capital_requirements`

Capital requirements are not applicable to domestic issuance. On the indirect Hong Kong pathway, the HKMA HK$25 million paid-up share capital applies to the HK-licensed entity; for PRC-listed parents, capital injected into the HK subsidiary is subject to SAFE outbound-investment registration and consolidates into the parent's financial statements under the Accounting Standards for Business Enterprises.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-reserve_backing-001` — `reserve_backing`

Reserve requirements are not applicable to domestic issuance, which is prohibited. On the indirect pathway through Hong Kong, HKMA reserve requirements apply to the HK-licensed entity; the PRC-connected parent holds no reserve obligation directly under PRC law but faces consolidation treatment under A-share listing rules.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Cross-border and data conditions

### `cn-prc-cross_border_data-001` — `cross_border_data`

Even where issuance is prohibited, stablecoin-related personal data (wallet KYC and merchant-onboarding data tied to PRC residents) falls within PIPL outbound-transfer scope and is the binding constraint that reaches non-PRC-affiliated cross-border firms. PIPL (effective 1 Nov 2021) requires that any cross-border transfer of personal information satisfy one of three gates: (a) a CAC security assessment, (b) personal-information-protection certification by a CAC-approved body, or (c) a CAC Standard Contract. The Data Security Law (DSL, effective 1 Sep 2021) subjects cross-border transfer of 'important data' to security review. The 22 March 2024 Provisions on Promoting and Regulating Cross-Border Data Flows raise the thresholds for mandatory security assessment, giving partial relief for routine business data (e.g. HR and contract-performance data). Free Trade Zone negative lists (Shanghai, Beijing, Hainan, and others) provide additional zone-specific relief.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-monetary_sovereignty-001` — `monetary_sovereignty`

Mainland China occupies the prohibitive pole of the monetary-sovereignty constraint. The eight-ministry Notice 银发〔2026〕42号 (in force 6 Feb 2026) reaffirms that virtual currencies have no legal-tender status and adds an explicit WRITTEN prohibition on overseas issuance of RMB-pegged stablecoins without lawful approval (未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币), plus an extraterritorial ban on PRC-controlled entities issuing virtual currencies abroad and restrictions on RWA tokenisation.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## AML, KYC and financial-crime controls

### `cn-prc-aml_kyc-001` — `aml_kyc`

The Anti-Money Laundering Law of the PRC and PBOC AML/CFT regulations apply to all financial institutions, and cryptocurrency-related transactions are explicitly subject to AML scrutiny under the 2017 ICO Notice (94 公告) and supporting circulars.

- Institutional/legal state: `operative` / `in_force_enacted`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Enforcement and implementation posture

### `cn-prc-implementation_status-001` — `implementation_status`

The regime is a stable prohibition with no scheduled formal rule change. Key milestones: the 2017 ICO ban (94 公告); the Data Security Law (1 Sep 2021); the reaffirmed comprehensive prohibition extended to offshore exchanges (24 Sep 2021); PIPL (1 Nov 2021); the 22 March 2024 cross-border data Provisions; the 2025 Hong Kong application window in which PRC-connected groups (Ant, JD, and state-owned banks) applied or expressed interest; and the 10 April 2026 HK first-license cohort, which excluded all PRC-connected applicants, private and state alike.

- Institutional/legal state: `no_regime` / `no_regime`.
- Evidence and uncertainty: `unverified` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.

### `cn-prc-regulatory_authority-001` — `regulatory_authority`

No single stablecoin regulator exists because there is no lawful domestic issuance pathway; instead, a coordinated multi-agency prohibition perimeter governs. The eight-ministry Notice 银发〔2026〕42号 (in force 6 Feb 2026), issued jointly with the Cyberspace Administration and the two supreme judicial organs, sets the perimeter: the People's Bank of China (PBOC) leads, with the NDRC, MIIT, MPS, SAMR, NFRA, CSRC, and SAFE. The 2026 Notice put the prohibition on private RMB-pegged stablecoin issuance into writing, formalising the stance PBOC had signalled to PRC tech groups in 2025. The CAC governs ICP, deep-synthesis/generative-AI content, and cross-border data flows; the CSRC governs A-share issuer disclosure and has directed brokerages to pause Hong Kong tokenisation activity; MIIT and SAFE supply supporting telecoms/ICP and outbound-capital measures.

- Institutional/legal state: `prohibited` / `prohibition`.
- Evidence and uncertainty: `firm_summary` / `high`.
- Decision-use gate: `unknown` / `unreviewed`.


## Line-by-line record matrix

| Record | Dimension | Legal / binding status | Evidence | Source and pinpoint | Review gate |
|---|---|---|---|---|---|
| `cn-prc-aml_kyc-001` | `aml_kyc` | `operative` / `in_force_enacted` | `unverified`; `high` uncertainty | Anti-Money Laundering Law of the PRC; PBOC AML/CFT regulations; 2017…<br>AML — PRC AML Law; PBOC AML/CFT; crypto AML scrutiny under 94 公告 | `unknown`; `unreviewed` |
| `cn-prc-bank_nonbank_routing-001` | `bank_nonbank_routing` | `prohibited` / `prohibition` | `unverified`; `high` uncertainty | PBOC framework; 2021 inter-ministerial Notice<br>Absence of a compliant issuance/routing architecture | `unknown`; `unreviewed` |
| `cn-prc-capital_requirements-001` | `capital_requirements` | `prohibited` / `prohibition` | `unverified`; `high` uncertainty | HKMA capital rules (HK entity); SAFE outbound-investment registration…<br>Capital — N/A domestically; indirect HK HK$25m + SAFE registration + consolidation | `unknown`; `unreviewed` |
| `cn-prc-cross_border_data-001` | `cross_border_data` | `operative` / `in_force_enacted` | `unverified`; `high` uncertainty | Personal Information Protection Law (PIPL, eff. 1 Nov 2021); Data Sec…<br>PIPL three-gate outbound transfer; DSL important-data review; March 2024 threshold relief; FTZ negative lists | `unknown`; `unreviewed` |
| `cn-prc-distribution-001` | `distribution` | `prohibited` / `prohibition` | `unverified`; `high` uncertainty | [PRC prohibition on cryptocurrency promotion/offering/trading within t…](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml)<br>Domestic distribution prohibited; three indirect-pathway constraint layers (A-share / SAFE / PBOC-CAC) | `unknown`; `unreviewed` |
| `cn-prc-implementation_status-001` | `implementation_status` | `no_regime` / `no_regime` | `unverified`; `high` uncertainty | 94 公告 (2017); DSL (2021); PIPL (2021); 2024 cross-border data Provisi…<br>Implementation timeline — stable prohibition; 2017-2026 milestones | `unknown`; `unreviewed` |
| `cn-prc-issuer_pathway-001` | `issuer_pathway` | `prohibited` / `prohibition` | `firm_summary`; `high` uncertainty | [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026; repealed 银发〔2021〕23…](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml)<br>银发〔2026〕42号 (virtual-currency-related business activities in the PRC are illegal financial activities, strict… | `unknown`; `unreviewed` |
| `cn-prc-monetary_sovereignty-001` | `monetary_sovereignty` | `prohibited` / `prohibition` | `firm_summary`; `high` uncertainty | [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, eff. 6 Feb 2026; repealed 银发〔20…](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml)<br>银发〔2026〕42号 — 未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币 (no entity, domestic or overseas, may issue RMB-pegged stablecoins… | `unknown`; `unreviewed` |
| `cn-prc-permitted_activity_yield-001` | `permitted_activity_yield` | `prohibited` / `prohibition` | `unverified`; `high` uncertainty | PBOC et al. Notice on Preventing Token Fundraising Risks (2017); rela…<br>Prohibition context — no permitted issuer to which a yield rule could attach | `unknown`; `unreviewed` |
| `cn-prc-regulatory_authority-001` | `regulatory_authority` | `prohibited` / `prohibition` | `firm_summary`; `high` uncertainty | [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026); issuing bodies: PB…](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml)<br>银发〔2026〕42号 (a coordinated multi-agency prohibition perimeter; eight ministries plus the cyberspace administr… | `unknown`; `unreviewed` |
| `cn-prc-reserve_backing-001` | `reserve_backing` | `prohibited` / `prohibition` | `unverified`; `high` uncertainty | PRC prohibition on domestic issuance; HKMA reserve rules apply to HK-…<br>Reserve — N/A domestically; indirect HK pathway + A-share consolidation | `unknown`; `unreviewed` |
| `cn-prc-securities_classification-001` | `securities_classification` | `prohibited` / `prohibition` | `firm_summary`; `high` uncertainty | [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号); CSRC 公告〔2026〕1号《关于境内资产境外发行资产支持…](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml)<br>银发〔2026〕42号 (token issuance treated as illegal public fundraising / illegal financial activity); CSRC 公告〔2026… | `unknown`; `unreviewed` |

## Record-level propositions and unresolved work

### `cn-prc-aml_kyc-001`

The Anti-Money Laundering Law of the PRC and PBOC AML/CFT regulations apply to all financial institutions, and cryptocurrency-related transactions are explicitly subject to AML scrutiny under the 2017 ICO Notice (94 公告) and supporting circulars.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-bank_nonbank_routing-001`

With no domestic issuance pathway, there is no bank/non-bank routing architecture for compliant private-token issuance to characterize.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-capital_requirements-001`

Capital requirements are not applicable to domestic issuance. On the indirect Hong Kong pathway, the HKMA HK$25 million paid-up share capital applies to the HK-licensed entity; for PRC-listed parents, capital injected into the HK subsidiary is subject to SAFE outbound-investment registration and consolidates into the parent's financial statements under the Accounting Standards for Business Enterprises.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-cross_border_data-001`

Even where issuance is prohibited, stablecoin-related personal data (wallet KYC and merchant-onboarding data tied to PRC residents) falls within PIPL outbound-transfer scope and is the binding constraint that reaches non-PRC-affiliated cross-border firms. PIPL (effective 1 Nov 2021) requires that any cross-border transfer of personal information satisfy one of three gates: (a) a CAC security assessment, (b) personal-information-protection certification by a CAC-approved body, or (c) a CAC Standard Contract. The Data Security Law (DSL, effective 1 Sep 2021) subjects cross-border transfer of 'important data' to security review. The 22 March 2024 Provisions on Promoting and Regulating Cross-Border Data Flows raise the thresholds for mandatory security assessment, giving partial relief for routine business data (e.g. HR and contract-performance data). Free Trade Zone negative lists (Shanghai, Beijing, Hainan, and others) provide additional zone-specific relief.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `operative`; effective from `2021-11-01`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-distribution-001`

All cryptocurrency promotion, offering, and trading is prohibited within PRC territory, so there is no domestic distribution channel. For PRC-connected groups operating via Hong Kong, the indirect pathway carries three independent layers of constraint: (i) A-share listing rules (a Hong Kong subsidiary's stablecoin activities are subject to related-party-transaction disclosure, results consolidate into the listed parent under the Accounting Standards for Business Enterprises, and the CSRC may require special disclosure or pre-notification); (ii) SAFE outbound-capital control (capital injections into the HK subsidiary, profit repatriation, and intra-group financing are subject to SAFE registration and quota limits); and (iii) PBOC/CAC supervisory posture: the 2026 Notice (银发〔2026〕42号, in force 6 Feb 2026) now puts in writing the prohibition on private RMB-pegged stablecoin issuance, replacing the unpublished 2025 signalling and adding an explicit extraterritorial issuance ban.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `cn-prc-implementation_status-001`

The regime is a stable prohibition with no scheduled formal rule change. Key milestones: the 2017 ICO ban (94 公告); the Data Security Law (1 Sep 2021); the reaffirmed comprehensive prohibition extended to offshore exchanges (24 Sep 2021); PIPL (1 Nov 2021); the 22 March 2024 cross-border data Provisions; the 2025 Hong Kong application window in which PRC-connected groups (Ant, JD, and state-owned banks) applied or expressed interest; and the 10 April 2026 HK first-license cohort, which excluded all PRC-connected applicants, private and state alike.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `no_regime`; effective from `2021-09-24`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-issuer_pathway-001`

There is no domestic stablecoin issuance pathway. The 2017 ICO Notice (94公告) policy continues, and the 2026 Notice (银发〔2026〕42号, which repealed the 2021 Notice) treats token issuance and virtual-currency business activity as prohibited, upgrading the banned act from token-offering financing to issuing virtual currency. The live regulatory questions for PRC-connected groups therefore concern the indirect pathway through Hong Kong and the cross-border data, capital, and disclosure constraints that condition it, not a domestic licence. The behavioural boundary observed in 2025 tracks a private/state distinction: private internet groups (Ant, JD) applied for HK licences and then withdrew in October 2025; state-linked banks expressed interest and paused; and no PRC-affiliated applicant received a licence in the April 2026 first round.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `prohibited`; effective from `2021-09-24`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `cn-prc-monetary_sovereignty-001`

Mainland China occupies the prohibitive pole of the monetary-sovereignty constraint. The eight-ministry Notice 银发〔2026〕42号 (in force 6 Feb 2026) reaffirms that virtual currencies have no legal-tender status and adds an explicit WRITTEN prohibition on overseas issuance of RMB-pegged stablecoins without lawful approval (未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币), plus an extraterritorial ban on PRC-controlled entities issuing virtual currencies abroad and restrictions on RWA tokenisation.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `cn-prc-permitted_activity_yield-001`

Because private token issuance and related fundraising are prohibited, there is no lawful domestic issuer that could pay yield; the yield question does not arise within a permitted perimeter.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-regulatory_authority-001`

No single stablecoin regulator exists because there is no lawful domestic issuance pathway; instead, a coordinated multi-agency prohibition perimeter governs. The eight-ministry Notice 银发〔2026〕42号 (in force 6 Feb 2026), issued jointly with the Cyberspace Administration and the two supreme judicial organs, sets the perimeter: the People's Bank of China (PBOC) leads, with the NDRC, MIIT, MPS, SAMR, NFRA, CSRC, and SAFE. The 2026 Notice put the prohibition on private RMB-pegged stablecoin issuance into writing, formalising the stance PBOC had signalled to PRC tech groups in 2025. The CAC governs ICP, deep-synthesis/generative-AI content, and cross-border data flows; the CSRC governs A-share issuer disclosure and has directed brokerages to pause Hong Kong tokenisation activity; MIIT and SAFE supply supporting telecoms/ICP and outbound-capital measures.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

### `cn-prc-reserve_backing-001`

Reserve requirements are not applicable to domestic issuance, which is prohibited. On the indirect pathway through Hong Kong, HKMA reserve requirements apply to the HK-licensed entity; the PRC-connected parent holds no reserve obligation directly under PRC law but faces consolidation treatment under A-share listing rules.

- Source disposition: `unavailable`; check status: `source_unavailable`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): official URL acquisition, freshness recheck, independent second review, reconciliation.

### `cn-prc-securities_classification-001`

Token issuance and exchange activity have been treated as unauthorized public fundraising / illegal financial activity rather than admitted securities offerings; there is no compliant securities pathway for private tokens.

- Source disposition: `official`; check status: `not_checked`.
- Temporal state: `prohibited`; effective from `None`; event `None`.
- Open gate(s): freshness recheck, independent second review, reconciliation.

## Legal-event relationships

No first-class event is mapped for this jurisdiction. This is an ontology gap, not proof of no legal change.

## Independent review and reconciliation protocol

1. Primary reviewer opens the official URL and records the exact operative pinpoint and check date.
2. A different, identified legal reviewer repeats the check without seeing the first disposition.
3. Agreement is recorded as `agreed`; disagreement records both readings and remains `reconciliation_required`.
4. A resolved row records the rationale and never overwrites the superseded reading silently.
5. Only `current` + `reconciled` + `official` rows may enter the decision-ready citable subset.

## Release gate

This dossier cannot be labelled complete legal research until every row has an official-source disposition, a current check, an exact pinpoint and independently attested reconciliation. Missing work remains visible in the ledger rather than being converted into a confidence score.

## Bibliography

1. [PRC prohibition on cryptocurrency promotion/offering/trading within territory; CSRC A-share disclosure rules; SAFE outbound-capital control…](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml) — Domestic distribution prohibited; three indirect-pathway constraint layers (A-share / SAFE / PBOC-CAC).
2. [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号); CSRC 公告〔2026〕1号《关于境内资产境外发行资产支持证券代币的监管指引》](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml) — 银发〔2026〕42号 (token issuance treated as illegal public fundraising / illegal financial activity); CSRC 公告〔2026〕1号 (RWA asset-backed-securities-token guidance: filing system + negat….
3. [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026); issuing bodies: PBOC, NDRC, MIIT, MPS, SAMR, NFRA, CSRC, SAFE, with 中央网信办/最高法/最高检](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml) — 银发〔2026〕42号 (a coordinated multi-agency prohibition perimeter; eight ministries plus the cyberspace administration and the two supreme judicial organs).
4. [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, 6 Feb 2026; repealed 银发〔2021〕237号); 2017 ICO Notice (94公告)](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml) — 银发〔2026〕42号 (virtual-currency-related business activities in the PRC are illegal financial activities, strictly prohibited; the prohibited act is upgraded from '代币发行融资' (token-off….
5. [《关于进一步防范和处置虚拟货币等相关风险的通知》(银发〔2026〕42号, eff. 6 Feb 2026; repealed 银发〔2021〕237号); 2017 ICO Notice (94公告)](https://www.csrc.gov.cn/csrc/c100028/c7614318/content.shtml) — 银发〔2026〕42号 — 未经许可，境内外任何主体不得在境外发行挂钩人民币的稳定币 (no entity, domestic or overseas, may issue RMB-pegged stablecoins overseas without approval); 境内主体及其控制的境外主体不得在境外发行虚拟货币 (PRC-controlled….

Bibliography entries reproduce committed source metadata. Inclusion is not a representation that the source was re-opened during this generation run.
