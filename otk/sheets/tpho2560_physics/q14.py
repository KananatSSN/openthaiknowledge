"""Theory 3 B.1: at the edge of a beam of n protons, length l and radius r0, Gauss gives qE = n q^2/(2 pi eps0 l r0) outward and Ampere gives qvB = mu0 n q^2 v^2/(2 pi l r0) inward, so a0 = n q^2 (1 - v^2/c^2)/(2 pi eps0 m l r0). Adapted: n (millions), the kinetic energy (MeV), r0 (mm) and l (cm) vary; returns a0 in units of 1e8 m/s^2."""

from math import pi, sqrt

EPS0, MU0, Q, M = 8.85e-12, 4e-7 * pi, 1.6e-19, 1.67e-27


def solve(count=1.0, energy=4.0, radius=1.0, length=30.0):
    v = sqrt(2 * energy * 1e6 * Q / M)
    n, r, span = count * 1e6, radius * 1e-3, length * 1e-2
    return n * Q * Q * (1 - EPS0 * MU0 * v * v) / (2 * pi * EPS0 * M * span * r) / 1e8


def check(count=1.0, energy=4.0, radius=1.0, length=30.0):
    # Sum the electric and magnetic forces on an edge proton from the
    # charge and current enclosed in thin shells (midpoint in r).
    v = sqrt(2 * energy * 1e6 * Q / M)
    n, r0, span = count * 1e6, radius * 1e-3, length * 1e-2
    shells = 1000
    charge = sum(n * Q * ((k + 1) ** 2 - k**2) / shells**2 for k in range(shells))
    electric = Q * charge / (2 * pi * EPS0 * span * r0)
    magnetic = Q * v * MU0 * charge * v / (2 * pi * span * r0)
    return (electric - magnetic) / M / 1e8


PARAMS = {"count": 1.0, "energy": 4.0, "radius": 1.0, "length": 30.0}
VARIANTS = [{"count": 3.0}, {"radius": 0.5}, {"energy": 10.0, "length": 20.0}]
ANSWER = 9.11089997962019
TOL = 1e-9
