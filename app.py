"""3R Bridge: choose, preserve and justify the least sentient model that can answer a question."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from bridge.catalogue import AREAS, EXAMPLES, REQUIREMENTS, REFINEMENTS, TIER_NAMES
from bridge.finder import ADEQUATE, PARTIAL, assess, lowest_adequate, n_per_group, report
from bridge import ui

st.set_page_config(page_title="3R Bridge", page_icon="🪜", layout="wide", initial_sidebar_state="collapsed")

SHORT = {0: "In silico", 1: "2D cells", 2: "3D human", 3: "Non-protected", 4: "Ex vivo", 5: "ASPA-protected"}
COLOURS = {ADEQUATE: "#1F6F63", PARTIAL: "#E2A33A", "unsuitable": "#C9D1CE"}

ui.inject_css()
ui.hero()

tab_finder, tab_guide, tab_bank = st.tabs(["Model Finder", "Licence Guide", "Biobank Guide"])

# ------------------------------------------------------------------ Model Finder
EX = {e[0]: e for e in EXAMPLES}
st.session_state.setdefault("mf_question", EXAMPLES[0][1])
st.session_state.setdefault("mf_area", EXAMPLES[0][2])


def load_example():
    label = st.session_state.get("mf_example")
    if not label:
        return
    _, q, a, needs, _ = EX[label]
    st.session_state["mf_question"] = q
    st.session_state["mf_area"] = a
    for k in REQUIREMENTS:
        st.session_state[f"need_{k}"] = k in needs


with tab_finder:
    st.pills("Try an example: click one and the ladder answers it", list(EX), key="mf_example", on_change=load_example)
    active = EX.get(st.session_state.get("mf_example"))
    if active and active[1] == st.session_state["mf_question"]:
        st.caption(f"Why: {active[4]}")
    left, right = st.columns([1, 1.6], gap="large")

    with left:
        st.subheader("1. Describe the question")
        question = st.text_area("Research question", key="mf_question", height=80)
        area = st.selectbox("Research area", list(AREAS), format_func=AREAS.get, key="mf_area")
        needs = [k for k, v in REQUIREMENTS.items() if st.checkbox(v, key=f"need_{k}")]

    results = assess(area, needs)
    choice = lowest_adequate(results)

    with right:
        st.subheader("2. Climb the replacement ladder")
        ui.pick_card(choice)
        ui.ladder(results, choice)

    with st.expander("See the fit scores behind the ladder"):
        # Ladder chart: one bar per model, grouped by tier, coloured by verdict.
        names = [r["name"] for r in results][::-1]
        fig = go.Figure(go.Bar(
            x=[max(r["score"], 0.15) for r in results][::-1],
            y=names,
            orientation="h",
            marker_color=[COLOURS[r["verdict"]] for r in results][::-1],
            customdata=[[TIER_NAMES[r["tier"]], r["verdict"], "; ".join(r["gaps"]) or "none"] for r in results][::-1],
            hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>Verdict: %{customdata[1]}<br>Unmet: %{customdata[2]}<extra></extra>",
        ))
        # Grey bands and labels mark each rung (tier) of the ladder.
        rev = results[::-1]
        start = 0
        for i in range(1, len(rev) + 1):
            if i == len(rev) or rev[i]["tier"] != rev[start]["tier"]:
                if rev[start]["tier"] % 2 == 0:
                    fig.add_shape(type="rect", xref="paper", x0=0, x1=1, yref="y",
                                  y0=start - 0.5, y1=i - 0.5, fillcolor="rgba(120,130,120,0.08)",
                                  line_width=0, layer="below")
                fig.add_annotation(xref="x", x=4.45, y=(start + i - 1) / 2, yref="y",
                                   text=SHORT[rev[start]["tier"]], showarrow=False,
                                   xanchor="right", font=dict(size=10, color="#7E887F"))
                start = i
        fig.update_layout(
            height=470, margin=dict(l=10, r=10, t=10, b=30),
            xaxis=dict(title="Fit for this question (0 to 3)", range=[0, 4.5], tickvals=[0, 1, 2, 3]),
            yaxis=dict(automargin=True), plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, width="stretch")
        st.caption("Fit for this question, from 0 (unsuitable) to 3 (strong). Each requirement a model "
                   "cannot meet removes a point.")

    st.subheader("Why each model fits, or does not")
    for tier in sorted(TIER_NAMES):
        group = [r for r in results if r["tier"] == tier]
        if not group:
            continue
        st.markdown(f"#### {TIER_NAMES[tier]}")
        for r in group:
            colour = COLOURS[r["verdict"]]
            with st.expander(f"{r['name']}: {r['verdict']}"):
                st.markdown(f"**Regulatory status.** {r['status']}")
                st.markdown(f"**Strengths.** {r['strengths']}")
                st.markdown(f"**Limits.** {r['limits']}")
                st.markdown(f"**Can it be banked?** {r['bankable']}")
                if r["gaps"]:
                    st.markdown("**Requirements it cannot meet:** " + "; ".join(r["gaps"]))
                elif r["base"] == 0:
                    st.markdown("**Not suited to this research area.**")

    st.divider()
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("3. Reduction: how many per group?")
        st.caption("Two-group comparison, two-sided t-test. Use a pilot or published data for the SD.")
        diff = st.number_input("Smallest difference worth detecting", min_value=0.01, value=20.0)
        sd = st.number_input("Expected standard deviation", min_value=0.01, value=15.0)
        a1, a2 = st.columns(2)
        alpha = a1.selectbox("Significance level", [0.05, 0.01], index=0)
        power = a2.selectbox("Power", [0.8, 0.85, 0.9], index=0)
        n = n_per_group(diff, sd, alpha, power)
        st.metric("Needed per group", n, help=f"{2*n} in total")
        sds = np.linspace(max(sd * 0.4, 0.01), sd * 1.6, 25)
        ns = [n_per_group(diff, s, alpha, power) for s in sds]
        f2 = go.Figure(go.Scatter(x=sds, y=ns, mode="lines", line=dict(width=3, color="#1F6F63"), fill="tozeroy", fillcolor="rgba(31,111,99,.08)"))
        f2.add_trace(go.Scatter(x=[sd], y=[n], mode="markers", marker=dict(size=13, color="#E2A33A", line=dict(width=2, color="#18322E"))))
        f2.update_layout(height=260, showlegend=False, margin=dict(l=10, r=10, t=10, b=30),
                         xaxis_title="Standard deviation", yaxis_title="n per group",
                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(f2, width="stretch")
        st.caption("Less variability means fewer animals: refinements such as better handling, "
                   "standardised housing and repeated imaging often reduce SD.")
        ss = dict(diff=diff, sd=sd, alpha=alpha, power=power, n=n)

    with c2:
        st.subheader("4. Refinement checklist")
        if choice and choice["tier"] < 5:
            st.caption("Your starting model is not a protected animal. The list applies if later steps need animals.")
        picked = [x for x in REFINEMENTS if st.checkbox(x, key=f"ref_{x}")]

    st.divider()
    st.subheader("5. Export the justification")
    md = report(question, area, needs, results, choice, ss, picked)
    st.download_button("Download summary (Markdown)", md, file_name="3Rs_justification.md", mime="text/markdown")
    with st.expander("Preview"):
        st.markdown(md)

    st.html('<p class="rb-foot">3R Bridge is a decision aid for discussion with Named Persons and ethical review bodies. '
            'It does not replace licensing, veterinary or AWERB advice.</p>')

# ------------------------------------------------------------------ Licence Guide
with tab_guide:
    from bridge.guide_ui import render_guide
    render_guide(results=results, choice=choice, ss=ss, refinements=picked, question=question)

# ------------------------------------------------------------------ Biobank Guide
with tab_bank:
    from bridge.biobank_ui import render_biobank
    render_biobank()
