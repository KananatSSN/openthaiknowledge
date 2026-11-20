"""Short29 figure: wheel with 4 thin spokes turning at omega; an arrow of length l flies perpendicular to the wheel. Entering just after a spoke passes, it has 2 pi/(4 omega) seconds before the next spoke arrives, so v_min = 4 omega l/(2 pi) = 2 omega l/pi. Adapted: n spokes; returns m/s."""

from math import pi


def solve(spokes=4, omega=10, length=0.6):
    return spokes * omega * length / (2 * pi)


def check(spokes=4, omega=10, length=0.6):
    # Bisect on v: the arrow occupies the wheel plane from t = 0 (spoke just
    # past) to t = l/v; it is safe while the next spoke has not swept to it.
    gap_angle = 2 * pi / spokes

    def safe(v):
        return omega * (length / v) <= gap_angle

    lo, hi = 1e-6, 1e6
    for _ in range(300):
        mid = (lo + hi) / 2
        if safe(mid):
            hi = mid
        else:
            lo = mid
    return hi


PARAMS = {"spokes": 4, "omega": 10, "length": 0.6}
VARIANTS = [{"spokes": 6}, {"spokes": 3, "omega": 20, "length": 0.5}, {"spokes": 8, "length": 1}]
TOL = 1e-9
ANSWER = 3.819718634205488
