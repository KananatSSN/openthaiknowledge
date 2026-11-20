"""Theory 1.2 d): beam A carries momentum P/c per second and leaves deviated by delta, so it pushes the bead sideways with F_x = (P/c) sin(delta) = 2(P/c)((n - 1)/n)(a - x)/R, and F_y is second order. Adapted: the power (mW), index, offsets and radius (micrometres) vary; returns piconewtons."""


def solve(power=10.0, index=1.5, beam=5.0, shift=2.0, radius=50.0):
    from otk.sheets.tpho2563_physics._shared import C

    return 2 * power * 1e-3 / C * (index - 1) / index * (beam - shift) / radius * 1e12


def check(power=10.0, index=1.5, beam=5.0, shift=2.0, radius=50.0):
    from math import sin

    from otk.sheets.tpho2563_physics._shared import C, sphere_deviation

    delta = sphere_deviation(beam - shift, radius, index)
    return power * 1e-3 / C * sin(delta) * 1e12


PARAMS = {"power": 10.0, "index": 1.5, "beam": 5.0, "shift": 2.0, "radius": 50.0}
VARIANTS = [{"power": 40.0}, {"index": 1.4}, {"shift": 1.0}]
ANSWER = 1.3333333333333335
TOL = 1e-2
