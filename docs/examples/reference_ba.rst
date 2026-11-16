Reference-normalized BA derivatives at a zero
============================================================

Reference normalization fixes a Baker–Akhiezer value to one at a supplied
Jacobian argument :math:`u_0`. With shift :math:`A=A(P)` and compatible
second-kind vector :math:`R=R(P)`, it evaluates

.. math::

   B(u;u_0)=\frac{\sigma(A-u)\sigma(u_0)}
   {\sigma(u)\sigma(A-u_0)}\exp(-R^T(u-u_0)).

This is the spectral BA quotient :math:`\Psi(P,u)/\Psi(P,u_0)` on the common
regular domain of the two expressions; the underlying spectral convention is
described in [BEH2005]_, equation (3.3). The sharp factor and the constant
sigma scale cancel from this ratio.

On the elliptic curve :math:`y^2=4x^3-4x`, choose :math:`P=(2,\sqrt{24})`
and evaluate at :math:`u=A(P)`. The numerator vanishes there, while the
denominator is regular. The logarithmic derivative has a pole, but the
ordinary derivatives remain finite. Using canonical :math:`\sigma'(0)=1`
gives an independent first-derivative expression:

.. math::

   \left.\frac{dB}{du}\right|_{u=A}
   =-\frac{\sigma(u_0)}{\sigma(A)\sigma(A-u_0)}
     \exp(-R(A-u_0)).

``baker_akhiezer_jet`` returns a tuple containing the value and ordinary
derivatives along ``u + t*direction`` at ``t=0``. Its reference argument stays
fixed. For this genus-one example ``direction=[1]`` gives derivatives in ``u``.

.. literalinclude:: ../../examples/baker_akhiezer/reference_ba_demo.py
   :language: python
   :start-at: from mpmath import mp
   :end-at: return jet, residual

The same calculation is checked by the documentation:

.. doctest::

   >>> from examples.baker_akhiezer.reference_ba_demo import documentation_example
   >>> jet, residual = documentation_example()
   >>> abs(jet[0]) < 1e-24 and residual < 1e-24
   True

The calculation uses 30 decimal digits and enforces absolute tolerances of
:math:`10^{-24}` for the zero value and first-derivative residual. These are
checks at the selected point, rather than error bounds for arbitrary inputs.
The evaluator differentiates the quotient directly, dividing only by the
denominator. Reference and denominator zeros still require a different chart.

Run the complete example from a source checkout with::

   python -m examples.baker_akhiezer.reference_ba_demo
