"""Plain-English licence guide for researchers new to in vivo work in the UK.

Definitions follow the Home Office "Guidance on the operation of the Animals
(Scientific Procedures) Act 1986" and its training guidance (November 2024).
Non-technical summary headings follow the Home Office published summaries.
This is a learning aid, not legal advice: the establishment's Named Persons
and the Home Office always have the final word.
"""
from __future__ import annotations

import re

# ------------------------------------------------------------- 1. do I need a licence?
SUBJECTS = {
    "none": "Human cells, human tissue or other non-animal methods only",
    "invert": "Invertebrates other than cephalopods (for example fruit flies, worms)",
    "tissue": "Tissue from animals killed humanely by someone else (Schedule 1)",
    "fish_amph": "Fish or amphibians",
    "mammal_bird_reptile": "Mammals, birds or reptiles (for example mice, rats)",
    "cephalopod": "Cephalopods (octopus, squid, cuttlefish)",
}


def licence_verdict(subject: str, stage_protected: bool, above_needle: bool, ga_harmful: bool,
                    schedule1_only: bool) -> tuple[str, str, list[str]]:
    """Return (headline, level, notes). level is one of 'none', 'schedule1', 'licence'."""
    notes = []
    if subject in ("none", "invert"):
        return ("ASPA does not apply to this work.", "none",
                ["No Home Office licence is needed. Good practice, ethics and any human tissue rules still apply."])
    if subject == "tissue":
        return ("You do not need a licence to use the tissue.", "none",
                ["The person who kills the animal by a Schedule 1 method must be trained, competent and on the "
                 "establishment's Schedule 1 register.",
                 "Sharing tissue from animals already used is a good Reduction step: ask your NACWO what is available."])
    if not stage_protected:
        return ("The animals are not yet protected at the life stage you will use.", "none",
                ["Fish and amphibians are protected once they can feed independently; mammals, birds and reptiles "
                 "from the last third of gestation or incubation; cephalopods from hatching.",
                 "Check the exact cut-off with your NTCO or NVS before you start. Once animals pass it, ASPA applies."])
    if schedule1_only and not above_needle and not ga_harmful:
        return ("Killing by a Schedule 1 method is not a regulated procedure.", "schedule1",
                ["You still need training and a competence sign-off, and you must be on the establishment's "
                 "Schedule 1 register before you do it unsupervised.",
                 "It must take place in a licensed establishment."])
    if above_needle or ga_harmful:
        if ga_harmful:
            notes.append("Breeding genetically altered animals that may suffer harm is itself a regulated procedure.")
        notes += ["You need a personal licence (PIL) for the techniques you will perform.",
                  "Your work must sit under a project licence (PPL), held by the scientist responsible for the programme.",
                  "The establishment must hold an establishment licence, and your project needs AWERB review."]
        return ("This is a regulated procedure under ASPA.", "licence", notes)
    return ("Probably not regulated, but check.", "none",
            ["If anything you do could cause pain, suffering, distress or lasting harm equal to a needle insertion "
             "or more, it becomes regulated. When unsure, ask your NTCO before you start."])


# ------------------------------------------------------------- 2. which personal licence?
TECHNIQUES = {
    "handling": ("Handling, restraint and observation", "A"),
    "injection": ("Injections or dosing without anaesthesia (for example subcutaneous, intraperitoneal, oral)", "A"),
    "blood": ("Blood sampling without anaesthesia", "A"),
    "behaviour": ("Behavioural tests that may cause stress", "A"),
    "brief_ga": ("Minor procedures under sedation or brief general anaesthesia (for example imaging, intravitreal injection)", "B"),
    "nonrecovery": ("Surgery under brief non-recovery general anaesthesia", "B"),
    "surgery": ("Surgery under general anaesthesia with recovery", "C"),
    "long_ga": ("Balanced or prolonged general anaesthesia", "C"),
    "nmb": ("Neuromuscular blocking agents", "D"),
}

CATEGORY_TEXT = {
    "A": "Minor or minimally invasive procedures not requiring sedation, analgesia or general anaesthesia.",
    "B": "Minor or minimally invasive procedures involving sedation, analgesia or brief general anaesthesia; "
         "surgical procedures under brief non-recovery general anaesthesia.",
    "C": "Surgical procedures involving general anaesthesia; balanced or prolonged general anaesthesia.",
    "D": "Use of neuromuscular blocking agents.",
}

MODULES = {
    "L": "Legislation (UK national module)",
    "E1": "Ethics, animal welfare and the 3Rs (level 1)",
    "PILA": "Basic biology, husbandry, humane killing and minor procedures, species-specific (theory and skills)",
    "K": "Humane killing (theory and skills)",
    "20": "Anaesthesia for minor procedures",
    "21": "Advanced anaesthesia",
    "22": "Principles of surgery",
}


