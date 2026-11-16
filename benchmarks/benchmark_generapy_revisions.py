"""Compare two committed Generapy revisions without running external tools.

Reuses historical genus-one, Wolfram and curve-period inputs, plus mixed-jet
and BA workloads. Run from the repo root with --output in an ignored directory.
The revisions are archived to temporary directories; checkout state is untouched.
"""

import argparse
from contextlib import ExitStack
import fnmatch
import hashlib
import importlib
import io
import json
import math
import os
from pathlib import Path
import platform
import select
from statistics import median
import subprocess
import sys
import tarfile
import tempfile
from time import perf_counter


REPO = Path(__file__).resolve().parents[1]


def jobs(groups, theta_dps=(50, 100)):
    """Reuse exact inputs; historical timing columns are context, not controls."""
    result = []

    def add(group, case, dps, **data):
        result.append(dict(group=group, case=case, dps=dps, **data))

    if 'genus-one' in groups:
        from benchmarks.rtheta.benchmark_rtheta_vs_jtheta import TAU_CASES, WORKLOADS, W_VALUES
        for dps in (50, 100):
            for name, re, im, _ in TAU_CASES:
                for label, _, degree, char, _ in WORKLOADS:
                    for mode in ('warm', 'cold'):
                        add('genus-one', f'{name}/{label}/{mode}', dps,
                            tau=[[(re, im)]], points=[[(r, i)] for r, i in W_VALUES],
                            char=[[(char[0], '0')], [(char[1], '0')]],
                            derivative=[degree], angular=True, cold=mode == 'cold')
    if 'theta' in groups:
        from benchmarks.rtheta import benchmark_rtheta_vs_wolfram as fixtures
        for dps in theta_dps:
            for case in fixtures.CASES:
                for label in fixtures.workloads(case):
                    if 'dz' in label and dps > case.get('derivative_max_dps', dps):
                        continue
                    char, derivative = fixtures.workload_data(label, case['genus'])
                    add('theta', f'{case["name"]}/{label}', dps, tau=case['tau'], char=char,
                        derivative=derivative,
                        points=[p[:case['genus']] for p in fixtures.workload_points(case, label)])
    if {'jets', 'ba'} & set(groups):
        from mpmath import mp
        from benchmarks.rtheta.directional_cases import cases
        for dps in (24, 40):
            ctx = mp.clone()
            ctx.dps = dps
            for name, tau, z, char in cases(ctx):
                if name not in ('g2-coupled', 'g3-coupled', 'g2-unreduced', 'g3-unreduced', 'issue17'):
                    continue
                def encode(v):
                    return [str(ctx.re(v)), str(ctx.im(v))]
                data = dict(tau=[[encode(v) for v in row] for row in tau],
                            points=[[encode(v) for v in z]],
                            char=[[encode(v) for v in row] for row in char])
                if 'jets' in groups:
                    for order in (2, 3):
                        add('jets', f'{name}/theta{order}', dps, order=order, **data)
                    add('jets', f'{name}/sigma3', dps, order=3, sigma=True, **data)
                if 'ba' in groups:
                    for dense in (False, True):
                        add('ba', f'{name}/{"dense" if dense else "coordinate"}', dps,
                            dense=dense, order=3, **data)
    if 'curves' in groups:
        from benchmarks.curves.curve_cases import catalog
        # The complete historical table, including its expected rejection.
        text = (REPO/'benchmarks/baselines/v0.1.0/curves_vs_sage.md').read_text()
        catalog = catalog()
        for line in text.splitlines():
            cells = [v.strip() for v in line.split('|')]
            if len(cells) == 8 and cells[3] in ('genera', 'generapy', 'hyperelliptic'):
                name, dps = cells[1], int(cells[2])
                add('curves', name, dps, curve=catalog[name],
                    historical_seconds=None if cells[5] == '—' else float(cells[5]))
    return result


