# Theta, mixed-jet and BA revision comparison

These are **pre-release v0.2.0 measurements**, not a claim that v0.2.0 has been published.

- Generated: 2026-11-16T01:28:22+00:00
- Previous main: `6134a3d99152e6948f0aea58948e732a2e8d868b`
- Candidate: `4f6475f3824461e8c0e8226b6806e8bd17189ad2`
- Python: 3.14.7; mpmath: 1.4.1
- Platform: macOS-27.0.1-arm64-arm-64bit-Mach-O
- Revisions were archived from Git into separate temporary directories and imported in isolated processes. The checkout was not switched.
- No Sage, Wolfram, FLINT, PARI or external theta implementation was launched.

Seven timed samples per revision after warm-up. Values are median
**milliseconds per workload**, not uniformly per individual function call:
genus-one samples contain six points, other scalar-theta samples contain up
to four points, mixed jets contain one jet and BA contains four shifted jets.
Result caches are cleared before each sample. See [protocol and interpretation](README.md).

`genus-one` uses the saved jtheta-comparison inputs, without timing jtheta.
`theta` uses the saved Wolfram-comparison inputs, without running Wolfram.
`jets` reuses coupled, unreduced and issue #17 data; sigma uses a full mixed jet.
`ba` uses the same explicit compatible period data and a coordinate or dense
direction. No curve construction is included in these numerical times.

