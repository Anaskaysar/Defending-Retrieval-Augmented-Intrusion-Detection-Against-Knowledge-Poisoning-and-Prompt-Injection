"""Build CEXP08 low-volume poison notebook from CEXP04 (Major 5 partial).

Fork only — does not modify CEXP04 source notebook.
"""
from __future__ import annotations

import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "CEXP04_Scaled_Eval" / "CEXP04_Scaled_Attack_Defense.ipynb"
OUT_DIR = ROOT / "CEXP08_Low_Volume_Poison"
OUT_NB = OUT_DIR / "CEXP08_Low_Volume_Poison.ipynb"
OUT_DIR.mkdir(parents=True, exist_ok=True)

nb = json.loads(SRC.read_text(encoding="utf-8"))


def cell_src(i: int) -> str:
    s = nb["cells"][i]["source"]
    return "".join(s) if isinstance(s, list) else s


def set_src(i: int, text: str) -> None:
    nb["cells"][i]["source"] = text.splitlines(keepends=True)


# --- Cell 0: title ---
set_src(
    0,
    """# CEXP08 — Low-Volume Poisoning (Major 5 partial)

**Fork of** `CEXP04_Scaled_Attack_Defense.ipynb` (do not edit CEXP04).  
**Goal:** answer CorruptRAG-style **low-volume** setting with absolute poison counts `{1, 2}`
docs injected into the KB (not rate-based 1–30%).

**Scope:** poison sweep only (undefended + full D1+D2+D3). Injection / latency skipped.  
**Kaggle:** Preprocessed_CIC_UNSW · GPU · Internet ON · `SMOKE_TEST=True` first.
""",
)

# --- Find and patch config cell (RUN_ID / POISON_RATES) ---
patched_cfg = False
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = cell_src(i)
    if "RUN_ID" in src and "POISON_RATES" in src and "SMOKE_TEST" in src:
        src = src.replace('RUN_ID       = "cexp04_scaled"', 'RUN_ID       = "cexp08_lowvol"')
        src = src.replace('RUN_ID = "cexp04_scaled"', 'RUN_ID = "cexp08_lowvol"')
        # Absolute counts instead of rates
        if "POISON_RATES = [0.10] if SMOKE_TEST else [0.01, 0.05, 0.10, 0.20, 0.30]" in src:
            src = src.replace(
                "POISON_RATES = [0.10] if SMOKE_TEST else [0.01, 0.05, 0.10, 0.20, 0.30]",
                "POISON_COUNTS = [1] if SMOKE_TEST else [1, 2]  # absolute # poisoned docs (Major 5)\n"
                "POISON_RATES = []  # unused; kept so old prints don't NameError",
            )
        # Skip injection + latency for this focused run
        # (regex, not a plain .replace: source uses aligned "RUN_LATENCY  = True"
        # with 2 spaces before "=", which a literal 1-space match silently misses —
        # found during pre-run review, see 04_ROUND2_VERSION_LOG.md R2-P3.4)
        src, _n_lat = re.subn(
            r"RUN_LATENCY\s*=\s*True",
            "RUN_LATENCY = False  # CEXP08: poison-only",
            src,
        )
        assert _n_lat == 1, f"RUN_LATENCY patch matched {_n_lat} times, expected 1 — check config cell text"
        if "INJECTION_MODES" in src:
            src = src.replace(
                'INJECTION_MODES = ["multi", "single"]',
                'INJECTION_MODES = []  # skipped in CEXP08',
            )
        # Paths
        src = src.replace("CEXP04_Scaled_Eval", "CEXP08_Low_Volume_Poison")
        src = src.replace("CEXP04_Latency", "CEXP08_Latency_unused")
        src = src.replace("/Scaled_Eval", "/Low_Volume_Poison")
        set_src(i, src)
        patched_cfg = True
        print(f"Patched config cell {i}")
        break
assert patched_cfg, "config cell not found"

