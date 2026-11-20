"""Shared Newton's-law model for problem 2: a string from a fixed point holds m2 part way down and m1 at its end; both turn about the vertical axis, upper string at alpha and lower string at beta to the vertical, m1 on the far side of the axis from m2. Angles in radians."""

from math import cos, sin, tan


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def beta_fixed(alpha, m1, m2):
    """Lower-string angle when m2 is tied at the midpoint (part 1).

    m1: T1 cos(beta) = m1 g and T1 sin(beta) = m1 w^2 (L/2)(sin beta - sin alpha);
    m2: T2 sin(alpha) + T1 sin(beta) = m2 w^2 (L/2) sin(alpha), T2 cos(alpha) = (m1 + m2) g.
    Eliminating w^2 leaves one equation in beta on (alpha, 90 degrees)."""
    def residual(beta):
        return (m1 + m2) * tan(alpha) + m1 * tan(beta) - m2 * tan(beta) * sin(alpha) / (sin(beta) - sin(alpha))

    eps = 1e-12
    return bisect(residual, alpha + eps, 1.5707963267948966 - 1e-9)


def beta_sliding(alpha, m1, m2):
    """Lower-string angle when m2 slides freely (part 2): one tension T in both
    parts, so T cos(beta) = m1 g and T cos(alpha) - T cos(beta) = m2 g."""
    return bisect(lambda beta: m1 * (cos(alpha) / cos(beta) - 1) - m2, 1e-12, 1.5707963267948966 - 1e-12)
