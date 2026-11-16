# Integration follow-up for issues #9 and #10

Pre-release v0.2.0 measurements, generated 2026-11-16T12:43:36+00:00.
This is a later checkpoint than the theta/BA comparison in this directory.

- Before: `c02262cb4b89047a11127d28f5213641ada02fd2` (main after PR #24).
- Candidate: `ac5ae8d36e9705e538461005573741adf1c4c5fe`.
- Fixes: `483535a` shares chart coordinate checks; `66e51fe` shares hyperelliptic branch factors.
- Python 3.14.7, mpmath 1.4.1; macOS-27.0.1-arm64-arm-64bit-Mach-O.
- Before source was archived into a temporary directory; candidate source was committed and the tracked checkout was clean during final measurements.
- The same benchmark runners and inputs were used sequentially for both sources. No tests or competing benchmarks ran alongside them.
- Raw samples and profiles remain untracked. No external mathematical tools were run.

## Findings and changes

The jet optimizations do not directly accelerate these integration routes.
Both reported gaps reproduced on previous main at 40 digits: approximately
16x for chart integration and 8x for the complex finite-base Abel call relative
to their direct-quadrature references. These are distinct sources of overhead.

**Chart integration (#9).** Each scalar pullback previously performed the
coordinate conversion and ambient-curve validation again, so integrating two
forms repeated them at the same quadrature node. Residual and scale calculation
also repeated the same polynomial monomials. The candidate evaluates the forms
as a batch with one validated coordinate map per node and shares those
polynomial terms. Every node still undergoes coordinate validation. Newton
correction, sheet-separation checks, ambiguous-node refinement and endpoint
label checks are retained.

**Finite-base Abel integration (#10).** The automatic route cancels a shared
branch reference, then evaluates its marked branch-to-target/base paths. Each
differential component previously recalculated the same product of continued
square roots at common quadrature nodes. The candidate reuses that product and
the abscissa within one path evaluation, keyed by node and working precision.
Each component retains its adaptive quadrature and error test. Root-product
branches, anchor selection and integration paths are unchanged. Reuse does not
persist across calls, targets or numerical contexts.

At 40 digits in the final matched local benchmark:

| Workload | Before s | Candidate s | Before / candidate |
|---|---:|---:|---:|
| real-branch, chart | 0.154779 | 0.119045 | 1.30x |
| real-branch, finite-base-abel | 0.020330 | 0.010810 | 1.88x |
| complex-regular, finite-base-abel | 0.084167 | 0.046853 | 1.80x |
| genus-one-control, finite-base-abel | 0.006591 | 0.005797 | 1.14x |
| genus-three-control, finite-base-abel | 0.042221 | 0.015599 | 2.71x |

The chart improvement is about 23–24% over 20/40/80 digits in this local
fixture; the complex Abel improvement is about 44%. Genus-three sharing gives
about 2.6–2.8x speedup, while the genus-one control improves about 11–12%.
These are sampled local timings, not portable performance guarantees.

Remaining chart cost includes Newton corrections and sheet/ambient validation
at each quadrature node. The direct reference knows its square-root branch
analytically. The complex automatic Abel result still takes about 4.4x its direct
reference time and about 3.2x `path-and-integral` at 40 digits. Its two marked
paths are longer than the short direct segment. Further path shortening would
need to establish compatible lifts and period conventions; it is beyond these
shared-work optimizations. For a deliberately selected finite contour,
`Curve.path` plus `Curve.integral` already provides the explicit integration
route; exposing automatic forms (#13) would make that route more convenient.

## Validation and protocol

196 focused tests passed across chart integration, chart contracts,
hyperelliptic Abel/period calculations, shared first-/second-kind lifts,
Kleinian Curve inputs and BA jets. Added checks cover batch evaluation under
order refinement, invalid ambient coordinates, monomial integrals on both
sheets of odd/even-degree curves and identical quadrature nodes requested at
different precisions. Changed numerical lines have 100% diff coverage.

All 33 local-integral combinations and all 21 chart controls passed the
existing benchmark accuracy checks on both sources. Reported errors are
identical before/after in every row; all chart continuation segment/refinement
counts also match. The local runner uses an eight-decimal-digit tolerance
margin and the chart runner a three-digit margin; actual scaled errors are
included below. The genus-three 40-digit control differs from its default
quadrature reference by approximately 6.4e-38 in both sources. These benchmark
checks complement the stricter mathematical regression tests.

Each local method has a fresh context/curve, one first timed call and seven
subsequent timed samples. Construction and independent reference calculations
are excluded. The complex fixture prepares its reusable path outside timing;
`path-and-integral` constructs a path again inside each measured call. The
chart-control runner warms each operation before five timed samples; continuation
measurements batch 20 calls per sample. All target precisions are 20/40/80 digits.

## Complete local-integral results

Times include all returned differential components. First-call times are shown
separately from warm medians. `Before / candidate` above one means faster.

| Case | Method | dps | Before first s | Candidate first s | Before warm s | Candidate warm s | Before / candidate | Scaled error, both sources |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| real-branch | direct | 20 | 0.005160 | 0.005125 | 0.003471 | 0.003505 | 0.990 | 0.0 |
| real-branch | chart | 20 | 0.081412 | 0.067424 | 0.063520 | 0.048318 | 1.315 | 2.11758236814e-22 |
| real-branch | finite-base-abel | 20 | 0.023835 | 0.015475 | 0.017463 | 0.009020 | 1.936 | 0.0 |
| complex-regular | direct | 20 | 0.005138 | 0.005112 | 0.004253 | 0.004347 | 0.978 | 0.0 |
| complex-regular | prebuilt-path | 20 | 0.026966 | 0.027138 | 0.005648 | 0.005546 | 1.018 | 1.07163794357e-22 |
| complex-regular | path-and-integral | 20 | 0.029625 | 0.056583 | 0.007806 | 0.008053 | 0.969 | 1.07163794357e-22 |
| complex-regular | finite-base-abel | 20 | 0.079006 | 0.044456 | 0.069926 | 0.038923 | 1.797 | 0.0 |
| genus-one-control | direct | 20 | 0.003085 | 0.003103 | 0.001562 | 0.001573 | 0.993 | 0.0 |
| genus-one-control | finite-base-abel | 20 | 0.005042 | 0.004907 | 0.002832 | 0.002533 | 1.118 | 0.0 |
| genus-three-control | direct | 20 | 0.010138 | 0.010953 | 0.008435 | 0.008595 | 0.981 | 0.0 |
| genus-three-control | finite-base-abel | 20 | 0.024684 | 0.013490 | 0.017649 | 0.006916 | 2.552 | 0.0 |
| real-branch | direct | 40 | 0.013444 | 0.013627 | 0.009865 | 0.010061 | 0.981 | 0.0 |
| real-branch | chart | 40 | 0.252924 | 0.218953 | 0.154779 | 0.119045 | 1.300 | 1.14794370197e-41 |
| real-branch | finite-base-abel | 40 | 0.026696 | 0.018310 | 0.020330 | 0.010810 | 1.881 | 0.0 |
| complex-regular | direct | 40 | 0.012328 | 0.012525 | 0.010569 | 0.010631 | 0.994 | 0.0 |
| complex-regular | prebuilt-path | 40 | 0.112206 | 0.114396 | 0.012185 | 0.012081 | 1.009 | 3.61524140854e-43 |
| complex-regular | path-and-integral | 40 | 0.113052 | 0.114637 | 0.014575 | 0.014677 | 0.993 | 3.61524140854e-43 |
| complex-regular | finite-base-abel | 40 | 0.090896 | 0.053083 | 0.084167 | 0.046853 | 1.796 | 0.0 |
| genus-one-control | direct | 40 | 0.007501 | 0.007240 | 0.003765 | 0.003898 | 0.966 | 0.0 |
| genus-one-control | finite-base-abel | 40 | 0.010728 | 0.010028 | 0.006591 | 0.005797 | 1.137 | 0.0 |
| genus-three-control | direct | 40 | 0.021270 | 0.020821 | 0.017497 | 0.017356 | 1.008 | 0.0 |
| genus-three-control | finite-base-abel | 40 | 0.051933 | 0.025281 | 0.042221 | 0.015599 | 2.707 | 6.36104303857e-38 |
| real-branch | direct | 80 | 0.035055 | 0.035542 | 0.025961 | 0.025817 | 1.006 | 0.0 |
| real-branch | chart | 80 | 0.828185 | 0.735600 | 0.340771 | 0.258805 | 1.317 | 2.10843958865e-81 |
| real-branch | finite-base-abel | 80 | 0.067736 | 0.040683 | 0.053961 | 0.027621 | 1.954 | 0.0 |
| complex-regular | direct | 80 | 0.032935 | 0.032912 | 0.027885 | 0.027685 | 1.007 | 0.0 |
| complex-regular | prebuilt-path | 80 | 0.496761 | 0.503520 | 0.029808 | 0.029715 | 1.003 | 3.32007488484e-83 |
| complex-regular | path-and-integral | 80 | 0.501854 | 0.505857 | 0.032963 | 0.033013 | 0.998 | 3.32007488484e-83 |
| complex-regular | finite-base-abel | 80 | 0.243258 | 0.141469 | 0.227059 | 0.126888 | 1.789 | 0.0 |
| genus-one-control | direct | 80 | 0.019171 | 0.019511 | 0.010100 | 0.010237 | 0.987 | 0.0 |
| genus-one-control | finite-base-abel | 80 | 0.027344 | 0.026120 | 0.016689 | 0.014807 | 1.127 | 0.0 |
| genus-three-control | direct | 80 | 0.063525 | 0.064070 | 0.054244 | 0.053929 | 1.006 | 0.0 |
| genus-three-control | finite-base-abel | 80 | 0.162662 | 0.058332 | 0.113687 | 0.040581 | 2.802 | 0.0 |

## Complete chart-control results

Median seconds. Continuation is unchanged algorithmically; its measurements
serve as a control. Integral times include continuation and all forms.

| Case | dps | Before continuation s | Candidate continuation s | Before integral s | Candidate integral s | Before / candidate integral | Scaled error, both sources |
|---|---:|---:|---:|---:|---:|---:|---:|
| turning-point-1-segments | 20 | 0.009296 | 0.009240 | 0.126761 | 0.097126 | 1.305 | 1.37608144128e-21 |
| turning-point-32-segments | 20 | 0.012915 | 0.013002 | 0.237660 | 0.177548 | 1.339 | 1.37608144128e-21 |
| degree-1 | 20 | 0.000226 | 0.000224 | 0.003066 | 0.002819 | 1.088 | 3.27714791346e-21 |
| degree-3 | 20 | 0.002078 | 0.002049 | 0.023935 | 0.022392 | 1.069 | 5.56746973262e-21 |
| complex-square-root | 20 | 0.001211 | 0.001197 | 0.017342 | 0.016854 | 1.029 | 3.59365644535e-21 |
| infinity-chart-tail | 20 | 0.000331 | 0.000319 | 0.004670 | 0.004383 | 1.066 | 2.32934060495e-21 |
| finite-degree-drop | 20 | 0.000376 | 0.000378 | 0.005025 | 0.004637 | 1.084 | 1.4823076577e-21 |
| turning-point-1-segments | 40 | 0.010703 | 0.010629 | 0.274265 | 0.207839 | 1.320 | 1.86493811018e-41 |
| turning-point-32-segments | 40 | 0.015027 | 0.015000 | 0.516371 | 0.392371 | 1.316 | 5.73971850987e-42 |
| degree-1 | 40 | 0.000241 | 0.000241 | 0.006160 | 0.005520 | 1.116 | 1.48045453639e-41 |
| degree-3 | 40 | 0.002360 | 0.002361 | 0.051602 | 0.048978 | 1.054 | 2.5151094914e-41 |
| complex-square-root | 40 | 0.001465 | 0.001476 | 0.040097 | 0.039194 | 1.023 | 1.14794370197e-41 |
| infinity-chart-tail | 40 | 0.000375 | 0.000372 | 0.010380 | 0.009831 | 1.056 | 4.01780295691e-41 |
| finite-degree-drop | 40 | 0.000426 | 0.000435 | 0.010938 | 0.010484 | 1.043 | 8.60957776481e-42 |
| turning-point-1-segments | 80 | 0.012626 | 0.012471 | 0.605000 | 0.460785 | 1.313 | 3.42535033306e-81 |
| turning-point-32-segments | 80 | 0.017603 | 0.017472 | 1.154734 | 0.874163 | 1.321 | 1.58132969148e-81 |
| degree-1 | 80 | 0.000262 | 0.000258 | 0.011934 | 0.010603 | 1.125 | 1.35958276889e-81 |
| degree-3 | 80 | 0.002768 | 0.002720 | 0.115389 | 0.108712 | 1.061 | 2.30976328034e-81 |
| complex-square-root | 80 | 0.001933 | 0.001914 | 0.105754 | 0.102112 | 1.036 | 0.0 |
| infinity-chart-tail | 80 | 0.000425 | 0.000422 | 0.023776 | 0.022198 | 1.071 | 5.27109897162e-81 |
| finite-degree-drop | 80 | 0.000489 | 0.000490 | 0.024915 | 0.023538 | 1.059 | 0.0 |

## Reproduction

Create a temporary source snapshot of the before commit and run the same
committed runner against it and the candidate. Run commands sequentially.
The runner's `--source` selects the imported numerical code; changing the
checkout is unnecessary. Source hashes include a generated version file when
present, so commit provenance is recorded above as well.

```sh
mkdir -p /tmp/generapy-integration-before
git archive c02262cb4b89047a11127d28f5213641ada02fd2 src | tar -x -C /tmp/generapy-integration-before
python benchmarks/curves/benchmark_local_integrals.py \
  --source /tmp/generapy-integration-before/src --digits 20 40 80 --trials 7
python benchmarks/curves/benchmark_local_integrals.py \
  --source src --digits 20 40 80 --trials 7
python benchmarks/curves/benchmark_chart_continuation.py \
  --source /tmp/generapy-integration-before/src --digits 20 40 80 --trials 5
python benchmarks/curves/benchmark_chart_continuation.py \
  --source src --digits 20 40 80 --trials 5
```

Create the temporary directory first, and use the recorded candidate source
for the `src` runs. Redirect JSON stdout to an ignored location if saving raw
reports. The local runner's before/after source hashes were:

- Before: `d4a7c52eccc2dc8a7d7611e96ab546a2a4554b28d529374c3f1e462ed1e3f7fa`
- Candidate: `3bbc1ca3f073f6f01df4442b15447cc8a5e10364a14604f2b45df627f27fb1d6`
