# CFM shrinkage detector: novelty extensions and competing work

Research date: 2026-10-31. Current objective under evaluation: a cheap, model-agnostic diagnostic that detects shrinkage in causal foundation models (CFMs) such as CausalPFN, using a cross-fitted AIPW reference, a one-sided z-test, abstention under poor overlap, and a simulated positive control.

Evidence tags used throughout:
- **[P-read]**: I read the primary text or code directly (PDF text extraction, cloned repo, published CSV).
- **[P-fetch]**: primary page, read through a summarising fetch tool. Numbers should be spot-checked before quoting.
- **[P-meta]**: primary metadata or abstract only (arXiv API, proceedings listing).
- **[S]**: secondary (search excerpt, or another paper's description or reference list).
- **Foundational**: older work, included as background.
- **"My calculation" / "Inference"**: my own work, not a published claim.

Peer-review status: Melnychuk et al., Wang et al., Reuter et al. (ICML 2026), CausalPFN, Do-PFN, De Bartolomeis et al. (NeurIPS 2025) and CausalFM (ICLR 2026) are peer reviewed. Stith et al., Zhang, Jung et al., Schulman et al., Mourao et al. and Neunhoeffer are preprints or working papers.

## Cross-cutting: has the base objective's premise changed?

### Takeaway
Yes. Since September 2026, CFM shrinkage has been named in print, and CausalPFN looks like the wrong flagship for "toward zero" shrinkage: Do-PFN and CausalFM show it, CausalPFN largely does not. A user-side detection test still appears to be missing, so the niche exists, but a z-test against AIPW is too simple to carry a novelty claim alone.

### Cited Findings
- Stith, Rahmani, Cresswell, "Causal Foundation Models", arXiv preprint, Sep 2026. On RealCause-Lalonde, Do-PFN and CausalFM have ATE relative error near 1 with tiny standard errors, which the authors read as "a systematic shrinkage of the predicted effect toward zero", while CausalPFN reaches 0.17 on CPS. [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003)
- The same paper lists "automatic detection of mismatch between the target DGP and the training prior" as a desirable future property, and calls it especially difficult in the causal setting. This is direct support for a diagnostic being an open problem. [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003)
- Zhang, "Learning to Fluctuate: Statistical Foundations for Causal Tabular Pretraining", arXiv preprint, Sep 2026. Argues that latent-effect supervision "rewards posterior shrinkage", and reports that shrinkage improves point risk near the prior centre but attenuates shifted effects. [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- In Zhang's Table 3 (four-stratum synthetic mechanism, effect shift), the released CausalPFN-S has RMSE .0695 and through-origin response slope 1.021, close to AIPW/DML (.0663, 1.026). A matched in-house latent-effect network has RMSE .1364 and slope −.058. The slope is against the oracle efficient fluctuation, not against effect size. Zhang's "−75 g versus −150 g" example is an illustrative hypothetical, not a CausalPFN measurement. [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- Melnychuk, Balazadeh, Feuerriegel, Krishnan, "Frequentist Consistency of Prior-Data Fitted Networks for Causal Inference", ICML 2026 (PMLR 306). The named mechanism is prior-induced confounding bias: the learned prior shrinks *observed confounding* toward zero, not the effect. Its Δ measure is the gap between the ATE and the difference in observed group means. [P-fetch] — [arXiv 2603.12037](https://arxiv.org/abs/2603.12037)
- CausalPFN's code z-standardises outcomes **separately per treatment arm** before the network and restores each arm's mean and scale afterwards (`_get_y0_y1_shift_scale`, lines 128-156; standardisation line 257; restoration line 298, commit b7ed2f1, v0.1.5). [P-read] — [icl_model.py](https://github.com/vdblm/CausalPFN/blob/b7ed2f1e1d58a83c608d08ced3dee955f0a7c221/src/causalpfn/models/icl_model.py)
- Arm statistics are computed on each query's context, which is selected by nearest neighbours on a gradient-boosting weak-learner CATE. [P-read] — [causal_estimator.py](https://github.com/vdblm/CausalPFN/blob/b7ed2f1e1d58a83c608d08ced3dee955f0a7c221/src/causalpfn/causal_estimator.py)
- By contrast, the Stith et al. benchmark wrapper for Do-PFN standardises Y once across all units, and converts back by multiplying by Y's standard deviation. This is the benchmark wrapper, not necessarily the official library. [P-read] — [wrap_dopfn.py](https://github.com/layer6ai-labs/cfms/blob/84c1dea61bab3da1cd36ba02ae47b5dd0af7e98b/causal_bench/wrap_dopfn.py)
- My calculation from the checked-in benchmark results (`benchmark_results_cpu.csv`, commit 84c1dea, 10 realisations per cell, ratio of `ate_hat` to `ate_true`). Scaling code was inspected and shows no obvious unit bug, but these results are not independently re-run. [P-read] — [cfms data folder](https://github.com/layer6ai-labs/cfms/tree/main/data)

| Estimator | Mean ratio, Lalonde-CPS (true ATE about −7056) | Mean ratio, Lalonde-PSID (true ATE about −13450) |
|---|---|---|
| CausalFM | 0.058 | 0.053 |
| Do-PFN | 0.116 | 0.113 |
| CausalPFN | 0.973 (SD .197) | 0.763 (SD .127) |
| S-learner | 0.026 | 0.293 |
| X-learner | 0.109 | 0.111 |
| DR-learner | 0.110 | 0.358 |
| T-learner | 1.277 | 0.986 |
| IPW | 1.136 | 0.966 |
| Debiased ML | 0.908 (SD .405) | 0.855 (SD .358) |

- Caveat on that table: RealCause simulates outcomes from a fitted generative model, and the comparison has very little covariate overlap. [P-read] — [LALONDE_DATASET.md](https://github.com/layer6ai-labs/cfms/blob/main/docs/LALONDE_DATASET.md)
- Reuter et al. attribute CausalPFN's RealCause advantage to its training data closely mimicking the RealCause DGP, so a CausalPFN win here may not generalise. [S] — [arXiv 2602.14972](https://arxiv.org/abs/2602.14972)
- Project notebook facts (local file `/Users/chiranthr/Documents/Projects/ADA_PROJECT/shrinkage_detector_round3_gpu.ipynb`). `detector()` flags only if the CFM is closer to zero than AIPW with z > 1.645, using AIPW's SE alone. `truly_shrunk()` labels shrinkage only above a 10% margin. `fake_cfm()` adds independent Gaussian noise (SD 0.05). The notebook states round 1 found "CausalPFN barely shrank". [P-read]
- My calculation on the notebook's simulator only (2M draws, no CFM involved): the naive arm difference exceeds the ATE by +0.90 under good overlap and +1.50 under poor overlap, so confounding bias is positive.

### Inferences
- **Primary reframing hypothesis, not run.** With per-arm standardisation, if the network predicts nothing useful, the estimate falls back to the local difference in arm means rather than to zero. So CausalPFN's natural failure is under-adjustment (pull toward the naive contrast), which matches Melnychuk et al.'s mechanism. Do-PFN and CausalFM (pooled standardisation) can fail toward zero.
- **A likely explanation of the team's round 1 null, not run.** In the notebook's DGP, a pull toward the naive contrast moves a positive estimate *up*, away from zero, so the one-sided detector cannot see it. At effects of 16 or more, a +0.9 bias is also under 6% of the effect, below the 10% label. The big-effect sweep may be structurally unable to fire. Cheapest test: negate `score` in `simulate()` so naive bias is about −0.9, then run effects 1, 2, 4.
- The S-learner versus T-learner gap in the table resembles the Do-PFN/CausalFM versus CausalPFN gap. The analogy is suggestive but incomplete: X- and DR-learners also shrink, while Debiased ML does not, so pooled versus per-arm handling cannot be the whole story.
- The objective's wording should change from "shrinkage toward zero for large effects" to something like "attenuation toward an anchor, where the anchor depends on the model's outcome handling".

### Gaps
- None of the mechanism claims above have been tested by running the models. They rest on code reading plus published numbers.
- This field is moving very fast: four directly relevant preprints appeared between 2 Sep and 16 Oct 2026. Any "nobody has done X" claim must be re-checked immediately before submission.

## Direction 1: Detect-then-repair (CFM inside AIPW/DML/TMLE, or one-step correction)

### Takeaway
**Crowded.** Four repair routes appeared in 2026 (two peer reviewed, two preprints), including an ICML 2026 paper that does exactly the one-step correction, co-authored by two CausalPFN authors. Coverage evidence is thinner than the theory, and the test-then-repair decision rule appears unstudied. Feasibility on T4: good for a small comparison, poor for a new repair method.

### Cited Findings
**What exists**
- Melnychuk et al., ICML 2026: one-step posterior correction (OSPC), implemented with martingale posteriors (MP-OSPC), restores frequentist consistency and gives a semi-parametric Bernstein-von Mises result. It covers TabPFN as main backbone, and CausalPFN as plug-in and as nuisance. Do-PFN is excluded as non-identifiable. Code exists, including `prior_bias_check` notebooks. [P-fetch; repo P-read] — [arXiv 2603.12037](https://arxiv.org/abs/2603.12037), [repo](https://github.com/Valentyn1997/freq-cons-pfns)
- **Does it restore coverage?** That paper reports no coverage rates. It reports TV distance to the A-IPTW asymptotic normal and a KS distance on the PIT. IHDP results are mixed: CausalPFN plug-in dTV .239 / dKS .14; TabPFN-only MP-OSPC dTV .319 / dKS .09. [P-fetch] — [arXiv 2603.12037](https://arxiv.org/html/2603.12037v3)
- Its limits: TabPFN's inverse-propensity posterior concentrates only up to about n = 1000; propensities below .05 are truncated; CausalPFN outcome posteriors degrade as n grows; most ACIC 2016 datasets have |Δ| below .25, and MP-OSPC almost always helps above that. [P-fetch] — [arXiv 2603.12037](https://arxiv.org/html/2603.12037v3)
- Melnychuk et al.'s diagnostics are not usable on a real user dataset: Δ is computed on prior datasets and R̂₂ uses true nuisance functions. [P-fetch] — [arXiv 2603.12037](https://arxiv.org/html/2603.12037v3)
- Neunhoeffer, "Learning from Small Data: Tabular Foundation Models for Political Science", job market paper, Sep 2026. TabPFN as DML nuisance (partially linear model, 5 folds, θ = 0.5, n = 500, 500 replications): bias −0.002, coverage 95.0% (MCSE 1.0). TabPFN plug-in without orthogonal score: bias −0.229, coverage 0%. Tuned boosting: 89.4%. The author notes this rests on simulation, not theory. CFMs were deliberately not used, citing Melnychuk et al. [P-read] — [PDF](https://www.marcel-neunhoeffer.com/pdf/papers/neunhoeffer_learning-from-small-data.pdf)
- A documented DoubleML + TabPFN example exists. [S] — [DoubleML docs](https://docs.doubleml.org/dev/examples/learners/py_tabpfn.html)
- Mourao, Hajage, Bystrova, Bouvarel, Lapidus, Carrat, Glemain, "Prior-Data Fitted Networks for Causal Inference: a Simulation Study with Real-World Scenarios", arXiv preprint, 2026. At n = 1000 (Indomethacin / Rotterdam): CausalPFN coverage 54.3% / 67.6%; TabPFN IPTW 95.2% / 91.1%; TabPFN T-learner 93.7% / 91.5%. AIPW and TMLE were not evaluated. TabPFN with bootstrap reached about 16,500 s on Rotterdam. [P-fetch] — [arXiv 2603.15928](https://arxiv.org/abs/2603.15928)
- Zhang, 2026 (training-side repair): fluctuation-supervised pretraining. Known-effect semisynthesis at n = 256: as the effect rises from .025 to .15, coverage goes .972 → .919, versus 1.000 → .112 for latent-effect supervision. [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- Wang et al., "Unveiling Prior-data Fitted Networks on Causal Effect Estimation: Pre-training or Finetuning?", ICML 2026. Proposes target-specific fine-tuning (PWF, MSF) for "prior uncoverage". Authors are from Stith et al.'s reference list: Haotian Wang, Xinpeng Lv, Hao Zou, Yanghao Xiao, Shanzhi Gu, Yang Shi, Yunxin Mao, Yuanxing Zhang, Mingyang Geng, Shaowu Yang, Haoxuan Li, Wenjing Yang, Peng Cui, Zhouchen Lin. [S] — [ICML listing](https://icml.cc/virtual/2026/poster/63252)
- Schulman, Bynum, Wald, "Unit-level aggregation breaks coverage in causal foundation models", arXiv preprint, Oct 2026. New heads on a frozen CausalPFN raise full-sample coverage from 53% to about 90% across six benchmarks. [P-fetch] — [arXiv 2610.22770](https://arxiv.org/abs/2610.22770)

**Nearby**
- De Bartolomeis, Abad, Wang, Donhauser, Duch, Yang, Dahabreh, "Efficient Randomized Experiments Using Foundation Models", NeurIPS 2025. Hybrid AIPW with LLM predictions stays valid when predictions are arbitrarily biased. RCT setting, not CFMs. [P-meta] — [arXiv 2502.04262](https://arxiv.org/abs/2502.04262)
- Yiu, Fong, Holmes, Rousseau, "Semiparametric posterior corrections", arXiv 2023. Foundational for posterior one-step correction; journal not re-verified. [P-meta] — [arXiv 2306.06059](https://arxiv.org/abs/2306.06059)
- Angelopoulos, Bates, Fannjiang, Jordan, Zrnic, "Prediction-Powered Inference", arXiv 2023. Foundational for the rectifier idea; journal not re-verified. [P-meta] — [arXiv 2301.09633](https://arxiv.org/abs/2301.09633)
- Oberst, D'Amour, Chen, Wang, Sontag, Yadlowsky, "Understanding the Risks and Rewards of Combining Unbiased and Possibly Biased Estimators, with Applications to Causal Inference", arXiv 2022; venue not re-verified. Relevant to a CFM + AIPW combination. [P-meta] — [arXiv 2205.10467](https://arxiv.org/abs/2205.10467)
- Leeb and Pötscher, "Model Selection and Inference: Facts and Fiction", Econometric Theory 21(1), 2005. Foundational: ignoring a selection step invalidates later inference; pretest estimators are the classic case. [S] — [Cambridge](https://www.cambridge.org/core/journals/econometric-theory/article/abs/model-selection-and-inference-facts-and-fiction/EF3C7D79D5AFC4C6325345A3C8E26296)

### Inferences
- **Adds:** do not pitch a new repair. Two narrow claims remain: (a) actual coverage of AIPW with CausalPFN as outcome nuisance, across effect size and confounding sign, since available coverage numbers cover TabPFN rather than CausalPFN-as-nuisance; (b) "detect, then use CFM if not flagged" is a pretest estimator, so a not-flagged result is not a licence. This could be a useful negative result, especially given Schulman et al.'s independent coverage failure.
- **Work:** about 1-2 person-weeks. Cross-fitted AIPW with CausalPFN outcomes is feasible on T4. TabPFN-only MP-OSPC is memory intensive (the authors used an H200 GPU), so use the copula variant or reuse their code at n ≤ 1000. These effort numbers are my judgement.

### Gaps
- Melnychuk et al.'s Figures 9 and 13 (CausalPFN outcome + TabPFN propensity) had no extractable values, so CausalPFN-as-nuisance performance there is unknown to me.
- Negative result: no independent replication of OSPC found, no coverage study of CausalPFN inside AIPW, no analysis of test-then-repair for CFMs. Queries: "TabPFN nuisance double machine learning AIPW coverage treatment effect"; "debiasing causal foundation model one-step correction prior-data fitted network valid inference"; "test-then-pool pretest estimator inflated type I error combining biased and unbiased estimators causal".
- The test-then-pool literature itself did not surface in search, so Viele-style references remain unverified and are not cited here.

## Direction 2: Rescaling as the mechanism, and metamorphic testing

### Takeaway
**Open, with a trap.** I found no metamorphic test suite for CFMs. The nearest work (Jung et al., Sep 2026) uses controlled SCM changes that cannot run on a user's real data. The trap: Y×c, Y+c and Y+δT are all essentially vacuous for CausalPFN because of its per-arm standardisation, so a useful suite needs relations that preprocessing cannot satisfy automatically. Feasibility on T4: very good.

### Cited Findings
- Jung, Seo, Byun, Lee, Song, "What You Observe Determines How You Identify Causal Effects: Evaluating Causal Models across Observational Views" (CausalIDView), arXiv preprint, Sep 2026. "Stay" reverses the confounding contribution, leaving true CATE unchanged. "Move" doubles the mediator-outcome response, doubling true CATE. CausalPFN shows relatively large Stay errors, Do-PFN large Move errors, CausalFM a view-dependent mix. Does not test shifts of Y or injected constants. The text and table disagree on one null-effect claim (Illinois). Code is public. [P-fetch] — [arXiv 2609.36881](https://arxiv.org/abs/2609.36881), [repo](https://github.com/MLAI-Yonsei/CausalIDView)
- Clark, Foster, Prifling, Walkinshaw, Hierons, Schmidt, Turner, "Testing Causality in Scientific Modelling Software", ACM TOSEM 2023. Uses causal inference to test software against metamorphic relations; the reverse direction from testing a causal estimator. [P-meta] — [arXiv 2209.00357](https://arxiv.org/abs/2209.00357), [ACM](https://dl.acm.org/doi/10.1145/3607184)
- Clark, Foster, Walkinshaw, Hierons, "Metamorphic Testing with Causal Graphs", IEEE ICST 2023. Generates metamorphic relations from DAGs. [P-fetch] — [White Rose eprint](https://eprints.whiterose.ac.uk/id/eprint/195317/)
- Regression and scale equivariance are classical properties of regression estimators, attributed to Rousseeuw and Leroy (1987). Foundational; the book itself was not retrieved. [S] — [arXiv 1801.04716](https://arxiv.org/pdf/1801.04716), [arXiv 2604.14182](https://arxiv.org/pdf/2604.14182)
- TabPFN z-normalises inputs, so feature scaling does not change predictions, and the network expects roughly normal features and targets. Authors not re-verified (Hollmann et al.). [S] — [Nature 2025](https://www.nature.com/articles/s41586-024-08328-6)
- Biloš, Wilson, Schneider, Nevmyvaka, "A Mechanistic Study of Tabular Foundation Models", arXiv 2026: column invariance is broken in TabPFNv2 by learned per-feature weights, and label invariance by learned label embeddings. [S] — [arXiv 2605.21288](https://arxiv.org/abs/2605.21288)
- CausalPFN's prior: noise variance is "uniformly drawn from (0, Var(μt)]", so noise never exceeds signal variance in training. Heterogeneity is scaled by γ ∈ [0,1]. Output is a discrete posterior on [−10, 10], rescaled to the outcome scale. [P-fetch] — [arXiv 2506.07918](https://arxiv.org/html/2506.07918v2). The [−10, 10] range, but not the noise prior, is confirmed in [code](https://github.com/vdblm/CausalPFN/blob/b7ed2f1e1d58a83c608d08ced3dee955f0a7c221/src/causalpfn/models/icl_model.py) [P-read]
- High-dimensional inputs: the code path for `tabdpt` checkpoints builds a `TruncatedSVD` to the model's maximum feature count; default `max_context_length` is 4096. [P-read] — [causal_estimator.py](https://github.com/vdblm/CausalPFN/blob/b7ed2f1e1d58a83c608d08ced3dee955f0a7c221/src/causalpfn/causal_estimator.py)

### Inferences
Relation map, derived by me from the code reading. Treat as hypotheses to confirm in one Colab session.

| Relation | Expected result | Value for CausalPFN |
|---|---|---|
| Y → cY | Estimate × c | Vacuous, standardisation handles it |
| Y → Y + c | Unchanged | Vacuous |
| Y → Y + δT, constant δ | Estimate + δ | Near-vacuous: within a stratum, network inputs are identical; only the weak-learner stratifier can break it. Informative for pooled-standardising models |
| **Y → Y + δ(X)T, with δ correlated with propensity** | Estimate + mean δ(X) | Informative. A naive-anchored model moves by E[δ(X)|T=1] instead |
| T → 1−T | Estimate × −1 | Not guaranteed |
| Row or column permutation, adding noise covariates, rotating X | Unchanged or nearly so | Not guaranteed, see Biloš et al. |

- **The key new quantity, my proposal.** Adjustment fraction = (observed shift − E[δ|T=1]) / (mean δ − E[δ|T=1]). A value of 1 means full confounding adjustment; 0 means the model behaves like the naive contrast. It targets Melnychuk et al.'s mechanism, on the user's own data, with no reference estimator.
- **Why the oracle is exact, my derivation.** δ(X) is a known function of X applied to treated outcomes, so the change in the sample ATE is exactly mean δ(X) even under hidden confounding. This should be confirmed in simulation and reviewed by someone comfortable with the theory.
- **Rescaling mechanism.** For CausalPFN, the effect-to-outcome-SD ratio is largely invisible to the network in a homogeneous-effect case. What it can see is within-arm signal-to-noise. So the notebook's `B_NOISE = [1.0, 0.25]` probes the wrong side: the prior boundary is noise variance *above* signal variance, which argues for testing higher noise, not lower.
- For pooled standardisation, with a very large homogeneous effect and balanced arms, the standardised effect saturates near 2 (it tends to 1/√(p(1−p))), and the outcome turns bimodal. Prediction: failure is prior shift in outcome shape rather than a raw magnitude problem.
- **Adds:** "first metamorphic audit of CFMs" with a per-model failure profile, and a warning that the obvious relations have no power. **Work:** about 1-2 person-weeks.

### Gaps
- Negative result: no paper applying metamorphic relations to a CFM or a tabular foundation model. Queries: "metamorphic testing causal effect estimators invariance tabular foundation model"; 'TabPFN "metamorphic" OR "invariance" test feature scaling target transformation robustness tabular foundation model'; '"metamorphic relations" treatment effect estimation CATE causal inference library testing'.
- arXiv API queries `all:"prior-data fitted" AND all:"metamorphic"` and `all:"foundation model" AND all:"metamorphic" AND all:tabular` returned empty, but arXiv began returning HTTP 429 in the same run, so those empties are **not reliable** evidence. Semantic Scholar was not queried.
- No paper directly tests CFM bias as a function of effect size relative to outcome SD. Mourao et al. used two fixed ATEs. Insufficient publicly verifiable evidence beyond Zhang's effect-shift experiments.
- The exact behaviour of the weak-learner stratifier under injected effects is unmeasured.

## Direction 3: Plasmode / planted-effect self-test on the user's own data

### Takeaway
**Mature elsewhere, open for CFMs as a deployment self-test.** OHDSI has done effect injection and empirical calibration in pharmacoepidemiology for years, and DoWhy has a generic known-effect refuter. CFM papers use known-effect semisynthesis only as a developer-side benchmark. Using it on the user's own data, with a slope and intercept calibration, looks unclaimed. Feasibility on T4: very good, and it is the cheapest option with real novelty.

### Cited Findings
**Effect injection in OHDSI (foundational)**
- Schuemie, Hripcsak, Ryan, Madigan, Suchard, "Empirical confidence interval calibration for population-level effect estimation studies in observational healthcare data", PNAS 115(11):2571-2577, 2018. Positive controls are synthesised by modifying negative controls; calibration restores near-nominal coverage. [S] — [DOI](https://doi.org/10.1073/pnas.1708282114), [record](https://omicsdi.org/dataset/biostudies-literature/S-EPMC5856503)
- Schuemie et al., "Interpreting observational studies: why empirical calibration is needed to correct p-values", Statistics in Medicine 33(2):209-218, 2014 (one vignette gives 2013). [S] — [package manual](https://ohdsi.r-universe.dev/EmpiricalCalibration/doc/manual.html)
- Schuemie, Cepeda, Suchard, Yang, Tian, Schuler, Ryan, Madigan, Hripcsak, "How Confident Are We About Observational Findings in Health Care: A Benchmark Study", Harvard Data Science Review 2.1, 2020. From 200 negative controls, an L1-regularised Poisson model on baseline covariates injects outcomes to reach rate ratios 1.5, 2 and 4, giving 600 positive controls. This preserves measured but not unmeasured confounding, and the authors say the resulting metrics may be somewhat optimistic. Before calibration, roughly half of 95% intervals covered the truth in most contexts. [P-fetch] — [HDSR](https://hdsr.mitpress.mit.edu/pub/fxz7kr65)
- Injection is implemented in `MethodEvaluation::synthesizePositiveControls`. The page was seen through search; a later fetch returned 404. [S] — [rdrr](https://rdrr.io/github/OHDSI/MethodEvaluation/man/synthesizePositiveControls.html)
- CI calibration needs a model of how systematic error varies with true effect size: assumed from negative controls alone, or estimated with positive controls. [S] — [vignette](https://ohdsi.r-universe.dev/EmpiricalCalibration/doc/EmpiricalCiCalibrationVignette.html)
- Phil. Trans. R. Soc. A 2018 paper, "Improving reproducibility by using high-throughput observational studies with empirical calibration", describes injecting simulated outcomes during exposure. The PMC page returned a CAPTCHA, so authors were not verified. [S] — [PMC6107542](https://pmc.ncbi.nlm.nih.gov/articles/PMC6107542)

**Plasmode methodology**
- Schreck, Slynko, Saadati, Benner, "Statistical plasmode simulations: Potentials, challenges and recommendations", Statistics in Medicine 43(9):1804-1825, 2024. Tutorial, framing plasmodes as complementary to parametric simulation. [S] — [arXiv 2305.06028](https://arxiv.org/abs/2305.06028)
- Shaw, Gruber, Williamson, Desai, Shortreed, Krakauer, Nelson, van der Laan, "A cautionary note for plasmode simulation studies in the setting of causal inference", arXiv 2025. "Sample Treatment" (bootstrap X and observed T together, then generate Y) biases evaluation of propensity-based methods through a positivity violation, with bias of order n^(-1/2). They recommend "Generate Treatment". [P-fetch] — [arXiv 2504.11740](https://arxiv.org/abs/2504.11740)
- Advani, Kitagawa, Słoczyński, "Mostly Harmless Simulations? Using Monte Carlo Studies for Estimator Selection", Journal of Applied Econometrics 34(6):893-910, 2019. Empirical Monte Carlo is unlikely to be informative for estimator selection except under restrictive conditions, and does worse than random at picking lowest absolute bias in their setting. [S] — [arXiv 1809.09527](https://arxiv.org/abs/1809.09527)
- Knaus, Lechner, Strittmatter, "Machine Learning Estimation of Heterogeneous Causal Effects: Empirical Monte Carlo Evidence", Econometrics Journal 24:134-161, 2021. Uses empirical Monte Carlo constructively. [P-meta] — [arXiv 1810.13237](https://arxiv.org/abs/1810.13237)

**Closest in or near the CFM space**
- Zhang, 2026: "known-effect semisynthesis" retains only real stratum proportions and samples new assignments and outcomes, so it is not injection into real outcomes. NSW re-randomised null and post-treatment contrasts are also evaluated, and "lower RMSE can coexist with residual attenuation". [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- Jung et al., 2026: pre-treatment outcomes from three RCTs (ACTG 175, Pennsylvania Reemployment Bonus, Illinois UI) as negative controls. [P-fetch] — [arXiv 2609.36881](https://arxiv.org/abs/2609.36881)
- Stith et al. 2026 show Do-PFN and CausalFM errors with tiny standard errors, but test no injection. [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003)
- de Vassimon Manela, Battaglia, Evans, "Marginal Causal Flows for Validation and Inference", NeurIPS 2024 (Frugal Flows): generates data resembling real data with a user-defined ATE. It needs a flow per dataset, so it is heavier. [P-fetch] — [arXiv 2411.01295](https://arxiv.org/abs/2411.01295)
- Sharma and Kiciman, "DoWhy: An End-to-End Library for Causal Inference", arXiv 2020. [P-meta] — [arXiv 2011.04216](https://arxiv.org/abs/2011.04216)
- **The nearest software precedent.** DoWhy's dummy outcome refuter adds a user-supplied `true_causal_effect(T)` to a transformed dummy outcome on held-out data, then refits the estimator. The default is no effect. Its signature takes only the treatment column, so a covariate-dependent δ(X) is not supported in that argument. It is generic, with no CFM use and no slope or intercept calibration. Any novelty claim must acknowledge it. [P-read] — [dummy_outcome_refuter.py](https://github.com/py-why/dowhy/blob/main/dowhy/causal_refuters/dummy_outcome_refuter.py)
- Panagopoulos, "Real vs. Semi-Simulated: Rethinking Evaluation for Treatment Effect Estimation", arXiv 2026: semi-simulated rankings do not transfer to real data. No CFMs included. This motivates testing on the user's own data. [P-fetch] — [arXiv 2605.10430](https://arxiv.org/abs/2605.10430)
- Non-scholarly: a personal GitHub PR describes a "known-truth battery" scoring classical estimators against planted effects. Numbers unverified. [S] — [pacland PR](https://github.com/robmitchellengineering-hub/pacland/pull/171)

### Inferences
- **Adds, my proposal:** an empirical calibration for CFMs by direct analogy to OHDSI. Inject effects at several sizes and shapes to estimate slope; use placebo or re-randomised nulls for the intercept; report estimate as (τ̂ − a)/b. Claims: reference-free, runs on the user's data, unaffected by hidden confounding in its response oracle, costs only a few forward passes.
- **Paired design:** comparing τ̂(D_δ) with τ̂(D) on the same X, T and noise should cancel much sampling noise, so power may be high at small n. This needs checking, because a CFM is not a linear smoother.
- **Honest limit 1:** this measures response, not absolute bias. A model with a constant offset and slope 1 passes. It therefore complements, not replaces, the AIPW arm.
- **Honest limit 2:** constant injection into CausalPFN is near-vacuous (Direction 2). Covariate-dependent injection is needed, and binary outcomes need sampled flips, as OHDSI does.
- **Honest limit 3:** to obtain replicates, do not bootstrap X and T together (Shaw et al.). Use subsampling without replacement or random draws of δ(X). This adaptation is mine and is untested.
- **Honest limit 4:** Advani et al. warn against over-claiming. Pitch this as falsification of a specific property, not as selecting the best estimator.
- **Work:** about 1 person-week for the core. At the notebook's stated runtime (700 datasets in 1-1.5 hours on T4, about 5-8 s per dataset including AIPW), a 5-effect-size self-test costs under a minute per dataset.

### Gaps
- Negative result: no paper or tool found that injects a known effect into a user's real outcomes to audit a CFM at deployment time, or that ports OHDSI calibration to CFMs. Queries: "synthetic positive controls effect injection empirical calibration Schuemie OHDSI"; "plasmode simulation recommendations 2024 causal machine learning treatment effect evaluation real data"; "injected known treatment effect into real data validate estimator placebo empirical Monte Carlo causal machine learning"; "planted effect self-test causal estimator real dataset known additive effect added to treated outcomes recover slope foundation model"; "causal foundation model diagnostic detect failure on user data placebo negative control audit CausalPFN".
- arXiv API `all:"causal foundation model" AND all:placebo` and `AND all:diagnostic` returned empty in the rate-limited run, so they are not reliable.
- Whether placebo and injection stay valid for CFMs that stratify internally (CausalPFN's weak learner) is untested.

## Direction 4: A full failure taxonomy for CFMs

### Takeaway
**Crowded piecemeal, open as a unified user-side decision table.** Nearly every axis now has at least one 2026 paper, but none tells a user which failure applies to their dataset. Feasibility on T4: acceptable only if restricted to 2-3 axes. A full grid is too large.

### Cited Findings

| Failure axis | Verified evidence | Source and tag |
|---|---|---|
| Poor overlap | Under weak overlap, raw FSP's V̂/V was .328 with native coverage .706 versus oracle-variance coverage .998. IHDP overlap problems undercut guarantees for debiased estimators | [Zhang 2026](https://arxiv.org/abs/2609.26290) [P-read]; [Melnychuk 2026](https://arxiv.org/html/2603.12037v3) [P-fetch] |
| Shift from training prior | CausalPFN is "reliably calibrated" in distribution but "severely overconfident" out of distribution; temperature scaling is the proposed fix. "Prior uncoverage" causes unavoidable bias | [Balazadeh 2025](https://arxiv.org/html/2506.07918v2) [P-fetch]; [Wang 2026](https://icml.cc/virtual/2026/poster/63252) [S] |
| Small n | CausalPFN coverage 54.3% / 67.6% even at n = 1000 on binary outcome scenarios | [Mourao 2026](https://arxiv.org/abs/2603.15928) [P-fetch] |
| Large n, context limit | "Performance degradation is evident on the largest marketing tables". TabCF does not necessarily improve with n due to the context window | [Balazadeh 2025](https://arxiv.org/html/2506.07918v2) [P-fetch]; [Chen et al. 2026, TabCF](https://arxiv.org/abs/2605.05993) [S] |
| High dimensionality | CausalPFN code path uses `TruncatedSVD` to fit the feature limit. TabPFN limit is about 10,000 rows and 500 features | [code](https://github.com/vdblm/CausalPFN/blob/b7ed2f1e1d58a83c608d08ced3dee955f0a7c221/src/causalpfn/causal_estimator.py) [P-read]; [Neunhoeffer 2026](https://www.marcel-neunhoeffer.com/pdf/papers/neunhoeffer_learning-from-small-data.pdf) [P-read] |
| Outcome type | Binary-outcome coverage failure above. Do-PFN's published domain is continuous input and output | [Mourao 2026](https://arxiv.org/abs/2603.15928) [P-fetch]; [Zhang 2026](https://arxiv.org/abs/2609.26290) [P-read] |
| Treatment type | CausalPFN: only binary implemented. Continuous treatments addressed separately | [Balazadeh 2025](https://arxiv.org/html/2506.07918v2) [P-fetch]; [Stith, Barath, Balazadeh, Cresswell, Krishnan 2026](https://arxiv.org/abs/2605.15133) [P-meta] |
| Unobserved confounding | CausalPFN assumes strong ignorability. Sensitivity via PFN; control function via TFM. Do-PFN described as non-identifiable | [Balazadeh 2025](https://arxiv.org/html/2506.07918v2) [P-fetch]; [Javurek, Frauen, Brockschmidt, Schweisthal, Feuerriegel 2026](https://arxiv.org/abs/2605.10590) [P-meta]; [TabCF](https://arxiv.org/abs/2605.05993) [S]; [Melnychuk 2026](https://arxiv.org/abs/2603.12037) [P-fetch] |
| Aggregation | ACIC 2016: calibrated full-sample interval covers in 8 of 40 datasets, uncalibrated 18 of 40. Six benchmarks: 53% | [Schulman 2026](https://arxiv.org/abs/2610.22770) [P-fetch] |
| Bad covariates | Post-treatment covariates in the query: Ham, Kim, Kim, Kim, Lee, "A structural view of query misspecification in causal foundation models", ICML 2026 workshop | [Stith 2026 reference list](https://arxiv.org/abs/2609.03003) [S] |
| Graph misspecification | Advantage of graph-aware models grows when assumption is violated | [Reuter et al. 2026](https://arxiv.org/abs/2602.14972) [S] |

- Stith et al.'s reliability section reviews Melnychuk, Mourao, Wang and Ham, and offers no taxonomy or user-side procedure. It also says it is unclear whether Mourao et al. calibrated CausalPFN before testing. [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003)
- Talupula and Sharma, "Temporal Causal Prior-Data Fitted Networks for Panel Data with Learned Reliability Signals", arXiv 2026, learn reliability signals (null, confounding, identifiability scores), described as heuristics rather than guarantees, for panel data and evaluated on synthetic data. This is the nearest "self-reporting" work; it flags rather than abstains. [P-fetch] — [arXiv 2606.20889](https://arxiv.org/abs/2606.20889)
- Zhang's Table 1 pairs assumptions with observable diagnostics, but for theorem conditions in a training-side framework. [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)

### Inferences
- **Adds:** a taxonomy on its own is a survey-style claim, and Stith et al. already partly occupy that space. Its publishable form is a decision table: *observable signal on the user's data → likely failure → action*. Limit it to effect or confounding direction, overlap, and context size versus n.
- **Work:** 3-5 person-weeks for even a restricted grid; full six-axis coverage is unrealistic on Colab. Better as a section than as the headline contribution.

### Gaps
- Queries: "benchmark causal foundation models CausalPFN Do-PFN comparison failure modes overlap covariate shift prior"; "CausalPFN shrinkage bias large treatment effects evaluation critique". Negative result: no unified failure taxonomy with user-side diagnostics found.
- A summarised line from Mourao et al. said CausalPFN is limited to binary *outcomes*, while the CausalPFN paper's stated limit is binary *treatments*. I did not resolve this by reading Mourao directly, so it is not used.

## Direction 5: Formal contribution (valid inference for the difference, TOST, anytime-valid)

### Takeaway
**Open but narrow.** I found no valid-inference result specifically for the difference between a black-box CFM and a cross-fitted AIPW on shared data, and no TOST framing. It adds rigour more than headline novelty, but the project needs part of it anyway because the current test and label do not match. Feasibility on T4: very good, little GPU needed. Requires someone comfortable with asymptotics.

### Cited Findings
- Hausman, "Specification Tests in Econometrics", Econometrica 46(6):1251-1271, 1978. Foundational: the simple variance-difference form depends on one estimator being efficient under the null, so that its covariance with the difference is zero. [P-meta for citation; S for the explanation] — [Econometric Society](https://www.econometricsociety.org/publications/econometrica/1978/11/01/specification-tests-econometrics), [explainer](https://casrai.org/guides/hausman-test-fixed-vs-random-effects)
- Hartman and Hidalgo, "An Equivalence Approach to Balance and Placebo Tests", American Journal of Political Science 62(4):1000-1013, 2018. Argues the usual null of no difference is wrong for placebo-type tests, and to use equivalence tests with substantive bounds. [S] — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/126115)
- TOST mechanics: equivalence can be read from a 100(1−2α)% CI lying inside the region; standard TOST can be liberal in finite samples. [S] — [PMC primer](https://pmc.ncbi.nlm.nih.gov/articles/PMC5856600/), [bioRxiv](https://www.biorxiv.org/content/10.1101/2023.03.11.532179.full.pdf)
- Dalal, Blöbaum, Kasiviswanathan, Ramdas, "Anytime-Valid Inference for Double/Debiased Machine Learning of Causal Parameters", arXiv 2024. Time-uniform DML under conditions slightly stronger than standard DML; no journal version confirmed. [P-meta] — [arXiv 2408.09598](https://arxiv.org/abs/2408.09598)
- Hussain, Oberst, Shih, Sontag, "Falsification before Extrapolation in Causal Effect Estimation", NeurIPS 2022. A test of agreement between estimators, comparing observational against RCT data. Different setting from shared data. [P-meta] — [arXiv 2209.13708](https://arxiv.org/abs/2209.13708)
- Cross-fitted AIPW can have substantial variance inflation in high dimensions ("A New Central Limit Theorem for the Augmented IPW Estimator"; authors not re-verified). [S] — [arXiv 2205.10198](https://arxiv.org/abs/2205.10198)
- Melnychuk et al.'s correction is an EIF-based term added to a PFN plug-in, and Zhang's "sampling response coefficient" is a relationship between a frozen estimator and P_n ψ. Neither is used as a hypothesis test. [P-fetch; P-read] — [arXiv 2603.12037](https://arxiv.org/abs/2603.12037), [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- The notebook uses only AIPW's SE in its z-statistic, and `fake_cfm` adds independent noise, so the positive control cannot reveal any error from CFM variance or shared-data covariance. [P-read] (local notebook)

### Inferences
- **Current weakness.** Var(AIPW − CFM) = V_A + V_C − 2Cov. Using V_A alone is conservative if the CFM tracks AIPW closely, and anti-conservative if the CFM is noisy and weakly correlated. Neither is detected by the current positive control.
- **Test/label mismatch.** `detector` tests gap > 0; `truly_shrunk` labels gap > 10%. At large n or large effects, the test will flag trivial gaps. A non-inferiority or TOST form fixes this directly: H0 "shrunk by more than 10%" versus "not". A margin relative to an estimated effect needs a delta-method or Fieller-type treatment.
- **Three concrete options, in order of preference. These are my proposals.**
  1. **Rectifier test.** Use the CFM's own μ̂₁, μ̂₀ in the AIPW correction. The AIPW minus plug-in difference is then the sample mean of the correction term, so it is a one-sample z-test with variance from its empirical variance, and CFM context drawn from other folds. This handles shared data by construction. CausalPFN's model class has `predict_cepo`, but the estimator-level method is private (`_predict_cepo`), so some light wrapping is needed. Requires a check of rate and stability conditions; Neunhoeffer notes convergence rates for PFNs are not yet proven.
  2. **Sample split.** CFM context from fold A, AIPW on fold B, so the variance is V_A + V_C. Simple, loses power.
  3. **Joint bootstrap** of both estimators. Feasible for B of about 100-200 given forward-pass cost. Caution: Shaw et al.'s duplicate-covariate problem also applies to propensity models under bootstrap resampling.
- **Anytime-valid:** skip, or leave as a remark. It is only useful when data truly arrive sequentially, and that is not the use case. It would add theory cost with little payoff.
- **Adds:** a small proposition with a simulated coverage study, plus a margin-based verdict: "shrunk by more than 10%" or "demonstrably not". **Work:** about 2-3 person-weeks.

### Gaps
- Negative result: no paper on TOST or equivalence tests between a black-box causal estimator and AIPW; no Hausman-with-DML on shared data found. Queries: "equivalence test two one-sided TOST causal estimator agreement doubly robust benchmark black-box estimator"; "Hausman test double machine learning difference between two estimators cross-fitting variance overlapping data".
- The rectifier variance claim is my derivation and is not checked against a published theorem.

## Direction 6: Multi-model evaluation

### Takeaway
**Crowded as a benchmark, open for this specific diagnostic.** Three 2026 preprints already compare CausalPFN, Do-PFN and CausalFM with classical methods, but none applies a common shrinkage test across effect size and confounding direction. Public data already suggests that shrinkage is not CFM-specific. Feasibility on T4: good, because wrappers exist.

### Cited Findings
- Stith et al. 2026: tests CausalPFN, Do-PFN, CausalFM against T/S/X/DR learners, Debiased ML, IPW. Median CATE runtimes on matched CPU: 18.4 s, 115.1 s, 31.2 s. GPU results and full CSVs are released, with Colab notebooks. [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003), [repo](https://github.com/layer6ai-labs/cfms)
- From my CSV calculation (see cross-cutting section): near-zero ratios on Lalonde-CPS occur for S-, X- and DR-learners as well as Do-PFN and CausalFM, but not for T-learner, IPW, Debiased ML or CausalPFN. [P-read] — [data](https://github.com/layer6ai-labs/cfms/tree/main/data)
- GPU median total runtimes from that CSV: CausalPFN about 8.9 s (CPS) and 1.9 s (PSID); Do-PFN 6.6 s and 1.4 s; CausalFM 3.2 s and 0.2 s. [P-read] — [data](https://github.com/layer6ai-labs/cfms/tree/main/data)
- Jung et al. 2026: CausalPFN, Do-PFN, CausalFM versus Causal Tree, TARNet, GRF/Causal Forest, CFRNet, ForestDRIV, KIV, with TabPFN modular estimators. TabPFN modular approaches are competitive; no estimator wins everywhere. [P-fetch] — [arXiv 2609.36881](https://arxiv.org/abs/2609.36881)
- Zhang 2026 includes CausalPFN-S, S/T/X/DR learners, AIPW/DML and Do-PFN, flagged as out-of-domain. Response slopes at n = 256 on a separate grid: FSP .819, S-learner .951, AIPW .988, DML 1.008. [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- Melnychuk et al. test TabPFN, CausalPFN, CausalFM, and exclude Do-PFN. [P-fetch] — [arXiv 2603.12037](https://arxiv.org/abs/2603.12037)
- Conflict on Do-PFN's validity: Do-PFN's own paper reports accurate estimates without a causal graph, [P-meta] — [NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ff997469ac66cf893c4183efeb22212a-Abstract-Conference.html); Melnychuk et al. call it non-identifiable and exclude it, [P-fetch] — [arXiv 2603.12037](https://arxiv.org/abs/2603.12037); Stith et al. find ATE relative error near 1, [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003).
- Reuter, Dhir, Diaconu, Robertson, Ossen, Hutter, Weller, van der Wilk, Schölkopf, "Use What You Know: Causal Foundation Models with Partial Graphs", ICML 2026. [P-meta] — [arXiv 2602.14972](https://arxiv.org/abs/2602.14972)
- Panagopoulos 2026 uses TARNet, CFR, DragonNet, Causal Forest but no CFMs. [P-fetch] — [arXiv 2605.10430](https://arxiv.org/abs/2605.10430)

### Inferences
- **Answer to "is shrinkage CFM-specific?":** on current public evidence, no. It looks model- and architecture-specific rather than class-specific. The grid needs extending beyond one semi-synthetic family before this becomes a claim.
- **Adds:** a reproducible "attenuation profile" per estimator, and a mechanism test. **A sharp and cheap experiment, my proposal:** apply per-arm outcome standardisation around Do-PFN and CausalFM and see if toward-zero attenuation drops, and whether bias toward the naive contrast rises. Same in reverse by disabling it in CausalPFN (more invasive). I found no paper isolating this.
- **Work:** about 1-2 person-weeks using the `cfms` wrappers. Three CFMs and AIPW, T/S/X/DR and causal forest are fine. Dragonnet and TARNet need per-dataset training, so restrict their grid. Do not re-run the FLAML metalearner benchmark: the README puts a full run at about 105 CPU-hours. Use default learners instead, and disclose it.

### Gaps
- Negative result: no paper tests Dragonnet alongside CFMs on a shrinkage metric. "Dragonnet" appears in Zhang only as related work.
- Do-PFN and CausalFM on Colab T4 were not tested by me; the `cfms` README claims zero-setup Colab notebooks. Do-PFN and CausalFM require separate repo clones.
- X-learner and DR-learner shrinkage in the CSV is unexplained and may reflect tuning or heavy-tailed outcomes. Check before leaning on it.

## Direction 7: Practical application or real-case audit

### Takeaway
**Open, but thin.** I found no independent clinical or policy deployment of a CFM. Published real-data uses are mostly benchmark-style. An audit here adds external credibility rather than method novelty. Feasibility: good, with public data.

### Cited Findings
- Marketing: CausalPFN's repo ships a Hillstrom uplift notebook and a Colab for reducing A/B testing cost. The paper's real-data evaluation uses Hillstrom, Lenta, Retail Hero (X5), Megafon and Criteo, via scikit-uplift and Qini scores, with 50k subsamples on the largest. [P-read for README; P-fetch for paper] — [repo](https://github.com/vdblm/CausalPFN/), [arXiv 2506.07918](https://arxiv.org/html/2506.07918v2)
- Policy: Melnychuk et al.'s Appendix G analyses strict COVID-19 lockdowns (Banholzer et al. 2021 data, n = 264, outcome weekly relative case growth), with TabPFN- and CausalPFN-based estimators and A-IPTW. Estimators agree on a negative ATE but differ in location and spread; MP-OSPC aligns most closely with A-IPTW. This is the only real observational policy application I found, and it is by the authors. [P-fetch] — [arXiv 2603.12037](https://arxiv.org/html/2603.12037v3)
- Clinical: Mourao et al. is an independent evaluation built from Indomethacin (n = 570, true ATE −0.062) and Rotterdam (n = 2260, true ATE −0.101), simulated at n = 200, 500, 1000. Unfavourable to CausalPFN. It is a simulation, not a deployment. [P-fetch] — [arXiv 2603.15928](https://arxiv.org/abs/2603.15928)
- Trials used as tests: NSW (Dehejia-Wahba experimental sample, 185 treated and 260 control) and Gerber et al. social pressure turnout, in Zhang. [P-read] — [arXiv 2609.26290](https://arxiv.org/abs/2609.26290)
- ACTG 175, Pennsylvania Reemployment Bonus, Illinois UI pre-treatment outcomes, in Jung et al. [P-fetch] — [arXiv 2609.36881](https://arxiv.org/abs/2609.36881)
- Gentzel, Pruthi, Jensen, "How and Why to Use Experimental Data to Evaluate Methods for Observational Causal Inference", ICML 2021 (PMLR 139:3660-3671). Observational sampling from RCTs (OSRCT) gives real-outcome datasets with induced confounding and known effects. Foundational. [S] — [PMLR](https://proceedings.mlr.press/v139/gentzel21a.html)
- Kleper and Melamed, "Benchmarking foundation models for improving confounding control in target trial emulation", medRxiv, May 2026: emulated active-comparator trials with real confounding by indication, to avoid semi-simulated data. No hits in its text for CausalPFN, TabPFN, negative control or injection, so it refers to other foundation models. [P-read] — [medRxiv](https://www.medrxiv.org/content/10.64898/2026.05.09.26352820v1.full.pdf)
- Domain extensions exist outside tabular effect estimation (MapPFN and PerturbPFN for perturbation; SIC, SurvivalPFN, SurvPFN for survival), per Stith et al. Not audited here. [S] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003)

### Inferences
- **Best audit design, my suggestion:** OSRCT on Hillstrom and NSW. Real outcomes and covariates, known confounding direction chosen by you, RCT-estimated reference, and easy flipping of confounding sign. This directly tests the cross-cutting hypothesis on real data. Note: 64k rows must fit `max_context_length` 4096, so CausalPFN's context handling is itself under test.
- **Adds:** "on real outcomes with known RCT reference, the detector or adjustment fraction identifies the same direction of failure". It is a validation claim, not a method claim. **Work:** about 1 person-week. Data available through scikit-uplift (as used by CausalPFN).
- The lockdown dataset is attractive because published estimates exist, but it has no ground truth, and n = 264 means low power for a detector.

### Gaps
- "TACO: TabPFN Augmented Causal Outcomes for Early Detection of Long COVID" (medRxiv 2025) appeared in search but the fetch returned 403. Insufficient publicly verifiable evidence on whether it estimates causal effects.
- Negative result: no independent real-world deployment found, no OSRCT use with CFMs found. Queries: "CausalPFN real-world application case study clinical OR marketing OR policy applied"; "causal foundation model treatment effect electronic health records real-world evidence TabPFN target trial emulation 2026"; "OSRCT observational sampling from randomized controlled trials evaluate CausalPFN OR causal foundation model OR TabPFN". Absence from search is not proof of absence, especially for industry use.

## Direction 8: Trust layer or agentic guardrail

### Takeaway
**Mostly trend-chasing as a primary claim.** I found no agent that calls a CFM, so a CFM guardrail has no current user to protect. Causal agents already include generic validation loops, and benchmarks already test abstention. Feasibility is fine for a wrapper, and weak for a credible evaluation.

### Cited Findings
- Acharya, Shrestha, Emmerson, Verma, Bhardwaj, Simko, Pandey, Haghighat, Yang, Janzing, Sachan, Schölkopf, Jin, "Causal AI Scientist: Towards End-to-End Causal Inference with Large Language Models", ICML 2026 workshop poster (AI as a Tool for Mathematics, Computer Science, and Machine Learning). Uses a decision tree and a "validation feedback loop that performs post-selection empirical diagnostics". Evaluated on CauSciBench. No mention of CFMs on the page. [P-fetch] — [ICML](https://icml.cc/virtual/2026/74805); earlier NeurIPS 2025 workshop [listing](https://neurips.cc/virtual/2025/124113); [repo](https://github.com/causalNLP/causal-agent) [S]
- Wang, Zhou, Wu, Singh, Nan, Jin, Philip, Patnaik, Zhu, Singh, Prashant, Shen, Huang, "Causal-Copilot: An Autonomous Causal Analysis Agent", arXiv 2025. Knowledge-backed algorithm selection; evaluation focused on discovery with synthetic graphs. [S] — [arXiv 2504.13263](https://arxiv.org/abs/2504.13263)
- Leban, Saarinen, Sun, "CausalDS: Benchmarking Causal Reasoning in Data-Science Agents", arXiv Jul 2026 (v2 Oct). "Abstention is tested directly": for unidentified targets, the graded answer is to abstain. Its full text has no hits for CausalPFN, TabPFN, or foundation model. [P-read] — [arXiv 2607.08093](https://arxiv.org/abs/2607.08093)
- Han, Kuang, Zhao, Ye, Wu, "Causal Agent based on Large Language Model", arXiv 2024 (v3 Aug 2026). Tools include causal-learn and EconML, per search. [P-fetch for metadata; S for tools] — [arXiv 2408.06849](https://arxiv.org/abs/2408.06849)
- Tan and Syrgkanis, "CausalSmith: A Formally Grounded, Self-Improving Agentic Framework for Automated Research in Causal Inference", arXiv 2026. [P-meta] — [arXiv 2607.22511](https://arxiv.org/abs/2607.22511)
- Singh et al., "CausalGuard: Conformal Inference under Graph Uncertainty", arXiv 2026. The LLM only supplies an edge prior; not an agent and no CFM mentioned. "Guard" refers to statistical validity. [P-fetch] — [arXiv 2605.21928](https://arxiv.org/abs/2605.21928)
- Bazgir, Habibdoust, Zhang, Song, "Causal MAS: A Survey of Large Language Model Architectures for Discovery and Effect Estimation", arXiv 2025. [P-fetch] — [arXiv 2509.00987](https://arxiv.org/abs/2509.00987)
- Lee, Lin, Ku, Hsu, Huang, Wu, Kang, "LLM-based Agents for Automated Confounder Discovery and Subgroup Analysis in Causal Inference", arXiv 2025. [P-meta] — [arXiv 2508.07221](https://arxiv.org/abs/2508.07221)
- Stith et al. suggest a future interface that lets the analyst specify estimand and assumptions and report whether the estimand is identified. This is a human interface, not an agent. [P-read] — [arXiv 2609.03003](https://arxiv.org/abs/2609.03003)

### Inferences
- **The real niche is small:** a CFM's speed makes it a natural agent tool, and CFM errors can have tiny uncertainty (Stith et al.), so a silent wrong answer is plausible. But this is an argument for the future, not an observed problem.
- **Adds:** a claim like "guardrail improves agent outcomes" would first require building the integrated pipeline and an evaluation. High effort, with LLM API costs, for a weak claim, and exposed to overlap from any team that adds a similar check.
- **Recommendation:** return a machine-readable verdict (`trust` / `abstain` / `fallback_to_AIPW`) from the diagnostic and mention agent use as future work. **Work:** a couple of days for the verdict; 3+ person-weeks for a real evaluation.

### Gaps
- Negative result: no agent found that calls CausalPFN, Do-PFN or a TabPFN-based causal estimator, and no CFM-specific guardrail. Queries: "LLM agent causal inference pipeline guardrails Causal-Copilot Causal AI Scientist benchmark"; "Causal AI Scientist LLM causal data science agent refutation validation tools 2026"; "LLM agent uses CausalPFN OR TabPFN tool causal effect estimation agent foundation model pipeline". Search-level result only; repos were not code-searched.
- CAIS's specific diagnostics were not read in full.

## Overall: which extensions best raise novelty?

### Takeaway
Reposition from "a shrinkage detector" to **"a reference-free metamorphic audit for CFMs"**: Directions 2 and 3 are the novelty core, Direction 5 gives it statistical validity, and Directions 6 and 7 validate it. Avoid leading with Directions 1, 4 or 8.

### Cited Findings
Directions and evidence are cited in the sections above. Status judgements below are mine.

| Direction | Status | Novelty gain | Work (my judgement) | Decision |
|---|---|---|---|---|
| 2. Metamorphic tests | Open, with vacuous-relation trap | High | 1-2 person-weeks | **Core** |
| 3. Planted-effect self-test | Mature in OHDSI, open for CFMs | High | About 1 person-week | **Core** |
| 5. Formal inference and margin | Open, narrow | Medium, and needed anyway | 2-3 person-weeks | **Include, rectifier + margin only** |
| 6. Multi-model | Crowded benchmark, open diagnostic | Medium | 1-2 person-weeks | **Include, for validation and mechanism** |
| 7. Real-data audit | Thin | Low to medium | About 1 person-week | **Include, OSRCT demo** |
| 1. Detect-then-repair | Crowded | Low, unless pretest result is striking | 1-2 person-weeks | **One comparison only** |
| 4. Full taxonomy | Crowded piecemeal | Low to medium | 3-5 person-weeks | **Restrict to 2-3 axes** |
| 8. Agent guardrail | Weak niche | Low | 3+ person-weeks | **Future-work line only** |

### Inferences
Candidate publishable claims, all **hypotheses until run**:
1. Constant planted effects are essentially uninformative for per-arm-standardising CFMs, so the obvious self-test gives false reassurance.
2. Covariate-dependent injection gives a reference-free adjustment fraction that tracks prior-induced confounding bias on the user's own data.
3. Attenuation toward zero is tied to outcome handling, not to being a CFM. Non-CFM learners show it, and CausalPFN largely does not.
4. Per-arm standardisation trades toward-zero shrinkage for pull toward the naive contrast.
5. A margin-based rectifier test gives valid verdicts on "shrunk by more than 10%", while the current z-test does not align with that label.
6. Not being flagged does not imply valid coverage.

Suggested first steps, in order, each cheap:
1. Flip the confounding sign in the existing notebook and re-run the effects 1, 2, 4. This is the fastest test of the reframing hypothesis, and if it fails, claims 1-4 need revisiting.
2. Run the relation table once on one dataset each for CausalPFN and Do-PFN.
3. Only then commit to the revised objective.

Suggested revised objective, subject to step 1: "A reference-free metamorphic audit for causal foundation models that combines covariate-dependent planted effects with an AIPW rectifier test and a non-inferiority margin, identifies each model's attenuation anchor, and is validated on CausalPFN, Do-PFN, CausalFM and classical comparators on simulated data and on observational samples drawn from RCTs."

### Gaps
- **Search coverage limits.** Semantic Scholar was not queried. arXiv API returned HTTP 429 after a few queries and on retries, so all negative claims rest on web search plus reading the most relevant papers. They mean "not found", not "does not exist".
- **Unread portions.** Long fetches were truncated. Jung et al. (first 100k of about 215k characters) and Schulman et al. (first 100k of about 138k) were not fully read, and Stith et al., Zhang, Neunhoeffer and CausalDS were read by targeted sections rather than end to end. Some competing claims could sit in unread appendices.
- **Primary not retrieved.** Rousseeuw and Leroy (1987), Schuemie 2014 and PNAS 2018 full texts, and the Phil. Trans. 2018 paper were verified only via citations and excerpts.
- **Mourao author list.** The fetched abstract page summary mentioned 21 additional authors; arXiv API and Stith et al.'s reference list both give seven. I used seven.
- **Pace of the field.** All of this needs re-checking before submission.
