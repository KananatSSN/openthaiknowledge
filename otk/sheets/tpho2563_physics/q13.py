"""Theory 3.2-3.5: light from A (d1 from the mass) to B (d2) bending at distance y takes t = l1/c + (2GM/c^3) ln(4 d1 d2/y^2) with l1 = d1 + d2 + y^2(d1 + d2)/(2 d1 d2); dt/dy = 0 gives y^2 = (4GM/c^2) d1 d2/(d1 + d2). Adapted: the lens mass (1e41 kg) and the source and observer distances (Mpc) vary; returns kiloparsecs."""

from math import sqrt


def solve(mass=3.55, source=2360.0, observer=940.0):
    from otk.sheets.tpho2563_physics._shared import C, G, PARSEC

    d1, d2 = source * 1e6 * PARSEC, observer * 1e6 * PARSEC
    return sqrt(4 * G * mass * 1e41 / C**2 * d1 * d2 / (d1 + d2)) / (1e3 * PARSEC)


def check(mass=3.55, source=2360.0, observer=940.0):
    from math import log

    from otk.sheets.tpho2563_physics._shared import C, G, PARSEC, golden_min

    # Fermat: minimise the travel time over y, with the exact path lengths
    d1, d2 = source * 1e6 * PARSEC, observer * 1e6 * PARSEC
    m = mass * 1e41

    def delay(y):
        # path length beyond d1 + d2, written to avoid cancelling large terms
        extra = y * y / (sqrt(y * y + d1 * d1) + d1) + y * y / (sqrt(y * y + d2 * d2) + d2)
        return extra / C + 2 * G * m / C**3 * log(4 * d1 * d2 / y**2)

    kpc = 1e3 * PARSEC
    return golden_min(delay, 0.1 * kpc, 100 * kpc) / kpc


PARAMS = {"mass": 3.55, "source": 2360.0, "observer": 940.0}
VARIANTS = [{"mass": 1.0}, {"source": 1000.0}, {"observer": 400.0}]
ANSWER = 4.78796351008996
TOL = 1e-6
