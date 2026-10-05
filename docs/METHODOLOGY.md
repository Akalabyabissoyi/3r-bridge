# Methodology

## Replacement ladder
Models are ordered in tiers from least to most animal-dependent: in silico, human 2D cells, human 3D/microphysiological,
non-protected organisms, ex vivo tissue, protected vertebrates.

## Scoring
- **Area score (0-3)** for each model and research area: unsuitable, partial, good, strong.
- **Requirements** (human biology, intact organism, behaviour, vertebrate physiology, throughput, long study, regulatory test
  guideline). Each unmet requirement removes one point. Missing a *hard* requirement (human, organism, behaviour, vertebrate)
  caps the verdict at "partial".
- **Verdict:** adequate (score 2-3), partial (1), unsuitable (0). The *lowest adequate* model is the first adequate one on the
  ladder; ties within a tier go to the higher score.

## Robustness
Each area score is moved by one point up or down, one model at a time, and the ladder re-run. The share of changes that
leave the recommendation unchanged is reported as high (>=90%), moderate (>=75%) or low. It measures sensitivity to scoring
error, not correctness.

## Sample size
Formulas from `statsmodels` (t-test, paired t-test, one-way ANOVA, normal approximation for proportions) and Schoenfeld's
formula for log-rank events. Rank-based tests add 15%. Attrition inflates by 1/(1 - dropout).
Validated against reference values in `tests/test_stats.py`. Always confirm designs with the NC3Rs Experimental Design Assistant.

## Limits
Scores are judgements, the catalogue is small, and regulatory notes are summaries. The tool supports discussion and does not replace
Named Persons, an AWERB, a statistician or the regulator.
