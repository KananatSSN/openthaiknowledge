"""Theory 3.2.3: the fringes first vanish (n = 0) at 2 d0 sin(alpha) = lambda/2, i.e. d0 ~ lambda/(2 (2 alpha)) for small alpha. Adapted: lambda (nm) and the angular separation 2 alpha (arcsec); returns d0 in mm."""

from math import radians, sin


def solve(wavelength=550, separation=5.0):
    angle = separation / 206264.806
    return wavelength * 1e-9 / (2 * angle) * 1e3


def check(wavelength=550, separation=5.0):
    # Bisect on d: the intensity of the summed fringe patterns of the two
    # stars at the screen centre direction is flat (contrast zero) first at
    # d0: phase difference 2 pi d (2 sin(alpha))/lambda = pi.
    alpha = radians(separation / 3600 / 2)
    lo, hi = 0.0, 1e5
    for _ in range(200):
        mid = (lo + hi) / 2
        phase = 2 * 3.141592653589793 * mid * 1e-3 * 2 * sin(alpha) / (wavelength * 1e-9)
        lo, hi = (mid, hi) if phase < 3.141592653589793 else (lo, mid)
    return lo


PARAMS = {"wavelength": 550, "separation": 5.0}
VARIANTS = [{"separation": 1.0}, {"wavelength": 650}, {"separation": 20.0, "wavelength": 450}]
ANSWER = 11.34456433
TOL = 1e-6
