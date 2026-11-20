"""Theory 3.1 figure 3.1: a solid cylinder m1 (free axle) tied to a block m2 on a fixed incline, pulled up-slope by F; at the least F that holds them the block's static friction mu_s m2 g cos(theta) acts up-slope and the cylinder needs no friction: F = (m1 + m2) g sin(theta) - mu_s m2 g cos(theta). Adapted: numbers; newtons with g = 10."""

from math import radians, sin, cos


def solve(roller=2, block=3, angle=37, friction=0.4, g=10):
    t = radians(angle)
    return (roller + block) * g * sin(t) - friction * block * g * cos(t)


def check(roller=2, block=3, angle=37, friction=0.4, g=10):
    # Bisect on F: is the friction the block needs within its limit?
    t = radians(angle)

    def holds(force):
        tension = roller * g * sin(t)                 # holds the cylinder
        needed = block * g * sin(t) + tension - force  # up-slope friction on the block
        return abs(needed) <= friction * block * g * cos(t) + 1e-12

    lo, hi = -1e3, (roller + block) * g
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if holds(mid) else (mid, hi)
    return hi


PARAMS = {"roller": 2, "block": 3, "angle": 37, "friction": 0.4, "g": 10}
VARIANTS = [{"angle": 53}, {"friction": 0.2, "roller": 5}, {"block": 1, "angle": 30}]
ANSWER = 20.507125037034896
TOL = 1e-9
