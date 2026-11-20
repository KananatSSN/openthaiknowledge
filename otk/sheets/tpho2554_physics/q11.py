"""Theory 2.6: with one tension T, m2 needs T(sin alpha + sin beta) = m2 w^2 L2 sin alpha and m1 needs T sin beta = m1 w^2 (L1 sin beta - L2 sin alpha); eliminating w^2 gives L2/L1 = m1 sin(beta)(sin alpha + sin beta)/(sin alpha [m1(sin alpha + sin beta) + m2 sin beta]) with cos(beta) = m1 cos(alpha)/(m1 + m2). Adapted: masses and alpha (degrees) vary; returns L2/L1."""

from math import acos, cos, radians, sin


def solve(m1=2.0, m2=1.0, alpha=30.0):
    a = radians(alpha)
    b = acos(m1 * cos(a) / (m1 + m2))
    sa, sb = sin(a), sin(b)
    return m1 * sb * (sa + sb) / (sa * (m1 * (sa + sb) + m2 * sb))


def check(m1=2.0, m2=1.0, alpha=30.0, g=9.8):
    # Fix L1 = 1 and search for the L2 at which one omega satisfies both masses.
    from otk.sheets.tpho2554_physics._spin import beta_sliding, bisect

    a = radians(alpha)
    b = beta_sliding(a, m1, m2)
    tension = (m1 + m2) * g / cos(a)
    sa, sb = sin(a), sin(b)

    def residual(L2):
        w2 = tension * (sa + sb) / (m2 * L2 * sa)
        return tension * sb - m1 * w2 * (sb - L2 * sa)

    return bisect(residual, 1e-9, sb / sa)


PARAMS = {"m1": 2.0, "m2": 1.0, "alpha": 30.0}
VARIANTS = [{"m1": 3.0}, {"m2": 2.0, "alpha": 20.0}, {"alpha": 45.0}]
ANSWER = 1.246462563779938
TOL = 1e-9
