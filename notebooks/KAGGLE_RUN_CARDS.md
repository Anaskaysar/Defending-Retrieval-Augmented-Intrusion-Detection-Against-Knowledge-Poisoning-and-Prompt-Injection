# Kaggle Run Cards — Round 2 (CEXP04 / 05 / 06)

Each experiment is a **standalone** notebook. Upload separately. Do not depend on another notebook’s `/kaggle/working` output.

## Shared input dataset

Attach the same dataset you already use for CEXP02:

| Field | Value |
|-------|--------|
| Dataset title | **Preprocessed_CIC_UNSW** |
| Expected tree | `Processed_CIC_UNSW/Processed/CIC/*.npy` (+ `label_encoder_cic.pkl`) |
| Also present | `baseline_results.csv`, `baseline_results_full.json` (reference only) |

Path discovery in notebooks tries:

- `/kaggle/input/preprocessed-cic-unsw/Processed_CIC_UNSW/Processed/CIC`
- `/kaggle/input/datasets/kaysarulanas/preprocessed-cic-unsw/Processed_CIC_UNSW/Processed/CIC`

## Session settings (all three)

- Accelerator: **GPU T4**
- Internet: **ON** (pip + HuggingFace Mistral / BGE-M3)
- Persistence: download `/kaggle/working/...` after each run

## Run order (recommended)

| Order | Notebook | Folder | First run |
|-------|----------|--------|-----------|
| 1 | `CEXP04_Scaled_Attack_Defense.ipynb` | `CEXP04_Scaled_Eval/` | `SMOKE_TEST=True` |
| 2 | `CEXP05_Ablation.ipynb` | `CEXP05_Ablation/` | `SMOKE_TEST=True` |
| 3 | `CEXP06_FilterRAG_Style.ipynb` | `CEXP06_Defense_Baseline/` | `SMOKE_TEST=True` |

After smoke OK → set `SMOKE_TEST=False` and re-run (or duplicate notebook as `*_full`).

## Download → local Results (never into old Attack_Defense)

| Kaggle output | Local path |
|---------------|------------|
| `/kaggle/working/CEXP04_Scaled_Eval/` | `Experiment_Lab/conf_track/Results/Scaled_Eval/` |
| `/kaggle/working/CEXP04_Latency/` | `Experiment_Lab/conf_track/Results/Latency/` |
| `/kaggle/working/CEXP05_Ablation/` | `Experiment_Lab/conf_track/Results/Ablation/` |
| `/kaggle/working/CEXP06_Defense_Baseline/` | `Experiment_Lab/conf_track/Results/Defense_Baseline/` |

## Freeze rule

**Do not edit** `CEXP01_*`, `CEXP02_*`, `CEXP03_*` or `Results/{Baselines,RAG_Clean,Attack_Defense}/`.

## Rebuild notebooks from fork script (optional)

```text
python Experiment_Lab/conf_track/CEXP04_Scaled_Eval/_build_round2_notebooks.py
```

Source of the fork remains the frozen `CEXP03_Attack_Defense_v2.ipynb` (read-only).
