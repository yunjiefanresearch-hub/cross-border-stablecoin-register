# Five-layer review and Draft PR plan

The deployment ZIP contains no `.git` history. The following is an executable review plan, **not** a
claim that five commits or Draft PRs exist.

| Layer | Branch / commit subject | Scope | Required reviewers | Hard gate |
|---|---|---|---|---|
| A | `agent/cbsr-a-runtime` / `build: canonical reproducible delivery` | constraints, verifier, package, CI | maintainer + security | full local verifier and remote platform matrix |
| B | `agent/cbsr-b-regulatory` / `data: migrate evidence and temporal review model` | 152 YAML, ledgers, dossiers, events | two independent legal reviewers | current/reconciled evidence; no synthetic identity |
| C | `agent/cbsr-c-governance` / `docs: align governance privacy and public interest` | DPG/SDG/GDC/DPI, privacy, templates | governance + privacy | exact matrices and no-overclaim checks |
| D | `agent/cbsr-d-agenticfi` / `feat: add typed policy domain and receipts` | schemas, stablecoin pack, engine, pilots | architecture + security | 31 scenarios, mutation tests, pilot replay |
| E | `agent/cbsr-e-research-release` / `docs: complete research and release evidence` | mixed methods, claims, whitepaper, manifests | independent peer reviewer + release manager | all prior layers green; external gates closed |

Create each branch from the preceding approved layer or split the source snapshot into the five subjects,
push them, create Draft PRs, retain URLs and SHAs, and never merge Layer E while regulatory, security,
GitHub or Windows hard gates remain open.
