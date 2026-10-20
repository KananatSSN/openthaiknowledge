"""Theory 1.1 (b): diffraction at the hole spreads each edge of the image by L(1.22 lambda/a), so A = a + L theta + 2(1.22 lambda L/a). Adapted: a (mm), L (cm), lambda (nm) and theta vary; returns A in mm."""


def solve(hole=0.5, depth=20.0, wavelength=550.0, angle=0.0093):
    a, L, lam = hole * 1e-3, depth * 1e-2, wavelength * 1e-9
    return (a + L * angle + 2 * 1.22 * lam * L / a) * 1e3


def check(hole=0.5, depth=20.0, wavelength=550.0, angle=0.0093):
    # Widen each extreme ray by the first-minimum angle of the circular hole.
    from math import tan

    a, L, lam = hole * 1e-3, depth * 1e-2, wavelength * 1e-9
    spread = angle / 2 + 1.22 * lam / a
    return (a + 2 * L * tan(spread)) * 1e3


PARAMS = {"hole": 0.5, "depth": 20.0, "wavelength": 550.0, "angle": 0.0093}
VARIANTS = [{"hole": 0.3}, {"depth": 50.0, "wavelength": 450.0}, {"hole": 1.0}]
ANSWER = 2.8968000000000003
TOL = 1e-4
