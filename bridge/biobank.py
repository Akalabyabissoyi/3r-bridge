"""Using human tissue, cells and biobank samples in UK research: what approvals apply.

Based on the Human Tissue Act 2004 (England, Wales and Northern Ireland), Human Tissue Authority (HTA)
guidance and Codes of Practice, Health Research Authority (HRA) guidance on research tissue banks, and the
UK Code of Practice for the Use of Human Stem Cell Lines. A learning aid, not legal advice.
"""

MATERIALS = {
    "human_tissue": "Human tissue or primary cells (fresh, frozen or fixed), including blood with cells",
    "cell_line": "An established human cell line, for example from a culture collection",
    "hesc": "A human embryonic stem cell line",
    "acellular": "Extracted DNA or RNA, or other cell-free material",
    "animal": "Animal tissue or cells",
}

SOURCES = {
    "rtb": "A research tissue bank with ethical (REC) approval",
    "project_rec": "Collected for my own project, which has REC approval",
    "other": "Another source, from abroad, or I am not sure",
}


def biobank_verdict(material: str, source: str = "rtb", identifiable: bool = False, deceased: bool = False,
                    patients: bool = False, gm: bool = False) -> tuple[str, str, list[str]]:
    """Return (headline, level, what you need). Level is 'none', 'conditions' or 'licence'."""
    needs: list[str] = []
    if patients and material != "animal":
        return ("A different regime applies: human application", "licence", [
            "Procuring, testing, processing, storing or distributing human tissue or cells for use in patients "
            "needs an HTA licence under the Human Tissue (Quality and Safety for Human Application) Regulations 2007.",
            "If the cells are manufactured into a medicine, such as an advanced therapy, the MHRA regulates it and "
            "manufacture must follow Good Manufacturing Practice.",
            "Talk to your institution's HTA Designated Individual and regulatory affairs team before you start.",
        ])

    if material == "human_tissue":
        if deceased:
            needs.append("Tissue from people who have died always needs appropriate consent for research; "
                         "anonymising it does not remove this.")
        if source == "rtb":
            if identifiable:
                headline, level = "You need your own ethical approval", "conditions"
                needs += ["A bank's generic ethical approval covers projects that receive non-identifiable samples. "
                          "If samples or data could identify donors to you, apply for project-specific REC approval "
                          "(through IRAS).",
                          "With project-specific REC approval, you do not need HTA-licensed premises for storage "
                          "during the project."]
            else:
                headline, level = "No HTA licence needed for your storage, within the bank's terms", "conditions"
                needs += ["Use the samples only within the bank's approved terms and the donors' consent.",
                          "Samples and data must be non-identifiable to you when released.",
                          "Sign the bank's supply agreement (material transfer agreement) before samples arrive.",
                          "Return or dispose of leftover material as the agreement says, and keep records."]
        elif source == "project_rec":
            headline, level = "No HTA licence needed while your REC approval lasts", "conditions"
            needs += ["Storage for an ethically approved project does not need HTA-licensed premises.",
                      "Get consent unless your REC agreed an exception, for example residual tissue from living "
                      "people that you cannot link to them.",
                      "When the approval ends, leftover tissue must be disposed of, moved to HTA-licensed premises "
                      "or transferred to a research tissue bank."]
        else:
            headline, level = "Storage for research usually needs an HTA licence", "licence"
            needs += ["Store the tissue on premises covered by your institution's HTA research licence, or obtain "
                      "project-specific REC approval.",
                      "Check that the donors' consent covers your use, including for tissue from abroad.",
                      "Ask your HTA Designated Individual before ordering: they oversee the licence."]
    elif material == "cell_line":
        headline, level = "Cell lines are not 'relevant material': no HTA licence needed", "none"
        needs += ["Check the supplier documents ethical sourcing and donor consent for your type of use.",
                  "Read the material transfer agreement, especially limits on commercial use and sharing.",
                  "Authenticate the line (STR profile) and test for mycoplasma.",
                  "If you derive a line yourself from tissue, the tissue rules apply until the original cells "
                  "have been replaced by division in culture."]
    elif material == "hesc":
        headline, level = "Follow the stem cell line Code of Practice", "conditions"
        needs += ["Access to human embryonic stem cell lines has required approval from the UK Stem Cell Bank "
                  "Steering Committee; check the current process with the UK Stem Cell Bank.",
                  "Follow the Code of Practice for the Use of Human Stem Cell Lines.",
                  "Creating new lines from embryos is licensed by the HFEA."]
    elif material == "acellular":
        headline, level = "Cell-free material is not 'relevant material': no HTA licence needed", "none"
        needs += ["Storing tissue briefly only to extract DNA or RNA does not need an HTA licence.",
                  "Analysing human DNA still needs the donors' consent or an exception agreed by a REC.",
                  "Genetic data is special category data under UK GDPR: agree how it is stored and shared."]
    else:
        headline, level = "No HTA licence: animal tissue is outside the Human Tissue Act", "none"
        needs += ["Tissue from animals killed by a Schedule 1 method needs no Home Office project licence; "
                  "procedures on living animals to obtain it do.",
                  "Sharing tissue between groups is a Reduction measure: ask your animal unit about tissue sharing.",
                  "Importing animal products may need an APHA import authorisation; check biosafety for zoonoses."]

    if identifiable and material in ("human_tissue", "acellular", "cell_line"):
        needs.append("Identifiable data comes under UK GDPR: agree a data protection plan with your data "
                     "protection officer.")
    if gm:
        needs.append("Genetic modification needs a GM risk assessment approved by your genetic modification "
                     "safety committee, and HSE notification depending on the class of activity.")
    return headline, level, needs


