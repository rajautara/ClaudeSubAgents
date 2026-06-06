# Data Science Subagents (Python Stack)

A set of Claude Code subagents for an end-to-end data science workflow.

## Installation

Copy these into your project:
- `.claude/agents/` -> your **project root** `.claude/agents/` (shared with the team, committed to git)
- `.claude/commands/` -> slash commands (`/eda`, `/train-baseline`, `/full-pipeline`)
- `.claude/settings.json` + `.claude/scripts/` -> SessionStart hook that sets up the
  folder structure and installs deps so a fresh session is ready to run
- `CLAUDE.md` -> your **project root** (global context all subagents read)

Or, to use the agents across every project, copy `.claude/agents/` to
`~/.claude/agents/` (your home directory) instead.

Then in Claude Code, run `/agents` to confirm they all loaded.

## Subagents & roles

| Subagent | When to use | Focus |
|---|---|---|
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
                                   viz-specialist (called whenever a plot is needed)
notebook-engineer (project structure & reproducibility) · code-tester (tests for src/)
stats-analyst (inference / A-B testing) · rag-specialist (retrieval-augmented LLM apps)
```

The held-out test split is created once by `data-cleaner` (before feature
engineering) and evaluated exactly once at the end by `model-evaluator`.
`feature-engineer` builds a Pipeline fit on the train set only, so no leakage
occurs during cross-validation.

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

## Notes

- Each subagent has its own separate context window — it does not pollute the main conversation. Great for long pipelines.
- `CLAUDE.md` holds global, project-wide context (stack, structure, conventions). Subagent `.md` files hold task-specific behavior. They complement each other.
- Edit any `.md` to tweak behavior — change the `tools` field to limit access (e.g. remove `Bash` from a subagent that should not run code).
- Each subagent pins a `model` in its frontmatter: heavier reasoning agents use `sonnet`, lighter mechanical ones (`viz-specialist`, `notebook-engineer`) use `haiku` to save cost. Change to `opus` or `inherit` as you prefer.
- Add more subagents as your stack needs (e.g. `geospatial-specialist`, `causal-inference-specialist`, `llm-eval-specialist`).
- After editing agent files mid-session, run `/agents` again (or start a fresh session) to reload.
