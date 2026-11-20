"""Theory 1 g): released from rest at r0 on the x axis, the charge keeps r = r0 and is fastest at theta = pi, where (1/2) m0 v^2 = q0 p/(4 pi eps0 r0^2), v = sqrt(p q0/(2 pi eps0 m0 r0^2)). Adapted: the dipole moment (nC m), q0 (uC), m0 (g) and r0 (cm) vary; returns m/s."""

from math import pi, sqrt


def solve(moment=1.0, charge=1.0, mass=1.0, radius=5.0):
    from otk.sheets.tpho2565_physics._shared import EPS0

    return sqrt(moment * 1e-9 * charge * 1e-6 / (2 * pi * EPS0 * mass * 1e-3 * (radius * 1e-2) ** 2))


def check(moment=1.0, charge=1.0, mass=1.0, radius=5.0, steps=20000):
    from otk.sheets.tpho2565_physics._shared import COULOMB

    # step the motion in the plane with the point-dipole field, record the top speed
    p, q, m = moment * 1e-9, charge * 1e-6, mass * 1e-3
    x, z, vx, vz = radius * 1e-2, 0.0, 0.0, 0.0

    def accel(x, z):
        r = (x * x + z * z) ** 0.5
        c, s = z / r, x / r
        er, et = COULOMB * 2 * p * c / r**3, COULOMB * p * s / r**3
        # r_hat = (s, c), theta_hat = (c, -s) in (x, z)
        return q / m * (er * s + et * c), q / m * (er * c - et * s)

    beta = (2 * COULOMB * p * q / (m * (radius * 1e-2) ** 4)) ** 0.5
    dt = 3.0 / beta / steps
    top = 0.0
    for _ in range(steps):
        ax, az = accel(x, z)
        vx2, vz2 = vx + ax * dt / 2, vz + az * dt / 2
        x, z = x + vx2 * dt, z + vz2 * dt
        ax, az = accel(x, z)
        vx, vz = vx2 + ax * dt / 2, vz2 + az * dt / 2
        top = max(top, (vx * vx + vz * vz) ** 0.5)
    return top


PARAMS = {"moment": 1.0, "charge": 1.0, "mass": 1.0, "radius": 5.0}
VARIANTS = [{"radius": 10.0}, {"mass": 4.0}, {"moment": 2.0}]
ANSWER = 2.681453700959719
TOL = 1e-4
