"""Theory 3 c), d): with internal energy P/((gamma - 1) rho) the compressible Bernoulli law is c^2/(gamma - 1) + v^2/2 = constant, so the outlet temperature at Mach M is T1 = T0/(1 + (gamma - 1) M^2/2). Adapted: T0 (K), M and gamma vary; returns kelvin."""


def solve(start=300.0, mach=0.8, gamma=1.4):
    return start / (1 + (gamma - 1) * mach**2 / 2)


def check(start=300.0, mach=0.8, gamma=1.4, gas=287.0):
    from otk.sheets.tpho2565_physics._shared import bisect

    # c_p T + v^2/2 = c_p T0 with v = M sqrt(gamma R T)
    cp = gamma * gas / (gamma - 1)
    return bisect(lambda t: cp * t + 0.5 * mach**2 * gamma * gas * t - cp * start, 1.0, start)


PARAMS = {"start": 300.0, "mach": 0.8, "gamma": 1.4}
VARIANTS = [{"mach": 1.0}, {"gamma": 5 / 3}, {"start": 500.0, "mach": 0.5}]
ANSWER = 265.9574468085106
TOL = 1e-9
