# RAG-IDS — Defending Retrieval-Augmented Intrusion Detection

**Paper:** _Defending Retrieval-Augmented Intrusion Detection Against Knowledge Poisoning and Prompt Injection_
**Venue:** IEEE Cyber Incident Response, Coordination, Containment & Control (CIC) 2026, Research Track — **accepted**
**Authors:** Kaysarul Anas Apurba, Md. Hasibul Hasan, Mahedee Zaman Moon, Sk. Md. Mizanur Rahman, Atsuo Inomata

This repository contains the code, configuration, and result artifacts needed
to reproduce the experiments in the paper. It is a curated public release cut
from a larger private research workspace. **The manuscript itself is not
included here** — read the published version at the venue (link/DOI to
follow once available in the IEEE proceedings).

## System overview

RAG-IDS is a three-tier multi-agent retrieval-augmented intrusion detection
pipeline (Detection → Reasoning → Response agents) with a retrieval-boundary
defense against knowledge poisoning and prompt injection:

- **D1** — soft trust-score filter
- **D2** — label-embedding consistency check (LECC)
- **D3** — prompt sanitizer (regex pattern bank + embedding similarity)

Evaluated on CIC-UNSW-NB15 using BGE-M3 + FAISS/BM25 hybrid retrieval and
Mistral-7B-Instruct (4-bit NF4 quantization).

## What's included

| Path             | Contents                                                        |
| ---------------- | ----------------------------------------------------------------|
| `notebooks/`     | CEXP01–CEXP08 experiment notebooks / scripts                    |
| `results/`       | Summary JSON + plots used in the paper (no raw per-query dumps) |
| `configs/`       | Shared experiment knobs (seeds, \(k\), poison rates, …)         |
| `docs/findings/` | Short per-experiment result write-ups                           |

## What's _not_ included

- The paper manuscript itself — see the published version at IEEE CIC 2026
  (link/DOI to follow once available)
- Private discussion notes / internal review drafts
- Journal-track (extended) experiments — in progress
- Literature PDF archive
- Fat checkpoints with full `y_true` / `y_pred` arrays (summaries only)

## Dataset

Experiments use **CIC-UNSW-NB15**. On Kaggle, attach the preprocessed dataset
**Preprocessed_CIC_UNSW**. Raw corpus citation appears in the paper.

## Quick start (Kaggle)

1. New notebook → GPU + Internet ON
2. Add dataset **Preprocessed_CIC_UNSW**
3. Upload the relevant notebook from `notebooks/`
4. Set `SMOKE_TEST=True` first, then full run (`SEED` ∈ {42, 123, 7})
5. Download `/kaggle/working/...` outputs into `results/`

See `notebooks/KAGGLE_RUN_CARDS.md` and per-experiment `README.md` files for
run-specific instructions.

## Experiments

| ID     | Role                                                           |
| ------ | ----------------------------------------------------------------|
| CEXP01 | ML baselines (Random Forest / XGBoost / CNN-LSTM)              |
| CEXP02 | Clean RAG-IDS characterization                                 |
| CEXP04 | Scaled poison + injection eval (3 seeds) — main adversarial tables |
| CEXP05 | Defense component ablation (D1/D2/D3, isolates LECC)           |
| CEXP06 | FilterRAG-style hard-filter external baseline                  |
| CEXP07 | Same-set ML rescoring on CEXP04 indices                        |
| CEXP08 | Low-volume poison probe (1–2 documents)                        |

## Citation

```bibtex
@inproceedings{apurba2026ragids,
  title     = {Defending Retrieval-Augmented Intrusion Detection Against
               Knowledge Poisoning and Prompt Injection},
  author    = {Apurba, Kaysarul Anas and Hasan, Md. Hasibul and Moon,
               Mahedee Zaman and Rahman, Sk. Md. Mizanur and Inomata, Atsuo},
  booktitle = {Proc. IEEE Cyber Incident Response, Coordination, Containment
               \& Control (CIC)},
  year      = {2026},
  note      = {To appear}
}
```

## License

Code and scripts: MIT (see `LICENSE`).
Dataset rights remain with the original CIC-UNSW-NB15 providers.

## Contact

Kaysarul Anas Apurba — kaysarulanas2@gmail.com