def pil_categories(selected: list[str]) -> list[str]:
    """Personal licence categories implied by the techniques chosen (A is always included)."""
    cats = {"A"} | {TECHNIQUES[t][1] for t in selected}
    if "C" in cats:  # Home Office training routes treat PIL C as building on A and B
        cats.add("B")
    order = ["A", "B", "C", "D"]
    return [c for c in order if c in cats]


def modules_for(categories: list[str]) -> list[str]:
    """Accredited modules for the highest category, per Home Office training guidance (Nov 2024)."""
    mods = ["L", "E1", "PILA", "K"]
    if "B" in categories or "C" in categories:
        mods.append("20")
    if "C" in categories:
        mods += ["21", "22"]
    return mods


# ------------------------------------------------------------- 3. who to talk to
NAMED_PERSONS = [
    ("NTCO", "Named Training and Competency Officer",
     "Your training route, modules, supervision and competence sign-off. Talk to them first."),
    ("NACWO", "Named Animal Care and Welfare Officer",
     "Day-to-day care and husbandry, housing, and the practicalities of running your study in the unit."),
    ("NVS", "Named Veterinary Surgeon",
     "Anaesthesia, analgesia, humane endpoints and any animal health concern, at any time."),
    ("NIO", "Named Information Officer",
     "Species information, local SOPs and 3Rs resources."),
    ("HOLC", "Home Office Liaison Contact",
     "Submitting and tracking licence applications on ASPeL."),
    ("AWERB", "Animal Welfare and Ethical Review Body",
     "Reviews project licence applications and amendments; can advise on the 3Rs before you submit."),
    ("PPL holder", "Your project licence holder",
     "Owns the programme of work; makes sure your procedures are covered by a protocol and supervises you."),
]

# ------------------------------------------------------------- 4. severity
SEVERITY = {
    "sub-threshold": "Below the threshold for a regulated procedure (used when reporting actual severity).",
    "non-recovery": "Performed entirely under general anaesthesia from which the animal does not recover consciousness.",
    "mild": "Likely short-term mild pain, suffering or distress, with no significant impairment of well-being or general condition.",
    "moderate": "Likely short-term moderate pain, suffering or distress, or long-lasting mild pain, suffering or distress, "
                "or moderate impairment of well-being or general condition.",
    "severe": "Likely severe pain, suffering or distress, or long-lasting moderate pain, suffering or distress, "
              "or severe impairment of well-being or general condition.",
}

ENDPOINTS = [
    "Body weight loss of more than a set percentage of baseline (agree the figure with your NVS)",
    "Hunched posture, piloerection or reduced movement lasting longer than a set time",
    "Not eating or drinking",
    "Tumour size above a set limit, or ulceration",
    "Wound breakdown or infection after surgery",
    "Signs of pain on a grimace scale above an agreed score",
    "Any unexpected adverse effect not described in the protocol",
]

# ------------------------------------------------------------- 5. non-technical summary
# Headings as used in Home Office published non-technical summaries.
NTS = [
    ("Objectives and benefits", [
        ("aim", "What's the aim of this project?", "One or two sentences a non-scientist would understand."),
        ("why", "Why is it important to undertake this work?", "The problem and who it affects."),
        ("outputs", "What outputs do you think you will see at the end of this project?", "Papers, data, new methods, candidate treatments."),
        ("benefit", "Who or what will benefit from these outputs, and how?", "Patients, other scientists, animals, industry; short and long term."),
        ("maximise", "How will you look to maximise the outputs of this work?", "Open data, publishing negative results, sharing tissue and methods."),
    ]),
    ("Predicted harms", [
        ("species", "Species and numbers of animals expected to be used", "For example: Mice: 600."),
        ("why_species", "Explain why you are using these types of animals and your choice of life stages", ""),
        ("typical", "Typically, what will be done to an animal used in your project?", "Plain description of the procedures, how often and for how long."),
        ("effects", "What are the expected impacts and/or adverse effects for the animals during your project?", ""),
        ("severity", "Expected severity categories and the proportion of animals in each category, per species", ""),
        ("fate", "What will happen to animals at the end of this project?", "For example: killed humanely, kept alive, re-homed."),
    ]),
    ("Replacement", [
        ("need_animals", "Why do you need to use animals to achieve the aim of your project?", ""),
        ("alternatives", "Which non-animal alternatives did you consider for use in this project?", ""),
        ("not_suitable", "Why were they not suitable?", ""),
    ]),
    ("Reduction", [
        ("numbers", "How have you estimated the numbers of animals you will use?", ""),
        ("design", "What steps did you take during the experimental design phase to reduce the number of animals being used in this project?", ""),
        ("optimise", "What measures, apart from good experimental design, will you use to optimise the number of animals you plan to use in your project?", "Pilot studies, efficient breeding, sharing tissue, imaging for repeated measures."),
    ]),
    ("Refinement", [
        ("models", "Which animal models and methods will you use during this project? Explain why these models and methods cause the least pain, suffering, distress, or lasting harm to the animals", ""),
        ("less_sentient", "Why can't you use animals that are less sentient?", ""),
        ("refine", "How will you refine the procedures you're using to minimise the welfare costs (harms) for the animals?", ""),
        ("guidance", "What published best practice guidance will you follow to ensure experiments are conducted in the most refined way?", "For example: PREPARE, ARRIVE 2.0, NC3Rs resources, LASA guidance."),
        ("informed", "How will you stay informed about advances in the 3Rs, and implement these advances effectively, during the project?", "For example: NC3Rs newsletters, your NIO, local 3Rs events."),
    ]),
]

