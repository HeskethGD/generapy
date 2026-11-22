# v0.3.0 targeted general-curve profile

This supplements the [release catalogue comparison](README.md) with the
adversarial genus-four fixture from [issue #33](https://github.com/HeskethGD/generapy/issues/33).
Its polynomial and supplied basis are also in the tracked
[genus-four regression](../../../tests/integration/test_curve_genus4_pipeline.py).

These measurements were captured at development checkpoint `0fc6ebc`.
The release candidate has identical numerical code; intervening changes are
documentation, merge metadata and benchmark reports. They are reused here
with their actual source revisions, rather than labelled as new tagged runs.
In this profile, pre-PR main is `b8c8f02`, which already includes resultant
robustness fixes; it is not the published v0.2.0 reference. No workaround was
applied to an old source tree. The spectral fixture is additional to the
26-case historical release catalogue.

The continuation follow-up compares the previous quadrature checkpoint
(`e6d000b`, remeasured) with completed source `0fc6ebc` on the same issue #33
quintic, supplied basis, points and 20-digit protocol described below.
Both revisions ran sequentially from isolated committed snapshots on the same
machine. The initial pre-PR timings remain included for context; these are
focused issue measurements, not a comprehensive release baseline.

| Operation (seconds) | Pre-PR main | Previous checkpoint | Completed branch |
| --- | ---: | ---: | ---: |
| Cold genus/cover setup | 41.02 | 42.17 | 1.65 |
| First-kind periods after genus | 155.51 | 12.75 | 10.87 |
| First Abel call after periods | 43.29 | 7.75 | 2.23 |
| Repeated Abel call | 43.42 | 6.84 | 1.37 |
| Nearby-point Abel call | 43.06 | 6.82 | 1.37 |

Repeated Abel calls improve about 5x over the previous checkpoint and 32x
over pre-PR main. Cold cover setup improves about 25x. Observed genus plus
period setup totals about 12.5 s, versus 54.9 s at the previous checkpoint
and 196.5 s before the PR.

The main change permits close groups of sheets to translate together without
forcing subdivision at the scale of their internal gaps. Prediction-error
and nearest-neighbour checks remain, the original absolute-motion acceptance
is retained, and the additional route constrains changes in every pairwise
sheet difference. Implicit-derivative coefficient setup is shared per fibre.
The ordinary integration policy recognizes newly coarse shared-motion lifts
and retains guarded node evaluation for them.

The representative open lift now has 46 intervals instead of 1,079;
continuation falls from about 5.7 s to 0.21 s. Open-path integration remains
about 1.16 s. Paths, base-point conventions and raw Abel representatives are
preserved: sampled Abel values agree with the previous checkpoint within
`2.1e-22`, and the 20-/30-digit comparisons remain within `2.5e-22`.

Riemann constants after warmed periods take 6.80 s at 20 digits and 10.32 s
at 30 digits. Shared normalization evaluates the original basis once per
node, reducing this stage from 13.93 s with the same relative-motion cover
(`65923f5`). Returned Riemann-constant vectors are bit-for-bit identical to
that version at both precisions. Riemann vanishing for the repeated effective
divisor `3*P` was checked on all five sheets: scaled residuals are below
`9e-20` at 20 digits and `1.6e-29` at 30 digits. At both precisions, Im(tau) remains positive-definite,
and base-point subtraction agrees.

Radial monodromy on the monic quintic takes 4.21 s; the original non-monic
presentation takes 3.27 s. Both return genus four, transitive actions and
identity products, with total ramification 16 and 14 respectively. These
new monodromy and Riemann timings have no freshly matched pre-PR baseline;
they should not be compared as controlled speed ratios to the issue's
historical figures.

A balanced Fermat-quartic control ran four process blocks per revision, each
with six warm batches of four Abel maps. Warm medians are 0.1492 s before
and 0.1505 s after (24 samples each); ranges are 0.1469–0.1547 s and
0.1483–0.1780 s. The small-case cost remains approximately 0.15 s.

Validation: 537 curve tests pass, repository-wide lint and whitespace checks
pass, and the HTML documentation builds with warnings treated as errors.
The genus-four marked-period regression runs at both 20 and 30 digits.

The original cold-cover, repeated-continuation and iterated-integration
follow-up areas have now been addressed and measured. Further changes to
custom-basis representation would be a separate feature, rather than work
required to finish issue #33.

