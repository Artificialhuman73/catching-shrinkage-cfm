# Causal foundation models and amortized causal estimators: documented failures, biases and shrinkage (2024 to 31 Oct 2026)

Evidence tags used on every claim:
- **[P]** verified by me from the primary source: paper full text, official page, or repository code
- **[S]** secondary: reported by another paper or an index, not checked at the origin
- **[I]** my inference (these sit in the Inferences subsections)

Similarity percentages estimate overlap with the objective (model-agnostic runtime detector of shrinkage in CFMs, cross-fitted AIPW reference, one-sided z-test, abstention under poor overlap, positive control in simulation). **They are my judgement, not a measured quantity.**

Status note: most 2026 papers below are arXiv preprints without peer review unless a venue is given.

## Q1. What are the main CFMs and amortized causal estimators, and what priors and normalisation do they use?

### Takeaway
The core CFMs are CausalPFN, Do-PFN and CausalFM, with precursors CInA, CaML and BBCI, and a fast-growing 2026 family around them. No published source gives the distribution of true effect sizes in the CausalPFN prior. The repository shows that CausalPFN z-standardises outcomes **separately per treatment arm**, while Do-PFN and CausalFM use a single outcome scaling. This looks like the most decision-relevant technical fact for the objective.

### Cited Findings

**Catalogue of models and closest work.** All titles and authors are [P] from arXiv, the proceedings page, or the official conference page unless marked. "Sim." is my judgement.

