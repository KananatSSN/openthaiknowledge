"""Theory 3(d) figure: the two electrons displaced equally and oppositely oscillate with x'' = -(3Qe/(4 pi eps0 m R^3)) x, f = (1/2 pi) sqrt(3Qe/(4 pi eps0 m R^3)). Adapted: Q = Z e and R in nm; hertz with the paper's constants."""

from math import pi, sqrt

E, M, EPS0 = 1.6e-19, 9.1e-31, 8.85e-12


def solve(radius=0.2, charge=2):
    r = radius * 1e-9
    return sqrt(3 * charge * E * E / (4 * pi * EPS0 * M * r**3)) / (2 * pi)


def check(radius=0.2, charge=2):
    # Numerical stiffness: the force on one electron at x0 + s (the other at
    # -(x0 + s)) from the nucleus and the other electron, differentiated in s.
    r = radius * 1e-9
    k = E * E / (4 * pi * EPS0)
    x0 = (1 / (4 * charge)) ** (1 / 3) * r

    def force(s):
        x = x0 + s
        return -k * charge * x / r**3 + k / (2 * x) ** 2

    h = 1e-6 * x0
    stiffness = -(force(h) - force(-h)) / (2 * h)
    return sqrt(stiffness / M) / (2 * pi)


PARAMS = {"radius": 0.2, "charge": 2}
VARIANTS = [{"charge": 4}, {"radius": 0.5, "charge": 6}, {"radius": 0.1}]
ANSWER = 2192166226218908.8
TOL = 1e-6
