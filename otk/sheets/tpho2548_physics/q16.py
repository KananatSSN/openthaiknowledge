"""Theory 3.5: the lower disc is lifted while pi rho K^2 [ln(R/a) - 1/2 + a^2/(2R^2)] - rho pi a^2 v0^2 >= m g. Adapted: numbers; the largest mass in kg with g = 9.8."""

from math import log, pi


def solve(density=1.2, tube=0.01, speed=20, gap=0.002, rim=0.1, g=9.8):
    k = tube**2 * speed / (2 * gap)
    lift = pi * density * k * k * (log(rim / tube) - 0.5 + tube**2 / (2 * rim**2))
    return (lift - density * pi * tube**2 * speed**2) / g


def check(density=1.2, tube=0.01, speed=20, gap=0.002, rim=0.1, g=9.8):
    # Net force from a ring sum of the pressure, minus the jet's momentum flux,
    # then bisect on the mass that it just supports.
    k = tube**2 * speed / (2 * gap)
    n = 200000
    lift = 0.0
    for i in range(n):
        r = tube + (rim - tube) * (i + 0.5) / n
        lift += density * k * k / 2 * (1 / r**2 - 1 / rim**2) * 2 * pi * r * (rim - tube) / n
    net = lift - density * pi * tube**2 * speed**2
    lo, hi = 0.0, 1e6
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if net - mid * g >= 0 else (lo, mid)
    return lo


PARAMS = {"density": 1.2, "tube": 0.01, "speed": 20, "gap": 0.002, "rim": 0.1, "g": 9.8}
VARIANTS = [{"rim": 0.2}, {"speed": 30, "gap": 0.001}, {"tube": 0.005, "gap": 0.0005}]
ANSWER = 0.15845024156063725
TOL = 1e-6
