"""Original cartoon illustrations for 3R Bridge, drawn as inline SVG.

One consistent style: rounded shapes, a 2.2 px spruce ink outline and flat fills
from the app palette. Everything is hand-built here, so there are no image files
or third-party artwork to licence.
"""

import base64

INK = "#18322E"
SPRUCE = "#1F6F63"
MINT = "#CFE6DD"
AMBER = "#E2A33A"
LILAC = "#8C7CE0"
LILAC_SOFT = "#DCD6FA"
PINK = "#F2B8AE"
PAPER = "#FFFFFF"
GREY = "#B9C3BE"

S = f'stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"'


def _svg(body: str, size: int = 56, vb: str = "0 0 64 64", label: str = "") -> str:
    """Return the drawing as an <img> with an SVG data URI (Streamlit strips inline <svg>)."""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{size}" height="{size}">{body}</svg>'
    data = base64.b64encode(svg.encode()).decode()
    alt = f' alt="{label}"' if label else ' alt="" aria-hidden="true"'
    return f'<img src="data:image/svg+xml;base64,{data}" width="{size}" height="{size}"{alt} style="display:block">'


def insilico(size=56):
    return _svg(f'''
      <rect x="8" y="12" width="48" height="32" rx="5" fill="{MINT}" {S}/>
      <path d="M26 52h12M32 44v8" {S} fill="none"/>
      <path d="M20 34l8-12 9 8 7-10" fill="none" stroke="{SPRUCE}" stroke-width="2.2" stroke-linecap="round"/>
      <circle cx="20" cy="34" r="3.2" fill="{AMBER}" {S}/><circle cx="28" cy="22" r="3.2" fill="{PAPER}" {S}/>
      <circle cx="37" cy="30" r="3.2" fill="{LILAC}" {S}/><circle cx="44" cy="20" r="3.2" fill="{PAPER}" {S}/>''',
                size, label="Computer model")


def cells2d(size=56):
    return _svg(f'''
      <ellipse cx="32" cy="38" rx="25" ry="12" fill="{PAPER}" {S}/>
      <ellipse cx="32" cy="34" rx="25" ry="12" fill="{MINT}" {S}/>
      <circle cx="22" cy="33" r="4" fill="{PINK}" {S}/><circle cx="33" cy="30" r="4" fill="{LILAC_SOFT}" {S}/>
      <circle cx="42" cy="35" r="4" fill="{PINK}" {S}/><circle cx="30" cy="39" r="3.4" fill="{LILAC_SOFT}" {S}/>
      <circle cx="22.5" cy="33" r="1" fill="{INK}"/><circle cx="33" cy="30" r="1" fill="{INK}"/>
      <circle cx="42" cy="35" r="1" fill="{INK}"/>''', size, label="Petri dish with cells")


def spheroid(size=56):
    return _svg(f'''
      <circle cx="32" cy="34" r="20" fill="{LILAC_SOFT}" {S}/>
      <circle cx="24" cy="27" r="7" fill="{PINK}" {S}/><circle cx="38" cy="26" r="7" fill="{LILAC}" {S}/>
      <circle cx="31" cy="38" r="7.5" fill="{PINK}" {S}/><circle cx="43" cy="39" r="6" fill="{LILAC_SOFT}" {S}/>
      <circle cx="21" cy="40" r="5.5" fill="{LILAC_SOFT}" {S}/>
      <path d="M50 12l2 4 4 1-4 2-2 4-2-4-4-2 4-1z" fill="{AMBER}" {S}/>''', size, label="3D spheroid")


def fly(size=56):
    return _svg(f'''
      <ellipse cx="22" cy="24" rx="12" ry="7" transform="rotate(-25 22 24)" fill="{PAPER}" fill-opacity=".85" {S}/>
      <ellipse cx="42" cy="24" rx="12" ry="7" transform="rotate(25 42 24)" fill="{PAPER}" fill-opacity=".85" {S}/>
      <ellipse cx="32" cy="40" rx="9" ry="13" fill="{AMBER}" {S}/>
      <path d="M24 40h16M25 46h14" {S} fill="none"/>
      <circle cx="32" cy="24" r="8" fill="{AMBER}" {S}/>
      <circle cx="27" cy="22" r="4" fill="#D2483B" {S}/><circle cx="37" cy="22" r="4" fill="#D2483B" {S}/>
      <path d="M29 16l-3-6M35 16l3-6" {S} fill="none"/>''', size, label="Fruit fly")


def tissue(size=56):
    return _svg(f'''
      <path d="M10 40c6-10 14-14 22-12s14-6 22-2l-2 14c-8-4-14 4-22 2s-14 2-20 8z" fill="{PINK}" {S}/>
      <path d="M12 34c6-10 14-14 22-12s14-6 22-2" fill="none" stroke="{LILAC}" stroke-width="2.2" stroke-linecap="round"/>
      <circle cx="24" cy="36" r="1.8" fill="{INK}"/><circle cx="33" cy="33" r="1.8" fill="{INK}"/>
      <circle cx="42" cy="35" r="1.8" fill="{INK}"/><circle cx="29" cy="40" r="1.8" fill="{INK}"/>''',
                size, label="Tissue slice")


