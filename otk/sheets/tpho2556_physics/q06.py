"""Theory 1.2 (c): dv/dt = -sin(theta) v dv/dz equals -C_d rho0 e^(-alpha z) pi r^2 v^2/(2m); integrating from v = u high up gives v = u exp(a e^(bz)) with a = -C_d rho0 pi r^2/(2 m alpha sin theta), b = -alpha. Adapted: C_d, r, m and theta (degrees) vary, rho0 = 1.2 kg/m^3, alpha = 1/(8 km); returns a."""

from math import pi, radians, sin


def solve(drag=1.0, radius=1.0, mass=10000.0, angle=45.0, rho0=1.2, alpha=1.25e-4):
    return -drag * rho0 * pi * radius**2 / (2 * mass * alpha * sin(radians(angle)))


def check(drag=1.0, radius=1.0, mass=10000.0, angle=45.0, rho0=1.2, alpha=1.25e-4):
    # Integrate the descent from 150 km with RK4 in height and read off
    # ln(v/u) at sea level, where e^(bz) = 1.
    s = sin(radians(angle))

    def slope(z, lnv):
        return drag * rho0 * pi * radius**2 / (2 * mass) * 2.718281828459045 ** (-alpha * z) / s

    z, lnv = 150e3, 0.0
    n = 30000
    h = -z / n
    for _ in range(n):
        # Simpson step: the slope depends on z only
        lnv += h * (slope(z, lnv) + 4 * slope(z + h / 2, lnv) + slope(z + h, lnv)) / 6
        z += h
    return lnv


PARAMS = {"drag": 1.0, "radius": 1.0, "mass": 10000.0, "angle": 45.0, "rho0": 1.2, "alpha": 1.25e-4}
VARIANTS = [{"angle": 30.0}, {"radius": 0.5, "mass": 1250.0}, {"drag": 0.6}]
ANSWER = -2.132583810316016
TOL = 1e-6
