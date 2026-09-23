"""CEXP07 — Rescore frozen RF/XGBoost on CEXP04 eval_set_ids (Major 3).

CPU-only. Does not modify CEXP01 or Results/Baselines.
Writes to Results/ML_Subset_Eval/.
"""
from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

ROOT = Path(r"d:\LLM-IDS_RAG")
PROC_CIC = ROOT / "Experiment_Lab" / "Data" / "Processed" / "CIC"
RES_BASE = ROOT / "Experiment_Lab" / "conf_track" / "Results" / "Baselines"
OUT_DIR = ROOT / "Experiment_Lab" / "conf_track" / "Results" / "ML_Subset_Eval"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EVAL_ID_FILES = {
    42: ROOT
    / "Experiment_Lab"
    / "conf_track"
    / "Results"
    / "Ablation"
    / "CEXP05_Ablation"
    / "eval_set_ids_N499_seed42.json",
    123: ROOT
    / "Experiment_Lab"
    / "conf_track"
    / "Results"
    / "Scaled_Eval"
    / "CEXP04_ScaledEval_1223Seeds"
    / "eval_set_ids_N499_seed123.json",
    7: ROOT
    / "Experiment_Lab"
    / "conf_track"
    / "Results"
    / "Scaled_Eval"
    / "CEXpP04_7_Seed"
    / "CEXP04_Scaled_Eval_7seed"
    / "eval_set_ids_N499_seed7.json",
}

# CEXP04 clean undefended F1/FPR (same eval protocol) — from seed JSONs / aggregate
RAG_CLEAN = {
    42: {"f1": 0.2649, "fpr": 0.0745, "source": "CEXP04 recovered / CEXP05 clean undef"},
    123: {"f1": 0.2879, "fpr": 0.0748, "source": "CEXP04 seed123 clean undef"},
    7: {"f1": 0.2564, "fpr": 0.0750, "source": "CEXP04 seed7 clean undef"},
}


def evaluate(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    fp = cm.sum(axis=0) - np.diag(cm)
    tn = cm.sum() - (cm.sum(axis=0) + cm.sum(axis=1) - np.diag(cm))
    macro_fpr = float((fp / (fp + tn + 1e-9)).mean())
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "macro_f1": round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        "macro_precision": round(
            float(precision_score(y_true, y_pred, average="macro", zero_division=0)), 4
        ),
        "macro_recall": round(
            float(recall_score(y_true, y_pred, average="macro", zero_division=0)), 4
        ),
        "macro_fpr": round(macro_fpr, 4),
    }


