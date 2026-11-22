"""Measure the issue #33 general-curve pipeline independently of the full suite.

Run with --after v0.3.0 --output /tmp/pipeline.json. Optionally add --before
REV for a fresh matched comparison. Each precision/trial/revision uses a new
process and an archived source tree. No external mathematics tools are used.
"""

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
from statistics import median
import subprocess
import sys
import tempfile
from time import perf_counter


REPO = Path(__file__).resolve().parents[1]
QUINTIC = {
    (5, 0): (1, 1), (4, 0): (-11, 1), (3, 2): (-2, 1),
    (3, 1): (7, 1), (3, 0): (-234, 1), (2, 2): (11, 1),
    (2, 1): (-89, 1), (2, 0): (30759, 4), (1, 4): (1, 1),
    (1, 3): (-7, 1), (1, 2): (274, 1), (1, 1): (-2613, 4),
    (1, 0): (-550865, 16), (0, 3): (52, 1), (0, 2): (-6464, 1),
    (0, 1): (21886, 1), (0, 0): (49559, 2),
}


def worker(snapshot, digits):
    """Time public operations without instrumentation or validation in timings."""
    sys.path.insert(0, str(snapshot / 'src'))
    import generapy
    import mpmath
    from mpmath import mp

    assert Path(generapy.__file__).resolve().is_relative_to(snapshot.resolve())
    ctx = mp.clone()
    ctx.dps = digits
    terms = {(j, i): ctx.mpf(p)/q for (i, j), (p, q) in QUINTIC.items()}

    def fy(x, y):
        return ctx.fsum(c*j*x**i*y**(j-1) for (i, j), c in terms.items() if j)

    forms = (lambda x, y: 1/fy(x, y), lambda x, y: y/fy(x, y),
             lambda x, y: x/fy(x, y), lambda x, y: (y*y-x*x)/fy(x, y))
    curve = generapy.Curve(terms, differentials_kind_1=forms, ctx=ctx)
    result = dict(digits=digits, mpmath=mpmath.__version__, phases=[], values={})

    def phase(name, function):
        print(f'Starting {name} ({digits} digits)', file=sys.stderr, flush=True)
        start = perf_counter()
        value = function()
        seconds = perf_counter()-start
        result['phases'].append(dict(name=name, seconds=seconds))
        print(f'Finished {name}: {seconds:.3f}s', file=sys.stderr, flush=True)
        return value

    genus = phase('cold_genus', lambda: curve.genus)
    periods = phase('periods_after_genus', curve.periods_kind_1)
    points = [curve.fibre(ctx.mpc(x, y))[0] for x, y in [('3.3', '1.7'), ('3.31', '1.71')]]
    abel = []
    for name, point in [('abel_first', points[0]), ('abel_repeat', points[0]), ('abel_nearby', points[1])]:
        value = phase(name, lambda: curve.abel_map_kind_1(point, reduce=False).value)
        abel.append(value)
        result['values'][name] = [str(v) for v in value]
    constant = phase('riemann_constant_after_abel', curve.riemann_constant)
    for name in ('omega', 'omega_prime', 'tau'):
        matrix = getattr(periods, name)
        result['values'][name] = [str(v) for v in matrix]
    result['values']['riemann_constant'] = [str(v) for v in constant.value]

    # These checks run after all timings so they cannot warm the measured stages.
    assert genus == 4 and min(periods.imaginary_eigenvalues) > 0
    assert curve.validate(periods).passed
    tolerance = ctx.mpf(10)**(5-digits)
    assert ctx.norm(abel[0]-abel[1]) < tolerance
    increment = curve.abel_map_kind_1(points[1], base_place=points[0], reduce=False).value
    base_residual = ctx.norm(increment-(abel[2]-abel[0]))
    assert base_residual < tolerance
    argument = 3*((2*periods.omega)**-1*abel[0])+constant.value
    from generapy.curves import _operations
    reduced = _operations.lattice_reduce(ctx, argument, periods.tau).value
    residual = abs(generapy.rtheta(reduced, periods.tau, ctx=ctx))
    scale = max(ctx.one, abs(generapy.rtheta(ctx.matrix(['.13', '.17', '.19', '.23']), periods.tau, ctx=ctx)))
    assert residual/scale < tolerance
    assert all(ctx.isfinite(ctx.mpc(v)) for values in result['values'].values() for v in values)
    assert ctx.dps == digits
    result.update(status='ok', base_change_residual=str(base_residual), theta_residual=str(residual/scale))
    print(json.dumps(result), flush=True)


