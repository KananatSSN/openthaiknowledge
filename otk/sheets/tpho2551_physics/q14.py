"""Lab 1 figure: a closed air column in a hose of length L sits h above the tank's water level, so P = P_atm - rho g h and Boyle gives (P_atm - rho g h) L = P_atm L0: 1/L = 1/L0 - (rho g/(P_atm L0)) h is a line in h; P_atm = rho g (intercept/|slope|). Adapted: synthetic slope and intercept of 1/L (1/m) against h (m); pascals."""


def solve(slope=-0.1935, intercept=2.0, rho=1000, g=9.8):
    return rho * g * intercept / abs(slope)


def check(slope=-0.1935, intercept=2.0, rho=1000, g=9.8):
    # Two points on the line, then Boyle's law between them for P_atm.
    h1, h2 = 0.2, 1.4
    l1, l2 = 1 / (intercept + slope * h1), 1 / (intercept + slope * h2)
    # (P - rho g h1) l1 = (P - rho g h2) l2
    return rho * g * (h1 * l1 - h2 * l2) / (l1 - l2)


PARAMS = {"slope": -0.1935, "intercept": 2.0, "rho": 1000, "g": 9.8}
VARIANTS = [{"intercept": 1.25, "slope": -0.121}, {"slope": -0.2}, {"intercept": 4.0, "slope": -0.387}]
ANSWER = 101291.98966408268
TOL = 1e-9
