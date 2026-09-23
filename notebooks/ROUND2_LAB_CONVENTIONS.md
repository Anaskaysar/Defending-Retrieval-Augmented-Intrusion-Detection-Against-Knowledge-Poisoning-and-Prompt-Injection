# Round 2 Lab Conventions (CIC → public release)

These rules keep the repo reviewable now and clean when we open the GitHub after publication.

---

## 0. Kaggle-first

Every Round 2 experiment notebook must run **standalone on Kaggle**:

- Input: dataset **Preprocessed_CIC_UNSW** only (see `KAGGLE_RUN_CARDS.md`)
- No dependency on another notebook’s `/kaggle/working` artifacts
- Write outputs under `/kaggle/working/CEXP0N_*/` then download into the matching local `Results/` folder

## 1. Golden rule: freeze the past

**Never modify, rename, or overwrite:**

- `CEXP01_Baselines/`, `CEXP02_RAG_Clean/`, `CEXP03_Attack_Defense/`
- `Results/Baselines/`, `Results/RAG_Clean/`, `Results/Attack_Defense/`
- Any historical notebook under those trees (`*_v2.ipynb`, `v3-final2.ipynb`, etc.)

**Reuse = copy.** Fork CEXP03 into a *new* CEXP0N folder. Cite the source notebook name + date in the new README.

---

## 2. New work lives in new folders

| Work item | Experiment folder | Results folder |
|-----------|-------------------|----------------|
| Scaled eval + FPR + injection (strong) | `CEXP04_Scaled_Eval/` | `Results/Scaled_Eval/` |
| D1/D2/D3 ablation | `CEXP05_Ablation/` *or* cells in CEXP04 | `Results/Ablation/` |
| FilterRAG-style baseline | `CEXP06_Defense_Baseline/` *or* cells in CEXP04 | `Results/Defense_Baseline/` |
| Latency | timed in CEXP04 (preferred) | `Results/Latency/` |

Prefer one primary notebook in CEXP04 for shared harness (sampler, KB, classify), and either:

- **Option A (recommended for tracking):** separate CEXP05/CEXP06 notebooks that *import* shared helpers from a new `CEXP04_Scaled_Eval/lib/` module, or  
- **Option B:** one CEXP04 notebook with clearly titled sections (`## A Scaled`, `## B Ablation`, …) still writing to the four Results dirs above.

Do **not** dump Round 2 JSON into `Results/Attack_Defense/`.

---

## 3. Naming

| Kind | Pattern | Example |
|------|---------|---------|
| Experiment folder | `CEXP0N_Short_Name/` | `CEXP04_Scaled_Eval/` |
| Notebook | `CEXP0N_Descriptive.ipynb` | `CEXP04_Scaled_Attack_Defense.ipynb` |
| Result JSON | `{cexp}_{topic}_{YYYYMMDD}.json` | `cexp04_scaled_poison_20260722.json` |
| Figures | `{nn}_{description}.png` or `.pdf` | `01_f1_vs_poison_rate_scaled.pdf` |
| Checkpoints | `ckpt_{topic}_seed{S}.json` | `ckpt_poison_seed42.json` |
| Eval ID lists | `eval_set_ids_N{n}_seed{S}.json` | `eval_set_ids_N500_seed42.json` |

Use **PDF/vector** figures for the paper when regenerating; keep PNG for notebooks if needed.

---

## 4. Every new experiment folder must have a README

Minimum sections (same spirit as `EXPERIMENT_CHECKLIST.md`):

1. Objective  
2. Hypothesis  
3. Setup (dataset path, models, seeds, hardware, N)  
4. Source fork (“Copied from `CEXP03_Attack_Defense_v2.ipynb`; do not edit original”)  
5. How to reproduce  
6. Results summary  
7. Files saved (map to `Results/...`)  
8. Known issues  

---

## 5. Code style for new notebooks

- Top cell: `RUN_ID`, `SEED`, `N_EVAL`, `SMOKE_TEST`, `POISON_RATES`, `OUTPUT_DIR` pointing only under `Results/Scaled_Eval` (etc.).
- Never write into `Results/Attack_Defense/` or CEXP03 paths.
- Prefer `pathlib.Path`; create output dirs with `mkdir(parents=True, exist_ok=True)`.
- Checkpoint long loops every *k* queries.
- Log FPR alongside F1 for every defense config.
- Record `hardware`, `git_commit` (if available), and `notebook_name` in every results JSON.
- Shared constants: keep defense hyperparameters fixed unless the ablation deliberately changes them (`D1_THETA=0.40`, `D2_PERCENTILE=95`, `LAMBDA_S=0.3`, `K_DOCS=5`).

---

## 6. Prompt library

- Do not rewrite historical prompt files used by CEXP03.
- Add new files as `*_r2.md` / `*_v2.txt` under the appropriate `Prompt_Library/` subfolder and reference them from CEXP04+.

---

## 7. Version log

Every meaningful change set is recorded in:

`Discussion_Docs/round2/04_ROUND2_VERSION_LOG.md`

Tags: `R2-P1.x` (writing), `R2-P2.x` (experiments), `R2-P3.x` (submit).

---

## 8. Public release checklist (post-publication)

- [ ] Old CEXP01–03 + Results remain as-is (pilot archive)  
- [ ] Round 2 Results folders complete with JSON + figures  
- [ ] READMEs filled; no absolute machine-specific secrets  
- [ ] Version log finalized  
- [ ] Root README points to `conf_track/` layout and this conventions file  
