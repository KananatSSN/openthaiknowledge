"""Theory 2.3: a long solenoid with n turns per metre carries B = mu0 n I, linking n l turns of area pi r^2, so L = mu0 n^2 pi r^2 l. Adapted: the turns per cm, radius (cm) and length (cm) vary; returns millihenries."""

from math import pi


def solve(turns=10.0, radius=2.0, length=50.0):
    from otk.sheets.tpho2562_physics._shared import MU0

    n, r, ell = turns * 1e2, radius * 1e-2, length * 1e-2
    return MU0 * n**2 * pi * r**2 * ell * 1e3


def check(turns=10.0, radius=2.0, length=50.0):
    from otk.sheets.tpho2562_physics._shared import MU0

    # flux linkage per ampere, from the field of the whole winding
    total = turns * length  # turns in the coil
    field = MU0 * total / (length * 1e-2)
    area = pi * (radius * 1e-2) ** 2
    return total * field * area * 1e3


PARAMS = {"turns": 10.0, "radius": 2.0, "length": 50.0}
VARIANTS = [{"turns": 20.0}, {"radius": 1.0}, {"length": 30.0}]
ANSWER = 0.7895683520871486
TOL = 1e-9
