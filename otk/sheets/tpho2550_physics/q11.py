"""Theory 3.3 figure 3.2: F replaced by a hanging m3 over a light pulley; the cylinder rolls (I = m1 r^2/2), the block slides with mu_k: a = g[m3 - (m1 + m2) sin(theta) - mu_k m2 cos(theta)]/((3/2) m1 + m2 + m3). Adapted: numbers; m/s^2 with g = 10."""

from math import radians, sin, cos


def solve(roller=2, block=3, hanging=8, angle=37, kinetic=0.2, g=10):
    t = radians(angle)
    return g * (hanging - (roller + block) * sin(t) - kinetic * block * cos(t)) / (1.5 * roller + block + hanging)


def check(roller=2, block=3, hanging=8, angle=37, kinetic=0.2, g=10):
    # Energy: after the system moves s from rest, the gain in kinetic energy
    # (with the cylinder's spin) equals the net work; a = v^2/(2s).
    t = radians(angle)
    s = 1.0
    work = hanging * g * s - (roller + block) * g * sin(t) * s - kinetic * block * g * cos(t) * s
    inertia_per_r2 = 0.5 * roller
    v2 = 2 * work / (roller + block + hanging + inertia_per_r2)
    return v2 / (2 * s)


PARAMS = {"roller": 2, "block": 3, "hanging": 8, "angle": 37, "kinetic": 0.2, "g": 10}
VARIANTS = [{"hanging": 12}, {"angle": 30, "kinetic": 0.1}, {"roller": 4, "block": 1}]
ANSWER = 3.2226739844367023
TOL = 1e-9
