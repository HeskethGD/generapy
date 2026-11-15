Baker–Akhiezer functions on opposite sheets
============================================================

For the genus-two curve
:math:`y^2=4x^5+\lambda_4x^4+\cdots+\lambda_0`, the normalized
Baker–Akhiezer functions on opposite sheets satisfy [BEH2005]_,
equations (3.3) and (3.8),

.. math::

   \Psi((x,y),u)\Psi((x,-y),u)
   = x^2-\wp_{22}(u)x-\wp_{12}(u).

The right side is the Bolza polynomial. The argument :math:`u\in\mathbb C^2`
is free, with :math:`\sigma(u)\ne0`; it need not be the Abel image of a
single point. The spectral points :math:`(x,\pm y)` must lie on the curve
and have nonzero sharp normalizers.

We use :math:`y^2=4x(x^2-1)(x^2-4)`, :math:`x=3` and
:math:`u=(0.13,0.27)`. The automatic basis is
:math:`(dx/y,x\,dx/y)`, with the unique point at infinity as the Abel origin.
For this ordering, the sharp factor is :math:`\sigma_2(A(P))`, where the
subscript uses the paper's one-based coordinates. Generapy's P-function
indices are zero-based.

Passing the same ``Curve`` to both BA calls supplies the periods,
characteristic, canonical sigma scale and compatible first-/second-kind
integrals. The exponent uses the BEL sign convention described in
:func:`generapy.kleinian_baker_akhiezer`. Both sheet calls use unreduced
infinity-based lifts.

.. literalinclude:: ../../examples/baker_akhiezer/baker_akhiezer_demo.py
   :language: python
   :start-at: from mpmath import mp
   :end-at: return product, bolza, residual

The documentation checks the same runnable calculation:

.. doctest::

   >>> from examples.baker_akhiezer.baker_akhiezer_demo import documentation_example
   >>> product, bolza, residual = documentation_example()
   >>> residual < 1e-24
   True

The script uses 30 decimal digits and checks an absolute residual below
:math:`10^{-24}` at these arguments. This tests the sigma normalization,
sharp factors and sheet product against a separately evaluated P-function
expression. It is a sampled identity check, rather than an error bound for
arbitrary inputs. This example covers the odd-degree hyperelliptic evaluator;
it does not construct BA functions on general curves.

Run the complete example from a source checkout with::

   python -m examples.baker_akhiezer.baker_akhiezer_demo
