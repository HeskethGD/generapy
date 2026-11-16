"""Compare directional jets, full contractions and direct/reduced theta paths.

Run: python -m benchmarks.rtheta.benchmark_directional_jets
Result caches are cleared before each timed call; numerical setup stays warm.
Use --output for an experimental JSON report, not an official release baseline.
"""

import argparse
import importlib
import json
import math
import platform
from pathlib import Path
from statistics import median
import subprocess
from time import perf_counter

from mpmath import mp
import generapy
from generapy import (
    baker_akhiezer_jet, kleinian_sigma_directional_jet, kleinian_sigma_jet,
    rtheta_directional_jet, rtheta_jet,
)
from .directional_cases import cases

rt = importlib.import_module('generapy.riemann_theta')
kl = importlib.import_module('generapy.kleinian')


def contract(ctx, jet, direction, order):
    return tuple(ctx.fsum(
        math.factorial(n)//math.prod(math.factorial(k) for k in index)
        * ctx.fprod(d**k for d, k in zip(direction, index))*v
        for index, v in jet.items() if sum(index) == n) for n in range(order+1))


def clear_results(ctx):
    rt._rtheta_evaluation_cache.cache_clear(ctx)
    rt._rtheta_directional_evaluation_cache.cache_clear(ctx)


def theta_path(ctx, z, tau, char, direction, order, method, directional):
    if method == 'auto':
        return (rtheta_directional_jet(z, tau, direction, order, char, ctx=ctx) if directional else
                contract(ctx, rtheta_jet(z, tau, order, char, ctx=ctx), direction, order))
    z, key, a, b = rt._normalise_rtheta_inputs(ctx, z, tau, char)
    magnitude = max([ctx.mag(v) for v in z+a+b] + [0])
    norm = ctx.sqrt(ctx.fsum(abs(d)**2 for d in direction))
    guard = order*max(0, ctx.mag(norm)) if directional and norm > 1 else 0
    with ctx.extraprec(10*(order+1)+2*max(0, magnitude)+guard):
        derivatives = tuple(rt._multiindices(len(z), order))
        if method == 'reduced':
            reduced, ops, _ = rt._rtheta_reduction_data(ctx, key)
            if directional:
                result = rt._rtheta_directional_reduced(ctx, z, key, a, b, direction, order, ops, reduced)
            else:
                values = rt._rtheta_reduced_derivatives(ctx, z, key, a, b, derivatives, ops, reduced)
                result = contract(ctx, dict(zip(derivatives, values)), direction, order)
        elif directional:
            result = rt._rtheta_directional_sum(ctx, z, key, a, b, direction, order)
        else:
            values = rt._rtheta_sum(ctx, z, key, a, b, derivatives)
            result = contract(ctx, dict(zip(derivatives, values)), direction, order)
    return tuple(+v for v in result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dps', nargs='+', type=int, default=[24, 40])
    parser.add_argument('--cases', nargs='+', default=['g2-coupled', 'g3-coupled', 'g2-unreduced', 'issue17', 'g4-coupled', 'g5-coupled'])
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--workloads', nargs='+', choices=['theta', 'sigma', 'ba'], default=['theta', 'sigma', 'ba'])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rows = []
    source_before = subprocess.check_output(['git', 'diff', 'HEAD'], text=True)
    for dps in args.dps:
        ctx = mp.clone()
        ctx.dps = dps
        for name, tau, z, char in cases(ctx):
            if name not in args.cases:
                continue
            genus = len(z)
            omega, kappa = ctx.eye(genus)/2, ctx.eye(genus)/10
            for label, direction in (('coordinate', [0]*(genus-1)+[1]),
                                     ('dense', [ctx.mpf(1)/(i+1) for i in range(genus)])):
                for workload in args.workloads:
                    reference = None
                    methods = ('full-direct', 'full-reduced', 'full-auto', 'directional-direct', 'directional-reduced', 'directional-auto') if workload == 'theta' else ('full', 'directional')
                    for method in methods:
                        def run():
                            if workload == 'theta':
                                family, path = method.split('-')
                                return theta_path(ctx, z, tau, char, direction, 3, path, family == 'directional')
                            if workload == 'sigma':
                                if method == 'full':
                                    return contract(ctx, kleinian_sigma_jet(z, omega, tau, kappa, 3, char, ctx=ctx), direction, 3)
                                return kleinian_sigma_directional_jet(z, omega, tau, kappa, 3, char, direction=direction, ctx=ctx)
                            original = kl._sigma_directional_jet
                            if method == 'full':
                                def old(ctx, u, direction, order, omega, tau, kappa, characteristic, normalization):
                                    return contract(ctx, kleinian_sigma_jet(u, omega, tau, kappa, order, characteristic,
                                                                           normalization, ctx=ctx), direction, order)
                                kl._sigma_directional_jet = old
                            try:
                                return tuple(v for mode in range(4) for v in baker_akhiezer_jet(
                                    z, shift=[ctx.mpf(mode+1)/7]*genus, second_kind=[ctx.mpf('.1')]*genus,
                                    omega=omega, tau=tau, kappa=kappa, characteristic=char,
                                    normalization='reference', reference=[v/2+ctx.mpf('.07') for v in z],
                                    direction=direction, order=3, ctx=ctx))
                            finally:
                                kl._sigma_directional_jet = original
                        run()
                        times = []
                        for _ in range(args.repeats):
                            clear_results(ctx)
                            start = perf_counter()
                            result = run()
                            times.append(perf_counter()-start)
                        if reference is None:
                            reference = result
                        error = max(abs(a-b)/max(1, abs(b)) for a, b in zip(result, reference))
                        assert error < ctx.mpf(10)**(7-dps), (name, method, error)
                        row = dict(case=name, dps=dps, direction=label, workload=workload,
                                   method=method, seconds=median(times), scaled_error=str(error))
                        rows.append(row)
                    print(f'{name} {dps} digits {label} {workload}: passed', flush=True)
    assert source_before == subprocess.check_output(['git', 'diff', 'HEAD'], text=True), 'source changed during benchmark'
    report = dict(python=platform.python_version(), platform=platform.platform(), generapy=generapy.__version__,
                  commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                  dirty=bool(subprocess.check_output(['git', 'status', '--porcelain'], text=True)),
                  experimental=True, rows=rows)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2))
    else:
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
