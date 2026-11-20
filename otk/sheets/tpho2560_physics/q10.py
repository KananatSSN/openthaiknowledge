"""Theory 2.5: the detector reads V = V_max cos^2(theta) with theta = pi L alpha h/lambda0; the reference 0.5 V of 1.0 V sits at theta = 0.75 pi, and 0.6 V at theta = arccos(-sqrt(0.6)), 0.10 rad further, so Delta h = 0.10 lambda0/(pi L alpha) = 12 ppm (add water). Adapted: the reading (V) varies with V_max = 1.0 V, L = 1.0 cm, alpha = 0.146 and lambda0 = 550 nm; returns Delta h in ppm."""

from math import acos, pi, sqrt


def solve(reading=0.6, peak=1.0, length=1.0, alpha=0.146, wavelength=550.0):
    shift = acos(-sqrt(reading / peak)) - 0.75 * pi
    return shift * wavelength * 1e-9 / (pi * length * 1e-2 * alpha) * 1e6


def check(reading=0.6, peak=1.0, length=1.0, alpha=0.146, wavelength=550.0):
    # Bisect the concentration change on the rising side of the reference.
    from math import cos

    from otk.sheets.tpho2560_physics._shared import bisect

    k = pi * length * 1e-2 * alpha / (wavelength * 1e-9)

    def volts(dh):
        return peak * cos(0.75 * pi + k * dh) ** 2 - reading

    return bisect(volts, 0.0, 0.25 * pi / k) * 1e6


PARAMS = {"reading": 0.6, "peak": 1.0, "length": 1.0, "alpha": 0.146, "wavelength": 550.0}
VARIANTS = [{"reading": 0.55}, {"reading": 0.8}, {"reading": 0.7, "length": 2.0}]
ANSWER = 12.072540844841175
TOL = 1e-9
