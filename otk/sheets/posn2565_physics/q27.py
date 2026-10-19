"""Short27 figure: launch speed v0; target B on a wall a distance D away, near the launch height. To first order the aim must be raised above the line to B by delta theta = g D / (2 v0^2). g = 10."""

from math import asin


def solve(distance=10, speed=100, g=10):
    return g * distance / (2 * speed**2)


def check(distance=10, speed=100, g=10):
    # Exact low-angle solution for a level target: sin(2 theta) = g D / v0^2.
    return asin(g * distance / speed**2) / 2


PARAMS = {"distance": 10, "speed": 100, "g": 10}
VARIANTS = [{"distance": 20, "speed": 200}, {"speed": 150}, {"distance": 50, "speed": 250}]
TOL = 1e-4
ANSWER = 0.005
