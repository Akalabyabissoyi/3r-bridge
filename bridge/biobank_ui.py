"""Streamlit interface for the Biobank Guide tab."""
from __future__ import annotations

import html

import streamlit as st

from . import art, ui
from .biobank import ASK_BIOBANK, FIND, MATERIALS, REFERENCES, SOURCES, WHO_HELPS, biobank_verdict

LEVEL_CLASS = {"none": "none", "conditions": "schedule1", "licence": "licence"}
MATERIAL_ART = {"human_tissue": art.tissue, "cell_line": art.cells2d, "hesc": art.spheroid,
                "acellular": art.insilico, "animal": art.mouse}
WHO_ART = [art.tissue, art.spheroid, art.insilico, art.cells2d, art.fly, art.insilico]


def render_biobank():
    ui.say("Human tissue and cells can replace animals in many studies, and biobanks make them available. "
           "They have their own rules, mostly about consent and storage. Let's work out what applies to you.")
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        material = st.radio("What will you use?", list(MATERIALS), format_func=MATERIALS.get, key="b_material")
        source, identifiable, deceased = "rtb", False, False
        if material == "human_tissue":
            source = st.radio("Where does it come from?", list(SOURCES), format_func=SOURCES.get, key="b_source")
            deceased = st.checkbox("Some donors have died", key="b_deceased")
        if material in ("human_tissue", "acellular", "cell_line"):
            identifiable = st.checkbox("The samples or linked data could identify donors to me", key="b_ident")
        patients = material != "animal" and st.checkbox("Cells or tissue will be used in patients", key="b_patients")
        gm = st.checkbox("I will genetically modify the cells", key="b_gm")
    headline, level, needs = biobank_verdict(material, source, identifiable, deceased, patients, gm)
    with right:
        items = "".join(f"<li>{html.escape(n)}</li>" for n in needs)
        st.html(f'<div class="rb-verdict {LEVEL_CLASS[level]}">{MATERIAL_ART[material](60)}'
                f'<div><h3>{html.escape(headline)}</h3><ul>{items}</ul></div></div>')
        st.caption("England, Wales and Northern Ireland. Scotland has its own Act; outside the UK, local law applies.")

    st.markdown("#### Before you order: questions to ask a biobank")
    st.caption("Approval is only half of it. How a sample was collected, frozen, stored and thawed decides whether "
               "your results mean anything.")
    rows = "".join(f'<div class="rb-ask"><b>{html.escape(k)}</b><span>{html.escape(q)}</span></div>' for k, q in ASK_BIOBANK)
    st.html(f'<div class="rb-asks">{rows}</div>')

    st.markdown("#### Who can help")
    cards = "".join(f'<div class="rb-person">{f(40)}<div><b>{html.escape(n)}</b><p>{html.escape(d)}</p></div></div>'
                    for (n, d), f in zip(WHO_HELPS, WHO_ART))
    st.html(f'<div class="rb-people">{cards}</div>')

    st.markdown("#### Where to find samples")
    links = "".join(f'<a class="rb-find" href="{u}" target="_blank" rel="noopener"><b>{html.escape(n)}</b>'
                    f'<span>{html.escape(d)}</span></a>' for n, u, d in FIND)
    st.html(f'<div class="rb-finds">{links}</div>')

    with st.expander("Sources"):
        for n, u in REFERENCES:
            st.markdown(f"- [{n}]({u})")
    st.html('<p class="rb-foot">This guide grew out of discussions on biobanking and post-thaw readiness at the '
            "SLTB 2026 pre-conference mini-symposium at BIOCEV, Czech Republic. A learning aid, not legal advice: "
            "your HTA Designated Individual and ethics committee have the final word.</p>")
