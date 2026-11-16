"""Shared deterministic controls and the standalone issue #17 fixture."""

from .benchmark_rtheta_implementations import CASES


ISSUE17_TAU = (
    (('.5061827897506581', '.31172905255754557'), ('.6030229299594175', '-.04359505958080551'), ('-.3101196265653908', '-.06326260427442727')),
    (('.6030229299594175', '-.04359505958080551'), ('-.028249856592070074', '.8375139200826641'), ('-.11881417648110583', '-.4622511800480431')),
    (('-.3101196265653908', '-.06326260427442727'), ('-.11881417648110583', '-.4622511800480431'), ('.598971866744514', '.8569930428687905')),
)
ISSUE17_Z = (('.08349057041152029', '.272628770125157'),
             ('-.7846449196406094', '-.3896019731779659'),
             ('.2820346235628105', '.03848614663265641'))


def cases(ctx):
    """Return exact-decimal inputs with coupled, shifted and higher-genus cases."""
    result = []
    for case in CASES:
        tau = tuple(tuple(ctx.mpc(*v) for v in row) for row in case['tau'])
        for i, z in enumerate(case['zs']):
            genus = len(z)
            characteristic = ((ctx.mpf('.5'),)*genus, (ctx.zero,)*genus)
            result.append((case['name'] + ('-shifted' if i else ''), tau,
                           tuple(ctx.mpc(*v) for v in z), characteristic))
    result.append(('issue17', tuple(tuple(ctx.mpc(*v) for v in row) for row in ISSUE17_TAU),
                   tuple(ctx.mpc(*v) for v in ISSUE17_Z),
                   ((ctx.mpf('.5'), ctx.mpf('.5'), ctx.zero),
                    (ctx.zero, ctx.mpf('.5'), ctx.mpf('.5')))))
    for genus, damping in ((4, '1.4'), (5, '3')):
        tau = tuple(tuple(ctx.mpc(ctx.mpf(i % 3)/20, ctx.mpf(damping)+ctx.mpf(i % 4)/10)
                          if i == j else ctx.mpc('.02', '.15') if abs(i-j) == 1 else ctx.zero
                          for j in range(genus)) for i in range(genus))
        result.append((f'g{genus}-coupled', tau, tuple(ctx.mpc('.13', '.02') for _ in range(genus)),
                       ((ctx.zero,)*genus, (ctx.zero,)*genus)))
    return result
