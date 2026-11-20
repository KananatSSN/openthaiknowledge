"""Theory 1.6-1.7: at a circular jump with H >> h the momentum balance per unit rim length is rho h v^2 = (1/2) rho g H^2, so H^2 = 2 h v^2/g; the thin layer keeps the jet speed v = 4Q/(pi d^2) and Q = 2 pi R h v, giving R = 4Q^2/(pi^2 d^2 g H^2). Adapted: the flow (cm^3/s), jet diameter (mm) and depth after the jump (mm) vary; returns R in cm with g = 9.8."""

from math import pi


def solve(flow=20.0, diameter=5.0, depth=3.0):
    q, d, h = flow * 1e-6, diameter * 1e-3, depth * 1e-3
    return 4 * q**2 / (pi**2 * d**2 * 9.8 * h**2) * 1e2


def check(flow=20.0, diameter=5.0, depth=3.0):
    q, d, big = flow * 1e-6, diameter * 1e-3, depth * 1e-3
    v = q / (pi * (d / 2) ** 2)
    thin = 9.8 * big**2 / (2 * v**2)
    return q / (2 * pi * thin * v) * 1e2


PARAMS = {"flow": 20.0, "diameter": 5.0, "depth": 3.0}
VARIANTS = [{"flow": 40.0}, {"diameter": 8.0}, {"depth": 2.0}]
ANSWER = 7.352104028468951
TOL = 1e-9
