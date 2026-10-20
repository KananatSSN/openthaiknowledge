"""Lab 2, part 2.3 figure 1: a uniform beam (mass M, length L) pivoted at A and held level by the spring at B oscillates with T = 2 pi sqrt(M/(3k)) since (1/3) M L^2 theta'' = -k L^2 theta; so M = 3 k T^2/(4 pi^2). Adapted: synthetic k and T; kg."""

from math import pi, sqrt


def solve(spring=40.0, period=0.5):
    return 3 * spring * period**2 / (4 * pi**2)


def check(spring=40.0, period=0.5, length=1.0):
    # Bisect on M: the beam's period from its moment of inertia about A.
    def swing(mass):
        inertia = mass * length**2 / 3
        return 2 * pi * sqrt(inertia / (spring * length**2))

    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if swing(mid) < period else (lo, mid)
    return lo


PARAMS = {"spring": 40.0, "period": 0.5}
VARIANTS = [{"period": 0.8}, {"spring": 25.0}, {"spring": 60.0, "period": 0.3}]
ANSWER = 0.7599088773175333
TOL = 1e-9
