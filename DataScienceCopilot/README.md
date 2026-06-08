# Data Science Custom Agents — GitHub Copilot (Python Stack)

A set of **GitHub Copilot** custom agents for an end-to-end data science
workflow. This is the Copilot port of the [`DataScience/`](../DataScience)
Claude Code suite — same 19 roles, same prompts, in Copilot's file format.

## Installation

Copy these into your project:
- `.github/agents/` -> your **project root** `.github/agents/` (committed, shared
  with the team). Copilot picks these up automatically.
- `.github/prompts/` -> prompt files you invoke in chat (`/eda`,
  `/train-baseline`, `/full-pipeline`).
- `.github/copilot-instructions.md` -> your **project root** `.github/`
  (global, project-wide context Copilot reads for every chat).
- `.devcontainer/` + `scripts/` -> optional: auto-creates the folder structure
  and installs deps in Codespaces / Dev Containers.

Then open **Copilot Chat** in VS Code and open the agent picker — the 19 agents
should be listed.

> **Compatibility:** the current format is `.github/agents/*.agent.md` (custom
> agents), which also works with the GitHub Copilot **cloud coding agent**. Older
> VS Code builds called these "custom chat modes" and used
> `.github/chatmodes/*.chatmode.md` — the body is identical, just rename the files
> and folder if you are on an older VS Code.

## Agents & roles

| Agent | When to use | Focus |
|---|---|---|
| `ds-orchestrator` | Want one agent to drive everything | **Coordinator** — auto-delegates each stage to the specialists below |
| `data-ingestion` | Need to pull source data | Step 0: SQL/API/cloud/files -> immutable `data/raw/` |
| `data-explorer` | New dataset | EDA, profiling, missing values, correlation |
| `data-cleaner` | After EDA | Impute, dedup, fix dtypes, standardize, **create held-out split** |
| `data-validator` | Guard data quality | Schema/contracts (pandera/GE), drift detection |
| `feature-engineer` | Data is clean | Encoding, scaling, feature creation/selection |
| `stats-analyst` | Inference, not prediction | Hypothesis tests, A/B testing, power, causal |
| `model-trainer` | Features ready | Classical ML: baseline + tune (sklearn/xgb/lgbm/catboost) |
| `dl-trainer` | Deep learning task | PyTorch NN (MLP/CNN/RNN/Transformer), auto-GPU |
| `transformer-finetuner` | Fine-tune an LLM/NLP model | HuggingFace transformers, LoRA/QLoRA, auto-GPU |
| `timeseries-specialist` | Temporal / forecasting data | ARIMA/Prophet/sktime, temporal CV, lag features |
| `rag-specialist` | RAG / semantic search | Chunking, embeddings, vector DB, retrieval eval |
| `recommender-specialist` | Personalization / ranking | CF, content-based, matrix factorization, ranking metrics |
| `anomaly-detector` | Rare-event / fraud / faults | IsolationForest/LOF/OC-SVM/autoencoder, scarce labels |
| `model-evaluator` | After training | Metrics, error analysis, SHAP, validation |
| `model-deployer` | Ship an evaluated model | FastAPI/ONNX/Docker, batch & online inference |
| `viz-specialist` | Whenever a plot is needed | Visualization (matplotlib/seaborn/plotly) |
| `notebook-engineer` | Refactor/setup | Reproducibility, project structure, notebook hygiene |
| `code-tester` | After logic moves to `src/` | pytest unit tests, fixtures, determinism, edge cases |
| `mlops-orchestrator` | Automate & version the pipeline | DVC/Makefile, MLflow/W&B, model registry, CI |

## Typical workflow

```
data-ingestion -> data-explorer -> data-cleaner -> data-validator -> feature-engineer -> [ model-trainer
   (-> data/raw/)                (+ held-out split)   (schema)        (build Pipeline)     | dl-trainer
                                                                                          | transformer-finetuner
                                                                                          | timeseries-specialist ]
                                                                                                  |
                                                                                                  v
                                                                              model-evaluator -> model-deployer
                                            ^                                                          (serve)
                                   viz-specialist (used whenever a plot is needed)
notebook-engineer (project structure & reproducibility) · code-tester (tests for src/)
stats-analyst (inference / A-B testing) · rag-specialist (retrieval-augmented LLM apps)
```

