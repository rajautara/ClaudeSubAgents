#!/usr/bin/env bash
# SessionStart hook: get a .NET solution ready to work on in a fresh Claude Code
# session (local or on the web). Idempotent and safe to run repeatedly.
set -euo pipefail

echo "[session_start] preparing .NET workspace..."

if ! command -v dotnet >/dev/null 2>&1; then
  echo "[session_start] dotnet SDK not found on PATH — skipping restore/build."
  exit 0
fi

echo "[session_start] dotnet $(dotnet --version 2>/dev/null || echo '?')"

# Find a solution or projects; only restore/build if something exists.
sln="$(ls ./*.sln 2>/dev/null | head -n1 || true)"
if [ -n "$sln" ] || ls ./**/*.csproj >/dev/null 2>&1; then
  echo "[session_start] restoring packages..."
  dotnet restore ${sln:+"$sln"} 2>/dev/null || echo "[session_start] restore skipped/failed"
  echo "[session_start] building (Debug)..."
  dotnet build ${sln:+"$sln"} -c Debug --no-restore 2>/dev/null \
    || echo "[session_start] build skipped/failed — open and fix before relying on it"
else
  echo "[session_start] no .sln/.csproj yet — ask solution-architect to scaffold one."
fi

echo "[session_start] ready. Reminder: no secrets in source; use 'dotnet user-secrets' for dev."
