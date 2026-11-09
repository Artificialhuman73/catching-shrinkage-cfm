import os
import numpy as np
import pandas as pd
from scipy.special import expit
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

D = 6  # number of covariates
DGPS = ["notebook", "tau_on_confounder", "flipped", "scaled"]

# ---------- 1. Data generator (we know the truth) ----------
def simulate(n, effect_size, overlap, seed, noise_sd=1.0, dgp="notebook"):
    """effect_size = true ATE. overlap: 'good' or 'poor'. noise_sd = outcome noise.
    dgp picks the design:
      notebook:          same as rounds 1-3. Confounding stays fixed while the effect grows.
      tau_on_confounder: the effect size depends on X0, which also drives treatment.
      flipped:           confounding runs the other way (the naive contrast is too low).
      scaled:            confounding grows with the effect, so it never becomes negligible.
    The random draws match rounds 1-3 for the same seed.
    """
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, size=(n, D))
    # Nonlinear confounding: the same features drive treatment and outcome
    score = X[:, 0] - 0.5 * X[:, 1] + 0.8 * (X[:, 2] ** 2 - 1) + 0.5 * X[:, 0] * X[:, 3]
    if dgp == "flipped":
        score = -score
    strength = 0.6 if overlap == "good" else 2.0   # bigger = more extreme propensities
    e = expit(strength * score)
    T = rng.binomial(1, e)
    mu0 = 1.0 * X[:, 0] + np.sin(2 * X[:, 1]) + 0.7 * X[:, 2] ** 2 + 0.5 * X[:, 3] * X[:, 4]
    if dgp == "scaled":
        mu0 = mu0 - effect_size * X[:, 0]
    if dgp == "tau_on_confounder":
        tau = effect_size * (1 - 0.5 * X[:, 0])
    else:
        tau = effect_size * (1 + 0.5 * X[:, 4])        # heterogeneous effect, mean = effect_size
    Y = mu0 + T * tau + rng.normal(0, noise_sd, size=n)
    true_ate = float(tau.mean())                       # sample ATE (the "answer key")
    return X, T, Y, e, true_ate, mu0, mu0 + tau

# ---------- 2. AIPW with cross-fitting ----------
def _outcome_model(kind, seed):
    if kind == "flexible":
        return HistGradientBoostingRegressor(max_iter=200, learning_rate=0.05, random_state=seed)
    return LinearRegression()          # 'wrong': linear model on a nonlinear truth

def _prop_model(kind, seed):
    if kind == "flexible":
        # Round 4 fix: boosted propensities were overconfident (down to 0.003 where the truth is >= 0.03),
        # which biased AIPW by up to -46% at effect 1. Degree-2 logistic gave valid coverage at both sizes.
        return make_pipeline(StandardScaler(), PolynomialFeatures(2, include_bias=False), LogisticRegression(C=1.0, max_iter=2000))
    return LogisticRegression(max_iter=1000)   # 'wrong': misses the squared / interaction terms

NUISANCE_SPECS = {
    "both_ok":       ("flexible", "flexible"),
    "outcome_wrong": ("wrong",    "flexible"),
    "prop_wrong":    ("flexible", "wrong"),
    "both_wrong":    ("wrong",    "wrong"),
}

def crossfit_propensity(X, T, seed, folds=5, kind="flexible"):
    e_hat = np.zeros(len(T))
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        e_hat[te] = _prop_model(kind, seed).fit(X[tr], T[tr]).predict_proba(X[te])[:, 1]
    return e_hat

def aipw(X, T, Y, spec, seed, folds=5, clip=0.01, e_hat=None):
    """Returns ATE estimate, its standard error, fitted propensities and held-out outcome predictions.
    Pass e_hat to reuse propensities that were already fitted on the same X, T, seed and folds."""
    out_kind, prop_kind = NUISANCE_SPECS[spec]
    n = len(Y)
    if e_hat is None:
        e_hat = crossfit_propensity(X, T, seed, folds, prop_kind)
    mu0_hat, mu1_hat = np.zeros(n), np.zeros(n)
    for tr, te in KFold(folds, shuffle=True, random_state=seed).split(X):
        for t, store in ((0, mu0_hat), (1, mu1_hat)):
            idx = tr[T[tr] == t]
            om = _outcome_model(out_kind, seed).fit(X[idx], Y[idx])
            store[te] = om.predict(X[te])
    e_c = np.clip(e_hat, clip, 1 - clip)
    psi = (mu1_hat - mu0_hat
           + T * (Y - mu1_hat) / e_c
           - (1 - T) * (Y - mu0_hat) / (1 - e_c))       # influence-function scores
    ate = psi.mean()
    se = psi.std(ddof=1) / np.sqrt(n)
    return float(ate), float(se), e_hat, mu0_hat, mu1_hat

# ---------- 3. The detectors ----------
def extreme_share(e_hat):
    return float(np.mean((e_hat < 0.02) | (e_hat > 0.98)))

def detector(cfm_ate, aipw_ate, aipw_se, e_hat, alpha_z=1.645, overlap_tol=0.05):
    """Rounds 1-3: flags any gap toward zero bigger than AIPW's noise. Unchanged, kept as the baseline."""
    if extreme_share(e_hat) > overlap_tol:
        return "uncertain", np.nan
    gap = aipw_ate - cfm_ate
    z = np.sign(aipw_ate) * gap / max(aipw_se, 1e-12)   # >0 means CFM sits closer to 0
    return ("flag" if z > alpha_z else "no_flag"), float(z)

def _verdict(z, alpha_z):
    if z > alpha_z:
        return "shrunk"
    return "not_shrunk" if z < -alpha_z else "inconclusive"

