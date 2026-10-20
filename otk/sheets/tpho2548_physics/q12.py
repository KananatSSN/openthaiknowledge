"""Theory 3.1 figure: air (density rho) blown at v0 down a tube of radius a spreads between two discs t apart; continuity pi a^2 v0 = 2 pi r t v gives v = a^2 v0/(2 t r). Adapted: numbers for a, v0, t, r; m/s."""

from math import pi


def solve(tube=0.01, speed=20, gap=0.002, radius=0.05):
    return tube**2 * speed / (2 * gap * radius)


def check(tube=0.01, speed=20, gap=0.002, radius=0.05):
    # Volume flux through the cylinder of radius r between the discs, by
    # summing strips around it.
    n = 3600
    strip = 2 * pi * radius / n * gap
    flow = pi * tube**2 * speed
    return flow / (strip * n)


PARAMS = {"tube": 0.01, "speed": 20, "gap": 0.002, "radius": 0.05}
VARIANTS = [{"radius": 0.01}, {"gap": 0.001, "speed": 5}, {"tube": 0.005, "radius": 0.2}]
ANSWER = 10.0
TOL = 1e-9
