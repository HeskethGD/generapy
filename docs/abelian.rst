Abelian functions
-----------------

Riemann theta functions generalize the Jacobi theta functions from one
complex variable to several. They arose in Riemann's theory of Abelian
functions and compact Riemann surfaces and are fundamental in complex
analysis, algebraic geometry, and integrable systems.

Theta functions are quasiperiodic. For integer vectors
:math:`m,n\in\mathbb Z^g`, the zero-characteristic function satisfies

.. math::

   \theta(z+m+\tau n\mid\tau)
   = \exp\!\left(-\pi i n^T\tau n-2\pi i n^Tz\right)\theta(z\mid\tau).

Suitable ratios and combinations are multiply-periodic Abelian functions. In
genus two these are meromorphic functions of two complex variables with a
rank-four period lattice. Kleinian sigma, zeta, and P-functions extend the
Weierstrass functions to higher genus.

Riemann theta functions
.......................

The :ref:`Bobenko theta calculation <bobenko-theta-example>` uses ``rtheta``
for characteristic-dependent theta quotients and ``rtheta_jet`` for their
derivatives along the flow.

.. autofunction:: generapy.rtheta

The following plots show two real slices and the modulus over two real
variables for genus-two period matrices. Similar slices and surfaces are
illustrated in `DLMF section 21.4 <https://dlmf.nist.gov/21.4>`_.

.. plot::

   import matplotlib.pyplot as plt
   from mpmath import j, plot, re
   from generapy import rtheta

   tau = [[j, -0.5], [-0.5, j]]
   curves = [
       lambda x: re(rtheta([x, x/2], tau)),
       lambda x: re(rtheta([x, 2*x], tau)),
   ]
   fig, ax = plt.subplots()
   plot(curves, [-2, 2], axes=ax)
   # mpmath supplies its own styles; distinguish slices without colour.
   for line, style in zip(ax.lines, ("-", "--")):
       line.set_color("#015758")
       line.set_linestyle(style)
   ax.legend([r"$z=(x,x/2)$", r"$z=(x,2x)$"])

.. plot::

   import matplotlib.pyplot as plt
   from mpmath import j, splot
   from generapy import rtheta

   tau = [[j, 0.5], [0.5, j]]
   fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
   surface = lambda x, y: abs(rtheta([x, y], tau))
   splot(surface, [-1, 1], [-1, 1], points=35, keep_aspect=False,
         axes=ax, plot3d_kwargs={"color": "#015758"})
   ax.set_zlabel(r"$|\theta(z\mid\tau)|$")

.. autofunction:: generapy.rtheta_jet

For derivatives along a single direction, ``rtheta_directional_jet`` returns
only the requested ordinary derivatives, including the value. For example::

   from generapy import rtheta_directional_jet

   theta_jet = rtheta_directional_jet([0.1, 0.2], [[1j, 0], [0, 1j]],
                                     direction=[1, -0.5], order=3)

.. autofunction:: generapy.rtheta_directional_jet

Curve data for Kleinian functions
.................................

Curve construction, homology markings, period matrices, Riemann constants,
and Abel maps are documented in :doc:`algebraic_curves`. For a recognized
hyperelliptic curve, the functions accept the curve directly::

   polynomial = {(0, 2): 1, (1, 0): 4, (3, 0): -4}
   curve = Curve(polynomial=polynomial)
   value = kleinian_sigma([0.2], curve=curve)
   wp = kleinian_p([0.2], indices=(0, 0), curve=polynomial)

A sparse mapping is sufficient for automatic bases. A ``Curve`` also carries
custom bases and its numerical context. Point-independent setup is cached by
context and precision for repeated evaluations. The specialist route accepts
``omega``, ``tau``, ``kappa``, and ``characteristic`` explicitly; all must refer
to the same basis and homology marking. Curve and explicit period inputs cannot
be mixed.
The optional ``ctx`` argument uses the same convention throughout Generapy;
see the :ref:`Curve constructor examples <numerical-contexts>` for an
independent-precision example.

The :ref:`custom-differential-bases` guide covers custom first-kind sequences
and compatible second-kind forms. These are bound to ``Curve`` at construction;
its period, Riemann-constant, and Abel-map methods use the same bases automatically.
The Abel vector, ``omega``, ``kappa``, and P-function indices all refer to
that ordered basis. A change of basis or second-kind convention changes the
meaning of these inputs. In particular, the hyperelliptic sigma normalization
assumes the automatic differential ordering and scaling; it is not a general
normalizer for arbitrary custom bases.

The :ref:`Manakov example <manakov-period-data>` constructs and reuses these
inputs for a hyperelliptic curve; the :ref:`Bernatska example <bernatska-custom-bases>`
uses explicit first- and second-kind differential bases on a trigonal curve.


Kleinian functions
..................

The Kleinian functions use unnormalized Abelian coordinates ``u``. Their
period data are the first-kind half-period matrix ``omega``, the normalized
Riemann matrix ``tau``, and the symmetric matrix ``kappa``. The convention is

