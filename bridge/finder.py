"""Scoring, sample size and report logic for the Model Finder."""
from __future__ import annotations

import math
from datetime import date

from statsmodels.stats.power import TTestIndPower

from .catalogue import AREAS, MODELS, REQUIREMENTS, TIER_NAMES, REFERENCES

ADEQUATE, PARTIAL, UNSUITABLE = "adequate", "partial", "unsuitable"

# Requirements a model must meet to be called adequate: missing one is a dealbreaker, not a deduction.
HARD = {"human", "organism", "behaviour", "vertebrate"}


def assess(area: str, needs: list[str]) -> list[dict]:
    """Return every model with a fit score, a verdict and the reasons behind it.

    The score starts from the model's suitability for the research area (0-3).
    Each requirement the model cannot meet removes one point and is recorded
    as a reason, so the user can see exactly why a model fell off the ladder.
    A model that misses a hard requirement (human biology, intact organism,
    behaviour, vertebrate physiology) can be partly suitable at best.
    """
    out = []
    for m in MODELS:
        base = m["scores"][area]
        missing = [n for n in needs if not m["provides"][n]]
        gaps = [REQUIREMENTS[n] for n in missing]
        score = max(0, base - len(gaps))
        if score >= 2 and HARD & set(missing):
            score = 1
        if base == 0:
            verdict = UNSUITABLE
        elif score >= 2:
            verdict = ADEQUATE
        elif score == 1:
            verdict = PARTIAL
        else:
            verdict = UNSUITABLE
        out.append({**m, "base": base, "score": score, "gaps": gaps, "verdict": verdict})
    return sorted(out, key=lambda r: (r["tier"], -r["score"]))


def lowest_adequate(results: list[dict]) -> dict | None:
    """The first model on the ladder that can answer the question: the 3Rs choice."""
    for r in results:
        if r["verdict"] == ADEQUATE:
            return r
    return None


def n_per_group(diff: float, sd: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Animals (or replicates) per group for a two-sided, two-group t-test."""
    if sd <= 0 or diff <= 0:
        raise ValueError("difference and SD must be positive")
    d = diff / sd
    n = TTestIndPower().solve_power(effect_size=d, alpha=alpha, power=power, alternative="two-sided")
    return int(math.ceil(n))


def report(question: str, area: str, needs: list[str], results: list[dict], choice: dict | None,
           ss: dict | None, refinements: list[str]) -> str:
    """Markdown summary structured along PREPARE / ARRIVE lines, for a project plan or AWERB."""
    L = [f"# 3Rs justification summary", "", f"_Generated with 3R Bridge on {date.today():%d %B %Y}. "
         "A decision aid to support discussion, not regulatory advice._", "",
         "## Research question", "", question or "(not given)", "",
         f"**Research area:** {AREAS[area]}", ""]
    if needs:
        L += ["**Requirements:**", ""] + [f"- {REQUIREMENTS[n]}" for n in needs] + [""]
    L += ["## Replacement", ""]
    if choice:
        L += [f"**Lowest adequate model on the ladder:** {choice['name']} ({TIER_NAMES[choice['tier']]}).",
              f"Regulatory status: {choice['status']}", ""]
    else:
        L += ["No model met every requirement. Consider splitting the question so earlier steps use non-animal methods.", ""]
    L += ["| Tier | Model | Verdict | Why |", "|---|---|---|---|"]
    for r in results:
        why = "; ".join(r["gaps"]) if r["gaps"] else ("Not suited to this research area" if r["base"] == 0 else "Meets the stated requirements")
        L.append(f"| {TIER_NAMES[r['tier']]} | {r['name']} | {r['verdict']} | {why} |")
    L += ["", "## Reduction", ""]
    if ss:
        L += [f"Two-group comparison, two-sided t-test: detect a difference of {ss['diff']} with SD {ss['sd']} "
              f"(effect size d = {ss['diff']/ss['sd']:.2f}), alpha {ss['alpha']}, power {ss['power']:.0%}: "
              f"**{ss['n']} per group**, {2*ss['n']} in total.",
              "Check the design and analysis with the NC3Rs Experimental Design Assistant.", ""]
    else:
        L += ["No sample size calculation entered.", ""]
    L += ["## Refinement", ""]
    L += [f"- [x] {x}" for x in refinements] if refinements else ["No refinements selected."]
    L += ["", "## References", ""] + [f"- {r}" for r in REFERENCES]
    return "\n".join(L)
