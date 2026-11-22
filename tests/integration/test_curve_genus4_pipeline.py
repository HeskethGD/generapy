"""The issue #33 quintic retains its marked periods after coarser lifting."""

import pytest
from mpmath import mp

from generapy import Curve
from tests.unit.test_curve_polynomial import QUINTIC


# Independent 30-digit snapshot from the previous, fine-mesh pipeline.
REFERENCE_TAU = [['(1.20702046184892687045466069178 + 1.59984724157783029013486450952j)',
  '(-0.412521163955896534015968104405 - 0.556568714161959294593704694093j)',
  '(-0.707020461848926870454660691785 - 0.119358422988621732851128387756j)',
  '(0.00547589761327177462021282466482 - 0.206874742286633529807059202971j)'],
 ['(-0.412521163955896534015968104405 - 0.556568714161959294593704694093j)',
  '(0.5 + 0.858121130656955306524029548734j)',
  '(0.825042327911793068031936208809 + 5.69336520146534641830984815238e-33j)',
  '(-0.0874788360441034659840318955953 - 0.0319320121699380407644740784937j)'],
 ['(-0.707020461848926870454660691785 - 0.119358422988621732851128387756j)',
  '(0.825042327911793068031936208809 + 5.69336520146534641830984815238e-33j)',
  '(-2.02877908347422727092887969713e-33 + 0.238716845977243465702256775511j)',
  '(0.282027742924529580304913658886 + 0.119358422988621732851128387756j)'],
 ['(0.00547589761327177462021282466482 - 0.206874742286633529807059202971j)',
  '(-0.0874788360441034659840318955953 - 0.0319320121699380407644740784937j)',
  '(0.282027742924529580304913658886 + 0.119358422988621732851128387756j)',
  '(0.282027742924529580304913658886 + 1.75618803000824135585219746125j)']]


@pytest.mark.parametrize('digits', [20, 30])
def test_genus_four_coarse_cover_preserves_periods_and_precision(digits):
    ctx = mp.clone()
    ctx.dps = digits
    terms = {(j, i): ctx.mpf(p)/q for (i, j), (p, q) in QUINTIC.items()}

    def fy(x, y):
        return ctx.fsum(c*j*x**i*y**(j-1) for (i, j), c in terms.items() if j)

    forms = (lambda x, y: 1/fy(x, y), lambda x, y: y/fy(x, y),
             lambda x, y: x/fy(x, y), lambda x, y: (y*y-x*x)/fy(x, y))
    curve = Curve(terms, differentials_kind_1=forms, ctx=ctx)
    periods = curve.periods_kind_1()
    expected = ctx.matrix([[ctx.mpc(v) for v in row] for row in REFERENCE_TAU])
    assert periods.genus == 4
    assert ctx.norm(periods.tau-expected) < 10000*ctx.eps*max(1, ctx.norm(expected))
    assert min(periods.imaginary_eigenvalues) > 0
    assert ctx.dps == digits
