# CEXP08 — Low-Volume Poison (Major 5 partial) — FINDINGS

**Source:** `Experiment_Lab/conf_track/Results/Low_Volume_Poison/CEXP04_Scaled_Eval/cexp04_results_cexp08_lowvol_seed42_N499.json`  
**Protocol:** same as CEXP04 (`N=499`, `KB=2000`, `k=5`, seed 42). Absolute poison counts `{1, 2}` (~0.05% / 0.1% of KB).  
**Scope:** undefended + full D1+D2+D3 only. Injection/latency skipped.

## Numbers

| Setting | Undef F1 | Def F1 | Undef FPR | Def FPR | R |
|---------|----------|--------|-----------|---------|---|
| Clean   | 0.2611   | 0.2638 | 0.0749    | 0.0749  | — |
| n=1     | 0.2611   | 0.2638 | 0.0749    | 0.0749  | 1.0103 |
| n=2     | 0.2611   | 0.2638 | 0.0749    | 0.0749  | 1.0103 |

## Interpretation

Injecting 1–2 PoisonedRAG-style relabelled documents into a 2,000-doc KB has **no measurable effect** on F1 or FPR under this retrieval setting (`k=5`). Defended F1 stays at the clean-defended level (`R≈1.01`). This closes the CorruptRAG-style *absolute-count* realism probe for the conference package; adaptive embedding attacks (Phantom / CPA-RAG) remain journal future work.
