"""Theory 2.4: along the x axis E_p peaks at x ~ +-0.39a with E_p,max ~ 5.866 ke^2/a, so a positron from far away needs (1/2) m_e v0^2 = E_p,max, v0 ~ 3.425 sqrt(ke^2/(m_e a)). Adapted: a in nm; returns v0 in m/s with ke^2 = 2.307e-28 J m and m_e = 9.109e-31 kg."""

from math import sqrt


def _energy(x):
    return 2 / sqrt((0.5 + x) ** 2 + 0.25) + 2 / sqrt((0.5 - x) ** 2 + 0.25)


def solve(side=0.1, ke2=2.307e-28, mass=9.109e-31):
    # Golden-section search for the barrier between the centre and x = a.
    lo, hi = 0.0, 1.0
    phi = (sqrt(5) - 1) / 2
    for _ in range(200):
        x1, x2 = hi - phi * (hi - lo), lo + phi * (hi - lo)
        if _energy(x1) > _energy(x2):
            hi = x2
        else:
            lo = x1
    peak = _energy((lo + hi) / 2)
    return sqrt(2 * peak * ke2 / (mass * side * 1e-9))


def check(side=0.1, ke2=2.307e-28, mass=9.109e-31):
    # Fire positrons from far along the axis at trial speeds (energy
    # bookkeeping against the highest point of a fine grid) and bisect on the
    # speed that just gets through.
    a = side * 1e-9
    grid = [-1 + 2 * k / 20000 for k in range(20001)]
    barrier = max(_energy(x) for x in grid) * ke2 / a
    start = _energy(-1e6) * ke2 / a

    def passes(v):
        return 0.5 * mass * v * v + start >= barrier

    lo, hi = 0.0, 1e9
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if passes(mid) else (mid, hi)
    return hi


PARAMS = {"side": 0.1, "ke2": 2.307e-28, "mass": 9.109e-31}
VARIANTS = [{"side": 0.05}, {"side": 1.0}, {"side": 0.3}]
ANSWER = 5450893.483286931
TOL = 1e-3
