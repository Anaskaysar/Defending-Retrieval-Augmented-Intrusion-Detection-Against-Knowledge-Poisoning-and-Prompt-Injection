# Results — Defense_Baseline (CEXP06)

**Rule:** New Round 2 outputs only. Prefer `FilterRag_Final/` over `Old_FilterRag/`.

## Seed 42 — corrected v2 (`FilterRag_Final/`)

- `filterrag_style_vs_ours_cexp06_filterrag_style_v2_seed42.json`
- `ckpt_filterrag_summary_v2_seed42.json`
- Comparison figures (`01_f1_fpr_*`, `02_recovery_R_*`)
- `B0_TAU=0.9718` (query→doc k-th calibration) — **engages**

| Rate | Undef F1 | B0 F1 | Full F1 | R_B0 | R_Full |
|------|----------|-------|---------|------|--------|
| 1%   | 0.2621   | 0.1878| 0.2630  | 0.719| 1.007  |
| 5%   | 0.2381   | 0.1663| 0.2295  | 0.637| 0.879  |
| 10%  | 0.2211   | 0.1631| 0.2080  | 0.625| 0.797  |
| 20%  | 0.2079   | 0.1521| 0.1980  | 0.583| 0.758  |
| 30%  | 0.1702   | 0.1359| 0.1552  | 0.521| 0.594  |

**Takeaway:** hard cosine B0 underperforms Undefended and Full at every rate;
soft demotion + LECC wins this workload.

## Old diagnostic (`Old_FilterRag/`)

Failed doc→doc calibration (`τ≈0.9943`) made B0 identical to Undefended —
kept only as the audit trail of the bug.

Findings write-up: `Paper_Writing/conf/round2_notes/03_CEXP06_FilterRAG/FINDINGS.md`