.. math::

   \begin{aligned}
   \tau&=\omega^{-1}\omega',\\
   v&=(2\omega)^{-1}u.
   \end{aligned}

The characteristic uses the same literal convention as :func:`generapy.rtheta`.
The explicit-period route retains the zero-characteristic default; curve-based
calls derive the curve's Riemann characteristic.
Curve-based sigma calls automatically select hyperelliptic normalization for
the automatic hyperelliptic basis, and theta scaling (multiplier one) otherwise.
Explicit-period calls default to theta scaling; ``normalization="hyperelliptic"``
selects the hyperelliptic convention when those inputs use its basis and
characteristic. Other curves currently require compatible second-kind forms
bound to ``Curve``; automatic second-kind construction and Schur normalization
for general ``(n,s)`` curves are not yet available.

``kleinian_sigma_normalization`` returns the scalar multiplier independently.
It requires no second-kind matrix. For example, in genus one its result makes
the first derivative at the origin equal to one::

   C = kleinian_sigma_normalization(curve=curve)
   raw = kleinian_sigma_jet([0], curve=curve, order=1,
                           normalization="theta")
   normalized_derivative = C * raw[(1,)]

Zeta and P-functions are independent of this multiplier and do not calculate it.

The :doc:`Baker formula example <examples/baker_formula>` verifies the
genus-two addition identity relating sigma ratios to Kleinian P functions.

The :ref:`Ônishi sigma calculation <onishi-sigma-example>` uses
``kleinian_sigma`` and ``kleinian_sigma_jet`` on Abel images, including
derivatives where sigma itself vanishes. The
:ref:`Manakov solution <manakov-kleinian-example>` uses batched
``kleinian_p`` evaluations to reconstruct amplitudes and momenta.

.. autofunction:: generapy.kleinian_sigma_normalization

.. autofunction:: generapy.kleinian_sigma

.. autofunction:: generapy.kleinian_sigma_jet

``kleinian_sigma_directional_jet`` evaluates derivatives along :math:`u+t\,d`
using the same curve, period and normalization conventions as sigma. Its tuple
contains ordinary derivatives from order zero through the requested order::

   from generapy import kleinian_sigma_directional_jet

   jet = kleinian_sigma_directional_jet([0.2], curve=curve,
                                        direction=[1], order=3)

.. autofunction:: generapy.kleinian_sigma_directional_jet

.. autofunction:: generapy.kleinian_zeta

.. autofunction:: generapy.kleinian_p

Baker–Akhiezer functions
........................

Baker–Akhiezer functions are functions on algebraic curves with prescribed
poles and exponential behavior, used to construct spectral eigenfunctions
and finite-gap solutions of integrable equations [Krichever1977]_. Their
sigma-function representation builds on classical Abelian function theory;
see [Baker1907]_.

Generapy supports hyperelliptic spectral normalization (the default) and
reference normalization, which sets the value at a chosen argument to one.
Both support ordinary directional derivatives.

**A hyperelliptic spectral value.** Supply a curve and a spectral point
:math:`P=(x,y)` on it. Here ``normalization="spectral"`` is shown explicitly;
it can be omitted::

   from mpmath import mp
   from generapy import Curve, baker_akhiezer, baker_akhiezer_jet

   mp.dps = 30
   curve = Curve({(0, 2): 1, (3, 0): -4, (1, 0): 4})
   point = (2, mp.sqrt(24))
   u = [mp.mpf('0.3')]
   value = baker_akhiezer(u, curve=curve, point=point,
                          normalization="spectral")

**A reference-normalized value.** Select ``normalization="reference"`` and
provide the argument ``reference=u0`` where the function should equal one::

   u0 = [mp.mpf('0.2')]
   value = baker_akhiezer(u, curve=curve, point=point,
                          normalization="reference", reference=u0)

**Using supplied Abel integrals.** If the Abel shift :math:`A(P)` and
second-kind vector :math:`R(P)` are already available, pass their vectors
as ``shift`` and ``second_kind`` instead of ``point``. The curve still
supplies the period data in this example::

   shift = curve.abel_map_kind_1(point).value
   second_kind = curve.abel_map_kind_2(point).value
   value = baker_akhiezer(u, curve=curve, shift=shift, second_kind=second_kind,
                          normalization="reference", reference=u0)

**Directional derivatives.** Request the value and derivatives through order
three along :math:`u+t\,d`, with the reference argument held fixed::

   jet = baker_akhiezer_jet(u, curve=curve, point=point,
                           normalization="reference", reference=u0,
                           direction=[1], order=3)

The :doc:`genus-two spectral example <examples/baker_akhiezer>` checks the
product on opposite sheets. The :doc:`reference derivative example
<examples/reference_ba>` evaluates a BA zero with a finite, nonzero first
derivative. Formulas, data conventions and parameter requirements follow.

.. autofunction:: generapy.baker_akhiezer

.. autofunction:: generapy.baker_akhiezer_jet

For the classical development of Abelian, theta, sigma, and multiply periodic
functions, see [Baker1907]_, [BEL1997]_, [CEEK2000]_, [Onishi2005]_,
and the references therein.
