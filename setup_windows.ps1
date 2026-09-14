param(
    [string]$Python = "",
    [switch]$Recreate,
    [string]$EvidenceDir = "artifacts/validation/windows"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$EvidencePath = Join-Path $PSScriptRoot $EvidenceDir
New-Item -ItemType Directory -Force -Path $EvidencePath | Out-Null
$TranscriptPath = Join-Path $EvidencePath "setup-and-verify.log"
Start-Transcript -Path $TranscriptPath -Force | Out-Null

try {
    if (-not $Python) {
        if (Get-Command py -ErrorAction SilentlyContinue) {
            $Python = "py"
            $PythonArgs = @("-3.12")
        } elseif (Get-Command python -ErrorAction SilentlyContinue) {
            $Python = "python"
            $PythonArgs = @()
        } else {
            throw "Python was not found. Install Python 3.12, then rerun this script."
        }
    } else {
        $PythonArgs = @()
    }

    $Version = & $Python @PythonArgs -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
    if ($LASTEXITCODE -ne 0) { throw "Unable to run the selected Python interpreter." }
    $Minor = ($Version -split '\.')[0..1] -join '.'
    if ($Minor -ne "3.12") {
        throw "The Windows clean-room hash lock targets Python 3.12. Selected: $Version. Linux CI also tests 3.10, 3.11 and 3.13."
    }

    $RepositoryPath = (Get-Item -LiteralPath $PSScriptRoot).FullName
    $VenvPath = [IO.Path]::GetFullPath((Join-Path $RepositoryPath ".venv"))
    if (Test-Path -LiteralPath $VenvPath) {
        if (-not $Recreate) {
            throw ".venv already exists. Run .\verify_windows.ps1, or rerun setup with -Recreate for a clean room."
        }
        $ExistingVenv = Get-Item -LiteralPath $VenvPath -Force
        if (-not $ExistingVenv.PSIsContainer -or
            ($ExistingVenv.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
            $ExistingVenv.Parent.FullName -ne $RepositoryPath -or
            $ExistingVenv.Name -ne ".venv") {
            throw "Refusing to recreate a linked or unexpected .venv target: $VenvPath"
        }
        Write-Host "[1/5] Removing the explicitly selected CBSR .venv"
        Remove-Item -LiteralPath $VenvPath -Recurse -Force
    }

    Write-Host "[1/5] Creating clean .venv with Python $Version"
    & $Python @PythonArgs -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed." }
    $VenvPython = Join-Path $VenvPath "Scripts/python.exe"
    $SharedPipCache = Join-Path $env:TEMP "cbsr-pip-cache"
    $env:PIP_CACHE_DIR = $SharedPipCache
    $env:CBSR_PIP_CACHE_DIR = $SharedPipCache
    $env:CBSR_PIP_AUDIT_CACHE_DIR = Join-Path $env:TEMP "cbsr-pip-audit-cache"

    Write-Host "[2/5] Installing the SHA-256-verified development graph"
    & $VenvPython -m pip install --require-hashes --only-binary=:all: -r constraints/dev-hashes.txt
    if ($LASTEXITCODE -ne 0) { throw "Hash-checked dependency installation failed." }

    Write-Host "[3/5] Building and hash-checking this checkout's CBSR wheel"
    $LocalWheelDirectory = Join-Path $EvidencePath ("local-wheel-" + [guid]::NewGuid().ToString("N"))
    & $VenvPython -m build --wheel --no-isolation --outdir $LocalWheelDirectory
    if ($LASTEXITCODE -ne 0) { throw "Local CBSR wheel build failed." }
    & $VenvPython tools/install_local_wheel.py --wheel-dir $LocalWheelDirectory
    if ($LASTEXITCODE -ne 0) { throw "Local wheel installation failed." }

    Write-Host "[4/5] Checking the resolved environment"
    & $VenvPython -m pip check
    if ($LASTEXITCODE -ne 0) { throw "pip check failed." }
    & $VenvPython -m pip freeze | Out-File -Encoding utf8 (Join-Path $EvidencePath "pip-freeze.txt")

    Write-Host "[5/5] Running the only canonical verifier"
    $env:CBSR_EVIDENCE_DIR = $EvidencePath
    $env:PYTHONUTF8 = "1"
    $env:CBSR_BUILD_DATE = "2026-08-20"
    & $VenvPython -m tools.verify
    if ($LASTEXITCODE -ne 0) { throw "Canonical verification failed." }

    Write-Host "CBSR is ready. Start it with .\run_mcp.ps1"
    Write-Host "Evidence: $EvidencePath"
}
finally {
    Stop-Transcript | Out-Null
}
