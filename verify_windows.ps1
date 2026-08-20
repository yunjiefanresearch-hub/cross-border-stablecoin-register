param([string]$EvidenceDir = "artifacts/validation/windows")

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$VenvPython = Join-Path $PSScriptRoot ".venv/Scripts/python.exe"
if (-not (Test-Path $VenvPython)) {
    throw ".venv is missing. Run .\setup_windows.ps1 first."
}

$EvidencePath = Join-Path $PSScriptRoot $EvidenceDir
New-Item -ItemType Directory -Force -Path $EvidencePath | Out-Null
$TranscriptPath = Join-Path $EvidencePath "recheck.log"
Start-Transcript -Path $TranscriptPath -Force | Out-Null
try {
    $env:CBSR_EVIDENCE_DIR = $EvidencePath
    $env:PYTHONUTF8 = "1"
    $env:CBSR_BUILD_DATE = "2026-08-20"
    & $VenvPython -m pip check
    if ($LASTEXITCODE -ne 0) { throw "pip check failed." }
    & $VenvPython -m tools.verify
    if ($LASTEXITCODE -ne 0) { throw "Canonical verification failed." }
    Write-Host "VERIFY OK. Evidence: $EvidencePath"
}
finally {
    Stop-Transcript | Out-Null
}
