"""Theory 2.2: vertically T1 cos(beta) = m1 g and T2 cos(alpha) = m2 g + T1 cos(beta), so the upper tension is T2 = (m1 + m2) g/cos(alpha) and the lower T1 = m1 g/cos(beta). Adapted: masses (kg) and angles (degrees) vary; returns T2 in newtons with g = 9.8."""

from math import cos, radians


def solve(m1=2.0, m2=1.0, alpha=30.0, beta=38.3, g=9.8):
    return (m1 + m2) * g / cos(radians(alpha))


def check(m1=2.0, m2=1.0, alpha=30.0, beta=38.3, g=9.8):
    # Lower string first, then the vertical balance at m2.
    lower = m1 * g / cos(radians(beta))
    return (m2 * g + lower * cos(radians(beta))) / cos(radians(alpha))


PARAMS = {"m1": 2.0, "m2": 1.0, "alpha": 30.0, "beta": 38.3, "g": 9.8}
VARIANTS = [{"m1": 3.0, "beta": 35.5}, {"alpha": 45.0, "beta": 68.0}, {"m2": 2.0, "beta": 48.3}]
ANSWER = 33.948195828349995
TOL = 1e-12
