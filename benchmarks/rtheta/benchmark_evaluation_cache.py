"""Compare result-cache hits, moving arguments and shared BA-style sigma jets.

Run: python -m benchmarks.rtheta.benchmark_evaluation_cache
Only the evaluated-result cache is disabled for the comparison; period,
reduction and truncation caches remain warm in both measurements.
"""

import argparse
import importlib
import json
import platform
from statistics import median
import subprocess
from time import perf_counter

import generapy
from generapy import baker_akhiezer_jet, kleinian_sigma_jet, rtheta_jet
from mpmath import mp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=int, default=8)
    parser.add_argument('--repeats', type=int, default=3)
    args = parser.parse_args()
    ctx = mp.clone()
    ctx.dps = 30
    rt = importlib.import_module('generapy.riemann_theta')
    cache = rt._rtheta_evaluation_cache
    directional_cache = rt._rtheta_directional_evaluation_cache
    results = {}
    try:
        for genus in (2, 3):
            tau = ctx.eye(genus) * ctx.j
            omega = ctx.eye(genus)/2
            kappa = ctx.eye(genus)/10
            u = tuple(ctx.mpf(i+1)/10 for i in range(genus))

            def theta_workload(moving):
                output = []
                for sample in range(args.samples):
                    z = [v + (ctx.mpf(sample)/100 if moving else 0) for v in u]
                    output.extend(rtheta_jet(z, tau, 3, ctx=ctx).values())
                return tuple(output)

            def sigma_workload():
                output = []
                for sample in range(args.samples):
                    z = tuple(v + ctx.mpf(sample)/100 for v in u)
                    for mode in range(4):
                        shifted = tuple(v + ctx.mpf(mode+1)/20 for v in z)
                        for point in (z, shifted):
                            output.extend(kleinian_sigma_jet(
                                point, omega, tau, kappa, 3, ctx=ctx).values())
                return tuple(output)

            def ba_workload():
                output = []
                for sample in range(args.samples):
                    z = tuple(v + ctx.mpf(sample)/100 for v in u)
                    for mode in range(4):
                        output.extend(baker_akhiezer_jet(
                            z, shift=[ctx.mpf(mode+1)/20]*genus,
                            second_kind=[ctx.mpf('.1')]*genus,
                            omega=omega, tau=tau, kappa=kappa,
                            normalization='reference', reference=[ctx.mpf('.07')]*genus,
                            direction=[1]*genus, order=3, ctx=ctx))
                return tuple(output)

            for name, workload in (
                ('identical theta jets', lambda: theta_workload(False)),
                ('moving theta jets', lambda: theta_workload(True)),
                ('four shifts sharing sigma denominator', sigma_workload),
                ('reference BA jets, four shifts', ba_workload),
            ):
                # Populate point-independent setup before either timing.
                reference = workload()
                timings = {}
                for enabled in (False, True):
                    rt._rtheta_evaluation_cache = cache if enabled else rt._rtheta_evaluate
                    rt._rtheta_directional_evaluation_cache = (
                        directional_cache if enabled else rt._rtheta_directional_evaluate)
                    elapsed = []
                    for _ in range(args.repeats):
                        cache.cache_clear(ctx)
                        directional_cache.cache_clear(ctx)
                        start = perf_counter()
                        actual = workload()
                        elapsed.append(perf_counter()-start)
                        assert actual == reference
                    timings['cached' if enabled else 'uncached'] = median(elapsed)
                timings['speedup'] = timings['uncached']/timings['cached']
                results[f'g{genus}: {name}'] = timings
    finally:
        rt._rtheta_evaluation_cache = cache
        rt._rtheta_directional_evaluation_cache = directional_cache
    print(json.dumps({
        'version': generapy.__version__, 'python': platform.python_version(),
        'platform': platform.platform(), 'dps': ctx.dps,
        'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], text=True)),
        'experimental': True, 'samples': args.samples, 'repeats': args.repeats,
        'results': results,
    }, indent=2))


if __name__ == '__main__':
    main()
