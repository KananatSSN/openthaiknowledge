"""Lab 1, part 1.3 figure: a body of mass m swings about a pivot O a distance d from its centre of mass with T = 2 pi sqrt(I/(mgd)); the moment of inertia about the centre of mass is I_cm = mgdT^2/(4 pi^2) - md^2. Adapted: the 26.0 g coat hanger with synthetic d and T; g cm^2 with g = 980 cm/s^2."""

from math import pi


def solve(mass=26.0, distance=8, period=0.9, g=980):
    return mass * g * distance * period**2 / (4 * pi**2) - mass * distance**2


def check(mass=26.0, distance=8, period=0.9, g=980):
    # Bisect on I_cm until the compound-pendulum period, with the pivot inertia
    # from the parallel-axis theorem, matches the measured one.
    from math import sqrt

    def swing(i_cm):
        return 2 * pi * sqrt((i_cm + mass * distance**2) / (mass * g * distance))

    lo, hi = 0.0, 1e9
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if swing(mid) < period else (lo, mid)
    return lo


PARAMS = {"mass": 26.0, "distance": 8, "period": 0.9, "g": 980}
VARIANTS = [{"distance": 12, "period": 0.95}, {"distance": 4, "period": 1.1}, {"mass": 30, "period": 1.0}]
ANSWER = 2518.2952899149623
TOL = 1e-6
