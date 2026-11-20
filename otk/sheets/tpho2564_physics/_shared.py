"""Small numerical tools shared by the TPhO 20 checks."""

from math import cos, pi, sin

EPS0, CHARGE, ELECTRON = 8.854e-12, 1.602e-19, 9.109e-31
HALF_DISC = 4 / (3 * pi)  # centre of mass of a half disc, in radii


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


def rolling_inertia(turn, tube, half, radius, k=HALF_DISC):
    """Moment of inertia about the contact point of a thin tube (mass `tube`)
    welded to a half cylinder (mass `half`) whose centre of mass sits k R from
    the axis, `turn` radians from straight down."""
    r = radius
    tube_part = 2 * tube * r * r
    # the half cylinder: I about its own cm, plus m times its distance to the contact
    own = 0.5 * half * r * r - half * (k * r) ** 2
    dx, dy = k * r * sin(turn), r - k * r * cos(turn)
    return tube_part + own + half * (dx * dx + dy * dy)


def alpha_for(current, side):
    """alpha in V'' = alpha/sqrt(V) for a current through plates of side `side` (m)."""
    return current / (EPS0 * side * side) * (ELECTRON / (2 * CHARGE)) ** 0.5


def gap_for(current, volts, side, steps=4000):
    """The distance over which the space-charge potential rises from 0 to `volts`:
    (V')^2 = 4 alpha sqrt(V), so dx = dV/(2 sqrt(alpha) V^(1/4)); with V = u^4,
    dx = 2 u^2 du/sqrt(alpha), summed by the midpoint rule."""
    alpha = alpha_for(current, side)
    top = volts**0.25
    du = top / steps
    return sum(2 * ((i + 0.5) * du) ** 2 * du for i in range(steps)) / alpha**0.5
