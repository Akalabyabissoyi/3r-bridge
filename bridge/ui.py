"""Visual layer for 3R Bridge: page styling and illustrated HTML components."""
from __future__ import annotations

import html

import streamlit as st

from . import art
from .catalogue import TIER_NAMES

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap');

:root{
  --paper:#F5F7F6; --card:#FFFFFF; --ink:#18322E; --ink-2:#4B605B; --ink-3:#566763;
  --spruce:#1F6F63; --mint:#CFE6DD; --amber:#E2A33A; --amber-soft:#FBE9C6;
  --lilac:#8C7CE0; --lilac-soft:#ECE8FD; --line:#DCE3E0; --unsuit:#C9D1CE;
}
html, body, [class*="css"], .stMarkdown, .stText, p, li, label, input, textarea{
  font-family:'Atkinson Hyperlegible', system-ui, sans-serif !important;
}
h1, h2, h3, h4, .rb-display{ font-family:'Bricolage Grotesque', system-ui, sans-serif !important; color:var(--ink); letter-spacing:-.01em; }
.stApp{ background:var(--paper); }
.block-container{ padding-top:1.4rem; max-width:1180px; }
h2{ font-size:1.55rem !important; } h3{ font-size:1.22rem !important; }

/* tabs */
.stTabs [data-baseweb="tab-list"]{ gap:.4rem; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"]{ font-family:'Bricolage Grotesque', sans-serif; font-size:1.05rem; padding:.55rem 1rem; border-radius:10px 10px 0 0; }
.stTabs [aria-selected="true"]{ background:var(--card); color:var(--spruce) !important; }
.stTabs [data-baseweb="tab-highlight"]{ background:var(--spruce); }

/* hero */
.rb-brand{ display:flex; align-items:center; gap:.45rem; font-family:'Bricolage Grotesque', sans-serif; font-weight:700; font-size:1.15rem; color:var(--ink); margin:0 0 .7rem; }
.rb-hero{ display:grid; grid-template-columns:minmax(0,1.25fr) minmax(0,1fr); gap:1.5rem; align-items:center;
  background:var(--card); border:1px solid var(--line); border-radius:22px; padding:1.6rem 1.9rem; margin-bottom:1.1rem; }
.rb-hero h1{ font-size:clamp(1.7rem, 2.8vw, 2.35rem); line-height:1.05; margin:0 0 .6rem; font-weight:700; }
.rb-hero p{ color:var(--ink-2); font-size:1.08rem; max-width:52ch; margin:0; line-height:1.55; }
.rb-climb{ display:flex; align-items:flex-end; justify-content:center; gap:.1rem; }
.rb-climb .step{ display:flex; flex-direction:column; align-items:center; }
.rb-climb .step span{ display:block; width:58px; height:6px; background:var(--ink); border-radius:3px; margin-top:2px; }
@media (max-width:760px){ .rb-hero{ grid-template-columns:1fr; } .rb-climb{ display:none; } }

/* ladder */
.rb-ladder{ position:relative; padding:.3rem 0 .3rem; }
.rb-ladder:before, .rb-ladder:after{ content:""; position:absolute; top:0; bottom:0; width:6px; background:var(--ink); border-radius:3px; }
.rb-ladder:before{ left:0; } .rb-ladder:after{ right:0; }
.rb-rung{ position:relative; display:grid; grid-template-columns:64px minmax(0,1fr); gap:.9rem; align-items:center;
  margin:0 6px; padding:.7rem .9rem .8rem; border-bottom:6px solid var(--ink); background:var(--card); }
.rb-rung:first-child{ border-top:6px solid var(--ink); }
.rb-rung.protected{ background:#FBF6EF; }
.rb-rung.here{ background:var(--mint); }
.rb-rung h4{ margin:0 0 .35rem; font-size:1rem; font-weight:700; }
.rb-chips{ display:flex; flex-wrap:wrap; gap:.35rem; }
.rb-chip{ font-size:.86rem; padding:.22rem .6rem; border-radius:999px; border:1.5px solid var(--ink); background:var(--card); color:var(--ink); }
.rb-chip.adequate{ background:var(--spruce); color:#fff; border-color:var(--spruce); }
.rb-chip.partial{ background:var(--amber-soft); border-color:var(--amber); }
.rb-chip.unsuitable{ border-color:var(--unsuit); color:var(--ink-3); background:transparent; }
.rb-chip.pick{ box-shadow:0 0 0 3px var(--amber); }
.rb-flag{ position:absolute; right:12px; top:-30px; display:flex; align-items:flex-end; gap:.3rem; animation:rb-hop .7s ease-out 1; }
.rb-flag b{ background:var(--amber); color:var(--ink); padding:.25rem .65rem; border-radius:10px 10px 10px 2px; font-size:.86rem;
  font-family:'Bricolage Grotesque', sans-serif; border:2px solid var(--ink); }
@keyframes rb-hop{ 0%{ transform:translateY(14px); opacity:0 } 60%{ transform:translateY(-4px); opacity:1 } 100%{ transform:none } }
@media (prefers-reduced-motion: reduce){ .rb-flag{ animation:none; } }
.rb-legend{ display:flex; gap:1rem; flex-wrap:wrap; font-size:.86rem; color:var(--ink-2); margin:.6rem 0 0; }
.rb-legend i{ display:inline-block; width:12px; height:12px; border-radius:50%; margin-right:.35rem; vertical-align:-1px; border:1.5px solid var(--ink); }

/* pick card */
.rb-pick{ background:var(--card); border:2px solid var(--spruce); border-radius:16px; padding:1rem 1.1rem; display:flex; gap:.9rem; align-items:center; margin-bottom:1rem; }
.rb-pick .t{ font-family:'Bricolage Grotesque', sans-serif; font-size:1.2rem; font-weight:700; color:var(--ink); }
.rb-pick .s{ color:var(--ink-2); font-size:.93rem; margin-top:.15rem; }

/* guide */
.rb-say{ display:flex; gap:1rem; align-items:flex-end; margin:.2rem 0 1rem; }
.rb-bubble{ position:relative; background:var(--card); border:2px solid var(--ink); border-radius:18px; padding:.85rem 1.1rem; max-width:62ch;
  font-size:1.04rem; line-height:1.5; color:var(--ink); }
.rb-bubble:before{ content:""; position:absolute; left:-12px; bottom:22px; border:10px solid transparent; border-right-color:var(--ink); border-left:0; }
.rb-verdict{ display:flex; gap:1rem; align-items:flex-start; border-radius:16px; padding:1rem 1.15rem; margin:.6rem 0; border:2px solid var(--ink); }
.rb-verdict.none{ background:var(--mint); } .rb-verdict.schedule1{ background:var(--lilac-soft); } .rb-verdict.licence{ background:var(--amber-soft); }
.rb-verdict h3{ margin:.1rem 0 .4rem; }
.rb-verdict ul{ margin:0; padding-left:1.1rem; } .rb-verdict li{ margin:.2rem 0; }
.rb-people{ display:grid; grid-template-columns:repeat(auto-fill, minmax(250px, 1fr)); gap:.8rem; }
.rb-person{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:.9rem; display:flex; gap:.75rem; }
.rb-person b{ font-family:'Bricolage Grotesque', sans-serif; font-size:1.02rem; }
.rb-person small{ display:block; color:var(--ink-3); margin-bottom:.25rem; }
.rb-person p{ margin:0; font-size:.93rem; color:var(--ink-2); line-height:1.45; }
.rb-path{ display:flex; flex-wrap:wrap; align-items:center; gap:.4rem; margin-top:1rem; }
.rb-path span{ background:var(--card); border:1.5px solid var(--ink); border-radius:999px; padding:.25rem .7rem; font-size:.9rem; }
.rb-path em{ color:var(--ink-3); font-style:normal; }
.rb-lic{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:1rem 1.1rem; height:100%; }
.rb-cat{ display:inline-flex; width:2.1rem; height:2.1rem; border-radius:50%; align-items:center; justify-content:center;
  font-family:'Bricolage Grotesque', sans-serif; font-weight:700; border:2px solid var(--ink); background:var(--amber-soft); margin-right:.35rem; }
.rb-foot{ color:var(--ink-3); font-size:.85rem; margin-top:1.4rem; }

/* streamlit widgets */
.stButton button, .stDownloadButton button{ border-radius:999px; border:2px solid var(--ink); font-weight:700; }
.stButton button[kind="primary"]{ background:var(--spruce); border-color:var(--spruce); color:#fff; }
.stDownloadButton button{ background:var(--spruce); color:#fff; border-color:var(--spruce); }
div[data-testid="stExpander"]{ background:var(--card); border-radius:14px; }
[data-testid="stMetricValue"]{ font-family:'Bricolage Grotesque', sans-serif; color:var(--spruce); }
/* start-here cards */
.rb-start{ display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:.8rem; margin:-.3rem 0 1.1rem; }
.rb-start div{ display:flex; gap:.8rem; align-items:center; background:var(--card); border:1px solid var(--line); border-radius:16px; padding:.75rem 1rem; }
.rb-start b{ font-family:'Bricolage Grotesque', sans-serif; font-size:1.05rem; display:block; }
.rb-start small{ color:var(--ink-2); font-size:.93rem; }
@media (max-width:760px){ .rb-start{ grid-template-columns:1fr; } }

/* journey */
.rb-journey{ display:flex; gap:0; margin:.3rem 0 1rem; overflow-x:auto; padding-bottom:.2rem; }
.rb-stage{ flex:1 0 96px; position:relative; text-align:center; padding-top:1.9rem; }
.rb-stage:before{ content:""; position:absolute; top:.72rem; left:0; right:0; height:4px; background:var(--line); }
.rb-stage:first-child:before{ left:50%; } .rb-stage:last-child:before{ right:50%; }
.rb-stage.done:before{ background:var(--spruce); }
.rb-stage i{ position:absolute; top:.15rem; left:50%; transform:translateX(-50%); width:1.2rem; height:1.2rem; border-radius:50%;
  background:var(--card); border:2.5px solid var(--ink-3); }
.rb-stage.done i{ background:var(--spruce); border-color:var(--spruce); }
.rb-stage.now i{ background:var(--amber); border-color:var(--ink); width:1.5rem; height:1.5rem; top:0; }
.rb-stage b{ display:block; font-family:'Bricolage Grotesque', sans-serif; font-size:.95rem; color:var(--ink); }
.rb-stage small{ display:block; color:var(--ink-3); font-size:.8rem; line-height:1.3; padding:0 .3rem; }
.rb-stage.now small{ color:var(--ink-2); }

/* examples */
.rb-ex{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:.8rem; margin:.4rem 0 .8rem; }
.rb-ex > div{ border-radius:16px; padding:.85rem 1rem; border:1.5px solid var(--ink); }
.rb-ex .yes{ background:var(--amber-soft); } .rb-ex .no{ background:var(--mint); }
.rb-ex h4{ display:flex; align-items:center; gap:.5rem; margin:0 0 .4rem; font-size:1rem; }
.rb-ex ul{ margin:0; padding-left:1.1rem; } .rb-ex li{ margin:.18rem 0; font-size:.95rem; }
@media (max-width:760px){ .rb-ex{ grid-template-columns:1fr; } }
.rb-term{ margin:.1rem 0 .55rem; } .rb-term b{ color:var(--spruce); }
/* worked examples */
.rb-exhead{ display:flex; gap:1rem; align-items:flex-start; background:var(--card); border:1.5px solid var(--ink); border-radius:18px; padding:1rem 1.15rem; margin:.4rem 0 .8rem; }
.rb-exhead h3{ margin:0 0 .25rem; } .rb-exhead .ref{ color:var(--ink-3); font-size:.88rem; }
.rb-exhead .why{ margin:.45rem 0 .6rem; color:var(--ink-2); }
.rb-facts{ display:flex; flex-wrap:wrap; gap:.35rem; margin-bottom:.7rem; }
.rb-facts span{ font-size:.86rem; padding:.2rem .6rem; border-radius:999px; background:var(--paper); border:1px solid var(--line); }
.rb-facts b{ color:var(--ink-2); font-weight:700; }
.rb-sev{ display:flex; height:14px; border-radius:7px; overflow:hidden; border:1.5px solid var(--ink); max-width:420px; }
.rb-sev i{ display:block; } .rb-sev .mild{ background:var(--mint); } .rb-sev .moderate{ background:var(--amber); }
.rb-sevlab{ font-size:.86rem; color:var(--ink-2); margin-top:.3rem; }
.rb-lesson{ border-left:4px solid var(--amber); background:var(--amber-soft); border-radius:0 10px 10px 0; padding:.5rem .8rem; margin:.4rem 0 .2rem; font-size:.95rem; }
.rb-lesson b{ font-family:'Bricolage Grotesque', sans-serif; }
/* biobank */
.rb-asks{ display:grid; grid-template-columns:repeat(2, minmax(0,1fr)); gap:.6rem; }
.rb-ask{ background:var(--card); border:1px solid var(--line); border-left:4px solid var(--lilac); border-radius:0 12px 12px 0; padding:.6rem .85rem; }
.rb-ask b{ display:block; font-family:'Bricolage Grotesque', sans-serif; color:var(--ink); }
.rb-ask span{ font-size:.94rem; color:var(--ink-2); line-height:1.45; }
.rb-finds{ display:grid; grid-template-columns:repeat(auto-fill, minmax(230px,1fr)); gap:.6rem; }
.rb-find{ display:block; text-decoration:none; background:var(--card); border:1.5px solid var(--ink); border-radius:14px; padding:.7rem .9rem; color:var(--ink) !important; }
.rb-find:hover, .rb-find:focus-visible{ background:var(--mint); }
.rb-find b{ display:block; font-family:'Bricolage Grotesque', sans-serif; }
.rb-find span{ font-size:.92rem; color:var(--ink-2); }
@media (max-width:760px){ .rb-asks{ grid-template-columns:1fr; } }

/* accessibility: visible keyboard focus and no motion for people who ask for none */
a:focus-visible, button:focus-visible, [role="tab"]:focus-visible, input:focus-visible, textarea:focus-visible,
select:focus-visible, [tabindex]:focus-visible{ outline:3px solid var(--spruce) !important; outline-offset:2px; }
@media (prefers-reduced-motion: reduce){ *, *:before, *:after{ animation:none !important; transition:none !important; scroll-behavior:auto !important; } }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def hero():
    icons = "".join(
        f'<div class="step" style="margin-bottom:{i*14}px">{"" if i != 3 else art.mascot(64)}{f(46)}<span></span></div>'
        for i, f in enumerate([art.mouse, art.tissue, art.fly, art.spheroid, art.cells2d, art.insilico])
    )
    st.html(f"""
    <div class="rb-brand">{art.fly(30)}<span>3R Bridge</span></div>
    <div class="rb-hero">
      <div>
        <h1 class="rb-display">Start with the least sentient model that can answer your question.</h1>
        <p>3R Bridge helps you weigh computer models, human 3D tissue models and non-protected organisms
        before animals, plan Reduction and Refinement, and, if animals are needed, find your way through a UK licence
        application with confidence.</p>
      </div>
      <div class="rb-climb" aria-hidden="true">{icons}</div>
    </div>
    <div class="rb-start">
      <div>{art.spheroid(44)}<span><b>Planning a study?</b><small>Use the Model Finder to choose the least sentient model and justify it.</small></span></div>
      <div>{art.mascot(48)}<span><b>New to animal work?</b><small>Open the Licence Guide tab. Dot walks you through your licence step by step.</small></span></div>
      <div>{art.tissue(44)}<span><b>Using human samples?</b><small>The Biobank Guide shows the approvals for tissue, cells and biobank samples.</small></span></div>
    </div>""")


def ladder(results: list[dict], choice: dict | None):
    rungs = []
    for tier in sorted(TIER_NAMES):
        group = [r for r in results if r["tier"] == tier]
        if not group:
            continue
        here = choice is not None and choice["tier"] == tier
        chips = "".join(
            f'<span class="rb-chip {r["verdict"]}{" pick" if choice and r["key"] == choice["key"] else ""}" '
            f'title="{html.escape(r["verdict"])}">{html.escape(r["name"])}</span>' for r in group)
        flag = (f'<div class="rb-flag">{art.mascot(56)}<b>Start here</b></div>' if here else "")
        cls = "rb-rung" + (" protected" if tier == 5 else "") + (" here" if here else "")
        rungs.append(f'<div class="{cls}">{flag}<div>{art.TIER_ART[tier](56)}</div>'
                     f'<div><h4>{html.escape(TIER_NAMES[tier])}</h4><div class="rb-chips">{chips}</div></div></div>')
    st.html(f"""
    <div class="rb-ladder">{''.join(rungs)}</div>
    <div class="rb-legend"><span><i style="background:#1F6F63;border-color:#1F6F63"></i>Adequate</span>
      <span><i style="background:#FBE9C6;border-color:#E2A33A"></i>Partly suitable</span>
      <span><i style="background:transparent;border-color:#C9D1CE"></i>Unsuitable</span>
      <span>Top rung: no animals. Bottom rung: animals protected under ASPA.</span></div>""")


def _model_art(model: dict, size: int):
    if "zebrafish" in model["name"].lower():
        return art.fish(size)
    return art.TIER_ART[model["tier"]](size)


def pick_card(choice: dict | None):
    if choice:
        st.html(f"""<div class="rb-pick">{_model_art(choice, 52)}
          <div><div class="t">Start here: {html.escape(choice['name'])}</div>
          <div class="s">{html.escape(TIER_NAMES[choice['tier']])}. {html.escape(choice['status'])}</div></div></div>""")
    else:
        st.html(f"""<div class="rb-pick" style="border-color:#E2A33A">{art.mascot(56, 'neutral')}
          <div><div class="t">No single model meets every requirement</div>
          <div class="s">Split the question, so the early steps use non-animal methods and animals answer only what is left.</div></div></div>""")


def say(text: str, mood: str = "happy"):
    st.html(f'<div class="rb-say">{art.mascot(92, mood)}<div class="rb-bubble">{text}</div></div>')


VERDICT_ART = {"none": art.cells2d, "schedule1": art.tissue, "licence": art.mouse}


def verdict(headline: str, level: str, notes: list[str]):
    items = "".join(f"<li>{html.escape(n)}</li>" for n in notes)
    st.html(f"""<div class="rb-verdict {level}">{VERDICT_ART[level](60)}
      <div><h3>{html.escape(headline)}</h3><ul>{items}</ul></div></div>""")


def people(named_persons):
    cards = "".join(
        f'<div class="rb-person">{art.ROLE_BADGES[short]}<div><b>{html.escape(short)}</b>'
        f'<small>{html.escape(long)}</small><p>{html.escape(when)}</p></div></div>'
        for short, long, when in named_persons)
    path = ["NTCO: training", "PPL holder: your protocol", "NACWO and NVS: practical plans",
            "AWERB: review", "HOLC: submit on ASPeL"]
    st.html(f'<div class="rb-people">{cards}</div><div class="rb-path"><em>A typical order:</em>' +
            '<em>then</em>'.join(f"<span>{p}</span>" for p in path) + '</div>')


def licence_card(cats: list[str], category_text: dict):
    rows = "".join(f'<p style="margin:.55rem 0"><span class="rb-cat">{c}</span>{html.escape(category_text[c])}</p>' for c in cats)
    st.html(f'<div class="rb-lic"><h3>Your personal licence categories</h3>{rows}</div>')


def modules_card(mods: list[str], modules: dict):
    rows = "".join(f'<li><b>Module {m}</b>: {html.escape(modules[m])}</li>' for m in mods)
    st.html(f'<div class="rb-lic"><h3>Accredited training modules</h3><ul style="padding-left:1.1rem;margin:0">{rows}</ul></div>')


def journey(stages, now: int):
    """The licence journey as a track; stages before `now` are done, `now` is highlighted."""
    cells = []
    for i, (n, d) in enumerate(stages):
        cls = "rb-stage" + (" done" if i < now else "") + (" now" if i == now else "")
        cur = ' aria-current="step"' if i == now else ""
        cells.append(f'<div class="{cls}" role="listitem"{cur}><i></i><b>{html.escape(n)}</b><small>{html.escape(d)}</small></div>')
    cells = "".join(cells)
    st.html(f'<div class="rb-journey" role="list" aria-label="Your licence journey">{cells}</div>')


def examples(regulated, not_regulated):
    yes = "".join(f"<li>{html.escape(x)}</li>" for x in regulated)
    no = "".join(f"<li>{html.escape(x)}</li>" for x in not_regulated)
    st.html(f"""<div class="rb-ex">
      <div class="yes"><h4>{art.mouse(30)}Usually needs a licence</h4><ul>{yes}</ul></div>
      <div class="no"><h4>{art.fly(30)}Usually does not</h4><ul>{no}</ul></div></div>""")


def example_card(ex: dict):
    facts = "".join(f"<span><b>{html.escape(k)}:</b> {html.escape(v)}</span>" for k, v in ex["facts"].items())
    sev = ex["severity"]
    bar = "".join(f'<i class="{k.lower()}" style="width:{v}%"></i>' for k, v in sev.items() if v)
    label = ex.get("severity_text") or ", ".join(f"{k} {v}%" for k, v in sev.items() if v)
    icon = getattr(art, ex["art"])(64)
    st.html(f"""<div class="rb-exhead">{icon}<div style="flex:1">
      <h3>{html.escape(ex["title"])}</h3><div class="ref">Granted July to September 2025, {html.escape(ex["ref"])}</div>
      <p class="why">{html.escape(ex["why_read"])}</p><div class="rb-facts">{facts}</div>
      <div class="rb-sev" role="img" aria-label="Expected severity: {html.escape(label)}">{bar}</div>
      <div class="rb-sevlab">Expected severity: {html.escape(label)}</div></div></div>""")


def lesson(text: str):
    st.html(f'<div class="rb-lesson"><b>What to learn:</b> {html.escape(text)}</div>')
