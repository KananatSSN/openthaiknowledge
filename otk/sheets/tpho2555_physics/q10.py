"""Theory 3 (a) figure 1: a Gaussian pillbox around the plate encloses charge 2 sigma A and its two faces carry flux 2EA, so E = sigma/epsilon0 outside a conductor with sigma on each face. Adapted: sigma (microcoulombs per square metre) varies; returns E in kV/m."""

EPS0 = 8.85e-12


def solve(density=1.0):
    return density * 1e-6 / EPS0 / 1e3


def check(density=1.0):
    # The two charged faces as huge discs (radius 1 km), field on the axis
    # 1 mm outside: each gives sigma/(2 eps0)(1 - z/sqrt(z^2 + R^2)).
    from math import sqrt

    sigma, R = density * 1e-6, 1e3
    total = 0.0
    for z in (1e-3, 1e-3 + 1e-4):     # near face and far face (plate 0.1 mm thick)
        total += sigma / (2 * EPS0) * (1 - z / sqrt(z * z + R * R))
    return total / 1e3


PARAMS = {"density": 1.0}
VARIANTS = [{"density": 5.0}, {"density": 0.2}, {"density": 12.0}]
ANSWER = 112.99435028248585
TOL = 1e-5
