#!/usr/bin/env python
"""PreToolUse hook: block Write/Edit/NotebookEdit on files under data/raw/.

Raw data is immutable (see CLAUDE.md conventions). Claude Code calls this hook
before each file-writing tool runs, passing the tool call as JSON on stdin.
Exit code 2 blocks the tool call and feeds stderr back to the agent as the
reason; exit code 0 allows it. Works on Linux, macOS, and Windows (any Python 3).

Note: this guards the file tools. Writes that happen inside Bash-executed
Python scripts are not interceptable here — that case stays covered by the
CLAUDE.md rule and the permissions deny list.
"""
import json
import sys
from pathlib import PurePosixPath


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed/missing input -> fail open, don't break the session

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        return 0

    parts = PurePosixPath(path.replace("\\", "/")).parts
    for i in range(len(parts) - 1):
        if parts[i] == "data" and parts[i + 1] == "raw":
            sys.stderr.write(
                f"BLOCKED: '{path}' is under data/raw/, which is immutable "
                "(CLAUDE.md convention). Never modify raw data - write derived "
                "outputs to data/interim/, data/processed/ or data/clean/ "
                "instead. If you must re-land source data, use data-ingestion "
                "with a new dated/versioned filename.\n"
            )
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
