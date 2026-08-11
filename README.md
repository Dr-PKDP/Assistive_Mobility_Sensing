# Evidence-Quality Analysis — Ground-Plane Hazard Sensing Review

Data and analysis code supporting the evidence-quality scoring exercise in
*"Sensing Technologies for Ground-Plane Hazard Detection in Assistive
Mobility Devices for the Visually Impaired: A Task-Specific Review and
Evidence-Quality Assessment"* (Section 5 and Section 7).

Every number, statistical test, and figure in the paper's evidence-quality
analysis can be reproduced from the data in this repository using the
scripts in `scripts/`.

## What this is

Forty primary studies on ground-plane hazard sensing (ultrasonic, infrared,
LiDAR, and camera-based) were each scored against two rubrics:

- **ASS (Architectural Sophistication Score)**, 1–4: how technically complex
  the detection method is.
- **VRS (Validation Rigor Score)**, 0–4: how rigorously the study validated
  its results, one point each for sample-size reporting, adverse-condition
  testing, real-user validation, and stratified accuracy reporting.

The central finding is that these two scores are statistically uncorrelated
across the corpus (Spearman's ρ ≈ 0.065, p ≈ 0.69) — architectural
sophistication has risen significantly over the review period, but
validation rigor has not kept pace to a statistically meaningful degree.
The full rubric definitions are in Table 7 of the paper.

## Repository structure

```
data/
  scored_studies.json        The 40-study corpus: ASS, VRS (with all four
                              sub-criteria), modality, publication year, and
                              citation metadata for each study.
  accuracy_subset.json       The 12 studies (of 40) reporting a single-task
                              accuracy figure clean enough for direct
                              comparison, with the exact source figure(s)
                              each percentage was derived from.
  intra_rater_recheck.json   The 12-study blind re-scoring exercise
                              (Section 7): independently re-derived ASS/VRS
                              with reasoning recorded before comparison to
                              the original scores.

scripts/
  01_corpus_analysis.py        Main corpus-wide correlation, ASS>=3 vs
                                ASS<=2 breakdown, boundary cases, VRS
                                sub-criterion breakdown, modality comparison.
  02_temporal_trend.py         Year-vs-ASS/VRS analysis, bootstrap CI,
                                median-split test, regenerates Fig. 3.
  03_accuracy_vs_rigor.py      Tests whether headline accuracy correlates
                                with validation rigor (it doesn't, and if
                                anything trends negative).
  04_intra_rater_reliability.py  Reproduces the Section 7 reliability check
                                  (agreement %, weighted Cohen's kappa).
  05_generate_fig2.py           Regenerates Fig. 2 (ASS/VRS bubble chart).

figures/
  Output directory for regenerated figures (created on first run).
```

## Running the analysis

```bash
pip install -r requirements.txt
cd scripts
python 01_corpus_analysis.py
python 02_temporal_trend.py
python 03_accuracy_vs_rigor.py
python 04_intra_rater_reliability.py
python 05_generate_fig2.py
```

Each script prints its results alongside the corresponding value as stated
in the paper, so any discrepancy is immediately visible. There is exactly
one intentional, documented discrepancy — see the note printed by
`04_intra_rater_reliability.py` and "Corrections found during this
project" below.

## Corrections found during this project

Two errors were found and fixed while preparing this analysis, both
documented in the paper's Section 7 for transparency:

1. **A scoring error caught by the intra-rater check.** One study
   (`Chaudhary&Verma[57]`) had been scored ASS = 2 against an earlier,
   incorrect description of its method as a lightweight single-stage
   classifier. The study actually uses an EfficientNet backbone with
   spatial-channel attention — ASS = 4. `scored_studies.json` reflects the
   corrected score; the correction moves the corpus-wide correlation
   further from significance, not toward it.

2. **A stale citation-number lookup, found while preparing this
   repository.** One study's reference number had shifted during a later
   reference-list edit without the corresponding year lookup being
   updated, causing its publication year to be read from an unrelated
   reference (a laser safety standard) that happened to share a nearby
   citation number. The affected study's year was corrected from 2014 to
   2024; every year-dependent number in `02_temporal_trend.py`'s output
   reflects the corrected value.

Both corrections are applied in the data files as shipped; running the
scripts reproduces the paper's final, corrected numbers, not the
intermediate incorrect ones.

## Methodological notes and limitations

- The intra-rater check (`04_intra_rater_reliability.py`) is **intra**-rater
  consistency under imperfect blinding, not genuine **inter**-rater
  reliability — a true independent second scorer was not available. It
  should be read as a lower bound on how reproducible the rubric is.
- The accuracy-vs-rigor analysis (`03_accuracy_vs_rigor.py`) uses only 12
  of 40 studies, since 70% of the corpus does not report a single-task
  accuracy figure clean enough to compare directly. The negative
  correlation found is directionally consistent with the paper's
  Achirei/Berthe contrast but does not reach statistical significance at
  this reduced sample size.
- Modality was assigned by locating each study's citation number within
  the corresponding subsection of the paper (Section 4.2–4.5). Two studies
  cited as a combined pair (`[23, 24]`) required a manual override rather
  than automatic detection, since automatic substring matching only finds
  standalone bracket citations — see `data/scored_studies.json` generation
  logic in the scripts for details.

## Citation

If you use this dataset or code, please cite the paper this repository
accompanies (full citation to be added on publication).
