"""Build the single-file web app: python scripts/build_html.py  ->  3r-path.html (and docs/index.html).

All content comes from the same Python modules the Streamlit app uses; regulatory verdicts are pre-computed for every
input combination, so the HTML contains no duplicated legal logic.
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bridge import biobank, licence  # noqa: E402
from bridge.catalogue import (  # noqa: E402
    AREAS,
    DATA_LAST_REVIEWED,
    DATA_VERSION,
    EXAMPLES,
    MODELS,
    REFERENCES,
    REFINEMENTS,
    REQUIREMENTS,
    TIER_NAMES,
)
from bridge.regions import LAST_REVIEWED, REGIONS  # noqa: E402


def licence_table() -> dict:
    out = {}
    for subject in licence.SUBJECTS:
        for stage, above, ga, s1 in itertools.product([0, 1], repeat=4):
            out[f"{subject}|{stage}|{above}|{ga}|{s1}"] = list(
                licence.licence_verdict(subject, bool(stage), bool(above), bool(ga), bool(s1)))
    return out


def biobank_table() -> dict:
    out = {}
    for material, source in itertools.product(biobank.MATERIALS, biobank.SOURCES):
        for ident, dec, pat, gm in itertools.product([0, 1], repeat=4):
            out[f"{material}|{source}|{ident}|{dec}|{pat}|{gm}"] = list(
                biobank.biobank_verdict(material, source, bool(ident), bool(dec), bool(pat), bool(gm)))
    return out


def data() -> dict:
    return {
        "version": DATA_VERSION, "lastReviewed": DATA_LAST_REVIEWED, "regionsReviewed": LAST_REVIEWED,
        "areas": AREAS, "requirements": REQUIREMENTS, "tiers": {str(k): v for k, v in TIER_NAMES.items()},
        "models": MODELS, "refinements": REFINEMENTS, "references": REFERENCES, "regions": REGIONS,
        "examples": [dict(label=a, question=b, area=c, needs=d, why=e) for a, b, c, d, e in EXAMPLES],
        "licence": {
            "subjects": licence.SUBJECTS, "verdict": licence_table(),
            "techniques": {k: list(v) for k, v in licence.TECHNIQUES.items()}, "categoryText": licence.CATEGORY_TEXT,
            "modules": licence.MODULES, "named": [list(x) for x in licence.NAMED_PERSONS],
            "worries": [list(x) for x in licence.WORRIES], "checklist": licence.CHECKLIST_PIL,
            "journey": [list(x) for x in licence.JOURNEY], "regulated": licence.EXAMPLES_REGULATED,
            "notRegulated": licence.EXAMPLES_NOT_REGULATED,
        },
        "biobank": {
            "materials": biobank.MATERIALS, "sources": biobank.SOURCES, "verdict": biobank_table(),
            "ask": [list(x) for x in biobank.ASK_BIOBANK], "who": [list(x) for x in biobank.WHO_HELPS],
            "find": [list(x) for x in biobank.FIND], "references": [list(x) for x in biobank.REFERENCES],
        },
    }


def build() -> str:
    payload = json.dumps(data(), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (ROOT / "web" / "template.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)


if __name__ == "__main__":
    html = build()
    for target in (ROOT / "3r-path.html", ROOT / "docs" / "index.html"):
        target.write_text(html, encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)} ({len(html) // 1024} KB)")
