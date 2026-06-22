# Project Review — Claude Code Setup

Three ways to trigger the same review, all sharing one brain (the `project-reviewer` subagent).

## Structure
```
.claude/
├── agents/
│   └── project-reviewer.md      # THE BRAIN: isolated context, read-only, model: opus
├── commands/
│   └── review-project.md        # Trigger: /review-project [focus]
└── skills/
    └── project-review/
        ├── SKILL.md             # Auto-invocable trigger; delegates to the subagent
        └── reference.md         # Full protocol (fallback when the subagent is absent)
```

## Installation
Copy the `.claude/` folder to your **project root** (project scope — commit it to git to share with your team):
```
cp -r .claude /path/to/your-project/
```
Or place it in `~/.claude/` (user scope) to use it across **all** projects.
After copying, **restart your Claude Code session** so the files are loaded (agents/skills added directly to disk require a restart).

## When to use which

| Format | How it triggers | When to use |
|---|---|---|
| **Command** `/review-project` | Typed explicitly | When you want a review right now, with full control. Pass a focus: `/review-project src/api` or `/review-project security only` |
| **Skill** `project-review` | Auto, when Claude detects the intent ("review my project", "is this well built") | When you want Claude to decide when to use it, without remembering a command name |
| **Agent** `project-reviewer` | Called by the command/skill, or explicitly: "use the project-reviewer subagent" | The actual brain — don't delete it. Isolated context keeps the main session clean |

## Why a subagent + thin triggers?
- A review reads many files → if it runs in the main session, your context fills with raw output and answer quality degrades.
- The subagent runs in its own context window, reads everything, and returns **only the final report** to the main session.
- `tools: Read, Grep, Glob, Bash` only (no Write/Edit) = a genuine read-only audit at the tooling level.
- `model: opus` because strategic review needs deep reasoning. Switch to `sonnet` for cheaper/faster runs.

## Tips
- **Repeat review:** attach the previous report and add: "Compare against the previous review — what improved, regressed, or remains open?"
- **Multi-agent cross-check:** run it on Opus and Sonnet, then compare. Findings that appear in both are usually the most reliable.
- **For your trading/EA projects:** the security section already includes an idempotency + replay-protection checklist for order execution — keep it.
- **100% no-questions mode:** in `project-reviewer.md`, change the Phase 0.6 line to "Never ask questions; proceed with best inference and mark all assumptions."