ASK_BIOBANK = [
    ("Consent", "Does the donors' consent cover my use, including genetic analysis, commercial work and data sharing?"),
    ("Approvals", "What ethical approval does the bank hold, and what are its release terms?"),
    ("Before freezing", "How long between collection and processing, and how long until freezing?"),
    ("Freezing", "Which cryoprotectant, cooling rate and container were used?"),
    ("Storage", "At what temperature, for how long, and how many freeze and thaw cycles so far?"),
    ("After thawing", "What viability, recovery and function were measured after thawing, and how long do cells "
                      "need to recover before they are ready to use?"),
    ("Quality", "Is the bank accredited, for example to ISO 20387 for biobanking, with full traceability?"),
    ("Cell lines", "Is there an STR profile, a mycoplasma result and a passage number?"),
    ("Data", "What clinical data comes with the samples, and under what agreement?"),
    ("Shipping", "Dry shipper or dry ice, and is the temperature logged in transit?"),
]

WHO_HELPS = [
    ("HTA Designated Individual", "Oversees your institution's HTA licence; ask before you store any human tissue."),
    ("Tissue bank manager", "Explains what samples exist, the access process and the supply agreement."),
    ("Research Ethics Committee", "Reviews projects that need their own approval, through IRAS."),
    ("Research governance and contracts", "Sign material transfer and data agreements on your institution's behalf."),
    ("Biological and GM safety officer", "Risk assessments for infectious material and genetic modification."),
    ("Data protection officer", "Advises when samples come with personal or genetic data."),
]

FIND = [
    ("UKCRC Tissue Directory", "https://www.biobankinguk.org/", "Search UK biobanks and their sample collections."),
    ("UK Biobank", "https://www.ukbiobank.ac.uk/", "Data and samples from 500,000 volunteers, by application."),
    ("BBMRI-ERIC Directory", "https://directory.bbmri-eric.eu/", "European biobanks and collections."),
    ("Culture collections", "https://www.culturecollections.org.uk/", "Authenticated cell lines, such as ECACC."),
]

REFERENCES = [
    ("HTA research FAQs", "https://www.hta.gov.uk/guidance-professionals/guidance-sector/research/research-faqs"),
    ("HRA: research tissue banks",
     "https://www.hra.nhs.uk/planning-and-improving-research/policies-standards-legislation/research-tissue-banks-and-research-databases/research-tissue-banks-faqs/"),
    ("HRA: use of human tissue in research",
     "https://www.hra.nhs.uk/planning-and-improving-research/policies-standards-legislation/use-tissue-research/"),
    ("HTA: human application", "https://www.hta.gov.uk/guidance-professionals/guidance-sector/human-application"),
    ("UK Stem Cell Bank: policies",
     "https://nibsc.org/science_and_research/advanced_therapies/uk_stem_cell_bank/policies_guidelines_and_due_diligence.aspx"),
]
