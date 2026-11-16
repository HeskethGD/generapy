"""Direct directional jets versus full tensors and independent theta functions."""

import importlib
import math

from mpmath import mp
import pytest

from generapy import (
    Curve, kleinian_sigma_directional_jet, kleinian_sigma_jet,
    rtheta_directional_jet, rtheta_jet,
)
from benchmarks.rtheta.directional_cases import cases

rt = importlib.import_module('generapy.riemann_theta')


def contract(ctx, jet, direction, order):
    return tuple(ctx.fsum(
        math.factorial(n)//math.prod(math.factorial(k) for k in index)
        * ctx.fprod(d**k for d, k in zip(direction, index))*v
        for index, v in jet.items() if sum(index) == n) for n in range(order+1))


@pytest.mark.parametrize('case_name', ['g1', 'g2-coupled', 'g2-unreduced-shifted', 'g3-unreduced', 'issue17'])
def test_theta_directional_direct_reduced_and_full_tensor_agree(case_name):
    ctx = mp.clone()
    ctx.dps = 32
    _, tau, z, char = next(case for case in cases(ctx) if case[0] == case_name)
    genus = len(z)
    directions = ([0]*genus, [0]*(genus-1)+[1], [ctx.mpc('.7', '.2')/(i+1) for i in range(genus)])
    full = rtheta_jet(z, tau, 3, char, ctx=ctx)
    for direction in directions:
        expected = contract(ctx, full, direction, 3)
        actual = rtheta_directional_jet(z, tau, direction, 3, char, ctx=ctx)
        with ctx.extraprec(70):
            reduced, ops, _ = rt._rtheta_reduction_data(ctx, tau)
            alternate = rt._rtheta_directional_reduced(
                ctx, z, tau, *char, direction, 3, ops, reduced)
            direct = rt._rtheta_directional_sum(ctx, z, tau, *char, direction, 3)
        for result in (actual, alternate, direct):
            for a, b in zip(result, expected):
                assert abs(a-b) < ctx.mpf('1e-26')*max(1, abs(b))


@pytest.mark.parametrize('order', [0, 1, 2, 3, 5])
@pytest.mark.parametrize('scale', ['1e-8', '1', '1e8'])
def test_genus_one_complex_direction_at_zero_matches_jtheta(order, scale):
    ctx = mp.clone()
    ctx.dps = 35
    tau = ctx.mpc('.17', '.03')
    direction = ctx.mpc('.6', '.2')*ctx.mpf(scale)
    actual = rtheta_directional_jet([0], [[tau]], [direction], order, [[.5], [.5]], ctx=ctx)
    with ctx.extraprec(200):
        q = ctx.exp(ctx.pi*ctx.j*tau)
        expected = tuple(-(ctx.pi*direction)**n*ctx.jtheta(1, 0, q, derivative=n) for n in range(order+1))
    for a, b in zip(actual, expected):
        assert abs(a-b) < ctx.mpf('1e-27')*max(1, abs(b))


def test_sigma_directional_dense_transformation_and_gaussian():
    ctx = mp.clone()
    ctx.dps = 30
    for case_name in ('g2-coupled', 'issue17'):
        _, tau, u, char = next(case for case in cases(ctx) if case[0] == case_name)
        genus = len(u)
        omega = ctx.eye(genus)/2
        omega[0, 1] = ctx.mpf('.07')
        kappa = ctx.matrix([[ctx.mpf('.12') if i == j else ctx.mpf('.03')
                            for j in range(genus)] for i in range(genus)])
        for direction in ([0]*genus, [0]*(genus-1)+[1], [ctx.mpc('.3', '.1')/(i+1) for i in range(genus)]):
            full = kleinian_sigma_jet(u, omega, tau, kappa, 3, char, ctx=ctx)
            expected = contract(ctx, full, direction, 3)
            for order in range(4):
                actual = kleinian_sigma_directional_jet(
                    u, omega, tau, kappa, order, char, direction=direction, ctx=ctx)
                for a, b in zip(actual, expected):
                    assert abs(a-b) < ctx.mpf('1e-24')*max(1, abs(b))


