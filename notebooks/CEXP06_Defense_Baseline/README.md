# CEXP06 — FilterRAG-Style Defense Baseline

**Track:** Conference (IEEE CIC 2026 Round 2)  
**Status:** Notebook ready for Kaggle  
**Version:** `R2-P2.10` (tau recalibration fix `R2-P2.9` + plots moved in-notebook `R2-P2.10`)  
**Notebook:** `CEXP06_FilterRAG_Style.ipynb`  
**Standalone:** Yes — same **Preprocessed_CIC_UNSW** dataset

## Objective

Compare Undefended vs **B0** (simplified FilterRAG-style hard cosine filter) vs **Full D1+D2+D3**.

## Kaggle steps

1. New notebook → GPU + Internet ON  
2. Add **Preprocessed_CIC_UNSW**  
3. Open `CEXP06_FilterRAG_Style.ipynb`  
4. Smoke then full  
5. Download `/kaggle/working/CEXP06_Defense_Baseline/` → local `Results/Defense_Baseline/` — this now includes the two comparison figures (`01_f1_fpr_baseline_comparison_seed{S}.{png,pdf}`, `02_recovery_R_baseline_comparison_seed{S}.{png,pdf}`), no separate plotting step needed

## Notes

- B0 is described in results JSON as *simplified FilterRAG-style*, citing Edemacu et al. (`arXiv:2508.02835`) — not a full ML-FilterRAG reimplementation.
- **Plots are generated inside this notebook now** (cells after the baseline comparison), not in a separate notebook. `CEXP06_Generate_Plots.ipynb` still exists as a local-only fallback for re-plotting an already-downloaded results JSON (e.g. the original pre-fix seed=42 run) without needing a Kaggle session — it is not required for a fresh run of this notebook.
- The final plotting cell includes a standing sanity check that flags (doesn't just silently produce) the case where `filterrag_style_B0` comes out numerically identical to `undefended` at every rate — the signature of a mis-calibrated `B0_TAU` that never actually filters anything (see `04_ROUND2_VERSION_LOG.md` `R2-P2.7`/`R2-P2.9`).
- `RUN_ID` is `cexp06_filterrag_style_v2` (bumped from `cexp06_filterrag_style` when the tau calibration was fixed) so a rerun can't accidentally resume from the old invalid-B0 checkpoints.
