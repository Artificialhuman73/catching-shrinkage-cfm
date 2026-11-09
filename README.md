# Catching Shrinkage in Causal Foundation Models

Can a cheap statistical check tell when CausalPFN reports a treatment effect that is too small?

Team: Chiranth R (PES1UG24AM354), Vihaan Wadhwa (PES1UG24AM319), Krish Mathur (PES1UG24AM914), P Saanvi (PES1UG24AM905)

**Start here:** [reports/Catching_Shrinkage_Explained.pdf](reports/Catching_Shrinkage_Explained.pdf) explains the experiment, the results and a review in plain language. The slides are in [reports/Catching_Shrinkage_Project_Report.pptx](reports/Catching_Shrinkage_Project_Report.pptx).

## Main findings (round 4, 1,440 simulated datasets)

- CausalPFN does not shrink large effects on our simulators: no run was more than 10% off at true effects of 4 and above, and every run at effect 128 was within 1.1%.
- The reason is that it rescales each treatment group before the network sees the data, so the effect's size never passes through the learned part.
- Its errors are at small effects (42% of runs more than 10% off at effect 1), mostly too large: it corrects about 96% of the confounding.
- Scale and shift self-checks pass exactly and therefore prove nothing for this model.
- The AIPW reference was the main source of false alarms; a planted-effect self-test works without any reference.

## Files

| Path | What it is |
|---|---|
| `shrinkage_detector_round3_gpu.ipynb` | Round 3 notebook (original detector) |
| `shrinkage_detector_round4_gpu.ipynb` | Round 4 GPU notebook: metamorphic test and real-CausalPFN anchor test (run on a Colab T4) |
| `round4_core.py` | Simulators, cross-fitted AIPW, the three detectors, planted-effect test |
| `round4_build_cache.py` | Builds the CPU AIPW cache the notebook uses |
| `round4_controls_cpu.py` | Controls: known shrinkage, broken reference, planted self-test |
| `analyze_round4.py` | Writes `results/round4/summary.md` |
| `results/round4/` | All round 4 result CSVs and the executed Colab notebook |
| `reports/` | Explanatory PDF, slides, novelty report; `reports/build/` has the scripts that make them |
| `OVERNIGHT_PLAN.md` | Log of the round 4 run |
