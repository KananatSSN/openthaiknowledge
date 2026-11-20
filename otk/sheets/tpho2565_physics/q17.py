"""Theory 3 g): the largest flow is Q_max = A sqrt(P0 rho0 f(beta*)), the outlet then being sonic. Adapted: P0 (kPa), rho0 (kg/m^3), A (cm^2) and gamma vary; returns g/s."""

from math import sqrt


def solve(pressure=200.0, density=2.32, area=1.0, gamma=1.4):
    from otk.sheets.tpho2565_physics.q15 import flow_factor

    beta = (2 / (gamma + 1)) ** (gamma / (gamma - 1))
    return area * 1e-4 * sqrt(pressure * 1e3 * density * flow_factor(beta, gamma)) * 1e3


def check(pressure=200.0, density=2.32, area=1.0, gamma=1.4):
    # sonic outlet: T* = 2 T0/(gamma + 1), rho* from the adiabat, speed c*
    t_ratio = 2 / (gamma + 1)
    rho = density * t_ratio ** (1 / (gamma - 1))
    sound = sqrt(gamma * pressure * 1e3 / density * t_ratio)
    return rho * sound * area * 1e-4 * 1e3


PARAMS = {"pressure": 200.0, "density": 2.32, "area": 1.0, "gamma": 1.4}
VARIANTS = [{"gamma": 5 / 3}, {"area": 0.5}, {"pressure": 500.0, "density": 5.8}]
ANSWER = 46.64222611020807
TOL = 1e-9
