---
name: project-review
description: >-
  Comprehensive autonomous project/system review. Triggers when the user wants to
  review, audit, assess, critique, sanity-check, or do technical due diligence on a
  codebase, app, system, or project — including questions like "is this well built",
  "what are the risks", "how maintainable is this", or "review my project". Discovers
  the project's purpose, stack, and stage automatically, then evaluates architecture,
  code quality, security, performance, maintainability, extensibility, devops, risk,
  and strategy, ending with a verdict and prioritized roadmap. Read-only.
---

# Project Review

When this skill is invoked, delegate the work to the **project-reviewer** subagent so the heavy multi-file reading happens in an isolated context and the main session stays clean.

Instruction to issue:

> Use the project-reviewer subagent to run a full autonomous review of this project. It should self-discover purpose, stack, and stage, then review all 10 dimensions and return the report with a verdict and prioritized roadmap. Read-only — do not modify any files.

If the user named a specific area, pass it through (e.g. "focus on the API layer" or "security only").

If the `project-reviewer` subagent does not exist in this environment, run the review inline yourself using the same protocol: **Phase 0 discovery → Project Understanding Brief → 10-dimension review → verdict + roadmap**, evidence-first, calibrated to the project's stage, and never modifying files. See `reference.md` for the full protocol.
