"""Theory 2.4-2.5: coil 1 (n1 turns per metre) makes B = mu0 n1 I1 inside coil 2, whose n2 l turns of area pi r^2 link mu0 n1 n2 pi r^2 l I1, so M = mu0 n1 n2 pi r^2 l = sqrt(L1 L2). Adapted: both windings (turns per cm), the radius and length (cm) vary; returns millihenries."""

from math import pi, sqrt


def solve(first=10.0, second=40.0, radius=2.0, length=50.0):
    from otk.sheets.tpho2562_physics._shared import MU0

    return MU0 * first * 1e2 * second * 1e2 * pi * (radius * 1e-2) ** 2 * length * 1e-2 * 1e3


def check(first=10.0, second=40.0, radius=2.0, length=50.0):
    from otk.sheets.tpho2562_physics import q07

    return sqrt(q07.check(turns=first, radius=radius, length=length) * q07.check(turns=second, radius=radius, length=length))


PARAMS = {"first": 10.0, "second": 40.0, "radius": 2.0, "length": 50.0}
VARIANTS = [{"first": 5.0}, {"second": 20.0}, {"radius": 3.0}]
ANSWER = 3.1582734083485944
TOL = 1e-9
