# Benchmark Progress Log

This file tracks significant performance improvements and benchmark baseline updates for genera. Each entry documents changes that affected performance characteristics.

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
Their measured times mostly differ by single-digit percentages; one short
directional sample differed by 17%, so these runs do not establish a universal
speedup or a strict regression bound.

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

**Summary**: Established initial performance baseline for genera

**Algebraic curve periods (curves_vs_sage.md):**
- **Hyperelliptic curves**: genera is 5-10x faster than Sage across all genera (1-4) and precision levels (30-50 digits)
  - Genus 1, 30 digits: 0.018s vs 0.168s (9.4x faster)
  - Genus 2, 30 digits: 0.066s vs 0.508s (7.7x faster)
  - Genus 3, 30 digits: 0.162s vs 1.186s (7.3x faster)
  - Genus 3, 50 digits: 0.364s vs 1.640s (4.5x faster)
  - Genus 3 generic case (expensive): 0.183s vs 15.6s (85x faster!)

- **General curves**: Performance competitive with Sage
  - Trigonal genus-3: genera 2.5s vs Sage 2.6s (comparable)
  - Klein quartic: genera slower (1.9s vs 0.9s) - possible optimization target
  - Kovalevskaya: genera much slower (11.3s vs 3.4s) - uses user-supplied basis

**Accuracy**: All test cases passed accuracy validation at both 30 and 50 digit precision

**Hyperelliptic periods isolated benchmark (hyperelliptic_vs_sage.md):**
- Genus 1, 30 digits: 10ms (genera) vs 110ms (Sage) - 11x faster
- Genus 2, 30 digits: 63ms (genera) vs 539ms (Sage) - 8.5x faster
- vs abelfunctions (fixed 15-digit precision): genera 18-55x faster

**Riemann theta vs jtheta (rtheta_vs_jtheta.md):**
- Warmed steady-state: genera competitive with jtheta (0.67-1.24x ratio at 50 dps)
- Cold start: genera slower (5-18x slower) due to Python overhead vs C implementation
- Accuracy: Maximum scaled error < 1e-98 at 100 digits
- Note: jtheta is a specialized genus-1 C library; genera is pure Python and handles arbitrary genus

**Riemann theta vs Wolfram Engine (rtheta_vs_wolfram.md):**
- Overall geometric mean: genera 0.40x (2.5x faster than Wolfram)
- Unreduced cases: genera 0.03-0.16x (up to 33x faster!) - Wolfram struggles with unreduced tau
- Regular cases: genera competitive to slightly slower (0.55-1.23x)
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

Optimized the derivative radius selection algorithm in src/genera/curves/_radius.py.
The new approach reduces the number of terms in the theta series expansion by ~40%
for high-genus cases, with minimal impact on low-genus performance.

Specific improvements:
- Genus 3, 50 digits: 8.2s → 3.9s (2.1x)
- Genus 2, 50 digits: 2.1s → 2.0s (1.05x)
- Genus 1: No change (different code path)

-->
