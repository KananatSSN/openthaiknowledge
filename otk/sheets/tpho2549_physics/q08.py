"""Theory 3(a): in Thomson's atom (charge Q spread uniformly in radius R) an electron inside feels -eQx/(4 pi eps0 R^3), simple harmonic with omega^2 = Qe/(4 pi eps0 m R^3). Adapted: hydrogen (Q = e) of radius R in nm; omega in rad/s with e = 1.6e-19 C, m = 9.1e-31 kg, eps0 = 8.85e-12."""

from math import pi, sqrt

E, M, EPS0 = 1.6e-19, 9.1e-31, 8.85e-12


def solve(radius=0.1, charge=1):
    r = radius * 1e-9
    return sqrt(charge * E * E / (4 * pi * EPS0 * M * r**3))


def check(radius=0.1, charge=1):
    # Time-step the electron from rest at x = R/2 under the Gauss's-law field
    # and time a full period between turning points.
    r = radius * 1e-9
    k = charge * E * E / (4 * pi * EPS0 * r**3)  # force constant
    x, v, t = r / 2, 0.0, 0.0
    dt = 2 * pi * sqrt(M / k) / 200000
    turns = []
    prev_v = 0.0
    while len(turns) < 3:
        v += -k * x / M * dt
        x += v * dt
        t += dt
        if prev_v < 0 <= v or prev_v > 0 >= v:
            turns.append(t)
        prev_v = v
    return 2 * pi / (turns[2] - turns[0])


PARAMS = {"radius": 0.1, "charge": 1}
VARIANTS = [{"radius": 0.3}, {"radius": 0.05}, {"charge": 2}]
ANSWER = 1.5904598829646326e+16
TOL = 1e-4
