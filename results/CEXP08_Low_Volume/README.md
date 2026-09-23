# Low-Volume Poison Results (CEXP08)

**Status:** complete (seed 42, `SMOKE_TEST=False`, `N=499`).

## Key result
Injecting **1 or 2** PoisonedRAG-style docs into a 2,000-doc KB does **not**
move F1/FPR relative to clean on this seed (`R=1.010` for both counts).

| Setting | Undef F1 | Def F1 | FPR | R |
|---------|----------|--------|-----|---|
| Clean   | 0.2611   | 0.2638 | 0.0749 | — |
| n=1     | 0.2611   | 0.2638 | 0.0749 | 1.0103 |
| n=2     | 0.2611   | 0.2638 | 0.0749 | 1.0103 |

## Files
- `CEXP04_Scaled_Eval/cexp04_results_cexp08_lowvol_seed42_N499.json` (final)
- `CEXP04_Scaled_Eval/ckpt_poison_sweep_summary_seed42.json`
- `CEXP04_Scaled_Eval/01_f1_fpr_vs_poison_cexp08_lowvol.png`
- per-condition `ckpt_n{1,2}-{Undef,Def}_seed42.json`

Note: Kaggle wrote under a nested `CEXP04_Scaled_Eval/` folder name leftover
from the fork; content is CEXP08 (`run_id=cexp08_lowvol`).
