"""
05_generate_fig2.py

Regenerates Fig. 2 (ASS vs VRS bubble chart, Section 5) from
data/scored_studies.json.

Run:
    python 05_generate_fig2.py
Output:
    figures/fig2_ass_vrs_bubble.png
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

DATA = Path(__file__).parent.parent / "data" / "scored_studies.json"
FIGDIR = Path(__file__).parent.parent / "figures"


def main():
    studies = json.load(open(DATA))
    ass = [v["ass"] for v in studies.values()]
    vrs = [v["vrs_total"] for v in studies.values()]

    rho, p = stats.spearmanr(ass, vrs)

    counts = {}
    for a, r in zip(ass, vrs):
        counts[(a, r)] = counts.get((a, r), 0) + 1

    fig, ax = plt.subplots(figsize=(7, 5.5))
    for (a, r), count in counts.items():
        ax.scatter(a, r, s=count * 220, alpha=0.6, color="#2166ac", edgecolors="#0b3d6e", linewidth=1)
        ax.annotate(str(count), (a, r), ha="center", va="center", fontsize=9,
                    fontweight="bold", color="white")

    ax.set_xlabel("Architectural Sophistication Score (ASS)")
    ax.set_ylabel("Validation Rigor Score (VRS)")
    ax.set_xticks([1, 2, 3, 4])
    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_xlim(0.5, 4.5)
    ax.set_ylim(-0.5, 4.5)
    ax.grid(alpha=0.25)
    ax.set_title(f"Spearman ρ = {rho:.3f}, p = {p:.2f} (n={len(ass)})", fontsize=11)
    plt.tight_layout()

    FIGDIR.mkdir(exist_ok=True)
    plt.savefig(FIGDIR / "fig2_ass_vrs_bubble.png", dpi=200, bbox_inches="tight")
    print(f"Figure saved to {FIGDIR / 'fig2_ass_vrs_bubble.png'}")
    print(f"rho={rho:.4f}, p={p:.4f}  (paper: rho=0.065, p=0.69)")


if __name__ == "__main__":
    main()
