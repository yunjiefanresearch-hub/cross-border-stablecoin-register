# CBSR 0.11 rollback notes

1. Stop downstream decision use; retain affected action/receipt hashes and logs without sensitive payloads.
2. Verify the target artifact checksum and restore the prior immutable wheel/ZIP. Do not copy generated outputs selectively.
3. Restore source YAML and regenerate all projections with that version's canonical verifier.
4. Do not downgrade new review fields into a claim of currentness. Preserve the v0.11 research ledger for audit.
5. Revoke or mark incompatible mandates/receipts by schema and engine version; unsigned receipts are not authorization.
6. Record incident, scope, owner, timeline, restored hash and validation evidence. Reopen only after the complete verifier passes.

Rollback cannot reverse an external legal change, data disclosure, credential leak or already-consumed downstream decision.
Those events require the applicable incident, correction and notification procedure.
