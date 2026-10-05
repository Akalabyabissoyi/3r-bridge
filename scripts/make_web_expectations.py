"""Write Python reference results (ladder verdicts, robustness, sample sizes) for scripts/verify_web.js to compare against."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from bridge import stats  # noqa: E402
from bridge.catalogue import AREAS, REQUIREMENTS  # noqa: E402
from bridge.finder import assess, lowest_adequate, robustness  # noqa: E402

ex = {"stats": [], "ladder": []}
for d, sd, a, p, r in [(1, 1, .05, .8, 1), (20, 15, .05, .8, 1), (5, 3, .01, .9, 2), (0.3, 1, .05, .85, .5), (2, 1, .05, .8, 1), (10, 40, .05, .9, 1)]:
    ex["stats"].append(["two", [d, sd, a, p, r], stats.n_per_group(d, sd, a, p, r)])
for d, sd, a, p in [(1, 1, .05, .8), (0.5, 2, .01, .9), (3, 2, .05, .85)]:
    ex["stats"].append(["paired", [d, sd, a, p], stats.n_paired(d, sd, a, p)])
for f, k, a, p in [(.25, 3, .05, .8), (.4, 4, .01, .9), (.1, 5, .05, .8)]:
    ex["stats"].append(["anova", [f, k, a, p], stats.n_anova(f, k, a, p)])
for p1, p2, a, p, r in [(.5, .25, .05, .8, 1), (.9, .6, .01, .9, 1), (.2, .1, .05, .8, 2)]:
    ex["stats"].append(["props", [p1, p2, a, p, r], stats.n_proportions(p1, p2, a, p, r)])
for hr, a, p in [(.5, .05, .8), (.7, .01, .9), (2, .05, .85)]:
    ex["stats"].append(["events", [hr, a, p], stats.survival_events(hr, a, p)])
needs = list(REQUIREMENTS)
for area in AREAS:
    for mask in range(1 << len(needs)):
        ns = [n for i, n in enumerate(needs) if mask >> i & 1]
        res = assess(area, ns)
        pk = lowest_adequate(res)
        rb = robustness(area, ns)
        ex["ladder"].append([area, ns, [[r["key"], r["verdict"], r["score"]] for r in res],
                             pk["key"] if pk else None, round(rb["stable"], 6), rb["label"]])
json.dump(ex, sys.stdout)