def difference(left, right, digits):
    """Compare every saved period, Abel coordinate and Riemann constant."""
    from mpmath import mp
    ctx = mp.clone()
    ctx.dps = digits+20
    assert left.keys() == right.keys()
    errors = []
    for name in left:
        assert len(left[name]) == len(right[name])
        errors.extend(abs(ctx.mpc(a)-ctx.mpc(b))/max(1, abs(ctx.mpc(a))) for a, b in zip(left[name], right[name]))
    error = max(errors, default=ctx.zero)
    assert error < ctx.mpf(10)**(5-digits), str(error)
    return str(error)


def summarize(report):
    rows = []
    for label in report['commits']:
        for digits in report['digits']:
            samples = [s for s in report['samples'] if s['revision'] == label and s['digits'] == digits]
            if not samples:
                continue
            for phase in samples[0]['phases']:
                name = phase['name']
                times = [next(p['seconds'] for p in s['phases'] if p['name'] == name) for s in samples]
                rows.append(dict(revision=label, digits=digits, phase=name,
                                 median=median(times), minimum=min(times), maximum=max(times), trials=len(times)))
    return rows


def render(report):
    lines = ['# Fresh general-curve pipeline measurements', '',
             f"Recorded {report['created']}; Python {report['python']}, mpmath {report['samples'][0]['mpmath']}.",
             f"Platform: {report['platform']}.", '',
             'Only the issue #33 supplied-basis genus-four workload was run.',
             'The existing 268-configuration release comparison was not rerun or modified.', '',
             '## Protocol', '',
             f"Each precision/revision has {report['trials']} fresh-process trials from archived committed source.",
             'Import, curve construction, fibre point selection and validation are excluded from timings.',
             'Stages run in table order on the same curve: periods reuse genus setup;',
             'the first Abel call follows periods; repeat and nearby calls reuse the marked setup.',
             'Riemann constants follow those Abel calls. No internal functions are patched.',
             'Validation checks period validity, repeated Abel agreement, base-point subtraction,',
             'Riemann vanishing at the effective divisor 3P, finite outputs and restored precision.',
             'Saved outputs are also compared between trials, precisions and revisions when available.', '',
             '## Source revisions', '']
    lines.extend(f'- {label}: `{commit}`.' for label, commit in report['commits'].items())
    lines += ['', f"Harness SHA-256: `{report['harness_sha256']}`.", '',
              '## Timings', '', '| Revision | Digits | Operation | Median seconds | Range | Trials |',
              '| --- | ---: | --- | ---: | ---: | ---: |']
    for row in report['summary']:
        lines.append(f"| {row['revision']} | {row['digits']} | {row['phase']} | {row['median']:.4f} | "
                     f"{row['minimum']:.4f}–{row['maximum']:.4f} | {row['trials']} |")
    lines += ['', '## Accuracy', '', f"All {len(report['samples'])} fresh trials passed the checks above.",
              'Cross-run comparisons use maximum scaled difference abs(a-b)/max(1,abs(a)),',
              'with tolerance 10**(5-dps) at the lower precision.', '']
    for check in report['comparisons']:
        lines.append(f"- {check['name']}: `{check['scaled_error']}`.")
    lines += ['', 'These current-tag timings supplement the separately retained historical development',
              'comparison. A candidate-only run establishes a repeatable baseline; it does not',
              'constitute a newly matched speedup comparison against the historical measurements.', '',
              '## Reproduction', '', '```sh',
              'python -m benchmarks.benchmark_general_curve_pipeline \\',
              f"  --after {report['commits']['after']} --dps {' '.join(map(str, report['digits']))} --trials {report['trials']} \\",
              '  --output /tmp/generapy-pipeline.json --report /tmp/generapy-pipeline.md', '```', '',
              'Add `--before REV` for a fresh comparison, alternating revision order between trials.',
              'Choose new output paths. Raw JSON remains untracked; only the Markdown report is retained.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--after', default='HEAD')
    parser.add_argument('--before')
    parser.add_argument('--dps', type=int, nargs='+', default=[20, 30])
    parser.add_argument('--trials', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=600)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--worker', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(args.worker, args.dps[0])
        return
    if not args.output or args.output.exists() or (args.report and args.report.exists()):
        parser.error('choose new output/report paths')
    if args.trials < 1 or min(args.dps) < 15 or len(args.dps) != len(set(args.dps)):
        parser.error('use positive trials and distinct precisions of at least 15 digits')
    from benchmarks.benchmark_generapy_revisions import archive
    harness = Path(__file__).resolve()
    digest = hashlib.sha256(harness.read_bytes()).hexdigest()
    initial_source = subprocess.check_output(['git', 'diff', 'HEAD', '--', 'src'], cwd=REPO)
    if initial_source:
        parser.error('commit numerical source changes before benchmarking')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = dict(created=datetime.now(timezone.utc).isoformat(), python=platform.python_version(),
                  platform=platform.platform(), digits=args.dps, trials=args.trials,
                  harness_sha256=digest, samples=[], comparisons=[])
    lock_dir = REPO/'benchmarks/results'
    lock_dir.mkdir(parents=True, exist_ok=True)
    with (lock_dir/'.general-curve-pipeline.lock').open('a+') as lock, tempfile.TemporaryDirectory(prefix='generapy-pipeline-') as temporary:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        revisions = {'before': args.before, 'after': args.after} if args.before else {'after': args.after}
        snapshots = {name: Path(temporary)/name for name in revisions}
        report['commits'] = {name: archive(revision, snapshots[name]) for name, revision in revisions.items()}
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        env.pop('PYTHONHOME', None)
        for digits in args.dps:
            for trial in range(args.trials):
                order = list(revisions) if trial % 2 == 0 else list(reversed(revisions))
                for label in order:
                    print(f'{label}: {digits} digits, trial {trial+1}/{args.trials}', flush=True)
                    process = subprocess.Popen([sys.executable, '-I', str(harness), '--worker', str(snapshots[label]),
                                                '--dps', str(digits)], stdout=subprocess.PIPE, text=True,
                                               cwd=temporary, env=env, start_new_session=True)
                    try:
                        stdout, _ = process.communicate(timeout=args.timeout)
                    except BaseException:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.communicate()
                        raise
                    if process.returncode:
                        raise RuntimeError(f'{label}/{digits}/{trial}: worker failed ({process.returncode})')
                    sample = dict(json.loads(stdout), revision=label, trial=trial+1)
                    report['samples'].append(sample)
                    args.output.write_text(json.dumps(report, indent=2)+'\n')
        for sample in report['samples'][1:]:
            reference = report['samples'][0]
            digits = min(sample['digits'], reference['digits'])
            error = difference(reference['values'], sample['values'], digits)
            report['comparisons'].append(dict(name=f"{reference['revision']}/{reference['digits']}/1 versus "
                                             f"{sample['revision']}/{sample['digits']}/{sample['trial']}", scaled_error=error))
        assert hashlib.sha256(harness.read_bytes()).hexdigest() == digest, 'harness changed during run'
        assert subprocess.check_output(['git', 'diff', 'HEAD', '--', 'src'], cwd=REPO) == initial_source
        report['summary'] = summarize(report)
        report['status'] = 'ok'
        args.output.write_text(json.dumps(report, indent=2)+'\n')
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(render(report))
        print('All pipeline trials and numerical comparisons passed.', flush=True)


if __name__ == '__main__':
    main()
