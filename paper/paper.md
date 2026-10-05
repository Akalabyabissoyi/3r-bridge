---
title: "3R Path: an open decision aid for choosing, preserving and justifying the least sentient research model"
tags:
  - Python
  - 3Rs
  - new approach methodologies
  - research ethics
  - biobanking
authors:
  - name: Akalabya Bissoyi
    orcid: 0000-0002-0909-8556
    affiliation: 1
affiliations:
  - name: Manchester Institute of Biotechnology, University of Manchester, UK
    index: 1
date: 5 October 2026
bibliography: paper.bib
---

<!-- DRAFT. Before submission: add the expert-review evaluation (docs/EXPERT_REVIEW.md), a usage/pilot section,
     the Zenodo DOI, and check every statement and reference. -->

# Summary

3R Path is an open-source Python and Streamlit tool that helps researchers choose the least sentient model able to answer a
research question, size a study, plan welfare refinements and export a structured 3Rs justification. It also includes a
plain-English guide to UK licensing under the Animals (Scientific Procedures) Act 1986 and a guide to approvals for human
tissue and biobank samples. Scoring data are versioned, referenced and open to community correction.

# Statement of need

The 3Rs principle [@russell1959] asks researchers to replace, reduce and refine animal use, and reporting and planning
guidelines such as ARRIVE 2.0 [@arrive2020] and PREPARE [@prepare2018] are widely endorsed. Early-career researchers and
members of review bodies still lack a quick, transparent way to ask, "what is the least sentient model that can genuinely
answer this question?", and to document the reasoning. Existing resources are mostly static guidance documents. 3R Path
turns that reasoning into an explicit, inspectable procedure and also supports preservation (cryopreservation and banking of
validated non-animal models, e.g. @bissoyi2023) so that models can be shared rather than rebuilt.

# Functionality

- **Model Finder:** scores eleven model types across nine research areas and seven requirements, returns the lowest adequate
  rung of a replacement ladder with reasons and literature, reports how robust that recommendation is to one-point scoring
  errors, and lets users override scores with a recorded reason.
- **Reduction:** sample-size calculators for two-group, paired, ANOVA, proportion and time-to-event designs with unequal
  allocation and attrition.
- **Exports:** Markdown, Word and JSON justification structured along PREPARE and ARRIVE lines.
- **Guides:** UK licence guide, human tissue and biobank guide, orientation notes for the EU, US and OECD.
- **Software:** installable package, command-line interface, Docker image, continuous integration and an automated check
  that flags out-of-date regulatory content.

# Limitations

Scores are expert judgements pending formal review. The tool is a learning and discussion aid, not regulatory advice.

# Acknowledgements

Worked examples are condensed from Home Office non-technical summaries (Open Government Licence v3.0).

# References
