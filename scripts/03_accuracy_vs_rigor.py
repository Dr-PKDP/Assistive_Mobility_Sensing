"""
03_accuracy_vs_rigor.py

Tests whether studies reporting higher headline accuracy tend to score
lower on validation rigor, generalizing the Achirei/Berthe anecdotal
contrast in Section 5 to the full subset of studies with a comparable
accuracy figure.

Only studies reporting a single-task accuracy percentage clean enough to
average or use directly are included (see data/accuracy_subset.json for
exactly how each figure was derived from the paper's own tables). Range,
resolution (e.g. "2 cm elevation change"), and purely qualitative claims
("high accuracy", "not quantified") are excluded by design, not omission.

Run:
    python 03_accuracy_vs_rigor.py
"""
import json
from pathlib import Path

from scipy import stats

DATA_DIR = Path(__file__).parent.parent / "data"


def main():
    studies = json.load(open(DATA_DIR / "scored_studies.json"))
    accuracy = json.load(open(DATA_DIR / "accuracy_subset.json"))

    n_total = len(studies)
    n_with_accuracy = len(accuracy)
    print(f"{n_with_accuracy}/{n_total} studies ({n_with_accuracy/n_total*100:.0f}%) "
          f"report a comparable accuracy figure.")

    acc_vals, vrs_vals = [], []
    for key, entry in accuracy.items():
        acc_vals.append(entry["accuracy_pct"])
        vrs_vals.append(studies[key]["vrs_total"])
        print(f"  {key}: {entry['accuracy_pct']:.1f}% (VRS={studies[key]['vrs_total']}) "
              f"— {entry['note']}")

    rho, p = stats.spearmanr(acc_vals, vrs_vals)
    print(f"\nSpearman rho (accuracy vs VRS) = {rho:.2f}, p = {p:.2f}, n = {len(acc_vals)}")
    print("(Paper reports: rho = -0.35, p = 0.27, n = 12)")


if __name__ == "__main__":
    main()
