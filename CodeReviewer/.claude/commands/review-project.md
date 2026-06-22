---
description: Run a full autonomous principal-architect review of this project (delegates to the project-reviewer subagent, isolated context, read-only).
argument-hint: "[optional: path or area to focus on, e.g. src/api or 'security only']"
---

Use the **project-reviewer** subagent to perform a comprehensive, autonomous review of this project.

The subagent will discover the project's purpose, stack, and stage on its own, then review across all 10 dimensions (concept, architecture, code quality, security, performance, maintainability, extensibility, devops, risk, strategy) and return a full report with a verdict and prioritized roadmap.

Focus / scope for this run (if any): $ARGUMENTS

If no focus is given, review the whole project. Remember: this is a read-only audit — the subagent must not modify any files.
