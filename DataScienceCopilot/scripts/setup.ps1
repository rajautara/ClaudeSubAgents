# Environment setup: make the project runnable on a Windows host (no container).
# The devcontainer uses scripts/setup.sh (Linux); use this when running directly
# on Windows: powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
# Idempotent - safe to run repeatedly.
$ErrorActionPreference = 'Stop'

Write-Host "[setup] preparing data science workspace..."

# 1. Ensure the standard project structure exists.
$dirs = @(
    'data/raw', 'data/interim', 'data/processed', 'data/clean',
    'src', 'models', 'reports/figures', 'notebooks', 'tests', 'deploy'
)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

# 2. Install dependencies if a manifest is present. Prefer uv, fall back to pip.
if (Get-Command uv -ErrorAction SilentlyContinue) {
    if (Test-Path pyproject.toml) {
        try { & uv sync } catch { Write-Host "[setup] uv sync skipped" }
    } elseif (Test-Path requirements.txt) {
        try { & uv pip install -r requirements.txt } catch { Write-Host "[setup] uv pip install skipped" }
    }
} elseif (Get-Command pip -ErrorAction SilentlyContinue) {
    if (Test-Path requirements.txt) {
        try { & pip install -q -r requirements.txt } catch {}
    }
}

# 3. Reproducibility: pin a default seed for any tooling that reads it.
$env:PYTHONHASHSEED = '42'

Write-Host "[setup] ready. Reminder: data/ is git-ignored; raw data is immutable."
