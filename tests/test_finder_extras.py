import json

from bridge.catalogue import EXAMPLES
from bridge.export import as_dict, as_docx, as_json
from bridge.finder import assess, lowest_adequate, report, robustness


def test_override_changes_pick_and_is_flagged():
    base = lowest_adequate(assess("hepatotox", ["human"]))
    res = assess("hepatotox", ["human"], {"insilico": 3})
    assert lowest_adequate(res)["key"] == "insilico" != base["key"]
    assert [r["overridden"] for r in res if r["key"] == "insilico"] == [True]


def test_override_validated():
    import pytest
    with pytest.raises(ValueError):
        assess("gut", [], {"insilico": 4})


def test_robustness_shape_and_range():
    for _, _, area, needs, _ in EXAMPLES:
        r = robustness(area, needs)
        assert 0 <= r["stable"] <= 1 and r["label"] in {"high", "moderate", "low"} and r["n_tests"] > 0


def test_close_call_is_less_robust_than_clear_cut():
    assert robustness("sensory", ["organism", "behaviour"])["stable"] >= robustness("gut", [])["stable"]


def _pack(area="gut", needs=()):
    needs = list(needs)
    res = assess(area, needs)
    return ("q", area, needs, res, lowest_adequate(res), None, ["x"], robustness(area, needs), {"M": "why"})


def test_exports_roundtrip():
    data = json.loads(as_json(*_pack()))
    assert data["lowest_adequate_model"]["key"] == "barrier" and data["score_overrides"] == {"M": "why"}
    assert as_docx(*_pack())[:2] == b"PK"  # a docx is a zip file
    assert as_dict(*_pack())["ladder"][0]["evidence"] is not None


def test_report_mentions_robustness_evidence_and_overrides():
    md = report(*_pack())
    assert "Robustness" in md and "Supporting literature" in md and "Scores changed by the user" in md
