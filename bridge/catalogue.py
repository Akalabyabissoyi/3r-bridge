"""Model catalogue for the 3R Bridge Model Finder.

Each model sits on a "replacement ladder": tier 0 is the least sentient /
least animal-dependent option, tier 5 is a protected vertebrate. Scores are
expert judgements (0 = unsuitable, 1 = partial, 2 = good, 3 = strong) for how
well a model can answer questions in each research area. They are a starting
point for discussion with researchers, not a regulatory decision.
"""

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

MODELS = [
    dict(
        key="insilico", name="In silico: QSAR, PBPK and connectome models", tier=0,
        status="Not regulated under ASPA. No animals.",
        scores=dict(hepatotox=1, gut=1, neural=1, sensory=1, devgen=0, immune=0, pk=2, regen=0, cryo=1),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=0, throughput=1, longterm=1, regulatory=0),
        strengths="Fast, cheap, unlimited conditions. PBPK can predict human exposure; whole-brain connectome models (for example the FlyWire Drosophila brain) can generate circuit hypotheses before any experiment.",
        limits="Only as good as the data behind it. Usually needs experimental validation.",
        bankable="Not applicable.",
    ),
    dict(
        key="cells2d", name="Human cell lines and primary cells (2D)", tier=1,
        status="Not regulated under ASPA. Human material may need consent and HTA-compliant handling.",
        scores=dict(hepatotox=1, gut=1, neural=1, sensory=0, devgen=1, immune=2, pk=0, regen=1, cryo=2),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=1, throughput=1, longterm=0, regulatory=1),
        strengths="Human, reproducible, high throughput. Primary immune cells such as PBMCs give donor-relevant responses.",
        limits="Lose tissue architecture and much of their differentiated function in 2D.",
        bankable="Yes. Routine cryopreservation; assay-ready frozen monolayers remove repeat culture (Tomas et al., Biomacromolecules 2022).",
    ),
    dict(
        key="spheroid", name="3D liver spheroids", tier=2,
        status="Not regulated under ASPA.",
        scores=dict(hepatotox=3, gut=0, neural=0, sensory=0, devgen=0, immune=1, pk=1, regen=1, cryo=3),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=1, throughput=1, longterm=1, regulatory=0),
        strengths="Keep liver function and drug metabolism for weeks, and suit repeat-dose toxicity better than 2D culture.",
        limits="Single organ, no blood flow or systemic exposure.",
        bankable="Yes. Spheroids can be cryopreserved with macromolecular cryoprotectants and used straight from the freezer (Bissoyi et al., ACS Appl. Mater. Interfaces 2023).",
    ),
    dict(
        key="barrier", name="Intestinal Transwell barrier models (Caco-2 / HT29-MTX)", tier=2,
        status="Not regulated under ASPA.",
        scores=dict(hepatotox=0, gut=3, neural=0, sensory=0, devgen=0, immune=1, pk=1, regen=0, cryo=3),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=1, throughput=1, longterm=0, regulatory=1),
        strengths="Measure permeability, TEER and tight junctions; widely used to predict intestinal absorption.",
        limits="Normally take about three weeks to differentiate; lack the full cell diversity of the gut.",
        bankable="Yes. Differentiated barriers frozen on the Transwell recover function in about 7 days instead of 21 (Bissoyi et al., ACS Appl. Mater. Interfaces 2024).",
    ),
    dict(
        key="organoid", name="Organoids (iPSC or adult stem cell derived)", tier=2,
        status="Not regulated under ASPA. Matrigel and some reagents are animal-derived; consider animal-free matrices.",
        scores=dict(hepatotox=2, gut=2, neural=2, sensory=1, devgen=2, immune=1, pk=0, regen=2, cryo=2),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=1, throughput=1, longterm=1, regulatory=0),
        strengths="Self-organising human tissue with several cell types; patient-specific disease models.",
        limits="Variable between batches; immature compared with adult tissue; no vasculature.",
        bankable="Partly. Organoids can be cryopreserved, but recovery varies by type.",
    ),
    dict(
        key="chip", name="Organ-on-chip and microphysiological systems", tier=2,
        status="Not regulated under ASPA.",
        scores=dict(hepatotox=3, gut=3, neural=1, sensory=0, devgen=0, immune=2, pk=2, regen=1, cryo=1),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=1, throughput=0, longterm=1, regulatory=0),
        strengths="Add flow, mechanical forces and links between organ compartments; some multi-organ chips model systemic exposure.",
        limits="Lower throughput, specialist equipment, still being validated for regulatory use.",
        bankable="Limited. Banking pre-built chips is an open problem.",
    ),
    dict(
        key="drosophila", name="Drosophila melanogaster (fruit fly)", tier=3,
        status="Invertebrate, not protected under ASPA.",
        scores=dict(hepatotox=1, gut=2, neural=3, sensory=3, devgen=3, immune=2, pk=1, regen=1, cryo=2),
        provides=dict(human=0, organism=1, behaviour=1, vertebrate=0, throughput=1, longterm=1, regulatory=0),
        strengths="Whole organism with behaviour and powerful genetics; about 75 percent of human disease genes have a fly counterpart. A complete adult brain connectome (FlyWire, 2024) makes circuit questions tractable.",
        limits="Not a vertebrate: limited for mammalian physiology, adaptive immunity and PK.",
        bankable="Emerging. Embryo vitrification lets fly lines be stored frozen instead of maintained as live stocks.",
    ),
    dict(
        key="celegans", name="C. elegans (nematode)", tier=3,
        status="Invertebrate, not protected under ASPA.",
        scores=dict(hepatotox=1, gut=1, neural=2, sensory=2, devgen=3, immune=1, pk=0, regen=0, cryo=2),
        provides=dict(human=0, organism=1, behaviour=1, vertebrate=0, throughput=1, longterm=0, regulatory=0),
        strengths="Tiny, fast, fully mapped nervous system and cell lineage; very high throughput.",
        limits="Far from mammalian physiology.",
        bankable="Yes. Routinely stored frozen.",
    ),
    dict(
        key="zebrafish", name="Zebrafish larvae before independent feeding", tier=3,
        status="Not protected under ASPA until capable of independent feeding (about 5 days post-fertilisation at 28.5 C). Older fish are protected.",
        scores=dict(hepatotox=2, gut=1, neural=2, sensory=2, devgen=3, immune=1, pk=1, regen=2, cryo=1),
        provides=dict(human=0, organism=1, behaviour=1, vertebrate=1, throughput=1, longterm=0, regulatory=1),
        strengths="Vertebrate organism, transparent, high throughput; established for developmental toxicity screening.",
        limits="Short non-protected window; work beyond it needs licences.",
        bankable="Partly. Sperm cryopreservation is routine; embryos are not.",
    ),
    dict(
        key="exvivo", name="Ex vivo tissue (precision-cut slices, explants)", tier=4,
        status="Uses tissue from animals or humans. Tissue shared from animals already killed for other studies avoids extra animals.",
        scores=dict(hepatotox=3, gut=2, neural=2, sensory=1, devgen=0, immune=2, pk=0, regen=1, cryo=2),
        provides=dict(human=1, organism=0, behaviour=0, vertebrate=1, throughput=0, longterm=0, regulatory=0),
        strengths="Keeps the native architecture and every cell type of the tissue; one animal or donor gives many slices.",
        limits="Short viability (days); limited throughput.",
        bankable="Partly. Cryopreserved slices and tissue banks extend use of each donor.",
    ),
    dict(
        key="rodent", name="Rodents (mice, rats)", tier=5,
        status="Protected under ASPA. Needs establishment, project and personal licences, ethical review and full application of the 3Rs.",
        scores=dict(hepatotox=2, gut=2, neural=3, sensory=3, devgen=2, immune=3, pk=3, regen=3, cryo=2),
        provides=dict(human=0, organism=1, behaviour=1, vertebrate=1, throughput=0, longterm=1, regulatory=1),
        strengths="Whole mammalian physiology, systemic exposure, adaptive immunity and complex behaviour.",
        limits="Ethical cost; species differences from humans; lower throughput and higher cost.",
        bankable="Yes. Embryo and sperm cryopreservation lets lines be archived instead of bred continuously.",
    ),
]

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