def margin_detector(cfm_ate, aipw_ate, aipw_se, e_hat, margin=0.10, alpha_z=1.645, overlap_tol=0.05):
    """Tests the claim the label makes: is the CFM more than `margin` closer to zero than the truth?
    Fixes the null, but still uses AIPW's SE alone."""
    if extreme_share(e_hat) > overlap_tol:
        return "uncertain", np.nan
    z = np.sign(aipw_ate) * ((1 - margin) * aipw_ate - cfm_ate) / max((1 - margin) * aipw_se, 1e-12)
    return _verdict(z, alpha_z), float(z)

def rectifier_scores(mu0_hat, mu1_hat, T, Y, e_hat, clip=0.01):
    """Each unit's correction to the model's own held-out predictions, weighted as in AIPW."""
    e_c = np.clip(e_hat, clip, 1 - clip)
    return T * (Y - mu1_hat) / e_c - (1 - T) * (Y - mu0_hat) / (1 - e_c)

def rectifier_detector(mu0_hat, mu1_hat, T, Y, e_hat, margin=0.10, alpha_z=1.645, overlap_tol=0.05):
    """Margin test on a sample mean. mu0_hat and mu1_hat must be held-out predictions.
    The mean of the scores is (1-margin)*ATE - CFM ATE, and their spread is its own SE,
    so the variance accounts for both estimates using the same data."""
    if extreme_share(e_hat) > overlap_tol:
        return "uncertain", np.nan, np.nan
    r = rectifier_scores(mu0_hat, mu1_hat, T, Y, e_hat)
    cate = mu1_hat - mu0_hat
    psi = (1 - margin) * r - margin * cate
    n = len(Y)
    s = np.sign(cate.mean() + r.mean())
    z = s * psi.mean() / max(psi.std(ddof=1) / np.sqrt(n), 1e-12)
    z0 = s * r.mean() / max(r.std(ddof=1) / np.sqrt(n), 1e-12)       # no margin: >0 toward zero, <0 away from it
    return _verdict(z, alpha_z), float(z), float(z0)

# ---------- 4. Ground-truth labels ----------
def truly_shrunk(cfm_ate, true_ate, rel_tol=0.10):
    """CFM estimate is pulled toward zero by more than 10% of the true effect."""
    return bool(np.sign(true_ate) * (true_ate - cfm_ate) > rel_tol * abs(true_ate))

def truly_inflated(cfm_ate, true_ate, rel_tol=0.10):
    """CFM estimate is pushed away from zero by more than 10% of the true effect."""
    return bool(np.sign(true_ate) * (cfm_ate - true_ate) > rel_tol * abs(true_ate))

# ---------- 5. Planted-effect self-test ----------
def planted_effect(X, Y, k):
    """A known effect that varies with X0, which drives treatment, centred so the true ATE does not move.
    Built from X rather than estimated propensities: those also set the AIPW weights, which made the
    plant largest exactly where the weights were most extreme. Y + T*delta needs no reference to judge."""
    x = X[:, 0]
    return k * Y.std() * (x - x.mean()) / x.std()

def naive_contrast(T, Y):
    return float(Y[T == 1].mean() - Y[T == 0].mean())

# ---------- 6. Results helpers ----------
def done_keys(path, cols):
    if not os.path.exists(path):
        return set()
    prev = pd.read_csv(path)
    return set(map(tuple, prev[cols].drop_duplicates().values.tolist()))

# ---------- 7. AIPW cache: all the CPU-only work, done once ----------
def treatment_key(seed, n, dgp):
    """Treatment depends only on X and the direction of confounding, not on the effect size."""
    return f"{seed}_{n}_{int(dgp == 'flipped')}"

def _propensity_job(key, dgp, n, seed):
    X, T, *_ = simulate(n, 1.0, "good", seed, dgp=dgp)
    return key, crossfit_propensity(X, T, seed)

def _aipw_job(seed, dgp, es, n, e_hat):
    X, T, Y, *_ = simulate(n, es, "good", seed, dgp=dgp)
    a, se, *_ = aipw(X, T, Y, "both_ok", seed, e_hat=e_hat)
    return dict(dgp=dgp, effect_size=es, n=n, seed=seed, aipw_ate=a, aipw_se=se, y_check=float(Y.sum()))

def build_aipw_cache(grid, csv_path, npz_path, n_jobs=-1):
    """grid holds (seed, dgp, effect_size, n). Finished work is kept, so this can be re-run or run elsewhere first.
    Propensity models are fitted once per (seed, n, confounding direction) instead of once per dataset,
    and each worker uses one thread because boosting scales better across datasets than within one fit."""
    from joblib import Parallel, delayed, parallel_config
    props = dict(np.load(npz_path)) if os.path.exists(npz_path) else {}
    todo = {treatment_key(s, n, d): (d, n, s) for s, d, es, n in grid if treatment_key(s, n, d) not in props}
    done = done_keys(csv_path, ["seed", "dgp", "effect_size", "n"])
    rest = [g for g in grid if g not in done]
    with parallel_config(backend="loky", inner_max_num_threads=1):
        if todo:
            props.update(Parallel(n_jobs=n_jobs)(delayed(_propensity_job)(k, *v) for k, v in todo.items()))
            np.savez(npz_path, **props)
        for i in range(0, len(rest), 200):       # saved in blocks so an interruption loses little
            rows = Parallel(n_jobs=n_jobs)(delayed(_aipw_job)(s, d, es, n, props[treatment_key(s, n, d)])
                                           for s, d, es, n in rest[i:i + 200])
            pd.DataFrame(rows).to_csv(csv_path, mode="a", header=not os.path.exists(csv_path), index=False)
    return props