# --- Patch craft_poison_docs to accept n_poison_abs ---
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = cell_src(i)
    if "def craft_poison_docs" not in src:
        continue
    old = "def craft_poison_docs(kb_d, kb_e, poison_rate, seed=SEED):"
    new = (
        "def craft_poison_docs(kb_d, kb_e, poison_rate=None, n_poison_abs=None, seed=SEED):\n"
        "    \"\"\"PoisonedRAG-style relabel. Prefer n_poison_abs for low-volume (Major 5).\"\"\""
    )
    if old not in src:
        # try alternate signature already multiline
        print(f"craft_poison signature not exact in cell {i}; attempting flexible patch")
    else:
        src = src.replace(old, new, 1)
    # Replace n_poison computation
    needle = "n_poison   = max(1, int(len(kb_d) * poison_rate))"
    repl = (
        "if n_poison_abs is not None:\n"
        "        n_poison = max(1, int(n_poison_abs))\n"
        "    else:\n"
        "        n_poison = max(1, int(len(kb_d) * float(poison_rate)))"
    )
    if needle in src:
        src = src.replace(needle, repl, 1)
    else:
        needle2 = "n_poison = max(1, int(len(kb_d) * poison_rate))"
        if needle2 in src:
            src = src.replace(needle2, repl, 1)
    set_src(i, src)
    print(f"Patched craft_poison_docs in cell {i}")
    break

