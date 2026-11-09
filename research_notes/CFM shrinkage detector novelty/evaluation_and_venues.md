# Evaluation evidence, benchmarks and venues for a CFM shrinkage diagnostic

Research date: 2026-10-31. Objective under review: a cheap, model-agnostic diagnostic that detects shrinkage in causal foundation models (e.g. CausalPFN) by comparing them with a cross-fitted AIPW reference using a one-sided z-test, abstaining under poor overlap. Current evidence: one synthetic DGP, 6 covariates, nonlinear confounding, heterogeneous effects, effect sizes 1-128, n = 500 and 2000, noise SD 1.0 and 0.25, 25-30 seeds per cell. No real-model results yet.

Evidence tags used throughout:
- **[P]** primary source text read directly (paper PDF or source, official page, code).
- **[P*]** primary source, but seen only through a search summary or snippet, not opened by me.
- **[S]** secondary source (aggregator, law-firm commentary, bookseller listing, third-party tracker).
- **[C]** computed by me from a cited formula.
- Anything else is an explicit inference or gap. Foundational items (pre-2024) are labelled **foundational**.

---

## Simulation study standards: ADEMP, neutrality, replications, Monte Carlo error, simulator bias

### Takeaway
ADEMP plus reported Monte Carlo SEs is the accepted baseline, and n_sim should be derived from a target MCSE. At 25-30 seeds the MCSE on a rejection rate is 4 to 9 percentage points, which cannot support a claim of type I error control. Causal benchmark critics (Curth et al.) add that a single DGP cannot support a general claim, because DGP choice largely decides who wins.

### Cited Findings

