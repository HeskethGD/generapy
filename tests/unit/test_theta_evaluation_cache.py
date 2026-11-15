"""Evaluated theta results are reusable without leaking mutable jets."""

import importlib

import pytest
from mpmath import mp

from generapy import rtheta, rtheta_jet

rt = importlib.import_module('generapy.riemann_theta')


@pytest.mark.parametrize('imaginary_tau', ['1', '.02'])
def test_identical_requests_reuse_summation_and_return_fresh_jets(monkeypatch, imaginary_tau):
    ctx = mp.clone()
    ctx.dps = 25
    tau = [[ctx.j * ctx.mpf(imaginary_tau)]]
    z = [ctx.mpf('.2')]
    calls = []
    original = rt._rtheta_sum

    def counted(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(rt, '_rtheta_sum', counted)
    value = rtheta(z, tau, ctx=ctx)
    assert rtheta(z, tau, ctx=ctx) == value
    assert len(calls) == 1
    first = rtheta_jet(z, tau, 3, ctx=ctx)
    expected = first.copy()
    first[(0,)] = 999
    assert rtheta_jet(z, tau, 3, ctx=ctx) == expected
    assert len(calls) == 2
    q = ctx.exp(ctx.pi * ctx.j * tau[0][0])
    for n in range(4):
        independent = ctx.pi**n * ctx.jtheta(3, ctx.pi*z[0], q, derivative=n)
        assert abs(expected[(n,)] - independent) < ctx.mpf('1e-22') * max(1, abs(independent))


def test_cache_separates_inputs_context_and_numerical_state():
    ctx = mp.clone()
    ctx.dps = 25
    cache = rt._rtheta_evaluation_cache
    tau = [[ctx.j]]
    z = [ctx.mpf('.2')]
    reference = rtheta(z, tau, ctx=ctx)
    rtheta([ctx.mpf('.3')], tau, ctx=ctx)
    rtheta(z, [[2*ctx.j]], ctx=ctx)
    rtheta(z, tau, [[.5], [.5]], ctx=ctx)
    rtheta(z, tau, derivative=1, ctx=ctx)
    rtheta_jet(z, tau, 2, ctx=ctx)
    assert cache.cache_info(ctx).misses == 6
    with ctx.extraprec(20):
        rtheta(z, tau, ctx=ctx)
    assert cache.cache_info(ctx).misses == 7
    ctx.trap_complex = True
    assert rtheta(z, tau, ctx=ctx) == reference
    assert cache.cache_info(ctx).misses == 8
    other = mp.clone()
    other.dps = ctx.dps
    rtheta(z, tau, ctx=other)
    assert cache.cache_info(other).misses == 1
    # Mutating public period input changes the key rather than reusing old data.
    tau[0][0] = 3*ctx.j
    assert rtheta(z, tau, ctx=ctx) != reference


def test_cache_evicts_old_results_and_skips_large_jets(monkeypatch):
    ctx = mp.clone()
    ctx.dps = 15
    cache = rt._rtheta_evaluation_cache
    for i in range(34):
        rtheta([ctx.mpf(i)/100], [[ctx.j]], ctx=ctx)
    assert cache.cache_info(ctx).currsize == 32
    misses = cache.cache_info(ctx).misses
    rtheta([0], [[ctx.j]], ctx=ctx)
    assert cache.cache_info(ctx).misses == misses + 1
    # Exercise the retention limit without performing a costly order-128 sum.
    calls = []

    def evaluate(*args):
        calls.append(1)
        return (ctx.one,) * len(args[-1])

    monkeypatch.setattr(rt, '_rtheta_evaluate', evaluate)
    request = ((0,),) * 129
    for _ in range(2):
        assert len(rt._rtheta_normalized_derivatives(
            ctx, (ctx.zero,), ((ctx.j,),), (ctx.zero,), (ctx.zero,), request)) == 129
    assert len(calls) == 2
    assert cache.cache_info(ctx).misses == misses + 1
