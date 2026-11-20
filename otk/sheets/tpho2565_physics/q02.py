"""Theory 1 b): at (r, theta) the dipole field is (2p cos(theta) r_hat + p sin(theta) theta_hat)/(4 pi eps0 r^3), of size p sqrt(1 + 3 cos^2 theta)/(4 pi eps0 r^3). Adapted: the dipole charge (nC), spacing (mm), distance (cm) and angle (degrees) vary; returns V/m."""

from math import cos, radians, sqrt


def solve(charge=1000.0, spacing=1.0, distance=5.0, angle=60.0):
    from otk.sheets.tpho2565_physics._shared import COULOMB

    p = charge * 1e-9 * spacing * 1e-3
    return COULOMB * p * sqrt(1 + 3 * cos(radians(angle)) ** 2) / (distance * 1e-2) ** 3


def check(charge=1000.0, spacing=1.0, distance=5.0, angle=60.0):
    from math import hypot, sin

    from otk.sheets.tpho2565_physics._shared import COULOMB

    # add the two Coulomb fields as vectors in the x-z plane
    q, h, r, t = charge * 1e-9, spacing * 1e-3 / 2, distance * 1e-2, radians(angle)
    x, z = r * sin(t), r * cos(t)
    ex = ez = 0.0
    for sign, zc in ((1, h), (-1, -h)):
        dx, dz = x, z - zc
        d3 = hypot(dx, dz) ** 3
        ex += sign * COULOMB * q * dx / d3
        ez += sign * COULOMB * q * dz / d3
    return hypot(ex, ez)


PARAMS = {"charge": 1000.0, "spacing": 1.0, "distance": 5.0, "angle": 60.0}
VARIANTS = [{"angle": 30.0}, {"distance": 10.0}, {"angle": 125.0}]
ANSWER = 95117.32535527275
TOL = 1e-3
