"""Part 1, 3: bulb and floor initially share velocity; elevator continues accelerating upward."""

from math import sqrt


def solve(h=2.95, a=2.0, g=9.8):
    return sqrt(2 * h / (g + a))


def check(h=2.95, a=2.0, g=9.8):
    # Independently intersect lab-frame trajectories (initial speed 4 m/s).
    lo, hi = 0.0, 1 + 2 * h
    for _ in range(100):
        t = (lo + hi) / 2
        bulb = h + 4 * t - g * t * t / 2
        floor = 4 * t + a * t * t / 2
        if bulb > floor:
            lo = t
        else:
            hi = t
    return (lo + hi) / 2


PARAMS = {"h": 2.95, "a": 2.0, "g": 9.8}
VARIANTS = [{"h": 5.9}, {"a": 0}, {"a": 4}]
ANSWER = 0.7071067811865476
