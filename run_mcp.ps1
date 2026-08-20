$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    throw ".venv is missing. Run .\setup_windows.ps1 first."
}
& .\.venv\Scripts\python.exe .\mcp_server.py
