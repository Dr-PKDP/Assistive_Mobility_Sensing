"""
02_temporal_trend.py

Reproduces the year-based analysis in Section 5 (sophistication and
validation rigor over time) and regenerates Fig. 3.

Run:
    python 02_temporal_trend.py
Output:
    figures/fig3_temporal_trend.png
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

DATA = Path(__file__).parent.parent / "data" / "scored_studies.json"
FIGDIR = Path(__file__).parent.parent / "figures"


def main():
    studies = json.load(open(DATA))
    years = np.array([v["publication_year"] for v in studies.values()])
    ass = np.array([v["ass"] for v in studies.values()], dtype=float)
    vrs = np.array([v["vrs_total"] for v in studies.values()], dtype=float)

    rho_ass, p_ass = stats.spearmanr(years, ass)
    rho_vrs, p_vrs = stats.spearmanr(years, vrs)
    print(f"Year vs ASS: rho={rho_ass:.3f}, p={p_ass:.3f}  (paper: 0.39, 0.013)")
    print(f"Year vs VRS: rho={rho_vrs:.3f}, p={p_vrs:.3f}  (paper: 0.15, 0.36)")

    # bootstrap CI for the corpus-wide ASS-VRS correlation (not year-dependent,
    # included here for completeness since it is reported in the same paragraph)
    rng = np.random.default_rng(42)
    boot = []
    n = len(ass)
    for _ in range(10000):
        idx = rng.integers(0, n, n)
        r, _ = stats.spearmanr(ass[idx], vrs[idx])
        if not np.isnan(r):
            boot.append(r)
    ci = np.percentile(boot, [2.5, 97.5])
    print(f"Bootstrap 95% CI for ASS-VRS rho: [{ci[0]:.2f}, {ci[1]:.2f}]  (paper: [-0.23, 0.36])")

    median_year = np.median(years)
    early = years <= median_year
    recent = years > median_year
    print(f"\nMedian year: {median_year:.0f}")
    print(f"Early (n={early.sum()}) mean VRS: {vrs[early].mean():.2f}")
    print(f"Recent (n={recent.sum()}) mean VRS: {vrs[recent].mean():.2f}")
    u, up = stats.mannwhitneyu(vrs[early], vrs[recent])
    print(f"Mann-Whitney p: {up:.2f}  (paper: 0.64)")

    # --- Figure 3 ---
    rng2 = np.random.default_rng(1)
    years_jit = years + rng2.uniform(-0.15, 0.15, len(years))
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))

    ax[0].scatter(years_jit, ass, alpha=0.6, s=50, color="#2166ac", edgecolors="white", linewidth=0.5)
    z1 = np.polyfit(years, ass, 1)
    xline = np.linspace(years.min(), years.max(), 100)
    ax[0].plot(xline, np.polyval(z1, xline), color="#2166ac", linestyle="--", linewidth=1.5)
    ax[0].set_xlabel("Publication year")
    ax[0].set_ylabel("Architectural Sophistication Score (ASS)")
    ax[0].set_title(f"(a) Sophistication over time\nSpearman ρ = {rho_ass:.2f}, p = {p_ass:.3f}", fontsize=10)
    ax[0].set_yticks([1, 2, 3, 4])
    ax[0].grid(alpha=0.25)

    ax[1].scatter(years_jit, vrs, alpha=0.6, s=50, color="#b2182b", edgecolors="white", linewidth=0.5)
    z2 = np.polyfit(years, vrs, 1)
    ax[1].plot(xline, np.polyval(z2, xline), color="#b2182b", linestyle="--", linewidth=1.5)
    ax[1].set_xlabel("Publication year")
    ax[1].set_ylabel("Validation Rigor Score (VRS)")
    ax[1].set_title(f"(b) Validation rigor over time\nSpearman ρ = {rho_vrs:.2f}, p = {p_vrs:.2f} (n.s.)", fontsize=10)
    ax[1].set_yticks([0, 1, 2, 3, 4])
    ax[1].grid(alpha=0.25)

    plt.tight_layout()
    FIGDIR.mkdir(exist_ok=True)
    plt.savefig(FIGDIR / "fig3_temporal_trend.png", dpi=200, bbox_inches="tight")
    print(f"\nFigure saved to {FIGDIR / 'fig3_temporal_trend.png'}")

    # --- Per-modality timing ---
    print("\n=== Per-modality publication-year summary ===")
    by_mod = {}
    for v in studies.values():
        by_mod.setdefault(v["modality"], []).append(v["publication_year"])
    for mod, yrs in by_mod.items():
        print(f"  {mod}: n={len(yrs)}, median={np.median(yrs):.0f}, "
              f"earliest={min(yrs)}, latest={max(yrs)}")


if __name__ == "__main__":
    main()
