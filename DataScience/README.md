# Data Science Subagents (Python Stack)

A set of Claude Code subagents for an end-to-end data science workflow.

## Installation

Copy these into your project:
- `.claude/agents/` -> your **project root** `.claude/agents/` (shared with the team, committed to git)
- `.claude/commands/` -> slash commands (`/eda`, `/train-baseline`, `/full-pipeline`,
  `/evaluate`, `/compare-models`, `/report`)
- `.claude/settings.json` + `.claude/scripts/` -> hooks & permissions:
  - SessionStart hook (cross-platform: `.sh` on Linux/macOS, `.ps1` on Windows)
    that sets up the folder structure and installs deps
  - PreToolUse hook (`protect_raw.py`) + permission deny rules that **block any
    edit to `data/raw/`** — raw-data immutability is enforced, not just stated
  - a permission allowlist (python/pytest/uv/pip/dvc/mlflow) so long pipelines
    run with fewer permission prompts
- `CLAUDE.md` -> your **project root** (global context all subagents read)

Or, to use the agents across every project, copy `.claude/agents/` to
`~/.claude/agents/` (your home directory) instead.

Then in Claude Code, run `/agents` to confirm they all loaded.

## Project structure (prepare this before running the subagents)

The subagents assume the layout below. The **SessionStart hook**
(`.claude/scripts/session_start.{sh,ps1}`) creates these folders automatically on
every fresh session, so normally you don't create them by hand — but this is where
each kind of file belongs:

```
.
├── data/                 # ALL datasets live here (git-ignored)
│   ├── raw/              # ← put your source dataset here (immutable, never edit)
│   ├── interim/          # intermediate transformed data
│   ├── processed/        # final data ready for modeling
│   └── clean/            # cleaned outputs from data-cleaner (+ held-out split)
├── src/                  # reusable, importable, testable modules
├── scripts/              # runnable scripts / pipelines (training, eval, one-off jobs)
├── notebooks/            # exploration only — logic graduates to src/
├── models/              # saved models, checkpoints, adapters
├── reports/             # written reports & decisions (audit trail)
│   └── figures/         # saved plots
├── tests/               # pytest tests for graduated src/ modules
├── deploy/              # serving artifacts (FastAPI/ONNX/Docker)
├── CLAUDE.md            # global context all subagents read
└── .claude/
    ├── agents/          # the subagent definitions
    ├── commands/        # /eda, /train-baseline, /full-pipeline, /evaluate, /compare-models, /report
    └── scripts/         # SessionStart hook + protect_raw.py (raw-data guard)
```

**Where do I put my dataset?** Drop your source files in **`data/raw/`** — this is
the immutable input every pipeline reads from (e.g. `data/raw/sales.csv`). The
subagents write derived data to `data/interim/`, `data/processed/`, and
`data/clean/`; never edit `data/raw/` by hand.

> If you are **not** using the SessionStart hook (e.g. you only copied the
> `.claude/agents/`), create at least `data/raw/` yourself and put your dataset
> there before invoking a subagent. The other folders are created on demand.

Notes:
- `data/` and large model artifacts should be **git-ignored**; commit code,
  metadata, and pointers (DVC/MLflow), not the data blobs.
- Generated code is never left only in the chat — subagents write it to a file:
  reusable logic → `src/`, runnable pipelines → `scripts/`, exploration →
  `notebooks/` (see Conventions in `CLAUDE.md`).

## Subagents & roles

