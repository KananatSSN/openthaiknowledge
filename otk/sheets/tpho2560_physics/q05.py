"""Theory 1.3.1 figure: a 2.0 mm pupil limits resolution by diffraction to the Rayleigh angle 1.22 lambda/D = 336 microradians at 550 nm. Adapted: lambda (nm) and the pupil diameter (mm) vary; returns the angle in microradians."""


def solve(wavelength=550.0, pupil=2.0):
    return 1.22 * wavelength * 1e-9 / (pupil * 1e-3) * 1e6


def check(wavelength=550.0, pupil=2.0):
    # First zero of the Airy pattern: J1(x) = 0 at x = 3.8317 (series and
    # bisection), angle = x lambda/(pi D).
    from math import factorial, pi

    from otk.sheets.tpho2560_physics._shared import bisect

    def j1(x):
        return sum((-1) ** k * (x / 2) ** (2 * k + 1) / (factorial(k) * factorial(k + 1)) for k in range(40))

    zero = bisect(j1, 3.0, 4.5)
    return zero * wavelength * 1e-9 / (pi * pupil * 1e-3) * 1e6


PARAMS = {"wavelength": 550.0, "pupil": 2.0}
VARIANTS = [{"pupil": 3.0}, {"wavelength": 450.0}, {"pupil": 5.0, "wavelength": 650.0}]
ANSWER = 335.5
TOL = 5e-4
