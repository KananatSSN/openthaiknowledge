"""Theory 1.1 (a)-(b) figure: light reflected from the wedge's two faces at thickness y = x tan(theta) reinforces when 2ny = (N + 1/2) lambda (a half-wave loss at one face), so bright fringes are Delta x = lambda/(2 n tan theta) apart. Adapted: lambda (nm), n and theta (mrad) vary; returns the spacing in mm."""

from math import tan


def solve(wavelength=550.0, index=1.5, angle=2.0):
    return wavelength * 1e-9 / (2 * index * tan(angle * 1e-3)) * 1e3


def check(wavelength=550.0, index=1.5, angle=2.0):
    from otk.sheets.tpho2557_physics._shared import bisect

    lam, t = wavelength * 1e-9, tan(angle * 1e-3)

    def bright(N):
        return bisect(lambda x: 2 * index * x * t - (N + 0.5) * lam, 0.0, 1.0)

    return (bright(4) - bright(3)) * 1e3


PARAMS = {"wavelength": 550.0, "index": 1.5, "angle": 2.0}
VARIANTS = [{"wavelength": 450.0}, {"index": 1.6, "angle": 0.5}, {"angle": 5.0}]
ANSWER = 0.09166654444441186
TOL = 1e-9
