"""Shared ray model for problem 3: a ray entering a spherical drop at incidence theta, refracting to phi (sin theta = n sin phi), reflecting N times inside, leaves deviated from its original line by alpha = 2 pi - (N + 1)(pi - 2 phi) - 2 theta."""

from math import asin, pi, sin


def deviation(theta, n, N):
    phi = asin(sin(theta) / n)
    return 2 * pi - (N + 1) * (pi - 2 * phi) - 2 * theta


def stationary(n, N):
    """Incidence where d(alpha)/d(theta) = 0, by bisection on a central difference."""
    def slope(t):
        h = 1e-7
        return deviation(t + h, n, N) - deviation(t - h, n, N)

    lo, hi = 1e-6, pi / 2 - 1e-6
    s_lo = slope(lo)
    for _ in range(100):
        mid = (lo + hi) / 2
        if (slope(mid) > 0) == (s_lo > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