def main():
    X_test = np.load(PROC_CIC / "X_test.npy")
    y_test = np.load(PROC_CIC / "y_test.npy")
    with open(PROC_CIC / "label_encoder_cic.pkl", "rb") as f:
        le = pickle.load(f)

    rf_path = RES_BASE / "rf_cic.pkl"
    xgb_path = RES_BASE / "xgb_cic.json"
    if not rf_path.exists():
        raise FileNotFoundError(f"Missing {rf_path} — retrain CEXP01 RF or restore pickle")
    if not xgb_path.exists():
        raise FileNotFoundError(f"Missing {xgb_path}")

    with open(rf_path, "rb") as f:
        rf = pickle.load(f)
    xgb_m = xgb.XGBClassifier()
    xgb_m.load_model(str(xgb_path))

    per_seed = []
    for seed, path in EVAL_ID_FILES.items():
        if not path.exists():
            print(f"SKIP seed={seed}: missing {path}")
            continue
        ev = json.loads(path.read_text(encoding="utf-8"))
        idx = np.asarray(ev["test_indices"], dtype=int)
        y_sub = y_test[idx]
        if "y" in ev:
            assert list(map(int, y_sub)) == list(map(int, ev["y"])), f"y mismatch seed={seed}"
        X_sub = X_test[idx]

        rf_m = evaluate(y_sub, rf.predict(X_sub))
        xgb_m_metrics = evaluate(y_sub, xgb_m.predict(X_sub))
        rag = RAG_CLEAN[seed]
        row = {
            "seed": seed,
            "n": int(len(idx)),
            "eval_set_ids": str(path.relative_to(ROOT)).replace("\\", "/"),
            "RandomForest": rf_m,
            "XGBoost": xgb_m_metrics,
            "RAG_IDS_clean_undef": {
                "macro_f1": rag["f1"],
                "macro_fpr": rag["fpr"],
                "note": rag["source"],
            },
        }
        per_seed.append(row)
        print(
            f"seed={seed} N={len(idx)}  "
            f"RF F1={rf_m['macro_f1']:.4f} FPR={rf_m['macro_fpr']:.4f}  "
            f"XGB F1={xgb_m_metrics['macro_f1']:.4f} FPR={xgb_m_metrics['macro_fpr']:.4f}  "
            f"RAG F1={rag['f1']:.4f} FPR={rag['fpr']:.4f}"
        )

    def mean_std(vals):
        a = np.asarray(vals, dtype=float)
        return {
            "mean": round(float(a.mean()), 4),
            "std": round(float(a.std(ddof=1)), 4) if len(a) > 1 else 0.0,
        }

    agg = {
        "experiment": "CEXP07_ML_Subset_Eval",
        "purpose": "Major 3 — RF/XGB on identical CEXP04 N=499 eval indices (3 seeds)",
        "models_source": {
            "rf": "Results/Baselines/rf_cic.pkl (frozen CEXP01)",
            "xgb": "Results/Baselines/xgb_cic.json (frozen CEXP01)",
        },
        "full_partition_reference_do_not_mix": {
            "note": "CEXP01 full 708k test — kept for characterization only",
            "RF_macro_f1": 0.4678,
            "XGBoost_macro_f1": 0.4752,
        },
        "per_seed": per_seed,
        "aggregate": {
            "RandomForest": {
                "macro_f1": mean_std([r["RandomForest"]["macro_f1"] for r in per_seed]),
                "macro_fpr": mean_std([r["RandomForest"]["macro_fpr"] for r in per_seed]),
            },
            "XGBoost": {
                "macro_f1": mean_std([r["XGBoost"]["macro_f1"] for r in per_seed]),
                "macro_fpr": mean_std([r["XGBoost"]["macro_fpr"] for r in per_seed]),
            },
            "RAG_IDS_clean_undef": {
                "macro_f1": mean_std([r["RAG_IDS_clean_undef"]["macro_f1"] for r in per_seed]),
                "macro_fpr": mean_std([r["RAG_IDS_clean_undef"]["macro_fpr"] for r in per_seed]),
            },
        },
    }

    out = OUT_DIR / "cexp07_ml_subset_3seeds.json"
    out.write_text(json.dumps(agg, indent=2), encoding="utf-8")
    print("Wrote", out)

    # paper-ready markdown
    md = []
    md.append("# CEXP07 — Same-set ML vs RAG (Major 3)\n")
    md.append("RF/XGB scored on **identical** CEXP04 `eval_set_ids` (N=499, seeds 42/123/7).\n")
    md.append("| Model | Macro F1 (mean±std) | Macro FPR (mean±std) |")
    md.append("|-------|---------------------|----------------------|")
    for name, key in [
        ("Random Forest", "RandomForest"),
        ("XGBoost", "XGBoost"),
        ("RAG-IDS (clean undef, CEXP04)", "RAG_IDS_clean_undef"),
    ]:
        f1 = agg["aggregate"][key]["macro_f1"]
        fpr = agg["aggregate"][key]["macro_fpr"]
        md.append(f"| {name} | {f1['mean']:.4f}±{f1['std']:.4f} | {fpr['mean']:.4f}±{fpr['std']:.4f} |")
    md.append(
        "\nFull-partition CEXP01 numbers (RF 0.468 / XGB 0.475) are **not** mixed into this table.\n"
    )
    (OUT_DIR / "FINDINGS.md").write_text("\n".join(md), encoding="utf-8")
    notes = (
        ROOT
        / "Paper_Writing"
        / "conf"
        / "round2_notes"
        / "04_CEXP07_ML_Subset"
    )
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "FINDINGS.md").write_text("\n".join(md), encoding="utf-8")
    print("Wrote FINDINGS.md")


if __name__ == "__main__":
    main()
