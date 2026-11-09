"""Summarises round 4 results into results/round4/summary.md and summary.json. Works on partial results."""
import json
import os
import numpy as np
import pandas as pd

R = "results/round4"
out, md = {}, []


def rate(s):
    return float(s.mean()) if len(s) else float("nan")


def mcse(p, n):
    return float(np.sqrt(p * (1 - p) / n)) if n else float("nan")


def table(df, title):
    md.append(f"\n### {title}\n")
    md.append(df.to_markdown())


# ---------- Test M ----------
if os.path.exists(f"{R}/round4_M_metamorphic.csv"):
    m = pd.read_csv(f"{R}/round4_M_metamorphic.csv")
    dev = pd.DataFrame({
        "Y*10": (m.cfm_y_times_10 - 10 * m.cfm_base).abs() / m.true_ate.abs(),
        "Y+100": (m.cfm_y_plus_100 - m.cfm_base).abs() / m.true_ate.abs(),
        **{f"Y+{d}T": (m[f"cfm_plus_{d}T"] - m.cfm_base - d).abs() / m.true_ate.abs() for d in (1, 8, 64)},
    })
    out["M_max_rel_dev"] = dev.max().to_dict()
    table(dev.max().to_frame("max deviation / true ATE"), f"Test M: constant transformations ({len(m)} datasets)")
    rows = {}
    for k in (0.5, 1, 2, 4):
        adj = 1 - (m[f"cfm_plant_{k}"] - m.cfm_base) / m[f"naive_shift_{k}"]
        rows[k] = adj.groupby(m.dgp).mean()
    adjM = pd.DataFrame(rows)
    out["M_adjust_fraction"] = adjM.to_dict()
    table(adjM.round(3), "Test M: CausalPFN adjustment fraction on a planted effect (1 = full adjustment, 0 = none), by plant size k")

# ---------- Test C ----------
if os.path.exists(f"{R}/round4_C_anchor.csv"):
    c = pd.read_csv(f"{R}/round4_C_anchor.csv")
    c["rel_bias"] = (c.cfm_ate - c.true_ate) / c.true_ate.abs()
    c["naive_rel_bias"] = (c.naive - c.true_ate) / c.true_ate.abs()
    c["aipw_rel_bias"] = (c.aipw_ate - c.true_ate) / c.true_ate.abs()
    c["anchor"] = (c.cfm_ate - c.naive) / (c.true_ate - c.naive)
    c["plant_adjust"] = 1 - (c.cfm_plant - c.cfm_ate) / c.naive_shift
    out["C_n_datasets"] = len(c)
    out["C_seeds"] = int(c.groupby(["dgp", "effect_size", "n"]).size().min())
    g = c.groupby(["dgp", "effect_size"])
    bias = pd.DataFrame({"CausalPFN": g.rel_bias.mean(), "naive": g.naive_rel_bias.mean(), "AIPW": g.aipw_rel_bias.mean()})
    out["C_bias"] = {f"{d}|{e:g}": v for (d, e), v in bias.round(4).to_dict("index").items()}
    table((100 * bias).round(1), f"Test C: mean signed relative bias, % ({len(c)} datasets, {out['C_seeds']}+ seeds per cell, both n pooled)")
    shr = pd.DataFrame({"shrunk >10%": g.truly_shrunk.mean(), "inflated >10%": g.truly_inflated.mean()})
    out["C_label_rates"] = {f"{d}|{e:g}": v for (d, e), v in shr.round(4).to_dict("index").items()}
    table((100 * shr).round(1), "Test C: share of runs where CausalPFN is >10% off, by direction, %")
    informative = c[c.naive_rel_bias.abs() > 0.10]
    anc = informative.groupby(["dgp", "effect_size"]).anchor.median()
    out["C_anchor_median"] = {f"{d}|{e:g}": v for (d, e), v in anc.round(4).items()}
    table(anc.round(3).unstack(), "Test C: median anchor fraction where the naive contrast is >10% wrong (1 = adjusts fully, 0 = returns naive)")
    out["C_plant_adjust_median"] = c.groupby("dgp").plant_adjust.median().round(4).to_dict()
    table(c.groupby(["dgp", "n"]).plant_adjust.median().round(3).unstack(), "Test C: median planted-effect adjustment fraction")
    out["C_corr_plant_vs_anchor"] = float(informative[["plant_adjust", "anchor"]].corr(method="spearman").iloc[0, 1]) if len(informative) > 5 else None
    # Detectors on the real model
    det = {}
    for name, col, flag in [("round 3 z-test", "decision_old", "flag"), ("margin test", "decision_margin", "shrunk"),
                            ("rectifier test", "decision_rect", "shrunk")]:
        lab = c.truly_shrunk_cf if name == "rectifier test" else c.truly_shrunk
        dec = c[c[col] != "uncertain"]
        lab = lab[dec.index]
        det[name] = dict(flag_rate=rate(dec[col] == flag), hits=rate((dec[col] == flag)[lab]), n_shrunk=int(lab.sum()),
                         false_alarms=rate((dec[col] == flag)[~lab]), n_not_shrunk=int((~lab).sum()),
                         uncertain=rate(c[col] == "uncertain"))
    infl = c.truly_inflated
    det["round 3 z-test"]["caught_inflated"] = rate(c.z_old[infl] < -1.645)
    det["rectifier test"]["caught_inflated"] = rate(c.z_rect_nomargin[c.truly_inflated_cf] < -1.645)
    out["C_detectors"] = det
    table(pd.DataFrame(det).T.round(3), "Test C: detectors on real CausalPFN")
    out["C_crossfit_vs_full_rel"] = float(((c.cfm_ate_cf - c.cfm_ate) / c.true_ate.abs()).abs().median())
    out["C_s_vs_ra_rel"] = float(((c.cfm_ate_ra - c.cfm_ate) / c.true_ate.abs()).abs().median())
    out["C_aipw_cover"] = rate((c.aipw_ate - 1.96 * c.aipw_se <= c.true_ate) & (c.true_ate <= c.aipw_ate + 1.96 * c.aipw_se))

