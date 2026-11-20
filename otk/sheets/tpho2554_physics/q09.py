"""Theory 2.4: for small angles the 2.3 relation becomes (m1/(m1 + m2)) beta^2 = alpha^2, so beta = alpha sqrt((m1 + m2)/m1). Adapted: masses and the small upper angle (degrees) vary; degrees."""

from math import sqrt


def solve(m1=2.0, m2=1.0, alpha=2.0):
    return alpha * sqrt((m1 + m2) / m1)


def check(m1=2.0, m2=1.0, alpha=2.0):
    # Newton's laws at a tiny angle, scaled up linearly.
    from math import degrees, radians

    from otk.sheets.tpho2554_physics._spin import beta_fixed

    tiny = radians(1e-3)
    return degrees(beta_fixed(tiny, m1, m2)) / 1e-3 * alpha


PARAMS = {"m1": 2.0, "m2": 1.0, "alpha": 2.0}
VARIANTS = [{"m1": 1.0}, {"m2": 3.0, "alpha": 3.0}, {"alpha": 1.5}]
ANSWER = 2.449489742783178
TOL = 1e-6
