"""Small numerical tools shared by the TPhO 16 checks."""


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


def cycle(p_a=10.0, v_a=0.4, ratio=5.0, t_a=400.0, t_min=300.0, steps=20000):
    """(work, heat in) of the triangle A -> B (isobaric) -> C (straight line) -> A
    (isochoric) for a monatomic ideal gas, integrating dQ = (5/2)p dV + (3/2)V dp
    along each side and adding only the positive parts. Pressures in atm, volumes
    in litres; returns joules."""
    atm, litre = 1.013e5, 1e-3
    p_c = p_a * t_min / t_a
    corners = [(p_a, v_a), (p_a, ratio * v_a), (p_c, v_a), (p_a, v_a)]
    work = heat_in = 0.0
    for (p0, v0), (p1, v1) in zip(corners, corners[1:]):
        for i in range(steps):
            pa, va = p0 + (p1 - p0) * i / steps, v0 + (v1 - v0) * i / steps
            pb, vb = p0 + (p1 - p0) * (i + 1) / steps, v0 + (v1 - v0) * (i + 1) / steps
            p, v = (pa + pb) / 2, (va + vb) / 2
            dv, dp = (vb - va) * litre, (pb - pa) * atm
            work += p * atm * dv
            dq = 2.5 * p * atm * dv + 1.5 * v * litre * dp
            if dq > 0:
                heat_in += dq
    return work, heat_in