# ---------- Test D ----------
if os.path.exists(f"{R}/round4_D_controls.csv"):
    d = pd.read_csv(f"{R}/round4_D_controls.csv")
    d = d[d.effect_size > 0]
    res = []
    for (cfm, s, n), g in d.groupby(["cfm", "shrink", "n"]):
        row = dict(cfm=cfm, shrink=s, n=n, runs=len(g),
                   old=rate(g.decision_old == "flag"), margin=rate(g.decision_margin == "shrunk"))
        if g.decision_rect.notna().any():
            row["rectifier"] = rate(g.decision_rect == "shrunk")
        if "decision_split" in g and g.decision_split.notna().any():
            row["split"] = rate(g.decision_split == "shrunk")
        res.append(row)
    res = pd.DataFrame(res).set_index(["cfm", "shrink", "n"])
    out["D_flag_rates"] = {f"{a}|{b:g}|{c_}": v for (a, b, c_), v in res.round(4).to_dict("index").items()}
    table(res.round(3), "Test D: share of runs flagged as shrunk, by stand-in CFM and planted shrinkage")
    # Size at the boundary: 10% shrinkage is the largest that should not be flagged
    b = res.xs(0.10, level="shrink")
    out["D_size_at_10pct"] = b.round(4).to_dict("index")
if os.path.exists(f"{R}/round4_F_reference_failure.csv"):
    f = pd.read_csv(f"{R}/round4_F_reference_failure.csv")
    fr = f[f.shrink == 0.0].groupby(["spec", "overlap", "n"]).agg(
        aipw_bias=("aipw_ate", lambda x: float(((x - f.loc[x.index, "true_ate"]) / f.loc[x.index, "true_ate"]).mean())),
        old_false_flag=("decision_old", lambda x: rate(x == "flag")),
        margin_false_flag=("decision_margin", lambda x: rate(x == "shrunk")),
        rect_false_flag=("decision_rect", lambda x: rate(x == "shrunk")),
        uncertain=("decision_old", lambda x: rate(x == "uncertain")))
    out["F"] = {f"{a}|{b}|{c_}": v for (a, b, c_), v in fr.round(4).to_dict("index").items()}
    table(fr.round(3), "Test F: perfect CFM, unreliable reference. Any flag here is a false alarm")
if os.path.exists(f"{R}/round4_P_planted_controls.csv"):
    p = pd.read_csv(f"{R}/round4_P_planted_controls.csv")
    pa = pd.DataFrame({
        "AIPW": (1 - (p.aipw_plant - p.aipw_ate) / p.naive_shift).groupby(p.dgp).median(),
        "T-learner": (1 - (p.tlearner_plant - p.tlearner_ate) / p.naive_shift).groupby(p.dgp).median(),
    })
    pa["naive (by definition)"] = 0.0
    out["P_adjust"] = pa.round(4).to_dict()
    table(pa.round(3), "Test P: planted-effect adjustment fraction for estimators we understand")

open(f"{R}/summary.md", "w").write("# Round 4 results\n" + "\n".join(md) + "\n")
def _keys(o):
    if isinstance(o, dict):
        return {("|".join(map(str, k)) if isinstance(k, tuple) else str(k)): _keys(v) for k, v in o.items()}
    return o
json.dump(_keys(out), open(f"{R}/summary.json", "w"), indent=1, default=float)
print("\n".join(md))
