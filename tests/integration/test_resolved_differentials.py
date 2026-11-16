"""Resolved bases agree with the numerical engine in original coordinates."""

import pytest
from mpmath import mp

from generapy import Curve, CurveDifferentials
from generapy.curves import CurveDifferentials as ExportedBasis
from generapy.curves import _operations


def hyperelliptic(ctx, genus, even=False):
    roots = tuple(map(ctx.mpf, range(-genus, genus+1+even)))
    coefficients = [ctx.mpf(4)]
    for root in roots:
        out = [ctx.zero]*(len(coefficients)+1)
        for i, c in enumerate(coefficients):
            out[i] -= root*c
            out[i+1] += c
        coefficients = out
    return Curve({(0, 2): 1, **{(i, 0): -c for i, c in enumerate(coefficients) if c}}, ctx=ctx), roots


def assert_close(ctx, a, b):
    assert abs(a-b) < 10000*ctx.eps*max(1, abs(a), abs(b))


@pytest.mark.parametrize('genus,even', [(2, False), (3, False), (2, True)])
@pytest.mark.parametrize('sign', [1, -1])
def test_resolved_forms_integrate_to_both_abel_increments(genus, even, sign):
    ctx = mp.clone()
    ctx.dps = 25
    curve, roots = hyperelliptic(ctx, genus, even)

    def point(x):
        return x, sign*2*ctx.sqrt(ctx.fprod(x-r for r in roots))

    base, target = [point(roots[-1]+ctx.mpf(t)) for t in ('.2', '.3')]
    path = curve.path(base, target)
    for kind in (1, 2):
        basis = getattr(curve, f'resolved_differentials_kind_{kind}')()
        assert isinstance(basis, CurveDifferentials)
        assert CurveDifferentials is ExportedBasis
        assert (basis.kind, basis.source, basis.engine, basis.marking,
                basis.coordinates, basis.working_precision) == (
                    kind, 'automatic', 'hyperelliptic', 'baker', 'original', ctx.prec)
        actual = curve.integral(basis.forms, path).values
        expected = getattr(curve, f'abel_map_kind_{kind}')(target, base_place=base).value
        for a, b in zip(actual, expected):
            assert_close(ctx, a, b)
        assert getattr(curve, f'differentials_kind_{kind}') is None


@pytest.mark.parametrize('leading', [1, 4])
@pytest.mark.parametrize('scale', [1, 7])
def test_completed_square_and_equation_scale_keep_original_coordinates(leading, scale):
    ctx = mp.clone()
    ctx.dps = 30
    # scale*((y+x**2/2)**2-leading*(x**5-5*x**3+4*x)) = 0.
    curve = Curve({(0, 2): scale, (2, 1): scale, (4, 0): ctx.mpf(scale)/4,
                   (5, 0): -scale*leading, (3, 0): 5*scale*leading,
                   (1, 0): -4*scale*leading}, ctx=ctx)
    x = ctx.mpf(3)
    z = ctx.sqrt(leading*(x**5-5*x**3+4*x))
    y = z-x*x/2
    first, second = curve.resolved_differentials_kind_1(), curve.resolved_differentials_kind_2()
    expected = (1/z, x/z, leading*(3*x**3-5*x)/(4*z), leading*x*x/(4*z))
    for f, v in zip(first.forms+second.forms, expected):
        assert_close(ctx, f(x, y), v)
    assert first.denominator == second.denominator == ((0, 1, 1), (2, 0, ctx.mpf('.5')))
    for basis in (first, second):
        for f, numerator in zip(basis.forms, basis.numerators):
            top = ctx.fsum(c*x**i*y**j for i, j, c in numerator)
            bottom = ctx.fsum(c*x**i*y**j for i, j, c in basis.denominator)
            assert_close(ctx, f(x, y), top/bottom)


def test_period_sign_and_basis_order_from_independent_a_cycle_quadrature():
    ctx = mp.clone()
    ctx.dps = 25
    curve, _ = hyperelliptic(ctx, 2)
    # Baker a1 surrounds [-2,-1] on the sheet with positive y there.
    def period(form):
        def value(t):
            x = -ctx.mpf('1.5')-ctx.cos(t)/2
            dx = ctx.sin(t)/2
            y = ctx.sin(t)*ctx.sqrt(abs(x*(x-1)*(x-2)))
            return form(x, y)*dx
        return 2*ctx.quad(value, [0, ctx.pi])

    for kind, matrix_name in ((1, 'omega'), (2, 'eta')):
        basis = getattr(curve, f'resolved_differentials_kind_{kind}')()
        periods = getattr(curve, f'periods_kind_{kind}')()
        matrix = getattr(periods, matrix_name)
        for row, form in enumerate(basis.forms):
            assert_close(ctx, period(form), (1 if kind == 1 else -1)*2*matrix[row, 0])


def test_genus_three_bel_numerators_have_the_expected_normalization():
    ctx = mp.clone()
    ctx.dps = 25
    curve, roots = hyperelliptic(ctx, 3)
    x = ctx.mpf(4)
    y = 2*ctx.sqrt(ctx.fprod(x-r for r in roots))
    basis = curve.resolved_differentials_kind_2()
    expected = ((5*x**5-42*x**3+49*x)/y, (3*x**4-14*x*x)/y, x**3/y)
    for form, value in zip(basis.forms, expected):
        assert_close(ctx, form(x, y), value)


