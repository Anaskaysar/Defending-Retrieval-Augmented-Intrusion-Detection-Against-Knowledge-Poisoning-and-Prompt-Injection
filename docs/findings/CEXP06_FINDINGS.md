# CEXP06 — FilterRAG-style Baseline v2 — FINDINGS

**Source:** `Results/Defense_Baseline/FilterRag_Final/.../filterrag_style_vs_ours_cexp06_filterrag_style_v2_seed42.json`  
**Calibration:** query→doc k-th similarity, `B0_TAU=0.9718`, `B0_M=20` (corrected vs. failed doc→doc τ=0.9943 no-op).  
**Protocol:** CEXP04-matched (`N=499`, seed 42).

## Numbers

| Rate | Undef F1 | B0 F1 | Full F1 | R_B0 | R_Full |
|------|----------|-------|---------|------|--------|
| 1%   | 0.2621   | 0.1878| 0.2630  | 0.719| 1.007  |
| 5%   | 0.2381   | 0.1663| 0.2295  | 0.637| 0.879  |
| 10%  | 0.2211   | 0.1631| 0.2080  | 0.625| 0.797  |
| 20%  | 0.2079   | 0.1521| 0.1980  | 0.583| 0.758  |
| 30%  | 0.1702   | 0.1359| 0.1552  | 0.521| 0.594  |

Clean undef F1 = 0.2611 (same seed-42 query set as CEXP08).

## Interpretation

B0 now **engages** (no longer identical to Undefended). Under PoisonedRAG-style relabelling on this IDS embedding space, hard cosine filtering is **too aggressive**: B0 F1 is below Undefended at every rate, and Full D1+D2+D3 dominates B0 on both absolute F1 and recovery R. Soft demotion + LECC is the better fit for this workload than a calibrated hard similarity filter.
