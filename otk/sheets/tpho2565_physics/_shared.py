"""Small numerical tools shared by the TPhO 21 checks."""

from math import log, pi

EPS0 = 8.854e-12
COULOMB = 1 / (4 * pi * EPS0)
BOHR, BOLTZMANN, MU0 = 9.274e-24, 1.38e-23, 4e-7 * pi


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


def two_level_entropy(x):
    """S/(N k_B) of two-level spins at x = mu B/(k_B T), from the probabilities."""
    up = 1 / (1 + pow(2.718281828459045, -2 * x))
    down = 1 - up
    return -sum(p * log(p) for p in (up, down) if p > 0)
