"""Model catalogue for the 3R Path Model Finder.

Each model sits on a "replacement ladder": tier 0 is the least sentient /
least animal-dependent option, tier 5 is a protected vertebrate. Scores are
expert judgements (0 = unsuitable, 1 = partial, 2 = good, 3 = strong) for how
well a model can answer questions in each research area. They are a starting
point for discussion with researchers, not a regulatory decision.
"""

import json
from pathlib import Path

AREAS = {
    "hepatotox": "Liver toxicity and drug metabolism",
    "gut": "Intestinal absorption and barrier function",
    "neural": "Neural circuits and behaviour",
    "sensory": "Sensory physiology (for example temperature sensing)",
    "devgen": "Development and genetics",
    "immune": "Immune and inflammatory responses",
    "pk": "Whole-body pharmacokinetics and systemic effects",
    "regen": "Tissue engineering, biomaterials and regeneration",
    "cryo": "Cryopreservation and biobanking methods",
}

# Requirements a question may carry, and how they affect suitability.
REQUIREMENTS = {
    "human": "Human-relevant biology is essential",
    "organism": "Needs an intact organism or interaction between organs",
    "behaviour": "Needs a behavioural readout",
    "vertebrate": "Needs vertebrate or mammalian physiology (for example adaptive immunity, mammalian PK)",
    "throughput": "Needs high throughput (many conditions or compounds)",
    "longterm": "Needs a long study (weeks or more)",
    "regulatory": "Results must meet a regulatory test guideline",
}

TIER_NAMES = {
    0: "In silico",
    1: "Human cells (2D)",
    2: "Human 3D and microphysiological",
    3: "Non-protected organisms",
    4: "Ex vivo tissue",
    5: "Protected vertebrates (ASPA)",
}

_DATA = json.loads((Path(__file__).parent / "data" / "models.json").read_text(encoding="utf-8"))
MODELS = _DATA["models"]
DATA_VERSION = _DATA["version"]
DATA_LAST_REVIEWED = _DATA["last_reviewed"]

REFINEMENTS = [
    "Non-aversive handling (tunnel or cupped hands instead of tail picking)",
    "Anaesthesia and pre-emptive analgesia plan agreed with the NVS",
    "Humane endpoints defined in advance, with a welfare score sheet",
    "More frequent monitoring at high-risk time points",
    "Pain assessment with validated tools such as grimace scales",
    "Least invasive sampling (for example microsampling of blood)",
    "In vivo imaging so each animal gives repeated measures over time",
    "Enrichment and social housing where compatible",
    "Staff signed off as competent before working unsupervised",
    "Pilot study to check endpoints and variability first",
]

REFERENCES = [
    "NC3Rs Experimental Design Assistant: https://eda.nc3rs.org.uk",
    "ARRIVE guidelines 2.0 (Percie du Sert et al., PLoS Biology 2020): https://arriveguidelines.org",
    "PREPARE guidelines (Smith et al., Laboratory Animals 2018): https://norecopa.no/prepare",
    "Animals (Scientific Procedures) Act 1986, Home Office guidance on its operation",
]


# One-click examples for the Model Finder: (button label, question, area, requirements, why).
EXAMPLES = [
    ("Liver injury", "Does compound X cause liver injury after repeated dosing?", "hepatotox", [],
     "Human liver spheroids keep liver function for weeks, so repeated dosing can be tested without animals."),
    ("Gut absorption", "How well is drug Y absorbed across the gut wall?", "gut", [],
     "A human intestinal barrier in a Transwell measures absorption directly, and is accepted for this question."),
    ("Dose in the brain", "What dose of drug Z reaches the brain in people?", "pk", ["human"],
     "A PBPK computer model predicts human doses from existing data, so no new animals are needed."),
    ("Cold avoidance", "Which brain circuits drive cold avoidance behaviour?", "sensory", ["organism", "behaviour"],
     "Behaviour needs a whole animal, but the fruit fly has the circuits and is not a protected animal."),
    ("Tissue regrowth", "Which signals trigger tissue regrowth after injury?", "regen", ["organism"],
     "Zebrafish larvae regrow tissue and can be studied before they are protected animals."),
    ("Cryoprotectant", "Does a new cryoprotectant protect cells through freezing and thawing?", "cryo", [],
     "Cells in culture answer this directly; move up to 3D models when you need tissue-like structure."),
    ("Vaccine response", "Does adjuvant W boost antibody responses after vaccination?", "immune", ["organism", "vertebrate"],
     "Antibody responses need a whole mammalian immune system, so this is where animals are justified."),
]
