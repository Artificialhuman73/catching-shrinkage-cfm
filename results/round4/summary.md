# Round 4 results

### Test M: constant transformations (40 datasets)

|       |   max deviation / true ATE |
|:------|---------------------------:|
| Y*10  |                1.39031e-06 |
| Y+100 |                2.65699e-07 |
| Y+1T  |                4.8163e-06  |
| Y+8T  |                3.98081e-06 |
| Y+64T |                5.02043e-06 |

### Test M: CausalPFN adjustment fraction on a planted effect (1 = full adjustment, 0 = none), by plant size k

| dgp               |   0.5 |   1.0 |   2.0 |   4.0 |
|:------------------|------:|------:|------:|------:|
| notebook          | 1.153 | 1.112 | 1.107 | 1.118 |
| tau_on_confounder | 1.171 | 1.115 | 1.12  | 1.121 |

### Test C: mean signed relative bias, % (1440 datasets, 30+ seeds per cell, both n pooled)

|                              |   CausalPFN |   naive |   AIPW |
|:-----------------------------|------------:|--------:|-------:|
| ('flipped', 1.0)             |        -6.3 |   -88.9 |   27   |
| ('flipped', 2.0)             |        -2.6 |   -44.4 |   14.6 |
| ('flipped', 4.0)             |        -1.2 |   -22.1 |    7.9 |
| ('flipped', 8.0)             |        -0.7 |   -11   |    4.4 |
| ('flipped', 32.0)            |        -0.2 |    -2.6 |    1.2 |
| ('flipped', 128.0)           |        -0.2 |    -0.5 |    0.2 |
| ('notebook', 1.0)            |         9.7 |    88.9 |  -28.1 |
| ('notebook', 2.0)            |         4.9 |    44.3 |  -15.6 |
| ('notebook', 4.0)            |         1.8 |    22.1 |   -8.3 |
| ('notebook', 8.0)            |         0.8 |    11   |   -4.6 |
| ('notebook', 32.0)           |         0.6 |     2.6 |   -1.4 |
| ('notebook', 128.0)          |         0.4 |     0.5 |   -0.3 |
| ('scaled', 1.0)              |         9.3 |    40.6 |  -13.8 |
| ('scaled', 2.0)              |         3.7 |    -3.9 |   -3.5 |
| ('scaled', 4.0)              |         1.4 |   -26.2 |   -1.6 |
| ('scaled', 8.0)              |         0.2 |   -37.3 |    0.7 |
| ('scaled', 32.0)             |         0.9 |   -45.6 |    3.4 |
| ('scaled', 128.0)            |         0.3 |   -47.7 |    3.9 |
| ('tau_on_confounder', 1.0)   |         8.7 |    77.1 |  -26.3 |
| ('tau_on_confounder', 2.0)   |         3.9 |    32.4 |  -11.5 |
| ('tau_on_confounder', 4.0)   |         1.8 |    10.1 |   -5.4 |
| ('tau_on_confounder', 8.0)   |         0.4 |    -1.1 |   -2.2 |
| ('tau_on_confounder', 32.0)  |         0.4 |    -9.5 |    0.3 |
| ('tau_on_confounder', 128.0) |         0.4 |   -11.6 |    1   |

### Test C: share of runs where CausalPFN is >10% off, by direction, %

|                              |   shrunk >10% |   inflated >10% |
|:-----------------------------|--------------:|----------------:|
| ('flipped', 1.0)             |          26.7 |             3.3 |
| ('flipped', 2.0)             |           3.3 |             0   |
| ('flipped', 4.0)             |           0   |             0   |
| ('flipped', 8.0)             |           0   |             0   |
| ('flipped', 32.0)            |           0   |             0   |
| ('flipped', 128.0)           |           0   |             0   |
| ('notebook', 1.0)            |           0   |            48.3 |
| ('notebook', 2.0)            |           0   |            11.7 |
| ('notebook', 4.0)            |           0   |             0   |
| ('notebook', 8.0)            |           0   |             0   |
| ('notebook', 32.0)           |           0   |             0   |
| ('notebook', 128.0)          |           0   |             0   |
| ('scaled', 1.0)              |           0   |            48.3 |
| ('scaled', 2.0)              |           0   |             6.7 |
| ('scaled', 4.0)              |           0   |             0   |
| ('scaled', 8.0)              |           0   |             0   |
| ('scaled', 32.0)             |           0   |             0   |
| ('scaled', 128.0)            |           0   |             0   |
| ('tau_on_confounder', 1.0)   |           0   |            41.7 |
| ('tau_on_confounder', 2.0)   |           0   |             6.7 |
| ('tau_on_confounder', 4.0)   |           0   |             0   |
| ('tau_on_confounder', 8.0)   |           0   |             0   |
| ('tau_on_confounder', 32.0)  |           0   |             0   |
| ('tau_on_confounder', 128.0) |           0   |             0   |