def mouse(size=56):
    return _svg(f'''
      <path d="M50 44c6 0 8 4 6 8" fill="none" {S}/>
      <ellipse cx="34" cy="40" rx="17" ry="11" fill="#E6E9E7" {S}/>
      <circle cx="18" cy="32" r="9" fill="#E6E9E7" {S}/>
      <circle cx="16" cy="22" r="5.5" fill="{PINK}" {S}/><circle cx="25" cy="25" r="4.5" fill="{PINK}" {S}/>
      <circle cx="15" cy="31" r="1.6" fill="{INK}"/><circle cx="9.5" cy="34" r="1.8" fill="{PINK}" {S}/>
      <path d="M26 51v2M40 51v2" {S}/>''', size, label="Mouse")


def fish(size=56):
    stripes = "".join(f'<path d="M{x} 24q2 8 0 16" fill="none" stroke="{LILAC}" stroke-width="2.4" stroke-linecap="round"/>' for x in (22, 29, 36))
    return _svg(f'''
      <path d="M46 32l12-10v20z" fill="{AMBER}" {S}/>
      <path d="M8 32q12-15 30-12q8 2 10 12q-2 10-10 12q-18 3-30-12z" fill="#FBE3B4" {S}/>
      {stripes}
      <path d="M28 21q2-6 8-6" fill="none" {S}/>
      <circle cx="15" cy="30" r="2.2" fill="{INK}"/>''', size, label="Zebrafish")


TIER_ART = {0: insilico, 1: cells2d, 2: spheroid, 3: fly, 4: tissue, 5: mouse}


def mascot(size=150, mood="happy"):
    """Dot, a fruit fly in lab goggles who guides new researchers."""
    mouth = ('<path d="M52 66q8 7 16 0" fill="none" ' + S + '/>') if mood == "happy" else \
            ('<path d="M53 68h14" fill="none" ' + S + '/>')
    return _svg(f'''
      <ellipse cx="34" cy="58" rx="22" ry="12" transform="rotate(-30 34 58)" fill="{PAPER}" fill-opacity=".9" {S}/>
      <ellipse cx="86" cy="58" rx="22" ry="12" transform="rotate(30 86 58)" fill="{PAPER}" fill-opacity=".9" {S}/>
      <ellipse cx="60" cy="92" rx="18" ry="22" fill="{AMBER}" {S}/>
      <path d="M45 90h30M46 100h28" {S} fill="none"/>
      <rect x="66" y="80" width="22" height="28" rx="3" fill="{PAPER}" {S} transform="rotate(10 77 94)"/>
      <path d="M71 89h11M70 95h11M69 101h7" stroke="{SPRUCE}" stroke-width="2" stroke-linecap="round" transform="rotate(10 77 94)"/>
      <path d="M66 98q-6-2-8-8" fill="none" {S}/>
      <circle cx="60" cy="56" r="20" fill="{AMBER}" {S}/>
      <path d="M50 38l-6-14M70 38l6-14" {S} fill="none"/>
      <circle cx="43" cy="23" r="3" fill="{INK}"/><circle cx="77" cy="23" r="3" fill="{INK}"/>
      <path d="M38 50h44" stroke="{SPRUCE}" stroke-width="4" stroke-linecap="round"/>
      <circle cx="50" cy="52" r="9" fill="#D2483B" {S}/><circle cx="70" cy="52" r="9" fill="#D2483B" {S}/>
      <circle cx="50" cy="52" r="10.5" fill="{MINT}" fill-opacity=".35" stroke="{SPRUCE}" stroke-width="2.4"/>
      <circle cx="70" cy="52" r="10.5" fill="{MINT}" fill-opacity=".35" stroke="{SPRUCE}" stroke-width="2.4"/>
      <circle cx="47" cy="49" r="2.4" fill="{PAPER}"/><circle cx="67" cy="49" r="2.4" fill="{PAPER}"/>
      {mouth}''', size, vb="0 0 120 120", label="Dot the fruit fly, your guide")


def _badge(glyph: str, fill: str, size=44) -> str:
    return _svg(f'<circle cx="32" cy="32" r="27" fill="{fill}" {S}/>{glyph}', size, label="")


ROLE_BADGES = {
    "NTCO": _badge(f'<path d="M18 28l14-7 14 7-14 7z" fill="{PAPER}" {S}/><path d="M24 31v8q8 5 16 0v-8" fill="none" {S}/>', MINT),
    "NACWO": _badge(f'<path d="M20 34l12-11 12 11v10H20z" fill="{PAPER}" {S}/><path d="M29 44v-6h6v6" fill="none" {S}/>', "#FBE3B4"),
    "NVS": _badge(f'<path d="M28 20h8v8h8v8h-8v8h-8v-8h-8v-8h8z" fill="{PAPER}" {S}/>', PINK),
    "NIO": _badge(f'<path d="M18 22h12q2 0 2 2v20q-2-2-4-2H18zM46 22H34q-2 0-2 2v20q2-2 4-2h10z" fill="{PAPER}" {S}/>', LILAC_SOFT),
    "HOLC": _badge(f'<rect x="18" y="22" width="28" height="20" rx="2" fill="{PAPER}" {S}/><path d="M18 24l14 10 14-10" fill="none" {S}/>', MINT),
    "AWERB": _badge(f'<path d="M32 18v26M22 44h20M20 26h24" {S} fill="none"/><path d="M20 26l-5 9h10zM44 26l-5 9h10z" fill="{PAPER}" {S}/>', "#FBE3B4"),
    "PPL holder": _badge(f'<path d="M28 18h8M29 18v10l-9 14q-1 3 2 3h20q3 0 2-3l-9-14V18" fill="{PAPER}" {S}/><path d="M23 38h18" stroke="{LILAC}" stroke-width="2.2"/>', LILAC_SOFT),
}
