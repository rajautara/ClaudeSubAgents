# SessionStart hook: make the project runnable in a fresh Claude Code session.
# Idempotent - safe to run on every session start. PowerShell port of session_start.sh.
$ErrorActionPreference = 'Stop'

Write-Host "[session_start] preparing data science workspace..."

# 1. Ensure the standard project structure exists.
$dirs = @(
    'data/raw', 'data/interim', 'data/processed', 'data/clean',
    'src', 'scripts', 'models', 'reports/figures', 'notebooks', 'tests', 'deploy'
)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

# 2. Install dependencies if a manifest is present. Prefer uv, fall back to pip.
if (Get-Command uv -ErrorAction SilentlyContinue) {
    if (Test-Path pyproject.toml) {
        try { & uv sync } catch { Write-Host "[session_start] uv sync skipped" }
    } elseif (Test-Path requirements.txt) {
        try { & uv pip install -r requirements.txt } catch { Write-Host "[session_start] uv pip install skipped" }
    }
} elseif (Get-Command pip -ErrorAction SilentlyContinue) {
    if (Test-Path requirements.txt) {
        try { & pip install -q -r requirements.txt } catch {}
    }
}

# 3. Reproducibility: pin a default seed for any tooling that reads it.
$env:PYTHONHASHSEED = '42'

Write-Host "[session_start] ready. Reminder: data/ is git-ignored; raw data is immutable."
