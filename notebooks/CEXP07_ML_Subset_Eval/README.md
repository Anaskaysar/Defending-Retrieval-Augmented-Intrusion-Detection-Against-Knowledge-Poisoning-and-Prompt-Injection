# CEXP07 — ML Subset Eval (Major 3)

**Track:** Conference Round 2  
**Status:** CPU script — no Kaggle/GPU  
**Closes:** Professor Major 3 (unified test set for ML vs RAG)

## Objective
Rescore frozen CEXP01 RF and XGBoost on the **identical** CEXP04 `eval_set_ids` (N=499, seeds 42/123/7).

## Setup
- Models: `Results/Baselines/rf_cic.pkl`, `xgb_cic.json` (read-only)
- Indices: CEXP04/05 `eval_set_ids_N499_seed*.json`
- Data: `Experiment_Lab/Data/Processed/CIC/{X,y}_test.npy`

## Reproduce
```bat
python Experiment_Lab\conf_track\CEXP07_ML_Subset_Eval\run_cexp07_ml_subset.py
```

## Outputs
`Results/ML_Subset_Eval/cexp07_ml_subset_3seeds.json` + `FINDINGS.md`

## Freeze rule
Does **not** modify CEXP01 or `Results/Baselines/`.
