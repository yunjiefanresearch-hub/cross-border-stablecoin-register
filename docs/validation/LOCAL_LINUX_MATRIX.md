# Local Linux Python matrix

> This is evidence from local Linux execution on 2026-08-20. It is not a
> substitute for a successful GitHub Actions run or a Windows 11 transcript.

| Python | Canonical steps | Generated artifacts | Warning policy | Audit | Wheel SHA-256 |
|---|---:|---:|---|---|---|
| 3.10.20 | 73/73 | 332 × 2 passes | `error` | `passed_locked_graph_against_2026-08-20_live_snapshot` | `02bfe7589dfb0f3f7e28240be2c79da73cd86134c668015f8258146c60177d4b` |
| 3.11.15 | 73/73 | 332 × 2 passes | `error` | `passed_locked_graph_against_2026-08-20_live_snapshot` | `02bfe7589dfb0f3f7e28240be2c79da73cd86134c668015f8258146c60177d4b` |
| 3.12.13 | 73/73 | 332 × 2 passes | `error` | `passed_no_known_vulnerabilities_live` | `02bfe7589dfb0f3f7e28240be2c79da73cd86134c668015f8258146c60177d4b` |
| 3.13.14 | 73/73 | 332 × 2 passes | `error` | `passed_locked_graph_against_2026-08-20_live_snapshot` | `02bfe7589dfb0f3f7e28240be2c79da73cd86134c668015f8258146c60177d4b` |

All four runs used constraint digest `6970056c0c0b56de1cdc63e21d4cd5fb2ee2e4ca21242d31b2ca628b8ca37a7a`, source fingerprint
`d3193c1c680b3a023455829e005446c54035f7328b69508539e1014fcfc649e9` and produced
the same wheel bytes. Raw logs are transient build evidence; their SHA-256 values and
the complete machine-readable results are recorded in `local-linux-matrix.json`.

GitHub Actions and Windows remain external release gates as described in
`PLATFORM_EVIDENCE.md`.
