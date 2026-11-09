"""Test D: do the detectors work when the answer is known? CPU only, no CausalPFN.

Stand-in CFMs with a known amount of shrinkage are judged by each detector:
  perfect:  the true outcome functions, shrunk by s. Its errors do not depend on the sample noise.
  tlearner: AIPW's own outcome models, shrunk by s. Its errors are correlated with AIPW's, like a real CFM's.
  aipw:     AIPW's own number, shrunk by s. The most correlated case.
  naive:    the difference in means. Fails by not adjusting, in either direction.
  ridge:    a heavily regularised S-learner. Shrinks for a real reason, not a planted one.

Reference-failure settings make AIPW itself unreliable while the CFM is perfect.
Test P measures the planted-effect self-test on estimators whose adjustment is understood.
"""
import itertools
import os
import sys
import time
import numpy as np
import pandas as pd
from joblib import Parallel, delayed, parallel_config
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from round4_core import (KFold, NUISANCE_SPECS, aipw, crossfit_propensity, detector, margin_detector, naive_contrast,
                         planted_effect, rectifier_detector, simulate, truly_inflated, truly_shrunk, done_keys)

OUT = "results/round4"
D_CSV = f"{OUT}/round4_D_controls.csv"
F_CSV = f"{OUT}/round4_F_reference_failure.csv"
P_CSV = f"{OUT}/round4_P_planted_controls.csv"

SHRINKS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.50]

# Test D: 500 seeds at the null where it is cheap, 200 where it is not
D_DGPS    = ["notebook", "tau_on_confounder"]
D_EFFECTS = [0.0, 1.0, 8.0, 128.0]
D_SEEDS   = {500: range(0, 500), 2000: range(0, 200)}

# Reference failure: AIPW is misspecified or overlap is poor, the CFM is perfect
F_EFFECTS = [1.0, 8.0]
F_NS      = [500, 2000]
F_SEEDS   = range(0, 200)
F_SETTINGS = [("both_ok", "good"), ("outcome_wrong", "good"), ("prop_wrong", "good"), ("both_wrong", "good"), ("both_ok", "poor")]

# Test P: planted-effect self-test
P_DGPS   = ["notebook", "tau_on_confounder", "flipped", "scaled"]
P_EFFECT = 4.0
P_NS     = [500, 2000]
P_SEEDS  = range(0, 100)
P_K      = 1.0


def _ridge_crossfit(X, T, Y, seed, folds=5):
    n = len(Y)
    mu0, mu1 = np.zeros(n), np.zeros(n)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        sc = StandardScaler().fit(X[tr])
        Ztr, Zte = sc.transform(X[tr]), sc.transform(X[te])
        m = Ridge(alpha=0.1 * len(tr)).fit(np.column_stack([T[tr], Ztr]), Y[tr])
        mu0[te] = m.predict(np.column_stack([np.zeros(len(te)), Zte]))
        mu1[te] = m.predict(np.column_stack([np.ones(len(te)), Zte]))
    return mu0, mu1


def _naive_crossfit(T, Y, seed, folds=5):
    n = len(Y)
    mu0, mu1 = np.zeros(n), np.zeros(n)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(Y.reshape(-1, 1)):
        mu0[te] = Y[tr][T[tr] == 0].mean()
        mu1[te] = Y[tr][T[tr] == 1].mean()
    return mu0, mu1


def _judge(base, name, s, c, a, se, eh, T, Y, ta, mu0=None, mu1=None):
    d0, z0 = detector(c, a, se, eh)
    dm, zm = margin_detector(c, a, se, eh)
    row = dict(base, cfm=name, shrink=s, cfm_ate=c, decision_old=d0, z_old=z0, decision_margin=dm, z_margin=zm,
               truly_shrunk=truly_shrunk(c, ta), truly_inflated=truly_inflated(c, ta))
    if mu0 is not None:
        dr, zr, zr0 = rectifier_detector(mu0, mu1, T, Y, eh)
        c_cf = float((mu1 - mu0).mean())
        row.update(decision_rect=dr, z_rect=zr, z_rect_nomargin=zr0, cfm_ate_cf=c_cf,
                   truly_shrunk_cf=truly_shrunk(c_cf, ta), truly_inflated_cf=truly_inflated(c_cf, ta))
    return row


def _split_reference(X, T, Y, tau, seed):
    """Sample splitting: the CFM sees one half and AIPW the other, so their errors are independent."""
    idx = np.random.default_rng(seed + 10_000).permutation(len(Y))
    half = len(Y) // 2
    A, B = idx[:half], idx[half:]
    a_b, se_b, eh_b, *_ = aipw(X[B], T[B], Y[B], "both_ok", seed)
    return float(tau[A].mean()), a_b, se_b, eh_b


