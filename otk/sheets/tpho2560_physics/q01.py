"""Theory 1.1: in the planet's frame the rock falls from rest far away at u and lands at sqrt(u^2 + 2gR); back in the observer's frame (the planet barely recoils) the rock moves at sqrt(u^2 + 2gR) - u, toward the planet. Adapted: u (km/s), g and R (km) vary; returns the speed in km/s."""

from math import sqrt


def solve(speed=5.0, gravity=9.8, radius=6400.0):
    u, R = speed * 1e3, radius * 1e3
    return (sqrt(u * u + 2 * gravity * R) - u) / 1e3


def check(speed=5.0, gravity=9.8, radius=6400.0):
    # Observer frame with a finite planet mass M = m/ratio: momentum gives the
    # planet's final speed w = u - ratio v, and energy (divided by m/2, with the
    # planet's term expanded) gives 2uv - ratio v^2 - v^2 + 2gR = 0. The rock is
    # pulled toward the planet, so take the root with v below u; bisect it.
    from math import sqrt

    from otk.sheets.tpho2560_physics._shared import bisect

    u, R = speed * 1e3, radius * 1e3
    ratio = 1e-9

    def energy(v):
        return 2 * u * v - ratio * v * v - v * v + 2 * gravity * R

    v = bisect(energy, u - 2 * sqrt(u * u + 2 * gravity * R), u)
    return abs(v) / 1e3


PARAMS = {"speed": 5.0, "gravity": 9.8, "radius": 6400.0}
VARIANTS = [{"speed": 20.0}, {"gravity": 3.7, "radius": 3400.0}, {"speed": 1.0}]
ANSWER = 7.265398485169571
TOL = 1e-6
