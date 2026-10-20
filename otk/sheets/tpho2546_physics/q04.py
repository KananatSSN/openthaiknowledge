"""Theory 1.3: m leaves the surface when N = 0 in the cylinder's frame, m v^2/R = mg cos theta - N - m (dV/dt) sin theta; with the cylinder free (finite M) that is at a smaller angle than cos^-1(2/3), the angle for a fixed cylinder. Adapted: returns 'smaller', 'larger' or 'equal' against cos^-1(2/3); mass_ratio = M/m, 0 for a fixed cylinder."""

from math import acos, cos, sin, sqrt


def _speeds(t, mass_ratio):
    big, small = mass_ratio, 1.0
    c, s = cos(t), sin(t)
    v = sqrt(2 * (big + small) * (1 - c) / (big + small * s * s))  # g = R = 1
    return v, small * v * c / (big + small)


def _compare(theta):
    fixed = acos(2 / 3)
    if abs(theta - fixed) < 1e-6:
        return "equal"
    return "smaller" if theta < fixed else "larger"


def solve(mass_ratio=4):
    if mass_ratio == 0:
        return _compare(acos(2 / 3))
    # Bisect N(theta) = cos theta - A sin theta - v^2 (g = R = 1), with
    # A = dV/dt = (dV/dtheta)(v/R).
    def normal(t):
        v, _ = _speeds(t, mass_ratio)
        h = 1e-7
        dV = (_speeds(t + h, mass_ratio)[1] - _speeds(t - h, mass_ratio)[1]) / (2 * h)
        return cos(t) - dV * v * sin(t) - v * v

    lo, hi = 1e-3, 1.5
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if normal(mid) > 0 else (lo, mid)
    return _compare(lo)


def check(mass_ratio=4):
    # Ground frame: the only horizontal force on the cylinder is the push
    # N sin theta, so contact ends where the cylinder's speed V stops growing.
    if mass_ratio == 0:
        v2 = lambda t: 2 * (1 - cos(t))  # noqa: E731
        lo, hi = 1e-3, 1.5
        for _ in range(80):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if cos(mid) - v2(mid) > 0 else (lo, mid)
        return _compare(lo)
    a, b = 1e-3, 1.5
    phi = (sqrt(5) - 1) / 2
    for _ in range(200):
        x1, x2 = b - phi * (b - a), a + phi * (b - a)
        if _speeds(x1, mass_ratio)[1] > _speeds(x2, mass_ratio)[1]:
            b = x2
        else:
            a = x1
    return _compare((a + b) / 2)


PARAMS = {"mass_ratio": 4}
VARIANTS = [{"mass_ratio": 0}, {"mass_ratio": 1}, {"mass_ratio": 50}]
ANSWER = 'smaller'