# Words that commonly make summaries hard for lay readers, with plainer options.
JARGON = {
    "in vivo": "in living animals", "in vitro": "in cells or tissue in the lab", "murine": "mouse",
    "phenotype": "characteristics", "pathogenesis": "how the disease develops", "efficacy": "how well it works",
    "aetiology": "cause", "etiology": "cause", "intraperitoneal": "into the abdomen", "subcutaneous": "under the skin",
    "intravenous": "into a vein", "administration": "giving", "transgenic": "genetically altered",
    "knockout": "with a gene switched off", "morbidity": "illness", "mortality": "death", "cohort": "group",
    "elucidate": "find out", "utilise": "use", "therapeutic": "treatment", "paradigm": "approach",
    "longitudinal": "over time", "inoculation": "injection", "xenograft": "human tumour grown in a mouse",
}


def readability(text: str) -> dict:
    """Simple plain-language checks: sentence length and jargon hits."""
    sentences = [s for s in re.split(r"[.!?]+\s", text.strip()) if s.strip()]
    words = re.findall(r"[A-Za-z']+", text)
    avg = len(words) / len(sentences) if sentences else 0
    low = " " + text.lower() + " "
    hits = [(w, alt) for w, alt in JARGON.items() if re.search(r"\b" + re.escape(w) + r"\b", low)]
    long_words = [w for w in words if len(w) >= 13]
    return {"words": len(words), "sentences": len(sentences), "avg": avg, "jargon": hits, "long_words": sorted(set(long_words))}


CHECKLIST = [
    "Accredited modules completed for my personal licence category",
    "Supervised practice done and competence signed off for each technique",
    "Met the NTCO, NACWO and NVS to discuss my plans",
    "Experimental design checked (for example with the NC3Rs Experimental Design Assistant)",
    "Non-animal alternatives searched and recorded",
    "Humane endpoints and a welfare score sheet agreed with the NVS",
    "Non-technical summary reviewed by someone outside my field",
    "AWERB review booked or completed",
    "Application submitted on ASPeL through the HOLC",
]


# ------------------------------------------------------------- jargon buster
GLOSSARY = {
    "ASPA": "The Animals (Scientific Procedures) Act 1986, the UK law that regulates scientific work on protected animals.",
    "ASRU": "The Animals in Science Regulation Unit, the part of the Home Office that grants licences and inspects establishments.",
    "ASPeL": "The Home Office's online system for applying for and managing licences.",
    "PIL": "Personal licence. Held by each person who carries out regulated procedures. This is the licence most new researchers apply for.",
    "PPL": "Project licence. Covers a programme of work and its protocols; usually held by the principal investigator. You work under it.",
    "PEL": "Establishment licence. Held by the institution where the work happens.",
    "Protocol": "One defined series of procedures within a project licence, with its own severity limit and humane endpoints.",
    "Regulated procedure": "Anything done to a protected animal for a scientific purpose that may cause pain, suffering, distress or lasting harm equal to a needle insertion or more.",
    "Protected animal": "Any living vertebrate other than humans, and any living cephalopod, from the life stages set out in the Act.",
    "Schedule 1": "The list of humane killing methods in the Act. Killing by these methods is not a regulated procedure, but you must be trained and on the register.",
    "Severity limit": "The most a protocol is allowed to affect an animal: sub-threshold, non-recovery, mild, moderate or severe.",
    "Actual severity": "What each animal actually experienced, recorded and reported to the Home Office every year.",
    "Humane endpoint": "A clear, pre-agreed sign that an animal must be removed from the study or humanely killed, to stop suffering going further.",
    "NTCO": "Named Training and Competency Officer. Makes sure you are trained, supervised and signed off as competent.",
    "NACWO": "Named Animal Care and Welfare Officer. Oversees day-to-day care and welfare in the animal unit.",
    "NVS": "Named Veterinary Surgeon. Advises on animal health, anaesthesia, pain relief and endpoints.",
    "NIO": "Named Information Officer. Makes sure you can find the information you need about your species and procedures.",
    "HOLC": "Home Office Liaison Contact. Handles licence applications and communication with the Home Office.",
    "NPRC": "Named Person Responsible for Compliance. Accountable for the establishment meeting its licence conditions.",
    "AWERB": "Animal Welfare and Ethical Review Body. Every establishment has one; it reviews project licences and promotes the 3Rs.",
    "NTS": "Non-technical summary. A plain-English summary of a project licence, published by the Home Office.",
    "Competence sign-off": "The point at which your establishment confirms you can perform a technique on a species without supervision.",
    "The 3Rs": "Replacement (avoid or replace animals), Reduction (use fewer), Refinement (minimise suffering and improve welfare).",
    "Culture of care": "An environment where everyone feels responsible for animal welfare and safe to raise concerns.",
    "NC3Rs": "The National Centre for the Replacement, Refinement and Reduction of Animals in Research, the UK's 3Rs organisation.",
}

