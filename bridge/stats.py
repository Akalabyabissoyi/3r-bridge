"""Sample-size calculators for the Reduction step.

Each function returns the number needed *per group* (or, for survival, the total number of events and animals)
before any allowance for attrition. Use `inflate_for_attrition` afterwards. Treat results as a starting point
and check the design with the NC3Rs Experimental Design Assistant.
"""
from __future__ import annotations

import math

from scipy.stats import norm
from statsmodels.stats.power import FTestAnovaPower, NormalIndPower, TTestIndPower, TTestPower
from statsmodels.stats.proportion import proportion_effectsize

# Mann-Whitney U needs about 1/0.864 times the t-test sample size when data are normal (asymptotic relative
# efficiency 0.955 squared is the usual conservative rule: add ~15 percent).
NONPARAMETRIC_FACTOR = 1.15

DESIGNS = {
    "two_group": "Two groups, continuous outcome (t-test)",
    "paired": "Paired or before/after, continuous outcome (paired t-test)",
    "anova": "Three or more groups, continuous outcome (one-way ANOVA)",
    "proportions": "Two groups, yes/no outcome (compare proportions)",
    "survival": "Time to event, two groups (log-rank)",
}


def _positive(**kw: float) -> None:
    for k, v in kw.items():
        if v <= 0:
            raise ValueError(f"{k} must be positive")


def _check(alpha: float, power: float) -> None:
    if not 0 < alpha < 1 or not 0 < power < 1:
        raise ValueError("alpha and power must be between 0 and 1")


def n_per_group(diff: float, sd: float, alpha: float = 0.05, power: float = 0.8, ratio: float = 1.0) -> int:
    """Group 1 size for a two-sided, two-group t-test; group 2 has `ratio` x group 1 (ratio=1: equal groups)."""
    _positive(difference=diff, sd=sd, ratio=ratio)
    _check(alpha, power)
    n = TTestIndPower().solve_power(effect_size=diff / sd, alpha=alpha, power=power, ratio=ratio,
                                    alternative="two-sided")
    return int(math.ceil(n))


def n_paired(diff: float, sd_diff: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Number of pairs, where `sd_diff` is the SD of the within-pair differences."""
    _positive(difference=diff, sd_diff=sd_diff)
    _check(alpha, power)
    n = TTestPower().solve_power(effect_size=diff / sd_diff, alpha=alpha, power=power, alternative="two-sided")
    return int(math.ceil(n))


def n_anova(effect_f: float, groups: int, alpha: float = 0.05, power: float = 0.8) -> int:
    """Per-group size for a one-way ANOVA with Cohen's f (0.1 small, 0.25 medium, 0.4 large)."""
    _positive(effect_f=effect_f)
    _check(alpha, power)
    if groups < 3:
        raise ValueError("ANOVA needs at least 3 groups; use the two-group calculator for 2")
    total = FTestAnovaPower().solve_power(effect_size=effect_f, alpha=alpha, power=power, k_groups=groups)
    return int(math.ceil(total / groups))


def n_proportions(p1: float, p2: float, alpha: float = 0.05, power: float = 0.8, ratio: float = 1.0) -> int:
    """Group 1 size to detect p1 versus p2 (arcsine effect size, two-sided)."""
    if not (0 < p1 < 1 and 0 < p2 < 1) or p1 == p2:
        raise ValueError("p1 and p2 must be different proportions between 0 and 1")
    _positive(ratio=ratio)
    _check(alpha, power)
    n = NormalIndPower().solve_power(effect_size=abs(proportion_effectsize(p1, p2)), alpha=alpha, power=power,
                                     ratio=ratio, alternative="two-sided")
    return int(math.ceil(n))


def survival_events(hazard_ratio: float, alpha: float = 0.05, power: float = 0.8, allocation: float = 0.5) -> int:
    """Total events needed for a log-rank test (Schoenfeld). `allocation` is the fraction in group 1."""
    if hazard_ratio <= 0 or hazard_ratio == 1:
        raise ValueError("hazard ratio must be positive and not 1")
    if not 0 < allocation < 1:
        raise ValueError("allocation must be between 0 and 1")
    _check(alpha, power)
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return int(math.ceil(z**2 / (allocation * (1 - allocation) * math.log(hazard_ratio) ** 2)))


def nonparametric_n(n_parametric: int) -> int:
    """Inflate a t-test sample size when you plan a rank-based test (Mann-Whitney) instead."""
    return int(math.ceil(n_parametric * NONPARAMETRIC_FACTOR))


def inflate_for_attrition(n: int, dropout: float) -> int:
    """Enrol enough to still have `n` after a fraction `dropout` (0 to <1) is lost."""
    if not 0 <= dropout < 1:
        raise ValueError("dropout must be in [0, 1)")
    return int(math.ceil(n / (1 - dropout)))
