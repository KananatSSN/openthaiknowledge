"""Small numerical tools shared by the TPhO 19 checks."""

from math import asin, sin

G, C, PARSEC = 6.67e-11, 3.00e8, 3.086e16
H_PLANCK = 6.63e-34


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


def golden_min(f, lo, hi, n=200):
    """The minimiser of a unimodal f on [lo, hi] by golden-section search."""
    r = (5**0.5 - 1) / 2
    a, b = lo, hi
    for _ in range(n):
        c, d = b - r * (b - a), a + r * (b - a)
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (a + b) / 2


def line(xs, ys):
    """(slope, intercept) of the least-squares line, by Cramer's rule."""
    n, sx, sy = len(xs), sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    det = n * sxx - sx * sx
    return (n * sxy - sx * sy) / det, (sxx * sy - sx * sxy) / det


def centred_line(xs, ys):
    """(slope, intercept) of the least-squares line about the means."""
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return slope, my - slope * mx


def sphere_deviation(offset, radius, index):
    """Exact deviation (rad) of a ray entering a sphere `offset` from its centre."""
    incidence = asin(offset / radius)
    refraction = asin(sin(incidence) / index)
    return 2 * (incidence - refraction)


def adiabatic_climb(t0, p0, p_top, mu=29.0e-3, g=9.81, gas=8.31, steps=20000):
    """(height, temperature) where dry air rising adiabatically reaches p_top,
    integrating dp = -rho g dz with T = T0 (p/p0)^(2/7)."""
    z, dp = 0.0, (p0 - p_top) / steps
    for i in range(steps):
        p = p0 - (i + 0.5) * dp
        t = t0 * (p / p0) ** (2 / 7)
        z += dp * gas * t / (p * mu * g)
    return z, t0 * (p_top / p0) ** (2 / 7)
