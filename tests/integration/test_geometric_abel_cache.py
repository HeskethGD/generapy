"""Repeated Abel maps reuse connectors without mixing numerical conventions."""

import pytest
from mpmath import mp

from generapy import Curve
from generapy.curves import _stages as stages


def values(curve, points):
    return tuple(curve.abel_map_kind_1(point, reduce=False).value for point in points)


def test_repeated_abel_maps_reuse_connectors_for_new_targets():
    ctx = mp.clone()
    ctx.dps = 20
    curve = Curve({(4, 0): 1, (0, 4): 1, (0, 0): -1}, ctx=ctx)
    stages._stage_geometric_abel_edge.cache_clear()
    values(curve, curve.fibre(ctx.mpc('1.2', '.3')))
    initial = stages._stage_geometric_abel_edge.cache_info()
    assert initial.misses > 0
    points = curve.fibre(ctx.mpc('1.21', '.31'))
    warm = values(curve, points)
    reused = stages._stage_geometric_abel_edge.cache_info()
    assert reused.hits > initial.hits and reused.misses == initial.misses
    stages._stage_geometric_abel_edge.cache_clear()
    fresh = values(curve, points)
    assert all(ctx.norm(a-b) < 1000*ctx.eps for a, b in zip(warm, fresh))


def test_connector_cache_separates_bases_kinds_contexts_and_precision():
    ctx = mp.clone()
    ctx.dps = 20
    terms = {(0, 2): 1, (3, 0): -1, (1, 0): 1}
    first = (lambda x, y: 1/y,)
    second = (lambda x, y: x/y,)
    curve = Curve(terms, differentials_kind_1=first,
                  differentials_kind_2=second, ctx=ctx)
    stages._stage_geometric_abel_edge.cache_clear()
    points = curve.fibre(ctx.mpc('2', '.2'))
    first_values = values(curve, points)
    misses = stages._stage_geometric_abel_edge.cache_info().misses
    second_values = tuple(curve.abel_map_kind_2(p).value for p in points)
    assert stages._stage_geometric_abel_edge.cache_info().misses > misses

    doubled = Curve(terms, differentials_kind_1=(lambda x, y: 2/y,),
                    differentials_kind_2=(lambda x, y: 2*x/y,), ctx=ctx)
    for p, a, b in zip(points, first_values, second_values):
        assert ctx.norm(doubled.abel_map_kind_1(p, reduce=False).value-2*a) < 1000*ctx.eps
        assert ctx.norm(doubled.abel_map_kind_2(p).value-2*b) < 1000*ctx.eps

    misses = stages._stage_geometric_abel_edge.cache_info().misses
    other = Curve(terms, differentials_kind_1=first, ctx=mp.clone())
    values(other, other.fibre(other.ctx.mpc('2', '.2')))
    assert stages._stage_geometric_abel_edge.cache_info().misses > misses

    misses = stages._stage_geometric_abel_edge.cache_info().misses
    ctx.dps = 30
    with pytest.warns(UserWarning, match='context changed'):
        points = curve.fibre(ctx.mpc('2', '.2'))
    high = values(curve, points)
    assert stages._stage_geometric_abel_edge.cache_info().misses > misses
    stages._stage_geometric_abel_edge.cache_clear()
    fresh = values(curve, points)
    assert all(ctx.norm(a-b) < 1000*ctx.eps for a, b in zip(high, fresh))


def test_unhashable_basis_keeps_operation_local_integration(monkeypatch):
    ctx = mp.clone()
    ctx.dps = 20

    class Form:
        __hash__ = None

        def __call__(self, x, y):
            return 1/y

    terms = {(0, 2): 1, (3, 0): -1, (1, 0): 1}
    curve = Curve(terms, differentials_kind_1=(Form(),), ctx=ctx)
    reference = Curve(terms, differentials_kind_1=(lambda x, y: 1/y,), ctx=ctx)
    points = curve.fibre(ctx.mpc('2', '.2'))
    expected = values(reference, points)

    def unexpected_cache(*args):
        pytest.fail('unhashable basis entered the shared connector cache')

    monkeypatch.setattr(stages, '_stage_geometric_abel_edge', unexpected_cache)
    for repeat in range(2):
        got = values(curve, points)
        assert all(ctx.norm(a-b) < 1000*ctx.eps for a, b in zip(got, expected))
