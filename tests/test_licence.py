from bridge.licence import licence_verdict, modules_for, pil_categories, readability


def test_flies_need_no_licence():
    assert licence_verdict("invert", True, True, False, False)[1] == "none"


def test_mouse_injection_is_regulated():
    assert licence_verdict("mammal_bird_reptile", True, True, False, False)[1] == "licence"


def test_larval_fish_before_feeding_not_protected():
    assert licence_verdict("fish_amph", False, True, False, False)[1] == "none"


def test_schedule1_only_not_regulated_but_flagged():
    assert licence_verdict("mammal_bird_reptile", True, False, False, True)[1] == "schedule1"


def test_harmful_ga_breeding_is_regulated():
    assert licence_verdict("mammal_bird_reptile", True, False, True, False)[1] == "licence"


def test_surgery_gives_category_c_and_modules():
    cats = pil_categories(["injection", "surgery"])
    assert cats == ["A", "B", "C"]
    assert modules_for(cats) == ["L", "E1", "PILA", "K", "20", "21", "22"]


def test_readability_flags_jargon():
    r = readability("We will use murine xenograft models in vivo. They are good.")
    words = [w for w, _ in r["jargon"]]
    assert "murine" in words and "in vivo" in words


def test_new_researcher_content():
    from bridge.licence import CHECKLIST_PIL, GLOSSARY, JOURNEY, STEP_STAGE, WORRIES
    for term in ("PIL", "PPL", "NTCO", "NACWO", "NVS", "Schedule 1", "Humane endpoint"):
        assert term in GLOSSARY
    assert len(STEP_STAGE) == 5 and max(STEP_STAGE) < len(JOURNEY)
    assert len(WORRIES) >= 5 and len(CHECKLIST_PIL) >= 5


def test_pil_sheet_builds():
    from datetime import date

    from bridge.guide_ui import _pil_docx
    data = _pil_docx({"Name": "Test", "Species": ["Mouse"]}, ["Injections"], ["A"],
                     [{"Module": "L", "Status": "Completed", "Provider": "X", "Date": date(2026, 1, 5)}], "Q?")
    assert data[:2] == b"PK"


def test_examples_complete():
    from bridge.examples import EXAMPLES
    assert len(EXAMPLES) == 3
    for e in EXAMPLES:
        assert sum(e["severity"].values()) == 100
        heads = [h for h, _, _ in e["sections"]]
        assert {"Replacement", "Reduction", "Refinement"} <= set(heads)
        assert all(t and tip for _, t, tip in e["sections"])
