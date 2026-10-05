# Changelog

All notable changes are listed here. The catalogue (`bridge/data/models.json`) is versioned with the package.

## 0.2.0 - 2026-10-05

### Added
- Catalogue moved to versioned data (`bridge/data/models.json`) with supporting literature and a review record per model.
- Sample-size calculators for paired, ANOVA, proportions and survival designs; unequal groups, rank-based allowance and attrition.
- Editable scores with a recorded reason, and a robustness check showing how stable a recommendation is.
- Word and JSON exports alongside Markdown; evidence and robustness appear in every export.
- "Other regulations" tab: EU, US and OECD/ICH orientation notes.
- Command-line interface (`python -m bridge`), installable package (`pyproject.toml`), Dockerfile.
- CI (tests on Python 3.10-3.13, lint, Docker build), monthly review-freshness check, Dependabot.
- Data-validation, export, statistics, CLI and headless app tests.
- Community files: contributing guide, code of conduct, issue and PR templates, expert-review protocol, privacy and
  methodology notes, JOSS paper draft.

### Changed
- Raised contrast of secondary text to meet WCAG AA; added visible keyboard focus and reduced-motion support.

## 0.1.0
- Model Finder, Licence Guide and Biobank Guide.
