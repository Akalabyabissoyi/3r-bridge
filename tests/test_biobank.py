from bridge.biobank import biobank_verdict


def test_cell_line_not_relevant_material():
    assert biobank_verdict("cell_line")[1] == "none"


def test_rtb_nonidentifiable_needs_no_licence_but_agreement():
    head, level, needs = biobank_verdict("human_tissue", "rtb")
    assert level == "conditions" and any("supply agreement" in n for n in needs)


def test_rtb_identifiable_needs_project_rec():
    head, level, needs = biobank_verdict("human_tissue", "rtb", identifiable=True)
    assert "own ethical approval" in head


def test_unknown_source_needs_hta_licence():
    assert biobank_verdict("human_tissue", "other")[1] == "licence"


def test_patients_switch_regime():
    assert "human application" in biobank_verdict("cell_line", patients=True)[0]


def test_deceased_consent_flagged():
    assert any("died" in n for n in biobank_verdict("human_tissue", "rtb", deceased=True)[2])
