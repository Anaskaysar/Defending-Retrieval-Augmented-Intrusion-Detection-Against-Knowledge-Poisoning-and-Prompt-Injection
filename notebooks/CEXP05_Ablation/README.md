# CEXP05 — Defense Component Ablation (D1 / D2 / D3)

**Track:** Conference (IEEE CIC 2026 Round 2)  
**Status:** Notebook ready for Kaggle  
**Version:** `R2-P2.1`  
**Notebook:** `CEXP05_Ablation.ipynb`  
**Standalone:** Yes — same **Preprocessed_CIC_UNSW** dataset (does not need CEXP04 working files)

## Objective

Isolate D1 / D2 / D3 on the scaled stratified eval set (same construction as CEXP04).

## Kaggle steps

1. New notebook → GPU + Internet ON  
2. Add **Preprocessed_CIC_UNSW**  
3. Open `CEXP05_Ablation.ipynb`  
4. `SMOKE_TEST=True` → Run All → then full with `False`  
5. Download `/kaggle/working/CEXP05_Ablation/` → local `Results/Ablation/`

## Configs (full run)

undefended · D2 only · full D1+D2+D3 · D1 only · D3 only · D1+D2  
Poison rates: **10%** and **30%** (smoke: 10% only, 3 configs)
