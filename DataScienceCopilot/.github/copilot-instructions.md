# Copilot instructions

Global context for this data science project. GitHub Copilot reads this file
automatically for every chat and agent in this repository. (Custom agent files in
`.github/agents/` define task-specific behavior; this file defines project-wide
defaults.)

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

## Hardware
- Use GPU automatically when available; fall back gracefully to CPU.
- On out-of-memory: reduce batch size, use gradient accumulation / checkpointing,
  or switch to QLoRA for large Transformer fine-tunes.

## Custom agents (in .github/agents/)
Pick the right agent from the Copilot Chat agent picker for each task — OR select
the single `ds-orchestrator` agent, which auto-delegates each stage to the
specialists below (via the `agent`/`runSubagent` tool), the same way Claude Code
routes work automatically.
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
- `model-evaluator` — metrics, error analysis, SHAP, validation
- `model-deployer` — package model for serving (FastAPI/ONNX/Docker)
- `recommender-specialist` — recommender systems (CF, content-based, matrix factorization)
- `anomaly-detector` — outlier/novelty detection (IsolationForest/LOF/OC-SVM/autoencoder)
- `viz-specialist` — plots (matplotlib/seaborn/plotly)
- `notebook-engineer` — reproducibility & project structure
- `code-tester` — pytest for graduated src/ modules
- `mlops-orchestrator` — reproducible pipelines, tracking, registry, CI (DVC/MLflow)

Typical flow:
ingest -> explore -> clean (+ create held-out split) -> validate (schema)
-> engineer (build Pipeline) -> train (model-trainer | dl-trainer |
transformer-finetuner | timeseries-specialist) -> evaluate -> deploy,
with viz-specialist used whenever a plot is needed, code-tester covering
src/ modules, and notebook-engineer supporting structure & reproducibility.
Use stats-analyst for inference/experiment questions, rag-specialist for
retrieval-augmented LLM apps.

## Experiment tracking & data versioning
- Track experiments with MLflow or Weights & Biases when configured: log params,
  metrics, and artifacts per run; reference the run id in `reports/`.
- Version data & pipelines with DVC (or lakeFS) so a model is reproducible from a
  known data snapshot + code commit. Record the data version with every model.
- `.gitignore` `data/` and large artifacts; commit metadata/pointers, not blobs.

## Automation
- Environment setup lives in `scripts/setup.sh` (creates the folder structure and
  installs deps). It runs automatically via `.devcontainer/devcontainer.json`
  (`postCreateCommand`) in Codespaces / Dev Containers; otherwise run it manually
  with `bash scripts/setup.sh`. (Plain Copilot in VS Code has no session-start hook.)
- Prompt files in `.github/prompts/`: `/eda`, `/train-baseline`, `/full-pipeline`.
