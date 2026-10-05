# Expert review protocol

The catalogue scores are currently **author judgement** (`review.status = "author-judgement"` in `bridge/data/models.json`).
This protocol turns them into community-reviewed values, and gives a record you can cite in a paper.

## Round design (modified Delphi)

1. **Panel.** Recruit 8-12 reviewers with relevant expertise: NAMs and in vitro modelling, in vivo pharmacology and
   toxicology, invertebrate and fish models, Named Persons (NACWO, NVS, NTCO), AWERB members. Note affiliation and years of experience.
2. **Round 1 (independent).** Each reviewer scores every model for every research area (0-3) and every requirement
   flag (0/1) in `reviews/template.csv` format, with a one-line rationale or citation wherever they differ from the catalogue by 2 or more.
3. **Summary.** Run `python scripts/review_stats.py reviews/round1.csv`. It reports the median, IQR and agreement
   (share of reviewers within one point of the median), and flags cells where the median differs from the catalogue.
4. **Round 2.** Share the anonymised summary; reviewers may revise. Consensus for a cell: at least 75% within one point
   of the median.
5. **Update.** Change the catalogue to the median where consensus is reached, add the citations raised, set
   `review.status = "expert-reviewed"`, `review.reviewers` to the panel size, and the date. Record cells without
   consensus in `notes` as contested.
6. **Publish** the anonymised responses (CSV) and a short methods note in the release.

## Keeping it current

A monthly workflow (`.github/workflows/review-freshness.yml`) opens an issue when any review is older than 180 days.
Re-review regulatory notes at least yearly and after any change in legislation or guidance.

## Verification of citations

Citations in the catalogue were added by the maintainer and must be checked against the original source (DOI, volume,
pages) before publication. Use the "Evidence or score update" issue template to report errors.