# ------------------------------------------------------------- the journey
JOURNEY = [
    ("Check", "Find out whether your work needs a licence"),
    ("Train", "Complete the accredited modules for your category"),
    ("Prepare", "Prepare your personal licence application with the NTCO"),
    ("Apply", "Submit on ASPeL, endorsed by your establishment"),
    ("Granted", "The Home Office grants your personal licence"),
    ("Practise", "Work under supervision on each technique"),
    ("Signed off", "Assessed as competent; work independently"),
    ("Keep learning", "CPD and regular competence review"),
]

# ------------------------------------------------------------- does my procedure count?
EXAMPLES_REGULATED = [
    "Injections (under the skin, into the abdomen, into a vein)",
    "Taking blood samples",
    "Dosing by mouth with a tube (gavage)",
    "Surgery, with or without recovery",
    "Diets or treatments expected to cause harm",
    "Breeding animals with a harmful genetic alteration",
    "Behavioural tests that may cause distress",
]
EXAMPLES_NOT_REGULATED = [
    "Watching or observing animals",
    "Routine husbandry and handling for care",
    "Humane killing by a Schedule 1 method (training and the register still apply)",
    "Work on invertebrates other than cephalopods, such as fruit flies",
    "Cells and tissue in the lab, including tissue from animals killed by Schedule 1",
]

# ------------------------------------------------------------- common worries
WORRIES = [
    ("I have never done a procedure. Will I be thrown in at the deep end?",
     "No. After your modules you practise under supervision, and you only work alone once you have been assessed as "
     "competent for each technique and species. Ask your NTCO who will supervise you."),
    ("What if I make a mistake during a procedure?",
     "Stop, make the animal safe and tell the NACWO or NVS straight away. Reporting early protects the animal and you. "
     "A good establishment treats this as a chance to learn, not to blame."),
    ("What if an animal looks unwell and I am not sure what to do?",
     "Contact the NACWO or the NVS, who can be reached at any time. Your protocol's humane endpoints tell you when an "
     "animal must be removed from the study."),
    ("I trained in another country. Do I have to start again?",
     "Not always. Previous training may count towards the modules. Bring your certificates to your NTCO and ask about exemptions."),
    ("Do I need a licence just to watch or help in the animal unit?",
     "No licence is needed to observe. You need one only to carry out regulated procedures yourself."),
    ("Who writes the project licence?",
     "Usually your principal investigator. As a new researcher you normally apply for a personal licence and work "
     "under their project licence."),
    ("Who can I talk to if I have a concern about how animals are treated?",
     "Any Named Person, especially the NACWO or NVS. Establishments also have routes to raise concerns confidentially."),
]

# ------------------------------------------------------------- personal licence preparation
SPECIES = ["Mouse", "Rat", "Zebrafish", "Xenopus", "Guinea pig", "Rabbit", "Other"]

CHECKLIST_PIL = [
    "Checked with the NTCO that my work needs a personal licence",
    "Accredited modules completed and certificates ready",
    "Supervisor and project licence holder agreed, and I know the project licence number",
    "Protocols I will work under identified with the project licence holder",
    "Visited the animal unit and met the NACWO and NVS",
    "Supervised practice plan agreed with the NTCO",
    "Application completed on ASPeL and sent for endorsement by my establishment",
]

# Which journey stage each guide step belongs to.
STEP_STAGE = [0, 1, 2, 2, 3]
