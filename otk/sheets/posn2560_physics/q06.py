"""Part 1, 6: projectile strikes hanging sphere horizontally, then falls vertically. Its final horizontal momentum is zero. Sphere rises without losses."""

from math import sqrt


def solve(mass=0.2, target=1, speed=3, g=9.8):
    return (mass * speed / target) ** 2 / (2 * g)


def check(mass=0.2, target=1, speed=3, g=9.8):
    # Search height whose descent speed restores the transferred momentum.
    lo, hi = 0.0, 1 + (mass * speed / target) ** 2 / g
    for _ in range(100):
        h = (lo + hi) / 2
        if target * sqrt(2 * g * h) < mass * speed:
            lo = h
        else:
            hi = h
    return (lo + hi) / 2


PARAMS = {"mass": 0.2, "target": 1, "speed": 3, "g": 9.8}
VARIANTS = [{"mass": 0.4}, {"target": 2}, {"speed": 6}]
ANSWER = 0.018367346938775515
