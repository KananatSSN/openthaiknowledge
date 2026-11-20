"""Theory 2.2: the sugar tube adds optical path (n - 1.33) L = alpha h L, so one fringe passes when alpha L Delta h = lambda0: Delta h = 550 nm/(0.146 x 1.0 cm) = 377 ppm. Adapted: lambda0 (nm), L (cm) and alpha vary; returns Delta h in ppm."""


def solve(wavelength=550.0, length=1.0, alpha=0.146):
    return wavelength * 1e-9 / (alpha * length * 1e-2) * 1e6


def check(wavelength=550.0, length=1.0, alpha=0.146):
    # Count wavelengths in the tube: N(h) = (1.33 + alpha h) L/lambda0;
    # bisect the h at which one more wavelength fits.
    from otk.sheets.tpho2560_physics._shared import bisect

    L, lam = length * 1e-2, wavelength * 1e-9

    def count(h):
        return (1.33 + alpha * h) * L / lam - 1.33 * L / lam - 1

    return bisect(count, 0.0, 1.0) * 1e6


PARAMS = {"wavelength": 550.0, "length": 1.0, "alpha": 0.146}
VARIANTS = [{"length": 2.0}, {"wavelength": 633.0}, {"alpha": 0.12, "length": 0.5}]
ANSWER = 376.7123287671233
TOL = 1e-9
