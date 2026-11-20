"""Theory 1.1 (c)-(d): heating stretches the wedge by alpha L0 Delta T along the incline, moving every thickness, and so every fringe, that far toward the thin end; Delta N = 2 n alpha L0 Delta T tan(theta)/lambda fringes pass, so alpha = lambda Delta N/(2 n L0 Delta T tan theta). Adapted: lambda (nm), n, L0 (cm), theta (mrad), Delta T and Delta N vary; returns alpha in units of 1e-6 per kelvin."""

from math import tan


def solve(wavelength=550.0, index=1.5, length=10.0, angle=20.0, warming=50.0, fringes=10):
    return wavelength * 1e-9 * fringes / (2 * index * length * 1e-2 * warming * tan(angle * 1e-3)) * 1e6


def check(wavelength=550.0, index=1.5, length=10.0, angle=20.0, warming=50.0, fringes=10):
    # Count the fringes that pass a fixed point as the wedge grows, then
    # bisect the expansion coefficient that gives the observed count.
    from otk.sheets.tpho2557_physics._shared import bisect

    lam, t = wavelength * 1e-9, tan(angle * 1e-3)
    spacing = lam / (2 * index * t)

    def passed(alpha):
        return alpha * length * 1e-2 * warming / spacing - fringes

    return bisect(passed, 0.0, 1.0) * 1e6


PARAMS = {"wavelength": 550.0, "index": 1.5, "length": 10.0, "angle": 20.0, "warming": 50.0, "fringes": 10}
VARIANTS = [{"fringes": 4}, {"warming": 80.0, "angle": 30.0}, {"index": 1.6, "length": 8.0}]
ANSWER = 18.330888823701216
TOL = 1e-9
