"""Theory 2.5 figure: when m2 slides freely the two parts share one tension, so T cos(beta) = m1 g and T cos(alpha) = (m1 + m2) g give cos(beta) = m1 cos(alpha)/(m1 + m2). Adapted: masses and alpha (degrees) vary; returns beta in degrees."""

from math import acos, cos, degrees, radians


def solve(m1=2.0, m2=1.0, alpha=30.0):
    return degrees(acos(m1 * cos(radians(alpha)) / (m1 + m2)))


def check(m1=2.0, m2=1.0, alpha=30.0):
    from otk.sheets.tpho2554_physics._spin import beta_sliding

    return degrees(beta_sliding(radians(alpha), m1, m2))


PARAMS = {"m1": 2.0, "m2": 1.0, "alpha": 30.0}
VARIANTS = [{"m1": 3.0}, {"m2": 2.0, "alpha": 20.0}, {"alpha": 45.0}]
ANSWER = 54.735610317245346
TOL = 1e-9
