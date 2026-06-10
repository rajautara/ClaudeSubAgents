# SessionStart hook: get a .NET solution ready to work on in a fresh Claude Code
# session. Idempotent and safe to run repeatedly. PowerShell port of session_start.sh.
$ErrorActionPreference = 'Stop'

Write-Host "[session_start] preparing .NET workspace..."

$dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
if (-not $dotnet) {
    Write-Host "[session_start] dotnet SDK not found on PATH - skipping restore/build."
    exit 0
}

$version = (& dotnet --version 2>$null)
if (-not $version) { $version = '?' }
Write-Host "[session_start] dotnet $version"

# Find a solution or projects; only restore/build if something exists.
$sln = Get-ChildItem -Path . -Filter *.sln -File -ErrorAction SilentlyContinue | Select-Object -First 1
$hasProj = Get-ChildItem -Path . -Filter *.csproj -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($sln -or $hasProj) {
    $target = if ($sln) { $sln.FullName } else { $null }

    Write-Host "[session_start] restoring packages..."
    try {
        if ($target) { & dotnet restore $target } else { & dotnet restore }
    } catch { Write-Host "[session_start] restore skipped/failed" }

    Write-Host "[session_start] building (Debug)..."
    try {
        if ($target) { & dotnet build $target -c Debug --no-restore }
        else { & dotnet build -c Debug --no-restore }
    } catch {
        Write-Host "[session_start] build skipped/failed - open and fix before relying on it"
    }
} else {
    Write-Host "[session_start] no .sln/.csproj yet - ask solution-architect to scaffold one."
}

Write-Host "[session_start] ready. Reminder: no secrets in source; use 'dotnet user-secrets' for dev."
