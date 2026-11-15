"""Independent checks of compatible Baker-marked Abel lifts (issue #11)."""

import pytest
from mpmath import mp

from generapy import Curve, kleinian_sigma_jet
from generapy import baker_akhiezer
from generapy.curves._hyperelliptic.model import _admissible_branch_vertex


@pytest.fixture(params=[25, 35, 45])
def curve(request):
    ctx = mp.clone()
    ctx.dps = request.param
    coefficients = tuple(map(ctx.mpf, (
        '-1124.75', '-675', '1250', '786', '-125', '-115', '0', '4')))
    return Curve({(0, 2): 1, **{
        (i, 0): -a for i, a in enumerate(coefficients) if a}}, ctx=ctx)


def sigma_second_kind(curve, abel):
    # Genus-three one-point sigma identity in the automatic BEL basis:
    # h(A(P)) = -R(P). This does not obtain R from Abel quadrature.
    jet = kleinian_sigma_jet(abel, order=2, curve=curve)
    sharp = jet[(0, 1, 0)]
    h2 = jet[(0, 2, 0)] / (2 * sharp)
    return -curve.ctx.matrix([
        jet[(1, 1, 0)] / sharp - jet[(1, 0, 0)] * h2 / sharp,
        h2, jet[(0, 1, 1)] / sharp])


def test_first_and_second_kind_share_lifts(curve):
    ctx = curve.ctx
    tolerance = ctx.mpf(10) ** (8 - ctx.dps)
    # The real target is equidistant from the nearby conjugate branch pair.
    # Perturb to either side of its distance bisector, including near ties.
    for offset in ('0', '1e-12', '-1e-12'):
        x = ctx.mpc('-2.5', offset)
        with ctx.extraprec(80):
            y = ctx.sqrt(ctx.fsum(-a * x**i for (i, j), a
                                 in curve.polynomial.items() if j == 0))
        y = +y
        for sign in (1, -1):
            target = (x, sign * y)
            first = curve.abel_map_kind_1(target)
            second = curve.abel_map_kind_2(target)
            expected = sigma_second_kind(curve, first.value)
            assert ctx.norm(second.value - expected) < tolerance

            reduced_first = curve.abel_map_kind_1(target, reduce=True)
            reduced_second = curve.abel_map_kind_2(target, reduce=True)
            assert reduced_first.reduction_shift == reduced_second.reduction_shift
            assert ctx.norm(reduced_second.value - sigma_second_kind(
                curve, reduced_first.value)) < tolerance


def test_ba_curve_route_uses_sigma_compatible_exponent(curve):
    ctx = curve.ctx
    target = (ctx.mpf('-2.5'), ctx.mpf('.5'))
    u = list(map(ctx.mpf, ('.13', '.17', '.23')))
    first = curve.periods_kind_1()
    second = curve.periods_kind_2()
    characteristic = curve.riemann_constant().characteristic
    for reduce in (False, True):
        abel = curve.abel_map_kind_1(target, reduce=reduce).value
        expected = baker_akhiezer(
            u, abel, sigma_second_kind(curve, abel), first.omega, first.tau,
            second.kappa, characteristic, ctx=ctx)
        actual = baker_akhiezer(
            u, curve=curve, point=target, reduce=reduce)
        assert abs(actual - expected) / max(1, abs(expected)) < ctx.mpf(10)**(8 - ctx.dps)


def test_finite_base_abel_maps_preserve_shared_lifts(curve):
    ctx = curve.ctx
    target = (ctx.mpf('-2.5'), ctx.mpf('.5'))
    x = ctx.mpf('-2.500001')
    with ctx.extraprec(80):
        y = ctx.sqrt(ctx.fsum(-a * x**i for (i, j), a
                             in curve.polynomial.items() if j == 0))
    base = (x, +y)
    target_abel = curve.abel_map_kind_1(target).value
    base_abel = curve.abel_map_kind_1(base).value
    expected = sigma_second_kind(curve, target_abel) - sigma_second_kind(curve, base_abel)
    for reduce in (False, True):
        first = curve.abel_map_kind_1(target, base_place=base, reduce=reduce)
        second = curve.abel_map_kind_2(target, base_place=base, reduce=reduce)
        shifted = expected.copy()
        if reduce:
            periods = curve.periods_kind_2()
            m, n = first.reduction_shift[:3], first.reduction_shift[3:]
            shifted += 2 * periods.eta * ctx.matrix(m) + 2 * periods.eta_prime * ctx.matrix(n)
        assert first.reduction_shift == second.reduction_shift
        assert ctx.norm(second.value - shifted) < ctx.mpf(10)**(8 - ctx.dps)
        if not reduce:
            assert ctx.norm(first.value - (target_abel - base_abel)) < ctx.mpf(10)**(8 - ctx.dps)


def test_branch_anchor_ties_use_order_without_overriding_distinct_distances():
    ctx = mp.clone()
    ctx.dps = 30
    target_eps = +ctx.eps
    for guard in (20, 60):
        with ctx.extraprec(guard):
            # Small errors in a resolved conjugate pair must not decide the lift.
            for error in (-target_eps / 10, 0, target_eps / 10):
                roots = (-ctx.j * (1 + error), ctx.j, ctx.mpf(10))
                assert _admissible_branch_vertex(ctx, 0, roots, target_eps) == 0
                assert _admissible_branch_vertex(ctx, ctx.j / 100, roots, target_eps) == 1
                assert _admissible_branch_vertex(ctx, -ctx.j / 100, roots, target_eps) == 0
