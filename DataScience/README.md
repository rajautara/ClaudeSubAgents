# Data Science Subagents (Python Stack)

A set of Claude Code subagents for an end-to-end data science workflow.

## Installation

Copy these into your project:
- `.claude/agents/` -> your **project root** `.claude/agents/` (shared with the team, committed to git)
- `CLAUDE.md` -> your **project root** (global context all subagents read)

Or, to use the agents across every project, copy `.claude/agents/` to
`~/.claude/agents/` (your home directory) instead.

Then in Claude Code, run `/agents` to confirm they all loaded.

## Subagents & roles

| Subagent | When to use | Focus |
|---|---|---|
| `data-explorer` | New dataset | EDA, profiling, missing values, correlation |
| `data-cleaner` | After EDA | Impute, dedup, fix dtypes, standardize, **create held-out split** |
| `feature-engineer` | Data is clean | Encoding, scaling, feature creation/selection |
| `model-trainer` | Features ready | Classical ML: baseline + tune (sklearn/xgb/lgbm/catboost) |
| `dl-trainer` | Deep learning task | PyTorch NN (MLP/CNN/RNN/Transformer), auto-GPU |
| `transformer-finetuner` | Fine-tune an LLM/NLP model | HuggingFace transformers, LoRA/QLoRA, auto-GPU |
| `model-evaluator` | After training | Metrics, error analysis, SHAP, validation |
| `viz-specialist` | Whenever a plot is needed | Visualization (matplotlib/seaborn/plotly) |
| `notebook-engineer` | Refactor/setup | Reproducibility, project structure, notebook hygiene |

## Typical workflow

```
data-explorer -> data-cleaner -> feature-engineer -> [ model-trainer
              (+ held-out split)   (build Pipeline)   | dl-trainer
                                                      | transformer-finetuner ] -> model-evaluator
                                       ^                                                  |
                              viz-specialist (called whenever a plot is needed)
notebook-engineer (support: project structure & reproducibility)
```

The held-out test split is created once by `data-cleaner` (before feature
engineering) and evaluated exactly once at the end by `model-evaluator`.
`feature-engineer` builds a Pipeline fit on the train set only, so no leakage
occurs during cross-validation.

## How to use

**Auto-delegation** — Claude Code picks the right subagent based on its `description`. Just say:
> "Profile the dataset sales.csv"  ->  `data-explorer` is invoked automatically.

**Manual** — name the subagent:
> "Use feature-engineer to encode the category column and scale the numericals."

**Chaining** — ask for the full workflow:
> "Run the full pipeline: explore, clean, engineer features, train a baseline + xgboost, then evaluate."

**Deep learning / fine-tuning:**
> "Use dl-trainer to build a CNN for this image dataset."
> "Use transformer-finetuner to LoRA fine-tune a BERT model for text classification."

## Notes

- Each subagent has its own separate context window — it does not pollute the main conversation. Great for long pipelines.
- `CLAUDE.md` holds global, project-wide context (stack, structure, conventions). Subagent `.md` files hold task-specific behavior. They complement each other.
- Edit any `.md` to tweak behavior — change the `tools` field to limit access (e.g. remove `Bash` from a subagent that should not run code).
- Each subagent pins a `model` in its frontmatter: heavier reasoning agents use `sonnet`, lighter mechanical ones (`viz-specialist`, `notebook-engineer`) use `haiku` to save cost. Change to `opus` or `inherit` as you prefer.
- Add more subagents as your stack needs (e.g. `timeseries-specialist`, `rag-specialist`).
- After editing agent files mid-session, run `/agents` again (or start a fresh session) to reload.
