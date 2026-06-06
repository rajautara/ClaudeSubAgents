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
| [DataScience](DataScience/) | Python 3.11+ | End-to-end data science: ingestion, EDA, cleaning/validation, feature engineering, classical ML, deep learning (PyTorch), Transformer fine-tuning, time-series, RAG, evaluation, deployment & MLOps |

### CSharpWindowsFullStack agents (14)

`solution-architect` · `backend-engineer` · `data-engineer` ·
`security-engineer` · `desktop-ui-engineer` · `winui-maui-engineer` ·
`windows-service-engineer` · `console-cli-engineer` · `interop-engineer` ·
`blazor-engineer` · `test-engineer` · `integration-test-engineer` ·
`build-deploy-engineer` · `code-reviewer`

### DataScience agents (19)

`data-ingestion` · `data-explorer` · `data-cleaner` · `data-validator` ·
`feature-engineer` · `stats-analyst` · `model-trainer` · `dl-trainer` ·
`transformer-finetuner` · `timeseries-specialist` · `rag-specialist` ·
`model-evaluator` · `model-deployer` · `viz-specialist` · `notebook-engineer` ·
`code-tester` · `recommender-specialist` · `anomaly-detector` ·
`mlops-orchestrator`

See each suite's README for the full role table, typical workflow, and usage
examples.

## Installation

Pick the suite that matches your project and copy its files in:

- `<suite>/.claude/agents/` → your **project root** `.claude/agents/`
  (commit to git to share with your team)
- `<suite>/CLAUDE.md` → your **project root** (global context every subagent reads)

To make the agents available across **all** your projects, copy the
`.claude/agents/` folder to `~/.claude/agents/` (your home directory) instead.

Then run `/agents` in Claude Code to confirm they loaded.

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
│   ├── .claude/agents/   # 12 C# / Windows subagents
│   ├── CLAUDE.md         # stack, architecture & conventions
│   └── README.md
└── DataScience/
    ├── .claude/agents/   # 9 data-science subagents
    ├── CLAUDE.md         # stack, structure & conventions
    └── README.md
```
