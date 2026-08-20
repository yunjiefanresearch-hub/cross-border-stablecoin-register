# Windows local deployment

This bundle is source-installable and does not assume a PyPI release. It is intended for the folder
you showed earlier, for example:

`C:\Users\yunji\OneDrive\ドキュメント\GitHub\cross-border-stablecoin-register`

## One-command setup

1. Extract the ZIP to a normal folder. Avoid extracting a second copy inside an older checkout.
2. Open that folder in File Explorer.
3. Right-click an empty area and choose **Open in Terminal**.
4. Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\setup_windows.ps1
```

The script creates `.venv`, installs the exact versions in `constraints/dev.txt`, runs `pip check`,
then calls the same `python -m tools.verify` used by Linux CI. The verifier performs two complete
regenerations, committed-output and second-pass hash checks, research reproduction, all positive and
negative gates, two reproducible wheel builds, clean wheel installation outside the repository, all six
AgenticFi tool calls with warnings treated as errors, SBOM generation, licence inventory and `pip-audit`.
A green final line is `VERIFY OK`.

If `.venv` already exists, setup stops rather than silently reusing it. Use the non-destructive recheck:

```powershell
.\verify_windows.ps1
```

To perform a deliberate clean-room rebuild of this project's `.venv`:

```powershell
.\setup_windows.ps1 -Recreate
```

The transcript, resolved dependency list and JSON verification summary are written to
`artifacts\validation\windows\`. These files are CI evidence and are not legal-currentness evidence.

## Recheck and run

```powershell
.\verify_windows.ps1
.\run_mcp.ps1
```

The MCP server uses stdio, so a blank-looking running terminal is normal. Stop it with `Ctrl+C`.

## MCP client configuration

Use absolute paths and forward slashes. Adjust the username/folder if yours differs:

```json
{
  "mcpServers": {
    "cbsr": {
      "command": "C:/Users/yunji/OneDrive/ドキュメント/GitHub/cross-border-stablecoin-register/.venv/Scripts/python.exe",
      "args": [
        "C:/Users/yunji/OneDrive/ドキュメント/GitHub/cross-border-stablecoin-register/mcp_server.py"
      ]
    }
  }
}
```

## Important evidence boundary

The bundle is runnable, but a successful test is not a legal-currentness certificate. Each record now
carries a derived freshness status. Stale, due, unknown, proposed, not-commenced or conflicting evidence
cannot return an unconditional `allow` from `evaluate_action`.

## Platform evidence boundary

The ZIP contains the exact Windows workflow and evidence capture path, but this Linux-built bundle does
not claim that Windows 11 has passed. A Windows claim becomes valid only after either:

- the GitHub Actions `verify-windows-clean-room-python-3.12` job succeeds and its artifact is retained; or
- the commands above succeed on a physical Windows 11 host and the generated transcript is preserved.

Likewise, Python 3.10-3.13 matrix status must be read from a real successful GitHub Actions run. Workflow
declaration is not execution evidence.
