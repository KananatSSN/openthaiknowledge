"""Part2 item 7 figure: a ring of mass M, radius R spins with rim speed v; a small arc of angle theta needs inward force (M theta/2pi) v^2/R, supplied by 2 T sin(theta/2) ~ T theta, so T = M v^2/(2 pi R). Newtons."""

from math import pi, sin


def solve(mass=2, speed=6, radius=0.5):
    return mass * speed**2 / (2 * pi * radius)


def check(mass=2, speed=6, radius=0.5):
    # Use a finite arc and the exact 2 T sin(theta/2) balance, shrinking theta.
    theta = 1e-4
    needed = mass * theta / (2 * pi) * speed**2 / radius
    return needed / (2 * sin(theta / 2))


PARAMS = {"mass": 2, "speed": 6, "radius": 0.5}
VARIANTS = [{"speed": 10}, {"mass": 5, "radius": 2}, {"radius": 0.1}]
TOL = 1e-8
ANSWER = 22.91831180523293
