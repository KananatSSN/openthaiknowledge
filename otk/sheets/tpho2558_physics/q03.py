"""Theory 1.1 (c): about theta0 the restoring force is -(mg cos theta0 + qE sin theta0) delta theta, so f = (1/2 pi) sqrt((mg cos theta0 + qE sin theta0)/(m l)) = (1/2 pi) sqrt(sqrt(g^2 + (qE/m)^2)/l). Adapted: q (microcoulombs), E (kN/C), m (g) and l (m) vary; returns f in Hz."""

from math import atan, cos, pi, sin, sqrt


def solve(charge=2.0, field=10.0, mass=4.0, length=0.5, g=9.8):
    qE, mg = charge * 1e-6 * field * 1e3, mass * 1e-3 * g
    t0 = atan(qE / mg)
    return sqrt((mg * cos(t0) + qE * sin(t0)) / (mass * 1e-3 * length)) / (2 * pi)


def check(charge=2.0, field=10.0, mass=4.0, length=0.5, g=9.8):
    # Stiffness from a central difference of the tangential force about the
    # bisected equilibrium angle.
    from otk.sheets.tpho2558_physics._shared import bisect

    qE, mg = charge * 1e-6 * field * 1e3, mass * 1e-3 * g

    def force(t):
        return qE * cos(t) - mg * sin(t)

    t0 = bisect(force, 0.0, pi / 2)
    h = 1e-6
    stiffness = -(force(t0 + h) - force(t0 - h)) / (2 * h)
    return sqrt(stiffness / (mass * 1e-3 * length)) / (2 * pi)


PARAMS = {"charge": 2.0, "field": 10.0, "mass": 4.0, "length": 0.5, "g": 9.8}
VARIANTS = [{"field": 5.0}, {"length": 1.2}, {"charge": 5.0, "field": 20.0, "mass": 20.0}]
ANSWER = 0.7465645401361176
TOL = 1e-8