def worker(snapshot):
    """Persistent numerical worker; each request has an independent context."""
    sys.path.insert(0, str(Path(snapshot)/'src'))
    import generapy as gp
    from mpmath import mp
    rt = importlib.import_module('generapy.riemann_theta')
    assert Path(gp.__file__).resolve().is_relative_to(Path(snapshot).resolve())

    def clear(ctx, cold=False):
        for name, value in vars(rt).items():
            if hasattr(value, 'cache_clear') and (cold or 'evaluation_cache' in name):
                value.cache_clear(ctx)

    for line in sys.stdin:
        request = json.loads(line)
        ctx = mp.clone()
        ctx.dps = request['dps']
        z = [ctx.mpc(*v) for v in request['points'][0]]
        points = [[ctx.mpc(*v) for v in row] for row in request['points']]
        if request.get('angular'):
            points = [[v/ctx.pi for v in row] for row in points]
        tau = [[ctx.mpc(*v) for v in row] for row in request['tau']]
        char = request['char']
        if char is not None:
            char = [[ctx.mpc(*v) for v in row] for row in char]
        genus = len(z)
        omega, kappa = ctx.eye(genus)/2, ctx.eye(genus)/10

        def evaluate():
            if request['group'] == 'ba':
                direction = ([ctx.one/(i+1) for i in range(genus)] if request['dense'] else
                             [0]*(genus-1)+[1])
                return tuple(v for mode in range(4) for v in gp.baker_akhiezer_jet(
                    z, shift=[ctx.mpf(mode+1)/7]*genus, second_kind=[ctx.mpf('.1')]*genus,
                    omega=omega, tau=tau, kappa=kappa, characteristic=char,
                    normalization='reference', reference=[v/2+ctx.mpf('.07') for v in z],
                    direction=direction, order=3, ctx=ctx))
            if request.get('sigma'):
                return tuple(gp.kleinian_sigma_jet(z, omega, tau, kappa, 3, char, ctx=ctx).values())
            if 'order' in request:
                return tuple(gp.rtheta_jet(z, tau, request['order'], char, ctx=ctx).values())
            result = []
            for point in points:
                if request.get('cold'):
                    clear(ctx, cold=True)
                result.append(gp.rtheta(point, tau, char, derivative=tuple(request['derivative']), ctx=ctx))
            return tuple(result)

        evaluate()  # Numerical setup, excluded from timing.
        times = []
        for _ in range(request['repeats']):
            clear(ctx)
            start = perf_counter()
            actual = evaluate()
            times.append(perf_counter()-start)
        assert all(ctx.isfinite(v) for v in actual)
        output = dict(times=times, values=[[str(ctx.re(v)), str(ctx.im(v))] for v in actual],
                      mpmath=importlib.import_module('mpmath').__version__,
                      import_path=gp.__file__)
        print(json.dumps(output), flush=True)


def archive(revision, target):
    commit = subprocess.check_output(['git', 'rev-parse', revision+'^{commit}'], cwd=REPO, text=True).strip()
    data = subprocess.check_output(['git', 'archive', commit, 'src'], cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(data)) as source:
        source.extractall(target, filter='data')
    return commit


