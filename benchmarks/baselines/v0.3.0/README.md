# v0.3.0 release-candidate baselines

Prepared 2026-11-22T02:39:01+00:00.
This is release preparation; it does not assert that v0.3.0 is published.

- Published reference: `v0.2.0`, commit `cd98830890aae1ae5d231b13980345733775bd2e`.
- Candidate: `a688d64852d49ffe6322a8c32bc84233e78e8401`.
- Python 3.14.7; mpmath 1.4.1.
- Platform: macOS-27.0.1-arm64-arm-64bit-Mach-O.
- Separate archived source snapshots were imported in isolated processes.
- No external mathematics engine was launched. Source and harness stability checks passed.

## Complete matched comparison

All 268 configurations passed: 266 numerical comparisons and two expected
singular-curve rejection configurations. Every valid curve trial passed its
validation. Lower candidate/reference ratios indicate faster measured execution.

| Group | Configurations | Geometric mean ratio | Ratio range |
| --- | ---: | ---: | ---: |
| genus-one | 96 | 0.992 | 0.936–1.054 |
| theta | 70 | 0.976 | 0.605–1.107 |
| jets | 30 | 0.991 | 0.895–1.034 |
| ba | 20 | 0.985 | 0.954–0.998 |
| curves | 52 | 0.996 | 0.902–1.047 |

The summary is the geometric mean of per-configuration median-time ratios,
not a pooled wall-time ratio. Timing ranges are descriptive, not confidence
intervals or guarantees for all inputs. Theta, sigma and BA evaluator source
is unchanged since v0.2.0; curve implementation changes are the focus of this
release. Individual increases and measurement variability are retained below.

- [Theta, genus-one, mixed-jet and BA tables](theta_and_ba.md)
- [All 26 curve cases at 30 and 50 digits](curve_periods.md)
- [Targeted genus-four pipeline profile and new-support checks](general_curve_pipeline.md)
- [Fresh v0.3.0 general-curve pipeline trials](pipeline_fresh.md)

The historical catalogue excludes the difficult issue #33 curve and does not
measure first/repeated Abel maps or Riemann constants. Its broadly unchanged
timings establish stability for those existing workloads. The separate pipeline
benchmark covers the optimized workload: six fresh v0.3.0 trials reproduce the
optimized development timings. The historical pre-fix comparison remains
separately labelled; it was not rerun to create this addition.

## Largest measured ratios

These are initial measurements, not declarations of statistically established
regressions. All numerical comparisons passed.

| Workload | Digits | v0.2.0 seconds | Candidate seconds | Candidate / v0.2.0 | Scaled error |
| --- | ---: | ---: | ---: | ---: | ---: |
| g2-coupled/half | 30 | 0.00715067 | 0.00791542 | 1.10695 | 0.0 |
| g2-near-boundary/half | 30 | 0.00634358 | 0.00682479 | 1.07586 | 0.0 |
| g2-coupled/zero | 30 | 0.00631121 | 0.00668325 | 1.05895 | 0.0 |
| generic/theta1/warm | 50 | 0.00170367 | 0.00179546 | 1.05388 | 0.0 |
| g1/zero | 100 | 0.0014375 | 0.00151163 | 1.05157 | 0.0 |
| hyper-g4-symmetric | 50 | 0.600818 | 0.628846 | 1.04665 | 0.0 |
| g2-diagonal/half | 50 | 0.00820308 | 0.00848458 | 1.03432 | 0.0 |
| g2-coupled/theta3 | 24 | 0.00406888 | 0.00420583 | 1.03366 | 0.0 |

## Targeted repeat check

The largest initial increase was `theta/g2-coupled/half` at 30 digits,
ratio 1.107. With 31 samples and reversed revision order, the ratio was
1.008. The initial approximately 11% increase did not repeat at
that magnitude. Both runs and the initial table are retained; apparent
speed-ups in unchanged evaluator code are also treated as timing variation.

```sh
.venv/bin/python -m benchmarks.benchmark_generapy_revisions \
  --before v0.2.0 --after a688d64852d49ffe6322a8c32bc84233e78e8401 \
  --groups theta --theta-dps 30 --filter 'theta/g2-coupled/half/30' \
  --repeats 31 --reverse-order --output /tmp/generapy-v030-repeat.json
```

## Protocol

The existing matched-revision harness was run with all workload groups,
scalar-theta precisions 30/50/100, seven numerical samples per revision and
three fresh-process curve trials per revision. Revision order alternates.
The numerical jobs include an untimed warm-up; evaluated-result caches are
cleared for each sample. Curve imports, warm-up, serialization and validation
are outside the measured construction/full-period calculation. Curve working
precision has 15 extra decimal digits. The expected singular case is retained
at both precisions, with no timing ratio assigned.

The harness requires maximum scaled output difference below `10**(5-dps)`.
Scaled difference is `abs(after-before)/max(1,abs(before))` across output
components. This is a sampled numerical check, not a universal error bound.

Reproduction (choose a new output path):

```sh
.venv/bin/python -m benchmarks.benchmark_generapy_revisions \
  --before v0.2.0 --after a688d64852d49ffe6322a8c32bc84233e78e8401 \
  --theta-dps 30 50 100 --output /tmp/generapy-v030-revisions.json
```

Harness SHA-256: `bd00c2497ce16a2e75deed5d823ab9670ae8364d988276f6dd4b20730bd7b01a`.
Only curated Markdown reports are tracked; raw samples remain ignored.
The final preparation commits add documentation and reports; numerical source
is unchanged from the measured candidate.
