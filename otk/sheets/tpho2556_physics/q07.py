"""Theory 1.2 (d): the meteor shines brightest where it loses kinetic energy fastest, the power C_d (1/2) rho v^3 pi r^2; with v = u exp(-A e^(-alpha z)) and A = C_d rho0 pi r^2/(2 m alpha sin theta), rho v^3 peaks where e^(-alpha z) = 1/(3A), so z_max = (1/alpha) ln(3A). Adapted: C_d, r, m and theta (degrees) vary, rho0 = 1.2 kg/m^3, alpha = 1/(8 km); returns z_max in km."""

from math import log, pi, radians, sin


def solve(drag=1.0, radius=1.0, mass=10000.0, angle=45.0, rho0=1.2, alpha=1.25e-4):
    A = drag * rho0 * pi * radius**2 / (2 * mass * alpha * sin(radians(angle)))
    return log(3 * A) / alpha / 1e3


def check(drag=1.0, radius=1.0, mass=10000.0, angle=45.0, rho0=1.2, alpha=1.25e-4):
    from otk.sheets.tpho2556_physics._meteor import brightest

    return brightest(drag, radius, mass, radians(angle), 20e3, rho0=rho0, alpha=alpha)[0] / 1e3


PARAMS = {"drag": 1.0, "radius": 1.0, "mass": 10000.0, "angle": 45.0, "rho0": 1.2, "alpha": 1.25e-4}
VARIANTS = [{"angle": 30.0}, {"radius": 0.5, "mass": 1250.0}, {"drag": 0.6, "angle": 70.0}]
ANSWER = 14.847572717738258
TOL = 1e-8