The held-out test split is created once by `data-cleaner` (before feature
engineering) and evaluated exactly once at the end by `model-evaluator`.
`feature-engineer` builds a Pipeline fit on the train set only, so no leakage
occurs during cross-validation.

## How to use

**Pick an agent** — open Copilot Chat, click the agent picker, and choose the
agent that matches your task. Then describe what you want:
> "Profile the dataset sales.csv"  (with **data-explorer** selected)

> "Encode the category column and scale the numericals."  (with **feature-engineer** selected)

**Prompt files** (in `.github/prompts/`) — type these in Copilot Chat:
> `/eda` — profile a dataset (pairs with `data-explorer`)
> `/train-baseline` — an honest baseline (pairs with `model-trainer`)
> `/full-pipeline` — walk the whole workflow end to end

Each prompt asks for its inputs (dataset path, target column, …) inline.

**Deep learning / fine-tuning:**
> Select **dl-trainer** and ask: "Build a CNN for this image dataset."
> Select **transformer-finetuner** and ask: "LoRA fine-tune a BERT model for text classification."

## Auto-delegation: the `ds-orchestrator` agent

Don't want to pick a specialist by hand for every step? Select the single
**`ds-orchestrator`** agent and describe your goal — it plans the task and
**automatically delegates each stage to the right specialist** (the same
auto-routing you get from Claude Code), then reports back:

> Select **ds-orchestrator** and ask:
> "Run the full pipeline on data/raw/sales.csv to predict churn."

It will, on its own, call `data-explorer` → `data-cleaner` → `feature-engineer`
→ `model-trainer` → `model-evaluator` (and `viz-specialist` whenever a plot is
needed), passing artifacts forward between them.

**Requirements (VS Code, GitHub Copilot multi-agent — shipped June 2026):**
- The orchestrator uses the **`agent` / `runSubagent`** tool (already set in its
  frontmatter) to spin up specialists; make sure subagents are enabled in your
  Copilot settings.
- Its `agents:` frontmatter lists exactly the 19 specialists it may delegate to,
  so it won't wander off to a generic coding agent.
- On older Copilot builds without subagent support, fall back to picking agents
  manually (below) or use the `/full-pipeline` prompt.

## Differences vs the Claude Code version

This port is faithful to the role prompts, but Copilot and Claude Code differ in
a few mechanics — worth knowing:

- **Delegation.** Claude Code auto-routes to the right subagent from its
  `description`. In Copilot you either pick the agent yourself from the picker, or
  select **`ds-orchestrator`** (above) to get the same automatic delegation.
- **No separate context window per agent.** Claude subagents each run in an
  isolated context; Copilot agents share the chat session's context.
- **`model` is not pinned.** The Claude version pins `sonnet` for reasoning-heavy
  agents and `haiku` for light ones (`viz-specialist`, `notebook-engineer`) to
  save cost. Copilot model names vary per plan, so the agent files leave `model`
  out. To replicate the intent, set a strong model for the reasoning-heavy agents
  and a faster/cheaper one for `viz-specialist` and `notebook-engineer` via the
  model picker (or add a `model:` line to the frontmatter if your IDE supports it).
- **Setup is a devcontainer, not a SessionStart hook.** Claude runs
  `session_start.sh` on every session; here `scripts/setup.sh` runs via the
  devcontainer `postCreateCommand`, or you run it manually once.

## Notes

- `.github/copilot-instructions.md` holds global, project-wide context (stack,
  structure, conventions). Each agent `.agent.md` holds task-specific behavior.
  They complement each other.
- Edit any `.agent.md` to tweak behavior — change the `tools` array to limit
  access (e.g. remove `runCommands` from an agent that should not run code, or set
  `tools: []` to disable all tools).
- Add more agents as your stack needs (e.g. `geospatial-specialist`,
  `causal-inference-specialist`, `llm-eval-specialist`).
