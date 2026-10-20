"""Theory 3.4: the cylinder rolls without slipping when f1 = (I/r^2) a = m1 a/2 <= mu_s m1 g cos(theta), so mu_s >= a/(2 g cos(theta)) with a from 3.3. Adapted: numbers."""

from math import radians, sin, cos


def solve(roller=2, block=3, hanging=8, angle=37, kinetic=0.2, g=10):
    t = radians(angle)
    a = g * (hanging - (roller + block) * sin(t) - kinetic * block * cos(t)) / (1.5 * roller + block + hanging)
    return a / (2 * g * cos(t))


def check(roller=2, block=3, hanging=8, angle=37, kinetic=0.2, g=10, radius=0.1):
    # Torque on the cylinder about its axle: f1 r = I alpha with alpha = a/r,
    # then the ratio of the needed friction to the normal force.
    t = radians(angle)
    s = 1.0
    work = (hanging - (roller + block) * sin(t) - kinetic * block * cos(t)) * g * s
    a = work / (roller + block + hanging + 0.5 * roller) / s
    inertia = 0.5 * roller * radius**2
    friction = inertia * (a / radius) / radius
    return friction / (roller * g * cos(t))


PARAMS = {"roller": 2, "block": 3, "hanging": 8, "angle": 37, "kinetic": 0.2, "g": 10}
VARIANTS = [{"hanging": 12}, {"angle": 30, "kinetic": 0.1}, {"roller": 4, "block": 1}]
ANSWER = 0.20176125052627983
TOL = 1e-9
