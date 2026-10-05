"""Summarise an expert-review round: python scripts/review_stats.py reviews/round1.csv

CSV columns: reviewer, model_key, area_key, score (0-3). Prints, for each model/area, the median score, spread,
agreement (share of reviewers within one point of the median) and where the catalogue score differs from the median.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bridge.catalogue import MODELS  # noqa: E402

CATALOGUE = {(m["key"], a): s for m in MODELS for a, s in m["scores"].items()}


def summarise(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for r in rows:
        score = int(r["score"])
        if not 0 <= score <= 3:
            raise ValueError(f"score out of range: {r}")
        groups[(r["model_key"], r["area_key"])].append(score)
    out = []
    for (model, area), scores in sorted(groups.items()):
        med = float(np.median(scores))
        out.append({"model": model, "area": area, "n": len(scores), "median": med,
                    "iqr": float(np.subtract(*np.percentile(scores, [75, 25]))),
                    "agreement": float(np.mean(np.abs(np.array(scores) - med) <= 1)),
                    "catalogue": CATALOGUE.get((model, area)),
                    "differs": CATALOGUE.get((model, area)) is not None and abs(med - CATALOGUE[(model, area)]) >= 1})
    return out


if __name__ == "__main__":
    with open(sys.argv[1], newline="", encoding="utf-8") as fh:
        res = summarise(list(csv.DictReader(fh)))
    print("model,area,n,median,iqr,agreement,catalogue,differs")
    for r in res:
        print(f"{r['model']},{r['area']},{r['n']},{r['median']},{r['iqr']},{r['agreement']:.2f},{r['catalogue']},{r['differs']}")
