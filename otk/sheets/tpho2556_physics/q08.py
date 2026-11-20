"""Theory 1.2 (e): at z_max the density is rho0/(3A) and the speed u e^(-1/3), so the stagnation pressure is (1/2) rho v^2 = rho0 u^2 e^(-2/3)/(6A) = m alpha u^2 sin(theta) e^(-2/3)/(3 C_d pi r^2). Adapted: C_d, r, m, theta (degrees) and u (km/s) vary; returns the pressure in MPa."""

from math import exp, pi, radians, sin


def solve(drag=1.0, radius=1.0, mass=10000.0, angle=45.0, speed=20.0, alpha=1.25e-4):
    return mass * alpha * (speed * 1e3) ** 2 * sin(radians(angle)) * exp(-2 / 3) / (3 * drag * pi * radius**2) / 1e6


def check(drag=1.0, radius=1.0, mass=10000.0, angle=45.0, speed=20.0, alpha=1.25e-4):
    from otk.sheets.tpho2556_physics._meteor import brightest

    _, rho, v = brightest(drag, radius, mass, radians(angle), speed * 1e3, alpha=alpha)
    return 0.5 * rho * v * v / 1e6


PARAMS = {"drag": 1.0, "radius": 1.0, "mass": 10000.0, "angle": 45.0, "speed": 20.0, "alpha": 1.25e-4}
VARIANTS = [{"angle": 30.0}, {"speed": 40.0}, {"radius": 0.5, "mass": 1250.0}]
ANSWER = 19.259908719142402
TOL = 1e-8