| Group | Case/workload | dps | Previous ms | Candidate ms | Candidate / previous |
|---|---|---:|---:|---:|---:|
| genus-one | comfortable/theta1/warm | 50 | 1.519 | 1.433 | 0.943 |
| genus-one | comfortable/theta1/cold | 50 | 8.596 | 8.662 | 1.008 |
| genus-one | comfortable/theta2/warm | 50 | 1.470 | 1.459 | 0.992 |
| genus-one | comfortable/theta2/cold | 50 | 10.442 | 10.249 | 0.982 |
| genus-one | comfortable/theta3/warm | 50 | 1.696 | 1.698 | 1.002 |
| genus-one | comfortable/theta3/cold | 50 | 10.621 | 10.435 | 0.982 |
| genus-one | comfortable/theta4/warm | 50 | 1.603 | 1.636 | 1.021 |
| genus-one | comfortable/theta4/cold | 50 | 10.408 | 10.490 | 1.008 |
| genus-one | comfortable/theta3 d1/warm | 50 | 1.975 | 2.283 | 1.156 |
| genus-one | comfortable/theta3 d1/cold | 50 | 22.066 | 22.211 | 1.007 |
| genus-one | comfortable/theta3 d2/warm | 50 | 1.994 | 2.009 | 1.008 |
| genus-one | comfortable/theta3 d2/cold | 50 | 25.232 | 25.569 | 1.013 |
| genus-one | generic/theta1/warm | 50 | 1.695 | 1.702 | 1.004 |
| genus-one | generic/theta1/cold | 50 | 10.399 | 10.392 | 0.999 |
| genus-one | generic/theta2/warm | 50 | 1.701 | 1.708 | 1.004 |
| genus-one | generic/theta2/cold | 50 | 10.271 | 10.340 | 1.007 |
| genus-one | generic/theta3/warm | 50 | 1.642 | 1.652 | 1.006 |
| genus-one | generic/theta3/cold | 50 | 10.248 | 10.260 | 1.001 |
| genus-one | generic/theta4/warm | 50 | 1.676 | 1.681 | 1.003 |
| genus-one | generic/theta4/cold | 50 | 10.282 | 10.313 | 1.003 |
| genus-one | generic/theta3 d1/warm | 50 | 2.126 | 2.106 | 0.991 |
| genus-one | generic/theta3 d1/cold | 50 | 22.169 | 22.254 | 1.004 |
| genus-one | generic/theta3 d2/warm | 50 | 2.175 | 2.197 | 1.010 |
| genus-one | generic/theta3 d2/cold | 50 | 25.331 | 25.492 | 1.006 |
| genus-one | near-boundary/theta1/warm | 50 | 1.892 | 1.882 | 0.995 |
| genus-one | near-boundary/theta1/cold | 50 | 10.482 | 10.501 | 1.002 |
| genus-one | near-boundary/theta2/warm | 50 | 1.897 | 1.909 | 1.006 |
| genus-one | near-boundary/theta2/cold | 50 | 10.476 | 10.531 | 1.005 |
| genus-one | near-boundary/theta3/warm | 50 | 1.873 | 1.921 | 1.026 |
| genus-one | near-boundary/theta3/cold | 50 | 10.444 | 10.678 | 1.022 |
| genus-one | near-boundary/theta4/warm | 50 | 1.928 | 1.901 | 0.986 |
| genus-one | near-boundary/theta4/cold | 50 | 10.523 | 10.605 | 1.008 |
| genus-one | near-boundary/theta3 d1/warm | 50 | 2.508 | 2.527 | 1.007 |
| genus-one | near-boundary/theta3 d1/cold | 50 | 23.147 | 23.482 | 1.014 |
| genus-one | near-boundary/theta3 d2/warm | 50 | 2.639 | 2.625 | 0.995 |
| genus-one | near-boundary/theta3 d2/cold | 50 | 26.049 | 26.489 | 1.017 |
| genus-one | strongly-unreduced/theta1/warm | 50 | 2.901 | 2.948 | 1.016 |
| genus-one | strongly-unreduced/theta1/cold | 50 | 20.261 | 20.506 | 1.012 |
| genus-one | strongly-unreduced/theta2/warm | 50 | 2.961 | 2.971 | 1.003 |
| genus-one | strongly-unreduced/theta2/cold | 50 | 20.689 | 20.643 | 0.998 |
| genus-one | strongly-unreduced/theta3/warm | 50 | 2.880 | 2.836 | 0.985 |
| genus-one | strongly-unreduced/theta3/cold | 50 | 20.292 | 20.434 | 1.007 |
| genus-one | strongly-unreduced/theta4/warm | 50 | 2.817 | 2.815 | 0.999 |
| genus-one | strongly-unreduced/theta4/cold | 50 | 20.191 | 20.222 | 1.002 |
| genus-one | strongly-unreduced/theta3 d1/warm | 50 | 4.060 | 4.048 | 0.997 |
| genus-one | strongly-unreduced/theta3 d1/cold | 50 | 36.674 | 36.806 | 1.004 |
| genus-one | strongly-unreduced/theta3 d2/warm | 50 | 4.330 | 4.403 | 1.017 |
| genus-one | strongly-unreduced/theta3 d2/cold | 50 | 44.386 | 44.995 | 1.014 |
| genus-one | comfortable/theta1/warm | 100 | 2.006 | 1.995 | 0.995 |
| genus-one | comfortable/theta1/cold | 100 | 12.350 | 12.374 | 1.002 |
| genus-one | comfortable/theta2/warm | 100 | 2.026 | 1.986 | 0.980 |
| genus-one | comfortable/theta2/cold | 100 | 12.374 | 12.609 | 1.019 |
| genus-one | comfortable/theta3/warm | 100 | 2.054 | 2.045 | 0.995 |
| genus-one | comfortable/theta3/cold | 100 | 12.269 | 12.419 | 1.012 |
| genus-one | comfortable/theta4/warm | 100 | 2.057 | 2.044 | 0.994 |
| genus-one | comfortable/theta4/cold | 100 | 12.289 | 12.411 | 1.010 |
| genus-one | comfortable/theta3 d1/warm | 100 | 2.474 | 2.470 | 0.998 |
| genus-one | comfortable/theta3 d1/cold | 100 | 26.060 | 26.443 | 1.015 |
| genus-one | comfortable/theta3 d2/warm | 100 | 2.693 | 2.663 | 0.989 |
| genus-one | comfortable/theta3 d2/cold | 100 | 30.445 | 30.054 | 0.987 |
| genus-one | generic/theta1/warm | 100 | 2.312 | 2.323 | 1.005 |
| genus-one | generic/theta1/cold | 100 | 12.552 | 12.625 | 1.006 |
| genus-one | generic/theta2/warm | 100 | 2.260 | 2.298 | 1.017 |
| genus-one | generic/theta2/cold | 100 | 12.555 | 12.662 | 1.008 |
| genus-one | generic/theta3/warm | 100 | 2.295 | 2.241 | 0.976 |
| genus-one | generic/theta3/cold | 100 | 12.491 | 12.499 | 1.001 |
| genus-one | generic/theta4/warm | 100 | 2.229 | 2.212 | 0.993 |
| genus-one | generic/theta4/cold | 100 | 12.412 | 12.591 | 1.014 |
| genus-one | generic/theta3 d1/warm | 100 | 2.751 | 2.746 | 0.998 |
| genus-one | generic/theta3 d1/cold | 100 | 26.165 | 26.824 | 1.025 |
| genus-one | generic/theta3 d2/warm | 100 | 2.939 | 2.918 | 0.993 |
| genus-one | generic/theta3 d2/cold | 100 | 30.316 | 30.280 | 0.999 |
| genus-one | near-boundary/theta1/warm | 100 | 2.567 | 2.601 | 1.013 |
| genus-one | near-boundary/theta1/cold | 100 | 13.280 | 13.486 | 1.016 |
| genus-one | near-boundary/theta2/warm | 100 | 2.694 | 2.637 | 0.979 |
| genus-one | near-boundary/theta2/cold | 100 | 13.350 | 13.347 | 1.000 |
| genus-one | near-boundary/theta3/warm | 100 | 2.591 | 2.559 | 0.988 |
| genus-one | near-boundary/theta3/cold | 100 | 13.253 | 13.403 | 1.011 |
| genus-one | near-boundary/theta4/warm | 100 | 2.656 | 2.573 | 0.969 |
| genus-one | near-boundary/theta4/cold | 100 | 13.264 | 13.391 | 1.010 |
| genus-one | near-boundary/theta3 d1/warm | 100 | 3.279 | 3.351 | 1.022 |
| genus-one | near-boundary/theta3 d1/cold | 100 | 27.391 | 27.609 | 1.008 |
| genus-one | near-boundary/theta3 d2/warm | 100 | 3.815 | 3.820 | 1.001 |
| genus-one | near-boundary/theta3 d2/cold | 100 | 31.670 | 31.849 | 1.006 |
| genus-one | strongly-unreduced/theta1/warm | 100 | 3.590 | 3.626 | 1.010 |
| genus-one | strongly-unreduced/theta1/cold | 100 | 25.009 | 25.587 | 1.023 |
| genus-one | strongly-unreduced/theta2/warm | 100 | 3.648 | 3.735 | 1.024 |
| genus-one | strongly-unreduced/theta2/cold | 100 | 25.359 | 25.284 | 0.997 |
| genus-one | strongly-unreduced/theta3/warm | 100 | 3.580 | 3.550 | 0.991 |
| genus-one | strongly-unreduced/theta3/cold | 100 | 25.107 | 25.437 | 1.013 |
| genus-one | strongly-unreduced/theta4/warm | 100 | 3.480 | 3.423 | 0.984 |
| genus-one | strongly-unreduced/theta4/cold | 100 | 25.192 | 25.116 | 0.997 |
| genus-one | strongly-unreduced/theta3 d1/warm | 100 | 4.687 | 4.720 | 1.007 |
| genus-one | strongly-unreduced/theta3 d1/cold | 100 | 43.057 | 43.655 | 1.014 |
| genus-one | strongly-unreduced/theta3 d2/warm | 100 | 5.309 | 5.374 | 1.012 |
| genus-one | strongly-unreduced/theta3 d2/cold | 100 | 52.821 | 53.046 | 1.004 |
| theta | g1/zero | 30 | 0.926 | 0.924 | 0.998 |
| theta | g1/half | 30 | 0.964 | 0.961 | 0.996 |
| theta | g2-diagonal/zero | 30 | 5.204 | 5.120 | 0.984 |
| theta | g2-diagonal/half | 30 | 5.097 | 5.050 | 0.991 |
| theta | g2-coupled/zero | 30 | 6.153 | 6.149 | 0.999 |
| theta | g2-coupled/half | 30 | 6.297 | 6.357 | 1.009 |
| theta | g2-coupled/dz0 | 30 | 6.318 | 5.978 | 0.946 |
| theta | g2-coupled/half-dz0 | 30 | 6.067 | 6.212 | 1.024 |
| theta | g3-diagonal/zero | 30 | 40.347 | 40.625 | 1.007 |
| theta | g3-diagonal/half | 30 | 41.823 | 41.890 | 1.002 |
| theta | g3-coupled/zero | 30 | 48.296 | 47.867 | 0.991 |
| theta | g3-coupled/half | 30 | 49.524 | 48.775 | 0.985 |
| theta | g3-coupled/dz0 | 30 | 51.201 | 51.094 | 0.998 |
| theta | g3-coupled/half-dz0 | 30 | 52.062 | 52.329 | 1.005 |
| theta | g2-near-boundary/zero | 30 | 6.051 | 6.241 | 1.031 |
| theta | g2-near-boundary/half | 30 | 6.115 | 6.210 | 1.016 |
| theta | g2-unreduced/zero | 30 | 2.702 | 2.774 | 1.026 |
| theta | g2-unreduced/half | 30 | 2.793 | 2.820 | 1.009 |
| theta | g2-unreduced/real | 30 | 2.802 | 2.817 | 1.006 |
| theta | g3-unreduced/zero | 30 | 25.963 | 25.833 | 0.995 |
| theta | g3-unreduced/half | 30 | 28.016 | 28.110 | 1.003 |
| theta | g3-unreduced/real | 30 | 26.697 | 26.567 | 0.995 |
| theta | g3-block/zero | 30 | 45.813 | 46.101 | 1.006 |
| theta | g3-block/half | 30 | 47.146 | 46.918 | 0.995 |
| theta | g1/zero | 100 | 1.426 | 1.452 | 1.018 |
| theta | g1/half | 100 | 1.379 | 1.406 | 1.020 |
| theta | g2-diagonal/zero | 100 | 13.912 | 13.987 | 1.005 |
| theta | g2-diagonal/half | 100 | 13.830 | 13.808 | 0.998 |
| theta | g2-coupled/zero | 100 | 15.166 | 14.952 | 0.986 |
| theta | g2-coupled/half | 100 | 15.159 | 15.116 | 0.997 |
| theta | g2-coupled/dz0 | 100 | 14.244 | 14.254 | 1.001 |
| theta | g2-coupled/half-dz0 | 100 | 14.626 | 14.475 | 0.990 |
| theta | g3-diagonal/zero | 100 | 175.803 | 175.275 | 0.997 |
| theta | g3-diagonal/half | 100 | 178.930 | 178.572 | 0.998 |
| theta | g3-coupled/zero | 100 | 211.246 | 209.626 | 0.992 |
| theta | g3-coupled/half | 100 | 213.307 | 208.183 | 0.976 |
| theta | g2-near-boundary/zero | 100 | 14.953 | 14.977 | 1.002 |
| theta | g2-near-boundary/half | 100 | 15.140 | 14.894 | 0.984 |
| theta | g2-unreduced/zero | 100 | 5.400 | 5.377 | 0.996 |
| theta | g2-unreduced/half | 100 | 5.486 | 5.535 | 1.009 |
| theta | g2-unreduced/real | 100 | 5.599 | 5.601 | 1.000 |
| theta | g3-unreduced/zero | 100 | 102.215 | 102.626 | 1.004 |
| theta | g3-unreduced/half | 100 | 105.056 | 105.515 | 1.004 |
| theta | g3-unreduced/real | 100 | 104.758 | 103.464 | 0.988 |
| theta | g3-block/zero | 100 | 202.294 | 201.194 | 0.995 |
| theta | g3-block/half | 100 | 205.050 | 202.036 | 0.985 |
| jets | g2-coupled/theta2 | 24 | 2.725 | 2.723 | 0.999 |
| jets | g2-coupled/theta3 | 24 | 4.095 | 4.028 | 0.984 |
| jets | g2-coupled/sigma3 | 24 | 5.034 | 5.013 | 0.996 |
| ba | g2-coupled/coordinate | 24 | 38.914 | 28.366 | 0.729 |
| ba | g2-coupled/dense | 24 | 38.710 | 29.242 | 0.755 |
| jets | g3-coupled/theta2 | 24 | 29.715 | 30.004 | 1.010 |
| jets | g3-coupled/theta3 | 24 | 55.020 | 55.205 | 1.003 |
| jets | g3-coupled/sigma3 | 24 | 62.750 | 63.109 | 1.006 |
| ba | g3-coupled/coordinate | 24 | 431.385 | 225.059 | 0.522 |
| ba | g3-coupled/dense | 24 | 451.641 | 244.123 | 0.541 |
| jets | g2-unreduced/theta2 | 24 | 2.719 | 2.739 | 1.007 |
| jets | g2-unreduced/theta3 | 24 | 5.290 | 5.320 | 1.006 |
| jets | g2-unreduced/sigma3 | 24 | 6.024 | 5.979 | 0.992 |
| ba | g2-unreduced/coordinate | 24 | 42.616 | 28.079 | 0.659 |
| ba | g2-unreduced/dense | 24 | 42.287 | 28.508 | 0.674 |
| jets | g3-unreduced/theta2 | 24 | 15.860 | 15.896 | 1.002 |
| jets | g3-unreduced/theta3 | 24 | 36.113 | 35.836 | 0.992 |
| jets | g3-unreduced/sigma3 | 24 | 39.877 | 39.880 | 1.000 |
| ba | g3-unreduced/coordinate | 24 | 265.760 | 161.132 | 0.606 |
| ba | g3-unreduced/dense | 24 | 265.768 | 162.134 | 0.610 |
| jets | issue17/theta2 | 24 | 64.066 | 45.243 | 0.706 |
| jets | issue17/theta3 | 24 | 153.401 | 88.419 | 0.576 |
| jets | issue17/sigma3 | 24 | 173.056 | 99.897 | 0.577 |
| ba | issue17/coordinate | 24 | 1092.110 | 410.120 | 0.376 |
| ba | issue17/dense | 24 | 1093.082 | 499.809 | 0.457 |
| jets | g2-coupled/theta2 | 40 | 3.673 | 3.643 | 0.992 |
| jets | g2-coupled/theta3 | 40 | 5.560 | 5.534 | 0.995 |
| jets | g2-coupled/sigma3 | 40 | 6.422 | 6.415 | 0.999 |
| ba | g2-coupled/coordinate | 40 | 48.778 | 35.760 | 0.733 |
| ba | g2-coupled/dense | 40 | 48.308 | 36.073 | 0.747 |
| jets | g3-coupled/theta2 | 40 | 47.554 | 47.070 | 0.990 |
| jets | g3-coupled/theta3 | 40 | 96.850 | 86.749 | 0.896 |
| jets | g3-coupled/sigma3 | 40 | 99.593 | 100.577 | 1.010 |
| ba | g3-coupled/coordinate | 40 | 683.617 | 329.668 | 0.482 |
| ba | g3-coupled/dense | 40 | 687.662 | 357.511 | 0.520 |
| jets | g2-unreduced/theta2 | 40 | 3.321 | 3.432 | 1.034 |
| jets | g2-unreduced/theta3 | 40 | 5.731 | 5.700 | 0.995 |
| jets | g2-unreduced/sigma3 | 40 | 6.433 | 6.396 | 0.994 |
| ba | g2-unreduced/coordinate | 40 | 46.745 | 33.176 | 0.710 |
| ba | g2-unreduced/dense | 40 | 46.884 | 33.121 | 0.706 |
| jets | g3-unreduced/theta2 | 40 | 23.836 | 24.075 | 1.010 |
| jets | g3-unreduced/theta3 | 40 | 47.664 | 47.912 | 1.005 |
| jets | g3-unreduced/sigma3 | 40 | 52.276 | 51.822 | 0.991 |
| ba | g3-unreduced/coordinate | 40 | 348.663 | 225.668 | 0.647 |
| ba | g3-unreduced/dense | 40 | 348.908 | 225.635 | 0.647 |
| jets | issue17/theta2 | 40 | 127.789 | 74.545 | 0.583 |
| jets | issue17/theta3 | 40 | 260.768 | 154.258 | 0.592 |
| jets | issue17/sigma3 | 40 | 281.234 | 167.766 | 0.597 |
| ba | issue17/coordinate | 40 | 1737.215 | 605.955 | 0.349 |
| ba | issue17/dense | 40 | 1747.253 | 734.880 | 0.421 |
| theta | g1/zero | 50 | 0.959 | 0.956 | 0.997 |
| theta | g1/half | 50 | 0.983 | 0.991 | 1.007 |
| theta | g2-diagonal/zero | 50 | 7.488 | 7.333 | 0.979 |
| theta | g2-diagonal/half | 50 | 8.518 | 7.995 | 0.939 |
| theta | g2-coupled/zero | 50 | 8.608 | 8.559 | 0.994 |
| theta | g2-coupled/half | 50 | 8.809 | 8.585 | 0.975 |
| theta | g2-coupled/dz0 | 50 | 8.273 | 8.246 | 0.997 |
| theta | g2-coupled/half-dz0 | 50 | 8.766 | 8.364 | 0.954 |
| theta | g3-diagonal/zero | 50 | 70.786 | 70.083 | 0.990 |
| theta | g3-diagonal/half | 50 | 74.181 | 73.077 | 0.985 |
| theta | g3-coupled/zero | 50 | 86.117 | 85.637 | 0.994 |
| theta | g3-coupled/half | 50 | 87.559 | 86.536 | 0.988 |
| theta | g3-coupled/dz0 | 50 | 85.953 | 85.403 | 0.994 |
| theta | g3-coupled/half-dz0 | 50 | 85.990 | 85.062 | 0.989 |
| theta | g2-near-boundary/zero | 50 | 8.393 | 8.480 | 1.010 |
| theta | g2-near-boundary/half | 50 | 8.540 | 8.452 | 0.990 |
| theta | g2-unreduced/zero | 50 | 3.576 | 3.476 | 0.972 |
| theta | g2-unreduced/half | 50 | 3.703 | 3.619 | 0.977 |
| theta | g2-unreduced/real | 50 | 3.658 | 3.609 | 0.987 |
| theta | g3-unreduced/zero | 50 | 45.487 | 44.882 | 0.987 |
| theta | g3-unreduced/half | 50 | 44.009 | 43.291 | 0.984 |
| theta | g3-unreduced/real | 50 | 45.917 | 45.222 | 0.985 |
| theta | g3-block/zero | 50 | 81.708 | 81.958 | 1.003 |
| theta | g3-block/half | 50 | 82.760 | 81.770 | 0.988 |

## Repeat check

| Case/workload | dps | Samples | Order | Previous ms | Candidate ms | Ratio |
|---|---:|---:|---|---:|---:|---:|
| comfortable/theta3 d1/warm | 50 | 31 | reversed | 1.779 | 1.800 | 1.012 |
