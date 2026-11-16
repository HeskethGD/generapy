"""Reference-normalized BA derivatives through a numerator zero.

Run: python -m examples.baker_akhiezer.reference_ba_demo
"""

from mpmath import mp

from generapy import Curve, baker_akhiezer_jet, kleinian_sigma


def documentation_example():
    """Return the ordinary jet and the independent first-derivative residual."""
    with mp.workdps(30):
        curve = Curve({(0, 2): 1, (3, 0): -4, (1, 0): 4})
        point = (mp.mpf(2), mp.sqrt(24))
        shift = curve.abel_map_kind_1(point).value[0]
        r = curve.abel_map_kind_2(point).value[0]
        reference = mp.mpf('.2')
        jet = baker_akhiezer_jet(
            [shift], curve=curve, point=point, direction=[1], order=3,
            normalization='reference', reference=[reference])

        # At u=A the numerator is sigma(0)=0. Canonical genus-one sigma'(0)=1
        # gives this first derivative directly, without a logarithmic quotient.
        sigma = lambda u: kleinian_sigma([u], curve=curve)
        expected_first = (-mp.exp(-r*(shift-reference))*sigma(reference)
                          / (sigma(shift)*sigma(shift-reference)))
        residual = abs(jet[1]-expected_first)
        assert all(mp.isfinite(v) for v in jet)
        assert abs(jet[0]) < mp.mpf('1e-24')
        assert abs(jet[1]) > mp.mpf('1e-5')
        assert residual < mp.mpf('1e-24')
        return jet, residual


if __name__ == '__main__':
    jet, residual = documentation_example()
    print('Value and ordinary derivatives:', tuple(mp.nstr(v, 12) for v in jet))
    print('First-derivative absolute residual:', mp.nstr(residual, 6))
