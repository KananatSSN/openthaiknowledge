"""Small numerical tools shared by the TPhO 13 checks."""


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
    """Solve a 3 x 3 linear system by Cramer's rule."""
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


def table(width, height, mu, wheel_behind=True, g=9.8):
    """(deceleration, dragging leg's N, wheel's N) per unit mass for the
    one-wheeled table sliding with its dragging leg behind or in front.

    Unknowns (a, N_leg, N_wheel): N_leg + N_wheel = g; mu N_leg = a; torques
    about the centre of mass (half-width w/2 to each leg, friction acting at
    depth h). With the wheel behind, the dragging leg leads; friction points
    backward, so its torque adds to the wheel's side."""
    s = 1 if wheel_behind else -1
    rows = [
        [0.0, 1.0, 1.0],
        [-1.0, mu, 0.0],
        [0.0, width / 2 - s * mu * height, -width / 2],
    ]
    return solve3(rows, [g, 0.0, 0.0])
