"""MC8 figure: m at u splits into equal halves moving on in the same direction; the kinetic energy doubles. v1 + v2 = 2u and v1^2 + v2^2 = 4u^2 give v1 = 0, v2 = 2u (answer 2). Adapted: energy ratio k; v = u(1 -+ sqrt(k - 1)). Returns (v1, v2)."""

from math import sqrt


def solve(speed=5, ratio=2):
    s = sqrt(ratio - 1)
    return speed * (1 - s), speed * (1 + s)


def check(speed=5, ratio=2):
    # Bisect on v1 in [0, u] (both forward) to match the energy.
    def energy(v1):
        v2 = 2 * speed - v1
        return (v1 * v1 + v2 * v2) / 2

    lo, hi = 0.0, float(speed)
    for _ in range(200):
        mid = (lo + hi) / 2
        if energy(mid) > ratio * speed * speed:
            lo = mid
        else:
            hi = mid
    v1 = (lo + hi) / 2
    return v1, 2 * speed - v1


PARAMS = {"speed": 5, "ratio": 2}
VARIANTS = [{"ratio": 1.25}, {"speed": 9, "ratio": 13 / 9}, {"ratio": 17 / 16, "speed": 8}]
TOL = 1e-7
ANSWER = (0.0, 10.0)
