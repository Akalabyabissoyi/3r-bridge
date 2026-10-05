from bridge.catalogue import AREAS, MODELS, REQUIREMENTS
from bridge.finder import assess, lowest_adequate, n_per_group, report


def test_every_model_scores_every_area_and_requirement():
    for m in MODELS:
        assert set(m["scores"]) == set(AREAS)
        assert set(m["provides"]) == set(REQUIREMENTS)


def test_liver_question_starts_below_animals():
    pick = lowest_adequate(assess("hepatotox", ["human"]))
    assert pick is not None and pick["tier"] < 5


def test_vertebrate_whole_body_question_reaches_animals():
    pick = lowest_adequate(assess("pk", ["organism", "vertebrate", "longterm"]))
    assert pick is not None and pick["key"] == "rodent"


def test_sensory_behaviour_question_lands_on_non_protected_organism():
    pick = lowest_adequate(assess("sensory", ["organism", "behaviour"]))
    assert pick["tier"] == 3


def test_sample_size_known_value():
    # d = 1.0, alpha 0.05, power 0.8 -> 17 per group (two-sided t-test)
    assert n_per_group(1.0, 1.0) == 17


def test_report_contains_sections():
    res = assess("gut", [])
    md = report("q", "gut", [], res, lowest_adequate(res), None, [])
    for h in ["## Replacement", "## Reduction", "## Refinement"]:
        assert h in md


def test_examples_land_on_expected_rungs():
    from bridge.catalogue import EXAMPLES
    expected = {"Liver injury": 2, "Cold avoidance": 3, "Tissue regrowth": 3, "Dose in the brain": 0,
                "Vaccine response": 5}
    for label, _, area, needs, _ in EXAMPLES:
        choice = lowest_adequate(assess(area, needs))
        assert choice is not None
        if label in expected:
            assert choice["tier"] == expected[label], label


def test_missing_hard_requirement_is_never_adequate():
    for r in assess("hepatotox", ["organism", "vertebrate"]):
        if r["verdict"] == "adequate":
            assert r["provides"]["organism"] and r["provides"]["vertebrate"]
