"""Command-line interface: `python -m bridge find ...` and `python -m bridge samplesize ...`."""
from __future__ import annotations

import argparse
import json
import sys

from . import stats
from .catalogue import AREAS, REQUIREMENTS
from .export import as_dict
from .finder import assess, lowest_adequate, report, robustness


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="3r-bridge", description="Choose the least sentient adequate research model.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("find", help="Climb the replacement ladder for a research question")
    f.add_argument("--area", required=True, choices=sorted(AREAS), help="; ".join(f"{k}={v}" for k, v in AREAS.items()))
    f.add_argument("--need", action="append", default=[], choices=sorted(REQUIREMENTS), help="repeatable")
    f.add_argument("--question", default="")
    f.add_argument("--format", choices=["text", "json", "markdown"], default="text")

    s = sub.add_parser("samplesize", help="Sample size for common designs")
    s.add_argument("design", choices=["two_group", "paired", "anova", "proportions", "survival"])
    s.add_argument("--diff", type=float)
    s.add_argument("--sd", type=float)
    s.add_argument("--effect-f", type=float)
    s.add_argument("--groups", type=int, default=3)
    s.add_argument("--p1", type=float)
    s.add_argument("--p2", type=float)
    s.add_argument("--hr", type=float)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s.add_argument("--dropout", type=float, default=0.0)

    a = ap.parse_args(argv)
    try:
        if a.cmd == "find":
            res = assess(a.area, a.need)
            pick = lowest_adequate(res)
            rob = robustness(a.area, a.need)
            if a.format == "json":
                print(json.dumps(as_dict(a.question, a.area, a.need, res, pick, None, [], rob), indent=2))
            elif a.format == "markdown":
                print(report(a.question, a.area, a.need, res, pick, None, [], rob))
            else:
                print(f"Lowest adequate model: {pick['name'] if pick else 'none'} (robustness: {rob['label']})")
                for r in res:
                    print(f"  tier {r['tier']}  {r['verdict']:<10} {r['name']}")
            return 0
        need = {"two_group": ("diff", "sd"), "paired": ("diff", "sd"), "anova": ("effect_f",),
                "proportions": ("p1", "p2"), "survival": ("hr",)}[a.design]
        missing = [n for n in need if getattr(a, n) is None]
        if missing:
            ap.error(f"{a.design} needs " + ", ".join("--" + m.replace("_", "-") for m in missing))
        if a.design == "two_group":
            n = stats.n_per_group(a.diff, a.sd, a.alpha, a.power)
        elif a.design == "paired":
            n = stats.n_paired(a.diff, a.sd, a.alpha, a.power)
        elif a.design == "anova":
            n = stats.n_anova(a.effect_f, a.groups, a.alpha, a.power)
        elif a.design == "proportions":
            n = stats.n_proportions(a.p1, a.p2, a.alpha, a.power)
        else:
            n = stats.survival_events(a.hr, a.alpha, a.power)
        unit = "events (total)" if a.design == "survival" else "pairs" if a.design == "paired" else "per group"
        print(f"{n} {unit}; with {a.dropout:.0%} attrition: {stats.inflate_for_attrition(n, a.dropout)}")
        return 0
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
