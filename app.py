"""3R Path: choose, preserve and justify the least sentient model that can answer a question."""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from bridge import stats, ui
from bridge.catalogue import (
    AREAS,
    EXAMPLES,
    MODELS,
    REFINEMENTS,
    REQUIREMENTS,
    TIER_NAMES,
)
from bridge.export import as_docx, as_json
from bridge.finder import ADEQUATE, PARTIAL, assess, lowest_adequate, report, robustness
from bridge.regions import LAST_REVIEWED as REGIONS_REVIEWED
from bridge.regions import REGIONS

st.set_page_config(page_title="3R Path", page_icon="🪜", layout="wide", initial_sidebar_state="collapsed")

SHORT = {0: "In silico", 1: "2D cells", 2: "3D human", 3: "Non-protected", 4: "Ex vivo", 5: "ASPA-protected"}
COLOURS = {ADEQUATE: "#1F6F63", PARTIAL: "#E2A33A", "unsuitable": "#C9D1CE"}

ui.inject_css()
ui.hero()

tab_finder, tab_guide, tab_bank, tab_world = st.tabs(["Model Finder", "Licence Guide", "Biobank Guide", "Other regulations"])

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

        overrides, reasons = {}, {}
        with st.expander("Disagree with a score? Change it"):
            st.caption("The catalogue scores are expert judgements. Set your own (0 unsuitable to 3 strong) for this "
                       "research area and say why; the change is recorded in the export.")
            for m in MODELS:
                base = m["scores"][area]
                c_a, c_b = st.columns([1, 1.4])
                val = c_a.selectbox(m["name"], [0, 1, 2, 3], index=base, key=f"ov_{area}_{m['key']}")
                if val != base:
                    overrides[m["key"]] = val
                    reasons[m["name"]] = c_b.text_input("Reason or source", key=f"ovr_{area}_{m['key']}")

    results = assess(area, needs, overrides)
    choice = lowest_adequate(results)
    robust = robustness(area, needs, overrides)

    with right:
        st.subheader("2. Climb the replacement ladder")
        ui.pick_card(choice)
        st.caption(f"Robustness: **{robust['label']}**. {robust['stable']:.0%} of one-point changes to the expert "
                   "scores leave this answer unchanged." + (f" It would change if: {', '.join(robust['flips'])}."
                                                            if robust["flips"] and robust["label"] != "high" else ""))
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
                if r.get("evidence"):
                    st.markdown("**Supporting literature.**\n" + "\n".join(f"- {e}" for e in r["evidence"]))
                if r["overridden"]:
                    st.markdown("**Score changed by you.**")
                if r["gaps"]:
                    st.markdown("**Requirements it cannot meet:** " + "; ".join(r["gaps"]))
                elif r["base"] == 0:
                    st.markdown("**Not suited to this research area.**")

    st.divider()
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("3. Reduction: how many animals?")
        st.caption("Pick the design that matches your main analysis. Use a pilot or published data for the SD.")
        design = st.selectbox("Study design", list(stats.DESIGNS), format_func=stats.DESIGNS.get)
        a1, a2 = st.columns(2)
        alpha = a1.selectbox("Significance level", [0.05, 0.01], index=0)
        power = a2.selectbox("Power", [0.8, 0.85, 0.9], index=0)
        dropout = st.slider("Allow for attrition (animals lost)", 0, 40, 0, format="%d%%") / 100
        diff = sd = None
        if design in ("two_group", "paired"):
            diff = st.number_input("Smallest difference worth detecting", min_value=0.01, value=20.0)
            sd = st.number_input("Expected standard deviation" + (" of the differences" if design == "paired" else ""),
                                 min_value=0.01, value=15.0)
        if design == "two_group":
            ratio = st.number_input("Group 2 size relative to group 1", min_value=0.25, max_value=4.0, value=1.0,
                                    step=0.25, help="1 means equal groups. Unequal groups need more animals in total.")
            ranks = st.checkbox("I will use a rank-based test (Mann-Whitney)")
            n = stats.n_per_group(diff, sd, alpha, power, ratio)
            if ranks:
                n = stats.nonparametric_n(n)
            n_eff = stats.inflate_for_attrition(n, dropout)
            total = n_eff + int(round(n_eff * ratio))
            unit, text = "per group (group 1)", (f"Two-group comparison, two-sided t-test{' with a rank-based test allowance' if ranks else ''}: "
                f"detect a difference of {diff} with SD {sd} (d = {diff/sd:.2f}), alpha {alpha}, power {power:.0%}, "
                f"group ratio 1:{ratio:g}: **{n} in group 1**; allowing {dropout:.0%} attrition, enrol {n_eff} and "
                f"{int(round(n_eff * ratio))} ({total} in total).")
        elif design == "paired":
            n = stats.n_paired(diff, sd, alpha, power)
            n_eff = stats.inflate_for_attrition(n, dropout)
            total, unit = n_eff, "pairs"
            text = (f"Paired design, two-sided paired t-test: detect a mean difference of {diff} with SD of differences {sd}, "
                    f"alpha {alpha}, power {power:.0%}: **{n} pairs**; allowing {dropout:.0%} attrition, enrol {n_eff}.")
        elif design == "anova":
            k = st.number_input("Number of groups", min_value=3, max_value=12, value=3)
            f = st.number_input("Effect size (Cohen's f)", min_value=0.05, max_value=1.0, value=0.25, step=0.05,
                                help="0.1 small, 0.25 medium, 0.4 large")
            n = stats.n_anova(f, int(k), alpha, power)
            n_eff = stats.inflate_for_attrition(n, dropout)
            total, unit = n_eff * int(k), "per group"
            text = (f"One-way ANOVA with {int(k)} groups: Cohen's f = {f}, alpha {alpha}, power {power:.0%}: "
                    f"**{n} per group**; allowing {dropout:.0%} attrition, enrol {n_eff} per group ({total} in total).")
        elif design == "proportions":
            p1 = st.number_input("Expected proportion, control", 0.01, 0.99, 0.5)
            p2 = st.number_input("Expected proportion, treated", 0.01, 0.99, 0.25)
            if p1 == p2:
                st.error("The two proportions must differ.")
                st.stop()
            n = stats.n_proportions(p1, p2, alpha, power)
            n_eff = stats.inflate_for_attrition(n, dropout)
            total, unit = 2 * n_eff, "per group"
            text = (f"Two proportions ({p1:.0%} versus {p2:.0%}), two-sided: alpha {alpha}, power {power:.0%}: "
                    f"**{n} per group**; allowing {dropout:.0%} attrition, enrol {n_eff} per group ({total} in total).")
        else:
            hr = st.number_input("Hazard ratio to detect", 0.05, 5.0, 0.5, step=0.05)
            if hr == 1:
                st.error("The hazard ratio must not be 1.")
                st.stop()
            n = stats.survival_events(hr, alpha, power)
            n_eff, total, unit = n, n, "events (total)"
            text = (f"Time to event, log-rank test: hazard ratio {hr}, alpha {alpha}, power {power:.0%}: "
                    f"**{n} events in total** (Schoenfeld). The number of animals depends on how many reach the event.")
        st.metric(f"Needed ({unit})", n_eff if design != "two_group" else n, help=f"{total} animals in total")
        if design == "two_group":
            sds = np.linspace(max(sd * 0.4, 0.01), sd * 1.6, 25)
            ns = [stats.n_per_group(diff, s_, alpha, power, ratio) for s_ in sds]
            f2 = go.Figure(go.Scatter(x=sds, y=ns, mode="lines", line=dict(width=3, color="#1F6F63"), fill="tozeroy", fillcolor="rgba(31,111,99,.08)"))
            f2.add_trace(go.Scatter(x=[sd], y=[stats.n_per_group(diff, sd, alpha, power, ratio)], mode="markers", marker=dict(size=13, color="#E2A33A", line=dict(width=2, color="#18322E"))))
            f2.update_layout(height=260, showlegend=False, margin=dict(l=10, r=10, t=10, b=30),
                             xaxis_title="Standard deviation", yaxis_title="n in group 1",
                             plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(f2, width="stretch")
            st.caption("Less variability means fewer animals: refinements such as better handling, "
                       "standardised housing and repeated imaging often reduce SD.")
        st.caption("Check the design and analysis with the [NC3Rs Experimental Design Assistant](https://eda.nc3rs.org.uk).")
        ss = dict(design=design, n=n, n_enrol=n_eff, total=total, alpha=alpha, power=power, dropout=dropout, text=text)
        if diff is not None:
            ss.update(diff=diff, sd=sd)

    with c2:
        st.subheader("4. Refinement checklist")
        if choice and choice["tier"] < 5:
            st.caption("Your starting model is not a protected animal. The list applies if later steps need animals.")
        picked = [x for x in REFINEMENTS if st.checkbox(x, key=f"ref_{x}")]

    st.divider()
    st.subheader("5. Export the justification")
    pack = (question, area, needs, results, choice, ss, picked, robust, reasons)
    md = report(*pack)
    d1, d2, d3 = st.columns(3)
    d1.download_button("Download summary (Markdown)", md, file_name="3Rs_justification.md", mime="text/markdown")
    d2.download_button("Download summary (Word)", as_docx(*pack), file_name="3Rs_justification.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    d3.download_button("Download data (JSON)", as_json(*pack), file_name="3Rs_justification.json",
                       mime="application/json")
    with st.expander("Preview"):
        st.markdown(md)

    st.html('<p class="rb-foot">3R Path is a decision aid for discussion with Named Persons and ethical review bodies. '
            'It does not replace licensing, veterinary or AWERB advice.</p>')

# ------------------------------------------------------------------ Licence Guide
with tab_guide:
    from bridge.guide_ui import render_guide
    render_guide(results=results, choice=choice, ss=ss, refinements=picked, question=question)

# ------------------------------------------------------------------ Biobank Guide
with tab_bank:
    from bridge.biobank_ui import render_biobank
    render_biobank()

# ------------------------------------------------------------------ Other regulations
with tab_world:
    st.subheader("Regulation beyond the UK")
    st.caption(f"Orientation notes, last reviewed {REGIONS_REVIEWED}. Not legal advice: confirm with your institution's "
               "animal welfare body and the competent authority. The Licence Guide itself covers the UK only.")
    for r in REGIONS.values():
        with st.expander(r["name"]):
            st.markdown(f"**Law.** {r['law']}")
            st.markdown(f"**What is protected.** {r['protected']}")
            st.markdown(f"**Authorisation.** {r['authorisation']}")
            st.markdown(f"**Alternatives.** {r['alternatives']}")
            st.markdown("**Read next.** " + "; ".join(r["read_next"]))
