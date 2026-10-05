# Contributing

Thank you for helping. The most valuable contributions are **evidence**: a better citation, a corrected score, a missing
model, or an out-of-date regulatory statement.

## Quick start

```bash
git clone https://github.com/Akalabyabissoyi/3r-bridge.git && cd 3r-bridge
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q && ruff check .
streamlit run app.py
```

## Changing scores, models or regulatory text

1. Scores and model entries live in `bridge/data/models.json`. Scores run 0 (unsuitable) to 3 (strong).
2. Every change needs a source: a paper (DOI), an OECD Test Guideline, a validation body (for example EURL ECVAM) or
   regulator guidance. Add it to the model's `evidence` list, and explain the reasoning in `notes` if it is not obvious.
3. Update the model's `review.last_reviewed` (and the top-level `last_reviewed`) to the date you checked it.
4. Add a line to `CHANGELOG.md`. Tests in `tests/test_data.py` check that entries are complete.
5. Not sure of the change? Open an "Evidence or score update" issue instead, and an expert can pick it up.

Substantial changes to scores follow the process in [docs/EXPERT_REVIEW.md](docs/EXPERT_REVIEW.md).

## Code

- Keep logic in `bridge/` free of Streamlit so it can be used from the CLI and other tools; only `*_ui.py` and `app.py` import it.
- Add tests with every change. `tests/test_ui_smoke.py` runs the whole app headlessly.
- Plain, jargon-free English in the UI. Regulatory text is a learning aid, not legal advice: keep the disclaimers.

## Good first issues

Look for the `good first issue` label: adding a reference, a jurisdiction note, a calculator option, or an accessibility fix.
