"""Theory 2.5: the wire melts when i^2 rho/(2 alpha pi^2 r^3) > To - Ta, so the least current is i = pi r sqrt(2 alpha r (To - Ta)/rho). Adapted: numbers for r, rho, alpha, To - Ta; amperes."""

from math import pi, sqrt


def solve(resistivity=11.5e-6, radius=0.1, alpha=1e-4, rise=300):
    return pi * radius * sqrt(2 * alpha * radius * rise / resistivity)


def check(resistivity=11.5e-6, radius=0.1, alpha=1e-4, rise=300, heat=0.23, density=7.3):
    # Bisect on the current for which the steady state (found by bisecting
    # dT/dt = 0 of the 2.3 equation) sits exactly at the melting point.
    def steady_rise(i):
        gain = i * i * resistivity / (pi**2 * radius**4 * heat * density)
        lo, hi = 0.0, 1e9
        for _ in range(200):
            mid = (lo + hi) / 2
            if gain - 2 * alpha * mid / (heat * radius * density) > 0:
                lo = mid
            else:
                hi = mid
        return lo

    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if steady_rise(mid) < rise else (lo, mid)
    return lo


PARAMS = {"resistivity": 11.5e-6, "radius": 0.1, "alpha": 1e-4, "rise": 300}
VARIANTS = [{"rise": 1000}, {"radius": 0.05, "alpha": 3e-4}, {"resistivity": 1.7e-6}]
ANSWER = 7.175903300602417
TOL = 1e-7
