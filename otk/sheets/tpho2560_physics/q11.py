"""Theory 2.6: if the source brightens so the peak becomes 1.1 V, the reference concentration reads 1.1 cos^2(0.75 pi) = 0.55 V; read against the old 1.0 V curve that means theta = arccos(-sqrt(0.55)), so the operator thinks h is 6 ppm too high. Adapted: the new peak (V) varies with L = 1.0 cm, alpha = 0.146 and lambda0 = 550 nm; returns the apparent Delta h in ppm."""

from math import acos, pi, sqrt


def solve(bright=1.1, length=1.0, alpha=0.146, wavelength=550.0):
    reading = bright * 0.5
    shift = acos(-sqrt(reading)) - 0.75 * pi
    return shift * wavelength * 1e-9 / (pi * length * 1e-2 * alpha) * 1e6


def check(bright=1.1, length=1.0, alpha=0.146, wavelength=550.0):
    from otk.sheets.tpho2560_physics import q10

    return q10.check(reading=bright * 0.5, peak=1.0, length=length, alpha=alpha, wavelength=wavelength)


PARAMS = {"bright": 1.1, "length": 1.0, "alpha": 0.146, "wavelength": 550.0}
VARIANTS = [{"bright": 1.2}, {"bright": 1.05}, {"bright": 1.3, "length": 2.0}]
ANSWER = 6.005600765785257
TOL = 1e-9
