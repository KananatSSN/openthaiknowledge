"""Theory 1.1 (c): a + 2.44 lambda L/a is least at a = sqrt(2.44 lambda L). Adapted: lambda (nm) and L (cm) vary; returns a in mm."""

from math import sqrt


def solve(wavelength=550.0, depth=20.0):
    return sqrt(2.44 * wavelength * 1e-9 * depth * 1e-2) * 1e3


def check(wavelength=550.0, depth=20.0):
    # Golden-section search on the image size.
    lam, L = wavelength * 1e-9, depth * 1e-2

    def size(a):
        return a + 2.44 * lam * L / a

    lo, hi = 1e-6, 1e-2
    r = (sqrt(5) - 1) / 2
    for _ in range(300):
        x1, x2 = hi - r * (hi - lo), lo + r * (hi - lo)
        if size(x1) < size(x2):
            hi = x2
        else:
            lo = x1
    return (lo + hi) / 2 * 1e3


PARAMS = {"wavelength": 550.0, "depth": 20.0}
VARIANTS = [{"wavelength": 450.0}, {"depth": 50.0}, {"wavelength": 650.0, "depth": 10.0}]
ANSWER = 0.5180733538795448
TOL = 1e-7
