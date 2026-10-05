import re

from bridge import art, ui
from bridge.examples import EXAMPLES


def test_every_tier_has_image_art_with_alt_text():
    for fn in art.TIER_ART.values():
        img = fn(40)
        assert img.startswith("<img") and 'alt="' in img and 'alt=""' not in img


def test_worked_examples_have_credit_and_text():
    assert EXAMPLES and all(e for e in EXAMPLES)


def test_ui_css_defines_focus_and_reduced_motion():
    assert ":focus-visible" in ui.CSS and "prefers-reduced-motion" in ui.CSS
    assert re.search(r"--ink-3:#[0-9A-Fa-f]{6}", ui.CSS)
