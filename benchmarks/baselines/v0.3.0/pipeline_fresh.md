# Fresh general-curve pipeline measurements

Recorded 2026-11-22T02:58:26.084450+00:00; Python 3.14.7, mpmath 1.4.1.
Platform: macOS-27.0.1-arm64-arm-64bit-Mach-O.

Only the issue #33 supplied-basis genus-four workload was run.
The existing 268-configuration release comparison was not rerun or modified.

## Protocol

Each precision/revision has 3 fresh-process trials from archived committed source.
Import, curve construction, fibre point selection and validation are excluded from timings.
Stages run in table order on the same curve: periods reuse genus setup;
the first Abel call follows periods; repeat and nearby calls reuse the marked setup.
Riemann constants follow those Abel calls. No internal functions are patched.
Validation checks period validity, repeated Abel agreement, base-point subtraction,
Riemann vanishing at the effective divisor 3P, finite outputs and restored precision.
Saved outputs are also compared between trials, precisions and revisions when available.

## Source revisions

- after: `2319e889d25944af41e0b5035dbde543349c98cb`.

Harness SHA-256: `a84e60c09f47ff3d03dde8c9374d96a220ba66975a2cec97f3cc31c35bc7e7cf`.

## Timings

| Revision | Digits | Operation | Median seconds | Range | Trials |
| --- | ---: | --- | ---: | ---: | ---: |
| after | 20 | cold_genus | 1.6076 | 1.6026–1.6526 | 3 |
| after | 20 | periods_after_genus | 10.9191 | 10.7449–11.0276 | 3 |
| after | 20 | abel_first | 2.2263 | 2.2231–2.2397 | 3 |
| after | 20 | abel_repeat | 1.3747 | 1.3672–1.3781 | 3 |
| after | 20 | abel_nearby | 1.3793 | 1.3678–1.4213 | 3 |
| after | 20 | riemann_constant_after_abel | 6.7578 | 6.7274–6.7803 | 3 |
| after | 30 | cold_genus | 1.7173 | 1.7130–1.7247 | 3 |
| after | 30 | periods_after_genus | 15.9060 | 15.7647–15.9655 | 3 |
| after | 30 | abel_first | 2.9865 | 2.9722–3.0264 | 3 |
| after | 30 | abel_repeat | 1.8701 | 1.8629–1.8722 | 3 |
| after | 30 | abel_nearby | 1.8576 | 1.8558–1.8899 | 3 |
| after | 30 | riemann_constant_after_abel | 10.2722 | 10.1577–10.2759 | 3 |

## Accuracy

All 6 fresh trials passed the checks above.
Cross-run comparisons use maximum scaled difference abs(a-b)/max(1,abs(a)),
with tolerance 10**(5-dps) at the lower precision.

- after/20/1 versus after/20/2: `0.0`.
- after/20/1 versus after/20/3: `0.0`.
- after/20/1 versus after/30/1: `4.013571915121288398857066488995222225974e-20`.
- after/20/1 versus after/30/2: `4.013571915121288398857066488995222225974e-20`.
- after/20/1 versus after/30/3: `4.013571915121288398857066488995222225974e-20`.

These current-tag timings supplement the separately retained historical development
comparison. A candidate-only run establishes a repeatable baseline; it does not
constitute a newly matched speedup comparison against the historical measurements.

## Reproduction

```sh
python -m benchmarks.benchmark_general_curve_pipeline \
  --after 2319e889d25944af41e0b5035dbde543349c98cb --dps 20 30 --trials 3 \
  --output /tmp/generapy-pipeline.json --report /tmp/generapy-pipeline.md
```

Add `--before REV` for a fresh comparison, alternating revision order between trials.
Choose new output paths. Raw JSON remains untracked; only the Markdown report is retained.
