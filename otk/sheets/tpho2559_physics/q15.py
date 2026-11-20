"""Theory 3.2: winding n turns lowers the rope angle to cos(theta_n) = cos(theta0) e^(2 n pi r/L), and the work F1 does while unwinding is F1 L (theta0 - theta_n), so b = L(theta0 - theta_n). Adapted: L (cm), r (mm), theta0 (degrees) and n vary; returns b in cm."""

from math import acos, cos, exp, pi, radians


def solve(arm=25.0, radius=3.0, angle=70.0, turns=3):
    t0 = radians(angle)
    tn = acos(cos(t0) * exp(2 * turns * pi * radius * 1e-3 / (arm * 1e-2)))
    return arm * (t0 - tn)


def check(arm=25.0, radius=3.0, angle=70.0, turns=3):
    from otk.sheets.tpho2559_physics._drill import wind

    t0 = radians(angle)
    return arm * (t0 - wind(t0, turns, radius * 1e-3, arm * 1e-2))


PARAMS = {"arm": 25.0, "radius": 3.0, "angle": 70.0, "turns": 3}
VARIANTS = [{"turns": 5}, {"arm": 30.0, "angle": 75.0}, {"radius": 4.0}]
ANSWER = 2.353329305401025
TOL = 1e-8
