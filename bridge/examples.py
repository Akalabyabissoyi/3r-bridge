"""Worked examples: three published Home Office non-technical summaries, condensed and annotated.

Source: Home Office, "Non-technical summaries for projects granted in 2025, July to September",
projects 1 to 3. Contains public sector information licensed under the Open Government Licence v3.0.
The text below is condensed, not verbatim; read the original for the full wording.
"""

SOURCE_URL = ("https://assets.publishing.service.gov.uk/media/69147901eba5bda2026fc82b/"
              "Non-technical+summaries+for+projects+granted+in+2025_+July+to+September.pdf")
SOURCE_PAGE = "https://www.gov.uk/government/publications/non-technical-summaries-granted-in-2025"
CREDIT = ("Condensed from Home Office non-technical summaries for projects granted July to September 2025. "
          "Contains public sector information licensed under the Open Government Licence v3.0.")

EXAMPLES = [
    {
        "key": "cancer",
        "label": "Mouse cancer model",
        "art": "mouse",
        "title": "Analysis of psychological stressors in cancer",
        "ref": "Project 2, page 11",
        "facts": {"Species": "Mice (BALB/c and C57BL/6), adults", "Numbers": "1,500", "Duration": "5 years",
                  "Purpose": "Basic and translational research", "Fate": "Killed at the end"},
        "severity": {"Mild": 0, "Moderate": 100},
        "why_read": "A typical tumour study. Notice how precisely it sets its humane endpoints.",
        "sections": [
            ("Aim and importance",
             "To understand how stress, such as restraint or social isolation, influences how breast, ovarian, "
             "endometrial, pancreatic and prostate cancers grow and spread, and whether stress changes how well "
             "treatments work. Links between stress and cancer are known mostly from population studies; the "
             "mechanisms are not.",
             "The importance case is short and concrete: how common the cancers are, and what is not yet known."),
            ("Benefits and sharing",
             "Patients, clinicians and researchers benefit: better awareness of stress management, better drug use "
             "and better trial design. Results go to journals and conferences, and the team gives talks to patient "
             "forums and runs lab tours.",
             "Benefits are given with timescales (publications in 1 to 2 years, clinical use in 5 to 10)."),
            ("Typical procedures",
             "Restraint in a tube for 1 to 2 hours a day, up to 8 weeks, or single housing. Cancer cells are injected "
             "under the skin, into the abdomen or mammary fat pad, or into the heart under isoflurane anaesthesia. "
             "Some mice receive a hormone blocker by mouth or injection.",
             "Each procedure states the route, duration and whether anaesthesia is used."),
            ("Harms and humane endpoints",
             "Tumours may reach a set maximum size (1.2 cm mean diameter, or 1.5 cm for drug studies). Spread to bone "
             "can cause limping or weight loss. A 10% loss of body weight, limping or lethargy are assessed, and mice "
             "close to the size limit are killed before it is exceeded.",
             "Endpoints are numbers someone can measure on the day, not vague words like 'unwell'."),
            ("Replacement",
             "The lab already uses cell lines and is developing organoids from human tumour tissue. These cannot yet "
             "reproduce the 3D tissue environment, mix of cell types and blood factors needed to study spread.",
             "It names the alternatives it actually uses and says exactly what they cannot do."),
            ("Reduction",
             "About 10 mice per group, usually 3 or 4 groups, from power calculations. Design was checked with "
             "statisticians and the NC3Rs Experimental Design Assistant. Tissue is shared with other researchers.",
             "Group size comes from a calculation and named tools; tissue sharing gets more from each animal."),
            ("Refinement",
             "Anaesthesia and pain relief whenever possible, weekly weighing, close monitoring for 2 hours after "
             "anaesthesia, high-calorie food for weight loss. Follows the Workman et al. (2010) cancer welfare "
             "guidelines and LASA guidance; checks the NC3Rs website monthly.",
             "It cites the field's welfare guideline, which reviewers look for in cancer work."),
        ],
    },
    {
        "key": "neuro",
        "label": "Mouse dementia research",
        "art": "tissue",
        "title": "Cellular mechanisms underlying neurodegeneration",
        "ref": "Project 3, page 19",
        "facts": {"Species": "Mice, embryo to aged", "Numbers": "4,400", "Duration": "5 years",
                  "Purpose": "Basic and translational research", "Fate": "Killed, or used in other projects"},
        "severity": {"Mild": 80, "Moderate": 20},
        "why_read": "Many animals are bred and aged rather than treated. Notice the case for mice over flies, worms or fish.",
        "sections": [
            ("Aim and importance",
             "To find how chemical and structural changes in brain proteins disrupt communication between brain "
             "cells and cause dementia, such as Alzheimer's disease, and so identify new routes to treatment.",
             "One clear sentence of aim, linked to a disease people recognise."),
            ("Benefits and sharing",
             "Open-access papers, published methods so others can repeat the work, training for industry researchers, "
             "public events, and publishing unsuccessful studies to stop others repeating them.",
             "Publishing negative results is itself a Reduction measure."),
            ("Typical procedures",
             "Breeding normal and genetically altered mice, some aged up to 2 years; giving some mice substances that "
             "change ageing or disease; and collecting tissue from young mice for brain cell and brain slice cultures.",
             "Breeding and ageing genetically altered animals can itself be a regulated procedure."),
            ("Harms",
             "Ageing mice may get benign tumours, hair loss or sore skin; dementia models show worsening learning "
             "and memory, and some have mobility problems. One line is prone to eye infections and is watched for them.",
             "Harms are listed per mouse line, including the boring but real ones of old age."),
            ("Replacement",
             "Human cell lines, stem-cell-derived brain cells, human post-mortem brain and computer modelling were "
             "all considered. Cell lines are genetically altered by immortalisation, stem-cell neurons are 'newborn' "
             "so poor for ageing, and post-mortem brain is a single snapshot that cannot be followed over time.",
             "Each alternative gets its own specific reason. This is what the Model Finder helps you write."),
            ("Reduction",
             "Formal calculations and pilots; much earlier mouse work replaced with long-term brain slice cultures, "
             "testing several conditions on tissue from one animal; tissue stored for many analyses; breeding planned "
             "so all pups are used.",
             "Ex vivo slices are a rung on the replacement ladder that also reduces numbers."),
            ("Refinement",
             "Uses models with only mild to moderate disease and avoids terminal stages; prefers young mice; handles "
             "mice before dosing. Mice are chosen because key Alzheimer's pathways are missing from fruit flies, worms "
             "and fish. Follows ARRIVE 2.0 and PREPARE.",
             "It explains why a less sentient species will not do, in terms of biology."),
        ],
    },
    {
        "key": "zebrafish",
        "label": "Zebrafish regeneration",
        "art": "fish",
        "title": "Analysis of cell signalling in a zebrafish disease regeneration model",
        "ref": "Project 1, page 5",
        "facts": {"Species": "Zebrafish, embryo to aged", "Numbers": "11,500", "Duration": "5 years",
                  "Purpose": "Basic research", "Fate": "Killed, or kept for non-regulated use or reuse"},
        "severity": {"Mild": 98, "Moderate": 2},
        "severity_text": "Mostly mild; under 2% moderate",
        "why_read": "Most of the science happens before fish are protected. Notice how life stage drives the design.",
        "sections": [
            ("Aim and importance",
             "To understand how cell signals control regeneration after injury. Fish can regrow organs after extensive "
             "damage, which may point to treatments for degenerative disease and injury.",
             "The species is chosen for a biological ability, not convenience."),
            ("Benefits and sharing",
             "Papers, conferences and possible patents; datasets in public repositories; manuscripts and theses "
             "posted online.",
             "Sharing raw data lets others reuse it instead of repeating experiments."),
            ("Typical procedures",
             "More than 95% of fish are used for breeding. Most experiments cut the tail tip at 2 to 3 days old and "
             "follow regrowth until 5.2 days, before the age of protection. Other fish receive drugs or have a small "
             "piece of fin removed.",
             "Compare with step 1: larval fish before independent feeding are not protected."),
            ("Harms",
             "Most fish lead healthy lives. Unexpected effects such as sores, ragged fins, swelling, tumours or weight "
             "loss lead to humane killing by a Schedule 1 method.",
             "A clear rule for what happens if an animal shows signs."),
            ("Replacement",
             "Cell culture cannot reproduce the interacting tissues of regeneration, such as inflammation and new "
             "blood vessels, or reveal signals from unexpected sources.",
             "Short and specific: what is missing in vitro."),
            ("Reduction",
             "Colony sizes are planned for breeding mutant and transgenic lines; each experiment has a written plan "
             "with group sizes and analysis; fish are genotyped before the protected age so only needed fish are raised.",
             "Early genotyping is a simple, powerful Reduction step."),
            ("Refinement",
             "Zebrafish are described as the least sentient vertebrate suitable. Transparent larvae let labelled "
             "cells be followed without killing; drugs are added to the water rather than injected; injuries are tiny "
             "and heal fast; anaesthesia and close monitoring are used.",
             "Each refinement removes a source of harm, such as injection or repeated killing."),
        ],
    },
]
