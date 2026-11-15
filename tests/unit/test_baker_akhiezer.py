"""Reference BA normalization and ordinary derivatives use literal arguments."""

import pytest
from mpmath import mp

from generapy import baker_akhiezer
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
    return (ctx.exp(ctx.mpf('.12')*z*z/2 + ctx.pi*ctx.j*a*a + 2*ctx.pi*ctx.j*a*(z+b))
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
