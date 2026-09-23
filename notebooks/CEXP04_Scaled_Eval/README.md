# CEXP04 — Scaled Attack / Defense Evaluation

**Track:** Conference (IEEE CIC 2026 Round 2)  
**Status:** Notebook ready for Kaggle  
**Version:** `R2-P2.0`  
**Notebook:** `CEXP04_Scaled_Attack_Defense.ipynb`  
**Standalone:** Yes — only needs dataset **Preprocessed_CIC_UNSW**

## Objective

Scale adversarial evaluation from CEXP03 pilot (*n*=45) to **N≥500** stratified queries (all 10 classes), log **FPR**, run **multi-doc + single-doc** injection, and measure **latency**.

## Kaggle steps

1. New notebook → GPU + Internet ON  
2. Add input: **Preprocessed_CIC_UNSW**  
3. Upload / open `CEXP04_Scaled_Attack_Defense.ipynb`  
4. Keep `SMOKE_TEST = True` → Run All  
5. If OK: set `SMOKE_TEST = False`, Run All (long)  
6. Download `/kaggle/working/CEXP04_Scaled_Eval/` and `/kaggle/working/CEXP04_Latency/`

## Source (read-only)

Forked from `../CEXP03_Attack_Defense/CEXP03_Attack_Defense_v2.ipynb` via `_build_round2_notebooks.py`.  
**Do not edit** any file under `CEXP03_Attack_Defense/`.

## Outputs

| Artifact | Path |
|----------|------|
| Metrics / plots / eval IDs | `../Results/Scaled_Eval/` (from Kaggle working) |
| Latency JSON | `../Results/Latency/` |

## Config highlights

| Knob | Smoke | Full |
|------|-------|------|
| `EVAL_N_PER_CLASS` | 2 → ~20 | 50 → **500** |
| Classes | all 10 | all 10 |
| Poison rates | `[0.10]` | 1–30% |
| Injection | multi + single | multi + single |
