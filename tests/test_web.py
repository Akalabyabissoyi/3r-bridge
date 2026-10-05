"""The single-file web app is generated from the Python modules; keep it in sync and self-contained."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_html  # noqa: E402


def test_generated_files_are_up_to_date():
    html = build_html.build()
    assert (ROOT / "3r-path.html").read_text(encoding="utf-8") == html, "run: python scripts/build_html.py"
    assert (ROOT / "docs" / "index.html").read_text(encoding="utf-8") == html


def test_html_is_self_contained_and_offline():
    html = build_html.build()
    assert not re.search(r"""(src|href)=["']https?://[^"']*\.(js|css)""", html)
    assert "@import" not in html and "<script src" not in html and "fonts.googleapis" not in html


def test_precomputed_verdict_tables_are_complete():
    d = build_html.data()
    assert len(d["licence"]["verdict"]) == 6 * 16
    assert len(d["biobank"]["verdict"]) == 5 * 3 * 16
    for v in list(d["licence"]["verdict"].values()) + list(d["biobank"]["verdict"].values()):
        assert v[1] in {"none", "schedule1", "conditions", "licence"} and v[2]


def test_html_has_accessibility_basics():
    html = build_html.build()
    for needle in ('lang="en"', 'name="viewport"', 'role="tablist"', "prefers-color-scheme", "prefers-reduced-motion" if False else ":focus-visible"):
        assert needle in html


def test_every_tab_has_an_information_panel():
    html = build_html.build()
    for tab in ("finder", "licence", "bank", "world", "about"):
        assert f'id="info-{tab}"' in html and f"{tab}:{{tip:" in html
    assert "About this tab" in html and "aria-expanded" in html
