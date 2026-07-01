# Claude SubAgents

A collection of ready-to-use [Claude Code](https://claude.com/claude-code)
subagent suites. Each suite is a self-contained set of specialized subagents
(under `.claude/agents/`) plus a `CLAUDE.md` of project-wide conventions, so you
can drop a whole team of focused agents into a new project and let Claude Code
delegate work to the right specialist.

## Suites

| Suite | Stack | What it covers |
|---|---|---|
| [CSharpWindowsFullStack](CSharpWindowsFullStack/) | C# / .NET 8 on Windows | Full-stack builds: console/CLI, WPF & WinForms, WinUI 3/MAUI, Worker/Windows Service, ASP.NET Core API, Blazor — plus data, security/auth, interop, testing, review, build/deploy |
| [DataScience](DataScience/) | Python 3.11+ | End-to-end data science: problem framing, ingestion, EDA, cleaning/validation, feature engineering, classical ML, clustering, deep learning (PyTorch), Transformer fine-tuning, time-series, RAG, evaluation, deployment, monitoring & MLOps |
| [DataScienceCopilot](DataScienceCopilot/) | Python 3.11+ | The DataScience suite ported to **GitHub Copilot** (custom agents under `.github/agents/`, prompt files, and `copilot-instructions.md`) — for VS Code Copilot or the Copilot cloud coding agent |
| [CodeReviewer](CodeReviewer/) | Language-agnostic | A read-only project-review subagent plus thin triggers (command `/review-project`, auto-invoked skill, and the agent itself) for autonomous architecture/security/maintainability audits |
| [KnowledgeBase](KnowledgeBase/) | Markdown + Python | An internal knowledge-base system: a lookup agent over a `knowledge-base/` of domain docs, plus a report-extractor that converts PDF/Word/Excel/scans into clean Markdown |
| [Grammarly](Grammarly/) | Language-agnostic | A writing-assistant toolkit: five commands/skills for fix-grammar, formalize, summarize, translate (Japanese ⇄ English, auto-detect), and expand — no agents, runs inline in the conversation |

### CSharpWindowsFullStack agents (14)

`solution-architect` · `backend-engineer` · `data-engineer` ·
`security-engineer` · `desktop-ui-engineer` · `winui-maui-engineer` ·
`windows-service-engineer` · `console-cli-engineer` · `interop-engineer` ·
`blazor-engineer` · `test-engineer` · `integration-test-engineer` ·
`build-deploy-engineer` · `code-reviewer`

### DataScience agents (22)

`problem-framer` · `data-ingestion` · `data-explorer` · `data-cleaner` ·
`data-validator` · `feature-engineer` · `stats-analyst` · `model-trainer` ·
`clustering-specialist` · `dl-trainer` · `transformer-finetuner` ·
`timeseries-specialist` · `rag-specialist` · `recommender-specialist` ·
`anomaly-detector` · `model-evaluator` · `model-deployer` · `model-monitor` ·
`viz-specialist` · `notebook-engineer` · `code-tester` · `mlops-orchestrator`

### DataScienceCopilot agents (20)

The DataScience roles in GitHub Copilot format, led by a `ds-orchestrator`:
`data-ingestion` · `data-explorer` · `data-cleaner` · `data-validator` ·
`feature-engineer` · `stats-analyst` · `model-trainer` · `dl-trainer` ·
`transformer-finetuner` · `timeseries-specialist` · `rag-specialist` ·
`recommender-specialist` · `anomaly-detector` · `model-evaluator` ·
`model-deployer` · `viz-specialist` · `notebook-engineer` · `code-tester` ·
`mlops-orchestrator`

### CodeReviewer agents (1)

`project-reviewer` — isolated context, read-only (`Read`/`Grep`/`Glob`/`Bash`),
`model: opus`. Triggered by the `/review-project` command, the auto-invoked
`project-review` skill, or by name.

### KnowledgeBase agents (2)

`kb-expert` (answers from the `knowledge-base/` index-first) ·
`report-extractor` (PDF/Word/Excel/scans → one Markdown file per report).
Commands `/kb` and `/extract`; skills `kb-lookup` and `report-extract`.

### Grammarly (no agents — 5 commands/skills)

`/fix-grammar` · `/formalize` · `/summarize` · `/translate` · `/expand`, each
paired with an auto-invoked skill of the same purpose (`fix-grammar` ·
`formalize` · `summarize` · `translate-ja-en` · `expand`). Lightweight text
transforms that run inline, no isolated-context subagent needed.

See each suite's README for the full role table, typical workflow, and usage
examples.

## Installation

Pick the suite that matches your project and copy its files in:

- `<suite>/.claude/` → your **project root** `.claude/` (agents, commands,
  skills, scripts and settings — commit to git to share with your team)
- `<suite>/CLAUDE.md` → your **project root** (global context every subagent
  reads), where the suite ships one

To make a suite's agents available across **all** your projects, copy its
`.claude/agents/` folder to `~/.claude/agents/` (your home directory) instead.

After copying files directly to disk, **restart your Claude Code session** so
they load, then run `/agents` to confirm.

> `DataScienceCopilot/` targets **GitHub Copilot** instead — copy its `.github/`
> folder (agents, prompts, `copilot-instructions.md`) to your project root.

## How it works

- **Auto-delegation** — Claude Code reads each subagent's `description` and
  routes your request to the right specialist automatically. Just describe what
  you want.
- **Manual** — name a subagent explicitly: *"Use data-engineer to add an EF Core
  migration."*
- **Chaining** — ask for a full workflow and the suite hands off stage to stage
  (e.g. architect → backend → tests → review → deploy).

Each subagent runs in its own context window, so multi-step builds don't pollute
the main conversation. `CLAUDE.md` defines project-wide rules; the per-agent
`.md` files define task-specific behavior — edit either to tune them, then run
`/agents` again to reload.

## Repository layout

```
ClaudeSubAgents/
├── CSharpWindowsFullStack/
│   ├── .claude/agents/     # 14 C# / Windows subagents
│   ├── .claude/commands/   # /scaffold-solution, /add-feature, /test-all
│   ├── CLAUDE.md           # stack, architecture & conventions
│   └── README.md
├── DataScience/
│   ├── .claude/agents/     # 22 data-science subagents (Claude Code)
│   ├── .claude/commands/   # /eda, /train-baseline, /full-pipeline, …
│   ├── CLAUDE.md           # stack, structure & conventions
│   └── README.md
├── DataScienceCopilot/
│   ├── .github/agents/     # 20 data-science custom agents (GitHub Copilot)
│   ├── .github/prompts/    # /eda, /train-baseline, /full-pipeline
│   ├── .github/copilot-instructions.md
│   └── README.md
├── CodeReviewer/
│   ├── .claude/agents/     # project-reviewer (the brain)
│   ├── .claude/commands/   # /review-project
│   ├── .claude/skills/     # project-review (auto-invoked)
│   └── README.md
├── KnowledgeBase/
│   ├── .claude/agents/     # kb-expert, report-extractor
│   ├── .claude/commands/   # /kb, /extract
│   ├── .claude/skills/     # kb-lookup, report-extract
│   ├── .claude/scripts/    # extract / rebuild-index / validate helpers
│   └── knowledge-base/     # the indexed domain docs
└── Grammarly/
    ├── .claude/commands/   # /fix-grammar, /formalize, /summarize, /translate, /expand
    ├── .claude/skills/     # fix-grammar, formalize, summarize, translate-ja-en, expand
    └── README.md
```

> Note: `CSharpWindowsFullStack/`, `DataScience/`, `CodeReviewer/`,
> `KnowledgeBase/` and `Grammarly/` target **Claude Code**;
> `DataScienceCopilot/` is the data-science suite in **GitHub Copilot** format.
