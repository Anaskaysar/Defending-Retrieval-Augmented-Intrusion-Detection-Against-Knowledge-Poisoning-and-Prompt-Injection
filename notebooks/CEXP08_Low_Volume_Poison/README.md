# CEXP08 — Low-Volume Poison (Major 5 partial)

**Fork of** `CEXP04_Scaled_Attack_Defense.ipynb` — CEXP04 untouched.  
**Closes:** Professor Major 5 *sub-point (b)* — CorruptRAG-style low-volume (1–2 docs).  
**Not claimed:** adaptive embedding attacks (Phantom / CPA-RAG) — still Future Work.

## Kaggle
1. New notebook → GPU + Internet ON  
2. Add **Preprocessed_CIC_UNSW**  
3. Upload `CEXP08_Low_Volume_Poison.ipynb`  
4. `SMOKE_TEST=True` first, then `False`, `SEED=42`  
5. Download `/kaggle/working/CEXP08_Low_Volume_Poison/` → local `Results/Low_Volume_Poison/`

## Config
- `POISON_COUNTS = [1, 2]` (absolute docs; KB≈2000 → ~0.05% / 0.1%)
- Undefended + Full D1+D2+D3 only
- Injection / latency skipped

## Rebuild from CEXP04
```bat
python Experiment_Lab\conf_track\CEXP08_Low_Volume_Poison\_build_cexp08.py
```
