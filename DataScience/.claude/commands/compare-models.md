---
description: Build a leaderboard comparing all trained models from the experiment log
argument-hint: [metric-to-rank-by]
---

Read `reports/experiments.md` (and MLflow/W&B runs if configured) and produce a
model comparison leaderboard.

Requirements:
- One table: model, key hyperparameters, CV score (mean ± std), train time,
  artifact path. Rank by `$ARGUMENTS` if given, otherwise by the primary metric
  from `reports/problem_charter.md`.
- Always include the baseline row — flag any model that does NOT beat it.
- Note comparability caveats: models compared on different splits/folds or
  different feature versions are NOT directly comparable — say so explicitly.
- Recommend ONE candidate to send to `model-evaluator`, with a short rationale
  (score, complexity, latency/interpretability constraints from the charter).
- Save the leaderboard to `reports/leaderboard.md`. Do NOT touch the held-out
  test set — this command compares CV results only.
