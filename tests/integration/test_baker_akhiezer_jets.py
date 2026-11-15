"""BA jets across automatic hyperelliptic and supplied trigonal data."""

import importlib
from itertools import product

from mpmath import mp
import pytest

from generapy import (
    Curve, baker_akhiezer, baker_akhiezer_jet, kleinian_p, kleinian_sigma, kleinian_zeta,
)


@pytest.fixture
def curve():
    ctx = mp.clone()
    ctx.dps = 30
    return Curve({(0, 2): 1, (5, 0): -4, (3, 0): 20, (1, 0): -16}, ctx=ctx)


@pytest.mark.parametrize('normalization', ['spectral', 'reference'])
def test_genus_two_spectral_equation_uses_public_ordinary_jets(curve, normalization):
    ctx = curve.ctx
    u = [ctx.mpf('.13'), ctx.mpf('.27')]
    kwargs = dict(curve=curve, point=(3, ctx.sqrt(480)), normalization=normalization)
    if normalization == 'reference':
        kwargs['reference'] = [ctx.mpf('.2'), ctx.mpf('.3')]
    jet = baker_akhiezer_jet(u, direction=[0, 1], order=3, **kwargs)
    potential = kleinian_p(u, curve=curve, indices=(1, 1))
    # CEEK equation (3.22), with lambda_4=0 for this curve.
    assert abs(jet[2] - (2*potential+3)*jet[0]) < ctx.mpf('1e-24') * max(1, abs(jet[2]))
    assert ctx.almosteq(jet[0], baker_akhiezer(u, **kwargs))


@pytest.mark.parametrize('normalization', ['spectral', 'reference'])
def test_dense_genus_two_jets_at_a_numerator_zero(curve, normalization):
    ctx = curve.ctx
    point = (3, ctx.sqrt(480))
    shift = curve.abel_map_kind_1(point).value
    other = curve.abel_map_kind_1((4, ctx.sqrt(2880))).value
    # A-u is another one-point Abel image, on the genus-two sigma divisor.
    u = shift-other
    direction = [ctx.mpf('.3'), ctx.mpf('-.7')]
    first, second = curve.periods_kind_1(), curve.periods_kind_2()
    r = curve.abel_map_kind_2(point).value
    characteristic = curve.riemann_constant().characteristic
    kwargs = dict(normalization=normalization)
    if normalization == 'reference':
        kwargs['reference'] = [ctx.mpf('.13'), ctx.mpf('.27')]
    jet = baker_akhiezer_jet(u, curve=curve, point=point, direction=direction, order=3, **kwargs)

    def value(t):
        return baker_akhiezer(
            u+ctx.matrix(direction)*t, shift, r, first.omega, first.tau,
            second.kappa, characteristic, ctx=ctx, **kwargs)

    assert abs(jet[0]) < ctx.mpf('1e-24')
    for n in range(1, 4):
        expected = ctx.diff(value, 0, n)
        assert ctx.isfinite(jet[n])
        assert abs(jet[n]-expected) < ctx.mpf('1e-23') * max(1, abs(expected))


def test_multiple_ba_points_reuse_denominator_jet_without_public_state(curve):
    ctx = curve.ctx
    rt = importlib.import_module('generapy.riemann_theta')
    u = list(map(ctx.mpf, ('.13', '.27')))
    kwargs = dict(curve=curve, direction=[0, 1], order=3)
    baker_akhiezer_jet(u, point=(3, ctx.sqrt(480)), **kwargs)
    hits = rt._rtheta_evaluation_cache.cache_info(ctx).hits
    baker_akhiezer_jet(u, point=(4, ctx.sqrt(2880)), **kwargs)
    assert rt._rtheta_evaluation_cache.cache_info(ctx).hits > hits


def test_reference_jets_are_invariant_under_compatible_cycle_reduction(curve):
    ctx = curve.ctx
    u = list(map(ctx.mpf, ('.13', '.27')))
    kwargs = dict(curve=curve, point=(3, ctx.sqrt(480)), normalization='reference',
                  reference=list(map(ctx.mpf, ('.2', '.3'))), direction=[.3, -.7], order=3)
    first = baker_akhiezer_jet(u, **kwargs)
    reduced = baker_akhiezer_jet(u, reduce=True, **kwargs)
    for actual, expected in zip(reduced, first):
        assert abs(actual-expected) < ctx.mpf('1e-24') * max(1, abs(expected))


def test_point_and_period_input_errors(curve):
    with pytest.raises(ValueError, match='point must be a vector'):
        baker_akhiezer([.2, .3], curve=curve, point=[[1, 2], [3, 4]])
    with pytest.raises(ValueError, match='ctx must be'):
        baker_akhiezer([.2, .3], curve=curve, point=(3, curve.ctx.sqrt(480)), ctx=mp.clone())
    with pytest.raises(ValueError, match='cannot be combined with explicit'):
        baker_akhiezer([.2, .3], curve=curve, point=(3, curve.ctx.sqrt(480)), omega=[[1]])


def test_supplied_trigonal_curve_jets_match_sigma_zeta_and_p():
    from examples.bernatska.bernatska_trigonal_demo import differentials, trigonal_curve

    with mp.workdps(18):
        first, second = differentials()
        curve = Curve(trigonal_curve(), differentials_kind_1=first, differentials_kind_2=second)
        point = curve.fibre(2)[0]
        shift = curve.abel_map_kind_1(point).value
        r = curve.abel_map_kind_2(point).value
        u, reference, direction = [mp.matrix(list(map(mp.mpf, values))) for values in (
            ('.2', '.11', '.27'), ('.13', '.17', '.19'), ('.6', '-.2', '.3'))]
        jet = baker_akhiezer_jet(u, shift=shift, second_kind=r, curve=curve,
                                reference=reference, normalization='reference',
                                direction=direction, order=3)
        sigma = lambda v: kleinian_sigma(v, curve=curve)
        expected = (sigma(shift-u)*sigma(reference)/(sigma(u)*sigma(shift-reference))
                    * mp.exp(-(r.T*(u-reference))[0]))
        z_u, z_a = kleinian_zeta(u, curve=curve), kleinian_zeta(shift-u, curve=curve)
        log1 = -(direction.T*(z_u+z_a+r))[0]
        contractions = []
        for degree in (2, 3):
            indices = tuple(product(range(3), repeat=degree))
            p_u = kleinian_p(u, curve=curve, indices=indices)
            p_a = kleinian_p(shift-u, curve=curve, indices=indices)
            contractions.append(mp.fsum(
                mp.fprod(direction[i] for i in index)*(v-w if degree == 2 else v+w)
                for index, v, w in zip(indices, p_u, p_a)))
        log2, log3 = contractions
        expected_jet = (expected, expected*log1, expected*(log1**2+log2),
                        expected*(log1**3+3*log1*log2+log3))
        for actual, expected in zip(jet, expected_jet):
            assert abs(actual-expected) < mp.mpf('1e-11') * max(1, abs(expected))