| Subagent | When to use | Focus |
|---|---|---|
| `problem-framer` | START of a project | Business objective -> DS problem, metrics, cost of errors (charter) |
| `data-ingestion` | Need to pull source data | Step 0: SQL/API/cloud/files -> immutable `data/raw/` |
| `data-explorer` | New dataset | EDA, profiling, missing values, target profile, correlation |
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
| `clustering-specialist` | Segmentation, no labels | KMeans/HDBSCAN/GMM, PCA/UMAP, cluster profiling |
| `model-evaluator` | After training | Metrics, error analysis, SHAP, threshold tuning, model card |
| `model-deployer` | Ship an evaluated model | FastAPI/ONNX/Docker, batch & online inference |
| `model-monitor` | After deployment | Drift, performance decay, alerting, retraining triggers |
| `viz-specialist` | Whenever a plot is needed | Visualization (matplotlib/seaborn/plotly) |
| `notebook-engineer` | Refactor/setup | Reproducibility, project structure, notebook hygiene |
| `code-tester` | After logic moves to `src/` | pytest unit tests, fixtures, determinism, edge cases |
| `mlops-orchestrator` | Automate & version the pipeline | DVC/Makefile, MLflow/W&B, model registry, CI |

## Typical workflow

```
problem-framer -> data-ingestion -> data-explorer -> data-cleaner -> data-validator -> feature-engineer
   (charter)        (-> data/raw/)                  (+ held-out split)   (schema)       (build Pipeline)
                                                                                                |
                                       [ model-trainer | dl-trainer | transformer-finetuner    v
                                         | timeseries-specialist ] -> model-evaluator -> model-deployer -> model-monitor
                                                                   (+ threshold, model card)    (serve)     (drift/decay)
                                   viz-specialist (called whenever a plot is needed)
notebook-engineer (project structure & reproducibility) · code-tester (tests for src/)
stats-analyst (inference / A-B testing) · rag-specialist (RAG apps) · clustering-specialist (segmentation)
```

The held-out test split is created once by `data-cleaner` (before feature
engineering) and evaluated exactly once at the end by `model-evaluator`.
`feature-engineer` builds a Pipeline fit on the train set only, so no leakage
occurs during cross-validation.

Handoff convention: agents pass work through `reports/` — each agent reads the
upstream reports it depends on (EDA report, cleaning log, problem charter), so
the audit trail doubles as the contract between stages.

## How to use

**Auto-delegation** — Claude Code picks the right subagent based on its `description`. Just say:
> "Profile the dataset sales.csv"  ->  `data-explorer` is invoked automatically.

**Manual** — name the subagent:
> "Use feature-engineer to encode the category column and scale the numericals."

**Chaining** — ask for the full workflow:
> "Run the full pipeline: explore, clean, engineer features, train a baseline + xgboost, then evaluate."

**Deep learning / fine-tuning:**
> "Use dl-trainer to build a CNN for this image dataset."
> "Use transformer-finetuner to LoRA fine-tune a BERT model for text classification."

**Slash commands** (in `.claude/commands/`):
> `/eda data/raw/sales.csv` — profile a dataset via `data-explorer`
> `/train-baseline price regression` — honest baseline via `model-trainer`
> `/full-pipeline data/raw/sales.csv churn` — chain the whole workflow end to end
> `/evaluate` — evaluate the latest model: metrics, threshold, model card
> `/compare-models` — leaderboard of all runs from `reports/experiments.md`
> `/report exec` — stakeholder-facing (non-technical) project summary

## Notes

- Each subagent has its own separate context window — it does not pollute the main conversation. Great for long pipelines.
- `CLAUDE.md` holds global, project-wide context (stack, structure, conventions). Subagent `.md` files hold task-specific behavior. They complement each other.
- Edit any `.md` to tweak behavior — change the `tools` field to limit access (e.g. remove `Bash` from a subagent that should not run code).
- Each subagent pins a `model` in its frontmatter: heavier reasoning agents use `sonnet`; `viz-specialist` uses `haiku` to save cost. Change to `opus` or `inherit` as you prefer.
- Raw-data immutability is enforced two ways in `.claude/settings.json`: permission `deny` rules for `Write/Edit(data/raw/**)` and a PreToolUse hook (`.claude/scripts/protect_raw.py`) that blocks the call with an explanation. Writes made inside Bash-run Python scripts can't be intercepted — that case is covered by the CLAUDE.md convention.
- Add more subagents as your stack needs (e.g. `geospatial-specialist`, `causal-inference-specialist`, `llm-eval-specialist`).
- After editing agent files mid-session, run `/agents` again (or start a fresh session) to reload.
