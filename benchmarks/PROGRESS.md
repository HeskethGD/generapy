# Benchmark Progress Log

This file tracks significant performance improvements and benchmark baseline updates for generapy. Each entry documents changes that affected performance characteristics.

## Purpose

- Record performance milestones at release boundaries
- Document optimization efforts and their impact
- Provide context for comparing baselines across versions
- Track regressions or unexpected slowdowns

## Format

Each entry should include:
- **Version/Date**: Release version or date of change
- **Benchmark(s)**: Which benchmark(s) were affected
- **Baseline**: Reference to committed baseline file(s)
- **Summary**: What changed and the measured impact
- **Details**: Implementation changes, optimization techniques, or relevant context

## Entries

<!-- Entries will be added as releases occur and optimizations are made -->

### v0.3.0 release-candidate baselines (2026-11-22)

**Reports:** [protocol and summary](baselines/v0.3.0/README.md),
[numerical functions](baselines/v0.3.0/theta_and_ba.md),
[curve periods](baselines/v0.3.0/curve_periods.md), and
[genus-four pipeline](baselines/v0.3.0/general_curve_pipeline.md).

The complete matched suite compared published v0.2.0 (`cd98830`) with
`a688d64`, using seven numerical samples and three fresh-process curve trials
per revision. All 268 configurations passed, including both expected singular
rejections. Geometric-mean candidate/reference ratios were 0.992 for genus
one, 0.976 for theta, 0.991 for jets, 0.985 for BA and 0.996 for curve periods.
All 26 catalogue curves ran at 30/50 digits; no external tools were launched.

The largest initial increase, theta g2-coupled/half at 30 digits (1.107), was
rechecked with 31 samples and reversed order: 1.008. Initial results remain
in the reports. The unchanged evaluator groups show timing variation; their
apparent improvements are not attributed to this release's code changes.
The separate genus-four profile retains its actual development revisions,
which have the same numerical implementation as this release candidate.

### Unreleased: completed general-curve performance pass (#33, 2026-11-22)

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

### Unreleased: measured genus-four pipeline improvements (#33, 2026-11-22)