| Paper (exact title) | Authors | Venue, year | ID / URL | What it does | Sim. |
|---|---|---|---|---|---|
| Learning to Fluctuate: Statistical Foundations for Causal Tabular Pretraining | Zhiheng Zhang | arXiv preprint, Sep 2026 (v2) | [2609.26290](https://arxiv.org/abs/2609.26290) | Argues latent-effect supervision "rewards posterior shrinkage"; trains on ATE plus influence-function fluctuation labels. Training-time fix, no runtime test. | 35% |
| Frequentist Consistency of Prior-Data Fitted Networks for Causal Inference | V. Melnychuk, V. Balazadeh, S. Feuerriegel, R. G. Krishnan | ICML 2026 (arXiv journal-ref), v3 Jul 2026 | [2603.12037](https://arxiv.org/abs/2603.12037) | Names prior-induced confounding bias; corrects it post hoc with a one-step posterior correction, compared against A-IPTW. Correction, not a test. | 30% |
| Causal Foundation Models | Christopher Stith, Hossein Rahmani, Jesse C. Cresswell | arXiv tutorial/review, Sep 2026 | [2609.03003](https://arxiv.org/abs/2609.03003) | Review plus Lalonde benchmark; reports Do-PFN and CausalFM shrinkage; calls for automatic prior-mismatch detection but proposes none. | 25% |
| Temporal Causal Prior-Data Fitted Networks for Panel Data with Learned Reliability Signals (TCPFN) | Shravan Talupula, Saurabh Sharma | arXiv, Jun 2026 | [2606.20889](https://arxiv.org/abs/2606.20889) | Built-in "Causal Judgment Head" predicting null-effect probability, identifiability and related signals. Not model-agnostic, no reference estimator, temporal setting. | 25% |
| "Estimating Causal Effects from Tabular Data with Assumption Gates and Automated Estimator Selection" for Trustworthy Artificial Intelligence (title as returned by Semantic Scholar) | Alessandro Berti | Electronics (MDPI), 2026 | [DOI 10.3390/electronics15194397](https://doi.org/10.3390/electronics15194397) | Abstract only: returns an estimate with diagnostics or a "reasoned refusal"; a pretrained neural router is the baseline. Full text blocked to me. | 25% (abstract only) |
| Causal Foundation Models Perform Better without Post-treatment Variables; A Structural View of Query Misspecification in Causal Foundation Models | Junha Ham, Deokgyu Kim, Doeun Kim, Serjin Kim, Sanghack Lee | ICML 2026 workshops (FMSD; SPIGM) | [71511](https://icml.cc/virtual/2026/71511), [74345](https://icml.cc/virtual/2026/74345) | TC-LD: a pre-inference filter for post-treatment covariates. A runtime check on inputs for a different failure. | 20% |
| Prior-Data Fitted Networks for Causal Inference: a Simulation Study with Real-World Scenarios | F. Mourao, D. Hajage, D. Bystrova, B. Bouvarel, N. Lapidus, F. Carrat, B. Glemain | arXiv, Mar 2026 (v2 Apr) | [2603.15928](https://arxiv.org/abs/2603.15928) | Independent clinical simulation: CausalPFN biased with poor coverage. | 20% |
| Unit-level aggregation breaks coverage in causal foundation models | Gabe Schulman, Lucius E. J. Bynum, Yoav Wald | arXiv, Oct 2026 | [2610.22770](https://arxiv.org/abs/2610.22770) | Shows ATE and subset intervals undercover due to independent aggregation; fixes with neural process heads. | 20% |
| Debiased Prior-Data Fitted Networks for Amortized Bayesian Semi-Parametric Inference | V. Melnychuk, E. Javurek, S. Feuerriegel | arXiv, Oct 2026 | [2610.28314](https://arxiv.org/abs/2610.28314) | EIF-based label and prior corrections during training. | 15% |
| Unveiling Prior-Data Fitted Networks on Causal Effect Estimation: Pre-Training or Fine-Tuning? | H. Wang, X. Lv, H. Zou, Y. Xiao, S. Gu, Y. Shi, Y. Mao, Y. Zhang, M. Geng, S. Yang, H. Li, W. Yang, P. Cui, Z. Lin | ICML 2026 | [poster 63252](https://icml.cc/virtual/2026/poster/63252) | "Prior uncoverage" causes bias; proposes fine-tuning. Abstract read only. | 15% |
| What You Observe Determines How You Identify Causal Effects: Evaluating Causal Models across Observational Views | H. Jung, G. Seo, H. Byun, J. Lee, K. Song | arXiv, Sep 2026 | [2609.36881](https://arxiv.org/abs/2609.36881) | CausalIDView benchmark, including doubling the true effect. | 15% |
| CausalPFN: Amortized Causal Effect Estimation via In-Context Learning | V. Balazadeh, H. Kamkari, V. Thomas, B. Li, J. Ma, J. C. Cresswell, R. G. Krishnan | NeurIPS 2025 (Spotlight [S]) | [2506.07918](https://arxiv.org/abs/2506.07918), [proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/e3d3db07c1bfb63e1d0b998996de1d12-Abstract-Conference.html) | Target model. Observational temperature calibration is the nearest built-in runtime check, and it addresses intervals, not bias. | 15% |
| Do-PFN: In-Context Learning for Causal Effect Estimation | J. Robertson, A. Reuter, S. Guo, N. Hollmann, F. Hutter, B. Schölkopf | NeurIPS 2025 | [2506.06039](https://arxiv.org/abs/2506.06039), [proceedings](https://papers.nips.cc/paper_files/paper/2025/hash/ff997469ac66cf893c4183efeb22212a-Abstract-Conference.html) | Predicts conditional interventional distributions; prior over SCMs. | 10% |
| Foundation Models for Causal Inference via Prior-Data Fitted Networks (CausalFM) | Y. Ma, D. Frauen, E. Javurek, S. Feuerriegel | ICLR 2026 [S] | [2506.10914](https://arxiv.org/abs/2506.10914) | Identifiability-aware priors; back-door, front-door, IV. | 5% |
| Market Impact Estimation via Causal Foundation Models | Dennis Thumm, Ying Chen | ICAIF 2026 | [2610.12537](https://arxiv.org/abs/2610.12537) | Proof of concept with transfer failures reported. | 5% |
| Can Tabular Foundation Models Amortize Statistical Inference? (TabCon) | K. Ye, S. Gong, H. Zhou, V. Zangirolami, C. Shi | arXiv, Sep 2026 | [2609.33114](https://arxiv.org/abs/2609.33114) | Amortized confidence intervals. Not a causal diagnostic. | 5% |
| How Well Do Prior-Data Fitted Networks Amortize Bayesian Inference? | M. Hülskamp, J. Kobialka, E. Sommer, T. Nagler, D. Rügamer | arXiv, Oct 2026 | [2610.13764](https://arxiv.org/abs/2610.13764) | Amortization error persists in rare prior settings. Not causal. | 5% |
| When and Why LLM Causal Priors Help: Closed-Loop Prior Selection for Amortized Causal Inference | Haohao Zhou | arXiv, Sep 2026 | [2609.06941](https://arxiv.org/abs/2609.06941) | Prior selection; finds synthetic diagnostics can mislead. | 5% |
| Towards Causal Foundation Model: on Duality between Causal Inference and Attention (CInA) | J. Zhang, J. Jennings, A. Hilmkil, N. Pawlowski, C. Zhang, C. Ma | ICML 2024 [S], published title differs ("...between Optimal Balancing and Attention") | [2310.00809](https://arxiv.org/abs/2310.00809) | Self-supervised covariate balancing across unlabeled datasets. | <5% |
| ACTIVA: Amortized Causal Effect Estimation via Variational Autoencoders | A. Sauter, S. Salehkaleybar, F. van Harmelen, A. Plaat, E. Acar | arXiv v4; venue unverified | [2503.01290](https://arxiv.org/abs/2503.01290) | Conditional VAE for interventional distributions. | <5% |
| Black Box Causal Inference: Effect Estimation via Meta Prediction (BBCI) | L. E. J. Bynum, A. M. Puli, D. Herrero-Quevedo, N. Nguyen, C. Fernandez-Granda, K. Cho, R. Ranganath | arXiv 2025; venue unverified | [2503.05985](https://arxiv.org/abs/2503.05985) | Meta-prediction of estimands from synthetic SCMs. Title and authors verified; the description is [S] from the Stith review. | <5% |
| Zero-shot causal learning (CaML) | H. Nilforoshan, M. Moor, Y. Roohani, Y. Chen, A. Šurina, M. Yasunaga, S. Oblak, J. Leskovec | NeurIPS 2023 [S] (foundational) | [2301.12292](https://arxiv.org/abs/2301.12292) | Meta-learning for CATE of unseen treatments. | <5% |
| Amortized Inference of Causal Models via Conditional Fixed-Point Iterations | D. Mahajan, J. Gladrow, A. Hilmkil, C. Zhang, M. Scetbon | TMLR 2025; ICLR 2026 J2C | [2410.06128](https://arxiv.org/abs/2410.06128) | Amortized causal models. Metadata only. | <5% |

**Extensions, metadata checked, not read for this question** (all <5% judged):
- [A Causal Foundation Model for Structure and Outcome Prediction](https://arxiv.org/abs/2606.26467) (TabPFN-CFM; Zhu et al., ICML 2026 workshop)
- [Causal Foundation Models with Continuous Treatments](https://arxiv.org/abs/2605.15133) (CCPFN; Stith et al.)
- [Use What You Know](https://arxiv.org/abs/2602.14972) (Reuter et al., ICML 2026)
- [IV-ICL](https://arxiv.org/abs/2605.12924) (Balazadeh et al.)
- [Amortizing Causal Sensitivity Analysis](https://arxiv.org/abs/2605.10590) (Javurek et al.)
- [Foundation Models for Partial Causal Identification](https://arxiv.org/abs/2608.20841) (Bellot and Dhir)
- [CausalLongPFN](https://arxiv.org/abs/2606.05797) (Zare et al.)
- [MOCA](https://arxiv.org/abs/2604.23107) (Wang and Ghosh)
- [CIDER-FM](https://arxiv.org/abs/2609.39523) (Gao et al.)
- [ProximalFM](https://arxiv.org/abs/2610.08078)

**CausalPFN prior and training data [P]:**
- Base tables come from [337 OpenML tables, totaling over 10^9 feature values](https://arxiv.org/html/2506.07918), or from synthetic tables made with the TabPFN v1 random-network generator.
- Each dataset picks [two random columns as raw mu_0 and mu_1; treatment comes from a random logit function](https://arxiv.org/html/2506.07918), so ignorability holds by construction.
- The [heterogeneity control gamma ~ Unif[0,1] sets tau = gamma*tau_raw + (1-gamma)*lambda_raw and preserves the ATE](https://arxiv.org/html/2506.07918). So the ATE is simply whatever the difference of two random columns averages to. There is no explicit effect-size prior.
- [Noise is Gaussian with variance uniform on (0, var(mu_t)], times input-dependent scale columns](https://arxiv.org/html/2506.07918).
- [Propensities are RCT, linear or nonlinear logits, then mixed with a hard threshold by xi in [0,1] to create poor positivity](https://arxiv.org/html/2506.07918).
- The [output is a 1024-bin histogram over [-10, 10], rescaled to the outcome scale, with out-of-range values clipped; training uses context up to 16K in the predictive phase and 2,048 in the causal phase](https://arxiv.org/html/2506.07918). [Training covers up to 100 covariates and inference up to 50,000 samples](https://arxiv.org/html/2506.07918).

**Distribution of true effect sizes in the CausalPFN prior: Insufficient publicly verifiable evidence.**
- The paper reports no such distribution, and the [repository tree](https://github.com/vdblm/CausalPFN) contains no prior generator or training script (checked 31 Oct 2026) [P].
- The closest public measurement is the [prior_bias_check/CausalPFN.ipynb notebook in the Melnychuk repo](https://github.com/Valentyn1997/freq-cons-pfns/blob/HEAD/prior_bias_check/CausalPFN.ipynb). It computes standardised ATEs but only reports confounding Delta = ATE minus difference in means, per Y SD, on 512 datasets: mean |Delta| = 0.041, 0.037 and 0.031 for 5, 50 and 100 covariates, with the plotted density sharply peaked at 0 (values with |Delta| >= 5 dropped first) [P].
- The sampled file is named `synthetic_backdoor_dgp_...pt` and is not in the repository. It is unclear whether it includes the OpenML part of the prior.

**How outcomes are normalised [P, code]:**
- **CausalPFN** z-standardises per arm. [`_get_y0_y1_shift_scale` computes separate mean and std for treated and control context](https://github.com/vdblm/CausalPFN/blob/main/src/causalpfn/models/icl_model.py), and `predict_cepo` returns `mean * y1_scale + y1_shift` for t=1 and `mean * y0_scale + y0_shift` for t=0. The same arm-wise transform applies to training targets in `cepo_losses`. The paper only says the interval is [scaled to match the outcomes](https://arxiv.org/html/2506.07918). Covariates are [normalised and clipped at 10 sigma](https://github.com/vdblm/CausalPFN/blob/main/src/causalpfn/models/model.py).
- **Do-PFN** uses one scaling: [`normalize_data(y_full, ...)` returns one `data_mean, data_std` over the context outcomes](https://github.com/jr2021/Do-PFN/blob/HEAD/scripts/transformer_prediction_interface/base.py).
- **CausalFM** uses one scaler in its data script: [`y_scaler` is fit on concatenated y0 and y1, and the ITE is recalculated in normalised space](https://github.com/yccm/CausalFM/blob/HEAD/DATA_standard/normalize_data.py). Inference-time normalisation in the toolkit was not checked.
- The Stith benchmark additionally [standardises X and Y globally before all three models and multiplies effects back by the outcome scale](https://github.com/layer6ai-labs/cfms/blob/main/causal_bench/wrap_foundation.py), with comments that raw scales are out of the priors' distribution.

**Other priors:**
- [Do-PFN trains on sampled SCMs including interventions; 7.3M parameters, v1 and v1.1 trained 48 and 96 hours; v1.1 graphs up to 60 nodes](https://arxiv.org/html/2506.06039) [P]. Its own authors say its prior has a [high probability of low-ATE datasets](https://arxiv.org/html/2506.06039) [P].
- [CausalFM uses causality-inspired Bayesian neural network priors by identification strategy](https://arxiv.org/abs/2506.10914) [P].
- [CInA uses multiple unlabeled datasets with covariate balancing as the self-supervised task](https://arxiv.org/abs/2310.00809) [P].
- [ACTIVA uses a transformer conditional VAE across training tasks, and its abstract notes that beyond the training distribution only a parametric shift of the simulator is tested](https://arxiv.org/abs/2503.01290) [P].

### Inferences
- [I, code-based, not empirically tested by me] CausalPFN's estimate decomposes as tau_hat(x) = (ybar1 - ybar0) + s1*m1(x) - s0*m0(x), with m in the network's standardised units. An uninformed network output therefore reproduces the **difference in means, not zero**.
- [I] Adding a constant c to all treated outcomes leaves the network input unchanged, so tau_hat moves exactly one-for-one. This is exact when each arm fits within `num_neighbours` (default 1024) so that context selection is inactive, and approximate above that, because the [gradient-boosting stratifier chooses neighbours](https://github.com/vdblm/CausalPFN/blob/main/src/causalpfn/causal_estimator.py). So **homogeneous additive large effects cannot produce shrinkage in CausalPFN at any effect size**.
- [I] This plausibly explains the project notebook's remark that CausalPFN ["barely shrank"](/Users/chiranthr/Documents/Projects/ADA_PROJECT/shrinkage_detector_round3_gpu.ipynb). With the notebook's tau = c(1 + 0.5*X4), the treated-arm SD scales with c, so the output still scales with c. I searched the corpus for this arm-wise explanation (terms: arm-wise, per-arm, within-arm and similar) and found no paper stating it.
- [I] A real cap exists on a different axis: each predicted CEPO is bounded to its arm mean plus or minus 10 arm SDs, since the bin centres span [-10, 10]. Saturation would come from extreme distance between an arm's mean and its CEPOs relative to that arm's SD, such as strong confounding, rather than from effect size as such.

### Gaps
- True effect-size distribution in the CausalPFN prior: not published. Reproducing it needs the unreleased generator or the author-supplied sample file.
- Whether Do-PFN's and CausalFM's single scaling causes their Lalonde shrinkage is untested in any source found.
- FoCAT and CausalEcon appear only as titles in [Semantic Scholar citation data](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.07918/citations). Insufficient publicly verifiable evidence (lookup rate-limited).

## Q2. Has anyone documented shrinkage, regularisation toward the prior, saturation, attenuation or poor extrapolation to large effects?

### Takeaway
Yes, and explicitly, mostly in 2026. However, the direct evidence of shrinkage toward zero concerns **Do-PFN, CausalFM and purpose-built latent-effect networks, not released CausalPFN**, for which the available evidence points the other way. The bias documented for CausalPFN is framed as prior-induced confounding bias (Melnychuk), which I read as a pull toward the unadjusted contrast rather than toward zero.

### Cited Findings
- **Stith et al. (Do-PFN, CausalFM) [P]:** ["All three CFMs receive identically standardized covariates and outcomes. Under this common treatment, CausalPFN recovers the population effect closely (ATE relative error 0.17 on Lalonde-CPS), while Do-PFN and CausalFM do not: both remain near a relative error of 1 on both cohorts (0.88 and 0.94), recovering only a small fraction of the true contrast. Their errors are moreover almost identical across the two cohorts and carry very small standard errors, which points to a systematic shrinkage of the predicted effect toward zero rather than to unstable estimation."](https://arxiv.org/html/2609.03003) The table gives [Do-PFN 0.88/0.89 and CausalFM 0.94/0.95 on CPS/PSID, over 10 seeds](https://arxiv.org/html/2609.03003). This is an inference from unsigned relative error. No signed errors are reported in the paper.
- **CausalPFN authors' head-to-head [P]:** [Do-PFN ATE relative error 0.57, 0.67, 0.87, 0.92 on IHDP, ACIC, CPS, PSID, versus CausalPFN 0.20, 0.05, 0.13, 0.22](https://arxiv.org/html/2506.07918). This agrees with Stith, though the authors have an obvious interest, and they do not use the word shrinkage.
- **Do-PFN authors on large ATEs [P]:** ["We do note, however, that Do-PFN's performance also seems to diverge in the largest ATE group. This result is likely explained by the high probability of low-ATE datasets in our prior, caused by the combination of additive noise and non-linearities with a squishing effect. This result highlights the need for future research in synthetic causal data-generation that creates strong treatment effects that persist across long causal chains."](https://arxiv.org/html/2506.06039) **Internal tension:** the main text says this ablation shows Do-PFN ["is robust to different magnitudes of base rate ATE."](https://arxiv.org/html/2506.06039) This is the earliest statement I found (Jun 2025 onward) linking large-effect degradation to a low-effect prior.
- **Zhang, theoretical mechanism [P]:** latent-effect supervision ["rewards posterior shrinkage instead of directly encoding the repeated-sample response needed in a fixed deployment population."](https://arxiv.org/abs/2609.26290)
- **Zhang, measurements [P]:**
  - [Raw latent-effect attains lower RMSE at the prior centre (.0176 versus .0621) "by shrinking toward the training prior", with response slope .214; under effect shift its RMSE rises to .1364 and its slope becomes -.058](https://arxiv.org/html/2609.26290).
  - [As the effect rose from .025 to .15, coverage under latent-effect supervision fell from 1.000 to .112, versus .972 to .919 for FSP](https://arxiv.org/html/2609.26290).
  - These are the author's own ablation networks, not a released CFM.
- **Zhang's birthweight example is hypothetical, not a result [P]:** the -75 g versus -150 g example is introduced as ["Consider a hypothetical hospital"](https://arxiv.org/html/2609.26290). It must not be cited as measured attenuation.
- **Released CausalPFN under effect shift [P]:** in [Zhang's Table 3, CausalPFN-S has shifted slope 1.021 and RMSE .0695, and AIPW/DML has 1.026 and .0663](https://arxiv.org/html/2609.26290), on Bernoulli outcomes at n=256 with [effect shift of random sign times Uniform[0.13, 0.20]](https://arxiv.org/html/2609.26290). This is direct independent evidence of no attenuation, though at modest effect sizes. Do-PFN there is [out of its published domain](https://arxiv.org/html/2609.26290).
- **Residual attenuation in real randomised data, for FSP rather than CausalPFN [P]:** [National Supported Work post-treatment mean .0957 versus benchmark .1106; Gerber turnout biases -.0077 and -.0241](https://arxiv.org/html/2609.26290). Abstract: ["two randomized-study evaluations show that lower RMSE can coexist with residual attenuation."](https://arxiv.org/abs/2609.26290)
- **Melnychuk et al. on PFN priors generally [P]:** ["the PFN's implicit prior (which is learned from synthetic training distributions) can systematically shrink the degree of observed confounding toward zero"](https://arxiv.org/html/2603.12037), so [the ATE can stay biased as n grows](https://arxiv.org/html/2603.12037). Note the shrinkage target is **confounding**, not the effect. They also say [CausalPFN "may yield approximately debiased posteriors" for Delta in (-0.25, 0.25)](https://arxiv.org/html/2603.12037), and that its [posterior performance degrades with increasing sample size, noting training up to n about 2000](https://arxiv.org/html/2603.12037).
- **Jung et al., doubling the effect [P]:** under a [Move intervention giving tau^move(x) = 2*tau_0(x), Do-PFN "shows consistently large Move errors with poor tracking when the CATE itself changes"; CausalPFN instead "shows relatively large Stay errors"](https://arxiv.org/html/2609.36881), meaning its predictions change when the target does not. The intervention doubles a mediator-outcome response; it is not a sweep over effect sizes.
- **Thumm and Chen [P]:** [enriching the prior "suppressed the zero-shot do-head response roughly three- to eight-fold across the transfer tiers while fitting its own prior well", and "predictive fit does not certify the causal readout"](https://arxiv.org/html/2610.12537). Attenuation-like behaviour in a market PFN.
- **Wang et al. [P, abstract]:** ["prior uncoverage" leads to posterior inconsistency and estimation bias](https://icml.cc/virtual/2026/poster/63252).
- **Hülskamp et al. [P]:** [residual amortization error persists "especially in rare settings under the prior pretraining distribution"](https://arxiv.org/abs/2610.13764). Not causal, but large effects would be such a setting if the prior is low-effect.
- **Melnychuk, Javurek, Feuerriegel [P]:** [an idealized PFN's concentration rate can depend on nuisance rates and slow as the prior becomes more diverse](https://arxiv.org/abs/2610.28314).
- **Shrinkage is not unique to CFMs on Lalonde [P]:**
  - Tuned classical estimators also reach relative error near 1 on Lalonde CPS: [S-Learner 0.97, X-Learner 0.89, DR-Learner 0.89](https://arxiv.org/html/2609.03003) in Stith; [TarNet 1.00, BART 0.99, Forest DML 1.03, Forest DR 1.20](https://arxiv.org/html/2506.07918) in Balazadeh.
  - Mourão separately notes the known mechanism where [ML g-computation downweights treatment, "causing the estimated treatment effect to shrink toward zero"](https://arxiv.org/html/2603.15928).

### Inferences
- [I] The objective's premise, that CausalPFN shrinks large effects toward zero, has **no published support, and code plus Zhang's table argue against it**. The documented phenomenon is real but sits in Do-PFN, CausalFM and direct effect-supervised nets.
- [I] A natural **real positive control** therefore exists: Do-PFN or CausalFM on RealCause-Lalonde. A caveat comes from the classical rows above: the DR reference may itself fail there, and overlap abstention may trigger. That dataset would test abstention as much as detection.
- [I] Mourão's tables fit partial adjustment: [CausalPFN's mean error versus the crude contrast's (x 10^-3) is 30.89 vs 61.22 and 30.73 vs 59.91 in Indomethacin at n=500 and 1000, and 19.25 vs 104.4 and 19.68 vs 105.19 in Rotterdam](https://arxiv.org/html/2603.15928). Mourão does not interpret it this way.
- [I] CausalPFN's likely bias direction is toward the difference in means. A **one-sided toward-zero test can miss it** whenever the naive contrast is larger in magnitude than the truth. A regime with large true effect but near-zero naive contrast (masking confounding) should look like shrinkage and would be a sharper CausalPFN stress test.

### Gaps
- No source reports signed ATE error versus true effect size for CausalPFN across a wide sweep (for example, the 1 to 128 grid in the project notebook). I found no published CausalPFN test at effect sizes of many outcome SDs.
- Mourão's signed direction: the error definition is in Supplementary B, which was not in the HTML I read. Direction relative to zero is unverified.

## Q3. What do the CausalPFN and Do-PFN papers report about uncertainty, calibration and coverage?

### Takeaway
CausalPFN claims "finite-sample calibrated" intervals, but its evaluation concerns unit-level CATE intervals, and the ATE interval has since been shown to undercover badly, even after temperature calibration. Do-PFN claims it is "overall well calibrated" for per-unit interventional predictions and reports no ATE-level interval coverage.

### Cited Findings

**CausalPFN paper [P]:**
- Claim: [a "principled uncertainty quantification framework ... to produce finite-sample calibrated credible intervals"](https://arxiv.org/html/2506.07918). But its limitations section also says ["We lack finite-sample theory characterizing the estimator's behavior in practical settings."](https://arxiv.org/html/2506.07918)
- Evidence: ["CausalPFN is reliably calibrated under in-distribution settings but becomes severely overconfident when evaluated on OOD DGPs"](https://arxiv.org/html/2506.07918).
- Method: temperature on the softmax, tuned with regression coverage on observed y. The basis is empirical: ["Because we empirically observe ICE_mu <= ICE_tau across model-DGP pairs, temperature scaling that brings ICE_mu to zero guarantees that CATE intervals are calibrated or conservative. We fit the temperature by 5-fold calibration on the observational data"](https://arxiv.org/html/2506.07918). So the "guarantee" rests on an observed inequality, not on a proof given there.
- Large-scale model: ["generally appears conservative"; post-hoc calibration moves curves near the diagonal](https://arxiv.org/html/2506.07918). Figures 7 to 14 are titled and described as CATE calibration. I found no ATE coverage table.

**CausalPFN repository [P, code] ([causal_estimator.py](https://github.com/vdblm/CausalPFN/blob/main/src/causalpfn/causal_estimator.py)):**
- `calibrate: bool = False` by default, so **default intervals are uncalibrated**. `n_folds` defaults to 3 (the paper says 5-fold).
- `estimate_ate_CI` is on `CATEEstimator`, not `ATEEstimator`. It returns the point estimate from `estimate_ate(X)` and bounds from `_estimate_ate_cate_CI`.
- ATE draws are `samples_1.mean(axis=0) - samples_0.mean(axis=0)`, with samples drawn independently per unit.
- Point estimates use `prediction_temperature = 1.0`, so calibration changes intervals but not point estimates.
- The code minimises absolute coverage deviation, whereas the paper's ICE is a signed integral.
- [v0.1.5 (2026-09-27) fixed the CI output shape and made `estimate_ate_CI` return a deterministic point estimate](https://github.com/vdblm/CausalPFN/blob/main/CHANGELOG.md).
- Evaluator hazard: `ATEEstimator.estimate_ate` caches `mu_0, mu_1`, and `fit` does not reset them, matching the bug recorded in the [project notebook](/Users/chiranthr/Documents/Projects/ADA_PROJECT/shrinkage_detector_round3_gpu.ipynb).

**Independent findings on those intervals:**
- [Schulman et al. [P]: "temperature-calibrated 95% intervals from CausalPFN ... fall below nominal coverage beyond groups of 30 out of 4802 units, and intervals for the full-sample average contain the true value in only 20% of datasets"](https://arxiv.org/abs/2610.22770) (ACIC 2016).
- Mechanism: [posterior DGP uncertainty correlates unit errors, and independent aggregation understates variance by a factor growing with group size](https://arxiv.org/abs/2610.22770). They confirm from [CausalPFN's code that per-unit draws are independent](https://arxiv.org/html/2610.22770). Across six benchmarks, [neural process heads on frozen CausalPFN cover the full-sample average in 90% and 89% of 240 datasets, versus 53% for CausalPFN](https://arxiv.org/html/2610.22770).
- [Mourão et al. [P], 95% coverage on clinical simulations, n=200, 500, 1000: Indomethacin 76.3, 67.4, 54.3%; Rotterdam 67.1, 69.7, 67.6%. Bias-eliminated coverage stays below 85%](https://arxiv.org/html/2603.15928). Coverage worsens with n in Indomethacin while [mean error stays near 30 x 10^-3 (true ATE -0.062)](https://arxiv.org/html/2603.15928). They conclude [poor coverage is "due to both estimation bias and inadequate uncertainty quantification"](https://arxiv.org/abs/2603.15928). Used [causalpfn version 0.1.4](https://arxiv.org/html/2603.15928).
- **Calibration status of Mourão, resolved [P]:** Stith says it is [not clear whether they calibrated](https://arxiv.org/html/2609.03003). Their public [Indomethacin](https://github.com/franciscomourao/PFNs_Causal_Inference/blob/HEAD/CausalPFN/indomethacin_causalpfn.ipynb) and [Rotterdam](https://github.com/franciscomourao/PFNs_Causal_Inference/blob/HEAD/CausalPFN/rotterdam_causalpfn.ipynb) notebooks build `CATEEstimator(device=..., verbose=True)` and never mention calibration. So they ran **uncalibrated**, assuming the default was also False in v0.1.4 (I read the default in current main).
- [Melnychuk [P]: naive CausalPFN plug-ins versus MP-OSPC compared by distance to A-IPTW and by PIT-based calibration; MP-OSPC "does not substantially alter the results for CausalPFN" on ACIC 2016](https://arxiv.org/html/2603.12037), where confounding levels align with the prior. My reading: **this softens the failure picture on ACIC and differs in emphasis from Schulman**, although their metrics also differ.
- [Thumm and Chen [P]: "Interval calibration does not survive transfer"](https://arxiv.org/html/2610.12537).

**Do-PFN [P]:**
- [PICP curves "confirm that Do-PFN is overall well calibrated"; slightly under-confident for identifiable case studies; uncertainty rises correctly in the unidentifiable Unobserved Confounder case](https://arxiv.org/html/2506.06039). The authors attribute under-confidence to [bar-distribution discretization and an imperfectly minimized loss](https://arxiv.org/html/2506.06039). PICP here concerns the interventional outcome, which includes aleatoric noise.
- Separate decomposition of uncertainty: [aleatoric, unidentifiability, and epistemic over the Markov equivalence class](https://arxiv.org/html/2506.06039).
- Critique: [Do-PFN has no aggregate estimator according to Schulman](https://arxiv.org/html/2610.22770) and is [excluded by Melnychuk for its non-identifiable formulation, following Ma et al.](https://arxiv.org/html/2603.12037). The CausalPFN paper argues [its posterior cannot in general concentrate on the true effect, even with unlimited data](https://arxiv.org/html/2506.07918) (competing authors).

### Inferences
- [I] CausalPFN's built-in interval cannot serve as the detector's comparison statistic: it is uncalibrated by default, and it is too narrow for ATEs even when calibrated. This supports using an external reference such as AIPW.
- [I] Since calibration leaves the point estimate unchanged, a temperature-based check cannot flag or correct point-estimate shrinkage. This is a clean separation from the objective.
- [I] Mourão's stable mean error across n matches Melnychuk's non-vanishing prior-bias argument. Mourão's effects are small (ATE -0.062, -0.101), so this is not evidence about large effects.

### Gaps
- No ATE-level coverage in the CausalPFN or Do-PFN papers themselves, as far as I found in text and figure captions (figures not visually inspected).
- Whether v0.1.4 had the same default for `calibrate` was not separately checked.

## Q4. Has anyone independently evaluated or critiqued these models?

### Takeaway
Yes, and critically, starting in 2026. Fully independent evaluations (Mourão, Zhang, Jung, Ham, Wang) exist, but two widely cited follow-ups share authors with CausalPFN. I found no independent evaluation that runs CFMs against known truth on real RCT benchmarks across effect sizes.

### Cited Findings

**Independence of each source (my reading of author lists):**
- **Independent of the CausalPFN and Do-PFN teams:** [Mourão](https://arxiv.org/abs/2603.15928), [Zhang](https://arxiv.org/abs/2609.26290), [Jung](https://arxiv.org/abs/2609.36881), [Ham](https://icml.cc/virtual/2026/71511), [Wang](https://icml.cc/virtual/2026/poster/63252), and [Schulman, Bynum, Wald](https://arxiv.org/abs/2610.22770). Bynum authored the competing BBCI.
- **Not independent of CausalPFN:** [Stith et al.](https://arxiv.org/abs/2609.03003) has Cresswell, a CausalPFN coauthor, so its statement ["our CausalPFN results independently replicate the values reported"](https://arxiv.org/html/2609.03003) needs that qualification. [Melnychuk et al.](https://arxiv.org/abs/2603.12037) includes Balazadeh and Krishnan.
- **Competing authors:** the CausalPFN and CausalFM papers each critique Do-PFN.

**Findings:**
- [Mourão [P] concludes "the computational burden of TabPFN and the limited performance of CausalPFN currently preclude their practical use in causal inference"](https://arxiv.org/html/2603.15928), noting limits: [two scenarios, binary variables, minimal adjustment set](https://arxiv.org/html/2603.15928). Their scenarios were simulated from real data with known truth, and [TabPFN-IPTW had near-nominal coverage (94.3 to 95.2%) in Indomethacin](https://arxiv.org/html/2603.15928).
- [Zhang [P]: Summary FSP lowers RMSE 10 to 13% and defect 79 to 86% against CausalPFN-S; S-learner has lower RMSE than FSP in this well-specified problem](https://arxiv.org/html/2609.26290). Zhang also evaluates the [official checkpoint at a pinned commit and hash](https://arxiv.org/html/2609.26290), a good audit pattern. Single-author preprint. It flags [Do-PFN as out of domain](https://arxiv.org/html/2609.26290), so its poor numbers there should not be overread.
- [Jung [P]: "no CFM consistently performs best and model rankings vary substantially"; "model-specific failures"](https://arxiv.org/abs/2609.36881).
- [Ham [P]: post-treatment covariates in queries hurt CFMs; removing them cut error by approximately 25% for Do-PFN and up to 72% for CausalPFN; TC-LD recovers 85.5 to 92.6% of Oracle headroom on the synthetic benchmark and detected all injected mediators on IHDP and ACIC 2016](https://icml.cc/virtual/2026/71511).
- [CausalPFN authors' own limits [P]: ignorability is untestable, and without it "CausalPFN has no guarantees of validity"; performance degrades on the largest marketing tables](https://arxiv.org/html/2506.07918).
- [Do-PFN authors' own limits [P]: generalization "critically depends" on the prior; "current validation is based on synthetic data"](https://arxiv.org/html/2506.06039). Mourão also notes [Do-PFN is limited to continuous outcomes](https://arxiv.org/html/2603.15928).
- [Zhou [P]: "In four of five experiments, synthetic diagnostic metrics and real-domain generalization give opposite testimony"](https://arxiv.org/html/2609.06941). This cautions against validating a detector only on synthetic data.
- [CausalFM's critique of Do-PFN [P]: mixing graphs in one prior "can lead to asymptotically biased estimates and non-informative posteriors"](https://arxiv.org/html/2506.10914).

**Citation coverage:** Semantic Scholar on 31 Oct 2026 returned [64 citing papers for CausalPFN](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.07918/citations), [69 for Do-PFN](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.06039/citations), and [47 for CausalFM](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.10914/citations). I screened them by title, and read or scanned the relevant ones.

### Inferences
- [I] The critique literature is recent and accelerating: Zhang, Stith, Jung, Schulman and the debiased-PFN paper all appeared in Sep to Oct 2026. Novelty claims should be dated, and may need rechecking at submission.

### Gaps
- No independent real-RCT evaluation with effect-size variation found. Zhang's RCT results concern FSP ensembles, not CausalPFN.
- Lower-profile citing papers were screened by title only. Examples not read: [Computational Identifiability](https://arxiv.org/abs/2606.19361), [DeDiCa](https://arxiv.org/abs/2610.23272).

## Q5. Is there prior work proposing a runtime check, diagnostic, falsification test or trust score specifically for CFMs?

### Takeaway
**Negative result for the exact combination.** Within this search, I found no work that compares a CFM's ATE against a cross-fitted doubly robust reference using a statistical test at runtime, with abstention, to detect shrinkage. Several adjacent ideas exist, and a CFM review names detection of prior mismatch as an open future need.

### Cited Findings

**Nearest neighbours, and how each differs:**
- **Stated as open [P]:** ["useful properties of future CFMs would include automatic detection of mismatch between the target DGP and the training prior. Both problems are especially difficult in the causal setting, where observational data does not fully characterize the distributions of interest."](https://arxiv.org/html/2609.03003) It frames the need generally and proposes no method. This is the strongest available support for a gap.
- **TCPFN [P]:** ["No existing causal PFN method outputs explicit per-pair reliability signals"; its Judgment Head lets the model "flag when those estimates may be unreliable"](https://arxiv.org/html/2606.20889). It is a learned head inside one model, not model-agnostic, has no reference estimator or hypothesis test, targets temporal data, and reports [null-effect detection accuracy 0.94, AUROC 0.99](https://arxiv.org/html/2606.20889) in training metrics. Code release pending at the time of the paper.
- **TC-LD (Ham) [P]:** [a filter applied before inference that flags likely post-treatment variables](https://icml.cc/virtual/2026/74345). It targets a different failure, and checks inputs rather than outputs.
- **Berti [S, abstract via index]:** [each effect query returns an estimate with diagnostics or a reasoned refusal; stress tests show consistent refusal when declared conditions fail; a pretrained neural router is the baseline](https://www.semanticscholar.org/paper/1a3fb05183905f0b4003179e2f7f643c15074845). Closest on **abstention**, but it gates classical estimator stacks on declared assumptions, and it is not a check on CFM output. It cites CausalPFN and Do-PFN according to Semantic Scholar. Full text not accessible, so details are unverified.
- **MP-OSPC (Melnychuk) [P]:** ["similar to the bias correction of the frequentist A-IPTW estimator"; for an already calibrated posterior the correction has essentially no asymptotic effect](https://arxiv.org/html/2603.12037). It is evaluated by total-variation distance to A-IPTW and uses PFN-derived nuisances at runtime, but it outputs a corrected posterior rather than a decision.
- **CausalPFN regression ICE [P]:** [computable from observational data with no counterfactuals](https://arxiv.org/html/2506.07918). A genuine runtime check, but of intervals only.
- **Zhang's response slope and teacher defect [P]:** [use the oracle teacher only for evaluation](https://arxiv.org/html/2609.26290), so they are not deployable. Calling them "diagnostics" must not be confused with a runtime test.
- **Schulman's coverage prediction [P]:** ["Both rho_S and m_S require the true effects, so neither can be computed in practice, and we use them only as diagnostics"](https://arxiv.org/html/2610.22770). Their deployable product is a corrective head, not a check.

**Search record for this negative result:**
- **arXiv API**, with hit counts:
  - `all:"causal foundation model"` 19; `all:"causal foundation models"` 19; `all:CausalPFN` 6; `all:"Do-PFN"` 3
  - `abs:"amortized" AND abs:"causal" AND abs:"shrinkage"` 1 (Zhang)
  - `abs:"prior-data fitted" AND abs:"causal"` 25; `abs:"prior-fitted" AND abs:"causal"` 11
  - `abs:"in-context" AND abs:"causal effect"` 258 (noisy; newest 25 screened)
  - `abs:"foundation model" AND abs:"causal" AND abs:"falsification"` **0**
  - `abs:"amortized" AND abs:"causal" AND abs:"diagnostic"` 4 (none relevant)
  - `abs:"prior-data fitted" AND abs:"doubly robust"` **0**
  - `abs:"foundation model" AND abs:"causal" AND abs:"attenuation"` 1 (Zhang); `abs:"foundation model" AND abs:"causal" AND abs:"shrinkage"` 1 (Zhang)
  - `abs:"prior-data fitted" AND abs:"bias" AND abs:"treatment effect"` 2 (Mourão, Melnychuk)
  - `abs:"amortized" AND abs:"treatment effect" AND abs:"calibration"` 2 (TabCon, CausalPFN)
  - `abs:"foundation model" AND abs:"treatment effect" AND abs:"trust"` **0**
  - `abs:"foundation model" AND abs:"causal" AND abs:"abstain"` **0**
  - `abs:"foundation model" AND abs:"AIPW"` **0**
- **Web search:** "causal foundation model shrinkage large effects amortized estimator failure"; "diagnostic falsification test trust score amortized causal estimator foundation model runtime check"; "independent evaluation CausalPFN benchmark comparison doubly robust real-world RCT"; "Do-PFN causal effect prior-fitted networks evaluation"; "CausalPFN amortized causal effect estimation"; "Mourao causal foundation models coverage credible intervals CausalPFN 2026"; "Ham 2026 post-treatment covariate causal foundation models filtering PFN"; "task-specific fine-tuning causal foundation model bias low prior coverage".
- **Full-text regex scan of 32 CFM-adjacent papers:** terms were falsif*, trust score, abstain/abstention, runtime check, sanity check, detect or flag or test near shrink*, detect or flag or test or diagnos* near AIPW/A-IPTW/doubly robust/DML, detect or flag near prior mismatch/OOD. Result: **zero hits** for falsif*, trust score, abstain, runtime check, and shrinkage detection. "Sanity check" and "trustworthy" hits were unrelated or are listed above. The DR-near-test pattern had one false positive. The mismatch pattern had one hit: Stith, quoted above.

### Inferences
- [I] What appears unclaimed: a **black-box output test**, comparing any CFM's ATE to a cross-fitted DR reference, with a calibrated false-alarm rate, overlap abstention and a positive control.
- [I] What is **not** novel: the shrinkage phenomenon and its mechanism (Do-PFN appendix, Melnychuk, Zhang, Stith), DR or EIF as a corrective or evaluation yardstick for PFNs (Melnychuk, Zhang), refusal logic in automated causal pipelines (Berti), and observational runtime calibration (CausalPFN).
- [I] Melnychuk's correction term is close to a test statistic: an EIF residual averaged under the PFN's nuisances, near zero when calibrated. A reader could reasonably view a z-test on model minus AIPW as a frequentist cousin. Cite this explicitly when claiming novelty.
- [I] Beyond the CFM literature, generic specification tests, including Hausman-style model-versus-DR comparisons, are older adjacent art. These are outside this note's scope and need separate checking.

### Gaps
- **Not exhaustive.** Google Scholar was not queried, and OpenReview, CLeaR, UAI and AISTATS proceedings were not crawled separately (only web search reach). The regex scan covered 32 full texts, not all 130+ citing records. Different wording would escape the patterns. Recent workshop papers and non-arXiv work may be missed.
- Berti's full text is blocked, so its relationship to CFMs is unverified beyond the abstract.

## Q6. How do these models compare with doubly robust estimators on benchmarks, according to their authors?

### Takeaway
Authors report that CFMs beat forest-based DR and DML estimators on CATE and on Lalonde ATE, but not uniformly on ATE. Simple T-learners and IPW are at least as competitive on ATE, and I found no model paper using plain cross-fitted AIPW as its main baseline (the strings AIPW and A-IPTW do not appear in the CausalPFN or Do-PFN full text). Benchmark rankings conflict across author groups.

### Cited Findings
- **CausalPFN Table 1 [P] (authors'):** [CausalPFN, Forest DML and Forest DR ATE relative errors: IHDP 0.20, 0.08, 0.17; ACIC 0.05, 0.05, 0.04; Lalonde CPS 0.13, 1.03, 1.20; PSID 0.22, 1.05, 3.64. Average ATE rank 4.45, 9.60, 8.38. Average CATE rank 2.30, 9.83, 10.00](https://arxiv.org/html/2506.07918). The table's rows do not include plain AIPW. On ATE rank, [T-Learner 4.31 and IPW 4.41 are slightly ahead of CausalPFN](https://arxiv.org/html/2506.07918), which the paper calls ["competitive for average ATE rank"](https://arxiv.org/html/2506.07918). DML wins clearly on IHDP ATE.
- **CausalPFN marketing RCTs [P]:** [Best mean normalized Qini on 50k subsamples, with a drop on full tables](https://arxiv.org/html/2506.07918). Qini is a ranking metric, so it says little about effect magnitude.
- **Stith Table 3 [P], Cresswell coauthor:** [ATE relative error on CPS/PSID: CausalPFN .17/.24; Debiased ML .34/.29; DR-Learner .89/.64; T-Learner .28/.04; IPW .15/.08; PEHE CausalPFN 8.97/14.00, Debiased ML 9.96/15.45, DR-Learner 13.45/24.09](https://arxiv.org/html/2609.03003). ["IPW ... showed the strongest results on ATE Relative Error"; "CausalPFN achieves the lowest average rank among CFMs, closely trailing the extensively tuned T-Learner"](https://arxiv.org/html/2609.03003).
- **Do-PFN [P] (authors'):** [On its six synthetic case studies "Do-PFN significantly outperforms our meta-learner, double machine learning, and deep-learning based baselines" on ATE](https://arxiv.org/html/2506.06039); [competitive on RealCause in unconfounded settings](https://arxiv.org/html/2506.06039). Those are the authors' own case studies, and the paper notes that [baseline performance "depends on the satisfaction of unconfoundedness"](https://arxiv.org/html/2506.06039), which some case studies violate by design.
- **CausalFM Table 2 [P] (authors'):** [PEHE on Synthetic/Jobs: DR-learner .765/.959; CausalPFN .557/.528; DoPFN .586/.482; CausalFM .515/.478](https://arxiv.org/html/2506.10914).
- **Conflict in rankings [P]:** Do-PFN [ties or beats CausalPFN on Jobs in the CausalFM table](https://arxiv.org/html/2506.10914) but is [far behind in the CausalPFN table](https://arxiv.org/html/2506.07918), and each paper's own model comes out on top.
- **TabPFN-2.5 [P] (vendor-reported):** ["PFN-based methods for CATE-estimation dominate the leaderboard, occupying the first seven positions"; TabPFN-2.5 as a T-Learner is strongest](https://arxiv.org/html/2511.08667). Note that this top entry is a predictive model used as a T-Learner, not one pretrained for causal targets.
- **Independent, well-specified comparison [P]:**
  - [Zhang Table 3 RMSE (typical, shifted, boundary): AIPW/DML .0664, .0663, .0798; CausalPFN-S .0702, .0695, .0802; teacher defect under shift .077 versus .200](https://arxiv.org/html/2609.26290). AIPW is slightly better on all three here, in a simple four-stratum problem.
  - On the continuous grid at n=256, [response slopes are .819 FSP, .951 S-learner, .988 full-fit AIPW, 1.008 cross-fitted DML](https://arxiv.org/html/2609.26290). So cross-fitted DML was the best-centred method there.
  - Clinical simulations: [TabPFN-based IPTW had low mean error and near-nominal coverage, unlike CausalPFN](https://arxiv.org/html/2603.15928).

### Inferences
- [I] The evidence supports AIPW as a good **centring** reference in well-specified settings with reasonable overlap (Zhang), but **not unconditionally**: DR-learner variants show relative errors of 0.64 to 3.64 on RealCause-Lalonde, and Forest DML 1.03 to 1.05, although Stith's Debiased ML reaches 0.29 to 0.34. The detector's abstention rule has real work to do, since on those benchmarks a flag could mean the reference failed.
- [I] DR implementations differ widely: Forest DR and EconML-style learners with [tuning and cubic covariate expansion](https://arxiv.org/html/2506.07918) are not the plain cross-fitted AIPW in the objective. Author benchmarks therefore say little about the specific reference proposed.
- [I] CFM versus DR comparisons appear to favour whoever designed the benchmark, so the detector's validation should report results across more than one author's benchmark.

### Gaps
- No model paper reports plain cross-fitted AIPW for the ATE as a main baseline on IHDP, ACIC or Lalonde with both point error and coverage. I did not check every appendix table of every paper for it.
- Effect-size-stratified comparison of CFM versus AIPW: none found, apart from Zhang's small-scale shift and the Do-PFN base-rate ablation (figure not numerically readable from text).
