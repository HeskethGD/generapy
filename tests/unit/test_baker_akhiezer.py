"""Reference BA normalization and ordinary derivatives use literal arguments."""

import pytest
from mpmath import mp

from generapy import baker_akhiezer, baker_akhiezer_jet
from generapy import kleinian as implementation


@pytest.fixture
def data():
    ctx = mp.clone()
    ctx.dps = 35
    return dict(shift=[ctx.mpf('.4')], second_kind=[ctx.mpf('.7')],
                omega=[[ctx.mpf('.5')]], tau=[[ctx.j]], kappa=[[ctx.mpf('.12')]],
                reference=[ctx.mpf('.13')], normalization='reference', ctx=ctx)


def independent_sigma(ctx, z, characteristic=(.5, .5)):
    # Literal theta characteristic expressed through genus-one jtheta(3).
    a, b = map(ctx.mpf, characteristic)
    return (ctx.exp(ctx.mpf('.12')*z*z/2 - ctx.pi*a*a + 2*ctx.pi*ctx.j*a*(z+b))
            * ctx.jtheta(3, ctx.pi*(z+b+ctx.j*a), ctx.exp(-ctx.pi)))


def independent_reference(ctx, u, data, characteristic=(.5, .5)):
    sigma = lambda z: independent_sigma(ctx, z, characteristic)
    a, r, ref = data['shift'][0], data['second_kind'][0], data['reference'][0]
    return (sigma(a-u)*sigma(ref)/(sigma(u)*sigma(a-ref))
            * ctx.exp(-r*(u-ref)))


@pytest.mark.parametrize('characteristic', [(.5, .5), (0, 0), (.2, -.3)])
def test_reference_matches_jtheta_without_assuming_parity(data, characteristic):
    ctx = data['ctx']
    args = dict(data, characteristic=([characteristic[0]], [characteristic[1]]))
    assert ctx.almosteq(baker_akhiezer(data['reference'], **args), 1)
    u = ctx.mpc('.2', '.03')
    expected = independent_reference(ctx, u, data, characteristic)
    assert abs(baker_akhiezer([u], **args) - expected) < ctx.mpf('1e-31')


def test_reference_agrees_with_normalized_spectral_ratio_and_skips_sharp(data, monkeypatch):
    ctx = data['ctx']
    data['characteristic'] = ((.5,), (.5,))
    spectral = dict(data, normalization='spectral')
    spectral.pop('reference')
    u = [ctx.mpf('.2')]
    expected = baker_akhiezer(u, **spectral)/baker_akhiezer(data['reference'], **spectral)

    def unnecessary(*args, **kwargs):
        raise AssertionError('reference normalization must not compute a sharp factor or canonical scale')

    monkeypatch.setattr(implementation, '_kleinian_sigma_sharp', unnecessary)
    monkeypatch.setattr(implementation, '_hyperelliptic_sigma_normalization', unnecessary)
    assert ctx.almosteq(baker_akhiezer(u, **data), expected)


@pytest.mark.parametrize('u, reference, message', [
    (0, '.13', 'denominator'), ('.2', 0, 'reference denominator'),
    ('.2', '.4', 'reference numerator'),
])
def test_known_zero_normalizers_raise_without_a_numerical_cutoff(data, u, reference, message):
    ctx = data['ctx']
    args = dict(data, reference=[ctx.mpf(reference)], characteristic=((.5,), (.5,)))
    with pytest.raises(ZeroDivisionError, match=message):
        baker_akhiezer([ctx.mpf(u)], **args)
    # A genuinely small nonzero denominator remains evaluable.
    assert ctx.isfinite(baker_akhiezer([ctx.mpf('1e-25')], **dict(data, characteristic=((.5,), (.5,)))))


@pytest.mark.parametrize('override, message', [
    ({'normalization': 'unknown'}, 'normalization'),
    ({'reference': None}, 'requires reference'),
    ({'normalization': 'spectral'}, 'reference requires'),
    ({'reference': [1, 2]}, 'reference must have length'),
    ({'shift': None}, 'shift and second_kind'),
    ({'second_kind': None}, 'shift and second_kind'),
])
def test_reference_input_errors(data, override, message):
    with pytest.raises(ValueError, match=message):
        baker_akhiezer([.2], **dict(data, **override))


