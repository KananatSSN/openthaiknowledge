"""Theory 1 a): far along the dipole's axis the field is E = 2p/(4 pi eps0 z^3). Adapted: the dipole charge (nC), spacing d (mm) and the distance z (cm) vary; returns V/m."""


def solve(charge=1000.0, spacing=1.0, distance=5.0):
    from otk.sheets.tpho2565_physics._shared import COULOMB

    p = charge * 1e-9 * spacing * 1e-3
    return 2 * COULOMB * p / (distance * 1e-2) ** 3


def check(charge=1000.0, spacing=1.0, distance=5.0):
    from otk.sheets.tpho2565_physics._shared import COULOMB

    # Coulomb's law for the two charges at +-d/2
    q, h, z = charge * 1e-9, spacing * 1e-3 / 2, distance * 1e-2
    return COULOMB * q * (1 / (z - h) ** 2 - 1 / (z + h) ** 2)


PARAMS = {"charge": 1000.0, "spacing": 1.0, "distance": 5.0}
VARIANTS = [{"distance": 10.0}, {"charge": 200.0}, {"spacing": 0.5}]
ANSWER = 143803.87900781148
TOL = 1e-3
