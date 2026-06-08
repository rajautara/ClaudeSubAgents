---
mode: agent
description: Run exploratory data analysis on a dataset (pairs with the data-explorer agent)
---

Switch to the **data-explorer** agent (or stay in Agent mode) and profile the
dataset at `${input:dataset:path to the dataset}`.

Produce the full EDA report: shape, dtypes, memory, missing-value profile,
summary statistics, anomalies (outliers, duplicates, constant/high-cardinality
columns), correlations, and concrete cleaning recommendations. Save the report
to `reports/`. Do not modify the original data.