**ADEMP and Monte Carlo error (foundational)**
- Morris, White and Crowther, "Using simulation studies to evaluate statistical methods", Statistics in Medicine 38(11):2074-2102, 2019, DOI 10.1002/sim.8086, sets out Aims, Data-generating mechanisms, Estimands, Methods, Performance measures. [P] (LaTeX source of [arXiv 1712.03198](https://arxiv.org/abs/1712.03198v3), downloaded and read; journal metadata from [UCL record](https://discovery-pp.ucl.ac.uk/id/eprint/10066118)).
- Coverage/rejection MCSE is sqrt(p(1-p)/n_sim); bias MCSE is sqrt(Var(theta_hat)/n_sim); EmpSE MCSE is EmpSE/sqrt(2(n_sim-1)). The paper's worked figure: for 95% coverage with required MCSE 0.5 percentage points, n_sim = 95*5/0.5^2 = 1,900; worst case (50%) needs 10,000. Its own example uses 1,600 repetitions, chosen to get bias MCSE below 0.005, giving coverage MCSE 0.54 at 95% and 1.25 at 50%. [P] [arXiv 1712.03198](https://arxiv.org/abs/1712.03198v3)
- It says a similar expression applies for power, and advises to "Choose a value of n_sim that achieves acceptable Monte Carlo SE for key performance measures". [P] [same source](https://arxiv.org/abs/1712.03198v3)
- Review of 100 Statistics in Medicine vol. 34 articles: 93 did not mention Monte Carlo SEs; 4 did not report n_sim; of the 87 reporting n_sim only 4 justified it (their tally of 87 vs 4 missing is as printed); common values were n_sim = 500 and 1,000. [P] [same source](https://arxiv.org/abs/1712.03198v3)
- The tutorial notes that "only one repetition" can suffice when demonstrating large-sample bias many SEs from truth. So a low n_sim can be defended for gross bias claims, not for rejection rates. [P] [same source](https://arxiv.org/abs/1712.03198v3)
- It recommends including "methods with known properties" as a check that those properties appear, using the same simulated data for all methods (paired comparison), and setting the seed once and storing RNG states. [P] [same source](https://arxiv.org/abs/1712.03198v3)

**MCSE arithmetic for this project** [C], from the formula above:

| n_sim | MCSE at p=0.05 | MCSE at p=0.50 | MCSE at p=0.80 |
|---|---|---|---|
| 25 | 4.36 pp | 10.00 pp | 8.00 pp |
| 30 | 3.98 pp | 9.13 pp | 7.30 pp |
| 100 | 2.18 pp | 5.00 pp | 4.00 pp |
| 250 | 1.38 pp | 3.16 pp | 2.53 pp |
| 500 | 0.97 pp | 2.24 pp | 1.79 pp |
| 1000 | 0.69 pp | 1.58 pp | 1.26 pp |
| 1900 | 0.50 pp | 1.15 pp | 0.92 pp |

- Required n_sim: type I error at 5% with MCSE 1 pp = 475; with MCSE 0.5 pp = 1,900; power at 80% with MCSE 2 pp = 400; with MCSE 1 pp = 1,600. [C]
- Zero false rejections in 30 seeds still has a 95% Clopper-Pearson upper bound of 11.6% (13.7% for 25 seeds; 1.5% for 250; 0.37% for 1000). [C]

**More recent guidance (2024-present)**
- Siepe, Bartoš, Morris, Boulesteix, Heck and Pawel, "Simulation Studies for Methodological Research in Psychology: A Standardized Template for Planning, Preregistration, and Reporting", Psychological Methods, 2024, DOI 10.1037/met0000695: ADEMP-PreReg template plus formulas for MCSE and for n_sim given a target MCSE. Their review of 321 articles found 100 (31.2%) with a simulation study and frequent omission of n_sim rationale and Monte Carlo uncertainty. [P*] [MCML record](https://mcml.ai/publications/sbm+24/); [Marburg note](https://www.uni-marburg.de/en/fb04/team-heck/news/news/new-preprint-on-simulation-studies-in-psychology)
- Heinze, Boulesteix, Kammer, Morris and White, "Phases of methodological research in biostatistics", Biometrical Journal 66(1):2200222, 2024, DOI 10.1002/bimj.202200222: Phase I (idea, reasoning, proofs), II (empirical evidence in a narrow target setting), III (wider settings and outcomes), IV (when preferred over alternatives). They say too many methods stop before III and IV. [P*] [arXiv 2209.13358](https://arxiv.org/abs/2209.13358v1)
- Pawel, Kook and Reeve, "Pitfalls and potentials in simulation studies: Questionable research practices in comparative simulation studies allow for spurious claims of superiority of any method", Biometrical Journal 2023, e2200091: illustrated with a novel method that has no expected gain; recommends preregistered protocols, rewarding neutral studies, and sharing code and data. [P] [arXiv 2203.13076](https://arxiv.org/abs/2203.13076)
- Friedrich and Friede, "On the role of benchmarking data sets and simulations in method comparison studies", Biometrical Journal 2024, 66:2200212 (journal reference via secondary record): comparisons are often "not neutral but favour a novel method"; argues for combining simulation and benchmarks. [P] abstract at [arXiv 2208.01457](https://arxiv.org/abs/2208.01457); journal details [S] [Augsburg repository](https://opus.bibliothek.uni-augsburg.de/opus4/frontdoor/index/index/docId/102296)
- Siepe et al. preprint (February 2026), "Why, When, And How To (Or Not To) Preregister A Simulation Study": preregistration benefits late-phase studies of mature methods more than early-phase studies of new methods. Preprint, not peer reviewed. [S] [Marburg news](https://www.uni-marburg.de/en/fb04/team-heck/nachrichten-und-termine/nachrichten/neuer-preprint-why-when-and-how-to-or-not-to-preregister-a-simulation-study)

**Simulator bias in causal benchmarks**
- Exact citation correction: Curth, Svensson, Weatherall and van der Schaar, "Really Doing Great at Estimating CATE? A Critical Look at ML Benchmarking Practices in Treatment Effect Estimation", NeurIPS 2021 Datasets and Benchmarks. **Foundational.** [P] [PDF](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/2a79ea27c279e471f4d180b08d62b00a-Paper-round2.pdf). Do not confuse with the workshop paper by Curth and van der Schaar, "Doing Great at Estimating CATE? On the Neglected Assumptions...", ICML 2021 NACI workshop. [P] [arXiv 2107.13346](https://arxiv.org/abs/2107.13346)
- Findings: IHDP-100 is "not one dataset". CATE spread sigma_tau ranges from 0.04 to 51.51 across the 100 realizations because the exponential surface differs per run, even though ATT is fixed by an offset. Averaged RMSE is dominated by the few runs with very large sigma_tau, so they suggest normalized RMSE or paired test statistics. They use this to question what TARNet's lead over causal forest (RMSE 0.88 vs 3.8 in Shalit et al.) really shows. ACIC2016 shows the same systematic favouring. [P] [same PDF](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/2a79ea27c279e471f4d180b08d62b00a-Paper-round2.pdf)
- They also argue downstream metrics (finding drivers of heterogeneity, correct treatment rules) matter, and that good RMSE does not imply good performance on these. They ran 5 seeds per model on each of 100 IHDP draws. [P] [same PDF](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/2a79ea27c279e471f4d180b08d62b00a-Paper-round2.pdf)
- Yu and Sun, "Do Contemporary Causal Inference Models Capture Real-World Heterogeneity? Findings from a Large-Scale Benchmark", ICLR 2025: 16 CATE models, 12 RCT-derived datasets, 43,200 sampled variants; 62% of CATE estimates have higher MSE than a zero-effect predictor; in datasets with a useful estimate, 80% have higher MSE than a constant-effect model. They deliberately chose datasets whose outcomes come "from field rather than simulation". [P] [arXiv 2410.07021](https://arxiv.org/abs/2410.07021); venue [P*] [ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/file/e1194b07221de8783a02087bb899d69f-Paper-Conference.pdf)
- Gentzel, Pruthi and Jensen, ICML 2021 (**foundational**): OSRCT creates observational-like samples from RCTs with unbiased effect estimates; across 37 datasets from RCTs, simulators, computational systems and synthetic-response data, performance differs noticeably by data source. [P] [arXiv 2010.03051](https://arxiv.org/abs/2010.03051v2)

**Replication counts actually used in accepted papers**
- Karlsson and Krijthe, ICML 2025: 250 repetitions per point. [P] [arXiv 2502.06231](https://arxiv.org/html/2502.06231v2)
- Hussain et al., AISTATS 2023: 100 simulations per setting. [P] [ar5iv 2301.13133](https://ar5iv.labs.arxiv.org/html/2301.13133)
- De Bartolomeis et al., UAI 2024: mean and SE over 5 runs in the figure read. [P] [arXiv 2404.18905](https://arxiv.org/html/2404.18905v2)
- ACIC 2016: 100 per scenario, 7,700 total. [P] [Dorie et al.](https://arxiv.org/abs/1707.02641). ACIC 2017: 250 per DGP, 8,000 total. [P] [Hahn et al.](https://arxiv.org/abs/1905.09515)

### Inferences
- The current 25-30 seeds per cell is below every test-calibration precedent above except De Bartolomeis et al. For this diagnostic, the headline claim is a rejection rate, so a defensible target is at least 500 per cell at the null and 250-500 on power curves, justified explicitly by target MCSE. If real-model inference is slow, use a small core grid at high n_sim and a sparse grid elsewhere, using the same datasets for all methods.
- A paper with one DGP sits at Heinze Phase II at best. Moving to publishable evidence means Phase III: several DGP families, including at least one the authors did not design.
- Report ADEMP explicitly and consider preregistering the design. Given Siepe et al. (2026), preregistration is optional for a new method, but it answers the Pawel et al. objection because the authors are also the method's developers.
- Curth's heavy-tail finding applies directly: aggregate detector results by sigma_tau stratum, not one mean across IHDP-100.

### Gaps
- No causal-ML venue publishes a numeric n_sim requirement that I could find. "Reviewers expect" here is inferred from tutorials, CFP wording and accepted-paper practice, not a stated rubric.
- I did not read the full text of Siepe et al. 2024 or Heinze et al. 2024, only record pages and abstracts. Their specific checklists are not verified here.

---

## Benchmarks where large or known effects can be studied

### Takeaway
No established benchmark I checked natively reaches the project's range (effect 128 with noise SD 1.0 or 0.25, i.e. 128 to 512 noise SDs). ACIC 2016 has median SATT of 0.68 outcome-SD, and ACIC 2017's largest factor ratio is effect 2 to noise 0.25, i.e. 8 [C]. Effect injection on top of these benchmarks is therefore needed. The RealCause scale knob rescales both potential outcomes, so it probably does not test what the diagnostic needs (see the scale-invariance section).

### Cited Findings

| Benchmark | What it is, key facts | Known criticism | Manipulating scale/effect | Availability | Status |
|---|---|---|---|---|---|
| **IHDP-100** (Hill 2011, JCGS 20(1):217-240) | Semi-synthetic on real RCT covariates (747 units in common usage; covariate count varies by paper) with simulated outcomes. Used by CausalPFN (100 realizations). | Curth et al.: heavy tail, sigma_tau 0.04-51.51, surface favours some learners. | Natural variation in sigma_tau; can replace outcome using npci settings A or B, or inject k*tau(x). | [vdorie/npci](https://github.com/vdorie/npci) cited by secondary sources; `ihdp_npci_1-100.{train,test}.npz` ship in the [CausalPFN repo](https://github.com/vdblm/CausalPFN) | Curth [P]; repo [P]; sample size [S] [CRAN bartcs](https://search.r-project.org/CRAN/refmans/bartcs/html/ihdp.html) |
| **ACIC 2016** (Dorie et al., Statistical Science 34(1):43-68, 2019) | 77 scenarios x 100 = 7,700 realizations. | Curth: favours some algorithms. Heterogeneity SD/outcome SD 0-2.06, quartiles 0.47, 0.73, 1.01. Median SATT 0.68 SD (IQR 0.57-0.79). No direct magnitude knob despite the call describing one. | R generator allows re-simulation; effects reported in outcome-SD units. | [vdorie/aciccomp](https://github.com/vdorie/aciccomp) (`aciccomp2016` R package); causallib mirror used by CausalPFN | [P] [arXiv 1707.02641](https://arxiv.org/abs/1707.02641); repo [P] |
| **ACIC 2017** (Hahn et al. 2019) | 32 DGPs x 250 = 8,000 datasets, targeted selection, n = 4,302 fixed covariates. | "95% nominal coverage is achieved by no method". Only known-function DGPs. | **Explicit factors:** effect magnitude xi in {1/3, 2}; noise eta in {0.25, 1.25}; selection strength. Closest to the project's noise levels. | `generate_data.R` provided with files; aciccomp repo has a `2017` folder (contents not described on the page) | [P] [arXiv 1905.09515](https://arxiv.org/abs/1905.09515) |
| **ACIC 2018 / LBIDD** (Shimoni et al. 2018) | IBM framework; covariates from Linked Births and Deaths Data; simulated treatment, effects, censoring; scaling and censoring evaluation tracks. | Not separately reviewed here. | Simulation parameters; effect-size knob not verified. | [GitHub](https://github.com/IBM-HRL-MLHLS/IBM-Causal-Inference-Benchmarking-Framework) has only a sample; full data on Synapse (Apache 2.0 for repo) | [P] |
| **ACIC 2019** | Low- and high-dimensional tracks, 3,200 datasets each, ATE and 95% CI, binary or continuous outcome, near-positivity violations. | Not reviewed here. | DGP R code released August 2019. | [Challenge site](https://sites.google.com/view/acic2019datachallenge/home) | [P] |
| **ACIC 2022** (Thal and Finucane) | Health-policy style panel data; 3,400 datasets = 200 x 17 DGPs. Tree-based methods did best; model-based intervals beat bootstrap. | Panel design, not iid tabular; poor direct fit to CausalPFN's API (inference). | Not verified. | Official site `acic2022.mathematica.org` did not resolve on 2026-10-31. Availability: Insufficient publicly verifiable evidence. | [P*] [Causal Methods Madness](https://muse.jhu.edu/article/895650); counts and findings as reported by a later paper [S] [arXiv 2511.23085](https://arxiv.org/pdf/2511.23085) |
| **Jobs/LaLonde** (LaLonde 1986; Dehejia-Wahba) | Real RCT plus CPS/PSID comparison. DW experimental benchmark $1,794. NSW: 297/425; DW: 185/260. | Imbens and Xu: overlap matters most; estimates can be robust but not valid; placebo tests are essential, goodness of fit is inadequate. | Real outcome in dollars, useful for a scale sanity check. Ratio of effect to outcome SD not extracted here. | [NBER page](https://users.nber.org/~rdehejia/nswdata.html); Imbens and Xu replication [openICPSR 232201](https://www.openicpsr.org/openicpsr/project/232201/version/V1/view) | [P]; JEP 39(4):173-202, 2025 via [RePEc](https://econpapers.repec.org/RePEc:aea:jecper:v:39:y:2025:i:4:p:173-202) [S] and [arXiv 2406.00827](https://arxiv.org/abs/2406.00827) [P] |
| **RealCause** (Neal, Huang, Raghupathi) | Generative models fit to real data; LaLonde PSID/CPS, Twins, IHDP, LBIDD. Used by CausalPFN and Do-PFN. | Generative fit is itself a model; Twins treatment selection is simulated. | Overlap, heterogeneity and **causal effect scale** knobs. Scale knob is Y(t)' = s*Y(t)/tau, i.e. rescales both potential outcomes. | [bradyneal/realcause](https://github.com/bradyneal/realcause), MIT; 100 samples per dataset; fitted models | [P] [arXiv 2011.15007](https://arxiv.org/abs/2011.15007) |
| **Twins** (Louizos et al. 2017, CEVAE) | US twin births 1989-1991; treatment is being heavier twin, outcome first-year mortality; sub-2kg same-sex twins. Sample size varies by paper (5,271 and 11,984 reported). | Binary outcome; preprocessing inconsistent across papers; treatment selection is simulated in RealCause's version, and treatment and outcome are generated in Karlsson and Krijthe's. | Scale change not meaningful on a binary outcome. | CEVAE repo has a `datasets` folder but its page does not confirm Twins data; RealCause provides samples | [S] [summary](https://arxiv.org/pdf/2007.10014); [P] [CEVAE repo](https://github.com/AMLab-Amsterdam/CEVAE); Karlsson and Krijthe use it for semi-synthetic tests [P] |
| **Hillstrom** (MineThatData) | 64,000 customers, three randomized arms; visit rate about 0.15, conversion about 0.009, spend 0-499. | Low base rates; marketing uplift only. CausalPFN used it for Qini, De Bartolomeis et al. as a semi-synthetic base. | Use real covariates with injected outcome effect. Its real effects are unlikely to test the large-effect regime (inference from the base rates). | [scikit-uplift loader](https://www.uplift-modeling.com/en/latest/api/datasets/fetch_hillstrom.html) | [P] |
| **OSRCT / RCT rejection sampling** | Subsample RCT so that it is confounded; RCT estimate is ground truth. Keith et al. show low bias where a prior approach does not always achieve it; ~70k real RCT with text covariates. | Sample shrinks: OSRCT reduces sample by about half when assignment rate is 0.5 (Gentzel); ground truth is itself an estimate with its own SE. | Inherits RCT effect, unless an effect is injected. | [Keith et al. repo](https://github.com/kakeith/rct_rejection_sampling); TMLR 2023 | [P*] [arXiv 2307.15176](https://arxiv.org/abs/2307.15176v3); Gentzel [P] |
| **Yu and Sun RCT set** | Criteo (13.98M), Ferman (103k), Hillstrom, Sandercock/IST (19.4k), eight GSS items (about 52k each). Real outcomes. | Paper's finding is itself that most CATE models fail here. | Inherits RCT effects. | Listed in paper Table 4 | [P] [arXiv 2410.07021](https://arxiv.org/abs/2410.07021) |
| **WHI** (RCT + obs pair) | CT + OS arms, used by Hussain et al. 2022, 2023 and De Bartolomeis et al. 2024 for falsification tests; De Bartolomeis et al. use a binary CHD outcome. | Binary in the De Bartolomeis use; true confounding unknown; requires request. | No effect control. | [BioLINCC](https://biolincc.nhlbi.nih.gov/studies/whi_ctos/): "Open BioLINCC Study", free registration and request, commercial-use restrictions | [P] |
| **Project STAR** | RCT on class size. Kallus, Puli and Shalit (NeurIPS 2018) built an RCT-plus-confounded-observational benchmark. | Effect relative to spread not extracted here. Dataset versions differ between sources. | Injection only. | [Harvard Dataverse doi:10.7910/DVN/SIWH9F](https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_datacite_primary_10_7910_dvn_siwh9f) | [P] [arXiv 1810.11646](https://arxiv.org/pdf/1810.11646v1.pdf); data record [S] |
| **CausalPFN's own suite** | IHDP (100), ACIC 2016 (10), LaLonde CPS and PSID (100 each, RealCause), total 310 tasks; marketing RCTs Hillstrom, Criteo, X5, Lenta, Megafon with Qini. | Author-selected. Only 10 of ACIC. Performance drops on largest tables. | As per underlying sets. | [CausalPFN repo](https://github.com/vdblm/CausalPFN) `benchmarks/` | [P] [arXiv 2506.07918](https://arxiv.org/html/2506.07918v2) |
| **OpenML-CTR23** | Curated regression suite (Fischer, Feurer, Bischl, AutoML workshop 2023). CausalPFN added CTR23 tables to its training library of 337 OpenML tables. | Part of training data, so holdout care needed: tables sharing covariates or outcomes with test sets were checked for leakage. | Use unseen tables as a covariate base and inject known effects. | [Catalogue CSV](https://github.com/vdblm/CausalPFN/blob/main/assets/openml_catalogue.csv) | [P] [arXiv 2506.07918](https://arxiv.org/html/2506.07918v2) |

Other findings:
- Source conflict: Hahn et al. describe the 4,302-row ACIC 2017 covariates as "individuals in the original IHDP data set" and as 500 smaller than the 2016 matrix, while Dorie et al. name the Collaborative Perinatal Project as the ACIC 2016 source. Check before describing the covariates in a paper. [P] [Hahn et al.](https://arxiv.org/abs/1905.09515); [P] [Dorie et al.](https://arxiv.org/abs/1707.02641)

### Inferences
- Suggested minimum evidence stack, using sources above: (1) ACIC 2017 as an externally designed factorial with an explicit effect and noise factor; (2) IHDP-100 stratified by sigma_tau; (3) ACIC 2016 with re-simulation; (4) RealCause LaLonde, with the scale knob used only as an equivariance check; (5) RCT-subsampled data (OSRCT or RCT rejection sampling) for realism and null calibration; (6) real covariate plasmodes with injected effects for the large-effect range.
- Holdout matters: IHDP, ACIC 2016 and LaLonde were used to report CausalPFN performance, and base tables are from OpenML. Report which benchmarks are development vs. confirmatory for the detector.
- ACIC 2022 and WHI are weak fits for a first paper: ACIC 2022's panel structure and WHI's request process and binary outcome add cost without testing large effects.

### Gaps
- ACIC 2018 effect-size parameters, and any "ACIC 2023 or later" challenge with public data: Insufficient publicly verifiable evidence.
- Data availability for ACIC 2022 after the official site failed: Insufficient publicly verifiable evidence.
- Direct quotes from Hill 2011 and Louizos 2017 were not read. Facts on them come via Curth et al. and secondary papers.
- LaLonde effect relative to outcome SD was not extracted; compute it directly from the NSW files.

---

## Real datasets with large effects; plasmode and injected-effect practice

### Takeaway
I found no accepted public positive-control tabular dataset with effects many outcome-SDs in size. The accepted practice is plasmode or synthetic positive controls: keep real covariates and baseline structure and inject a known effect. Empirical medicine also suggests that very large effects are rare, usually come from small trials and tend to shrink on later evidence, so a sweep up to 128 needs an explicit rationale.

### Cited Findings
- Schreck, Slynko, Saadati and Benner, "Statistical plasmode simulations: Potentials, challenges and recommendations", Statistics in Medicine 43(9):1804-1825, 2024, DOI 10.1002/sim.10012: resample real covariates and create artificial outcomes with a parametric outcome-generating model; gives a step-wise procedure and reporting guidance; notes there were no explicit guidelines before. Complementary to, not superior to, parametric simulation. [P*] [arXiv 2305.06028](https://arxiv.org/abs/2305.06028); [DKFZ record](https://inrepo02.dkfz.de/record/288132/export/print?ln=en)
- OHDSI Methods Benchmark (Schuemie et al., Harvard Data Science Review 2.1, 2020): uses negative controls plus "synthetic positive controls (drug-outcome pairs that augment negative controls with simulated causal effects)". Across four databases, only about half of 95% CIs contained the truth in most contexts. Later erratum concerns one IPTW implementation. **Foundational.** [P] [HDSR PDF](https://hdsr.mitpress.mit.edu/pub/fxz7kr65/download/pdf); erratum [P*] [MethodEvalViewer](https://data.ohdsi.org/MethodEvalViewer/)
- Its positive controls are made by an injection process on negative controls, with target effect sizes theta = 1.5, 2 and 4, and new outcomes sampled from a large-scale predictive model; 200 of the gold-standard set are negative controls. Coverage is one of its reported metrics. Note how small these targets are compared with this project's range. [P] [HDSR PDF](https://hdsr.mitpress.mit.edu/pub/fxz7kr65/download/pdf)
- Pereira, Horwitz and Ioannidis, JAMA 2012, 308(16):1676-1684 (**foundational**): 85,002 forest plots from 3,082 Cochrane reviews. Very large effects (OR >=5, P<.05) appeared in 9.7% of first trials, 6.1% only in later trials. 90% of first-trial and 98% of later-trial very large effects got smaller in meta-analysis (median OR 11.88 to 4.20; 10.02 to 2.60). Only 9.2% of 500 sampled topics sustained them at P<.001, none on mortality. Laboratory-defined efficacy outcomes were over-represented. [P] [PubMed](https://pubmed.ncbi.nlm.nih.gov/23093165/)
- Glasziou et al., BMJ 2007;334:349-351 (**foundational**): signal-to-noise framing of treatment effect vs prognosis; in the examples studied in detail, rate ratios often exceeded 10. [P*] [BMJ](https://www.bmj.com/content/334/7589/349)
- Causal Chambers (Gamella, Peters and Bühlmann): two physical systems (light tunnel, wind tunnel) with computer-controlled actuators and a validated causal model, CC BY 4.0 data. Authors frame them as a sanity check, not a replacement for real-world complexity. Case studies listed are discovery, OOD generalization, change points, ICA, symbolic regression, not effect estimation. arXiv [P*] [2404.11341](https://arxiv.org/abs/2404.11341v1); Nature Machine Intelligence 2025 citation via a repository listing [S] [GitHub mirror](https://github.com/standardgalactic/causal-chamber)

### Inferences
- An actuator-to-sensor experiment in the Causal Chambers is a plausible candidate for a real positive control with high signal relative to noise, but this use would be novel and needs randomization added or checked.
- Recommended injection design: Y' = Y + T * k * g(X), with real Y, X and T from an RCT or OSRCT sample, with k swept. Report k in units of outcome SD (Dorie et al. convention). The RCT arm provides a credible null (k = 0 plus real noise) and the injection provides known truth. This requires no generative model, unlike RealCause.
- Pereira et al. give reviewers an easy objection to a sweep up to 128 if the DGP's outcome SD is near 1. Answer it by describing large-effect regimes as a stress test, stating effects in outcome-SD units, and flagging realistic zones such as lab or biomarker outcomes.

### Gaps
- Insufficient publicly verifiable evidence of an accepted, public, tabular, randomized positive-control dataset with an effect several outcome-SDs in size.
- Candidates not verified here for effect size relative to spread: GSS question-wording experiments used by Yu and Sun; CRISPR or perturbation datasets (e.g. target gene knockdown); statin/LDL trials on BioLINCC. Each needs checking before being recommended.

---

## Scale-invariance as an evaluation issue

### Takeaway
Yes, the leading models normalise outcomes. CausalPFN's released inference code z-scores outcomes separately per treatment arm, then adds each arm's mean and SD back. That has two consequences. Rescaling Y, or adding a constant effect, cannot produce shrinkage by construction. And any under-fitted adjustment should pull the ATE toward the unadjusted difference in means, not toward zero. An effect-size sweep is common as a benchmark factor but not a standard reported test for these models.

### Cited Findings

**Code and paper facts, CausalPFN** ([repo](https://github.com/vdblm/CausalPFN) at commit b7ed2f1, v0.1.5, 2026-09-27; read directly, not executed) [P]
- `_get_y0_y1_shift_scale` computes context mean and SD per arm. Context outcomes are transformed as (y - y1_shift)/y1_scale for treated and (y - y0_shift)/y0_scale for control, with the comment "z-standardize the outcomes". File: `src/causalpfn/models/icl_model.py`, lines 128-155 and 171-176, and the same logic in inference at lines 256-259.
- Prediction is mapped back as `mean * y1_scale + y1_shift` for t=1 and `mean * y0_scale + y0_shift` for t=0 (line 298). So CATE(x) = [m1(x)*s1 + ybar1] - [m0(x)*s0 + ybar0].
- ATE paths in `causal_estimator.py`: the CATE estimator's `estimate_ate` is the mean of the CATE. `ATEEstimator` has algorithm "S" (default, mean of mu_1 - mu_0) and "RA" (uses factual Y in the observed arm, and the model only for counterfactuals). A shrinkage evaluation must state which path is tested.
- Bins: `vmin=-10.0, vmax=10.0`; model default HL-Gaussian `sigma` fallback 0.5 (`model_config.get("sigma", 0.5)`), checkpoint value not checked. The paper says: "discrete CEPO posterior over the interval [-10, 10]. We then scale the interval to match the scale of the outcomes and clip the out-of-range values." [P] [arXiv 2506.07918 App. D.2](https://arxiv.org/html/2506.07918v2)
- Covariates are normalized with `normalize_data` and clipped at 10 sigma (`models/model.py`). The loader supports a `tabdpt` model type; the released checkpoint's type was not inspected.
- For large data, context is chosen per query via a gradient boosting "weak learner" CATE stratification, with `num_neighbours=1024` per arm and `max_context_length=4096` by default, so standardization is then stratum-specific. The docstring says these parameters only matter when data do not fit in context. An arm larger than 1,024 units therefore changes behaviour, which can occur at n = 2000 with imbalanced arms (my reading of the code).
- Training noise: "we sample eps_t from a Gaussian with a variance uniformly drawn from (0, Var(mu_t)]". So training noise is never larger than signal, in the arm-level sense. [P] [arXiv 2506.07918 App. D.1](https://arxiv.org/html/2506.07918v2)
- The paper reports "The model generally appears conservative", possibly due to "Gaussian smoothing used in the histogram loss". This concerns calibration on synthetic DGPs, not large effects. [P] [same](https://arxiv.org/html/2506.07918v2)
- The arXiv v2 paper does not appear to describe outcome z-scoring: a text search of its HTML found no "standardiz" or "z-scor", and "normaliz" only for Qini and in the bibliography. It reports PEHE for Lalonde "in thousands". So the code is the authority here, and v2 may differ from the NeurIPS version, which I did not compare. [P]

**Other models**
- TabPFN regressor: bar-distribution borders are scaled by training target mean and SD, with stored `y_train_mean_`/`y_train_std`; default mean/variance normalization, optional power and quantile transforms. [P*] [TabPFN API](https://priorlabs.ai/reference/tabpfn/regressor)
- FT-Transformer (Gorishniy et al. 2021): "We apply standardization to regression targets for all algorithms." **Foundational.** [P] [arXiv 2106.11959](https://arxiv.org/abs/2106.11959)
- BART (Chipman, George, McCulloch): shift and rescale Y to [-0.5, 0.5] before applying priors. **Foundational.** [P] [arXiv 0806.3286](https://arxiv.org/abs/0806.3286)
- Do-PFN: outcome normalization not established from the abstract and summaries read. Benchmarks include RealCause. [P*] [NeurIPS 2025](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ff997469ac66cf893c4183efeb22212a-Abstract-Conference.html)

**Effect-size sensitivity as a practice**
- ACIC 2017 varies effect magnitude and noise as factors, and Dorie et al. report effects in outcome SD units. [P] [Hahn et al.](https://arxiv.org/abs/1905.09515); [Dorie et al.](https://arxiv.org/abs/1707.02641)
- RealCause provides a scale knob, explicitly so one can test settings "where the causal effect is large/small". [P] [arXiv 2011.15007](https://arxiv.org/abs/2011.15007)
- CausalPFN ablations cover sample and covariate size, and a heterogeneity parameter gamma in the training prior. I found no effect-magnitude sweep. [P] [arXiv 2506.07918](https://arxiv.org/html/2506.07918v2)
- The relative ATE error |ate_hat - ate|/|ate| used in CausalPFN is scale-free, but it is undefined or unstable near a zero ATE. [P for the formula; instability is my inference] [same](https://arxiv.org/html/2506.07918v2)

### Inferences
All of these derive from reading the code, are not empirically tested by me, and should be checked against the released checkpoint first. They assume default `calibrate=False` and that all units fit in context (each arm at most 1,024); beyond that, the weak-learner context selection can break the exact identities.
1. **Global rescale is a no-op.** Y to aY+b (a>0) leaves standardized inputs unchanged, so predictions transform exactly, up to floating point (and, at large n, trees in the context selector). RealCause's scale knob is such a transform: Y(t)' = s*Y(t)/tau. So it should not expose shrinkage, and any change in the detector's result under it reveals a bug or an estimator asymmetry. This makes a cheap **metamorphic unit test**.
2. **Constant additive effect is also a no-op.** Y(1) + k changes only y1_shift. Standardized inputs are identical for every k, so CATE(k) - CATE(0) = k exactly. Constant-effect shrinkage should be impossible by construction in this inference path. If the project observes it, the cause lies elsewhere (e.g. wrapper, clipping in another path, or Monte Carlo noise).
3. **Heterogeneous effects are where shrinkage can arise.** With tau = k*g(x), s1 grows with k and the z-target tends to standardized g(x). Any z-space regression-to-the-mean then multiplies by s1, so raw shrinkage of heterogeneity grows with k, but the *fraction* may plateau. A key test is whether the shrinkage ratio is flat or rising in k, measured separately for ATE and for SD(CATE).
4. **ATE fallback is not zero.** If m1, m0 tend to 0, the ATE estimate tends to ybar1 - ybar0, the naive difference in means, not 0, on both the S and RA paths. Under-adjustment therefore shows up as confounding bias, whose sign depends on the DGP. A **one-sided** test for "CFM smaller than AIPW" would have low power when naive bias pushes away from zero, and could be read as the wrong failure mode when bias pushes toward zero. The detector paper should report by bias sign, or justify one-sidedness, and consider a two-sided comparison plus a separate heterogeneity contrast.
5. **Report in standardized axes.** Use effect/SD(Y|T=0), SD(tau)/SD(Y), and SNR = SD(mu_t)/sigma, as raw "128" is meaningless for a z-scoring model. Also vary them independently: Y' = Y + T*k*g(X) changes tau alone, unlike RealCause's knob.
6. **Low-SNR is possibly more out-of-prior than high-SNR**, given noise variance at most Var(mu_t) in training. The detector's evaluation should include cells where noise exceeds arm-level signal.

### Gaps
- Empirical behaviour of the released checkpoint under these transforms was not run. The user's planned real-model test should settle this.
- Hugging Face checkpoint config (actual sigma, vmin, vmax) was not inspected. The paper states [-10, 10].
- No source was found that calls effect-size sensitivity a "standard" required test for tabular or causal transformers. Insufficient publicly verifiable evidence that it is standard.

---

## Positive and negative controls in method evaluation

### Takeaway
Negative controls and synthetic positive controls are well established in epidemiology and increasingly required in applied causal work. For a diagnostic, the direct analogues are planted-failure estimators (positive) and known-good estimators (negative), and neither tends to be labelled that way in causal ML.

### Cited Findings
- Lipsitch, Tchetgen Tchetgen and Cohen, Epidemiology 21(3):383-388, 2010 (**foundational**): exposure and outcome controls to detect confounding and other bias, adopted from laboratory practice. [P*] [PMC3053408](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/)
- Shi, Miao and Tchetgen Tchetgen review: extends to selection, measurement and homophily bias. A Leiden thesis chapter argues negative controls may lack specificity and sensitivity for unmeasured confounding. [S] [arXiv 2009.05641](https://arxiv.org/pdf/2009.05641.pdf); [Leiden](https://scholarlypublications.universiteitleiden.nl/access/item%3A3250847/view)
- Eggers, Tuñón and Dafoe, "Placebo Tests for Causal Inference", AJPS 68(3), 2024, DOI 10.1111/ajps.12818: typology by altered element (outcome, treatment, population) and tested assumption (identification, estimation); warns about uninformative tests and "null hacking" in placebo design. [P*] [Princeton record](https://collaborate.princeton.edu/en/publications/placebo-tests-for-causal-inference/)
- Imbens and Xu (JEP 2025): validation exercises "particularly placebo tests" are essential; LaLonde used 1975 earnings as a placebo outcome. [P] [arXiv 2406.00827](https://arxiv.org/abs/2406.00827)
- OHDSI benchmark: controls-based evaluation at scale, with empirical calibration from control estimates restoring coverage. **Foundational.** [P] [HDSR](https://hdsr.mitpress.mit.edu/pub/fxz7kr65/download/pdf)
- DoWhy refuters: placebo treatment and dummy outcome replace T or Y with a random variable, effect should go to zero. Docs read are v0.8, may be older than current. [P] [DoWhy docs](https://petergtz.github.io/dowhy/v0.8/user_guide/effect_inference/refute.html); [DoWhy paper](https://arxiv.org/pdf/2011.04216)
- Morris et al. recommend "methods with known properties" be included as checks. [P] [arXiv 1712.03198](https://arxiv.org/abs/1712.03198v3)

### Inferences
Suggested control battery:
- **Negative controls (detector should not fire):** AIPW from an independent split vs reference; an oracle-based estimator; a well-specified outcome regression; CFM at k=0 (null); placebo T or random-Y (AIPW and CFM both near zero).
- **Positive controls (detector must fire):** planted shrinkage such as lambda*tau_hat for a sweep of lambda; ridge-penalized S-learner, known to be regularised toward no effect; constant predictor; naive difference in means under confounding, as a realistic CFM-fallback analogue.
- **Reference failure controls:** deliberately mis-specified nuisance in AIPW; poor overlap; abstention rate must rise and not mask errors. Report conditional and unconditional operating characteristics, since abstaining changes the population tested.
- Avoid the null-hacking trap by pre-specifying which controls are used and reporting all of them.

### Gaps
- I did not find a causal-ML paper that presents a formal "planted shrinkage" control battery for a diagnostic. See the sibling novelty notes for whether this is a differentiator.

---

## What recent accepted diagnostics papers report

### Takeaway
Accepted diagnostics papers report rejection rate at a nominal alpha, power curves against effect, bias or sample size, semi-synthetic plus one real RCT-linked dataset, and sometimes coverage. Replications range from 5 to 250. Runtime is rarely reported, so a "cheap" claim needs its own measurement.

### Cited Findings

| Paper | Venue | What is tested | Metrics reported | Data | Reps | Cost |
|---|---|---|---|---|---|---|
| Karlsson and Krijthe, "Falsification of Unconfoundedness by Testing Independence of Causal Mechanisms" [PMLR 267:29128-29147](https://proceedings.mlr.press/v267/karlsson25a.html) | ICML 2025 | Unmeasured confounding | Falsification rate as type I error (should stay below alpha=0.05) and power, vs K, N, d, polynomial degree | Simulated; Twins semi-synthetic | 250, plus 1,000 bootstrap | Not in portion read |
| Yu and Sun [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e1194b07221de8783a02087bb899d69f-Paper-Conference.pdf) | ICLR 2025 | CATE models vs trivial baselines | Q-hat statistic, share worse than zero or constant effect, win share, SE and 95% CI table | 12 RCTs, 43,200 variants | Via variants | Not assessed |
| De Bartolomeis et al. [PMLR 244:943-965](https://proceedings.mlr.press/v244/de-bartolomeis24a.html) | UAI 2024 | Subgroup bias vs RCT, with tolerance | Rejection probability vs tolerance, lower bound on bias vs subgroup and sample size; alpha=0.05. No numeric type I rate in text read | Hillstrom semi-synthetic; WHI | 5 in figure | Not in portion read |
| Mahajan et al. [ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/71484f17ae8ddd0500c8571bed59926d-Abstract-Conference.html) | ICLR 2024 spotlight | Surrogate metrics for CATE selection | Performance of selected estimator across metrics; 34 metrics, 78 datasets (camera-ready); generative realistic datasets | Composition not read | Not extracted | Not assessed |
| Karlsson and Krijthe [NeurIPS 2023](https://papers.nips.cc/paper_files/paper/2023/hash/89e541b817ea043a971840a926e12b37-Abstract-Conference.html) | NeurIPS 2023 | Hidden confounding across environments | Detection, particularly when bias large | Simulated, semi-synthetic | Not read | Not read |
| Hussain et al. [PMLR 206](https://proceedings.mlr.press/v206/hussain23a.html) | AISTATS 2023 (**foundational**) | Internal and external validity vs RCT | Type I error vs alpha 0.05, power curves; WHI rejection rates by selection-bias strength (0.29 / 0.67 / 0.94 / 1.0 for MMR-Contrast at p=0, .05, .10, .15) | IHDP semi-synthetic; WHI | 100 simulations; bootstrap for WHI | Not in portion read |
| Hussain et al. [NeurIPS 2022](https://papers.neurips.cc/paper_files/paper/2022/file/28b5dfc51e5ae12d84fb7c6172a00df4-Paper-Conference.pdf) | NeurIPS 2022 (**foundational**) | Screening obs. studies with RCT, then extrapolate | Conservative intervals and coverage | IHDP semi-synthetic, WHI | Not read | Not read |

Status: Karlsson and Krijthe 2025, De Bartolomeis, Hussain 2023: evaluation details [P] from HTML, first 100k characters only. Yu and Sun: [P] abstract and tables. Mahajan, Karlsson 2023, Hussain 2022: [P*] from venue and abstract records.

Other relevant items:
- Hahn et al.'s challenge reports RMSE, coverage and interval length across subsets, with no method reaching nominal coverage. [P] [arXiv 1905.09515](https://arxiv.org/abs/1905.09515)
- CausalPFN's rank-vs-wall-clock figure is direct precedent for a time-vs-accuracy claim. [P] [repo README](https://github.com/vdblm/CausalPFN)

### Inferences
Reporting list for this detector:
- Type I error with MCSE, per cell; power vs standardized effect and vs true shrinkage fraction; AIPW reference CI coverage (since the z-test depends on it); abstention rate and conditional error given no abstention; false alarm vs miss by overlap level.
- Minimum detectable shrinkage at n = 500 and 2000.
- Baselines: at minimum compare with a simple RCT-free alternative such as a calibration slope or Qini-based check, and a naive bootstrap. See sibling notes on baseline methods.
- Wall-clock cost of diagnostic vs model fit, with hardware stated. Runtime reporting would be a small differentiator as it is uncommon.
- The Hussain et al. WHI p=0 rejection rate of 0.29 is above nominal, and the portion I read does not treat it as type I error (real data has no guaranteed null). This shows the difficulty of claiming calibration on real data. Expect reviewers to ask how the detector behaves when the reference is itself imperfect.

### Gaps
- I did not find a recent accepted paper on detecting shrinkage or large-effect failure in amortized causal models specifically (see sibling novelty notes).
- UAI 2025, AISTATS 2025, and CLeaR 2025-2026 proceedings were not systematically scanned. A targeted search found no type I error/coverage paper on CATE validation from 2025 beyond those listed; absence of evidence, not evidence of absence.

---

## Publication landscape: venues, CFPs, acceptance rates, negative results

### Takeaway
As of 2026-10-31 the nearest suitable deadlines are CLeaR 2027 (16 November 2026) and PAKDD 2027 (20 November 2026); UAI 2027's call is not posted. TMLR (rolling) is the best stated fit for a careful diagnostic or evaluation paper, because its criteria explicitly do not require novelty; Journal of Causal Inference (continuous publication) fits on scope. A pure negative result has an accepted home mainly at TMLR, if systematic, or at an ICBINB-type workshop when themes align; the 2026 ICBINB themes were not causal.

### Cited Findings

| Venue | Status on 2026-10-31 | Fit notes | Acceptance rate, source | Status |
|---|---|---|---|---|
| **CLeaR 2027** | Submission 16 Nov 2026 AoE; reviews 19 Jan 2027; decisions 22 Feb 2027; camera-ready 5 Apr 2027; **conference 3-5 May 2027**, Sorbonne, Paris; OpenReview. RIKEN and BERI pages say March 3-5, and the official site says May. | "Theory and methodology papers will be evaluated based on their novelty, technical quality, and potential impact"; application papers not required to have new methods. "Experimental methods and results are expected to be reproducible". Program highlights "benchmark datasets, or benchmark methodologies". Separate **dataset track is non-archival**. | No published rate found. Insufficient publicly verifiable evidence. | [P] from site bundle of [cclear.cc/2027](https://www.cclear.cc/2027); conflict [P] [RIKEN](https://aip.riken.jp/news/clear2027/?lang=en), [S] [BERI](https://www.beri.net/events/clear-2027) |
| **UAI 2027** | No official CFP found; UAI 2026 was Amsterdam, deadline 25 Feb 2026. Trackers project Feb 2027, labelled as projected. | PMLR; "novel theory, methodology and applications". | CFP gives none. Third party: 2025 230/750 = 30.7%; 2024 200/744 = 26.9%. | [P] [UAI 2026 CFP](https://auai.org/uai2026/call_for_papers); [S] [myhuiban](https://www.myhuiban.com/conference/416?lang=en-us); [S] [OpenCurious](https://www.opencurious.com/ai-conference-deadlines/uai-2027) |
| **AISTATS 2027** | **Closed**: full papers 6 Oct 2026; notifications 20 Jan 2027; Montreal, 3-6 May 2027. | PMLR. Next option is AISTATS 2028 cycle (no CFP). | Official: "Acceptance rates tend to be around 25%". Third party: 2025 583/1,861 = 31.3%. These disagree. | [P] [AISTATS 2027 CFP](https://virtual.aistats.org/Conferences/2027/CallForPapers); [S] [myhuiban](https://www.myhuiban.com/conference/1853?lang=en-us) |
| **TMLR** | Rolling; double-blind on OpenReview. | "emphasizes technical correctness over subjective significance"; "novelty of the studied method is not a necessary criterion". Reproducibility reports welcome if they systematically study robustness or generalizability and give actionable lessons; class-style reruns unlikely. Precedent: Keith et al. RCT rejection sampling. | None published. Insufficient publicly verifiable evidence. | [P] [TMLR](https://jmlr.org/tmlr/); [criteria](https://jmlr.org/tmlr/acceptance-criteria.html) |
| **Journal of Causal Inference** (De Gruyter) | Continuous publication; fully OA; **APC €1,050**, no submission fee. | Theoretical and applied causal research. EiCs Bareinboim, Díaz, Tian. | No rate published on the journal page. JIF 2.2 (2025, JCR 2026); CiteScore 3.3 (Scopus 2026); SJR 1.104. | [P] [journal page](https://www.degruyterbrill.com/jci) |
| **Statistics in Medicine; Biometrical Journal** | Journals. | Published the methods-evaluation works cited here. Fit if biostat framing is used. | Rates and indexing not verified. | Precedent [P]; rest: Insufficient publicly verifiable evidence |
| **Observational Studies** | Journal. | ACIC 2022 special issue. | Not verified. | [P*] [Project MUSE](https://muse.jhu.edu/article/895649) |
| **ECML PKDD** (Springer) | 2026 in Naples, done. 2027 call not verified. Journal track with Springer *Machine Learning* and *DMKD*; 2026 cutoffs 30 Oct 2025 and 15 Jan 2026. | Conference plus journal route. | 2026 research track 280/1150 (24.3%), applied track 90/381 (23.6%), per Springer blurb on a bookseller page. | [P] [journal track](https://ecmlpkdd.org/2026/submissions-journal-track/); [S] [listing](https://www.schweitzer-online.de/buch/Ceci/Machine-Learning-Knowledge-Discovery-Databases-Research-Track/9783032376565/A77857472/) |
| **PAKDD 2027** (Springer LNAI) | Wellington, 29 Jun-2 Jul 2027; deadline 20 Nov 2026; double-blind. | Lower-profile option; four tracks. | PAKDD 2024: 177/720 per Springer. PAKDD 2026: one listing says 97 full papers from 728, unclear whether whole-conference. PAKDD site says "often" below 30%. | [P*] [EasyChair CFP](https://easychair.org/cfp/PAKDD2027); [P*] [Springer 2024](https://link.springer.com/book/10.1007/978-981-97-2253-2); [S] [listing](https://www.schweitzer-online.de/en/buch/Long/Trends-Applications-Knowledge-Discovery-Data-Mining/9789819220137/A77016401/) |
| **IEEE ICDM 2026** | Closed; 6 June 2026 deadline; Shenyang, 12-15 Nov 2026. Single-blind, 10 pages, Research or Applied track. | Data-mining audience, less causal-statistical. | Third party only: 2021 98/990 (9.9%); old. No official 2026 rate found. | [P*] [CFP](https://www3.cs.stonybrook.edu/~icdm2026/CallforAppliedTrack/list.htm); [S] [myhuiban](https://www.myhuiban.com/conference/142.md) |
| **IEEE DSAA and other IEEE conferences** | Not verified. | | Insufficient publicly verifiable evidence. | Search gave no result |
| **NeurIPS 2026 workshops** | Closed for most: suggested submission 29 Aug 2026; mandatory notification 29 Sept 2026; December 2026. | Name list includes ICBINB-BIO, IAEval, EconML, E-values. No name clearly indicates causality. CauScien ran at NeurIPS 2025; 2026 status unknown. | None found. | [P] [OpenReview listing](https://openreview.net/venue?id=NeurIPS.cc); [P*] [NeurIPS call](https://neurips.cc/Conferences/2026/CallForWorkshops); [P*] [CauScien](https://sites.google.com/view/causcien/call-for-papers) |
| **CausalBench workshop** (WSDM) | CausalBench'26 held 26 Feb 2026, companion proceedings. 2027 not found. | Directly on benchmarking causal models; 4-6 pp, single-blind. | Not published. | [P] [CFP](https://groups.google.com/g/isaim/c/Y87gRmstexg) |

**Negative results**
- ICBINB still runs but its theme changes. ICLR 2025: "Challenges in Applied Deep Learning", sought negative results and failed applications, proceedings in PMLR v296. ICLR 2026: "dedicated to discussing negative results and rigorous evidence of limitations of LLMs", 4 pages, deadline 31 Jan 2026, archival status "being clarified", with a non-archival option. [P] [ICBINB 2026](https://sites.google.com/view/icbinb-2026/submit); [P*] [ICBINB 2025 CFP](https://lists.cnsorg.org/hyperkitty/list/comp-neuro@lists.cnsorg.org/thread/VVETGKHYB5WTIZUST3INQZEG7ZLIVZ2A/)
- NeurIPS 2026 lists a workshop "ICBINB-BIO"; I saw the name only, so scope is unverified. No ICLR 2027 ICBINB announcement found. [P] [OpenReview listing](https://openreview.net/venue?id=NeurIPS.cc)
- Insights from Negative Results in NLP exists but is NLP-focused. [P*] [ACL portal](https://www.aclweb.org/portal/node/5015)
- Curth et al. (NeurIPS D&B 2021), Yu and Sun (ICLR 2025) and Pawel et al. (Biometrical Journal) show critical evaluations can be published in strong venues when framed as a systematic evaluation with lessons. [P] (links above)

### Inferences
- Likely outcome-to-venue mapping:
  - **Detector works, evidence stack done:** UAI 2027 (if CFP matches), AISTATS 2028, or JCI. Consider TMLR for speed and no fixed deadline.
  - **Detector works, small scope:** workshop first, e.g. a causal or benchmarking workshop in 2027, non-archival where possible to preserve a journal version.
  - **CFMs do not shrink, or detector adds little** ("pure negative"): TMLR as a systematic robustness study of published methods; JCI as a methods note; ICBINB only if the 2027 theme fits. A bare "our detector did not work" is weak anywhere. "Scale equivariance of CausalPFN and what effect-size sweeps do and do not test" is an actionable lesson that meets TMLR's interest criterion.
- CLeaR 2027 in 16 days is not realistic without real-model results, based on the current state, unless a narrow, reproducible study is ready. Note also its stated criteria name novelty and potential impact.
- For Scopus or SCI requirements, JCI's JCR and Scopus metrics are verified on the publisher's page. Check other journals on Clarivate's Master Journal List and Scopus Sources directly.

### Gaps
- No primary acceptance rates found for CLeaR, TMLR, JCI, UAI, Statistics in Medicine or Biometrical Journal. Third-party rates are labelled; none should be treated as official.
- SCIE membership of JCI was not verified on Clarivate. The publisher page shows JCR metrics, and one third party lists SCIE. [S] [Journal Metrics](https://www.journalmetrics.org/journal/journal-of-causal-inference)
- ICBINB-BIO scope, any 2027 ICBINB, UAI 2027 CFP, ECML PKDD 2027 CFP, IEEE DSAA 2026/2027: Insufficient publicly verifiable evidence as of this date.
- Whether PMLR is confirmed for CLeaR 2027 proceedings was not isolated from the site text.

---

## Patentability of statistical diagnostics for ML estimators (brief, not legal advice)

### Takeaway
A statistical test applied to estimator outputs is likely to be treated as an abstract or mathematical method in the US, EPO and India unless claimed as a concrete technical improvement or tied to a specific technical purpose. Publication is the more natural route unless there is a specific technical embodiment; speak to a patent attorney before disclosing if patenting matters.

### Cited Findings
- US guidance: USPTO's 2024 AI guidance (89 FR 58128, 17 July 2024) says "it is common for claims to AI inventions to involve abstract ideas"; mathematical concepts cover "mathematical relationships, mathematical formulas or equations, and mathematical calculations"; a claim merely based on one does not recite it; eligibility can come from showing the invention "improves the functioning of a computer or improves another technology". [P] [Federal Register via GovInfo](https://www.govinfo.gov/content/pkg/FR-2024-07-17/html/2024-15377.htm)
- *SAP America v. InvestPic*, 898 F.3d 1161 (Fed. Cir. 2018) is the closest case: statistical analyses of investment data held ineligible, an advance in mathematical techniques remains abstract even if "[g]roundbreaking, innovative, or even brilliant". **Foundational.** [S, opinion text on a third-party host, read via fetch tool] [opinion copy](https://hallapproved.com/us/cases/cafc/2018/4523133); citation [S] [Knobbe summary](https://www.knobbe.com/blog/sap-america-inc-v-investpic-llc/)
- *Recentive Analytics v. Fox* (Fed. Cir. 18 Apr 2025): claims that only apply generic ML to a new data environment, without improving the ML model, are ineligible; not a categorical bar. [S] [Winston summary](https://www.winston.com/print/v2/content/1100404/recentive-analytics-v-foxin-precedential-case-of-first-impression-federal-circuit-holds-machine-learning-patents-that-do-not-improve-the-technology-ineligible-under-section-101.pdf)
- *Ex parte Desjardins* (PTAB Appeals Review Panel, 2025; designated precedential Nov 2025): recited technical improvements to how a model operates can give practical application; December 2025 memos reportedly brought this into the MPEP. Sources differ on memo dates; I did not read the USPTO originals. [S] [Pearl Cohen](https://www.pearlcohen.com/a-new-era-in-ai-patent-eligibility-in-view-of-ex-parte-desjardins/); [Bloomberg Law](https://news.bloomberglaw.com/ip-law/ai-patent-eligibility-has-shifted-with-one-machine-learning-case)
- EPO Guidelines G-II 3.3.1 (2025 edition): models "are per se of an abstract mathematical nature"; use "does not by itself render inventions... non-patentable"; technical example: neural net in a heart monitor; non-technical example: classifying text documents by content alone. 2026 edition not checked. [P] [EPO G-II 3.3.1](https://epo.org/en/legal/guidelines-epc/2025/g_ii_3_3_1.html)
- India: Patents Act s.3(k) excludes "a mathematical or business method or a computer program or algorithms"; 2025 CRI guidelines reportedly assess claims as a whole with attention to technical effect. Official text not read; dates conflict across sources. [S] [AIPPI](https://www.aippi.org/news/decoding-cri-guidelines-2025/); [Bar and Bench](https://www.barandbench.com/law-firms/view-point/revised-cri-guidelines-2025)

### Inferences
- A "one-sided z-test vs AIPW with abstention" claim reads as selecting data, analysing mathematically and reporting a result, like *SAP*. A stronger form would be a concrete automated system that uses the diagnostic to control a specific technical process, but that is narrow and unlikely to cover the general method.
- No statement here is legal advice. Effects of pre-filing publication on patent rights were not researched in this session.

### Gaps
- No primary USPTO text on Desjardins or the December 2025 memos was read. No specific eligibility decision on causal-estimator diagnostics was found: Insufficient publicly verifiable evidence.
