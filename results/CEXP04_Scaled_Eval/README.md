# Results — Scaled_Eval (CEXP04)

**Rule:** New Round 2 outputs only. Never copy into or overwrite `../Attack_Defense/`.

Expected artifacts (after runs):

- `cexp04_results_*.json` (use `_RECOVERED` suffix when rebuilt from notebook prints)
- `eval_set_ids_N*_seed*.json` (preferred — missing for seed=42 recovered run)
- `ckpt_*.json`
- `01_f1_fpr_vs_poison_*.png` / `.pdf`
- `03_injection_*.png` / `.pdf`
- Split tables: `poison_sweep_*`, `injection_results_*`, `clean_and_latency_*`
- FPR columns included in JSON for all poison rates

**Do not** put CEXP04 outputs under `Results/Attack_Defense/` (that tree is frozen CEXP03).
