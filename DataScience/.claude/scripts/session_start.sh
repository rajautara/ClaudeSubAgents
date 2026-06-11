#!/usr/bin/env bash
# SessionStart hook: make the project runnable in a fresh Claude Code session
# (local or on the web). Idempotent — safe to run on every session start.
set -euo pipefail

echo "[session_start] preparing data science workspace..."

# 1. Ensure the standard project structure exists.
mkdir -p data/{raw,interim,processed,clean} \
         src scripts models reports/figures notebooks tests deploy

# 2. Install dependencies if a manifest is present. Prefer uv, fall back to pip.
if command -v uv >/dev/null 2>&1; then
  if [ -f pyproject.toml ]; then
    uv sync 2>/dev/null || echo "[session_start] uv sync skipped"
  elif [ -f requirements.txt ]; then
    uv pip install -r requirements.txt 2>/dev/null || echo "[session_start] uv pip install skipped"
  fi
elif command -v pip >/dev/null 2>&1; then
  [ -f requirements.txt ] && pip install -q -r requirements.txt 2>/dev/null || true
fi

# Note: PYTHONHASHSEED=42 is set via "env" in .claude/settings.json — an export
# here would only affect this hook subprocess, not the session.

echo "[session_start] ready. Reminder: data/ is git-ignored; raw data is immutable."
