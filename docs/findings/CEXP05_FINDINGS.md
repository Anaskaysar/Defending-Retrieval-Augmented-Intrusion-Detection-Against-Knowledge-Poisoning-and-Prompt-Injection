# 02 CEXP05 — Ablation findings (for paper)

**Status:** Done (full download from `/kaggle/working`, not recovered)  
**N:** 499 · **SEED:** 42 · **SMOKE:** False · rates: 10%, 30%  
**Lab archive:** `Experiment_Lab/conf_track/Results/Ablation/CEXP05_Ablation/`  
**Executed notebook:** `Experiment_Lab/conf_track/CEXP05_Ablation/cex05-ablation_complete.ipynb`

## Placement

| Item | Path |
|------|------|
| JSON / plots / ckpts / `eval_set_ids` | `Results/Ablation/CEXP05_Ablation/` |
| Complete notebook | `CEXP05_Ablation/cex05-ablation_complete.ipynb` |
| Paper staging copies | this folder (`figures/` + JSON) |

Correct tree (Round 2). Do not put under `Results/Attack_Defense/`.

## Clean baseline (same protocol as CEXP04 seed 42)

| | F1 | FPR | Acc |
|--|-----|-----|-----|
| Clean undefended | 0.2649 | 0.0745 | 0.3293 |

Matches CEXP04 seed=42 clean undef — good cross-check.

## Ablation table (paper-ready)

| Config | F1 @10% | FPR @10% | R @10% | F1 @30% | FPR @30% | R @30% |
|--------|---------|----------|--------|---------|----------|--------|
| Undefended | 0.2220 | 0.0778 | 0.838 | 0.1702 | 0.0817 | 0.643 |
| D1 only | 0.2220 | 0.0778 | 0.838 | 0.1702 | 0.0817 | 0.643 |
| D2 only (LECC) | 0.2103 | 0.0787 | 0.794 | 0.1534 | 0.0838 | 0.579 |
| D3 only | 0.2217 | 0.0778 | 0.837 | 0.1737 | 0.0815 | 0.656 |
| D1+D2 | 0.2103 | 0.0787 | 0.794 | 0.1534 | 0.0838 | 0.579 |
| Full D1+D2+D3 | 0.2102 | 0.0787 | 0.794 | 0.1552 | 0.0836 | 0.586 |

R = F1_config / F1_clean_undef (same definition as CEXP04).

## What goes in the paper (talking points)

1. **Cross-check:** Undefended and Full @10%/30% match CEXP04 seed=42 poison rows — ablation used the same scaled protocol.
2. **D2 carries the defended path:** D2_only ≈ D1+D2 ≈ Full on both rates. Adding D1 (or D3) on top of D2 does not change poison F1 materially. Supports LECC as the active poison-side component (C1).
3. **D1 alone ≈ undefended:** soft trust score does not move poison metrics here — report honestly; D1 is a light prior, not the poison mitigator.
4. **D3 alone ≈ undefended on poison (by design):** D3 targets injection, not PoisonedRAG relabelling. Slight F1 edge at 30% (0.1737 vs 0.1702) is small — do **not** claim D3 as a poison defense.
5. **Honest framing required:** configs that include D2 have **lower** poisoned F1 than undefended at these rates (same pattern as CEXP04). Ablation explains *who shapes the defended pipeline*, not that demotion always raises absolute F1 vs undef under poison. Keep R as recovery vs clean; state the undef-vs-def nuance in Discussion.
6. **Injection ablation still from CEXP04** (multi vs single) — CEXP05 skipped injection by design.

## Figures

- `01_ablation_f1_seed42.png` / `.pdf`
- `02_ablation_R_fpr_seed42.png` / `.pdf`  
Regenerate at 300 dpi locally for camera-ready if needed.

## Open

- [ ] Optional: repeat ablation on seed 123/7 only if time (seed 42 enough for CIC compact table)
- [ ] Insert Ablation subsection + table into `main.tex` after FilterRAG / with paper rewrite pass
- [ ] Next GPU: CEXP04 seeds 123→7, then CEXP06 (per R2-P2.5 order)
