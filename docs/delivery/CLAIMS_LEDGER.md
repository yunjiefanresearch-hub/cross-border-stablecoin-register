# Claims ledger delivery contract

Claims: **157**. Independent review: **not_completed**.

Canonical machine-readable files: `research/claims/claims_ledger.csv` and `research/claims/claims_ledger.json`.

Every row contains claim text/type, record/evidence locator, freshness, reviewer, second reviewer, review date, status, strength, allowed use, uncertainty and limitation. Blank reviewer fields remain blank; no automated process may convert them into an independent attestation.

Verification: `python tools/verify_research_delivery.py`.
