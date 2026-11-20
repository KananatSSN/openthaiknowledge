"""Theory 3 f): with beta = P1/P0, Q^2 = P0 rho0 A^2 f(beta), f(beta) = (2 gamma/(gamma - 1))(beta^(2/gamma) - beta^(1 + 1/gamma)). Adapted: P0 (kPa), rho0 (kg/m^3), A (cm^2), beta and gamma vary; returns g/s."""

from math import sqrt


def flow_factor(beta, gamma):
    return 2 * gamma / (gamma - 1) * (beta ** (2 / gamma) - beta ** (1 + 1 / gamma))


def solve(pressure=200.0, density=2.32, area=1.0, ratio=0.7, gamma=1.4):
    return sqrt(pressure * 1e3 * density * (area * 1e-4) ** 2 * flow_factor(ratio, gamma)) * 1e3


def check(pressure=200.0, density=2.32, area=1.0, ratio=0.7, gamma=1.4):
    # outlet state along the adiabat, then the speed from c_p (T0 - T1) = v^2/2
    p0 = pressure * 1e3
    gas_t0 = p0 / density  # R T0 per unit mass
    t_ratio = ratio ** ((gamma - 1) / gamma)
    speed = sqrt(2 * gamma / (gamma - 1) * gas_t0 * (1 - t_ratio))
    rho1 = density * ratio ** (1 / gamma)
    return rho1 * area * 1e-4 * speed * 1e3


PARAMS = {"pressure": 200.0, "density": 2.32, "area": 1.0, "ratio": 0.7, "gamma": 1.4}
VARIANTS = [{"ratio": 0.9}, {"gamma": 5 / 3}, {"area": 0.5}]
ANSWER = 43.48060315860105
TOL = 1e-9