### Test C: median anchor fraction where the naive contrast is >10% wrong (1 = adjusts fully, 0 = returns naive)

| dgp               |   1.0 |   2.0 |   4.0 |     8.0 |    32.0 |   128.0 |
|:------------------|------:|------:|------:|--------:|--------:|--------:|
| flipped           | 0.922 | 0.939 | 0.938 |   0.93  | nan     | nan     |
| notebook          | 0.892 | 0.896 | 0.928 |   0.947 | nan     | nan     |
| scaled            | 0.765 | 1.044 | 1.057 |   1.005 |   1.021 |   1.006 |
| tau_on_confounder | 0.899 | 0.892 | 0.79  | nan     |   1.039 |   1.033 |

### Test C: median planted-effect adjustment fraction

| dgp               |   500 |   2000 |
|:------------------|------:|-------:|
| flipped           | 1.323 |  1.083 |
| notebook          | 1.199 |  0.986 |
| scaled            | 1.129 |  0.939 |
| tau_on_confounder | 1.195 |  0.976 |

### Test C: detectors on real CausalPFN

|                |   flag_rate |   hits |   n_shrunk |   false_alarms |   n_not_shrunk |   uncertain |   caught_inflated |
|:---------------|------------:|-------:|-----------:|---------------:|---------------:|------------:|------------------:|
| round 3 z-test |       0.038 |  0.2   |         15 |          0.036 |           1281 |         0.1 |             0.15  |
| margin test    |       0.008 |  0.133 |         15 |          0.007 |           1281 |         0.1 |           nan     |
| rectifier test |       0.002 |  0     |         17 |          0.002 |           1279 |         0.1 |             0.056 |

### Test D: share of runs flagged as shrunk, by stand-in CFM and planted shrinkage

