---
description: Generate a stakeholder-facing (non-technical) summary of the project so far
argument-hint: [audience, e.g. "exec" or "product team"]
---

Write a stakeholder-facing summary of the data science work so far, for the
audience: `$ARGUMENTS` (default: non-technical business stakeholders).

Source material — read what exists under `reports/` (problem_charter, eda_*,
cleaning_log, experiments, evaluation, model_card, monitoring) and
`reports/figures/`. Do not re-run analysis; summarize what is on record.

Requirements:
- Lead with the business question and the answer/recommendation — not the method.
- Plain language: no jargon without a one-line explanation; metrics translated
  to business terms ("catches 8 of 10 fraud cases, 1 in 20 alerts is a false
  alarm") with help from the cost-of-errors section of the charter.
- Include: what was done, what was found, how good the model is vs the status
  quo baseline, key caveats/risks (be honest — include limitations from
  `reports/evaluation.md`), and recommended next steps with owners.
- Embed or reference 2-4 of the most decision-relevant figures.
- Keep it to 1-2 pages. Save to `reports/stakeholder_summary.md`.
