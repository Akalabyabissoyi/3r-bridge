"""The catalogue is data: these tests fail if an entry is incomplete or stale in structure."""
from datetime import date

from bridge.catalogue import AREAS, DATA_LAST_REVIEWED, MODELS, REQUIREMENTS, TIER_NAMES


def test_unique_keys_and_valid_tiers():
    keys = [m["key"] for m in MODELS]
    assert len(keys) == len(set(keys))
    assert all(m["tier"] in TIER_NAMES for m in MODELS)


def test_scores_in_range_and_complete():
    for m in MODELS:
        assert set(m["scores"]) == set(AREAS)
        assert all(0 <= v <= 3 for v in m["scores"].values())
        assert set(m["provides"]) == set(REQUIREMENTS)
        assert all(v in (0, 1) for v in m["provides"].values())


def test_every_model_has_text_evidence_and_review_record():
    for m in MODELS:
        for field in ("name", "status", "strengths", "limits", "bankable"):
            assert m[field].strip(), (m["key"], field)
        assert m["evidence"], f"{m['key']} lacks supporting literature"
        assert m["review"]["status"] in {"author-judgement", "expert-reviewed"}
        date.fromisoformat(m["review"]["last_reviewed"])


def test_review_date_not_in_future():
    assert date.fromisoformat(DATA_LAST_REVIEWED) <= date.today()


def test_every_tier_has_a_model():
    assert {m["tier"] for m in MODELS} == set(TIER_NAMES)
