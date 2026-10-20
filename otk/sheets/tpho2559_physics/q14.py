"""Theory 3.1 figure 3: the massless beam needs 2T sin(theta) = F1, so the rope's torque on the shaft is 2T cos(theta) r = F1 r/tan(theta), against friction k(Mg + F1); alpha = (F1 r/tan theta - k(Mg + F1))/I. Adapted: F1 (N), theta (degrees), r (mm), M (kg), k (mm) and I (kg cm^2) vary; returns alpha in rad/s^2 with g = 9.8."""

from math import radians, tan


def solve(force=20.0, angle=20.0, radius=5.0, mass=1.0, k=2.0, inertia=10.0, g=9.8):
    torque = force * radius * 1e-3 / tan(radians(angle)) - k * 1e-3 * (mass * g + force)
    return torque / (inertia * 1e-4)


def check(force=20.0, angle=20.0, radius=5.0, mass=1.0, k=2.0, inertia=10.0, g=9.8):
    # Bisect the rope tension from the beam's balance, then resolve it.
    from math import cos, sin

    from otk.sheets.tpho2559_physics._shared import bisect

    t = radians(angle)
    tension = bisect(lambda T: 2 * T * sin(t) - force, 0.0, 1e6)
    return (2 * tension * cos(t) * radius * 1e-3 - k * 1e-3 * (mass * g + force)) / (inertia * 1e-4)


PARAMS = {"force": 20.0, "angle": 20.0, "radius": 5.0, "mass": 1.0, "k": 2.0, "inertia": 10.0, "g": 9.8}
VARIANTS = [{"angle": 35.0}, {"force": 40.0, "mass": 2.0}, {"inertia": 25.0}]
ANSWER = 215.14774194546226
TOL = 1e-9