def _seed_job_d(seed, n):
    """Everything for one seed and size. Treatment does not depend on the effect size, so the propensities are shared."""
    rows, eh = [], None
    for dgp, es in itertools.product(D_DGPS, D_EFFECTS):
        if es == 0.0 and dgp != "notebook":      # with no effect, these designs are the same data
            continue
        X, T, Y, e, ta, mu0, mu1 = simulate(n, es, "good", seed, dgp=dgp)
        tau = mu1 - mu0
        if eh is None:
            eh = crossfit_propensity(X, T, seed)
        a, se, _, m0h, m1h = aipw(X, T, Y, "both_ok", seed, e_hat=eh)
        base = dict(dgp=dgp, effect_size=es, n=n, seed=seed, true_ate=ta, aipw_ate=a, aipw_se=se, naive=naive_contrast(T, Y))
        tau_a, a_b, se_b, eh_b = _split_reference(X, T, Y, tau, seed)
        for s in ([0.0] if es == 0.0 else SHRINKS):
            row = _judge(base, "perfect", s, (1 - s) * ta, a, se, eh, T, Y, ta, mu0, mu0 + (1 - s) * tau)
            d3, z3 = margin_detector((1 - s) * tau_a, a_b, se_b, eh_b)
            row.update(decision_split=d3, z_split=z3)
            rows.append(row)
            cate = m1h - m0h
            rows.append(_judge(base, "tlearner", s, (1 - s) * float(cate.mean()), a, se, eh, T, Y, ta, m0h, m0h + (1 - s) * cate))
            rows.append(_judge(base, "aipw", s, (1 - s) * a, a, se, eh, T, Y, ta))
        m0n, m1n = _naive_crossfit(T, Y, seed)
        rows.append(_judge(base, "naive", 0.0, naive_contrast(T, Y), a, se, eh, T, Y, ta, m0n, m1n))
        m0r, m1r = _ridge_crossfit(X, T, Y, seed)
        rows.append(_judge(base, "ridge", 0.0, float((m1r - m0r).mean()), a, se, eh, T, Y, ta, m0r, m1r))
    return rows


def _seed_job_f(seed, n):
    rows = []
    for (spec, overlap), es in itertools.product(F_SETTINGS, F_EFFECTS):
        X, T, Y, e, ta, mu0, mu1 = simulate(n, es, overlap, seed)
        a, se, eh, *_ = aipw(X, T, Y, spec, seed)
        base = dict(spec=spec, overlap=overlap, effect_size=es, n=n, seed=seed, true_ate=ta, aipw_ate=a, aipw_se=se,
                    extreme_share=float(np.mean((eh < 0.02) | (eh > 0.98))))
        for s in (0.0, 0.20):
            rows.append(_judge(base, "perfect", s, (1 - s) * ta, a, se, eh, T, Y, ta, mu0, mu0 + (1 - s) * (mu1 - mu0)))
    return rows


def _seed_job_p(seed, n):
    rows = []
    for dgp in P_DGPS:
        X, T, Y, e, ta, *_ = simulate(n, P_EFFECT, "good", seed, dgp=dgp)
        eh = crossfit_propensity(X, T, seed)
        delta = planted_effect(X, Y, P_K)
        Y2 = Y + T * delta
        a, _, _, m0, m1 = aipw(X, T, Y, "both_ok", seed, e_hat=eh)
        a2, _, _, m02, m12 = aipw(X, T, Y2, "both_ok", seed, e_hat=eh)
        ns = float(delta[T == 1].mean())
        rows.append(dict(dgp=dgp, n=n, seed=seed, true_ate=ta, naive=naive_contrast(T, Y), naive_shift=ns,
                         aipw_ate=a, aipw_plant=a2, tlearner_ate=float((m1 - m0).mean()), tlearner_plant=float((m12 - m02).mean())))
    return rows


def _run(job, pairs, path, block=64):
    done = done_keys(path, ["seed", "n"]) if os.path.exists(path) else set()
    pairs = [p for p in pairs if p not in done]
    t0 = time.time()
    with parallel_config(backend="loky", inner_max_num_threads=1):
        for i in range(0, len(pairs), block):
            part = Parallel(n_jobs=8)(delayed(job)(s, n) for s, n in pairs[i:i + block])
            rows = [r for group in part for r in group]
            pd.DataFrame(rows).to_csv(path, mode="a", header=not os.path.exists(path), index=False)
            print(f"{os.path.basename(path)}: {min(i + block, len(pairs))}/{len(pairs)} seeds, {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # Seeds run in order so a stopped run is still balanced, and both sizes advance together
    d_pairs = sorted(((s, n) for n, seeds in D_SEEDS.items() for s in seeds), key=lambda p: (p[0], p[1]))
    _run(_seed_job_p, list(itertools.product(P_SEEDS, P_NS)), P_CSV)
    _run(_seed_job_f, list(itertools.product(F_SEEDS, F_NS)), F_CSV)
    _run(_seed_job_d, d_pairs, D_CSV)
    print("all controls done", flush=True)
