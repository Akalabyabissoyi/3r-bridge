# Changelog

All notable changes are listed here. The catalogue (`bridge/data/models.json`) is versioned with the package.

## Unreleased
- Removed the personal email address from SECURITY.md, CODE_OF_CONDUCT.md and pyproject.toml; contact is through the GitHub profile.

## 0.2.0 - 2026-10-05

### Design
- Every tab of the web app has an "About this tab" panel (what it does, how to use it, good to know) and a hover tooltip.
- Professional redesign of the web app with a purple and gold palette inspired by the University of Manchester colours (no logo or crest; the footer states it is an independent tool), masthead, ladder illustration, sticky tabs, badges and a polished dark mode. Contrast checked to WCAG AA.

### Renamed
- 3R Bridge is now **3R Path** ("Pathway to the 3Rs"). Command: `3r-path`; web file: `3r-path.html`. The Python package is still `bridge` and the repository URL is unchanged.

### Added
- `3r-path.html`: a single-file, offline, no-install web version (Model Finder, Licence Guide, Biobank Guide, regulations), built by `scripts/build_html.py` from the same Python data; parity with the Python package is checked by `scripts/verify_web.js` and `tests/test_web.py`.
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
