"""Theory 1.2 e): the two beams push a displaced bead back with -4(P/c)((n - 1)/n) x/R, so it oscillates at w^2 = 4P(n - 1)/(m c R n). Adapted: the power per beam (mW), index, bead radius (micrometres) and density (kg/m^3) vary; returns rad/s."""

from math import pi, sqrt


def solve(power=10.0, index=1.5, radius=5.0, density=2500.0):
    from otk.sheets.tpho2563_physics._shared import C

    r = radius * 1e-6
    mass = density * 4 / 3 * pi * r**3
    return sqrt(4 * power * 1e-3 * (index - 1) / (mass * C * r * index))


def check(power=10.0, index=1.5, radius=5.0, density=2500.0):
    from math import sin

    from otk.sheets.tpho2563_physics._shared import C, sphere_deviation

    # the restoring stiffness of the exact two-beam force about x = 0
    r = radius * 1e-6
    beam, step = 0.05 * r, 1e-4 * r
    p = power * 1e-3 / C

    def force(x):
        return p * sin(sphere_deviation(beam - x, r, index)) - p * sin(sphere_deviation(beam + x, r, index))

    stiffness = -(force(step) - force(-step)) / (2 * step)
    return sqrt(stiffness / (density * 4 / 3 * pi * r**3))


PARAMS = {"power": 10.0, "index": 1.5, "radius": 5.0, "density": 2500.0}
VARIANTS = [{"power": 40.0}, {"index": 1.6}, {"radius": 2.0}]
ANSWER = 2605.88006348224
TOL = 1e-2