def start_worker(snapshot, stack):
    env = dict(os.environ)
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    process = subprocess.Popen([sys.executable, '-I', str(Path(__file__).resolve()), '--worker', str(snapshot)],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                               cwd=snapshot, env=env, start_new_session=True)
    def cleanup():
        process.stdin.close()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    stack.callback(cleanup)
    return process


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--before', default='main')
    parser.add_argument('--after', default='HEAD')
    parser.add_argument('--groups', nargs='+', choices=['genus-one', 'theta', 'jets', 'ba', 'curves'],
                        default=['genus-one', 'theta', 'jets', 'ba', 'curves'])
    parser.add_argument('--repeats', type=int, default=7)
    parser.add_argument('--theta-dps', type=int, nargs='+', default=[50, 100],
                        help='Higher-genus scalar-theta precisions; historical reports use 50 and 100')
    parser.add_argument('--curve-repeats', type=int, default=3)
    parser.add_argument('--reverse-order', action='store_true', help='Reverse the alternating revision order')
    parser.add_argument('--filter', default='*', help='Glob matched against group/case/dps')
    parser.add_argument('--timeout', type=float, default=180)
    parser.add_argument('--output', type=Path, required=True, help='New ignored JSON report path')
    args = parser.parse_args()
    if args.output.exists() or args.repeats < 1 or args.curve_repeats < 1:
        parser.error('use a new output path and positive repeat counts')
    selected = [j for j in jobs(args.groups, args.theta_dps) if fnmatch.fnmatch(f'{j["group"]}/{j["case"]}/{j["dps"]}', args.filter)]
    if not selected:
        parser.error('no matching jobs')
    source_before = subprocess.check_output(['git', 'diff', 'HEAD'], cwd=REPO)
    def harness_hash():
        digest = hashlib.sha256()
        for path in sorted((REPO/'benchmarks').rglob('*.py')):
            digest.update(str(path.relative_to(REPO)).encode())
            digest.update(path.read_bytes())
        return digest.hexdigest()
    source_hash = harness_hash()
    report = dict(experimental=True, python=platform.python_version(), platform=platform.platform(),
                  repeats=args.repeats, curve_repeats=args.curve_repeats,
                  reverse_order=args.reverse_order, harness_sha256=source_hash, rows=[])
    with tempfile.TemporaryDirectory(prefix='generapy-revisions-') as temporary, ExitStack() as stack:
        snapshots = {name: Path(temporary)/name for name in ('before', 'after')}
        report['commits'] = {name: archive(getattr(args, name), path) for name, path in snapshots.items()}
        workers = {name: start_worker(path, stack) for name, path in snapshots.items()}
        from mpmath import mp
        for index, job in enumerate(selected):
            order = ('before', 'after') if (index+args.reverse_order) % 2 == 0 else ('after', 'before')
            samples = {}
            if job['group'] == 'curves':
                for repeat in range(args.curve_repeats):
                    for name in (order if repeat % 2 == 0 else order[::-1]):
                        request = dict(case=job['curve'], engine='generapy', repo=str(snapshots[name]),
                                       bits=math.ceil((job['dps']+15)*math.log2(10)))
                        completed = subprocess.run([sys.executable, '-I', str(REPO/'benchmarks/curves/period_worker.py')],
                                                   input=json.dumps(request), capture_output=True, text=True,
                                                   cwd=temporary, timeout=args.timeout, check=True)
                        row = json.loads(completed.stdout)
                        expected = job['curve']['expected_rejection']
                        assert (row['status'] == 'error') if expected else (row['status'] == 'ok' and row['validation']), row
                        if expected:
                            assert row['error_type'] == 'ValueError', row
                        sample = samples.setdefault(name, dict(times=[], values=row.get('periods', []),
                                                                status=row['status'], error=row.get('error')))
                        if not expected:
                            sample['times'].append(row['seconds'])
            else:
                for name in order:
                    process = workers[name]
                    process.stdin.write(json.dumps(dict(job, repeats=args.repeats))+'\n')
                    process.stdin.flush()
                    if not select.select([process.stdout], [], [], args.timeout)[0]:
                        raise TimeoutError(f'{name}: {job}')
                    samples[name] = json.loads(process.stdout.readline())
            ctx = mp.clone()
            ctx.dps = job['dps']+30
            def flattened(data):
                if job['group'] == 'curves':
                    return [ctx.mpc(*v) for row in data for v in row]
                return [ctx.mpc(*v) for v in data]
            before, after = [flattened(samples[n]['values']) for n in ('before', 'after')]
            assert len(before) == len(after)
            error = max((abs(a-b)/max(1, abs(a)) for a, b in zip(before, after)), default=ctx.zero)
            assert error < ctx.mpf(10)**(5-job['dps']), (job, error)
            timings = {n: median(s['times']) if s['times'] else None for n, s in samples.items()}
            ratio = timings['after']/timings['before'] if timings['before'] else None
            report['rows'].append(dict(job=job, samples=samples, seconds=timings, ratio=ratio, scaled_error=str(error)))
            args.output.write_text(json.dumps(report, indent=2))
            print(f'{index+1}/{len(selected)} {job["group"]}/{job["case"]}/{job["dps"]}: '
                  + (f'after/before {ratio:.3f}' if ratio else 'expected rejection'), flush=True)
    assert source_before == subprocess.check_output(['git', 'diff', 'HEAD'], cwd=REPO), 'source changed during benchmark'
    assert source_hash == harness_hash(), 'benchmark harness changed during run'
    report['completed'] = True
    args.output.write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--worker':
        worker(sys.argv[2])
    else:
        main()
