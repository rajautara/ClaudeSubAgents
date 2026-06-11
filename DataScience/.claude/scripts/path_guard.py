#!/usr/bin/env python
"""PreToolUse hook: keep the project layout clean.

Claude Code calls this hook before each Write/Edit/NotebookEdit, passing the
tool call as JSON on stdin. Exit code 2 blocks the call and feeds stderr back
to the agent as the reason; exit 0 allows it. Works on Linux, macOS, and
Windows (any Python 3).

Guards two CLAUDE.md conventions:
1. data/raw/ is immutable - no writes/edits ever.
2. The project root stays clean - no .py/.ipynb files at the root; code
   belongs in src/, scripts/, tests/, or notebooks/ (scratch -> scripts/tmp/).

Note: this guards the file tools. Writes that happen inside Bash-executed
Python scripts are not interceptable here — that case stays covered by the
CLAUDE.md rules and the permissions deny list.
"""
import json
import os
import sys
from pathlib import PurePosixPath

ROOT_ALLOWED = {"setup.py"}  # legacy packaging entry point


def _normalized(path: str) -> PurePosixPath:
    return PurePosixPath(path.replace("\\", "/"))


def _is_under_data_raw(p: PurePosixPath) -> bool:
    parts = p.parts
    return any(
        parts[i] == "data" and parts[i + 1] == "raw"
        for i in range(len(parts) - 1)
    )


def _is_code_file_at_project_root(p: PurePosixPath) -> bool:
    if p.suffix not in (".py", ".ipynb") or p.name in ROOT_ALLOWED:
        return False
    # Relative path with no directory component -> resolves to the cwd root.
    if not p.is_absolute() and len(p.parts) == 1:
        return True
    # Parent directory is exactly the project root.
    root = os.environ.get("CLAUDE_PROJECT_DIR", "").replace("\\", "/").rstrip("/")
    return bool(root) and str(p.parent).rstrip("/") == root


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed/missing input -> fail open, don't break the session

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        return 0

    p = _normalized(path)

    if _is_under_data_raw(p):
        sys.stderr.write(
            f"BLOCKED: '{path}' is under data/raw/, which is immutable "
            "(CLAUDE.md convention). Never modify raw data - write derived "
            "outputs to data/interim/, data/processed/ or data/clean/ "
            "instead. If you must re-land source data, use data-ingestion "
            "with a new dated/versioned filename.\n"
        )
        return 2

    if _is_code_file_at_project_root(p):
        sys.stderr.write(
            f"BLOCKED: '{path}' would create a code file in the project root. "
            "Keep the root clean (CLAUDE.md convention): reusable modules -> "
            "src/, runnable scripts -> scripts/, tests -> tests/, notebooks -> "
            "notebooks/. For throwaway/diagnostic scripts use scripts/tmp/ "
            "(git-ignored) and delete them when done - or run the check inline "
            "with `python -c` without creating a file at all.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
