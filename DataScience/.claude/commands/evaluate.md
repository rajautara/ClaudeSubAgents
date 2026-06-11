---
description: Evaluate the latest trained model on the held-out test set via model-evaluator
argument-hint: [model-path-or-name]
---

Use the `model-evaluator` subagent to evaluate the trained model
(`$ARGUMENTS` if given, otherwise the most recent model in `models/` per
`reports/experiments.md`).

Requirements:
- Evaluate on the held-out test split created by `data-cleaner` — touched ONCE.
- Full metrics for the problem type, error analysis by segment, calibration,
  and a decision-threshold recommendation tied to the cost of errors in
  `reports/problem_charter.md`.
- Compare against the baseline with a statistical check (bootstrap CI or
  paired test over CV folds), not just point estimates.
- Save plots to `reports/figures/`, the honest report to `reports/evaluation.md`,
  and the model card to `reports/model_card.md`.
