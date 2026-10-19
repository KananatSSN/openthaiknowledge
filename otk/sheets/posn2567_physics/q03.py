"""Short3 figure: equal masses; A at u hits B at rest; the kinetic energy after is half the energy before and both keep moving along u. Then v_A = v_B = u/2. Adapted: energy fraction f = (1 + s^2)/2; v_A, v_B = u(1 -+ s)/2."""

from math import sqrt


def solve(speed=8, fraction=0.5):
    s = sqrt(2 * fraction - 1)
    return speed * (1 - s) / 2, speed * (1 + s) / 2


def check(speed=8, fraction=0.5):
    # Bisect on A's final speed: momentum gives B's; match the energy, taking
    # the root with A no faster than B (no passing through).
    def energy(va):
        vb = speed - va
        return va * va + vb * vb

    lo, hi = 0.0, speed / 2
    for _ in range(200):
        mid = (lo + hi) / 2
        if energy(mid) > fraction * speed * speed:
            lo = mid
        else:
            hi = mid
    va = (lo + hi) / 2
    return va, speed - va


PARAMS = {"speed": 8, "fraction": 0.5}
VARIANTS = [{"fraction": 5 / 9}, {"speed": 10, "fraction": 0.625}, {"speed": 5, "fraction": 13 / 25}]
TOL = 1e-7
ANSWER = (4.0, 4.0)
