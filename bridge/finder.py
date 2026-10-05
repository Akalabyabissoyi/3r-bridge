"""Scoring, sample size and report logic for the Model Finder."""
from __future__ import annotations

from datetime import date

from .catalogue import AREAS, DATA_VERSION, MODELS, REFERENCES, REQUIREMENTS, TIER_NAMES
from .stats import n_per_group  # noqa: F401  (re-exported: kept here for backward compatibility)

ADEQUATE, PARTIAL, UNSUITABLE = "adequate", "partial", "unsuitable"

# Requirements a model must meet to be called adequate: missing one is a dealbreaker, not a deduction.
HARD = {"human", "organism", "behaviour", "vertebrate"}


def assess(area: str, needs: list[str], overrides: dict[str, int] | None = None) -> list[dict]:
    """Return every model with a fit score, a verdict and the reasons behind it.

    The score starts from the model's suitability for the research area (0-3).
    Each requirement the model cannot meet removes one point and is recorded
    as a reason, so the user can see exactly why a model fell off the ladder.
    A model that misses a hard requirement (human biology, intact organism,
    behaviour, vertebrate physiology) can be partly suitable at best.

    `overrides` maps a model key to a user-chosen area score (0-3) that replaces the catalogue value.
    """
    overrides = overrides or {}
    out = []
    for m in MODELS:
        base = overrides.get(m["key"], m["scores"][area])
        if not 0 <= base <= 3:
            raise ValueError(f"override for {m['key']} must be between 0 and 3")
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
        out.append({**m, "base": base, "score": score, "gaps": gaps, "verdict": verdict,
                    "overridden": m["key"] in overrides})
    return sorted(out, key=lambda r: (r["tier"], -r["score"]))


def lowest_adequate(results: list[dict]) -> dict | None:
    """The first model on the ladder that can answer the question: the 3Rs choice."""
    for r in results:
        if r["verdict"] == ADEQUATE:
            return r
    return None


def robustness(area: str, needs: list[str], overrides: dict[str, int] | None = None) -> dict:
    """How stable is the recommendation if the expert scores are slightly wrong?

    Every model's area score is nudged by one point up or down (one model at a time, within 0-3) and the
    ladder is re-run. `stable` is the share of those nudges that leave the lowest adequate model unchanged.
    A low value means the answer rests on a close call and deserves more expert discussion.
    """
    base = lowest_adequate(assess(area, needs, overrides))
    base_key = base["key"] if base else None
    current = {m["key"]: (overrides or {}).get(m["key"], m["scores"][area]) for m in MODELS}
    same = total = 0
    flips: list[str] = []
    for key, score in current.items():
        for delta in (-1, 1):
            new = score + delta
            if not 0 <= new <= 3:
                continue
            alt = lowest_adequate(assess(area, needs, {**current, key: new}))
            total += 1
            if (alt["key"] if alt else None) == base_key:
                same += 1
            else:
                flips.append(f"{key} {score}->{new}")
    stable = same / total if total else 1.0
    label = "high" if stable >= 0.9 else "moderate" if stable >= 0.75 else "low"
    return {"stable": stable, "label": label, "n_tests": total, "flips": flips}


def report(question: str, area: str, needs: list[str], results: list[dict], choice: dict | None,
           ss: dict | None, refinements: list[str], robust: dict | None = None,
           override_reasons: dict[str, str] | None = None) -> str:
    """Markdown summary structured along PREPARE / ARRIVE lines, for a project plan or AWERB."""
    L = ["# 3Rs justification summary", "", f"_Generated with 3R Bridge on {date.today():%d %B %Y}. "
         f"A decision aid to support discussion, not regulatory advice. Catalogue version {DATA_VERSION}._", "",
         "## Research question", "", question or "(not given)", "",
         f"**Research area:** {AREAS[area]}", ""]
    if needs:
        L += ["**Requirements:**", ""] + [f"- {REQUIREMENTS[n]}" for n in needs] + [""]
    L += ["## Replacement", ""]
    if choice:
        L += [f"**Lowest adequate model on the ladder:** {choice['name']} ({TIER_NAMES[choice['tier']]}).",
              f"Regulatory status: {choice['status']}", ""]
        if choice.get("evidence"):
            L += ["Supporting literature for this model:", ""] + [f"- {e}" for e in choice["evidence"]] + [""]
    else:
        L += ["No model met every requirement. Consider splitting the question so earlier steps use non-animal methods.", ""]
    if robust:
        L += ["", f"**Robustness of this recommendation: {robust['label']}** "
              f"({robust['stable']:.0%} of {robust['n_tests']} one-point score changes leave it unchanged). "
              "The catalogue scores are expert judgements; a low value means the choice is a close call."]
        if robust["flips"]:
            L += ["", "It would change if: " + ", ".join(robust["flips"]) + "."]
    if override_reasons:
        L += ["", "**Scores changed by the user:**", ""]
        L += [f"- {k}: {why or '(no reason given)'}" for k, why in override_reasons.items()]
    L += ["", "| Tier | Model | Verdict | Why |", "|---|---|---|---|"]
    for r in results:
        why = "; ".join(r["gaps"]) if r["gaps"] else ("Not suited to this research area" if r["base"] == 0 else "Meets the stated requirements")
        L.append(f"| {TIER_NAMES[r['tier']]} | {r['name']} | {r['verdict']} | {why} |")
    L += ["", "## Reduction", ""]
    if ss and ss.get("text"):
        L += [ss["text"], "Check the design and analysis with the NC3Rs Experimental Design Assistant.", ""]
    elif ss:
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