Compared committed snapshots of pre-PR main (`b8c8f02`), connector caching
(`79c4add`) and the final integration policy (`e6d000b`) on the actual
[issue #33 spectral quintic](https://github.com/HeskethGD/generapy/issues/33).
The rational polynomial is coordinate-swapped to be monic in y, with the four
supplied first-kind forms from the issue. No polynomial workaround is used.

Each revision ran in an isolated process on the same macOS ARM64 machine,
Python 3.14.7 and mpmath 1.4.1, at 20 decimal digits. Source snapshots were
unchanged while timing; no other benchmark instances ran concurrently.
One cold genus setup was followed by periods, an Abel map to
`fibre(3.3+1.7j)[0]`, the identical request, and a nearby target
`fibre(3.31+1.71j)[0]`. Abel reduction was disabled. These are focused single-run
issue measurements, not a comprehensive release baseline.

| Operation (seconds) | Pre-PR main | Connector cache | Final policy |
| --- | ---: | ---: | ---: |
| Cold genus/cover setup | 41.02 | 42.42 | 41.62 |
| First-kind periods after genus | 155.51 | 154.78 | 12.59 |
| First Abel call after periods | 43.29 | 43.22 | 7.73 |
| Repeated Abel call | 43.42 | 21.34 | 6.76 |
| Nearby-point Abel call | 43.06 | 21.38 | 6.80 |

The final policy reduces period integration after setup by about 12.4x and
repeated Abel evaluation by about 6.4x. Including cold genus setup, obtaining
periods falls from about 197 s to 54 s. Connector reuse removes roughly 22 s
per repeated call. The remaining open lift has 1,079 continuation intervals;
quadrature now uses panels on its straight spans, retaining those fine
samples for branch labels. Guarded node evaluation meets caller-precision
convergence checks. Short spans keep their existing integration route.

Final Abel values differ from pre-PR main by less than `2.1e-22`. A 30-digit
reference at `2d143b9` (the guarded panel integrator before short-path
selection) differs from the final 20-digit Abel values by at most `2.5e-22`.
Scaled matrix differences, using norm(error)/max(1,norm(reference)), are below
`5e-21` for the two half-period matrices and `2.3e-20` for tau. The imaginary
part of tau is positive-definite at both precisions. Base-point subtraction
has residual below `2e-22` at 20 digits and `2.2e-32` in the reference run.

A matched Fermat-quartic control compared `79c4add` with `e6d000b`: four
process blocks per revision in alternating order, each with one initial batch
and six warm batches of four Abel maps. Pooled warm medians are 0.1487 s and
0.1491 s. All 24 warm samples per revision are retained; ranges were
0.1475–0.1778 s and 0.1481–0.2508 s, respectively. The large short-path
penalty seen during development is avoided; this control shows no material
median change, with some timing variability.

Validation includes 528 passing curve tests and a warnings-as-errors HTML
build, with regressions for mesh-density independence, winding and sheet
labels, stored-lift precision, and nearby-pole rejection.

Remaining work is separate: cold cover construction still takes about 42 s,
and full-fibre open continuation accounts for about 5.7 s of each 6.8 s warm
Abel call. Riemann-constant iterated integration and radial monodromy were
not remeasured or optimized by this integration change. Further reductions
there should be profiled and tracked as specific follow-ups.

### Unreleased: geometric Abel connector reuse (#33, 2026-11-21)

Exploratory measurements on the Fermat quartic at 20 decimal digits compared
three batches of four first-kind Abel maps, one point per sheet at
`x = 1.2 + 0.3j`. Period setup was warmed before timing. The initial batch
warmed connector integrals; the next two batches measured repeated calls.
No source edits or other benchmark instances ran during either measurement.
These were development working-tree experiments, not a release baseline.

Warm batches fell from a median 0.313 s to 0.153 s, about 2.0x faster.
Connector integrations fell from 15 per warm batch to zero; all four open
paths were still integrated. Initial batches took 0.344 s before and 0.330 s
after. All returned value strings matched before and after at 20 digits.

The bounded cache stores immutable edge-integral vectors, separated by curve,
first- and second-kind bases, context and numerical state. Unhashable bases
retain operation-local reuse. This addresses repeated connector integration
only: the reported genus-four case, full-fibre open continuation, periods and
Riemann constants still need separate profiling. Issue #33 remains partial.

### v0.2.0 pre-release: shared integration work for #9/#10 (2026-11-16)

**Report:** [complete integration results and protocol](baselines/v0.2.0/integration.md).

Compared main after PR #24 (`c02262c`) with `ac5ae8d`, including chart
optimization `483535a` and Abel optimization `66e51fe`. The jet changes did
not address these integration costs. Profiling showed repeated coordinate
validation across chart forms and repeated continued square-root products
across Abel components.

Chart conversion and ambient residual/scale terms are now shared per node.
Hyperelliptic branch factors are shared at common quadrature nodes within a
single path evaluation, with precision included in reuse. Componentwise
adaptive quadrature, marked paths and branch checks are retained.

At 40 digits, chart integration fell from 0.155 s to 0.119 s, real finite-base
Abel integration from 0.0203 s to 0.0108 s and complex finite-base Abel
integration from 0.0842 s to 0.0469 s. Across 20/40/80 digits, the chart
fixture improves about 23–24%, complex Abel about 44%, and genus-three Abel
controls about 2.6–2.8x. Genus-one controls also improve slightly. Remaining
chart correction/validation and two marked Abel paths still cost more than
specialized direct quadrature; these are partial performance improvements.

All 33 local-integral and 21 chart-control combinations passed on both
sources; errors and chart segment/refinement counts match before/after.
196 focused tests passed and changed numerical lines have complete diff
coverage. Final timings used committed candidate sources and a clean tracked
tree; raw samples remain untracked. This is a later pre-release checkpoint,
not a replacement for the earlier theta/BA measurements below.

### v0.2.0 pre-release: matched Generapy regression checks (2026-11-16)

**Reports:** [overview and protocol](baselines/v0.2.0/README.md),
[theta, mixed jets and BA](baselines/v0.2.0/theta_and_ba.md),
[curve periods](baselines/v0.2.0/curve_periods.md).

Compared previous main `6134a3d` with candidate `4f6475f` in isolated archived
source trees using the same Python 3.14.7 and mpmath 1.4.1. No external
mathematical tools were run. Historical genus-one, higher-genus theta and
all 26 curve cases were reused, plus mixed-jet and BA controls. All 268
workload/precision combinations passed output checks, including both expected
singular-curve rejections. Valid curve trials also passed curve validation.

Geometric-mean candidate/previous time ratios were 1.004 for genus-one,
0.995 for scalar theta, 0.901 for mixed theta/sigma jets, 0.580 for BA and
1.000 for valid curve cases. Ratios below one mean faster evaluation. An
initial 15.6% increase in one short genus-one derivative workload became 1.2%
with 31 samples and reversed order. No repeatable large slowdown was found
in the tested workloads; the complete tables retain all initial measurements.

Compared with saved v0.1.0 times, cold genus-one measurements are about 4.8%
higher overall; previous main was already about 4.1% higher. Historical theta
reports used a different Python version, and the curve report omits interpreter
metadata, so those cross-date differences cannot be assigned to this PR.
The reports distinguish saved-number comparisons from the matched regression
control. This directory records a release candidate, not a published release.

### Development: directional jets and derivative-aware reduction (2026-11-16)

**Benchmark:** `python -m benchmarks.rtheta.benchmark_directional_jets`

**Status:** Experimental local measurements from development working trees,
not a release baseline. Runs used
Python 3.14.7, mpmath 1.4.1 and macOS 27.0.1 on arm64, at 24 and 40 decimal
digits. Reported timings are medians of two measured calls after a warm-up.
Evaluated-result caches were cleared before every timed call; period and
truncation setup stayed warm. All returned derivatives were checked alongside
timing. Raw JSON remains untracked.

Direct directional theta/sigma jets accumulate orders zero through three
without constructing all mixed partials. BA uses this path internally, with
the same public interface. The paired full-jet comparison contracts the mixed
jet to the same direction; BA compares four reference-normalized shifts,
retaining shared-denominator reuse within each sample in both implementations.

The following speedup ranges cover both coordinate and dense directions at
both precisions, using automatic path selection in each implementation:

| Fixture | Sigma: full / directional | BA: full / directional |
| --- | ---: | ---: |
| Genus 2 coupled | 1.46–1.64× | 1.35–1.43× |
| Genus 3 coupled | 1.99–2.33× | 1.78–1.97× |
| Issue #17 | 1.50–2.11× | 1.36–1.69× |
| Genus 4 coupled | 3.01–3.70× | 2.42–2.92× |
| Genus 5 coupled | 3.19–3.99× | 2.61–3.12× |

These are supplied period-data workloads, including synthetic genus-four/five
controls, rather than end-to-end curve computations. The issue #17 fixture is
copied from its standalone reproducer. Sigma and BA use explicit compatible
periods with `omega = I/2` and `kappa = I/10`.

Reduction selection now estimates derivative lattice radii, argument shifts,
transformed output work and composition cost. On #17, the order-three full
jet switches to reduction: approximately 0.134–0.136 s becomes 0.090–0.094 s
at 24 digits, and 0.233–0.237 s becomes 0.135–0.136 s at 40 digits. The
coordinate directional jet also selects reduction; the dense direction stays
direct because reduction makes its direction complex and costs more. The
coupled and strongly unreduced controls retain their existing path choices.
The full-versus-directional table above compares two evaluation methods in
this implementation, rather than two releases. The selector before/after
comparison used development trees with directional jets already implemented.
Some control timings increased: the genus-three unreduced dense directional
jet at 24 digits went from 19.14 ms to 22.40 ms (17% slower), and the #17 dense
directional jet went from 55.66 ms to 59.39 ms (6.7% slower) at 24 digits and
87.38 ms to 91.52 ms (4.7% slower) at 40 digits. Other control differences were
mostly single-digit percentages in either direction. With only two repeats,
these are observed slowdowns requiring more sampling, not established
regressions. The later v0.2.0 matched comparison above reuses the Generapy side
of the historical workloads with more samples. Those reports supersede this
early run for regression assessment; the external tools were not rerun.

Reproduce the bounded comparisons from the repository root:

```sh
python -m benchmarks.rtheta.benchmark_directional_jets --dps 24 40 \
  --cases issue17 g2-coupled g3-coupled g2-unreduced g3-unreduced \
  --workloads theta --repeats 2 --output /tmp/directional-theta.json
python -m benchmarks.rtheta.benchmark_directional_jets --dps 24 40 \
  --cases g2-coupled g3-coupled issue17 g4-coupled g5-coupled \
  --workloads sigma ba --repeats 2 --output /tmp/directional-sigma-ba.json
```

The theta comparison includes forced direct/reduced evaluations as well as
automatic selection. Regression tests compare all twenty #17 mixed partials
at both precisions, including a shifted argument, and compare directional
jets against full contractions, reduced paths and genus-one `jtheta` values.
No tail criterion was relaxed to obtain the timing changes.

### v0.1.0: Initial baseline (2026-10-01)

**Baselines:**
- `baselines/v0.1.0/curves_vs_sage.md` - Algebraic curve period computation
- `baselines/v0.1.0/hyperelliptic_vs_sage.md` - Hyperelliptic periods (isolated)
- `baselines/v0.1.0/rtheta_vs_jtheta.md` - Riemann theta vs jtheta
- `baselines/v0.1.0/rtheta_vs_wolfram.md` - Riemann theta vs Wolfram Engine

**Summary**: Established initial performance baseline for generapy

**Algebraic curve periods (curves_vs_sage.md):**
- **Hyperelliptic curves**: generapy is 5-10x faster than Sage across all genera (1-4) and precision levels (30-50 digits)
  - Genus 1, 30 digits: 0.018s vs 0.168s (9.4x faster)
  - Genus 2, 30 digits: 0.066s vs 0.508s (7.7x faster)
  - Genus 3, 30 digits: 0.162s vs 1.186s (7.3x faster)
  - Genus 3, 50 digits: 0.364s vs 1.640s (4.5x faster)
  - Genus 3 generic case (expensive): 0.183s vs 15.6s (85x faster!)

- **General curves**: Performance competitive with Sage
  - Trigonal genus-3: generapy 2.5s vs Sage 2.6s (comparable)
  - Klein quartic: generapy slower (1.9s vs 0.9s) - possible optimization target
  - Kovalevskaya: generapy much slower (11.3s vs 3.4s) - uses user-supplied basis

**Accuracy**: All test cases passed accuracy validation at both 30 and 50 digit precision

**Hyperelliptic periods isolated benchmark (hyperelliptic_vs_sage.md):**
- Genus 1, 30 digits: 10ms (generapy) vs 110ms (Sage) - 11x faster
- Genus 2, 30 digits: 63ms (generapy) vs 539ms (Sage) - 8.5x faster
- vs abelfunctions (fixed 15-digit precision): generapy 18-55x faster

**Riemann theta vs jtheta (rtheta_vs_jtheta.md):**
- Geometric-mean `rtheta / jtheta` time ratios: 1.32x warm and 8.59x cold at 50 dps; 1.23x warm and 7.66x cold at 100 dps. Ratios above one mean `rtheta` was slower.
- Accuracy: Maximum scaled error was 1.4922e-98 at 100 digits.
- `jtheta` is mpmath's specialized genus-one implementation, written in Python. Generapy's Riemann theta evaluator supports arbitrary genus. The timing report does not establish the cause of the cold-start difference.

**Riemann theta vs Wolfram Engine (rtheta_vs_wolfram.md):**
- Overall geometric mean: generapy 0.40x (2.5x faster than Wolfram)
- Unreduced cases: generapy 0.03-0.16x (up to 33x faster!) - Wolfram struggles with unreduced tau
- Regular cases: generapy competitive to slightly slower (0.55-1.23x)
- Genus 1, 50 digits: 0.26ms vs 0.40ms (1.5x faster)
- Genus 3 unreduced, 100 digits: 29ms vs 1028ms (35x faster!)
- Accuracy: Maximum scaled error < 6.3e-50 at 50 digits, < 2.7e-100 at 100 digits

**Infrastructure established:**
- 26+ algebraic curve test cases covering hyperelliptic and general curves
- Automated basis alignment and symplectic validation
- Isolated worker processes for fair comparison
- Riemann theta benchmarks with multiple reference implementations

The benchmark suite includes:
- **Curve benchmarks**: Comparison with SageMath for algebraic curve period computation
  - 26+ test cases covering hyperelliptic and general curves
  - Validation of differential basis, period matrices, and accuracy
- **Riemann theta benchmarks**: Comparisons with multiple reference implementations
  - Wolfram Engine (SiegelTheta)
  - jtheta implementation
  - FLINT acb_theta
  - SageMath hyperelliptic periods
  - PARI hyperelliptic periods
  - Internal implementation variants

Results tracking:
- Development runs: Git-ignored `results/TIMESTAMP/` directories
- Release baselines: Committed markdown reports in `baselines/vX.Y.Z/`
- This progress log: Manually curated performance narrative

**Next steps**: Establish v0.1.0 baseline after first release.

---

<!-- Future entries go here. Template:

### vX.Y.Z: Title of change (YYYY-MM-DD)

**Benchmark**: benchmark_name.py
**Baseline**: baselines/vX.Y.Z/benchmark_name.md
**Improvement**: 2.1x speedup for genus-3 cases at 50 digits
**Details**:

Optimized the derivative radius selection algorithm in src/generapy/curves/_radius.py.
The new approach reduces the number of terms in the theta series expansion by ~40%
for high-genus cases, with minimal impact on low-genus performance.

Specific improvements:
- Genus 3, 50 digits: 8.2s → 3.9s (2.1x)
- Genus 2, 50 digits: 2.1s → 2.0s (1.05x)
- Genus 1: No change (different code path)

-->
