# CLAUDE.md

Global context for this data science project. All subagents and chat sessions
should follow these conventions. (Subagent `.md` files in `.claude/agents/`
define task-specific behavior; this file defines project-wide defaults.)

## Stack
- Language: Python 3.11+
- Core: pandas / polars, numpy, scikit-learn
- Gradient boosting: xgboost, lightgbm, catboost
- Deep learning: PyTorch (use GPU automatically: cuda > mps > cpu)
- Transformers / NLP: HuggingFace transformers, datasets, peft, accelerate
- Viz: matplotlib, seaborn, plotly
- Experiment tracking: MLflow or Weights & Biases (if configured)
- Env management: prefer `uv` or `conda`; pin versions

## Project structure
```
data/
  raw/         # immutable source data — never edit
  interim/     # intermediate transformed data
  processed/   # final data ready for modeling
  clean/       # cleaned outputs from data-cleaner
src/           # reusable modules (importable, testable)
scripts/       # runnable scripts / pipelines (training, eval, one-off jobs)
notebooks/     # exploration only — logic graduates to src/
models/        # saved models, checkpoints, adapters
reports/       # written reports
  figures/     # saved plots
```

## Conventions
- NEVER modify files in `data/raw/`. Treat raw data as immutable.
- Set `random_state` / seeds everywhere (target seed: 42) for reproducibility.
- No data leakage: fit any transformer/scaler/encoder on the TRAIN set only;
  wrap preprocessing + model in a single Pipeline so leakage cannot occur in CV.
- Split ownership: the held-out train/test split is created once by `data-cleaner`,
  immediately after cleaning and BEFORE feature engineering. `feature-engineer` builds
  the Pipeline (fit on train only); `model-trainer` does CV within the train set.
- The test set is held out and evaluated exactly once, at the very end (by `model-evaluator`).
- Always train a simple baseline before complex models; complex models must beat it.
- Choose metrics appropriate to the problem (avoid plain accuracy on imbalanced data).
- Use relative paths via pathlib; do not hardcode absolute paths.
- Log experiments and decisions to `reports/` so there is an audit trail.
- Code placement (ALL subagents): never leave generated code living only in the
  chat response — always write it to a file in the repo so work is reproducible.
  - Reusable / importable / testable logic -> `src/` (as a module).
  - Exploration & throwaway analysis -> `notebooks/`; once stable, graduate it to `src/`.
  - Runnable scripts & pipelines (training, evaluation, one-off jobs) -> `scripts/`.
  - Tests for graduated `src/` modules -> `tests/` (owned by `code-tester`).

## Hardware
- Use GPU automatically when available; fall back gracefully to CPU.
- On out-of-memory: reduce batch size, use gradient accumulation / checkpointing,
  or switch to QLoRA for large Transformer fine-tunes.

## Subagents (in .claude/agents/)
- `problem-framer` — frame the business problem BEFORE any data work (charter)
- `data-ingestion` — pull raw data from SQL/API/cloud/files into data/raw/ (step 0)
- `data-explorer` — EDA & profiling
- `data-cleaner` — cleaning & preprocessing (+ owns the held-out split)
- `data-validator` — schema/contracts & drift detection (pandera/Great Expectations)
- `feature-engineer` — encoding, scaling, feature creation/selection
- `stats-analyst` — hypothesis testing, A/B tests, power, causal inference (non-ML)
- `model-trainer` — classical ML (sklearn/xgb/lgbm/catboost)
- `dl-trainer` — PyTorch neural networks (auto-GPU)
- `transformer-finetuner` — fine-tune HuggingFace Transformers (LoRA/QLoRA)
- `timeseries-specialist` — forecasting (ARIMA/Prophet/sktime), temporal CV
- `rag-specialist` — RAG / semantic search (chunking, embeddings, vector DB)
- `model-evaluator` — metrics, error analysis, SHAP, threshold tuning, model card
- `model-deployer` — package model for serving (FastAPI/ONNX/Docker)
- `model-monitor` — post-deployment monitoring: drift, decay, retraining triggers
- `recommender-specialist` — recommender systems (CF, content-based, matrix factorization)
- `anomaly-detector` — outlier/novelty detection (IsolationForest/LOF/OC-SVM/autoencoder)
- `clustering-specialist` — unsupervised segmentation (KMeans/HDBSCAN/GMM, PCA/UMAP)
- `viz-specialist` — plots (matplotlib/seaborn/plotly)
- `notebook-engineer` — reproducibility & project structure
- `code-tester` — pytest for graduated src/ modules
- `mlops-orchestrator` — reproducible pipelines, tracking, registry, CI (DVC/MLflow)

Typical flow:
frame (problem charter) -> ingest -> explore -> clean (+ create held-out split)
-> validate (schema) -> engineer (build Pipeline) -> train (model-trainer |
dl-trainer | transformer-finetuner | timeseries-specialist) -> evaluate
(+ threshold + model card) -> deploy -> monitor (drift/decay/retraining),
with viz-specialist called whenever a plot is needed, code-tester covering
src/ modules, and notebook-engineer supporting structure & reproducibility.
Use stats-analyst for inference/experiment questions, rag-specialist for
retrieval-augmented LLM apps, clustering-specialist for unsupervised
segmentation.

Handoff convention: each agent reads the upstream reports it depends on
(e.g. data-cleaner reads the EDA report; model-evaluator reads the problem
charter for the success bar and cost of errors) — the `reports/` folder is
the contract between stages, not just an archive.

## Experiment tracking & data versioning
- Track experiments with MLflow or Weights & Biases when configured: log params,
  metrics, and artifacts per run; reference the run id in `reports/`.
- Version data & pipelines with DVC (or lakeFS) so a model is reproducible from a
  known data snapshot + code commit. Record the data version with every model.
- `.gitignore` `data/` and large artifacts; commit metadata/pointers, not blobs.

## Automation & enforcement
- A SessionStart hook (`.claude/settings.json` -> `session_start.sh` on
  Linux/macOS, `session_start.ps1` on Windows) creates the folder structure and
  installs deps so a fresh session is ready to run.
- Raw-data immutability is ENFORCED, not just stated: a PreToolUse hook
  (`.claude/scripts/protect_raw.py`) plus permission deny rules block any
  Write/Edit under `data/raw/`. Write derived data elsewhere.
- `PYTHONHASHSEED=42` is set session-wide via `env` in `.claude/settings.json`.
- Common DS commands (python, pytest, uv, pip install, dvc, mlflow) are
  pre-allowed in `.claude/settings.json` to reduce permission prompts.
- Slash commands in `.claude/commands/`: `/eda`, `/train-baseline`,
  `/full-pipeline`, `/evaluate`, `/compare-models`, `/report`.