# --- Rewrite poison sweep loop as a WHOLE cell ---
# CEXP04's sweep cell mixes many `p_rate`/`_done_rates` references (loop var,
# resume-skip print, banner print, run_eval desc=, result dict, done-set add,
# final summary print). Per-string .replace() historically missed several of
# them, so every rebuild reintroduced `NameError: name 'p_rate' is not defined`
# at run time on Kaggle (see 04_ROUND2_VERSION_LOG.md). We now overwrite the
# entire cell with a count-based template that is self-consistent.
CELL_SWEEP = r'''CLEAN_F1_REF = 0.1237   # CEXP02 characterization only - NOT used for R
# R uses clean undefended F1 on THIS eval set (CEXP04 protocol)

# -- Resume: reload prior progress for this SEED, if any (R2-P2.0.2) --
_outer_ck = load_ckpt("poison_sweep_summary")
poison_results = _outer_ck.get("poison_results", []) if _outer_ck else []
clean_undef = _outer_ck.get("clean_undef") if _outer_ck else None
clean_def = _outer_ck.get("clean_def") if _outer_ck else None
latency_results = _outer_ck.get("latency_results") if _outer_ck else None
_done_counts = {r.get("n_poison_abs") for r in poison_results if r.get("n_poison_abs") is not None}
if _outer_ck:
    print(f"Resuming poison sweep (seed={SEED}): {len(poison_results)}/{len(POISON_COUNTS)} counts already done: {sorted(_done_counts)}")

print("\n=== CLEAN EVAL (CEXP08 / CEXP04 protocol) ===")
if clean_undef is None:
    clean_undef = run_eval(
        eval_X, eval_y, clean_faiss, kb_docs, kb_embs, clean_bm25,
        use_defense=False, desc="Clean-Undef", time_stages=False,
    )
if clean_def is None:
    clean_def = run_eval(
        eval_X, eval_y, clean_faiss, kb_docs, kb_embs, clean_bm25,
        d2_centroids, d2_thresholds, d3_inj_embs,
        use_defense=True, desc="Clean-Def_full", time_stages=False,
    )
print(f"\nClean Undef: F1={clean_undef['f1']:.4f}  FPR={clean_undef['fpr']:.4f}")
print(f"Clean Def:   F1={clean_def['f1']:.4f}  FPR={clean_def['fpr']:.4f}")
print(f"(CEXP02 ref macro-F1={CLEAN_F1_REF} is a different protocol - do not mix)")

# Latency skipped in CEXP08 (RUN_LATENCY=False); branch kept for parity
if RUN_LATENCY and latency_results is None:
    print(f"\n=== LATENCY (first {LATENCY_N} queries, clean defended) ===")
    lat_X, lat_y = eval_X[:LATENCY_N], eval_y[:LATENCY_N]
    lat = run_eval(
        lat_X, lat_y, clean_faiss, kb_docs, kb_embs, clean_bm25,
        d2_centroids, d2_thresholds, d3_inj_embs,
        use_defense=True, desc="Latency-Def", time_stages=True, max_print=5,
    )
    latency_results = {
        "n": LATENCY_N,
        "hardware": torch.cuda.get_device_name(0) if DEVICE == "cuda" else "cpu",
        "stages_ms": lat.get("latency_ms"),
        "f1_on_subset": lat["f1"],
        "fpr_on_subset": lat["fpr"],
    }
    with open(LAT_DIR / f"latency_per_stage_{RUN_ID}_seed{SEED}.json", "w") as f:
        json.dump(latency_results, f, indent=2)
    print("Latency saved to", LAT_DIR)
elif latency_results is not None:
    print("Latency already computed for this seed - reusing cached result.")
else:
    print("CEXP08: latency skipped (RUN_LATENCY=False).")

save_ckpt("poison_sweep_summary", {
    "clean_undef": clean_undef, "clean_def": clean_def,
    "latency_results": latency_results, "poison_results": poison_results,
})

for n_poison_abs in POISON_COUNTS:
    if n_poison_abs in _done_counts:
        print(f"\nn_poison={n_poison_abs}: already done (seed={SEED}) - skipping")
        continue
    print(f"\n{'='*60}\nLOW-VOLUME POISON: n_poison_abs={n_poison_abs}\n{'='*60}")
    pdocs, pembs = craft_poison_docs(kb_docs, kb_embs, n_poison_abs=n_poison_abs)
    all_docs = kb_docs + pdocs
    all_embs = np.vstack([kb_embs, pembs])
    n_total = len(all_docs)
    print(f"KB: {len(kb_docs)} clean + {len(pdocs)} poison = {n_total}")

    _cpu2 = faiss.IndexFlatIP(DIM)
    if USE_GPU_FAISS:
        p_faiss = faiss.index_cpu_to_gpu(faiss_res, 0, _cpu2)
    else:
        p_faiss = _cpu2
    p_faiss.add(all_embs.astype("float32"))
    p_bm25 = BM25Okapi([d["text"].lower().split() for d in all_docs])

    undef = run_eval(
        eval_X, eval_y, p_faiss, all_docs, all_embs, p_bm25,
        use_defense=False, n_kb=n_total, desc=f"n{n_poison_abs}-Undef",
    )
    def_full = run_eval(
        eval_X, eval_y, p_faiss, all_docs, all_embs, p_bm25,
        d2_centroids, d2_thresholds, d3_inj_embs,
        use_defense=True, n_kb=n_total, desc=f"n{n_poison_abs}-Def",
    )

    rec = def_full["f1"] / max(clean_undef["f1"], 1e-8)
    res = {
        "poison_rate": None,
        "n_poison_abs": int(n_poison_abs),
        "poison_rate_equiv": float(n_poison_abs) / max(len(kb_docs), 1),
        "n_poison": len(pdocs),
        "n_total": n_total,
        "undefended": {"f1": undef["f1"], "fpr": undef["fpr"], "accuracy": undef["accuracy"]},
        "defended_full": {"f1": def_full["f1"], "fpr": def_full["fpr"], "accuracy": def_full["accuracy"]},
        "recovery_R": round(rec, 4),
    }
    poison_results.append(res)
    _done_counts.add(n_poison_abs)
    print(
        f"  Undef F1={undef['f1']:.4f} FPR={undef['fpr']:.4f} | "
        f"Def F1={def_full['f1']:.4f} FPR={def_full['fpr']:.4f} | R={rec:.3f}"
    )
    save_ckpt("poison_sweep_summary", {
        "clean_undef": clean_undef, "clean_def": clean_def,
        "latency_results": latency_results, "poison_results": poison_results,
    })
    with open(RES_DIR / f"checkpoint_{RUN_ID}_seed{SEED}.json", "w") as f:
        json.dump(
            {"clean_undef": clean_undef, "clean_def": clean_def, "poison_results": poison_results},
            f, indent=2, default=str,
        )

print("\n=== LOW-VOLUME POISON SWEEP DONE ===")
print(f"{'n':>4} {'equiv%':>8} {'Undef_F1':>10} {'Undef_FPR':>10} {'Def_F1':>10} {'Def_FPR':>10} {'R':>8}")
for r in poison_results:
    eq = 100.0 * float(r.get("poison_rate_equiv") or 0.0)
    print(
        f"{r['n_poison_abs']:>4d} {eq:>7.3f}% {r['undefended']['f1']:>10.4f} {r['undefended']['fpr']:>10.4f}"
        f" {r['defended_full']['f1']:>10.4f} {r['defended_full']['fpr']:>10.4f} {r['recovery_R']:>8.3f}"
    )
'''
patched_sweep = False
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = cell_src(i)
    if "for p_rate in POISON_RATES:" not in src or "craft_poison_docs" not in src:
        continue
    set_src(i, CELL_SWEEP)
    compile("".join(nb["cells"][i]["source"]), f"cell{i}", "exec")
    patched_sweep = True
    print(f"Rewrote poison sweep cell {i} (full count-based template)")
    break
