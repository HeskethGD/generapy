# v0.2.0 pre-release benchmark record

These are **pre-release v0.2.0 measurements**, not a claim that v0.2.0 has been published.

- Generated: 2026-11-16T01:28:22+00:00
- Previous main: `6134a3d99152e6948f0aea58948e732a2e8d868b`
- Candidate: `4f6475f3824461e8c0e8226b6806e8bd17189ad2`
- Python: 3.14.7; mpmath: 1.4.1
- Platform: macOS-27.0.1-arm64-arm-64bit-Mach-O
- Revisions were archived from Git into separate temporary directories and imported in isolated processes. The checkout was not switched.
- No Sage, Wolfram, FLINT, PARI or external theta implementation was launched.

## Matched revision comparison

Lower candidate / previous time ratios are better. One means equal measured time.
The summary uses geometric means of workload ratios, not pooled wall times.
All 268 workload/precision combinations passed: 266 numerical comparisons and
both expected singular-curve rejections. The numerical outputs agree to their
serialized working-precision digits; curve validation passed in every valid trial.

| Group | Combinations | Candidate / previous, geometric mean | Range |
|---|---:|---:|---:|
| genus-one | 96 | 1.004 | 0.943–1.156 |
| theta | 70 | 0.995 | 0.939–1.031 |
| jets | 30 | 0.901 | 0.576–1.034 |
| ba | 20 | 0.580 | 0.349–0.755 |
| curves | 52 | 1.000 | 0.979–1.028 |

The largest initial increase was `comfortable/theta3 d1/warm` at 50 digits:
ratio 1.156 (15.6% slower).
With **31 samples and reversed revision order**, the ratio was
1.012 (1.2% slower).
The initial large increase did not repeat. In the complete curve comparison,
ratios ranged from 0.979
to 1.028; curve source is
unchanged between the revisions.

These samples do not demonstrate a repeatable large regression in the tested
workloads. They do not establish a bound for all inputs. The theta selector
remains heuristic; small measured changes and sampling variation are retained
in the full tables rather than removed.

- [Theta, mixed-jet and BA results](theta_and_ba.md)
- [Curve-period results, including historical times](curve_periods.md)

## Context against saved v0.1.0 numbers

The historical theta reports used Python 3.13.4 and an older, then
mpmath-integrated revision; the saved curve table omits interpreter metadata.
These comparisons reuse their mathematical inputs and only their
Generapy-side timings. They include intervening development and environment
changes, so they must **not** be attributed to this PR. Result-cache hits are
excluded here so the comparison measures numerical evaluation.

| Historical workload | Matching rows | Previous main / saved | Candidate / saved | Candidate range |
|---|---:|---:|---:|---:|
| Genus-one warm | 48 | 0.926 | 0.928 | 0.426–1.129 |
| Genus-one cold | 48 | 1.041 | 1.048 | 0.586–1.112 |
| Historical higher-genus theta table (including genus-one control) | 40 | 0.911 | 0.904 | 0.802–1.046 |
| Curve periods | 50 | 0.810 | 0.810 | 0.503–1.041 |

Cold genus-one timing is somewhat higher than the saved report overall.
The matched cold genus-one ratio is 1.007 (0.7% slower); previous main
already has most of the saved-report difference. This does not demonstrate a
large cold-start regression introduced by this branch. Warm genus-one, the
higher-genus theta table and curve-period
timings are lower overall than the saved numbers; individual rows can differ.

## Protocol and reproduction

Genus-one cases use 50/100 digits, scalar theta 30/50/100, mixed jets and
BA 24/40, and curves 30/50. Numerical workloads have one untimed warm-up
and seven timed samples per revision. Result caches are cleared before each
sample; setup caches remain
warm. Cold genus-one workloads clear all theta caches before each point.
BA samples evaluate four reference-normalized shifts and retain denominator
reuse within each sample. New direction-only APIs have no counterpart in
previous main, so the comparison uses existing public theta/sigma/BA APIs.

The revision running first alternates between workload combinations. Curve
cases have three trials per revision, alternating order within each case. Each
curve trial uses the existing period worker in a fresh process, with 15 extra
working digits. Imports, fixed warm-up, serialization and validation are excluded
from its timed curve construction and full first-kind period calculation.
The complete 26-case historical curve catalog is included at 30 and 50 digits,
including the expected singular-curve rejection.

The primary run included scalar theta at 30/100 digits. A supplemental run
added all 50-digit rows to match the historical table exactly. No first-run
samples were discarded. The repeat check above is reported separately.
The primary runner was committed as `4f6475f`; the supplemental precision
option and repeat runner were committed as `efd329f`. Equivalent workload
coverage can be reproduced in one run:

```sh
python -m benchmarks.benchmark_generapy_revisions \
  --before 6134a3d99152e6948f0aea58948e732a2e8d868b --after 4f6475f3824461e8c0e8226b6806e8bd17189ad2 \
  --theta-dps 30 50 100 --output /tmp/generapy-v020-revisions.json
python -m benchmarks.benchmark_generapy_revisions \
  --before 6134a3d99152e6948f0aea58948e732a2e8d868b --after 4f6475f3824461e8c0e8226b6806e8bd17189ad2 \
  --groups genus-one --filter 'genus-one/comfortable/theta3 d1/warm/50' \
  --repeats 31 --reverse-order --output /tmp/generapy-v020-repeat.json
```

Only aggregated Markdown is committed here. Raw samples remain untracked.
The runner verifies import locations, output agreement and unchanged sources;
all source-stability checks passed. Harness SHA-256 values for the recorded runs:


- `d19092ead96ce98e31008816f9d2c0f4699f039610a137cd018e30d783328637`
- `9f8e6caef97ed0197d87196b45eb7874de9623b4372605c91dc2080203cc305a`
