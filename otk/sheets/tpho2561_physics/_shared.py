"""Small numerical tools shared by the TPhO 17 checks."""


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


def solve3(rows, rhs):
    """3 x 3 linear system by Cramer's rule."""
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    d = det(rows)
    out = []
    for j in range(3):
        m = [r[:] for r in rows]
        for i in range(3):
            m[i][j] = rhs[i]
        out.append(det(m) / d)
    return out


def falling_rod(angle, g=9.8, length=1.0, mass=1.0):
    """(a_cm, alpha, N) for a rod released at rest with end A on a smooth floor:
    M a = M g - N, I alpha = N (L/2) cos(theta), a = (L/2) cos(theta) alpha."""
    from math import cos

    c = cos(angle)
    rows = [[mass, 0.0, 1.0], [0.0, mass * length**2 / 12, -length / 2 * c], [1.0, -length / 2 * c, 0.0]]
    return solve3(rows, [mass * g, 0.0, 0.0])
