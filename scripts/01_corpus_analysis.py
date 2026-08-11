"""
01_corpus_analysis.py

Reproduces every corpus-wide numeric claim in Section 5 ("Evidence-Quality
Analysis") of the paper, using data/scored_studies.json as the sole input,
and the Bonferroni multiple-comparisons correction disclosed in Section 7.

Run:
    python 01_corpus_analysis.py

Requires: scipy, numpy (see requirements.txt)
"""
import json
from pathlib import Path

import numpy as np
from scipy import stats

DATA = Path(__file__).parent.parent / "data" / "scored_studies.json"


def load():
    return json.load(open(DATA))


def main():
    studies = load()
    ass = np.array([v["ass"] for v in studies.values()])
    vrs = np.array([v["vrs_total"] for v in studies.values()])
    n = len(studies)

    print(f"n = {n} studies\n")

    # --- Main corpus-wide correlation (Section 5, paragraph 1) ---
    rho, p = stats.spearmanr(ass, vrs)
    print("=== Corpus-wide ASS vs VRS correlation ===")
    print(f"Spearman rho = {rho:.4f}, p = {p:.4f}")
    print("(Paper reports: rho = 0.065, p = 0.69)\n")

    # --- ASS>=3 vs ASS<=2 breakdown ---
    ge3 = ass >= 3
    le2 = ass <= 2
    le1 = vrs <= 1
    pct_ge3 = np.mean(le1[ge3]) * 100
    pct_le2 = np.mean(le1[le2]) * 100
    print("=== High- vs low-sophistication VRS<=1 rate ===")
    print(f"ASS>=3 with VRS<=1: {pct_ge3:.1f}% (n={ge3.sum()})")
    print(f"ASS<=2 with VRS<=1: {pct_le2:.1f}% (n={le2.sum()})")
    print("(Paper reports: 80.0% vs 83.3%)\n")

    # --- Mean VRS / zero-VRS rate ---
    print("=== Overall VRS distribution ===")
    print(f"Mean VRS = {vrs.mean():.3f}  (paper reports 0.58)")
    print(f"VRS = 0 count: {np.sum(vrs==0)}/{n}  (paper reports 27/40)\n")

    # --- ASS=4 studies (boundary case) ---
    print("=== ASS = 4 studies (boundary case) ===")
    for k, v in studies.items():
        if v["ass"] == 4:
            print(f"  {k}: year={v['publication_year']}, VRS={v['vrs_total']}")
    print()

    # --- VRS = 4 studies (boundary case) ---
    print("=== VRS = 4 studies (boundary case) ===")
    for k, v in studies.items():
        if v["vrs_total"] == 4:
            print(f"  {k}: ASS={v['ass']}")
    print()

    # --- VRS sub-criterion breakdown ---
    print("=== VRS sub-criterion breakdown ===")
    for crit, label in [
        ("v1_sample_size_reported", "V1 sample/dataset scale"),
        ("v2_test_conditions_specified", "V2 test conditions specified"),
        ("v3_real_user_validation", "V3 real-user validation"),
        ("v4_stratified_accuracy", "V4 stratified accuracy"),
    ]:
        count = sum(v[crit] for v in studies.values())
        print(f"  {label}: {count}/{n} = {count/n*100:.1f}%")
    print("(Paper reports: V1=10.0%, V2=20.0%, V3=10.0%, V4=17.5%)\n")

    # --- Modality-level VRS comparison ---
    print("=== Modality-level VRS comparison ===")
    by_modality = {}
    for v in studies.values():
        by_modality.setdefault(v["modality"], []).append(v["vrs_total"])
    for mod, vals in by_modality.items():
        print(f"  {mod}: n={len(vals)}, mean VRS={np.mean(vals):.2f}, median={np.median(vals):.1f}")
    h_stat, kw_p = stats.kruskal(*by_modality.values())
    print(f"  Kruskal-Wallis: H={h_stat:.3f}, p={kw_p:.3f}")
    print("(Paper reports: Infrared 1.50/n=4, Vision 1.00/n=9, Ultrasonic 0.31/n=16,")
    print(" LiDAR 0.27/n=11, H=5.28, p=0.15)\n")

    # --- Multiple-comparisons correction (Section 7) ---
    # All six tests reported across this script and 02_temporal_trend.py / 03_accuracy_vs_rigor.py,
    # collected here for the Bonferroni correction disclosed in the paper's Limitations section.
    print("=== Bonferroni correction across all six tests reported in Section 5 ===")
    six_tests = {
        "Corpus-wide ASS-VRS correlation": p,
        "Year vs ASS": 0.013,
        "Year vs VRS": 0.355,
        "Median-split Mann-Whitney": 0.644,
        "Modality Kruskal-Wallis": kw_p,
        "Accuracy vs VRS (n=12)": 0.269,
    }
    n_tests = len(six_tests)
    alpha_adj = 0.05 / n_tests
    print(f"n = {n_tests} tests, Bonferroni-adjusted alpha = 0.05/{n_tests} = {alpha_adj:.4f}")
    for name, raw_p in six_tests.items():
        corrected = min(raw_p * n_tests, 1.0)
        sig = "significant" if corrected < 0.05 else "not significant"
        print(f"  {name}: raw p={raw_p:.3f}, corrected p={corrected:.3f} ({sig})")
    print("(Paper reports: none survive correction; year-ASS corrects from p=0.013 to p=0.078)\n")


if __name__ == "__main__":
    main()
