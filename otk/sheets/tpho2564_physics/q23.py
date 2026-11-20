"""Theory 3.2 e): the two beams cross at an angle a/f, so the fringes are lambda f/a apart, whatever the screen distance. Adapted: lambda (nm), f (cm) and the cut a (mm) vary; returns mm."""


def solve(wavelength=600.0, focal=20.0, cut=1.0):
    return wavelength * 1e-9 * focal * 1e-2 / (cut * 1e-3) * 1e3


def check(wavelength=600.0, focal=20.0, cut=1.0):
    from math import atan, sin

    # two plane waves at +-(a/2)/f: fringes lambda/(2 sin(half angle))
    half = atan(cut * 1e-3 / 2 / (focal * 1e-2))
    return wavelength * 1e-9 / (2 * sin(half)) * 1e3


PARAMS = {"wavelength": 600.0, "focal": 20.0, "cut": 1.0}
VARIANTS = [{"wavelength": 450.0}, {"cut": 2.0}, {"focal": 50.0}]
ANSWER = 0.12000000000000002
TOL = 1e-4
