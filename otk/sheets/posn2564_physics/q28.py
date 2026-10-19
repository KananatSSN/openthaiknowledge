"""Short28 figure: A and B, equal mass m and equal charge q, released from rest D apart; far apart, |v_A - v_B| = q / sqrt(pi eps0 m D) (each moves at half that). SI units; k = 9e9. Inputs microcoulomb, gram, metre."""

from math import sqrt

K = 9e9


def solve(charge=2, mass=10, distance=0.9):
    q, m = charge * 1e-6, mass / 1000
    return 2 * sqrt(K * q * q / (m * distance))


def check(charge=2, mass=10, distance=0.9):
    # Integrate the motion in time. Units: D = 1, k q^2 / m = 1; each body sits
    # at +-x, so x'' = 1 / (2x)^2. Leapfrog with a step that grows with x, run
    # to x = 2e4, then add the small remaining potential energy as a tail.
    x, v = 0.5, 0.0
    while x < 2e4:
        dt = 2e-3 * x / max(v, 0.05)
        v += dt / 2 / (2 * x) ** 2
        x += dt * v
        v += dt / 2 / (2 * x) ** 2
    each = sqrt(v * v + 1 / (2 * x))
    scale = sqrt(K * (charge * 1e-6) ** 2 / (mass / 1000 * distance))
    return 2 * each * scale


TOL = 1e-3
PARAMS = {"charge": 2, "mass": 10, "distance": 0.9}
VARIANTS = [{"charge": 1, "mass": 1, "distance": 0.1}, {"distance": 0.4}, {"charge": 3, "mass": 9}]
ANSWER = 3.9999999999999996
