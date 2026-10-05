"""Run the whole Streamlit app headlessly and click through the main paths."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from bridge import stats


@pytest.fixture
def app():
    return AppTest.from_file(str(Path(__file__).resolve().parent.parent / "app.py"), default_timeout=60).run()


def test_app_starts_without_errors(app):
    assert not app.exception


@pytest.mark.parametrize("design", list(stats.DESIGNS))
def test_every_study_design_renders(app, design):
    [s for s in app.selectbox if s.label == "Study design"][0].set_value(design).run()
    assert not app.exception


def test_score_override_is_accepted(app):
    [s for s in app.selectbox if s.label.startswith("Human cell lines")][0].set_value(3).run()
    assert not app.exception
