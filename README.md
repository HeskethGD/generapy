# Generapy

<img src="https://raw.githubusercontent.com/HeskethGD/generapy/main/docs/_static/generapy-logo.png" alt="Generapy logo: a curved, gridded letter g in teal and gold" width="220">

Generapy is an early-stage numeric Python package for arbitrary-precision computation
with algebraic curves and Abelian functions, particularly for applications in
integrable systems.

Generapy uses [mpmath](https://mpmath.org/) for arbitrary-precision arithmetic.
It is an independent project and does not modify the mpmath namespace.
Generapy retains the applicable BSD-3-Clause copyright and licence notice.

## Installation

Install from PyPI:

```sh
pip install generapy
```

Requires Python 3.11 or later.

**Documentation:** https://generapy.readthedocs.io/en/latest/

## Quick Example

For example, verify Baker's genus-two addition formula using Kleinian sigma
and P functions at arbitrary Abelian arguments. The identity is from
H. F. Baker, *An Introduction to the Theory of Multiply Periodic Functions*
(Cambridge University Press, 1907), Chapter V, p. 100
([digitized edition](https://books.google.com/books?id=0EQLAAAAYAAJ&pg=PA100)):

```python
from mpmath import mp

from generapy import Curve
from generapy import kleinian_sigma as ks
from generapy import kleinian_p as kp

mp.dps = 30

# y² = 4x(x² - 1)(x² - 4) = 4x⁵ - 20x³ + 16x
polynomial = {(0, 2): 1, (5, 0): -4, (3, 0): 20, (1, 0): -16}
curve = Curve(polynomial)

u = mp.matrix([mp.mpf("0.3"), mp.mpf("0.2")])
v = mp.matrix([mp.mpf("0.1"), mp.mpf("0.4")])

lhs = ks(u + v, curve=curve) * ks(u - v, curve=curve) / (
    ks(u, curve=curve)**2 * ks(v, curve=curve)**2)

# Baker's indices are one-based; Generapy's indices are zero-based.
p11_u, p12_u, p22_u = kp(u, curve=curve, indices=((0, 0), (0, 1), (1, 1)))
p11_v, p12_v, p22_v = kp(v, curve=curve, indices=((0, 0), (0, 1), (1, 1)))
rhs = p22_u * p12_v - p12_u * p22_v + p11_v - p11_u

print(mp.nstr(abs(rhs - lhs), 6))  # 6.31089e-29
```

The curve supplies the period data and canonical hyperelliptic sigma
normalization automatically. See the [example walkthrough](https://generapy.readthedocs.io/en/latest/examples/baker_formula.html)
for the identity and conventions, or run the
[complete example](https://github.com/HeskethGD/generapy/blob/main/examples/baker_formula/baker_formula_demo.py).

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
developer setup, checks and contribution workflow.

## Examples

Literature-based numerical examples live in the repository's `examples/`
directory. They are not installed as part of the `generapy` package and do
not require plotting libraries. Run them from a source checkout, for example:

```sh
python -m examples.manakov.manakov_kleinian_demo
```

The dynamics examples compare their Abelian-function solutions against a
shared arbitrary-precision Runge--Kutta implementation. Lightweight versions
of the examples run in the test suite to keep the published workflows valid.
