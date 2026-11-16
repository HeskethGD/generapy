# Curve-period revision comparison

These are **pre-release v0.2.0 measurements**, not a claim that v0.2.0 has been published.

- Generated: 2026-11-16T01:28:22+00:00
- Previous main: `6134a3d99152e6948f0aea58948e732a2e8d868b`
- Candidate: `4f6475f3824461e8c0e8226b6806e8bd17189ad2`
- Python: 3.14.7; mpmath: 1.4.1
- Platform: macOS-27.0.1-arm64-arm-64bit-Mach-O
- Revisions were archived from Git into separate temporary directories and imported in isolated processes. The checkout was not switched.
- No Sage, Wolfram, FLINT, PARI or external theta implementation was launched.

Three fresh-process trials per revision at each target precision, including
15 extra working digits. All valid trials passed curve validation. See
[protocol and interpretation](README.md). Times are median seconds per curve
construction and full first-kind period calculation.

The saved column comes from the [v0.1.0 report](../v0.1.0/curves_vs_sage.md).
It is historical context across environment and intervening code changes,
not a measurement of the effect of this PR. The matched previous-main column
is the regression control. All 26 historical cases are included.

| Case | Target digits | Saved v0.1.0 s | Previous main s | Candidate s | Candidate / previous | Candidate / saved |
|---|---:|---:|---:|---:|---:|---:|
| hyper-g1-lemniscatic | 30 | 0.0179 | 0.0154 | 0.0155 | 1.002 | 0.863 |
| hyper-g1-lemniscatic | 50 | 0.0404 | 0.0349 | 0.0354 | 1.013 | 0.876 |
| hyper-g2-symmetric | 30 | 0.0661 | 0.0559 | 0.0559 | 0.999 | 0.845 |
| hyper-g2-symmetric | 50 | 0.1488 | 0.1279 | 0.1290 | 1.008 | 0.867 |
| hyper-g3-symmetric | 30 | 0.1617 | 0.1379 | 0.1371 | 0.994 | 0.848 |
| hyper-g3-symmetric | 50 | 0.3637 | 0.3118 | 0.3100 | 0.994 | 0.852 |
| hyper-g2-even | 30 | 0.0875 | 0.0747 | 0.0743 | 0.994 | 0.849 |
| hyper-g2-even | 50 | 0.1969 | 0.1687 | 0.1685 | 0.999 | 0.856 |
| hyper-g2-clustered | 30 | 0.0995 | 0.0835 | 0.0835 | 1.000 | 0.840 |
| hyper-g2-clustered | 50 | 0.1350 | 0.1147 | 0.1154 | 1.006 | 0.854 |
| hyper-g3-generic | 30 | 0.1831 | 0.1713 | 0.1719 | 1.003 | 0.939 |
| hyper-g3-generic | 50 | 0.4825 | 0.3222 | 0.3227 | 1.002 | 0.669 |
| hyper-g4-symmetric | 30 | 0.3139 | 0.2666 | 0.2671 | 1.002 | 0.851 |
| hyper-g4-symmetric | 50 | 0.7150 | 0.6121 | 0.6031 | 0.985 | 0.844 |
| general-g1-lemniscatic | 30 | 0.7022 | 0.3943 | 0.3942 | 1.000 | 0.561 |
| general-g1-lemniscatic | 50 | 1.2219 | 0.6122 | 0.6146 | 1.004 | 0.503 |
| general-trig-g3 | 30 | 2.4747 | 2.5554 | 2.5769 | 1.008 | 1.041 |
| general-trig-g3 | 50 | 3.8921 | 3.1536 | 3.1395 | 0.996 | 0.807 |
| general-trig-pure-g3 | 30 | 1.2305 | 0.9625 | 0.9632 | 1.001 | 0.783 |
| general-trig-pure-g3 | 50 | 2.0086 | 1.6383 | 1.6344 | 0.998 | 0.814 |
| general-trig-dense-g3 | 30 | 2.2787 | 1.8577 | 1.8523 | 0.997 | 0.813 |
| general-trig-dense-g3 | 50 | 3.3456 | 2.8060 | 2.8084 | 1.001 | 0.839 |
| general-klein-quartic-g3 | 30 | 1.8868 | 1.5146 | 1.5111 | 0.998 | 0.801 |
| general-klein-quartic-g3 | 50 | 2.9192 | 2.3676 | 2.3473 | 0.991 | 0.804 |
| general-fermat-quartic-g3 | 30 | 1.6067 | 1.1388 | 1.1384 | 1.000 | 0.709 |
| general-fermat-quartic-g3 | 50 | 2.6083 | 2.0822 | 2.0865 | 1.002 | 0.800 |
| general-super-g4 | 30 | 1.5576 | 1.2300 | 1.2282 | 0.999 | 0.788 |
| general-super-g4 | 50 | 2.5104 | 2.0576 | 2.0575 | 1.000 | 0.820 |
| general-kovalevskaya-g3 | 30 | 11.5681 | 8.9103 | 8.9610 | 1.006 | 0.775 |
| general-kovalevskaya-g3 | 50 | 17.3893 | 13.3287 | 13.3016 | 0.998 | 0.765 |
| nonmonic-elliptic | 30 | 0.4870 | 0.3987 | 0.4059 | 1.018 | 0.833 |
| nonmonic-elliptic | 50 | 0.7903 | 0.6643 | 0.6828 | 1.028 | 0.864 |
| general-trig-test-g3 | 30 | 1.2913 | 1.0261 | 1.0049 | 0.979 | 0.778 |
| general-trig-test-g3 | 50 | 1.9211 | 1.5677 | 1.5651 | 0.998 | 0.815 |
| general-trig-infinity-g3 | 30 | 1.2954 | 0.9607 | 0.9606 | 1.000 | 0.742 |
| general-trig-infinity-g3 | 50 | 2.0972 | 1.6272 | 1.6246 | 0.998 | 0.775 |
| klein-x-translated | 30 | 2.7261 | 2.2026 | 2.1668 | 0.984 | 0.795 |
| klein-x-translated | 50 | 3.9036 | 3.0963 | 3.1156 | 1.006 | 0.798 |
| klein-x-scaled | 30 | 1.8711 | 1.5123 | 1.5116 | 1.000 | 0.808 |
| klein-x-scaled | 50 | 2.9047 | 2.3447 | 2.3372 | 0.997 | 0.805 |
| general-mu-x-translated | 30 | 3.1592 | 2.5477 | 2.5359 | 0.995 | 0.803 |
| general-mu-x-translated | 50 | 4.7009 | 3.7340 | 3.7437 | 1.003 | 0.796 |
| hyper-g2-close-001 | 30 | 0.1117 | 0.0845 | 0.0841 | 0.995 | 0.753 |
| hyper-g2-close-001 | 50 | 0.2097 | 0.1816 | 0.1810 | 0.997 | 0.863 |
| hyper-g2-close-00001 | 30 | 0.1584 | 0.1373 | 0.1366 | 0.994 | 0.862 |
| hyper-g2-close-00001 | 50 | 0.2722 | 0.2317 | 0.2325 | 1.004 | 0.854 |
| hyper-g2-complex | 30 | 0.6065 | 0.5115 | 0.5117 | 1.000 | 0.844 |
| hyper-g2-complex | 50 | 0.7095 | 0.6217 | 0.6247 | 1.005 | 0.880 |
| hyper-g1-linear-y | 30 | 0.0181 | 0.0159 | 0.0157 | 0.989 | 0.869 |
| hyper-g1-linear-y | 50 | 0.0399 | 0.0358 | 0.0356 | 0.992 | 0.891 |
| singular-g1-double-point | 30 | rejected | rejected | rejected | — | — |
| singular-g1-double-point | 50 | rejected | rejected | rejected | — | — |

The singular double-point input raised `ValueError` in all three trials on both revisions at both precisions; it is not a speed comparison.
