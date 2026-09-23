# CEXP07 — Same-set ML vs RAG (Major 3)

RF/XGB scored on **identical** CEXP04 `eval_set_ids` (N=499, seeds 42/123/7).

| Model | Macro F1 (mean±std) | Macro FPR (mean±std) |
|-------|---------------------|----------------------|
| Random Forest | 0.6315±0.0180 | 0.0414±0.0022 |
| XGBoost | 0.6778±0.0219 | 0.0375±0.0027 |
| RAG-IDS (clean undef, CEXP04) | 0.2697±0.0163 | 0.0748±0.0003 |

Full-partition CEXP01 numbers (RF 0.468 / XGB 0.475) are **not** mixed into this table.