assert patched_sweep, "poison sweep cell not found — expected 'for p_rate in POISON_RATES:'"

# --- Patch poison plot cell: x-axis was "poison_rate" (always None for CEXP08
# entries), so `pct = [r * 100 for r in rates]` crashes with a TypeError on
# None * 100 — 100% reproducible, even in SMOKE_TEST, and it runs before the
# final results-JSON save cell. Found during pre-run review; switch x-axis to
# n_poison_abs (see 04_ROUND2_VERSION_LOG.md R2-P3.4). ---
patched_plot = False
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = cell_src(i)
    if 'r["poison_rate"] for r in poison_results' not in src:
        continue
    src2 = src.replace(
        '# Plot F1 / FPR vs poison rate\n'
        'rates = [r["poison_rate"] for r in poison_results]\n'
        'pct = [r * 100 for r in rates]\n',
        '# Plot F1 / FPR vs poison count (absolute docs, Major 5 low-volume)\n'
        'counts = [r["n_poison_abs"] for r in poison_results]\n',
    )
    src2 = src2.replace("axes[0].plot(pct, f1_u,", "axes[0].plot(counts, f1_u,")
    src2 = src2.replace("axes[0].plot(pct, f1_d,", "axes[0].plot(counts, f1_d,")
    src2 = src2.replace("axes[1].plot(pct, fpr_u,", "axes[1].plot(counts, fpr_u,")
    src2 = src2.replace("axes[1].plot(pct, fpr_d,", "axes[1].plot(counts, fpr_d,")
    src2 = src2.replace(
        'axes[0].set_xlabel("Poison rate (%)"); axes[0].set_ylabel("Macro F1"); '
        'axes[0].legend(); axes[0].set_title("F1 vs poison")',
        'axes[0].set_xlabel("Poison count (docs)"); axes[0].set_ylabel("Macro F1"); '
        'axes[0].legend(); axes[0].set_title("F1 vs low-volume poison count"); '
        'axes[0].set_xticks(counts)',
    )
    src2 = src2.replace(
        'axes[1].set_xlabel("Poison rate (%)"); axes[1].set_ylabel("FPR"); '
        'axes[1].legend(); axes[1].set_title("FPR vs poison")',
        'axes[1].set_xlabel("Poison count (docs)"); axes[1].set_ylabel("FPR"); '
        'axes[1].legend(); axes[1].set_title("FPR vs low-volume poison count"); '
        'axes[1].set_xticks(counts)',
    )
    assert "rates = [" not in src2 and "r * 100 for r in rates" not in src2, \
        "plot patch left a dangling 'rates'/pct reference — check replacement"
    set_src(i, src2)
    patched_plot = True
    print(f"Patched poison plot cell {i} (x-axis: poison_rate -> n_poison_abs)")
    break
assert patched_plot, "poison plot cell not found — expected to patch it"

# --- Skip injection cell body if present ---
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    src = cell_src(i)
    if "injection_results" in src and "INJECTION_PAYLOADS" in src and "for mode" in src:
        set_src(
            i,
            "injection_results = []\n"
            "print('CEXP08: injection skipped (poison-only Major 5 partial).')\n",
        )
        print(f"Stubbed injection cell {i}")
        break

# Save
OUT_NB.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print("Wrote", OUT_NB)

# README
(OUT_DIR / "README.md").write_text(
    """# CEXP08 — Low-Volume Poison (Major 5 partial)

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
python Experiment_Lab\\conf_track\\CEXP08_Low_Volume_Poison\\_build_cexp08.py
```
""",
    encoding="utf-8",
)
print("Wrote README")
