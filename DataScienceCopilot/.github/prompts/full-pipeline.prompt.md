---
mode: agent
description: Run the end-to-end DS pipeline, switching between the specialist agents
---

Run the full data science pipeline on `${input:source:dataset path or source}`
(target column: `${input:target:target column}`), moving through each stage and
passing artifacts forward. Switch to the named agent for each stage (or stay in
Agent mode and follow its instructions):

1. **data-ingestion** — if the input is a source (SQL/API/cloud) rather than a
   local file, land the raw data in `data/raw/` first. Skip if data is already local.
2. **data-explorer** — profile the dataset; produce the EDA report.
3. **data-cleaner** — clean, then create the held-out train/test split (stratified
   or time-aware as appropriate).
4. **data-validator** — codify a schema/contract for the cleaned data.
5. **feature-engineer** — build the preprocessing Pipeline (fit on train only).
6. **model-trainer** — baseline first, then candidate models tuned via CV.
   (Use **dl-trainer**, **transformer-finetuner**, or **timeseries-specialist**
   instead if the task is deep learning, NLP fine-tuning, or time-series.)
7. **model-evaluator** — evaluate ONCE on the held-out test set; honest report.

Switch to **viz-specialist** whenever a plot is needed. Respect every
copilot-instructions.md rule: no leakage, seed 42, baseline-before-complex,
correct metric, audit trail in `reports/`. Summarize results and next steps at the end.
