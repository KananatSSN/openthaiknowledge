"""Theory 2 (a) figure 1: all of E0 is kinetic at the equilibrium point, so u0^2 = 2E0/m. Adapted: m (g) and E0 (mJ) vary; returns u0 in m/s."""

from math import sqrt


def solve(mass=200.0, energy=40.0):
    return sqrt(2 * energy * 1e-3 / (mass * 1e-3))


def check(mass=200.0, energy=40.0, k=50.0):
    # Amplitude from E0 = k A^2/2, then the speed omega A at the centre.
    A = sqrt(2 * energy * 1e-3 / k)
    return A * sqrt(k / (mass * 1e-3))


PARAMS = {"mass": 200.0, "energy": 40.0}
VARIANTS = [{"mass": 50.0}, {"energy": 5.0}, {"mass": 500.0, "energy": 100.0}]
ANSWER = 0.6324555320336759
TOL = 1e-12
