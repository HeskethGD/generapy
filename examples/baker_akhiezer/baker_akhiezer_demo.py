"""Check the genus-two Baker–Akhiezer sheet-product identity.

Run with: python -m examples.baker_akhiezer.baker_akhiezer_demo
"""

from mpmath import mp

from generapy import Curve, kleinian_baker_akhiezer, kleinian_p


def documentation_example():
    """Return the sheet product, Bolza polynomial and absolute residual."""
    with mp.workdps(30):
        # y² = 4x(x² - 1)(x² - 4); du = (dx/y, x dx/y).
        curve = Curve({(0, 2): 1, (5, 0): -4, (3, 0): 20, (1, 0): -16})
        u = [mp.mpf('0.13'), mp.mpf('0.27')]
        x = mp.mpf(3)
        y = mp.sqrt(4*x*(x*x-1)*(x*x-4))
        psi_plus = kleinian_baker_akhiezer(u, curve=curve, target=(x, y))
        psi_minus = kleinian_baker_akhiezer(u, curve=curve, target=(x, -y))
        product = psi_plus * psi_minus

        # Braden, Enolskii & Hone (2005), equations (3.3) and (3.8).
        # Their wp_22 and wp_12 use one-based indices.
        wp22, wp12 = kleinian_p(u, curve=curve, indices=((1, 1), (0, 1)))
        bolza = x*x - wp22*x - wp12
        residual = abs(product - bolza)
        assert residual < mp.mpf('1e-24'), 'BA sheet-product identity failed'
        return product, bolza, residual


if __name__ == '__main__':
    product, bolza, residual = documentation_example()
    print('BA sheet product:', mp.nstr(product, 12))
    print('Bolza polynomial:', mp.nstr(bolza, 12))
    print('Absolute residual:', mp.nstr(residual, 6))
