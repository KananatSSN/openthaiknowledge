"""Theory 3.6: the image appears at beta = y/d2 from the lens, beta = sqrt((4GM/c^2) d1/(d2(d1 + d2))). Adapted: the lens mass (1e41 kg) and distances (Mpc, d1 from lens to source and d2 from lens to observer) vary; returns arcseconds."""

from math import pi, sqrt


def solve(mass=3.55, source=2360.0, observer=940.0):
    from otk.sheets.tpho2563_physics._shared import C, G, PARSEC

    d1, d2 = source * 1e6 * PARSEC, observer * 1e6 * PARSEC
    beta = sqrt(4 * G * mass * 1e41 / C**2 * d1 / (d2 * (d1 + d2)))
    return beta * 180 / pi * 3600


def check(mass=3.55, source=2360.0, observer=940.0):
    from otk.sheets.tpho2563_physics import q13
    from otk.sheets.tpho2563_physics._shared import PARSEC

    y = q13.check(mass=mass, source=source, observer=observer) * 1e3 * PARSEC
    return y / (observer * 1e6 * PARSEC) * 180 / pi * 3600


PARAMS = {"mass": 3.55, "source": 2360.0, "observer": 940.0}
VARIANTS = [{"mass": 1.0}, {"source": 1000.0}, {"observer": 400.0}]
ANSWER = 1.050625920986035
TOL = 1e-6
