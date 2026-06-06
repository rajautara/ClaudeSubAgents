---
description: Run exploratory data analysis on a dataset via the data-explorer subagent
argument-hint: <path-to-dataset>
---

Use the `data-explorer` subagent to profile the dataset at `$ARGUMENTS`.

Produce the full EDA report: shape, dtypes, memory, missing-value profile,
summary statistics, anomalies (outliers, duplicates, constant/high-cardinality
columns), correlations, and concrete cleaning recommendations. Save the report
to `reports/`. Do not modify the original data.
