"""Least-squares straight line by Cramer's rule, shared by the lab checks."""


def line(xs, ys):
    """(slope, intercept) of the least-squares line through the points."""
    n, sx, sy = len(xs), sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    det = n * sxx - sx * sx
    return (n * sxy - sx * sy) / det, (sxx * sy - sx * sxy) / det
