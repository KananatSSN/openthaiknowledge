"""Theory 3.4: adiabatically P = K rho^gamma with K = P_a/rho0^gamma, so to first order P_m = gamma (P_a/rho0) rho_m and c = sqrt(gamma P_a/rho0). Adapted: gamma, P_a (kPa) and rho0 vary; returns c in m/s."""

from math import sqrt


def solve(gamma=1.4, pressure=101.325, density=1.2):
    return sqrt(gamma * pressure * 1e3 / density)


def check(gamma=1.4, pressure=101.325, density=1.2):
    # Numerical derivative dP/d(rho) of the adiabat at rho0, then c^2 = dP/d(rho).
    K = pressure * 1e3 / density**gamma
    h = density * 1e-6
    slope = (K * (density + h) ** gamma - K * (density - h) ** gamma) / (2 * h)
    return sqrt(slope)


PARAMS = {"gamma": 1.4, "pressure": 101.325, "density": 1.2}
VARIANTS = [{"gamma": 5 / 3}, {"pressure": 80.0}, {"density": 1.29, "gamma": 1.3}]
ANSWER = 343.8204473267988
TOL = 1e-9
