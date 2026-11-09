"""Runs the CPU-only part of Test C (AIPW) with every core available, for upload to Colab.
Colab's T4 machine has 2 CPU threads, so this is much faster on a laptop. Optional: the notebook fills in anything missing."""
import itertools, os, sys, time
os.makedirs("results/round4", exist_ok=True)
from round4_core import build_aipw_cache

C_DGPS    = ["notebook", "tau_on_confounder", "flipped", "scaled"]
C_EFFECTS = [1.0, 2.0, 4.0, 8.0, 32.0, 128.0]
C_NS      = [500, 2000]
C_SEEDS   = range(0, 30)

if __name__ == "__main__":
    grid = list(itertools.product(C_SEEDS, C_DGPS, C_EFFECTS, C_NS))
    t0 = time.time()
    build_aipw_cache(grid, "results/round4/round4_aipw.csv", "results/round4/round4_propensities.npz", n_jobs=8)
    print(f"{len(grid)} datasets in {time.time() - t0:.0f}s")
