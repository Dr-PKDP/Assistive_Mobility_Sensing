"""
04_intra_rater_reliability.py

Reproduces the intra-rater consistency check reported in Section 7
(Limitations). A subsample of 12 studies, each selected because its
specific score is never stated anywhere in the paper's prose (only
discussed via compact table rows or a brief one-sentence mention), was
re-scored from the same source text without consulting the original
scores. See data/intra_rater_recheck.json for the reasoning recorded at
the time of each independent re-score, captured before comparison.

This is intra-rater consistency under imperfect blinding, not genuine
inter-rater reliability — see the paper's Section 7 for the caveat. It
should be read as a lower bound on rubric reproducibility.

Run:
    python 04_intra_rater_reliability.py
Requires: scikit-learn (for weighted Cohen's kappa)
"""
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import cohen_kappa_score

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    original = json.load(open(DATA_DIR / "scored_studies.json"))
    rescored = json.load(open(DATA_DIR / "intra_rater_recheck.json"))

    orig_ass, new_ass, orig_vrs, new_vrs = [], [], [], []
    ass_match, vrs_match, vrs_within1 = 0, 0, 0

    print(f"{'Study':<22} {'Orig ASS':>9} {'New':>5} | {'Orig VRS':>9} {'New':>5}")
    for key, v in rescored.items():
        o = original[key]
        nvrs = v["v1"] + v["v2"] + v["v3"] + v["v4"]
        orig_ass.append(o["ass"]); new_ass.append(v["ass"])
        orig_vrs.append(o["vrs_total"]); new_vrs.append(nvrs)
        if o["ass"] == v["ass"]:
            ass_match += 1
        if o["vrs_total"] == nvrs:
            vrs_match += 1
        if abs(o["vrs_total"] - nvrs) <= 1:
            vrs_within1 += 1
        print(f"{key:<22} {o['ass']:>9} {v['ass']:>5} | {o['vrs_total']:>9} {nvrs:>5}")

    n = len(rescored)
    print(f"\nASS exact agreement: {ass_match}/{n} = {ass_match/n*100:.0f}%")
    print(f"VRS exact agreement: {vrs_match}/{n} = {vrs_match/n*100:.0f}%")
    print(f"VRS within +/-1: {vrs_within1}/{n} = {vrs_within1/n*100:.0f}%")

    kappa_ass = cohen_kappa_score(orig_ass, new_ass, weights="linear")
    kappa_vrs = cohen_kappa_score(orig_vrs, new_vrs, weights="linear")
    print(f"\nWeighted Cohen's kappa (ASS): {kappa_ass:.2f}")
    print(f"Weighted Cohen's kappa (VRS): {kappa_vrs:.2f}")

    print("\nNOTE ON REPRODUCING THE PAPER'S EXACT NUMBERS (75% / kappa=0.57):")
    print("scored_studies.json has already been corrected for the one real error")
    print("this exercise found (Chaudhary&Verma[57], originally scored ASS=2,")
    print("corrected to ASS=4 — see 01_corpus_analysis.py). Against the current,")
    print("corrected data that case now shows as agreement (4 vs 4) rather than")
    print("the original disagreement (2 vs 4), so this script reports 10/12 (83%)")
    print("rather than the paper's stated 9/12 (75%). The paper's figure describes")
    print("the exercise as it originally ran, before the correction it produced")
    print("was applied; this script describes the same exercise's outcome against")
    print("the now-corrected corpus. Both are accurate — they answer 'how well did")
    print("re-scoring agree with the original data' at two different points in the")
    print("correction process, and the gap between them (75% -> 83%) is itself the")
    print("headline result: one real error, found and fixed, not rater noise.")


if __name__ == "__main__":
    main()
