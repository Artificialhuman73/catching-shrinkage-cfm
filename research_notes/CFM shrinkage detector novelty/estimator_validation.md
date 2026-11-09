# Prior art for validating, falsifying and diagnosing causal estimators against a reference (CFM shrinkage detector novelty)

Detector under evaluation: flag a causal foundation model (CFM) as shrunk when z = (AIPW - CFM)/SE_AIPW > 1.645, using a cross-fitted AIPW reference on the same data, and abstain if more than 5% of propensities are extreme. Its label is "shrunk by more than 10%"; its test null is "gap = 0".

Conventions used throughout:
- Evidence tags: **[FT]** = primary source, full text or the relevant passages read. **[ABS]** = primary source, abstract, listing or official docs page only. **[META]** = bibliographic metadata only (Crossref), content not read. **[SEC]** = secondary source or search snippet only.
- "Overlap %" is my own judgement, not a measured quantity. It estimates how much of the detector's five components a paper covers: C1 black-box versus doubly robust contrast; C2 same-data cross-fitted reference; C3 one-sided z with reference-only SE; C4 CFM or shrinkage target; C5 propensity-based abstention.
- "Foundational" marks pre-2024 work included because a reviewer would expect it to be cited.
- Any calculation labelled "my calculation" is mine and appears in no cited source.

## Overall: which existing work is closest to the detector?

### Takeaway
I found no paper that combines all of: a black-box CFM ATE, a same-data cross-fitted AIPW reference, a one-sided reference-SE z-test, and overlap abstention. Every component has precedent, though, and the closest single paper is Persson et al. (2026). The detector's statistic is close to an observational, one-sided, whole-population special case of its group-bias test. A novelty claim should rest on the combination and the deployment target, not on the test itself.

### Cited Findings
Ranked closest-first. Details are in the sections below.