def test_even_characteristic_reference_origin_is_regular(data):
    args = dict(data, reference=[0], characteristic=((0,), (0,)))
    assert data['ctx'].almosteq(baker_akhiezer([0], **args), 1)


@pytest.mark.parametrize('characteristic', [(.5, .5), (0, 0), (.2, -.3)])
@pytest.mark.parametrize('argument', ['.2', '.4'])
def test_reference_jets_match_independent_jtheta_derivatives(data, characteristic, argument):
    ctx = data['ctx']
    u, direction = ctx.mpf(argument), ctx.mpc('.6', '.1')
    args = dict(data, characteristic=([characteristic[0]], [characteristic[1]]))
    jet = baker_akhiezer_jet([u], direction=[direction], order=3, **args)
    assert len(jet) == 4
    for n, value in enumerate(jet):
        expected = ctx.diff(lambda t: independent_reference(ctx, u+direction*t, data, characteristic), 0, n)
        assert ctx.isfinite(value)
        assert abs(value-expected) < ctx.mpf('1e-29') * max(1, abs(expected))
    if argument == '.4' and characteristic == (.5, .5):
        assert abs(jet[0]) < ctx.mpf('1e-30')
        assert all(abs(value) > ctx.mpf('.01') for value in jet[1:])


@pytest.mark.parametrize('argument', ['.2', '.4'])
def test_spectral_jets_match_independent_jtheta_derivatives(data, argument):
    ctx = data['ctx']
    u, direction = ctx.mpf(argument), ctx.mpf('-.7')
    args = dict(data, normalization='spectral', characteristic=((.5,), (.5,)))
    args.pop('reference')

    def spectral(t):
        # Canonical sigma'(0)=1; raw sigma=-theta1(pi*u) exp(kappa*u²/2).
        scale = -1/(ctx.pi*ctx.jtheta(1, 0, ctx.exp(-ctx.pi), derivative=1))
        sigma = lambda z: scale*independent_sigma(ctx, z)
        z, a, r = u+t*direction, data['shift'][0], data['second_kind'][0]
        return sigma(a-z)*ctx.exp(-r*z)/(sigma(a)*sigma(z))

    jet = baker_akhiezer_jet([u], direction=[direction], order=3, **args)
    for n, value in enumerate(jet):
        expected = ctx.diff(spectral, 0, n)
        assert abs(value-expected) < ctx.mpf('1e-29') * max(1, abs(expected))


def test_zero_direction_and_zero_order(data):
    ctx = data['ctx']
    jet = baker_akhiezer_jet([.2], direction=[0], order=3, **data)
    assert jet[0] == baker_akhiezer([.2], **data)
    assert jet[1:] == (ctx.zero,)*3
    assert baker_akhiezer_jet([.2], direction=[1], order=0, **data) == (jet[0],)


@pytest.mark.parametrize('direction, order, message', [
    ([1], -1, 'order'), ([1], 1.5, 'order'), ([1], True, 'order'),
    (None, 1, 'direction'), ([1, 2], 1, 'direction must have length'),
    ([mp.inf], 1, 'direction entries must be finite'),
])
def test_jet_input_errors(data, direction, order, message):
    with pytest.raises(ValueError, match=message):
        baker_akhiezer_jet([.2], direction=direction, order=order, **data)


def test_spectral_sharp_origin_is_singular(data):
    args = dict(data, shift=[0], normalization='spectral', characteristic=((.5,), (.5,)))
    args.pop('reference')
    with pytest.raises(ZeroDivisionError, match='sharp normalizer'):
        baker_akhiezer_jet([.2], direction=[1], order=3, **args)


@pytest.mark.parametrize('sign', [1, -1])
def test_reference_signed_shifts_and_rates(data, sign):
    ctx = data['ctx']
    args = dict(data, shift=[sign*data['shift'][0]], second_kind=[sign*data['second_kind'][0]],
                characteristic=((.5,), (.5,)))
    jet = baker_akhiezer_jet([ctx.mpf('.2')], direction=[1], order=3, **args)
    for n, actual in enumerate(jet):
        expected = ctx.diff(lambda t: independent_reference(ctx, ctx.mpf('.2')+t, args), 0, n)
        assert abs(actual-expected) < ctx.mpf('1e-29') * max(1, abs(expected))
