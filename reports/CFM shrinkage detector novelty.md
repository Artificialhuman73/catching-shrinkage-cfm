# Redesign the shrinkage test before publishing

**As stated, this objective scores 3.90 out of 10 (Low Novelty). A full redesign could reach about 6.50 (Moderate Innovation), which is a credible journal paper but not a breakthrough.** The niche is real: a 2026 review names automatic detection of prior mismatch as an open need ([Stith et al.](https://arxiv.org/html/2609.03003)), and these searches found no black-box test of a causal foundation model (CFM) against a same-data doubly robust reference. However, the test statistic is old, close to a one-sided Hausman contrast and to [Persson et al.](https://arxiv.org/abs/2602.20383), and the premise does not fit the flagship target, because toward-zero shrinkage is documented in Do-PFN and CausalFM rather than in CausalPFN. **The most decision-relevant finding is that planned Test B should not be run as designed.** On the notebook's data generator, a method doing no adjustment at all lands within 1% of the truth at effect 128, and CausalPFN's code maps an uninformative network output to that same unadjusted answer, so a "no shrinkage" result is nearly guaranteed and would prove little. No valid real-model results exist yet, so nothing below is a finding about how CausalPFN behaves on this design. The cheapest next move is one Colab session on data generators that can reveal the failure, and that result should set the paper's direction.

*Evidence labels.* **Verified**: read in a primary source. **Code reading**: read in source code, not run. **Run**: numerical check actually executed for this report, with no CausalPFN involved. **Derived**: the researchers' own calculation or argument, untested and not checked against a published theorem. **Judgement**: opinion, including every percentage and score. "Not found" means not found in these searches, which were not exhaustive (Google Scholar was not queried and arXiv rate-limited some queries). Four directly relevant preprints appeared in Sep-Oct 2026, so every novelty claim must be rechecked before submission. Cited 2026 papers are preprints unless a venue is given.

## 1. Reformulated objective: a black-box check for attenuated estimates

**Objective.** Build a black-box, deployment-time check that uses only the user's own observational dataset to decide whether a CFM's average treatment effect (ATE) is pulled toward zero by more than a stated margin relative to a cross-fitted AIPW reference, and abstains when poor overlap makes that reference unreliable.

| Element | Summary |
|---|---|
| Problem | CFMs are networks pretrained on many simulated datasets, then applied to a new table without retraining. They answer fast, and users cannot see whether a given answer was pulled toward the training prior. |
| Contribution | A one-sided z-test on the CFM-versus-AIPW gap, an overlap gate and a planted-shrinkage positive control (a deliberately broken case the test must catch). AIPW, augmented inverse probability weighting, combines an outcome model and a treatment model and stays consistent if either is right. It is a doubly robust (DR) estimator. Cross-fitting means each unit is predicted by models trained on other units. |
| Novelty claim | Only the combination and the deployment target: black-box CFM, same-data reference, no RCT, no oracle. Neither the test nor the shrinkage phenomenon is new. |
| Application | Triage: trust a cheap CFM estimate, or fall back to a slower analysis. |
| Methodology | Simulation with known truth. Flag when `z = sign(AIPW) * (AIPW - CFM) / SE_AIPW > 1.645`. Abstain if more than 5% of estimated propensities (treatment probabilities) are below 0.02 or above 0.98. Label `truly_shrunk` when the CFM is more than 10% closer to zero than the true ATE. One data generator (DGP). |
| Expected outcome | Hoped for: about 5% false alarms and rising detection as shrinkage grows, on real models. Realistic today: see sections 6 and 12. |

**Status on 31 Oct 2026**, from the project notebook `shrinkage_detector_round3_gpu.ipynb`, whose figures are its own descriptions (no CSVs were available). Round 1: about 7% false alarms with AIPW set up properly, and CausalPFN barely shrank up to effect 8. Round 2: Test A (fake CFM, independent noise SD 0.05, planted shrink 0-50%, effects 1-8, n 500 and 2000, 30 seeds) worked per the notebook, with no numbers available; Test B was invalid because of a caching bug. Round 3: Test B (real CausalPFN, effects 1-128, n 500 and 2000, noise 1.0 and 0.25, 25 seeds, 700 datasets) **has not been run. There are no valid real-model results.**

## 2. Closest existing research: the test has close relatives, the target does not

Similarity percentages are **judgement, not measurement**. Where the two source notes differed, both values are shown as a range.

| Existing work | Similarity (%) | Differences | Overlap |
|---|---|---|---|
| [Persson et al. 2026](https://arxiv.org/abs/2602.20383), group bias test | 65 | RCT reference only; two-sided; group level; no overlap rule; no CFMs | Model-implied minus reference effect, Wald z, "model-agnostic"; attributes narrowed effects to regularisation shrinkage |
| [Hausman 1978](https://doi.org/10.2307/1913827) (foundational; metadata only) | 60 | Different denominator; efficiency roles inverted, since AIPW is the efficient estimator here | Flags disagreement between two estimators on the same data |
| [Hussain et al. 2022](https://arxiv.org/abs/2209.13708) | 50 | Independent RCT; two-sided; many candidates | Z-type reject rule; "failure to reject does not imply validity" |
| Doubly robust contrast, Robins and Rotnitzky 2001 via [course slides](http://www2.stat.duke.edu/~fl35/teaching/640/Chap3.5_Doubly%20Robust%20Estimation.pdf) (slides only) | 50 | Informal; compares DR with regression and IPW, not a black box | Same-data contrast as a diagnostic |
| [EconML DRTester](https://www.pywhy.org/EconML/_autosummary/econml.validate.DRTester.html), [grf test_calibration](https://www.rdocumentation.org/packages/grf/versions/2.6.0/topics/test_calibration) (docs only) | 45 | Slope, calibration and uplift tests; docs describe no one-sided mean-gap test or abstention | Cross-fitted DR checks of black-box effects; "is the mean prediction correct?" |
| [RCT-DUPLICATE](https://pubmed.ncbi.nlm.nih.gov/33327727/) (abstract) | 40 | RCT reference; two-sided; clinical | Same reference-only interval check |
| [De Bartolomeis et al. 2024](https://arxiv.org/abs/2404.18905) | 40 | RCT reference; kernel statistic; subgroups | One-sided rule with a tolerance, which this detector lacks |
| [Zhang 2026](https://arxiv.org/abs/2609.26290) | 35 | Fixes training; its slope diagnostic needs an oracle | CFM shrinkage as target; AIPW/DML as comparator |
| [Cornish et al.](https://arxiv.org/abs/2301.07210) (abstract) | 35 | Digital twins; different test; no AIPW | "Falsify, do not certify" a black box from observational data |
| [Melnychuk et al. 2026](https://arxiv.org/abs/2603.12037) (ICML) | 30-35 | Corrects rather than tests; targets confounding shrinkage; needs nuisance posteriors | Output of prior-data fitted networks (PFNs, the CFM family) compared with A-IPTW, an AIPW-type estimator; correction term is close to a test statistic (inference) |
| [TCPFN](https://arxiv.org/abs/2606.20889) | 25 | Learned head inside one temporal model; no reference or test | Runtime reliability signal for a CFM |
| [Berti 2026](https://doi.org/10.3390/electronics15194397) (abstract only) | 25 | Gates classical estimators on declared assumptions | Returns an estimate or a "reasoned refusal" |
| [Stith et al. 2026](https://arxiv.org/abs/2609.03003) | 20-25 | Observes shrinkage; proposes no test | Names both the phenomenon and the need |

## 3. Similarity analysis: new in combination, old in every part

A reviewer can map each part to prior work. The statistic is close to Persson's Wald test evaluated on the whole population. Its reference-only denominator matches RCT-DUPLICATE's estimate agreement. Conceptually it is calibration-in-the-large, the question grf's mean coefficient already asks. A Hausman test, for readers new to it, compares two estimators and treats large disagreement as evidence against the assumptions behind one of them. **Treat this detector as belonging to that family, and cite it.** Note too that "Hausman" had zero hits in the 13 ML-era papers checked, so no one was found to have analysed the same-data AIPW version.

What remains different is deployment: one dataset, no RCT, no oracle, aimed at CFM output. Neighbouring diagnostics need true effects ([Zhang](https://arxiv.org/html/2609.26290); [Schulman et al.](https://arxiv.org/html/2610.22770)), need a second study (Hussain, Persson) or live inside one model (TCPFN). The single-dataset property cuts both ways, because AIPW and the CFM share the unconfoundedness assumption (no hidden confounders). The test therefore measures **disagreement, not validity**, and "falsification" should be avoided or qualified.

Three different things are called shrinkage, and they should not be pooled: confounding pulled toward zero ([Melnychuk et al.](https://arxiv.org/html/2603.12037), also known as regularisation-induced confounding); effect magnitude attenuated toward the training prior ([Zhang](https://arxiv.org/abs/2609.26290), Stith); and heterogeneity pulled toward the mean (Persson). The detector addresses only the second, and only in the downward direction.

## 4. Research gap validation: one real gap solved partly, the best one untouched

| Claimed gap | Evidence and papers | Why it still exists | Does the objective solve it? |
|---|---|---|---|
| **G1.** No user-side test of whether one CFM estimate is attenuated | [Stith](https://arxiv.org/html/2609.03003) lists "automatic detection of mismatch between the target DGP and the training prior" as a future property. A full-text scan of 32 CFM-adjacent papers had zero hits for falsification, trust score, abstention, runtime check or shrinkage detection. [Melnychuk's](https://arxiv.org/html/2603.12037v3) diagnostics use prior datasets or true nuisance functions | Counterfactuals are unobserved, and the critique literature only began in 2026 | **Partly.** It gives a one-directional disagreement signal, not a validity check |
| **G2.** No signed CausalPFN error across a wide effect range | Not found. [CausalPFN's ablations](https://arxiv.org/html/2506.07918v2) include no effect-magnitude sweep. [Zhang's Table 3](https://arxiv.org/html/2609.26290) (response slope 1.021 versus 1.026 for AIPW/DML) covers modest effects on Bernoulli outcomes at n=256 | Benchmarks do not reach the range: [ACIC 2016](https://arxiv.org/abs/1707.02641) median effect is 0.68 outcome SD; [ACIC 2017](https://arxiv.org/abs/1905.09515) tops out at an effect-to-noise ratio of 8 | **Not as designed.** Test B cannot separate adjustment from no adjustment (section 6) |
| **G3.** No valid inference for CFM versus reference on shared data, and no margin-based verdict | Not found. "TOST" (two one-sided tests, an equivalence test) and "non-inferiority" had zero hits in nine neighbouring papers. [Persson](https://arxiv.org/abs/2602.20383) calls closed-form SEs "cumbersome" and bootstraps; [Oberst et al.](https://arxiv.org/abs/2205.10467) model the shared-sample covariance | Earlier work mostly had two datasets, so the covariance vanished. CFM asymptotics are unestablished | **No.** Reference-only SE and a zero-gap null |
| **G4.** Which way does each CFM fail? | [CausalPFN's code](https://github.com/vdblm/CausalPFN/blob/b7ed2f1e1d58a83c608d08ced3dee955f0a7c221/src/causalpfn/models/icl_model.py) standardises per arm; [Do-PFN's](https://github.com/jr2021/Do-PFN/blob/HEAD/scripts/transformer_prediction_interface/base.py) and [CausalFM's data script](https://github.com/yccm/CausalFM/blob/HEAD/DATA_standard/normalize_data.py) use one scaling (code reading). No paper found isolating this | The detail is in code, not in the CausalPFN paper text checked | **No.** A one-sided toward-zero test assumes the answer. This is the strongest unclaimed angle |
| **G5.** Control batteries and real positive controls for a detector | No formal planted-shrinkage battery found; no detector evaluated across synthetic validators such as [Credence](https://arxiv.org/abs/2202.04208) found; no independent real-RCT evaluation across effect sizes found | No detector existed to evaluate. No accepted public dataset with effects of many SDs was found | **Partly.** Test A is a start, on one DGP with independent noise |
| **G6.** Abstention for CFM audits | Weak as a gap. Overlap tools are mature ([Lei et al.](https://lihualei71.github.io/ovalue.pdf); [Jesson et al.](https://arxiv.org/abs/2007.00163)). No accepted share-of-extreme-propensities rule was found | The threshold is a local design choice | **Not a source of novelty.** The 5% rule is ad hoc |

## 5. Strengths: real usability, a stated need and complementarity

**It runs without an oracle, an RCT or retraining**, which separates it from the CFM diagnostics above. **The need is on record** in Stith et al., and interest is high: Semantic Scholar returned [64 citing papers for CausalPFN](https://api.semanticscholar.org/graph/v1/paper/arXiv:2506.07918/citations) on 31 Oct 2026. **It complements built-in checks.** Temperature calibration changes intervals but not point estimates (code reading), and CausalPFN's calibrated full-sample intervals [covered the truth in only 20% of ACIC 2016 datasets](https://arxiv.org/abs/2610.22770), so an external reference is justified. Slope tests target heterogeneity while this test targets the mean, so a CFM can pass one and fail the other (inference).

**AIPW is a defensible centre in simple settings:** [Zhang](https://arxiv.org/html/2609.26290) reports response slopes of .988 for AIPW and 1.008 for cross-fitted DML at n=256. **Abstaining rather than trimming** avoids changing the estimand, since [trimming targets an overlap-region effect](https://arxiv.org/abs/2601.11845). Finally, the team already has a positive control and a working T4 pipeline, and found its own caching bug.

## 6. Weaknesses: Test B's "no shrinkage" answer would mean little, and the statistic has three defects

**Planned Test B has very little ability to reveal shrinkage.** Run, using the notebook's exact `simulate()`, with no CausalPFN. Relative bias of the naive difference in means, n=2000, 2000 seeds, in percent:

| Effect | Notebook DGP (`tau = effect*(1+0.5*X4)`, X4 does not affect treatment) | Variant DGP (`tau = effect*(1-0.5*X0)`, X0 drives treatment) |
|---|---|---|
| 1 | +90.33 | +77.81 |
| 8 | +11.30 | -1.24 |
| 32 | +2.83 | -9.71 |
| 128 | +0.72 | -11.82 |

On the notebook's DGP the confounding bias stays near +0.9 in absolute terms while the effect grows, so bias relative to the effect shrinks automatically. Code reading of CausalPFN v0.1.5 (`causalpfn/models/icl_model.py`, lines 139-173 and 298) shows outcomes are z-standardised per treatment arm, and predictions map back as `mean * y1_scale + y1_shift` and `mean * y0_scale + y0_shift`. **An uninformative network output therefore reproduces the difference in means between arms, not zero** (read in code, not run against the checkpoint). Together these suggest a "NO shrinkage" verdict from Test B is nearly guaranteed by design and would not be strong evidence of robustness. In the variant DGP, where effect size is tied to a confounder, failing to adjust produces apparent shrinkage that does not vanish at large effects. **CausalPFN itself has not been run on either variant, so this is a prediction about the design, not a finding about the model.**

Three supporting points. Melnychuk et al. say CausalPFN ["may yield approximately debiased posteriors"](https://arxiv.org/html/2603.12037) when the gap between the ATE and the difference in means is within ±0.25 outcome SDs. Run for this report: on the notebook's DGP that gap is -0.161 at effect 8 and -0.012 at effect 128, so most of the grid sits in that zone (inference). Second, the code changes behaviour when an arm exceeds 1,024 units, and in 37.7% of n=2000 notebook datasets an arm does (run; code reading), so that cell mixes two inference regimes. Third, CausalPFN's prior [draws noise variance uniformly up to the signal variance](https://arxiv.org/html/2506.07918v2), so noise 1.0 and 0.25 probe the easier side (derived).

**The one-sided test looks away from CausalPFN's more likely failure.** With per-arm standardisation, the natural failure is a pull toward the unadjusted difference (derived from code reading). That matches [Melnychuk et al.'s](https://arxiv.org/html/2603.12037) prior-induced confounding bias, and [Mourão et al.'s](https://arxiv.org/html/2603.15928) error tables are consistent with partial adjustment (inference; signed direction unverified). On the notebook's DGP that pull moves a positive estimate up, away from zero, so `z` goes negative and nothing is flagged.

**The null does not match the label.** The test's null is "gap = 0"; the label is "more than 10% shrunk". With `t = effect/SE_AIPW` and the CFM treated as fixed, the chance of flagging exactly 10% shrinkage is Φ(0.1t − 1.645), where Φ is the normal CDF: 12.6% at t=5, 25.9% at t=10, 91.2% at t=30 (derived). So the test misses most labelled cases at low signal and flags trivial gaps at high signal. Because AIPW's SE includes effect heterogeneity, t cannot exceed about 45 at n=500 and 89 at n=2000 on this DGP; at that limit the test flags about 3.7% and 1.8% shrinkage half the time (derived). No literature basis for a 10% margin was found; [De Bartolomeis et al.](https://arxiv.org/abs/2404.18905) set tolerance by user choice or sensitivity bounds.

**The SE uses AIPW alone although both estimators share the data.** The correct variance is Var(AIPW) + Var(CFM) − 2Cov. With r = SD(CFM)/SD(AIPW) and ρ their correlation, the actual size of the "5%" test is 12.2% at r=1, ρ=0; 17.1% at r=2, ρ=0.5; and about 0.01% at r=1, ρ=0.9 (derived). Hausman's shortcut is unavailable because AIPW is the efficient estimator here. The honest reading of today's rule is "the CFM number lies below AIPW's one-sided 95% lower limit", formally valid only if the CFM is independent of AIPW's sample. A fully corrected variance is not a free fix either: under pure linear shrinkage it makes `z` independent of the amount of shrinkage (derived).

**Test A cannot expose that error.** `fake_cfm` adds independent noise (SD 0.05) to the sample truth, so r is near 0 and ρ is 0, the one case where the reference-only SE looks fine.

**The SE and the label target different quantities.** AIPW's SE includes the spread of effects across people, while `truly_shrunk` compares with the sample ATE of that same dataset, whose AIPW error lacks that term (derived). A perfect CFM that returns the sample ATE is the direct check:

[CHECK 2 RESULTS PENDING]

**A flag can mean the reference failed.** On RealCause-Lalonde, a semi-synthetic benchmark built from a job-training study, [Stith](https://arxiv.org/html/2609.03003) reports ATE relative errors of .89/.64 for DR-Learner and .34/.29 for Debiased ML, and [CausalPFN's authors](https://arxiv.org/html/2506.07918) report 1.20/3.64 for Forest DR. These implementations differ from plain cross-fitted AIPW, so this is suggestive only.

**The evidence base is thin.** At 25-30 seeds the [Monte Carlo error](https://arxiv.org/abs/1712.03198v3) on a rejection rate is 4 to 10 percentage points, and zero false alarms in 30 seeds still allows a true rate up to 11.6% (researchers' calculation), so the Round 1 figure of about 7% cannot be told apart from 5%. One DGP cannot support a general claim, since [DGP choice can favour some methods](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/2a79ea27c279e471f4d180b08d62b00a-Paper-round2.pdf). The install is unpinned, and CSVs live in a Colab folder that is cleared on disconnect. "Cheap" is unmeasured, and nuisance fitting dominates the cost. The 5% gate relies on estimated propensities, which [Lei et al. criticise](https://lihualei71.github.io/ovalue.pdf) as model dependent.

## 7. Novelty scores: moderate on deployment, low on method

All scores are judgement under the conservative policy supplied.

| Dimension | Score | Reasoning |
|---|---|---|
| Problem | 5 | Need named by Stith and no direct test found, but [Do-PFN's authors](https://arxiv.org/html/2506.06039), Zhang and Stith already report the phenomenon, and the CausalPFN premise is unsupported |
| Methodological | 4 | A one-sided contrast with a reference SE; 65% similar to Persson. Only the same-data CFM use is new |
| Architectural | 2 | No model proposed; a wrapper around existing estimators |
| Dataset | 2 | One self-written DGP; no new benchmark |
| Algorithmic | 3 | A threshold and a gate; the same-data variance problem is unsolved |
| Practical novelty | 4 | Deployable with no oracle or RCT, but no independent CFM deployment was found (the nearest independent evaluation, [Mourão et al.](https://arxiv.org/abs/2603.15928), is a simulation), and the AIPW it needs is itself an answer |
| Scientific contribution | 3 | No valid real-model result; Test B as designed is close to uninformative |
| Reproducibility | 4 | Public package and seeded code, but unpinned install, no retained results, one past caching bug |

| Innovation check | Class | Why |
|---|---|---|
| New problem | Moderate Innovation | User-side detection is open; the phenomenon itself is not |
| New solution | Incremental | Member of the Hausman and Persson family |
| New architecture | Already Well Explored | None proposed |
| New training strategy | Already Well Explored | None proposed; [Zhang](https://arxiv.org/abs/2609.26290), [Wang et al.](https://icml.cc/virtual/2026/poster/63252) and [Melnychuk, Javurek and Feuerriegel](https://arxiv.org/abs/2610.28314) occupy training-side fixes |
| New optimization | Already Well Explored | None proposed |
| New explainability | Incremental | Flag, no flag or uncertain; says nothing about why |
| New deployment strategy | Moderate Innovation | Runtime black-box audit with abstention was not found for CFMs |
| New evaluation methodology | Incremental | Planted controls are standard ([OHDSI](https://hdsr.mitpress.mit.edu/pub/fxz7kr65)); applying them to a CFM detector is a modest step |

## 8. Weighted overall score: 3.90 out of 10

| Criterion | Weight | Score | Weighted | Basis |
|---|---|---|---|---|
| Problem Originality | 20% | 5 | 1.00 | Section 7 |
| Methodological Innovation | 20% | 4 | 0.80 | Section 7 |
| Technical Contribution | 15% | 3 | 0.45 | No valid real results; two statistical defects |
| Research Gap Coverage | 15% | 4 | 0.60 | G1 and G5 partly; G2, G3 and G4 not |
| Practical Impact | 10% | 4 | 0.40 | Misses the likely failure; few known CFM deployments |
| Publication Potential | 10% | 3 | 0.30 | Not submittable without real-model results |
| Future Research Potential | 5% | 6 | 0.30 | Several open follow-ups, in a crowded field |
| Patent Potential | 5% | 1 | 0.05 | [Likely an abstract mathematical method](https://www.govinfo.gov/content/pkg/FR-2024-07-17/html/2024-15377.htm) |
| **Total** | 100% | | **3.90** | 1.00+0.80+0.45+0.60+0.40+0.30+0.30+0.05 |

The result is robust to reasonable disagreement: adding a full point to each of the four heaviest criteria gives 3.90 + 0.20 + 0.20 + 0.15 + 0.15 = 4.60, still below 5.

## 9. Novelty classification: Low Novelty as stated

**3.90 falls in "below 5: Low Novelty".** This grades the objective as written, with today's evidence. It is not a verdict on the area, which holds real openings (G3 and G4).

## 10. Publication readiness: not yet submittable, with a realistic route through TMLR or JCI

**These probabilities are subjective judgement. No data supports precise figures, so only ranges are given.** No primary acceptance rates were found for most of these venues.

| Route | As it stands | After steps 1-5 | After full plan |
|---|---|---|---|
| IEEE Conference (non-flagship) | 10-25% | 30-50% | 50-70% |
| Springer Conference (PAKDD class) | 5-15% | 20-35% | 35-55% |
| Scopus Journal | 5-15% | 25-40% | 45-65% |
| SCI Journal | Below 10% | 10-25% | 25-45% |
| Patent Potential | Below 5% | Below 5% | 5-10%, narrow technical embodiment only |

| Venue | Status on 31 Oct 2026 | Fit |
|---|---|---|
| [TMLR](https://jmlr.org/tmlr/) | Rolling | **Best fit.** Its criteria state ["novelty of the studied method is not a necessary criterion"](https://jmlr.org/tmlr/acceptance-criteria.html); welcomes systematic robustness studies with actionable lessons |
| [Journal of Causal Inference](https://www.degruyterbrill.com/jci) | Continuous; APC €1,050 | Scope fits. JIF 2.2, CiteScore 3.3 per publisher. SCIE membership not verified on Clarivate, so check it |
| UAI 2027 | No official call found; [2026 deadline was 25 Feb](https://auai.org/uai2026/call_for_papers); [a tracker projects Feb 2027](https://www.opencurious.com/ai-conference-deadlines/uai-2027) | Stretch target after the full plan |
| [CLeaR 2027](https://www.cclear.cc/2027) | 16 Nov 2026 AoE | Not realistic in 16 days without real-model results. Other pages list [different conference dates](https://aip.riken.jp/news/clear2027/?lang=en) |
| [PAKDD 2027](https://easychair.org/cfp/PAKDD2027) (Springer) | 20 Nov 2026, call seen via search summary | Not realistic this cycle |
| [AISTATS 2027](https://virtual.aistats.org/Conferences/2027/CallForPapers) | Closed 6 Oct 2026 | 2028 cycle has no call yet |
| ECML PKDD 2027 (Springer) | Call not verified | Insufficient publicly verifiable evidence |
| IEEE conferences | [ICDM 2026](https://www3.cs.stonybrook.edu/~icdm2026/CallforAppliedTrack/list.htm) closed 6 June 2026; DSAA and others not verified | Insufficient publicly verifiable evidence of a suitable open deadline |
| Workshops | [NeurIPS 2026 suggested date 29 Aug has passed](https://openreview.net/venue?id=NeurIPS.cc); [CausalBench 2026](https://groups.google.com/g/isaim/c/Y87gRmstexg) held, 2027 not found | Watch for 2027 calls |

On patents: *SAP v. InvestPic*, read from a [third-party copy of the opinion](https://hallapproved.com/us/cases/cafc/2018/4523133), held that statistical analysis stays abstract even if groundbreaking; [EPO guidance](https://epo.org/en/legal/guidelines-epc/2025/g_ii_3_3_1.html) requires a technical purpose. This is not legal advice. Consult an attorney before disclosure if patenting matters.

## 11. Risk of reviewer rejection: nine objections to prepare for

| Likely objection | Honest position today | What answers it |
|---|---|---|
| "One-sided Hausman with the wrong variance" | Correct | Cite Hausman; repair variance (step 4) |
| "Persson's test with AIPW" | Largely correct, though Persson says [extending beyond experiments "poses conceptual and technical challenges"](https://arxiv.org/abs/2602.20383) | Claim the single-dataset setting and meet those challenges |
| "Why detect instead of debias? Apply [Melnychuk's correction](https://arxiv.org/abs/2603.12037) or report AIPW" | The strongest objection, and no answer exists yet | Blanket replacement can lose, since [shrinkage lowers RMSE near the prior centre](https://arxiv.org/html/2609.26290) (.0176 versus .0621). A flag suits triage where [CFMs run 1-2 orders of magnitude faster than tuned learners on CPU](https://arxiv.org/abs/2609.03003). Melnychuk's correction needs nuisance posteriors and [reports no coverage rates](https://arxiv.org/html/2603.12037v3). Runtime comparison: not found. Step 9 tests this |
| "Your null does not match your label" | Correct | Margin test (step 4) |
| "CausalPFN does not shrink" | Evidence points that way: code reading, plus [Zhang's Table 3](https://arxiv.org/html/2609.26290) | Steps 2 and 3 |
| "Both estimators assume unconfoundedness" | Correct | Call it an audit of disagreement, never validation |
| "A flag may mean AIPW failed" | Untested | Reference-failure controls (step 5) |
| "One DGP, 25 seeds, easy control" | Correct | Steps 5 and 8, reported in [ADEMP](https://arxiv.org/abs/1712.03198v3) form (the standard simulation reporting template) |
| "Effects of 128 are unrealistic" | [Very large effects are rare and tend to shrink later](https://pubmed.ncbi.nlm.nih.gov/23093165/) | Present as a stress test, in outcome-SD units |

## 12. Recommended improvements: a cheap decisive experiment first, new claims second

**Stop first.** Do not spend GPU time on Test B as configured. Replacing its grid costs about the same runtime and yields an interpretable answer. All effort figures are judgement; runtimes use the notebook's stated 1-1.5 hours for 700 datasets on a T4.

**Candidate claims.** All are hypotheses until run. C0 comes from the design check above; C1-C6 come from the researchers' notes.

| Claim | Statement |
|---|---|
| C0 | Effect-size sweeps with fixed confounding cannot test adjustment |
| C1 | Constant planted effects are uninformative for per-arm-standardising CFMs, so the obvious self-test falsely reassures |
| C2 | Covariate-dependent planted effects give a reference-free "adjustment fraction" that tracks prior-induced confounding bias |
| C3 | Toward-zero attenuation is tied to outcome handling, not to being a CFM |
| C4 | Per-arm standardisation trades toward-zero shrinkage for a pull toward the unadjusted contrast |
| C5 | A margin-based test gives valid verdicts on "shrunk by more than 10%" |
| C6 | Not being flagged does not imply valid coverage |

| # | Step | Effort (T4) | What it adds | Claims |
|---|---|---|---|---|
| 1 | Add the difference in means as a baseline and a design gate: a DGP cell counts only if the naive error clearly exceeds the 10% label. Pin `causalpfn==0.1.5`, record the checkpoint hash [as Zhang did](https://arxiv.org/html/2609.26290), save CSVs to Drive, log the ATE path (S or RA) and arm sizes | 2-3 hours, no GPU | Stops uninformative runs; makes later results citable | C0 |
| 2 | **Anchor experiment on real CausalPFN** (table below): 4 DGPs x effects 1, 4, 32, 128 x n 500 and 2000 x 15 seeds = 480 datasets. Report signed bias and `(CFM - naive)/(truth - naive)`, where 1 is full adjustment and 0 is none. [Low seed counts are defensible for gross bias](https://arxiv.org/abs/1712.03198v3), not for rejection rates | Half a day; 40-65 min GPU | **Decides the paper's direction** | C0, C4 |
| 3 | Recompute signed ratios from [the public Stith CSV](https://github.com/layer6ai-labs/cfms/tree/main/data). Then run Do-PFN and CausalFM through [the `cfms` wrappers](https://github.com/layer6ai-labs/cfms) on step 2's DGPs and RealCause-Lalonde | 2 hours, then 2-4 days | **Real positive controls** | C3 |
| 4 | Repair the statistic. Replace the zero null with a non-inferiority margin (test "shrunk by more than 10%" rather than "any gap"), giving a three-way verdict: shrunk, not shrunk, inconclusive. Report both directions. Fix variance by sample splitting (simple, less power) or a rectifier test (below). Justify the 5% gate or replace it with [O-values](https://lihualei71.github.io/ovalue.pdf) | 1-2 person-weeks, mostly CPU | Statistical validity; removes two objections | C5 |
| 5 | Rebuild controls. Negative: oracle-based estimator, well-specified regression, zero-effect data. Positive: planted shrink built from AIPW itself so it is correlated, sweeping r and ρ; ridge S-learner; difference in means. Reference failure: misspecified nuisances, poor overlap. Use [at least 500 seeds at the null and 250-500 on power curves](https://arxiv.org/abs/1712.03198v3) on a small core grid, reusing each dataset across methods | About 1 person-week; CPU across sessions | Credible size and power (Monte Carlo error about 1 percentage point at the null) | C5 |
| 6 | Metamorphic audit (change the data in a way with a known effect on the right answer, then check the output): run the relation table once per model, then build the planted-effect self-test with `Y + delta(X)*T` | 2-3 person-weeks; under 1 min per dataset | **Novelty core** | C1, C2 |
| 7 | Mechanism test: wrap Do-PFN and CausalFM in per-arm standardisation, and check whether toward-zero attenuation drops and naive pull rises | 1-2 person-weeks | Explains why models differ | C3, C4 |
| 8 | External evidence: [OSRCT](https://proceedings.mlr.press/v139/gentzel21a.html) (subsampling a real RCT to create confounding with a known answer) on the Hillstrom marketing and NSW job-training RCTs; [ACIC 2017](https://arxiv.org/abs/1905.09515) factorial; IHDP-100 [stratified by effect spread](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/2a79ea27c279e471f4d180b08d62b00a-Paper-round2.pdf). Declare which are confirmatory | 1-2 person-weeks | Generalisation beyond one DGP | All |
| 9 | Detect versus debias: compare flag-then-fallback, plain AIPW and CFM-inside-AIPW on final MSE and coverage. A gating flag is a [pretest estimator](https://arxiv.org/abs/2005.10579), so detection accuracy alone is not enough | About 1 person-week | Answers the main objection; no coverage study of CausalPFN inside AIPW was found | C6 |
| 10 | Write up in ADEMP form, measure runtime for the "cheap" claim, and **rerun the novelty search just before submission** | About 1 person-week | Submission readiness | All |

Steps 1-5 are the minimum core, about 3-4 person-weeks. The full plan is roughly 9-13 person-weeks.

**Step 2 grid.** Naive relative bias in percent, n=2000. The first two rows are from the 2000-seed check above. The last two were run for this report with 500 seeds, difference in means only, no CausalPFN. "Gap" is ATE minus difference in means, per outcome SD.

| DGP | Change to `simulate()` | Effect 1 | Effect 8 | Effect 128 | Gap at 128 | What it can reveal |
|---|---|---|---|---|---|---|
| Notebook | None | +90.33 | +11.30 | +0.72 | -0.012 | Serves as a design control; little at large effects |
| Tau on confounder | `tau = effect*(1-0.5*X0)` | +77.81 | -1.24 | -11.82 | 0.213 | No adjustment looks like lasting shrinkage |
| Flipped confounding | `score = -score` | -89.88 | -11.28 | -0.75 | 0.012 | Under-adjustment looks like shrinkage at small effects; add effect 2 |
| Scaled confounding | `mu0 = mu0 - effect*X0` | +40.48 | -38.12 | -48.65 | 0.461 | **Sharpest test:** the gap stays outside Melnychuk's ±0.25 zone at large effects |

**How to read step 2.** If CausalPFN tracks the naive contrast in the last three rows, adopt the "attenuation toward an anchor" framing and continue. If it stays near the truth where the naive method fails, that is a citable robustness result that today's Test B could never deliver, and detection should target Do-PFN and CausalFM. If it moves toward zero as effects grow, the original premise survives. If time allows, add a cell with noise above arm-level signal and record the spread of unit-level effect estimates, since heterogeneity shrinkage can grow while the ATE stays correct (derived).

**Real positive controls (step 3).** Do-PFN and CausalFM are natural candidates. [Stith et al.](https://arxiv.org/html/2609.03003) report relative errors of .88/.89 and .94/.95 on Lalonde CPS/PSID against .17/.24 for CausalPFN, reading them as shrinkage from unsigned errors. The researchers' own calculation from [the public CSV](https://github.com/layer6ai-labs/cfms/tree/main/data), not re-run, gives mean estimate-to-truth ratios of .058/.053 for CausalFM, .116/.113 for Do-PFN and .973/.763 for CausalPFN. Three cautions apply. S-, X- and DR-learners also show low ratios on CPS, so this is not CFM-specific. [Lalonde has little overlap](https://github.com/layer6ai-labs/cfms/blob/main/docs/LALONDE_DATASET.md), so it tests abstention as much as detection. And neither Do-PFN nor CausalFM has been tried on T4 by the researchers.

**Rectifier test (step 4, researchers' derivation, not checked against a published theorem).** Plug the CFM's own outcome predictions into AIPW's correction term. AIPW minus the CFM plug-in then becomes a sample mean, testable with its own empirical variance, which handles shared data by construction. It is a frequentist cousin of Melnychuk's correction and must cite it. It needs light wrapping of a private method, and [PFN convergence rates are unproven](https://www.marcel-neunhoeffer.com/pdf/papers/neunhoeffer_learning-from-small-data.pdf).

**Planted-effect arm (step 6, researchers' proposal, untested).** Adding a known `delta(X)` to treated outcomes changes the sample ATE by exactly the mean of `delta(X)`. With shift as the observed change in the estimate, adjustment fraction = (shift − E[δ | T=1]) / (mean δ − E[δ | T=1]), where 1 means full adjustment and 0 means the model behaves like the naive contrast. Constant effects, `Y*c` and `Y+c` are vacuous for CausalPFN (code reading), so the obvious self-tests have no power. Limits: it measures response, not absolute bias, so it complements rather than replaces AIPW. Do not bootstrap X and T together ([Shaw et al.](https://arxiv.org/abs/2504.11740)), and pitch it as falsifying one property, not choosing a best estimator ([Advani et al.](https://arxiv.org/abs/1809.09527)). The prior art must be cited: [DoWhy's dummy outcome refuter](https://github.com/py-why/dowhy/blob/main/dowhy/causal_refuters/dummy_outcome_refuter.py) and [OHDSI's synthetic positive controls](https://hdsr.mitpress.mit.edu/pub/fxz7kr65).

**Revised objective, subject to step 2.** "An audit for causal foundation models that combines reference-free, covariate-dependent planted effects with an AIPW rectifier test and a non-inferiority margin, identifies each model's attenuation anchor, and is validated on CausalPFN, Do-PFN, CausalFM and classical comparators on simulated data and on observational samples drawn from RCTs."

**Avoid leading with** a new repair method (crowded), a full failure taxonomy (3-5 person-weeks, partly occupied by Stith) or an agent guardrail (no agent was found that calls a CFM). Keep the last as a future-work line.

## 13. Estimated novelty after improvements: 5.20 for repairs alone, 6.50 for the full plan

Both are judgement, and both assume the work succeeds.

| Criterion | Weight | Steps 1-5: score | Weighted | Full plan: score | Weighted |
|---|---|---|---|---|---|
| Problem Originality | 20% | 6 | 1.20 | 7 | 1.40 |
| Methodological Innovation | 20% | 5 | 1.00 | 7 | 1.40 |
| Technical Contribution | 15% | 5 | 0.75 | 6 | 0.90 |
| Research Gap Coverage | 15% | 6 | 0.90 | 7 | 1.05 |
| Practical Impact | 10% | 5 | 0.50 | 6 | 0.60 |
| Publication Potential | 10% | 5 | 0.50 | 7 | 0.70 |
| Future Research Potential | 5% | 6 | 0.30 | 7 | 0.35 |
| Patent Potential | 5% | 1 | 0.05 | 2 | 0.10 |
| **Total** | 100% | | **5.20** | | **6.50** |

Steps 1-5: 1.20+1.00+0.75+0.90+0.50+0.50+0.30+0.05 = **5.20, Incremental Research**. Full plan: 1.40+1.40+0.90+1.05+0.60+0.70+0.35+0.10 = **6.50, Moderate Innovation**. Reaching 7.0 would take, for example, a checked theorem for the rectifier test (Technical 6 to 8, +0.30) and evidence of real-data use (Practical 6 to 8, +0.20). That is a target, not a forecast. If C1-C4 fail, the fallback is a systematic robustness study for TMLR, with novelty staying near 5.

## 14. Final verdict: worth pursuing, but not in its current form

**Novel?** Narrowly. The deployment setting was not found in earlier work, but the statistic was, and the field is moving monthly. **Publishable?** Not today, because there is no valid real-model result and the statistic has known defects. After steps 1-5 it suits a lower-tier conference or a careful evaluation paper; with the full plan, TMLR or the Journal of Causal Inference are realistic. **Impactful?** Modestly, with one exception worth more than the detector itself: the finding that effect-size sweeps and constant planted effects may test nothing for models that standardise per arm, which would warn every future CFM evaluator, if step 2 and step 6 confirm it.

The team's most valuable position is not a sharper shrinkage alarm but a tool that reveals which way a given CFM fails. Replace Test B's grid with the four-DGP anchor experiment before using any more GPU time, and let that one session decide what the paper claims.

## Addendum: round 4 results (1 Nov 2026)

Run, not predicted. Code: `round4_core.py`, `shrinkage_detector_round4_gpu.ipynb`, `round4_controls_cpu.py`; numbers in `results/round4/summary.md` and `OVERNIGHT_PLAN.md`.

- **Check 2 (pending above) is superseded** by the controls below.
- **Metamorphic audit (real CausalPFN, 40 datasets):** Y×10, Y+100 and Y+c·T are followed exactly, so these self-tests carry no information about adjustment. This confirms claim C1.
- **Anchor experiment (real CausalPFN, 1,440 datasets, 4 simulators, effects 1–128):** no run was more than 10% off at effects of 4 and above; at 128 every run was within 1.1%. At effects 1–2 the error (3–10%) follows the naive contrast in sign, consistent with partial adjustment (C4) rather than shrinkage toward zero. The original shrinkage premise is not supported for CausalPFN on these simulators.
- **Planted-effect self-test:** after replacing a flawed first version, it scores AIPW 1.01 and T-learner 0.96 (median, 800 datasets) and CausalPFN 0.96 (80 datasets), with naive at 0 by construction. This supports C2.
- **The reference was the weak link:** with boosted-tree propensities AIPW erred −46.5% at effect 1 (n=500) against +1.4% with true propensities, and abstained on 10% of datasets. A degree-2 logistic propensity model removed the abstentions; caveat: it is correctly specified for this simulator.
- **Detector controls (500/200 seeds):** the round 3 z-test flags 60% of runs at only 10% shrinkage; the margin test holds its rate at the boundary (1.5%) with 62% power at 20%; the rectifier test is most powerful (78% at 20%) but over-flags at the boundary (11.7%). With both AIPW models misspecified, false flags were 93% (z-test), 45% (margin), 0.1% (rectifier).
- **Revised framing:** the strongest contributions are now the negative design result (effect-size sweeps and constant plants cannot test per-arm-standardising CFMs), the validated reference-free planted-effect self-test, and the evidence that the classical reference, not the CFM, dominated detector error. Do-PFN and CausalFM remain the natural real positive controls.
