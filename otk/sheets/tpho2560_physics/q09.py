"""Theory 2.3-2.4: the sugar path leads by phi = 2 pi L alpha h/lambda0 and the bright port receives the time average 2 I0 cos^2(phi/2) = 2 I0 cos^2(pi L alpha h/lambda0). Adapted: h (ppm), L (cm), alpha and lambda0 (nm) vary; returns the mean intensity as a multiple of I0."""

from math import cos, pi


def solve(conc=100.0, length=1.0, alpha=0.146, wavelength=550.0):
    phase = 2 * pi * length * 1e-2 * alpha * conc * 1e-6 / (wavelength * 1e-9)
    return 2 * cos(phase / 2) ** 2


def check(conc=100.0, length=1.0, alpha=0.146, wavelength=550.0):
    # Time-average (sin wt + sin(wt + phi))^2 over one period numerically.
    from math import sin

    phase = 2 * pi * length * 1e-2 * alpha * conc * 1e-6 / (wavelength * 1e-9)
    n = 20000
    return sum((sin(2 * pi * (k + 0.5) / n) + sin(2 * pi * (k + 0.5) / n + phase)) ** 2 for k in range(n)) / n


PARAMS = {"conc": 100.0, "length": 1.0, "alpha": 0.146, "wavelength": 550.0}
VARIANTS = [{"conc": 50.0}, {"conc": 250.0}, {"length": 2.0, "conc": 80.0}]
ANSWER = 0.9030487560311187
TOL = 1e-9
