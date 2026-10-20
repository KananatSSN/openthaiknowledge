"""Theory 1.1 (b) figure b: at rest the tangential forces balance, mg sin(theta0) = qE cos(theta0), so theta0 = arctan(qE/mg). Adapted: q (microcoulombs), E (kN/C) and m (g) vary; returns theta0 in degrees."""

from math import atan, degrees


def solve(charge=2.0, field=10.0, mass=4.0, g=9.8):
    return degrees(atan(charge * 1e-6 * field * 1e3 / (mass * 1e-3 * g)))


def check(charge=2.0, field=10.0, mass=4.0, g=9.8):
    from math import cos, pi, sin

    from otk.sheets.tpho2558_physics._shared import bisect

    qE, mg = charge * 1e-6 * field * 1e3, mass * 1e-3 * g
    return degrees(bisect(lambda t: qE * cos(t) - mg * sin(t), 0.0, pi / 2))


PARAMS = {"charge": 2.0, "field": 10.0, "mass": 4.0, "g": 9.8}
VARIANTS = [{"field": 5.0}, {"mass": 1.0}, {"charge": 5.0, "field": 20.0, "mass": 20.0}]
ANSWER = 27.03086025984298
TOL = 1e-9
