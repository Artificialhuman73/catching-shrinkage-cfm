"""Figures for the explanatory PDF, computed from results/round4 CSVs."""
import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = sys.argv[1] + "/results/round4"
OUT = sys.argv[2]
INK, INK2, GRID, SURF = "#1f2328", "#5a6773", "#e6e6e3", "#ffffff"
COL = {"notebook": "#2a78d6", "tau_on_confounder": "#eb6834", "flipped": "#1baf7a", "scaled": "#eda100"}
MK = {"notebook": "o", "tau_on_confounder": "s", "flipped": "^", "scaled": "D"}
NAME = {"notebook": "Original", "tau_on_confounder": "Effect tied to confounder", "flipped": "Flipped", "scaled": "Scaled"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "lines.linewidth": 2})
nums = {}

# ---------- Fig 1: CausalPFN vs naive error by effect size ----------
c = pd.read_csv(f"{R}/round4_C_anchor.csv")
c["rb"] = 100 * (c.cfm_ate - c.true_ate) / c.true_ate.abs()
c["nb"] = 100 * (c.naive - c.true_ate) / c.true_ate.abs()
g = c.groupby(["dgp", "effect_size"])[["rb", "nb"]].mean().reset_index()
effects = sorted(c.effect_size.unique())
fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
for ax, col, title, lim in [(axes[0], "rb", "CausalPFN", 15), (axes[1], "nb", "No adjustment (naive difference)", 95)]:
    ax.axhspan(-10, 10, color="#eef3f8", zorder=0)
    ax.axhline(0, color=INK2, lw=1)
    for d in COL:
        s = g[g.dgp == d]
        ax.plot(range(len(effects)), s[col], color=COL[d], marker=MK[d], ms=6, label=NAME[d])
    ax.set_xticks(range(len(effects)), [f"{e:g}" for e in effects])
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("True effect size")
    ax.set_title(title, loc="left", fontsize=11, color=INK, fontweight="bold")
axes[0].set_ylabel("Mean signed error (% of true effect)")
axes[0].text(5.1, 10.5, "±10% band", color=INK2, fontsize=8, ha="right")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, frameon=False, fontsize=9, loc="lower center", ncol=4)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(f"{OUT}/fig1_error.png", dpi=200)
plt.close(fig)
nums["off10_by_effect"] = (c.assign(o=c.rb.abs() > 10).groupby("effect_size").o.mean() * 100).round(1).to_dict()
nums["maxabs_by_effect"] = c.groupby("effect_size").rb.apply(lambda x: x.abs().max()).round(1).to_dict()
nums["truly_shrunk"] = int(c.truly_shrunk.sum())
nums["truly_inflated"] = int(c.truly_inflated.sum())

# ---------- Fig 2: share of runs >10% off ----------
off = nums["off10_by_effect"]
fig, ax = plt.subplots(figsize=(5.2, 3.0))
xs = range(len(effects))
vals = [off[e] for e in effects]
ax.bar(xs, vals, color="#2a78d6", width=0.55)
for x, v in zip(xs, vals):
    ax.text(x, v + 1.2, f"{v:.0f}%" if v else "0", ha="center", color=INK, fontsize=9)
ax.set_xticks(list(xs), [f"{e:g}" for e in effects])
ax.set_xlabel("True effect size")
ax.set_ylabel("Runs >10% off (%)")
ax.set_ylim(0, max(vals) + 8)
ax.grid(axis="x", visible=False)
fig.tight_layout()
fig.savefig(f"{OUT}/fig2_off10.png", dpi=200)
plt.close(fig)

# ---------- Fig 3: planted self-test ----------
p2 = pd.read_csv(f"{R}/round4_P2_plant_fixed.csv")
p = pd.read_csv(f"{R}/round4_P_planted_controls.csv")
adj = {
    "CausalPFN": 100 * p2.cfm_adj,
    "T-learner": 100 * (1 - (p.tlearner_plant - p.tlearner_ate) / p.naive_shift),
    "AIPW": 100 * (1 - (p.aipw_plant - p.aipw_ate) / p.naive_shift),
}
fig, ax = plt.subplots(figsize=(6.2, 2.7))
rows = [("No adjustment", 0, 0, 0, 0)] + [(k, v.median(), v.quantile(.1), v.quantile(.9), len(v)) for k, v in adj.items()]
for i, (k, med, lo, hi, n) in enumerate(rows):
    ax.plot([lo, hi], [i, i], color="#86b6ef", lw=5, solid_capstyle="round")
    ax.plot(med, i, "o", color="#2a78d6", ms=9, mec="white", mew=2)
    ax.text(132, i, f"{med:.0f}%" + (f"  (n={n})" if n else ""), va="center", color=INK, fontsize=9)
ax.axvline(100, color=INK2, lw=1, ls="--")
ax.set_yticks(range(len(rows)), [r[0] for r in rows])
ax.set_xlim(-5, 160)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xlabel("Planted bias removed (%): dot = median, bar = 10th–90th percentile")
ax.invert_yaxis()
ax.grid(axis="y", visible=False)
fig.tight_layout()
fig.savefig(f"{OUT}/fig3_plant.png", dpi=200)
plt.close(fig)
nums["plant"] = {k: [round(v.median() * 1, 1), round(v.quantile(.1), 1), round(v.quantile(.9), 1), len(v)] for k, v in adj.items()}

# ---------- Fig 4: detectors on known shrinkage ----------
d = pd.read_csv(f"{R}/round4_D_controls.csv")
d = d[(d.effect_size > 0) & (d.cfm == "perfect")]
rates = d.groupby("shrink").agg(z=("decision_old", lambda x: 100 * (x == "flag").mean()),
                                margin=("decision_margin", lambda x: 100 * (x == "shrunk").mean()),
                                rect=("decision_rect", lambda x: 100 * (x == "shrunk").mean()))
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.axvspan(-1, 10, color="#eef3f8", zorder=0)
ax.text(0.3, 95, "should NOT be flagged\n(≤10% shrinkage)", color=INK2, fontsize=8, va="top")
ax.axhline(5, color=INK2, lw=1, ls=":")
ax.text(51, 6.5, "5% target", color=INK2, fontsize=8, ha="right")
xs = 100 * rates.index.values
for col, name, cl, mk in [("z", "Round 3 z-test", "#eb6834", "o"), ("margin", "Margin test", "#2a78d6", "s"),
                          ("rect", "Rectifier test", "#1baf7a", "^")]:
    ax.plot(xs, rates[col], color=cl, marker=mk, ms=6, label=name)
ax.set_xlim(-1, 52)
ax.set_ylim(0, 100)
ax.set_xticks([0, 5, 10, 15, 20, 30, 50])
ax.set_xlabel("Planted shrinkage (%)")
ax.set_ylabel("Runs flagged as shrunk (%)")
ax.legend(frameon=False, fontsize=8.5, loc="center right", bbox_to_anchor=(1.0, 0.35))
fig.tight_layout()
fig.savefig(f"{OUT}/fig4_detectors.png", dpi=200)
plt.close(fig)
nums["detectors"] = rates.round(1).reset_index().to_dict("records")
nums["D_runs"] = int(len(d))

v2 = pd.read_csv(f"{R}/round4_C_anchor_v2.csv")
nums["real_flags_v2"] = {"z": round(100 * (v2.decision_old_v2 == "flag").mean(), 1),
                         "margin": round(100 * (v2.decision_margin_v2 == "shrunk").mean(), 1)}
json.dump(nums, open(f"{OUT}/nums.json", "w"), indent=1, default=float)
print(json.dumps(nums, indent=1, default=float))