|                          |   runs |   old |   margin |   rectifier |   split |
|:-------------------------|-------:|------:|---------:|------------:|--------:|
| ('aipw', 0.0, 500)       |   3000 | 0     |    0     |     nan     | nan     |
| ('aipw', 0.0, 2000)      |   1200 | 0     |    0     |     nan     | nan     |
| ('aipw', 0.05, 500)      |   3000 | 0.271 |    0     |     nan     | nan     |
| ('aipw', 0.05, 2000)     |   1200 | 0.652 |    0     |     nan     | nan     |
| ('aipw', 0.1, 500)       |   3000 | 0.556 |    0     |     nan     | nan     |
| ('aipw', 0.1, 2000)      |   1200 | 0.705 |    0     |     nan     | nan     |
| ('aipw', 0.15, 500)      |   3000 | 0.616 |    0.331 |     nan     | nan     |
| ('aipw', 0.15, 2000)     |   1200 | 0.907 |    0.656 |     nan     | nan     |
| ('aipw', 0.2, 500)       |   3000 | 0.646 |    0.572 |     nan     | nan     |
| ('aipw', 0.2, 2000)      |   1200 | 0.952 |    0.758 |     nan     | nan     |
| ('aipw', 0.3, 500)       |   3000 | 0.714 |    0.661 |     nan     | nan     |
| ('aipw', 0.3, 2000)      |   1200 | 0.978 |    0.961 |     nan     | nan     |
| ('aipw', 0.5, 500)       |   3000 | 0.817 |    0.794 |     nan     | nan     |
| ('aipw', 0.5, 2000)      |   1200 | 0.988 |    0.985 |     nan     | nan     |
| ('naive', 0.0, 500)      |   3000 | 0.182 |    0.04  |       0.059 | nan     |
| ('naive', 0.0, 2000)     |   1200 | 0.202 |    0.086 |       0.046 | nan     |
| ('perfect', 0.0, 500)    |   3000 | 0.013 |    0.007 |       0.002 |   0.027 |
| ('perfect', 0.0, 2000)   |   1200 | 0.021 |    0     |       0     |   0     |
| ('perfect', 0.05, 500)   |   3000 | 0.32  |    0.009 |       0.007 |   0.025 |
| ('perfect', 0.05, 2000)  |   1200 | 0.699 |    0.004 |       0     |   0.003 |
| ('perfect', 0.1, 500)    |   3000 | 0.533 |    0.013 |       0.145 |   0.042 |
| ('perfect', 0.1, 2000)   |   1200 | 0.768 |    0.021 |       0.047 |   0.059 |
| ('perfect', 0.15, 500)   |   3000 | 0.609 |    0.364 |       0.684 |   0.102 |
| ('perfect', 0.15, 2000)  |   1200 | 0.842 |    0.712 |       0.762 |   0.528 |
| ('perfect', 0.2, 500)    |   3000 | 0.655 |    0.556 |       0.74  |   0.223 |
| ('perfect', 0.2, 2000)   |   1200 | 0.902 |    0.781 |       0.877 |   0.708 |
| ('perfect', 0.3, 500)    |   3000 | 0.709 |    0.666 |       0.839 |   0.375 |
| ('perfect', 0.3, 2000)   |   1200 | 0.959 |    0.922 |       0.994 |   0.81  |
| ('perfect', 0.5, 500)    |   3000 | 0.791 |    0.773 |       0.965 |   0.476 |
| ('perfect', 0.5, 2000)   |   1200 | 0.982 |    0.98  |       1     |   0.932 |
| ('ridge', 0.0, 500)      |   3000 | 0.643 |    0.608 |       0.617 | nan     |
| ('ridge', 0.0, 2000)     |   1200 | 0.667 |    0.667 |       0.667 | nan     |
| ('tlearner', 0.0, 500)   |   3000 | 0.006 |    0.009 |       0.009 | nan     |
| ('tlearner', 0.0, 2000)  |   1200 | 0     |    0     |       0     | nan     |
| ('tlearner', 0.05, 500)  |   3000 | 0.259 |    0.007 |       0.007 | nan     |
| ('tlearner', 0.05, 2000) |   1200 | 0.588 |    0     |       0     | nan     |
| ('tlearner', 0.1, 500)   |   3000 | 0.447 |    0.006 |       0.023 | nan     |
| ('tlearner', 0.1, 2000)  |   1200 | 0.658 |    0     |       0.001 | nan     |
| ('tlearner', 0.15, 500)  |   3000 | 0.558 |    0.295 |       0.387 | nan     |
| ('tlearner', 0.15, 2000) |   1200 | 0.687 |    0.614 |       0.637 | nan     |
| ('tlearner', 0.2, 500)   |   3000 | 0.606 |    0.482 |       0.55  | nan     |
| ('tlearner', 0.2, 2000)  |   1200 | 0.774 |    0.661 |       0.662 | nan     |
| ('tlearner', 0.3, 500)   |   3000 | 0.656 |    0.622 |       0.643 | nan     |
| ('tlearner', 0.3, 2000)  |   1200 | 0.93  |    0.83  |       0.844 | nan     |
| ('tlearner', 0.5, 500)   |   3000 | 0.751 |    0.723 |       0.761 | nan     |
| ('tlearner', 0.5, 2000)  |   1200 | 0.979 |    0.978 |       0.978 | nan     |

### Test F: perfect CFM, unreliable reference. Any flag here is a false alarm

|                                 |   aipw_bias |   old_false_flag |   margin_false_flag |   rect_false_flag |   uncertain |
|:--------------------------------|------------:|-----------------:|--------------------:|------------------:|------------:|
| ('both_ok', 'good', 500)        |      -0.143 |            0.015 |               0.008 |             0     |           0 |
| ('both_ok', 'good', 2000)       |      -0.014 |            0.03  |               0     |             0     |           0 |
| ('both_ok', 'poor', 500)        |      -0.03  |            0     |               0     |             0     |           1 |
| ('both_ok', 'poor', 2000)       |       0.078 |            0     |               0     |             0     |           1 |
| ('both_wrong', 'good', 500)     |       0.294 |            0.86  |               0.405 |             0.002 |           0 |
| ('both_wrong', 'good', 2000)    |       0.291 |            1     |               0.5   |             0     |           0 |
| ('outcome_wrong', 'good', 500)  |      -0.171 |            0.005 |               0.005 |             0     |           0 |
| ('outcome_wrong', 'good', 2000) |      -0.03  |            0.01  |               0     |             0     |           0 |
| ('prop_wrong', 'good', 500)     |       0.105 |            0.252 |               0.052 |             0.002 |           0 |
| ('prop_wrong', 'good', 2000)    |       0.054 |            0.342 |               0.015 |             0     |           0 |

### Test P: planted-effect adjustment fraction for estimators we understand

| dgp               |   AIPW |   T-learner |   naive (by definition) |
|:------------------|-------:|------------:|------------------------:|
| flipped           |  0.999 |       0.983 |                       0 |
| notebook          |  1.01  |       0.959 |                       0 |
| scaled            |  1.017 |       0.954 |                       0 |
| tau_on_confounder |  1.008 |       0.958 |                       0 |
