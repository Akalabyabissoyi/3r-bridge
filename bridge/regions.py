"""Regulatory context beyond the UK, for researchers working under other regimes.

Short orientation notes with the instrument to read next, not legal advice. Check every point with your
institution's animal welfare body and the competent authority before relying on it. Review dates are shown in the app.
"""

LAST_REVIEWED = "2026-10-05"

REGIONS = {
    "uk": {
        "name": "United Kingdom",
        "law": "Animals (Scientific Procedures) Act 1986 (ASPA), enforced by the Home Office (Animals in Science Regulation Unit).",
        "protected": "Living vertebrates (mammals, birds and reptiles from the last third of gestation or incubation; fish and "
                     "amphibians from independent feeding) and cephalopods.",
        "authorisation": "Establishment, project and personal licences; local AWERB ethical review; Named Persons.",
        "alternatives": "A project licence must justify that no alternative to using protected animals is available, and apply the 3Rs.",
        "read_next": ["Home Office guidance on the operation of ASPA", "NC3Rs guidance and the ARRIVE guidelines 2.0"],
    },
    "eu": {
        "name": "European Union",
        "law": "Directive 2010/63/EU on the protection of animals used for scientific purposes, transposed into national law by each Member State.",
        "protected": "Live non-human vertebrates (larval forms from independent feeding; mammal, bird and reptile foetal forms "
                     "from the last third of development) and live cephalopods.",
        "authorisation": "Authorisation of establishments, projects (after a project evaluation, including harm-benefit assessment) and "
                         "competent persons by national competent authorities; an animal-welfare body at each establishment.",
        "alternatives": "Member States must not allow a procedure if another method not using live animals is recognised and "
                        "reasonably practicable (Article 13 of the Directive).",
        "read_next": ["Directive 2010/63/EU", "EURL ECVAM validated methods (EU Reference Laboratory for alternatives to animal testing)"],
    },
    "us": {
        "name": "United States",
        "law": "Animal Welfare Act (USDA) and the Public Health Service Policy (NIH/OLAW) for funded work; institutional "
               "IACUC review under the Guide for the Care and Use of Laboratory Animals.",
        "protected": "The Animal Welfare Act excludes rats of the genus Rattus, mice of the genus Mus bred for research and birds bred "
                     "for research; the PHS Policy covers all live vertebrate animals in funded work, so those species are still reviewed.",
        "authorisation": "Local IACUC protocol approval; no national project licence equivalent to the UK or EU.",
        "alternatives": "Researchers must consider alternatives and justify the number of animals. The FDA Modernization Act 2.0 (2022) "
                        "removed the statutory requirement for animal testing before drug trials, allowing validated non-animal methods.",
        "read_next": ["NIH OLAW PHS Policy", "FDA Modernization Act 2.0 and FDA guidance on new approach methodologies (NAMs)"],
    },
    "oecd": {
        "name": "OECD and ICH (data acceptance)",
        "law": "OECD Test Guidelines and the Mutual Acceptance of Data system; ICH guidelines for pharmaceuticals.",
        "protected": "Not applicable: these set which test results regulators will accept, not which animals are protected.",
        "authorisation": "None. Use a validated Test Guideline when a regulatory submission is the aim.",
        "alternatives": "Many OECD Test Guidelines are non-animal (for example in vitro skin and eye irritation) and can be "
                        "used in place of animal tests where the guideline covers the endpoint.",
        "read_next": ["OECD Test Guidelines programme", "ICH guidelines relevant to your product type"],
    },
}
