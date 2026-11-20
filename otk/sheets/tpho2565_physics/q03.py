"""Theory 1 c), d): a charge circling the dipole's axis needs E_z = 0, so 3 cos^2(theta_c) = 1 with theta_c = 125.3 deg for a positive charge, and its angular momentum is L_z = sqrt((1/(4 pi eps0)) (4/(3 sqrt 3)) p q0 m0), whatever the radius. Adapted: the dipole moment (nC m), q0 (uC) and m0 (g) vary; returns 1e-5 kg m^2/s."""

from math import sqrt


def solve(moment=1.0, charge=1.0, mass=1.0):
    from otk.sheets.tpho2565_physics._shared import COULOMB

    return sqrt(COULOMB * 4 / (3 * sqrt(3)) * moment * 1e-9 * charge * 1e-6 * mass * 1e-3) * 1e5


def check(moment=1.0, charge=1.0, mass=1.0, radius=0.05):
    from math import cos, sin

    from otk.sheets.tpho2565_physics._shared import COULOMB, bisect

    # find the angle where the field has no z part, then balance the inward pull
    p = moment * 1e-9

    def field(t):
        er = COULOMB * 2 * p * cos(t) / radius**3
        et = COULOMB * p * sin(t) / radius**3
        return er * cos(t) - et * sin(t), er * sin(t) + et * cos(t)

    t = bisect(lambda a: field(a)[0], 1.6, 3.1)
    pull = -charge * 1e-6 * field(t)[1]
    ring = radius * sin(t)
    speed = sqrt(pull * ring / (mass * 1e-3))
    return mass * 1e-3 * speed * ring * 1e5


PARAMS = {"moment": 1.0, "charge": 1.0, "mass": 1.0}
VARIANTS = [{"moment": 4.0}, {"charge": 0.25}, {"mass": 5.0}]
ANSWER = 8.31791281190141
TOL = 1e-9
