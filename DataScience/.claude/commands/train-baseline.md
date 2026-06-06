---
description: Train a quick, honest baseline model via the model-trainer subagent
argument-hint: [target-column] [problem-type]
---

Use the `model-trainer` subagent to train a baseline on the prepared data.

Context (optional): `$ARGUMENTS` (target column and/or problem type).

Requirements:
- Use the held-out split created by `data-cleaner`; do not re-split.
- Train a simple baseline first (DummyClassifier/LogisticRegression or
  LinearRegression) and report its score with the correct metric for the
  problem (F1/AUC/PR-AUC for imbalanced classification; RMSE/MAE/R² for
  regression — not plain accuracy on imbalanced data).
- Fit any preprocessing inside the Pipeline within CV to avoid leakage.
- Set random_state=42 and log the result to `reports/experiments.md`.

This baseline is the bar every more complex model must beat.
