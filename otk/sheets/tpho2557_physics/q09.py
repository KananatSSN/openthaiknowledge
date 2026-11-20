"""Theory 3.1 (f): the front compresses (Delta V/V0 = u/(v + u)) under Delta P = rho (v + u) u, so B = Delta P V0/Delta V = rho (v + u)^2 and, for v >> u, v = sqrt(B/rho), the speed of sound in water. Adapted: B (GPa) varies; returns v in m/s with rho = 1000."""

from math import sqrt


def solve(bulk=2.2):
    return sqrt(bulk * 1e9 / 1000)


def check(bulk=2.2):
    # Solve rho (v + u) u = B u/(v + u) for v with a tiny inflow u, by bisection.
    from otk.sheets.tpho2557_physics._shared import bisect

    u = 1e-9
    return bisect(lambda v: 1000 * (v + u) * u - bulk * 1e9 * u / (v + u), 1.0, 1e5)


PARAMS = {"bulk": 2.2}
VARIANTS = [{"bulk": 2.0}, {"bulk": 2.4}, {"bulk": 1.5}]
ANSWER = 1483.2396974191327
TOL = 1e-9