def test_resolved_forms_keep_the_callers_scaled_x_coordinate():
    ctx = mp.clone()
    ctx.dps = 25
    # y**2 = 4*((2*x)**5-5*(2*x)**3+4*(2*x)).
    curve = Curve({(0, 2): 1, (5, 0): -128, (3, 0): 160, (1, 0): -32}, ctx=ctx)
    x = ctx.mpf('1.5')
    y = ctx.sqrt(128*x**5-160*x**3+32*x)
    first, second = curve.resolved_differentials_kind_1(), curve.resolved_differentials_kind_2()
    for f, v in zip(first.forms+second.forms,
                    (1/y, x/y, (96*x**3-40*x)/y, 32*x*x/y)):
        assert_close(ctx, f(x, y), v)


@pytest.mark.parametrize('kind', [1, 2])
def test_resolved_automatic_forms_reject_singular_models(kind):
    curve = Curve({(0, 2): 1, (3, 0): -1, (1, 0): 3, (0, 0): -2})
    with pytest.raises(ValueError, match='distinct roots'):
        getattr(curve, f'resolved_differentials_kind_{kind}')()


def test_general_automatic_basis_matches_period_forms_without_period_integration(monkeypatch):
    ctx = mp.clone()
    ctx.dps = 20
    curve = Curve({(0, 3): 1, (3, 0): 1, (0, 0): -1}, ctx=ctx)
    original = _operations._stage_geometric_periods
    monkeypatch.setattr(_operations, '_stage_geometric_periods', lambda *a: pytest.fail('basis resolution integrated periods'))
    basis = curve.resolved_differentials_kind_1()
    assert (basis.source, basis.engine, basis.marking) == ('automatic', 'general', 'geometric-polygon')
    x, y = ctx.mpf('.2'), ctx.root(1-ctx.mpf('.2')**3, 3)
    assert_close(ctx, basis.forms[0](x, y), 1/(3*y*y))
    monkeypatch.setattr(_operations, '_stage_geometric_periods', original)
    assert_close(ctx, basis.forms[0](x, y), curve.periods_kind_1().differentials[0](x, y))
    with pytest.raises(ValueError, match='Construct Curve.*differentials_kind_2'):
        curve.resolved_differentials_kind_2()


def test_supplied_bases_preserve_callables_and_dispatch():
    ctx = mp.clone()
    ctx.dps = 20
    first, second = (lambda x, y: 1/y,), (lambda x, y: x/(4*y),)
    curve = Curve({(0, 2): 1, (3, 0): -1, (1, 0): 1},
                  differentials_kind_1=first, differentials_kind_2=second, ctx=ctx)
    for kind, supplied in ((1, first), (2, second)):
        basis = getattr(curve, f'resolved_differentials_kind_{kind}')()
        assert basis.forms == supplied
        assert basis.source == 'supplied'
        assert basis.engine == 'general' and basis.marking == 'geometric-polygon'
        assert basis.numerators is basis.denominator is None
        assert getattr(curve, f'differentials_kind_{kind}') == supplied


def test_second_kind_only_dispatch_uses_geometric_first_kind_basis():
    ctx = mp.clone()
    ctx.dps = 20
    second = (lambda x, y: x/(4*y),)
    curve = Curve({(0, 2): 1, (3, 0): -1, (1, 0): 1}, differentials_kind_2=second, ctx=ctx)
    basis = curve.resolved_differentials_kind_1()
    x, y = ctx.mpf(2), ctx.sqrt(6)
    assert_close(ctx, basis.forms[0](x, y), 1/(2*y))
    assert basis.source == 'automatic' and basis.marking == 'geometric-polygon'
    assert curve.resolved_differentials_kind_2().forms == second
    assert basis.marking == curve.periods_kind_1().marking


@pytest.mark.parametrize('kind', [1, 2])
def test_resolved_basis_rejects_wrong_supplied_dimension(kind):
    curve = Curve({(0, 2): 1, (3, 0): -1, (1, 0): 1},
                  **{f'differentials_kind_{kind}': (lambda x, y: 1/y, lambda x, y: x/y)})
    with pytest.raises(ValueError, match='one form per genus'):
        getattr(curve, f'resolved_differentials_kind_{kind}')()


def test_hyperelliptic_resolution_is_lazy_and_precision_is_explicit(monkeypatch):
    ctx = mp.clone()
    ctx.dps = 20
    leading = '4.123456789123456789123456789'
    curve = Curve({(0, 2): 1, (5, 0): '-'+leading, (3, 0): 5, (1, 0): -4}, ctx=ctx)
    monkeypatch.setattr(_operations, '_stage_hyperelliptic_periods', lambda *a: pytest.fail('basis resolution integrated periods'))
    old = curve.resolved_differentials_kind_2()
    with pytest.raises(AttributeError):
        old.source = 'changed'
    ctx.dps = 40
    with pytest.warns(UserWarning, match='context changed'):
        new = curve.resolved_differentials_kind_2()
    assert old.working_precision < new.working_precision == ctx.prec
    assert old.numerators[1][0][2] != new.numerators[1][0][2]
    assert_close(ctx, new.numerators[1][0][2], ctx.mpf(leading)/4)
