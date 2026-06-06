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

## Subagents (in .claude/agents/)
- `data-explorer` — EDA & profiling
- `data-cleaner` — cleaning & preprocessing
- `feature-engineer` — encoding, scaling, feature creation/selection
- `model-trainer` — classical ML (sklearn/xgb/lgbm/catboost)
- `dl-trainer` — PyTorch neural networks (auto-GPU)
- `transformer-finetuner` — fine-tune HuggingFace Transformers (LoRA/QLoRA)
- `model-evaluator` — metrics, error analysis, SHAP, validation
- `viz-specialist` — plots (matplotlib/seaborn/plotly)
- `notebook-engineer` — reproducibility & project structure

Typical flow:
explore -> clean (+ create held-out split) -> engineer (build Pipeline)
-> train (model-trainer | dl-trainer | transformer-finetuner) -> evaluate,
with viz-specialist called whenever a plot is needed and notebook-engineer
supporting structure & reproducibility.
