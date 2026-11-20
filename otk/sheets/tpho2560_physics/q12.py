"""Theory 3 A.1: a 4.0 MeV proton (non-relativistic) has v = sqrt(2E/m) = 2.77e7 m/s. Adapted: the kinetic energy (MeV) varies; returns v in units of 1e7 m/s."""

from math import sqrt


def solve(energy=4.0, mass=1.67e-27):
    return sqrt(2 * energy * 1e6 * 1.6e-19 / mass) / 1e7


def check(energy=4.0, mass=1.67e-27):
    # Accelerate from rest through the energy's equivalent voltage in small
    # steps of a uniform field over 1 m.
    from math import sqrt as root

    field = energy * 1e6        # V/m over 1 m
    a = 1.6e-19 * field / mass
    return root(2 * a * 1.0) / 1e7


PARAMS = {"energy": 4.0, "mass": 1.67e-27}
VARIANTS = [{"energy": 1.0}, {"energy": 10.0}, {"energy": 2.5}]
ANSWER = 2.7685141608239308
TOL = 1e-12