| Rank | Work | Overlap % (my judgement) | What a reviewer would say | Main difference |
|---|---|---|---|---|
| 1 | [Persson et al. 2026](https://arxiv.org/abs/2602.20383), group bias test [FT] | 65 | "This is their Wald test at group = everyone" | RCT reference only; two-sided; CATE aggregation, not CFMs; no abstention |
| 2 | [Hausman 1978](https://doi.org/10.2307/1913827) contrast test (foundational) [META] | 60 | "This is a one-sided Hausman test" | Different denominator and inverted efficiency roles (see the Hausman section) |
| 3 | [Hussain et al. 2022](https://arxiv.org/abs/2209.13708) [FT] | 50 | "Same z-test and reject rule, with an RCT" | Independent datasets, two-sided, multiple candidate estimators |
| 4 | Doubly robust as a diagnostic, Robins and Rotnitzky 2001 via [Duke slides](http://www2.stat.duke.edu/~fl35/teaching/640/Chap3.5_Doubly%20Robust%20Estimation.pdf) (foundational) [SEC] | 50 | "Comparing DR to a plug-in is old folk practice" | Informal; compares DR with regression and IPW, not a black box |
| 5 | [EconML DRTester](https://www.pywhy.org/EconML/_autosummary/econml.validate.DRTester.html) [ABS] | 45 | "Existing library already validates CATE against cross-fitted DR outcomes" | Slope, calibration and uplift tests; no one-sided mean-gap test; no abstention |
| 6 | [grf test_calibration](https://www.rdocumentation.org/packages/grf/versions/2.6.0/topics/test_calibration) [ABS] | 45 | "Mean coefficient = 1 is already the check" | Forest-oriented; uses a regression, not an AIPW contrast |
| 7 | [RCT-DUPLICATE estimate agreement](https://pubmed.ncbi.nlm.nih.gov/33327727/) (foundational) [ABS] | 40 | "Same reference-only CI check, with an RCT" | RCT reference; two-sided; clinical emulation |
| 8 | [De Bartolomeis et al. 2024](https://arxiv.org/abs/2404.18905) [FT] | 40 | "They already test bias up to a tolerance" | RCT reference; kernel test; no CFM |
| 9 | [Melnychuk et al. 2026](https://arxiv.org/abs/2603.12037) [FT] | 35 | "Why detect? Just apply this correction" | Debiases rather than detects; prior-induced confounding bias |
| 10 | [Zhang 2026](https://arxiv.org/abs/2609.26290) [FT] | 35 | "Already diagnosed and fixed CFM shrinkage" | Fixes pretraining; response slope needs an oracle |
| 11 | [Cornish et al.](https://arxiv.org/abs/2301.07210) [ABS] | 35 | "Falsifying a black box on observational data exists" | Digital twins; valid under confounding; different test |
| 12 | [Xu and Yadlowsky 2022](https://arxiv.org/abs/2203.13364) [ABS] | 30 | "DR-based calibration error covers this" | L2 CATE calibration metric |
| 13 | [Hussain et al. 2023](https://arxiv.org/abs/2301.13133), [Parikh et al.](https://arxiv.org/abs/2307.01449) [FT] | 30 each | "DR-signal falsification exists" | Two studies required |
| 14 | [Demirel et al. 2024](https://arxiv.org/abs/2402.15137), [Yang et al. 2023](https://arxiv.org/abs/2005.10579), [Oberst et al.](https://arxiv.org/abs/2205.10467) [FT] | 25 each | "Benchmarking and test-based integration" | Two studies required |
| 15 | [Stith et al. 2026](https://arxiv.org/abs/2609.03003), [Young and Dillon 2026](https://arxiv.org/abs/2601.11845) [FT] | 20 each | Evidence for the phenomenon or for DR, not a detector | No formal contrast test |

### Inferences
- Defensible novelty is narrow: a deployment-time, single-dataset check aimed at CFM attenuation, with no oracle and no RCT. The nearest deployed-CFM work either changes training (Zhang) or corrects output (Melnychuk).
- The single-dataset property cuts both ways. It removes the need for an RCT, but AIPW and the CFM share unconfoundedness, so the detector tests estimator disagreement, not validity. The word "falsification" should be avoided or qualified.
- Four attack lines to prepare for: (a) "one-sided Hausman with the wrong variance"; (b) "Persson with AIPW"; (c) "if you computed AIPW, why not report it or apply one-step correction"; (d) "your test null does not match your label".

### Gaps
- Absence of evidence is not proof of absence. Semantic Scholar and Google Scholar were not queried directly, and the Journal of Causal Inference was not searched as a separate venue; searches ran through the web search tool, the arXiv API and Crossref. The arXiv API returned HTTP 429 on some batches, and I fell back to abstract pages.
- Queries for this section: "causal foundation model black-box estimate validation AIPW reference shrinkage ATE pretrained amortized"; "test agreement black-box ATE estimator doubly robust cross-fit z-test diagnostic estimator bias detection"; "audit pretrained causal model against doubly robust estimator disagreement detect miscalibration amortized causal effect". None returned a matching detector.

## Is the detector essentially a one-sided Hausman test, and what is the correct variance?

### Takeaway
It belongs to the Hausman contrast family but is not Hausman's test. On the same data the correct variance is Var(AIPW) + Var(CFM) - 2Cov(AIPW, CFM), not SE_AIPW squared, and Hausman's shortcut does not apply because AIPW is the efficient estimator here. I found no ML-era Hausman test built on AIPW or DML.

### Cited Findings
Classical test:
- **Specification Tests in Econometrics** | J. A. Hausman | Econometrica 46(6):1251, 1978 | [DOI](https://doi.org/10.2307/1913827) | [META], foundational. Overlap 60%.
- The statistic is H = (b_c - b_e)'(V_c - V_e)^(-1)(b_c - b_e), compared with chi-squared. It compares an always-consistent estimator with one efficient under the tested assumption — [Stata hausman manual](https://www.stata.com/manuals/rhausman.pdf) [FT].
- The V_c - V_e simplification comes from Hausman's result that the covariance between an efficient estimator and its difference from an inefficient one is zero, so Var(q) = Var(b0) + Var(b1) - 2Cov(b1, b0) reduces to Var(b0) - Var(b1) — [Wikipedia, Durbin-Wu-Hausman](https://en.wikipedia.org/wiki/Durbin%E2%80%93Wu%E2%80%93Hausman_test) [SEC].
- Stata states that efficiency fails for pweighted or clustered estimators "so hausman cannot be used", and warns that a negative statistic means the data fail the test's asymptotic assumptions. It points to suest, whose alternative variance estimator of the difference is positive semidefinite and relaxes "the assumption that one of the estimators is efficient" — [Stata manual](https://www.stata.com/manuals/rhausman.pdf) [FT].
- **The impact of a Hausman pretest on the asymptotic size of a hypothesis test** | Patrik Guggenberger | Econometric Theory 26(2):369-382 | [DOI](https://doi.org/10.1017/s0266466609100026) | [META], foundational. Relevant if the detector gates a downstream estimator. Crossref's issued year is 2009; volume 26 is also often cited as 2010 (from memory, unverified). Overlap 15%.

Same-data variance as handled in nearby work:
- Persson et al. say closed-form SEs are "cumbersome" because they depend on "the covariance between the model-implied and experimental GATEs (unless independent samples are used)". They recommend a nonparametric bootstrap, and note that sample splitting removes the covariance "at the cost of a reduced effective sample size" — [Persson et al. 2026](https://arxiv.org/abs/2602.20383) [FT].
- Oberst et al. write the shared-sample covariance explicitly as sigma_bu. They note the unbiased and biased estimators "are not independent, due to the shared use of experimental samples", and estimate the variances and covariance by bootstrap or RAL plug-in — [Oberst et al.](https://arxiv.org/abs/2205.10467) [FT].
- Hussain et al. can use a summed-variance denominator only because "the observational and randomized datasets are distinct" — [Hussain et al. 2022](https://arxiv.org/abs/2209.13708) [FT].

Modern Hausman-type work (none is DML or AIPW):
- **Specification testing with grouped fixed effects** | Claudia Pigini, Alessandro Pionati, Francesco Valentini | arXiv 2023, updated 2025 | [2310.01950](https://arxiv.org/abs/2310.01950) | [ABS]. Does: a Hausman test contrasting one-way FE with two-way grouped FE, using jackknife-corrected estimators and a bootstrap for the variance of the contrasts. Differs: panel data; a search snippet's "ML" here means maximum likelihood, not machine learning. Overlap 15%. Useful as precedent for bootstrapping the contrast variance.
- **Testing Endogeneity with High Dimensional Covariates** | Zijian Guo, Hyunseung Kang, T. Tony Cai, Dylan S. Small | J. Econometrics 207(1):175-187, 2018 | [1609.06713](https://arxiv.org/abs/1609.06713) | [ABS], foundational. Does: finds Durbin-Wu-Hausman keeps size but loses power in high dimensions, and proposes a more powerful test. Differs: IV regression. Overlap 15%.
- **Parameter-Specific Bias Diagnostics in Random-Effects Panel Data Models** | Andrew T. Karl | arXiv 2024, v6 October 2026 | [2412.20555](https://arxiv.org/abs/2412.20555) | [ABS]. Does: a coefficient-level diagnostic complementing Hausman for mixed models. v1 was titled "Hausman's Consistency Test and an Internal Bias Diagnostic". Overlap 10%.
- **Testing the Unconfoundedness Assumption via Inverse Probability Weighted Estimators of (L)ATT** | Stephen G. Donald, Yu-Chin Hsu, Robert P. Lieli | JBES 32(3):395-415, 2014 | [DOI](https://doi.org/10.1080/07350015.2014.888290) | [META], foundational. Publisher page returned 403, so whether it is Hausman-type is unverified: Insufficient publicly verifiable evidence. Overlap not scored.

Doubly robust contrast as a diagnostic:
- Course slides attribute to Robins and Rotnitzky (2001) the practice of comparing DR with IPW and regression on the same data: DR close to IPW but not regression suggests a wrong outcome model. They add "one can even formalize a test for 'similarity'... but little empirical investigations on the performance of the test", and cite Mercatanti and Li (2014) as an example — [Fan Li, Duke STA 640 slides](http://www2.stat.duke.edu/~fl35/teaching/640/Chap3.5_Doubly%20Robust%20Estimation.pdf) [SEC]. Overlap 50%. The example paper exists — [Mercatanti and Li, Ann. Appl. Stat. 8(4):2485-2508, 2014](https://doi.org/10.1214/14-aoas784) [META].
- The influence-function variance estimator for DR estimators is reported biased when one nuisance is misspecified, which affects SE_AIPW — [Wu, Shao, et al. 2025, arXiv 2511.17907](https://arxiv.org/abs/2511.17907) [SEC for this claim; title and authors checked from the PDF].

### Inferences
All calculations here are mine.
- **Role inversion.** In Hausman's setup the reference is inefficient and robust, and the candidate is efficient under the null. Here AIPW is itself semiparametrically efficient under the standard conditions described by [Melnychuk et al.](https://arxiv.org/abs/2603.12037). So V_c - V_e is unavailable. If the CFM were also asymptotically equivalent to AIPW, the contrast would be o_p(1/sqrt(n)) and the test degenerate.
- **Actual size.** With D = AIPW - CFM, r = sd(CFM)/sd(AIPW) and rho = corr(AIPW, CFM), the null variance of z is 1 + r^2 - 2 rho r. The nominal 5% holds only when r = 0 or r = 2 rho.

| r | rho | sd(D)/sd(AIPW) | Actual size of z > 1.645 |
|---|---|---|---|
| 0 | n/a | 1.000 | 0.050 |
| 0.5 | 0 | 1.118 | 0.071 |
| 1 | 0 | 1.414 | 0.122 |
| 2 | 0.5 | 1.732 | 0.171 |
| 1 | 0.5 | 1.000 | 0.050 |
| 0.5 | 0.8 | 0.671 | 0.007 |
| 1 | 0.9 | 0.447 | 0.0001 |

- So the test is anti-conservative for a noisy CFM weakly correlated with AIPW, and very conservative for a CFM highly correlated with AIPW. The reported 5% cannot be assumed either way.
- **Correct variance does not automatically give the right label.** Under pure linear shrinkage CFM = s AIPW + (1-s) c0, the correct z is (AIPW - c0)/SE_AIPW for every s. That is a test of AIPW against the prior centre, and it no longer depends on the amount of shrinkage. The reference-SE z equals (1-s)(AIPW - c0)/SE_AIPW, which does scale with shrinkage. This is a real argument for keeping SE_AIPW, provided it is framed honestly.
- **Honest framing of the current statistic.** z > 1.645 is exactly "the CFM number lies below AIPW's lower one-sided 95% confidence limit". That treats the CFM output as a fixed claim. It is formally valid only if the CFM output is independent of the AIPW sample, for example under sample splitting.
- **Variance options, in my order of preference:** (a) a paired bootstrap of both estimators, which is cheap for the CFM's forward pass but not for nuisance refits; (b) sample splitting with Var = V_A + V_C; (c) joint influence-function stacking in the spirit of suest, which requires the CFM to be asymptotically linear, and that is unestablished. Shrinkage estimators may be non-regular near the prior centre, so bootstrap validity is a real question there.
- **Sign bug.** As written, z only flags AIPW > CFM. A negative true effect shrunk toward zero gives CFM > AIPW and z < 0, so it is never flagged. Zhang's own illustrative example is -150 g attenuated to about -75 g. The statistic needs sign(AIPW) normalisation.

### Gaps
- Robins and Rotnitzky (2001) was not read in the original; the claim rests on slides. Crossref did not return it.
- I could not find any source that names or analyses a one-sided Hausman test.
- Negative result: "Hausman" has zero hits in the full text of 13 ML-era papers I checked: Parikh, Yang, Oberst, Demirel, De Bartolomeis 2024 and 2025, Stith, CausalPFN, Zhang/Tan TabPFN, Melnychuk, Persson, Hussain 2022 and 2023.
- Queries: "Hausman test double machine learning specification test comparing estimators difference variance"; ""Hausman" test "debiased machine learning" OR "double machine learning" misspecification test nuisance"; "one-sided Hausman test directional alternative comparing estimators variance of difference same data bootstrap non-efficient estimator"; "Hausman-type test doubly robust estimator versus outcome regression contrast misspecification Robins Rotnitzky".

## Falsification and benchmarking against RCTs or reference estimators

### Takeaway
This literature supplies the detector's template (estimate, reference, z-test, reject), but almost all of it needs a second study, usually an RCT. Persson et al. is the nearest in statistic and purpose. De Bartolomeis et al. is the nearest on tolerance.

### Cited Findings
- **Detecting and Mitigating Group Bias in Heterogeneous Treatment Effects** | Joel Persson, Jurrien Bakker, Dennis Bohle, Stefan Feuerriegel, Florian von Wangenheim | arXiv preprint, February 2026 | [2602.20383](https://arxiv.org/abs/2602.20383) | [FT]. Overlap 65%.
  - Does: defines group bias as model-implied GATE minus experimentally identified GATE. Tests H0: b_g = 0 with a Wald z, rejecting "against its two-sided alternative". States the procedure is "nonparametric, model-agnostic". Treats the fitted CATE model as fixed. Proposes a shrinkage-weighted bias correction. Applied to a Booking.com A/B test and Criteo uplift data.
  - Directly on shrinkage: predicted GATEs "exhibit a substantially narrower range than the experimental GATEs", which it attributes to regularisation "shrinking heterogeneity in treatment effects toward the global mean".
  - Differs: randomised reference only; it says extension to non-experimental settings "poses conceptual and technical challenges". Two-sided, group-level, no overlap rule, no CFMs. Warns that reusing detection-stage estimates to evaluate mitigation causes post-selection bias.
- **Falsification before Extrapolation in Causal Effect Estimation** | Zeshan Hussain, Michael Oberst, Ming-Chieh Shih, David Sontag | NeurIPS 2022 | [2209.13708](https://arxiv.org/abs/2209.13708) | [FT], foundational. Overlap 50%.
  - Does: rejects observational estimators using a z-type statistic against RCT validation effects, with denominator s^2 = sigma_i^2(k)/N_k + sigma_i^2(0)/N_0, two-sided, Bonferroni-corrected. Failure to reject is not treated as validation: "failure to reject does not imply validity".
  - Differs: independent datasets, multiple candidates, zero-tolerance null, no shrinkage target.
- **Falsification of Internal and External Validity in Observational Studies via Conditional Moment Restrictions** | Zeshan Hussain, Ming-Chieh Shih, Michael Oberst, Ilker Demirel, David Sontag | AISTATS 2023, PMLR 206 | [2301.13133](https://arxiv.org/abs/2301.13133) | [FT]. Overlap 30%.
  - Does: a maximum moment restriction kernel test of H0: E[psi | X] = 0 with bootstrap critical values. Uses an IPW signal for the RCT and a doubly robust signal for the observational study. Uses the RCT CATE as "a proxy for the true CATE". Differs: needs both data sources; conditional rather than mean-level; exact-zero null.
- **Benchmarking Observational Studies with Experimental Data under Right-Censoring** | Ilker Demirel, Edward De Brouwer, Zeshan Hussain, Michael Oberst, Anthony Philippakis, David Sontag | AISTATS 2024, PMLR 238:4285-4293 | [2402.15137](https://arxiv.org/abs/2402.15137) | [FT]. Overlap 25%.
  - Does: extends the falsification test to censored outcomes with a censoring-doubly-robust signal. Calls it an "equivalence test of CATEs", but the null is an exact moment restriction. Differs: two studies; survival outcomes.
- **Detecting critical treatment effect bias in small subgroups** | Piersilvio De Bartolomeis, Javier Abad, Konstantin Donhauser, Fanny Yang | UAI 2024 | [2404.18905](https://arxiv.org/abs/2404.18905) | [FT]. Overlap 40%.
  - Does: tests whether the bias is "contained within a tolerance range" using a cross U-statistic, with a one-sided normal rejection rule, plus a lower bound on maximum subgroup bias. Says prior tests "fall short of incorporating tolerance functions". Differs: RCT reference; plug-in signal, with a doubly robust version listed as future work; targets subgroup bias.
- **A Double Machine Learning Approach to Combining Experimental and Observational Data** | Harsh Parikh, Marco Morucci, Vittorio Orlandi, Sudeepa Roy, Cynthia Rudin, Alexander Volfovsky | arXiv 2023, v4 2025 | [2307.01449](https://arxiv.org/abs/2307.01449) | [FT]. Overlap 30%.
  - Does: a cross-fitted DML falsification test for external validity and ignorability, built from a mean-independence null. Includes a no-free-lunch theorem on identifying which assumption failed. Differs: two samples; tests assumptions, not an estimator. Journal venue not verified.
- **Elastic Integrative Analysis of Randomised Trial and Real-World Data for Treatment Heterogeneity Estimation** | Shu Yang, Chenyin Gao, Donglin Zeng, Xiaofei Wang | JRSS-B 85(3):575-596, 2023 | [2005.10579](https://arxiv.org/abs/2005.10579) | [FT]. Overlap 25%.
  - Does: a chi-squared pre-test T of RCT-versus-real-world comparability that decides whether to use real-world data, with a data-adaptive threshold. Explicitly a non-regular pre-test estimator, and it studies local alternatives. Differs: two studies. Most relevant if a detector gates an estimator.
- **Understanding the Risks and Rewards of Combining Unbiased and Possibly Biased Estimators, with Applications to Causal Inference** | Michael Oberst, Alexander D'Amour, Minmin Chen, Yuyan Wang, David Sontag, Steve Yadlowsky | arXiv 2022 | [2205.10467](https://arxiv.org/abs/2205.10467) | [FT]. Overlap 25%.
  - Does: introduces the "bias threshold", the largest bias at which a combination still beats the unbiased estimator alone. Differs: combines estimators rather than flagging one. Venue not verified.
- **Causal Falsification of Digital Twins** | Rob Cornish, Muhammad Faaiz Taufiq, Arnaud Doucet, Chris Holmes | accepted to JMLR per arXiv | [2301.07210](https://arxiv.org/abs/2301.07210) | [ABS]. Overlap 35%.
  - Does: looks for situations where a simulator is wrong, using only observational trajectories, and stays valid under confounding. Argues observational data cannot certify such a model without strong assumptions. Differs: sequential twins and a different test; no AIPW; I did not read the test construction. The one-sided "falsify, do not certify" stance matches the detector.
- **Reevaluating Causal Estimation Methods with Data from a Product Release** | Justin Young, Eleanor Wiske Dillon | arXiv 2026, v3 October 2026 | [2601.11845](https://arxiv.org/abs/2601.11845) | [FT]. Overlap 20%.
  - Does: compares observational estimators with an experimental baseline. In the untrimmed sample "Only the doubly robust estimator" still contains the truth. DR is "generally the most robust", but on the targeted outcome "none of our attempts come close". Differs: no formal contrast test. A search snippet listed a third author on v1, so check the version when citing.
- **Emulating Randomized Clinical Trials With Nonrandomized Real-World Evidence Studies: First Results From the RCT DUPLICATE Initiative** | Jessica M. Franklin et al. | Circulation 143(10):1002-1013, 2021 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/33327727/) | [ABS], foundational. Overlap 40%.
  - Does: estimate agreement is the observational hazard ratio falling inside the RCT's 95% CI, 8 of 10 studies. This is a reference-only-SE check. Differs: RCT reference; two-sided.
- **Emulation of Randomized Clinical Trials With Nonrandomized Database Analyses: Results of 32 Clinical Trials** | Shirley V. Wang et al. | JAMA 329(16):1376-1385, 2023 | [PubMed](https://pubmed.ncbi.nlm.nih.gov/37097356/) | [ABS]. Overlap 30%. Pearson r 0.82; significance agreement 75%; estimate agreement 66%; standardised difference agreement 75%.
- **Detecting hidden confounding in observational data using multiple environments** | Rickard K. A. Karlsson, Jesse H. Krijthe | NeurIPS 2023 | [2205.13935](https://arxiv.org/abs/2205.13935) | [ABS]. Overlap 10%. Detects confounding via conditional independence tests across environments, and needs multiple datasets.

Evidence on how trustworthy a DR reference is:
- On Lalonde, Stith et al. report ATE relative error for Debiased ML of 0.34 (CPS) and 0.29 (PSID), DR-Learner 0.89 and 0.64, and IPW 0.15 and 0.08 — [Stith et al. 2026](https://arxiv.org/abs/2609.03003) [FT].
- First-stage predictive quality tracked estimate quality in a "near-monotonic" way — [Young and Dillon 2026](https://arxiv.org/abs/2601.11845) [FT].
- Propensity miscalibration can produce biased IPW and doubly robust estimates, per the authors — [Deshpande and Kuleshov, arXiv 2306.00382](https://arxiv.org/abs/2306.00382) [ABS].

### Inferences
- The detector's denominator matches RCT-DUPLICATE's estimate agreement more closely than it matches Hussain's summed-variance test. A reviewer may find that comparison, so cite it pre-emptively.
- Reference quality is the detector's weakest assumption. On Lalonde the published DML and DR errors exceed the 10% label threshold, so a gap may reflect reference error rather than CFM shrinkage. The EconML-based learners in Stith are not the same as a plain cross-fitted AIPW, so this is suggestive, not direct.
- Stith's S-, X- and DR-learner errors of 0.64 to 0.97 on Lalonde suggest near-total under-recovery is not unique to CFMs on that data.

### Gaps
- I did not find a benchmarking paper where the reference is a same-data AIPW rather than an external experiment.
- Yang et al. 2020 and later work by that group were not exhaustively checked. "Yang et al." in the brief is assumed to mean the elastic integrative analysis paper.
- Queries: "Hussain Oberst Sontag falsification internal external validity observational studies randomized trials"; "Demirel benchmarking observational studies with experimental data under right-censoring".

## Causal model selection and validation without ground truth

### Takeaway
These methods rank candidates or measure CATE calibration; they are not tests of one black box's mean against a reference. The closest are the calibration tools, because the detector is effectively a one-sided calibration-in-the-large check.

### Cited Findings
Model selection:
- **Empirical Analysis of Model Selection for Heterogeneous Causal Effect Estimation** | Divyat Mahajan, Ioannis Mitliagkas, Brady Neal, Vasilis Syrgkanis | ICLR 2024 (Spotlight) | [2211.01939](https://arxiv.org/abs/2211.01939) | [FT]. Overlap 15%.
  - arXiv v3 reports "34 metrics" and 415 CATE estimators across 78 datasets and 20 seeds. It finds DR and TMLE T scores "globally dominating", better than calibration and Qini scores. Conflict: a search summary of an earlier listing gave 9 metrics and 144 datasets, so cite by version. Differs: selection, not testing.
- **In Search of Insights, Not Magic Bullets: Towards Demystification of the Model Selection Dilemma in Heterogeneous Treatment Effect Estimation** | Alicia Curth, Mihaela van der Schaar | ICML 2023, PMLR 202 | [2302.02923](https://arxiv.org/abs/2302.02923) | [ABS]. Overlap 10%. Reports success and failure modes rather than a winner.
- **Validating Causal Inference Models via Influence Functions** | Ahmed Alaa, Mihaela van der Schaar | ICML 2019, PMLR 97:191-201 | [PMLR](https://proceedings.mlr.press/v97/alaa19a.html) | [ABS], foundational. Overlap 15%. Estimates a method's error using influence functions and a synthesised proximal dataset; 77 benchmark datasets. Differs: estimates loss, needs a synthetic dataset, no test.
- **A comparison of methods for model selection when estimating individual treatment effects** | Alejandro Schuler, Michael Baiocchi, Robert Tibshirani, Nigam Shah | arXiv 2018 | [1804.05146](https://arxiv.org/abs/1804.05146) | [ABS], foundational. Overlap 5%.
- **Counterfactual Cross-Validation: Stable Model Selection Procedure for Causal Inference Models** | Yuta Saito, Shota Yasui | arXiv 2019, updated 2020 | [1909.05299](https://arxiv.org/abs/1909.05299) | [ABS], foundational. Overlap 5%. Venue not verified in sources read.
- **Reliable Selection of Heterogeneous Treatment Effect Estimators** | Jiayi Guo, Zijun Gao | arXiv 2025, v2 September 2026 | [2511.18464](https://arxiv.org/abs/2511.18464) | [ABS]. Overlap 20%. Casts selection as multiple testing with a cross-fitted, exponentially weighted statistic and asymptotic FWER control, ground-truth free. Differs: compares candidates, not a mean gap; no abstention.
- **Selective machine learning of doubly robust functionals** | Yifan Cui, Eric Tchetgen Tchetgen | Biometrika, per arXiv | [1911.02029](https://arxiv.org/abs/1911.02029) | [ABS], foundational. Overlap 15%. A pseudo-risk selects nuisance learner pairs so the DR functional is least sensitive to nuisance error.

Calibration (the closest group):
- **Causal isotonic calibration for heterogeneous treatment effects** | Lars van der Laan, Ernesto Ulloa-Perez, Marco Carone, Alex Luedtke | ICML 2023 | [2302.14011](https://arxiv.org/abs/2302.14011) | [ABS]. Overlap 25%. A doubly robust post-hoc calibrator that "can be wrapped around any black-box". It fixes rather than tests, and works at CATE level.
- **Doubly robust inference via calibration** | Lars van der Laan, Alex Luedtke, Marco Carone | arXiv 2024, v3 August 2026 | [2411.02771](https://arxiv.org/abs/2411.02771) | [ABS]. Overlap 15%. Calibrates nuisances inside DML for doubly robust normality; useful to harden the AIPW reference.
- **Doubly Robust Calibration of Prediction Sets under Covariate Shift** | Yachong Yang, Arun Kumar Kuchibhotla, Eric Tchetgen Tchetgen | arXiv 2022 | [2203.01761](https://arxiv.org/abs/2203.01761) | [ABS]. Overlap 5%. Same phrase as the brief but not by van der Laan: do not conflate.
- **Calibration Error for Heterogeneous Treatment Effects** | Yizhe Xu, Steve Yadlowsky | AISTATS 2022 | [2203.13364](https://arxiv.org/abs/2203.13364) | [ABS]. Overlap 30%. A DR estimator of L2 expected calibration error, usable for trials and observational studies. Notes HTE methods often over- or under-estimate and that formal checks were "limited to the calibration slope".
- **Fisher-Schultz Lecture: Generic Machine Learning Inference on Heterogenous Treatment Effects in Randomized Experiments** | Victor Chernozhukov, Mert Demirer, Esther Duflo, Ivan Fernandez-Val | arXiv 2017, v8 2023 | [1712.04802](https://arxiv.org/abs/1712.04802) | [ABS], foundational. Overlap 35%. Best linear predictors using any ML proxy with repeated splitting. Differs: randomised experiments; slope focus. Econometrica publication details were not verified in sources read.
- **Debiased Machine Learning of Conditional Average Treatment Effects and Other Causal Functions** | Vira Semenova, Victor Chernozhukov | arXiv 2017, v6 2020 | [1702.06240](https://arxiv.org/abs/1702.06240) | [ABS], foundational. Overlap 15%. Orthogonal signals projected on basis functions; group indicators recover GATEs.
- **grf test_calibration** | docs | [R documentation](https://www.rdocumentation.org/packages/grf/versions/2.6.0/topics/test_calibration) | [ABS]. Overlap 45%. Best linear fit with mean and differential predictions. "A coefficient of 1 for mean.forest.prediction suggests that the mean forest prediction is correct". Cites Chernozhukov et al. Docs do not state whether p-values are one-sided.
- **EconML DRTester** | docs | [EconML](https://www.pywhy.org/EconML/_autosummary/econml.validate.DRTester.html) | [ABS]. Overlap 45%. Cross-fitted DR outcomes, a BLP test, a binned calibration score against the overall ATE, and QINI/TOC. `fit_nuisance` returns a DR ATE. The docs describe no one-sided test of the mean gap and no abstention. It cites [Dwivedi et al. 2020, arXiv 2008.10109](https://arxiv.org/abs/2008.10109) for calibration.
- **Calibration of Heterogeneous Treatment Effects in Randomized Experiments** | Yan Leng, Drew Dimmery | [SSRN version](https://doi.org/10.2139/ssrn.3875850) | [META]. Persson et al. cite it as a 2024 publication and describe it as regressing CATE within calibration bins onto experimental subgroup effects. Overlap not scored.
- **Machine Learning Who to Nudge: Causal vs Predictive Targeting in a Field Experiment on Student Financial Aid Renewal** | Susan Athey, Niall Keleher, et al. (author list cut off in my extraction) | arXiv 2023, v2 2024 | [2310.08672](https://arxiv.org/abs/2310.08672) | [FT]. Overlap 15%. A calibration regression of outcomes on tau-hat, with both known-propensity and AIPW variants; finds slopes "substantially less than one".

### Inferences
- A reviewer's simplest reframing: the detector is calibration-in-the-large. The grf mean coefficient is the ratio form of the same question, since a coefficient above 1 means the mean prediction is too small. That would be a one-sided test of coefficient > 1, which neither grf's docs nor DRTester's docs describe.
- Direction warning: slope conventions differ. In a calibration regression of outcome on prediction, a slope below 1 means predictions are too spread out, as in Athey et al., and shrinkage shows as a slope above 1. Regressing predictions on truth gives the opposite. Zhang's "response slope" is a third concept, the response to the oracle fluctuation. Do not pool these numbers.
- BLP slopes target heterogeneity, while the detector targets the mean. A CFM could pass one and fail the other, so the detector is complementary and not redundant with slope tests.

### Gaps
- Negative result: searched for "E-validation" as a named method and found nothing. Results were E-value sensitivity analysis and sequential e-value randomisation tests (for example [arXiv 2512.04366](https://arxiv.org/abs/2512.04366)), neither of which is an estimator validator. The name in the brief may be wrong; Insufficient publicly verifiable evidence that it exists.
- I found no one-sided, mean-level, model-agnostic calibration test for observational data in these tools.
- Queries: "Mahajan empirical analysis model selection heterogeneous causal effect estimation"; "doubly robust calibration of prediction sets conditional average treatment effect van der Laan causal isotonic calibration"; "E-validation causal estimator selection validation without ground truth 2025"; ""E-validation" causal treatment effect estimators"; "e-values sequential testing validate treatment effect estimator anytime-valid model validation causal 2025"; "grf test_calibration mean forest prediction best linear predictor calibration test causal forest"; "Xu Yadlowsky calibration error heterogeneous treatment effects AISTATS 2022".

## Sensitivity to synthetic validators

### Takeaway
Synthetic validators can set the ATE and confounding, which suits detector evaluation, but their authors warn that results are conditional on generator assumptions. I found no study of a diagnostic's sensitivity across validators; they all compare estimators.

### Cited Findings
- **Validating Causal Inference Methods** (Credence) | Harsh Parikh, Carlos Varjao, Louise Xu, Eric Tchetgen Tchetgen | ICML 2022, PMLR 162:17346-17358 | [2202.04208](https://arxiv.org/abs/2202.04208) | [FT]. Overlap 15%. Generates data anchored at the observed sample with user-set effects and confounding. Its diagnostics are "as good as these assumptions", and it "requires careful hyper-parameter tuning for each data set".
- **RealCause: Realistic Causal Inference Benchmarking** | Brady Neal, Chin-Wei Huang, Sunand Raghupathi | arXiv 2020 | [2011.15007](https://arxiv.org/abs/2011.15007) | [ABS], foundational. Overlap 10%. Evaluates over 1500 estimators and says the best on synthetic data are "unlikely to be the best" on real data.
- **Marginal Causal Flows for Validation and Inference** (Frugal Flows) | Daniel de Vassimon Manela, Laura Battaglia, Robin J. Evans | NeurIPS 2024 | [2411.01295](https://arxiv.org/abs/2411.01295) | [FT]. Overlap 15%. Exactly satisfies a user-defined ATE. The authors report that altering Credence's causal constraints "significantly affects the covariate dependencies", and that RealCause's post hoc adjustment prevents realistic modelling of a null ATE. This is the authors' own comparison; I found no independent replication.
- **Frugal, Flexible, Faithful: Causal Data Simulation via Frengression** | Linying Yang, Jens Magelund Tarp, Robin J. Evans, Xinwei Shen | arXiv 2025, v2 2026 | [2508.01018](https://arxiv.org/abs/2508.01018) | [ABS]. Overlap 10%. Extends the frugal parameterisation with deep generative models, including time-varying data.
- **Really Doing Great at Estimating CATE? A Critical Look at ML Benchmarking Practices in Treatment Effect Estimation** | Alicia Curth, David Svensson, James Weatherall, Mihaela van der Schaar | NeurIPS 2021 Datasets and Benchmarks | [NeurIPS listing](https://neurips.cc/virtual/2021/29845) | [SEC], foundational. Overlap 10%. The workshop version, [arXiv 2107.13346](https://arxiv.org/abs/2107.13346) [ABS], says IHDP and ACIC2016 characteristics favour some algorithms over others.
- **The Case for Evaluating Causal Models Using Interventional Measures and Empirical Data** | Amanda Gentzel, Dan Garant, David Jensen | NeurIPS 2019 | [1910.05387](https://arxiv.org/abs/1910.05387) | [ABS], foundational. Overlap 5%.
- **Position: Causal Machine Learning Requires Rigorous Synthetic Experiments for Broader Adoption** | Audrey Poinsot et al. | ICML 2025, PMLR 267:81995-82015 | [2508.08883](https://arxiv.org/abs/2508.08883) | [ABS]. Overlap 5%. Argues synthetic experiments are essential.
- **Using Wasserstein Generative Adversarial Networks for the Design of Monte Carlo Simulations** | Susan Athey, Guido Imbens, Jonas Metzger, Evan Munro | [NBER w26566](https://doi.org/10.3386/w26566) | [META], foundational. Not scored.
- A real-data alternative: Zhang subsamples randomised trials (National Supported Work and a social-pressure turnout trial) and compares against full-trial contrasts — [Zhang 2026](https://arxiv.org/abs/2609.26290) [FT].

### Inferences
- A CFM's shrinkage depends on the distance between the true effect and its training prior (Zhang), so detector power depends on the validator's effect-size distribution. Any AUC or power claim should be reported per validator and per effect-size band.
- Frugal Flows' exact ATE control suits a sweep of effect sizes with confounding held fixed. Credence's constraint option is a useful second generator, because disagreement between them would expose generator sensitivity.
- If AIPW is well specified on a validator by construction, the reference looks better than it would on real data, which would flatter the detector.
- Subsampling real RCTs, as Zhang does, gives a design-based reference that avoids generator dependence and should be included.

### Gaps
- Negative result: no paper found that evaluates a diagnostic or detector, rather than estimators, across CREDENCE, RealCause and Frugal Flows.
- Query: "Frugal Flows CREDENCE RealCause synthetic validation causal estimators".

## Prediction-powered inference, rectification, and PFNs inside DML/AIPW: why detect instead of debias?

### Takeaway
Debiasing is the strongest competing idea and now exists for PFNs through Melnychuk et al.'s one-step correction. PPI itself needs labelled outcomes or randomisation, so its direct analogue on observational data is AIPW-style correction. The detector needs an explicit reason to exist alongside these.

### Cited Findings
Direct competitors for CFMs:
- **Frequentist Consistency of Prior-Data Fitted Networks for Causal Inference** | Valentyn Melnychuk, Vahid Balazadeh, Stefan Feuerriegel, Rahul G. Krishnan | ICML 2026, PMLR 306 | [2603.12037](https://arxiv.org/abs/2603.12037) | [FT]. Overlap 35%. The [ICML site](https://icml.cc/virtual/2026/poster/61548) lists a slightly different title ending "for Causal Estimation".
  - Does: shows existing PFNs can have prior-induced confounding bias, so frequentist consistency fails: the implicit prior can "systematically shrink the degree of observed confounding toward zero". Proposes a one-step posterior correction via martingale posteriors, without full retraining, matching A-IPTW asymptotically.
  - Its footnote states this bias "is also referred to as regularization-induced confounding bias". It describes A-IPTW as a first-order bias correction of a plug-in estimator.
  - Differs: corrects rather than detects. Targets confounding shrinkage rather than effect-size attenuation. Needs nuisance posteriors, hence martingale posteriors. Benchmarks are synthetic and semi-synthetic. A [related blog post](https://zuseschoolrelai.de/blog/trusting-uncertainty-causal-foundation-models/) [SEC] says it applies on top of any pretrained PFN.
- **Learning to Fluctuate: Statistical Foundations for Causal Tabular Pretraining** | Zhiheng Zhang | arXiv preprint, September 2026 | [2609.26290](https://arxiv.org/abs/2609.26290) | [FT]. Overlap 35%.
  - Does: argues latent-effect supervision "rewards posterior shrinkage". Fixes it by labelling synthetic tables with ATE plus efficient influence-function fluctuation. Separates per-table orthogonal estimators, frozen PFNs, and downstream corrections such as MP-OSPC and WALDO.
  - Key numbers: at the prior centre, Raw latent-effect has lower RMSE (.0176 versus .0621) "by shrinking toward the training prior", with response slope .214 versus .955. Under effect shift, FSP lowers RMSE 54.2% with slopes .972 versus -.058, and RMSE is 10.19% below CausalPFN-S. On National Supported Work, the post-treatment mean is .0957 against a benchmark of .1106. At n = 256, response slopes are .819 FSP, .951 S-learner, .988 full-fit AIPW, 1.008 cross-fitted DML.
  - Differs: no deployment-time test. "The oracle teacher is used solely to score sampling defect and response slope". Its repeated-mechanism diagnostic (Proposition L.2) needs independent tables from a fixed mechanism. Uses AIPW/DML only as a comparator, with propensities clipped to [.05, .95].
- **Causal Foundation Models** | Christopher Stith, Hossein Rahmani, Jesse C. Cresswell | arXiv tutorial, September 2026 | [2609.03003](https://arxiv.org/abs/2609.03003) | [FT]. Overlap 20%.
  - Reports ATE relative error on Lalonde CPS/PSID: CausalPFN 0.17/0.24, Do-PFN 0.88/0.89, CausalFM 0.94/0.95. Says the near-identical errors with small SEs point "to a systematic shrinkage of the predicted effect toward zero rather than to unstable estimation". Differs: observation, no test.

Prediction-powered inference:
- **Prediction-powered inference** | Anastasios N. Angelopoulos, Stephen Bates, Clara Fannjiang, Michael I. Jordan, Tijana Zrnic | Science 382(6671):669-674, 2023 | [2301.09633](https://arxiv.org/abs/2301.09633) | [ABS], foundational. Overlap 15%. Valid CIs from a small labelled set plus predictions, no assumptions on the ML model.
- **PPI++: Efficient prediction-powered inference** | Anastasios N. Angelopoulos, John C. Duchi, Tijana Zrnic | Ann. Appl. Stat. 20(3):2235-2252, 2026 | [2311.01453](https://arxiv.org/abs/2311.01453) | [ABS]. Overlap 10%.
- **Cross-prediction-powered inference** | Tijana Zrnic, Emmanuel J. Candes | PNAS 121(15), 2024 | [2309.16598](https://arxiv.org/abs/2309.16598) | [ABS]. Overlap 10%.
- **Another look at statistical inference with machine learning-imputed data** | Jessica Gronsbell et al. | arXiv 2024, v7 2026 | [2411.19908](https://arxiv.org/abs/2411.19908) | [ABS]. Overlap 10%. Connects prediction-based inference to two-phase sampling and earlier statistical methods.
- **Prediction-powered Generalization of Causal Inferences** | Ilker Demirel, Ahmed Alaa, Anthony Philippakis, David Sontag | ICML 2024 | [2406.02873](https://arxiv.org/abs/2406.02873) | [ABS]. Overlap 15%. Supplements trial data with an observational prediction model, staying robust when that study is poor. Needs a trial.
- **Prediction-Powered Causal Inferences** | Riccardo Cadei et al. | [NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/hash/6b0a3a259d3dcb75dfe92f7269e2e05e-Abstract-Conference.html) | [2502.06343](https://arxiv.org/abs/2502.06343) | [ABS]. Overlap 10%. Predicts outcomes in unlabelled experiments; it does not rectify a black-box effect estimate.
- **Efficient Randomized Experiments Using Foundation Models** | Piersilvio De Bartolomeis, Javier Abad, Guanbo Wang, Konstantin Donhauser, Raymond M. Duch, Fanny Yang, Issa J. Dahabreh | NeurIPS 2025 | [2502.04262](https://arxiv.org/abs/2502.04262) | [FT]. Overlap 25%. H-AIPW combines AIPW estimators "whose outcome regression models are replaced with foundation models", valid even with arbitrarily biased predictions. Differs: randomised experiments.
- **Semiparametric posterior corrections** | Andrew Yiu, Edwin Fong, Chris Holmes, Judith Rousseau | arXiv 2023 | [2306.06059](https://arxiv.org/abs/2306.06059) | [ABS]. Overlap 10%. Source of the one-step posterior idea used by Melnychuk.

TabPFN or PFNs as nuisance models:
- DoubleML documentation runs `DoubleMLAPOS` with TabPFN as outcome and propensity learners on one simulated dataset (n = 1,000). TabPFN gives nuisance RMSE 8.30/6.86 versus 15.73/18.45 for LightGBM and takes 183 s on CPU versus 3.12 s; other learners were not tuned in detail — [DoubleML docs](https://docs.doubleml.org/stable/examples/learners/py_tabpfn.html) [ABS]. Overlap 15%.
- **TabPFN: One Model to Rule Them All?** | Qiong Zhang, Yan Shuo Tan, Qinglong Tian, Pengfei Li | arXiv 2025 | [2505.20003](https://arxiv.org/abs/2505.20003) | [FT]. Overlap 15%. Uses TabPFN inside S-, T-, X- and DR-learners. Under strong selection, performance degrades, "which we believe is due to the phenomenon of regularization-induced confounding"; the authors borrow BCF's propensity idea. Note this is their stated belief, not a proof.
- **Do-PFN: In-Context Learning for Causal Effect Estimation** | Jake Robertson, Arik Reuter, Siyuan Guo, Noah Hollmann, Frank Hutter, Bernhard Scholkopf | NeurIPS 2025 | [2506.06039](https://arxiv.org/abs/2506.06039) | [FT]. Overlap 10%. Its baselines include "DML (TabPFN)" using TabPFN as base learner.
- **Accurate predictions on small data with a tabular foundation model** | Noah Hollmann et al. | Nature 637(8045):319-326, 2025 | [DOI](https://doi.org/10.1038/s41586-024-08328-6) | [META].
- **A Causal Foundation Model for Structure and Outcome Prediction** (TabPFN-CFM) | Max Zhu, Martino Mansoldo, Ching-Hao Wang, Stefan Groha | ICML 2026 workshop | [2606.26467](https://arxiv.org/abs/2606.26467) | [ABS]. Overlap 5%.
- Context, CFM models with no detector: [CausalPFN](https://arxiv.org/abs/2506.07918) (NeurIPS 2025 per Stith's reference list) reports "calibrated uncertainty" and tunes temperature on observational data; [CausalFM](https://arxiv.org/abs/2506.10914) (ICLR 2026 per Stith's reference list); [BBCI](https://arxiv.org/abs/2503.05985); [CInA](https://arxiv.org/abs/2310.00809). CausalPFN's calibration passages read; [ABS] for the others.

### Inferences
- The rectification analogue: PPI's rectifier needs labels, but counterfactuals are never labelled in observational data. The natural rectifier is cross-fitted AIPW with the CFM as outcome model. That is what H-AIPW does for trials and what Melnychuk does at posterior level.
- The reviewer's strongest objection: the detector already pays for AIPW, so why not report it, or a correction? Defensible answers from the evidence:
  - Unconditional replacement can lose. Shrinkage lowers RMSE near the prior centre (Zhang), and FSP beat S-learner in 16 of 24 cells including all 12 weak-overlap cells, while AIPW-type estimators sit closer to the efficient response.
  - A flag serves audit and triage where no replacement is wanted, for example to decide whether to trust a cheap pass over many subsets (Stith reports CFMs 1 to 2 orders of magnitude faster than tuned learners on CPU).
  - One-step correction needs nuisance posteriors, which is more machinery than a contrast. Runtime comparison is unknown: I did not find one.
- If the flag gates an estimator, it is a pre-test estimator. Yang (non-regularity), Oberst (bias threshold), Guggenberger (size) and Persson (post-selection) all then apply, and evaluation must report the final estimator's MSE and coverage, not only detection accuracy.
- "Cheap" needs qualification. The nuisance cost dominates, and with TabPFN nuisances it may not be small on CPU.

### Gaps
- Negative result: no causal PPI paper found that rectifies a black-box ATE on purely observational data using an AIPW reference and tests the rectifier.
- I did not read Melnychuk's results tables. Whether OSPC restores magnitude under strong effect shift, as opposed to confounding-driven bias, is unverified.
- Queries: "prediction-powered causal inference rectify black-box treatment effect estimate"; "TabPFN nuisance model double machine learning AIPW prior-data fitted network causal effect"; "one-step debiasing causal foundation model TabPFN doubly robust correction CATE influence function pretrained"; "Frequentist Consistency of Prior-Data Fitted Networks for Causal Inference one-step posterior correction"; "Prediction-Powered Causal Inferences Cadei NeurIPS 2025 proceedings; CausalPFN NeurIPS 2025 accepted".

## Regularisation-induced confounding and shrinkage bias

### Takeaway
Regularisation bias and RIC are well established, and CFM-level attenuation is now documented by Stith and Zhang. I found no direct study of large-effect shrinkage in TARNet or Dragonnet style deep CATE estimators. Three distinct shrinkage concepts must be kept separate.

### Cited Findings
- **Regularization and Confounding in Linear Regression for Treatment Effect Estimation** | P. Richard Hahn, Carlos M. Carvalho, David Puelz, Jingyu He | Bayesian Analysis 13(1):163-182, 2018 | [DOI](https://doi.org/10.1214/16-ba1044) | [META], foundational. Overlap 15%. Cited by Melnychuk for RIC.
- **Bayesian Regression Tree Models for Causal Inference: Regularization, Confounding, and Heterogeneous Effects (with Discussion)** | P. Richard Hahn, Jared S. Murray, Carlos M. Carvalho | Bayesian Analysis 15(3):965-1056, 2020 | [1706.09523](https://arxiv.org/abs/1706.09523) | [ABS], foundational. Overlap 15%. Standard response-surface models "can yield badly biased estimates" under strong confounding. Uses the propensity as a covariate, and shrinks heterogeneity deliberately ("shrink to homogeneity").
- **Double/debiased machine learning for treatment and structural parameters** | Victor Chernozhukov et al. | Econometrics Journal 21(1):C1-C68, 2018 | [DOI](https://doi.org/10.1111/ectj.12097), [1608.00060](https://arxiv.org/abs/1608.00060) | [ABS], foundational. Overlap 20%. Naive plug-in of ML estimators "can behave very poorly due to the regularization bias", removed by an orthogonal score and cross-fitting.
- **Adapting Neural Networks for the Estimation of Treatment Effects** (Dragonnet, targeted regularisation) | Claudia Shi, David M. Blei, Victor Veitch | arXiv 2019 | [1906.02120](https://arxiv.org/abs/1906.02120) | [ABS], foundational. Overlap 10%. Fits nuisance networks to favour good downstream estimates. No shrinkage measurement stated in the abstract. Venue not re-verified.
- **On Inductive Biases for Heterogeneous Treatment Effect Estimation** | Alicia Curth, Mihaela van der Schaar | NeurIPS 2021 | [2106.03765](https://arxiv.org/abs/2106.03765) | [ABS], foundational. Overlap 10%. Studies shared-structure strategies. Points the other way: some strategies "implicitly encourage heterogeneity even when it does not exist".
- **In Nonparametric and High-Dimensional Models, Bayesian Ignorability is an Informative Prior** | Antonio R. Linero | JASA 119(548):2785-2798 | [2111.05137](https://arxiv.org/abs/2111.05137) | [ABS]. Overlap 10%. Ignorability implies a prior tightly concentrated around zero selection bias. Supports the mechanism in Melnychuk.
- **Debiased Bayesian inference for average treatment effects** | Kolyan Ray, Botond Szabo | NeurIPS 2019 | [1909.12078](https://arxiv.org/abs/1909.12078) | [ABS], foundational. Overlap 10%. A propensity-based prior modification corrects first-order posterior bias.
- **Double Robust Bayesian Inference on Average Treatment Effects** | Christoph Breunig, Ruixuan Liu, Zhengfei Yu | Econometrica 93(2):539-568, 2025 | [DOI](https://doi.org/10.3982/ecta21442) | [META]. Not scored.
- **Shrinkage Bayesian Causal Forests for Heterogeneous Treatment Effects Estimation** | Alberto Caron, Gianluca Baio, Ioanna Manolopoulou | JCGS 31(4):1202-1214, 2022 | [2102.06573](https://arxiv.org/abs/2102.06573) | [ABS]. Overlap 5%. Feature shrinkage, not effect attenuation.
- CATE-level regularisation shrink: Persson et al. attribute narrowed GATE ranges to regularisation and list "strong regularization" among conditions favouring group bias — [Persson et al. 2026](https://arxiv.org/abs/2602.20383) [FT].
- Meta-learner tutorial: the S-learner "may be biased towards zero" depending on regularisation — [PMC11379759](https://pmc.ncbi.nlm.nih.gov/articles/PMC11379759/) [SEC].
- General neural attenuation outside causal settings: [arXiv 2512.23138](https://arxiv.org/pdf/2512.23138) [SEC].

### Inferences
- Three concepts: (a) confounding shrinkage or RIC, where the prior pulls selection bias toward zero (Hahn, Linero, Melnychuk); (b) effect-magnitude attenuation toward the training prior's centre (Zhang, Stith); (c) heterogeneity shrinkage toward the mean, which can leave the ATE intact (Persson, BCF by design).
- The detector addresses only (b), and only the downward-gap direction. RIC need not bias toward zero, since its direction depends on the confounding. So it can inflate the estimate, which the one-sided test cannot flag, and a report should say so.
- Calling the phenomenon "RIC" would be imprecise and would invite "this is just Hahn et al.". Cite RIC as a neighbouring mechanism.

### Gaps
- Negative result: no paper found that directly measures shrinkage of large effects in TARNet, CFRNet or Dragonnet estimators.
- I did not read Hahn et al. (2018) in full; project Euclid returned an empty page.
- Queries: "deep CATE estimators shrinkage large treatment effects regularization bias underestimate"; "neural network CATE attenuation underestimated effect magnitude TARNet regression to mean calibration slope less than one".

## Overlap diagnostics and abstention

### Takeaway
Overlap diagnostics and abstention are both mature, but I found no accepted rule like "abstain if more than 5% of propensities are extreme". The threshold is ad hoc and should be justified empirically or replaced with a formal bound.

### Cited Findings
Overlap diagnostics and responses:
- **Distribution-Free Assessment of Population Overlap in Observational Studies** | Lihua Lei, Alexander D'Amour, Peng Ding, Avi Feller, Jasjeet Sekhon | manuscript dated July 2021 | [author PDF](https://lihualei71.github.io/ovalue.pdf) | [ABS]. Overlap 25%. Says examining estimated propensities "is heavily dependent on model specification and has poor uncertainty quantification", and proposes O-values, finite-sample upper confidence bounds on propensity extrema. Publication venue not verified.
- **Dealing with limited overlap in estimation of average treatment effects** | R. K. Crump, V. J. Hotz, G. W. Imbens, O. A. Mitnik | Biometrika 96(1):187-199, 2009 | [DOI](https://doi.org/10.1093/biomet/asn055) | [META], foundational. Overlap 15%. Young and Dillon apply its rule and get [0.026, 0.974], which removes 32% of the sample — [Young and Dillon 2026](https://arxiv.org/abs/2601.11845) [FT].
- **Balancing Covariates via Propensity Score Weighting** | Fan Li, Kari Lock Morgan, Alan M. Zaslavsky | JASA 113(521):390-400 | [DOI](https://doi.org/10.1080/01621459.2016.1260466) | [META], foundational. Overlap 5%.
- **Propensity score weighting under limited overlap and model misspecification** | Yunji Zhou, Roland A. Matsouaka, Laine Thomas | Stat. Methods Med. Res. 29(12):3721-3756, 2020 | [2006.04038](https://arxiv.org/abs/2006.04038) | [ABS]. Overlap 5%. Overlap, matching and entropy weights outperform IPW on bias, RMSE and coverage in their simulations.
- **Overlap in observational studies with high-dimensional covariates** | Alexander D'Amour, Peng Ding, Avi Feller, Lihua Lei, Jasjeet Sekhon | J. Econometrics 221(2):644-654, 2021 | [1711.02582](https://arxiv.org/abs/1711.02582) | [ABS], foundational. Overlap 10%. Strict overlap restricts covariate discrepancies more as dimension grows.
- **Diagnosing and responding to violations in the positivity assumption** | Maya L. Petersen et al. | Stat. Methods Med. Res. 21(1):31-54 | [DOI](https://doi.org/10.1177/0962280210386207) | [META], foundational. Not scored.
- **Characterization of Overlap in Observational Studies** | Oberst et al. | AISTATS 2020 | [clinicalml listing](https://clinicalml.org/publication/oberst-2020-overlap/) | [SEC]. Overlap 5%. Boolean-rule description of the overlap region.
- Trimming changes the estimand to an overlap-region effect; pruning "is often more important for credibility" than estimator choice — [Young and Dillon 2026](https://arxiv.org/abs/2601.11845) [FT].

Abstention and rejection:
- **Identifying Causal-Effect Inference Failure with Uncertainty-Aware Models** | Andrew Jesson, Soren Mindermann, Uri Shalit, Yarin Gal | NeurIPS 2020 | [2007.00163](https://arxiv.org/abs/2007.00163) | [ABS], foundational. Overlap 25%. Epistemic uncertainty flags no-overlap and covariate-shift units; a [search summary](https://oatml.cs.ox.ac.uk/publications/202010_JessonMindermannGal2020cate.html) reports that excluding high-uncertainty points outperforms propensity-based baselines [SEC]. Differs: per-unit CATE, uses the model's own uncertainty, no reference.
- **Policy Learning with Abstention** | Ayush Sawarni, Jikai Jin, Justin Whitehouse, Vasilis Syrgkanis | AISTATS 2026, [PMLR v300](https://proceedings.mlr.press/v300/sawarni26a.html) | [2510.19672](https://arxiv.org/abs/2510.19672) | [ABS]. Overlap 10%. Abstention built from disagreement among near-optimal policies, with fast regret guarantees. arXiv's comment says "AISTATS 2025", which conflicts with PMLR and [the AISTATS 2026 site](https://virtual.aistats.org/virtual/2026/poster/10728). Differs: policy learning, not ATE audit. Its disagreement-based rule is conceptually close to using estimator disagreement.
- **Counterfactually Comparing Abstaining Classifiers** | Yo Joong Choe, Aditya Gangrade, Aaditya Ramdas | NeurIPS 2023 | [2305.10564](https://arxiv.org/abs/2305.10564) | [ABS]. Overlap 10%. Relevant to how to score a system that abstains: counterfactual score, doubly robust estimators. Deterministic abstention makes the score unidentifiable.
- **A Causal Target for Learning to Defer Under Hidden Confounding** | Li et al. | AAAI 2026 | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/39493) | [SEC]. Overlap 5%.
- Hussain et al.'s Algorithm 1 rejects estimators but, as written, does not say what happens if all are rejected — [Hussain et al. 2022](https://arxiv.org/abs/2209.13708) [FT].

### Inferences
- Abstaining rather than trimming avoids an estimand change, which is a clean design choice to state.
- The 5% rule depends on estimated propensities, and Lei et al. criticise exactly this. An O-value based rule would be a low-cost upgrade.
- Scoring must condition on non-abstention, with coverage reported alongside. By analogy with Choe et al., whose setting is classifiers, a deterministic 5% rule cannot be scored on abstained cases.
- Tension to disclose: Zhang reports FSP's clearest gains in weak-overlap cells, so abstention may discard cases where a CFM is relatively strongest, although that is FSP versus S-learner and not a released CFM. In the same regime Zhang reports V-hat/V of .328 for raw FSP, so CFM uncertainty is also least trustworthy there.
- Clipping conventions vary ([.05, .95] in Zhang, [0.026, 0.974] data-driven in Young and Dillon). What counts as "extreme" should be justified in the report.

### Gaps
- Negative result: no paper states a share-of-extreme-propensities abstention threshold, and my searches surfaced no consensus cutoff.
- Negative result: I could not identify the "Nie et al." work in the brief. Searches returned no abstention-under-overlap paper by an author named Nie. Insufficient publicly verifiable evidence; the brief's author should confirm the citation. The closest paper for that idea is Sawarni et al.
- Queries: "abstain causal effect estimate poor overlap reject option Jesson identifying causal-effect inference failure uncertainty"; "Policy Learning with Abstention Syrgkanis overlap offline"; "Nie abstain policy poor overlap off-policy learning limited overlap deferral causal estimate selective"; "proportion extreme propensity scores threshold positivity diagnostic rule when to not estimate ATE overlap violation test".

## Equivalence and non-inferiority testing, given the label-null mismatch

### Takeaway
The mismatch is real: the detector's flag rate at exactly 10% shrinkage is set by signal-to-noise, not by the 10% label. I found no paper using TOST to compare an ML or foundation model estimate with a DR reference. For a one-directional label a single margin test is enough; TOST is needed only for a two-sided claim.

### Cited Findings
- **A comparison of the Two One-Sided Tests Procedure and the Power Approach for assessing the equivalence of average bioavailability** | Donald J. Schuirmann | J. Pharmacokinetics and Biopharmaceutics 15(6):657-680, 1987 | [DOI](https://doi.org/10.1007/bf01068419) | [META], foundational. Overlap 10%.
- TOST lets researchers reject a smallest effect size of interest — [Lakens et al. 2018](https://journals.sagepub.com/doi/full/10.1177/2515245918770963) [SEC].
- **From Sample Average Treatment Effect to Population Average Treatment Effect on the Treated: Combining Experimental with Observational Studies to Estimate Population Treatment Effects** | Erin Hartman, Richard Grieve, Roland Ramsahai, Jasjeet S. Sekhon | JRSS-A 178(3):757-778, 2015 | [journal](https://academic.oup.com/jrsssa/article/178/3/757/7058667) | [FT], foundational. Overlap 30%. Equivalence-based placebo tests, where the null is that the data are inconsistent with a valid design and only a low p-value with sufficient power supports it. Compares reweighted RCT and observational outcomes. Differs: treated-group outcome means, RCT required.
- **An Equivalence Approach to Balance and Placebo Tests** | Erin Hartman, F. Daniel Hidalgo | AJPS 62(4):1000-1013, 2018 | [DOI](https://doi.org/10.1111/ajps.12387) | [META], content from [MIT DSpace listing](https://dspace.mit.edu/handle/1721.1/126115) via a search summary [SEC]. Overlap 15%.
- **Nothing to See Here? A Non-Inferiority Approach to Parallel Trends** | Alyssa Bilinski, Laura A. Hatfield | Stat. Med. 45(3-5), 2026 | [DOI](https://doi.org/10.1002/sim.70296) | [META]. Overlap 10%. Non-inferiority logic applied to a causal assumption check.
- **Testing for Equivalence of Pre-Trends in Difference-in-Differences Estimation** | Holger Dette, Martin Schumann | JBES 42(4):1289-1301, 2024 | [DOI](https://doi.org/10.1080/07350015.2024.2308121) | [META]. Overlap 10%.
- De Bartolomeis et al. set tolerance by user choice or sensitivity-model bounds, and estimate the smallest tolerance at which the test no longer rejects, compared with a critical value equal to the absolute subgroup ATE — [De Bartolomeis et al. 2024](https://arxiv.org/abs/2404.18905) [FT].
- Demirel et al.'s "equivalence test" means an exact moment restriction, not a margin — [Demirel et al. 2024](https://arxiv.org/abs/2402.15137) [FT]. The null in Hussain et al. 2023 is also exact zero — [Hussain et al. 2023](https://arxiv.org/abs/2301.13133) [FT].
- Fraction-retention non-inferiority tests whether a new treatment keeps a prespecified fraction of the control's effect. This is the regulatory analogue of "retains at least 90% of the reference effect". Sources: [Hung et al., Stat. Med. 22(2):213-225](https://doi.org/10.1002/sim.1315) [META]; a [PLoS ONE paper on ratios of mean differences](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7282653/) [SEC]; Rothmann et al. 2003, seen only through a [listing](https://data.zhenzhi.com/details/1/908399253) and secondary mentions [SEC]. I did not retrieve the FDA guidance text.
- **Assessing the replicability of RCTs in RWE emulations** | Jeanette Koppe, Charlotte Micheloud, Stella Erdmann, Rachel Heyard, Leonhard Held | arXiv 2024 | [2412.09334](https://arxiv.org/abs/2412.09334) | [ABS]. Overlap 15%. A sceptical p-value for replication, extended to non-inferiority, applied to RCT DUPLICATE. An alternative to agreement metrics.
- Terminology check by text search: "TOST" and "non-inferiority" have zero hits in Demirel 2024, Hussain 2022 and 2023, De Bartolomeis 2024, Persson 2026, Young and Dillon, Melnychuk, Stith and Parikh. "Tolerance" is central only in De Bartolomeis (172 hits). This is my local grep of arXiv PDF text.

### Inferences
All calculations here are mine.
- With t = |tau|/SE_AIPW and the CFM treated as fixed, the probability of flagging a true 10% shrink is Phi(0.1 t - 1.645):

| t | Flag probability at exactly 10% shrink | Shrink detected with 80% power |
|---|---|---|
| 5 | 0.126 | 49.7% |
| 10 | 0.259 | 24.9% |
| 16.45 | 0.500 | 15.1% |
| 20 | 0.639 | 12.4% |
| 30 | 0.912 | 8.3% |
| 50 | about 1.0 | 5.0% |
| 100 | about 1.0 | 2.5% |

- So at low signal-to-noise the detector misses most labelled-positive cases, and at high signal-to-noise it flags shrinkage well under 10%. Reported precision and recall will depend strongly on the benchmark's t distribution. Results should be stratified by t.
- Three statements to keep distinct, with s = sign(AIPW) and all on a fixed-CFM basis:
  - Current test: H0 gap <= 0. Evidence of any shrinkage.
  - Flag test matching the label: H0 shrink <= 10%. Statistic s(0.9 AIPW - CFM)/(0.9 SE_AIPW).
  - Certification test: H0 shrink >= 10%. Statistic s(CFM - 0.9 AIPW)/(0.9 SE_AIPW). Passing this is what would license "not materially shrunk".
- TOST would add a bound on over-estimation, which is needed only if the claim is "close to AIPW" rather than "not attenuated".
- Running flag and certification tests together gives a three-way output: shrunk, not shrunk, inconclusive. Inconclusive is honest for low t, and it answers Hussain's "failure to reject does not imply validity".
- A relative margin is unstable when AIPW is near zero, so it needs an absolute-margin fallback or a further abstention rule. A Fieller-type treatment would be the rigorous version; I did not verify a source applying it here.
- None of these formulas account for the same-data dependence covered in the Hausman section.

### Gaps
- Negative result: no paper found applying TOST or non-inferiority to compare an ML or foundation model causal estimate with a doubly robust reference.
- No source found that gives a principled margin for estimator-versus-reference comparison. The 10% figure has no literature basis that I could find.
- Queries: "equivalence test TOST observational versus randomized estimate causal estimator agreement non-inferiority benchmarking"; "Hartman Hidalgo equivalence approach to balance and placebo tests; Hartman From SATE to PATT equivalence observational experimental"; "RCT-DUPLICATE "estimate agreement" defined within 95% confidence interval of the RCT estimate Franklin Circulation 2021"; "retention of effect non-inferiority fraction preserved margin ratio test Rothmann 2003 FDA guidance".