def test_sigma_directional_curve_and_mapping_normalization():
    ctx = mp.clone()
    ctx.dps = 25
    polynomial = {(0, 2): 1, (5, 0): -4, (3, 0): 20, (1, 0): -16}
    curve = Curve(polynomial, ctx=ctx)
    for normalization in ('theta', 'hyperelliptic'):
        full = kleinian_sigma_jet([.2, .3], curve=curve, order=3, normalization=normalization)
        expected = contract(ctx, full, [1, -.5], 3)
        for value in (curve, polynomial):
            actual = kleinian_sigma_directional_jet(
                [.2, .3], curve=value, order=3, direction=[1, -.5], normalization=normalization, ctx=ctx)
            assert all(abs(a-b) < ctx.mpf('1e-20')*max(1, abs(b)) for a, b in zip(actual, expected))


def test_directional_cache_keys_precision_context_and_direction():
    ctx = mp.clone()
    ctx.dps = 25
    cache = rt._rtheta_directional_evaluation_cache
    first = rtheta_directional_jet([.2], [[ctx.j]], [1], 3, ctx=ctx)
    assert rtheta_directional_jet([.2], [[ctx.j]], [1], 3, ctx=ctx) == first
    assert cache.cache_info(ctx).hits == 1
    for direction, order in (([2], 3), ([1], 2)):
        rtheta_directional_jet([.2], [[ctx.j]], direction, order, ctx=ctx)
    with ctx.extraprec(30):
        rtheta_directional_jet([.2], [[ctx.j]], [1], 3, ctx=ctx)
    assert cache.cache_info(ctx).misses == 4
    other = mp.clone()
    other.dps = 25
    rtheta_directional_jet([.2], [[other.j]], [1], 3, ctx=other)
    assert cache.cache_info(other).misses == 1


@pytest.mark.parametrize('a,b', [(0, 0), (.5, .5), (.2, -.3)])
def test_directional_characteristics_without_parity_assumptions(a, b):
    ctx = mp.clone()
    ctx.dps = 32
    z, tau, direction = [ctx.mpc('.13', '.03')], [[ctx.mpc('.17', '.03')]], [ctx.mpc('.6', '.2')]
    char = [[a], [b]]
    expected = contract(ctx, rtheta_jet(z, tau, 3, char, ctx=ctx), direction, 3)
    actual = rtheta_directional_jet(z, tau, direction, 3, char, ctx=ctx)
    assert all(abs(x-y) < ctx.mpf('1e-26')*max(1, abs(y)) for x, y in zip(actual, expected))


def test_directional_cache_retention_and_large_order_bypass(monkeypatch):
    ctx = mp.clone()
    ctx.dps = 15
    cache = rt._rtheta_directional_evaluation_cache
    for i in range(34):
        rtheta_directional_jet([ctx.mpf(i)/100], [[ctx.j]], [1], 1, ctx=ctx)
    assert cache.cache_info(ctx).currsize == 32
    misses = cache.cache_info(ctx).misses
    rtheta_directional_jet([0], [[ctx.j]], [1], 1, ctx=ctx)
    assert cache.cache_info(ctx).misses == misses+1
    calls = []

    def evaluate(*args):
        calls.append(1)
        return (ctx.one,)*(args[-1]+1)

    monkeypatch.setattr(rt, '_rtheta_directional_evaluate', evaluate)
    for _ in range(2):
        assert len(rtheta_directional_jet([0], [[ctx.j]], [1], 128, ctx=ctx)) == 129
    assert len(calls) == 2
    assert cache.cache_info(ctx).misses == misses+1


@pytest.mark.parametrize('direction, order, message', [
    ([1], -1, 'order'), ([1], 1.5, 'order'), ([1], True, 'order'),
    (None, 1, 'direction'), ([1, 2], 1, 'direction'), ([mp.inf], 1, 'finite'),
])
def test_directional_input_errors(direction, order, message):
    with pytest.raises(ValueError, match=message):
        rtheta_directional_jet([.2], [[1j]], direction, order)
    with pytest.raises(ValueError, match=message):
        kleinian_sigma_directional_jet([.2], [[.5]], [[1j]], [[0]], order, direction=direction)
