"""Theory 3 a), b): treating the gas as incompressible, Q = rho0 A v1 and Bernoulli gives P1 = P0 - Q^2/(2 rho0 A^2). Adapted: P0 (kPa), rho0 (kg/m^3), the outlet area A (cm^2) and Q (g/s) vary; returns kPa."""


def solve(pressure=200.0, density=2.32, area=1.0, flow=50.0):
    return (pressure * 1e3 - (flow * 1e-3) ** 2 / (2 * density * (area * 1e-4) ** 2)) / 1e3


def check(pressure=200.0, density=2.32, area=1.0, flow=50.0):
    v = flow * 1e-3 / (density * area * 1e-4)
    return (pressure * 1e3 - 0.5 * density * v * v) / 1e3


PARAMS = {"pressure": 200.0, "density": 2.32, "area": 1.0, "flow": 50.0}
VARIANTS = [{"flow": 30.0}, {"area": 2.0}, {"density": 1.2, "pressure": 101.0, "flow": 20.0}]
ANSWER = 146.1206896551724
TOL = 1e-9
