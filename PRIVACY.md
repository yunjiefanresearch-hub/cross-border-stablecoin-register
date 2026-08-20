# Privacy

The repository contains public regulatory material and static analysis. The local MCP server makes no
network calls and CBSR itself stores no user accounts, wallet keys, prompts, counterparties, or actions.

Decision requests and receipts may nevertheless contain sensitive operational data when a downstream
client creates them. Keep such data out of Git, issues, CI logs and public artifacts. Configure retention,
access, deletion and logging in the MCP client or hosting platform; this repository cannot guarantee a
third party's behavior. Use pseudonymous action and counterparty identifiers and the minimum fields needed.

## Data lifecycle and responsibility

- CBSR processes action payloads in memory and does not persist them unless a caller chooses to store a
  receipt. A hash is not anonymisation: low-entropy or linked identifiers can remain personal data.
- Downstream operators are responsible for lawful basis, purpose limitation, notice, access control,
  retention, deletion, data-subject rights, cross-border transfer and incident response.
- Do not put names, wallet private keys, credentials, sanctions-case files or unnecessary transaction
  details into an action. Use minimum, pseudonymous identifiers and keep re-identification keys outside
  CBSR.
- Public regulatory records may still contain names of officials or regulated entities drawn from public
  sources. Corrections and removal requests follow governance and applicable law; provenance is retained
  without republishing unnecessary personal data.
- The project has not completed a deployment-specific DPIA or equivalent assessment. Production use is a
  hard stop until the operator completes one and maps the result to the Universal DPI Safeguards.
