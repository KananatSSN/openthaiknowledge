"""Theory 3.2: at the greatest F that still holds the system, the block's friction acts down-slope: F = (m1 + m2) g sin(theta) + mu_s m2 g cos(theta). Adapted: numbers; newtons with g = 10."""

from math import radians, sin, cos


def solve(roller=2, block=3, angle=37, friction=0.4, g=10):
    t = radians(angle)
    return (roller + block) * g * sin(t) + friction * block * g * cos(t)


def check(roller=2, block=3, angle=37, friction=0.4, g=10):
    t = radians(angle)

    def holds(force):
        needed = (roller + block) * g * sin(t) - force
        return abs(needed) <= friction * block * g * cos(t) + 1e-12

    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if holds(mid) or mid < (roller + block) * g * sin(t) else (lo, mid)
    return lo


PARAMS = {"roller": 2, "block": 3, "angle": 37, "friction": 0.4, "g": 10}
VARIANTS = [{"angle": 53}, {"friction": 0.2, "roller": 5}, {"block": 1, "angle": 30}]
ANSWER = 39.67437727816993
TOL = 1e-9
