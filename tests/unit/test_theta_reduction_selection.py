"""Derivative-aware decisions on the issue #17 fixture and fast controls."""

import importlib

from mpmath import mp
import pytest

from generapy import rtheta, rtheta_directional_jet, rtheta_jet
from benchmarks.rtheta.directional_cases import cases

rt = importlib.import_module('generapy.riemann_theta')


@pytest.mark.parametrize('dps', [24, 40])
def test_issue17_full_jet_selects_reduction_and_matches_direct(monkeypatch, dps):
    ctx = mp.clone()
    ctx.dps = dps
    _, tau, z, char = next(case for case in cases(ctx) if case[0] == 'issue17')
    calls = []
    original = rt._rtheta_reduced_derivatives

    def record(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(rt, '_rtheta_reduced_derivatives', record)
    derivatives = tuple(rt._multiindices(3, 3))
    actual = rtheta_jet(z, tau, 3, char, ctx=ctx)
    assert len(calls) == 1
    for offset in (0, ctx.mpc('2.31', '-1.14')):
        shifted = (z[0]+offset, z[1], z[2])
        value = rtheta_jet(shifted, tau, 3, char, ctx=ctx)
        with ctx.extraprec(70):
            direct = rt._rtheta_sum(ctx, shifted, tau, *char, derivatives)
            reduced, ops, _ = rt._rtheta_reduction_data(ctx, tau)
            forced = original(ctx, shifted, tau, *char, derivatives, ops, reduced)
        for a, b, c in zip(value.values(), direct, forced):
            assert abs(a-b) < ctx.mpf(10)**(6-dps)*max(1, abs(b))
            assert abs(a-c) < ctx.mpf(10)**(6-dps)*max(1, abs(c))
    # A single partial has different work from the full 20-component jet.
    partial = rtheta(z, tau, char, derivative=(0, 0, 3), ctx=ctx)
    assert abs(partial-actual[(0, 0, 3)]) < ctx.mpf(10)**(6-dps)*max(1, abs(partial))


@pytest.mark.parametrize('dps', [24, 40])
@pytest.mark.parametrize('dense', [False, True])
def test_issue17_direction_changes_reduction_cost(monkeypatch, dps, dense):
    ctx = mp.clone()
    ctx.dps = dps
    _, tau, z, char = next(case for case in cases(ctx) if case[0] == 'issue17')
    direction = [ctx.mpf(1)/(i+1) for i in range(3)] if dense else [0, 0, 1]
    calls = []
    original = rt._rtheta_directional_reduced

    def record(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(rt, '_rtheta_directional_reduced', record)
    actual = rtheta_directional_jet(z, tau, direction, 3, char, ctx=ctx)
    assert bool(calls) == (not dense)
    with ctx.extraprec(70):
        expected = rt._rtheta_directional_sum(ctx, z, tau, *char, direction, 3)
    for a, b in zip(actual, expected):
        assert abs(a-b) < ctx.mpf(10)**(6-dps)*max(1, abs(b))


@pytest.mark.parametrize('name', ['g2-coupled', 'g3-coupled'])
def test_well_conditioned_controls_skip_reduction_setup(monkeypatch, name):
    ctx = mp.clone()
    ctx.dps = 24
    _, tau, z, char = next(case for case in cases(ctx) if case[0] == name)

    def unnecessary(*args):
        raise AssertionError('well-conditioned control must stay on the direct path')

    monkeypatch.setattr(rt, '_rtheta_reduction_data', unnecessary)
    assert len(rtheta_jet(z, tau, 3, char, ctx=ctx)) > 4
    assert len(rtheta_directional_jet(z, tau, [1]*len(z), 3, char, ctx=ctx)) == 4


def test_derivative_lattice_estimate_accounts_for_shift_and_direction():
    ctx = mp.clone()
    ctx.dps = 25
    tau = ((ctx.j,),)
    value_points = rt._rtheta_lattice_points(ctx, (ctx.zero,), tau, (0,))
    assert value_points == rt._rtheta_tau_data(ctx, tau)[6]
    centered = rt._rtheta_lattice_points(ctx, (ctx.zero,), tau, (0, 1, 2, 3), (ctx.one,))
    shifted = rt._rtheta_lattice_points(ctx, (20*ctx.j,), tau, (0, 1, 2, 3), (ctx.one,))
    amplified = rt._rtheta_lattice_points(ctx, (ctx.zero,), tau, (0, 1, 2, 3), (ctx.mpf('1e6'),))
    assert shifted > centered
    assert amplified > centered
