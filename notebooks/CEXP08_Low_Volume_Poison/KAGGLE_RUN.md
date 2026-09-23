# CEXP08 Kaggle run card (Major 5 — low-volume poison)

While FilterRAG (CEXP06) is running on one session, upload this on a **second** GPU notebook if quota allows; otherwise run immediately after FilterRAG finishes.

## Upload
1. New Kaggle notebook → **GPU** + Internet ON  
2. Add dataset **Preprocessed_CIC_UNSW**  
3. Upload: `Experiment_Lab/conf_track/CEXP08_Low_Volume_Poison/CEXP08_Low_Volume_Poison.ipynb`  
4. First pass: leave `SMOKE_TEST = True` (cell 4) → ~minutes  
5. Full: set `SMOKE_TEST = False`, `SEED = 42` → ~same order as a short CEXP04 poison-only slice (2 counts × 2 configs × 499 queries)

## Confirm before long run
Cell print must show:
- `RUN_ID : cexp08_lowvol`
- `Poison counts : [1, 2]` (not rates)
- `RES_DIR : /kaggle/working/CEXP08_Low_Volume_Poison`

## Download
`/kaggle/working/CEXP08_Low_Volume_Poison/` → local  
`Experiment_Lab/conf_track/Results/Low_Volume_Poison/`

Then tell Cursor to wire `n=1` / `n=2` R into `tab:poison` / Discussion.
