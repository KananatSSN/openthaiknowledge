"""Small numerical tools shared by the TPhO 18 checks."""

G, M_SUN, R_SUN = 6.67e-11, 2.0e30, 7.0e8
K_B, M_P = 1.38e-23, 1.67e-27
E, H, C = 1.60e-19, 6.63e-34, 3.00e8
MU0 = 4e-7 * 3.141592653589793


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
