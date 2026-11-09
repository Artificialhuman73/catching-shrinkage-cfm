# Overnight plan: round 4 finish (started 2026-10-31 night)

Each wake-up: read this file, do the first unchecked step, tick it, append a line to the Log. Stop scheduling once all steps are ticked.
Rules: CPU work on the Mac (8 cores, `OMP_NUM_THREADS=1`, joblib loky). Colab allows ONE session; always `colab stop` after use (`export PATH="$HOME/.local/bin:$PATH"`). Never overwrite results/round4/*.csv without moving the old file to results/round4/old/ first. Report only numbers actually produced.

Key paths
- Core code: round4_core.py · CPU controls: round4_controls_cpu.py · analysis: analyze_round4.py
- Notebook builder: scratchpad build_nb.py (path in session) → shrinkage_detector_round4_gpu.ipynb
- Deck builder: /private/tmp/claude-501/-Users-chiranthr-Documents-Projects-ADA-PROJECT/934a623f-7052-4478-998d-be0faaede78c/scratchpad/deck/build.js (run with `NODE_PATH=$PWD/node_modules node build.js` from that folder) → reports/Catching_Shrinkage_Project_Report.pptx. Validate with the pptx skill's scripts/office/validate.py, render with /Applications/LibreOffice.app/Contents/MacOS/soffice + pdftoppm.

Known facts so far
- Test C (1,440 datasets, real CausalPFN): no run >10% off at effects >=4; at effect 128 all within 1.1%. Small effects (1-2): 3-10% error following the naive contrast. In the deck.
- Test M: Y*10, Y+100, Y+c*T followed exactly. In the deck.
- Planted effect fixed (built from X0): CausalPFN adjusts 93-97%, T-learner 87-97%, AIPW 0.89-1.28 (6 seeds). File results/round4/round4_P2_plant_fixed.csv. Not yet in deck.
- AIPW reference bias: with HGB propensity, -46.5% at effect 1 (n=500); with true propensity +1.4%. Cause: overconfident propensities (min 0.003 vs true 0.03). Also causes ~10% overlap-gate abstentions. Comparison of calibrated propensity models running (task bqkb544f3 output in session tasks folder).

## Steps
- [x] 1. Read the propensity comparison output (reg_hgb / calib_hgb / poly_logit). Pick the model with smallest |bias| and coverage nearest 95% at both n and effects. Prefer a generic model (reg_hgb or calib_hgb) over poly_logit unless the generic ones are clearly worse; record the choice and why.
- [x] 2. Wait for round4_controls_cpu.py (Test D) to finish (controls.log says "all controls done"). Do not kill it.
- [x] 3. Put the chosen propensity model into round4_core.py `_prop_model("flexible")`. Move old D/F/P CSVs and round4_aipw.csv + propensities.npz to results/round4/old/. Rebuild AIPW cache (round4_build_cache.py) and re-run round4_controls_cpu.py (Test P now uses planted_effect(X, Y, k)).
- [x] 4. Recompute Test C detector decisions with the new AIPW cache locally (CausalPFN outputs are in round4_C_anchor.csv: cfm_ate; rectifier needs cross-fitted mu0/mu1 which were NOT saved, so recompute only old + margin detectors, and say so). Do not re-run Colab unless necessary.
- [x] 5. Run analyze_round4.py (fix any column issues), write results/round4/summary.md.
- [x] 6. Update the deck: slide 9 with new detector numbers (state the AIPW fix), add one slide "The reference was the weak link" (AIPW bias before/after fix, true-propensity check), add planted-effect self-test result to slide 7 or a new slide, update slide 10. Keep body text >=14pt, validate, render, inspect.
- [x] 7. Update reports/CFM shrinkage detector novelty.md with a short "Round 4 results" section. Write a final summary for the user at the end of the Log.

## Log
- 23:4x Plan written. D controls at 320/700 seeds.
- 23:5x Step 1: chose degree-2 polynomial logistic propensity. n=500: bias -40.8%/-4.9% (effect 1/8) but coverage 100%/100% (wide, honest SEs); n=2000 effect 1: -0.6%, cover 95%. reg_hgb +19.4/+2.4/+6.2%, cover 85/95/80%; calib_hgb +26.3/+3.7/+10.1%, cover 35/85/45%. Caveat: polynomial logistic is correctly specified for this simulator. Root cause also in the DGP: "good" overlap has true e up to 0.996.
- 23:5x Step 2: old controls finished ("all controls done"); moved to results/round4/old/.
- 23:5x Step 3 started: new AIPW cache + controls running in background (cache.log, controls.log).
- 23:5x n=2000 effect 8: reg_hgb +0.8% cover 100%, calib_hgb +1.5% cover 100%, poly_logit -0.2% cover 100%. Choice stands.
- 00:01 Step 3 running: AIPW cache 1000/1440.
- 00:31 Step 3: new AIPW cache done (1440 datasets, 389s). Controls running (128/700 D seeds).
- 00:3x Step 4 done -> results/round4/round4_C_anchor_v2.csv (old z-test + margin only; rectifier not recomputed, CausalPFN cross-fit predictions were not saved). Fixed AIPW: pooled bias at effect 1 -10.3% -> -7.2% (pooling hides per-simulator signs); 95% CI coverage 96.5% -> 99.2% (now conservative); overlap-gate abstentions 10.0% -> 0.0%. Flags on real CausalPFN: old z-test 3.4% -> 1.2%, margin 0.8% -> 0.3%. Of 18 truly shrunk runs (all effect 1-2) each test now catches 1: the wider honest SEs cost power at small effects.
- 01:01 Step 3 done: controls finished with fixed AIPW (D: 500 seeds n=500, 200 n=2000).
- 01:0x Step 5 done: analyze_round4.py fixed (tuple JSON keys), summary.md written. Key control results (stand-in "perfect" CFM, flag %):
  old z-test: 0% shrink 1.5, 5% shrink 42.8, 10% (boundary) 60.0, 20% 72.5 -> flags trivial gaps at large effects (97.6% at 10% shrink, effect 128).
  margin test: boundary 1.5 (valid), 20% 62.0, 30% 73.9. At effect 1 power only 15-31%.
  rectifier: boundary 11.7 for perfect CFM (18.4% at effect 128, over nominal 5%), 1.7 for T-learner; power 77.9% at 20%.
  sample split: valid (4.7 at boundary) but weak (36% at 20%).
  Reference failure (perfect CFM): both_wrong -> old 93.0%, margin 45.2%, rectifier 0.1% false flags; prop_wrong -> old 29.8, margin 3.4, rectifier 0.1.
  Real shrinker (ridge, 68% truly shrunk): flagged 62-65% by all three. Naive CFM: margin 5.3, rectifier 5.5.
  Planted self-test validated: median adjustment AIPW 1.00-1.02, T-learner 0.95-0.98, CausalPFN 0.93-0.97 (P2, 10 seeds).
- 01:1x Step 6 done: deck now 12 slides (new: Result 3 planted self-test, Result 4 weak reference, Result 5 detectors on known shrinkage; conclusion rewritten; slide 8 AIPW line relabelled). Validated, rendered, inspected. Old builder kept as build_v1_backup.js.
- 01:1x Step 7 done: round 4 addendum appended to reports/CFM shrinkage detector novelty.md.

## Final summary
Deck: reports/Catching_Shrinkage_Project_Report.pptx (12 slides). Main findings: (1) CausalPFN did not shrink large effects on 4 simulators (1,440 datasets; 0 runs >10% off at effects >=4). (2) Constant self-checks are absorbed exactly, so they test nothing. (3) A planted-effect self-test that needs no reference works: CausalPFN adjusts ~96%, AIPW ~101%. (4) The AIPW reference was the main error source (-46.5% at effect 1 from overconfident propensities); fixed with a degree-2 logistic model (caveat: correctly specified here). (5) The margin test is the only one that holds its error rate at the 10% boundary; the rectifier is most powerful and robust to a bad reference but over-flags at the boundary. Open: power at small effects, Do-PFN/CausalFM positive controls, rectifier calibration. No Colab sessions left running.
