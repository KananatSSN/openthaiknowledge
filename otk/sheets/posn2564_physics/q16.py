"""MC16 figure: two -e charges on a circle around +2e at the centre; theta is the angle at the centre between them. Energy is least at theta = 180 deg (answer 4). Adapted quantity: that least energy in units of k e^2 / r for a centre charge +Ze: -2Z + 1/2."""

from math import cos, pi, sqrt


def solve(centre=2):
    return -2 * centre + 0.5


def check(centre=2):
    # Brute-force theta over a fine grid of the three pair energies (r = 1).
    best_theta, best = 0.0, float("inf")
    for k in range(1, 18001):
        theta = pi * k / 18000
        pair = sqrt(2 - 2 * cos(theta))
        energy = -centre - centre + 1 / pair
        if energy < best:
            best_theta, best = theta, energy
    assert abs(best_theta - pi) < 1e-9
    return best


PARAMS = {"centre": 2}
VARIANTS = [{"centre": 1}, {"centre": 3}, {"centre": 5}]
ANSWER = -3.5
