"""Theory 2.2 (a)-(b) figure: the bamboo insulates and the push is quick, so the air is compressed adiabatically, P_a L0^gamma = P L^gamma, until PA = F + P_a A: L = L0 (P_a A/(F + P_a A))^(c_V/c_P). Adapted: L0 (cm), F (N) and A (cm^2) vary with P_a = 1.0e5 Pa and gamma = 1.4; returns L in cm."""


def solve(rest=30.0, grip=10.0, area=1.0, gamma=1.4, air=1.0e5):
    return rest * (air * area * 1e-4 / (grip + air * area * 1e-4)) ** (1 / gamma)


def check(rest=30.0, grip=10.0, area=1.0, gamma=1.4, air=1.0e5):
    # Compress the column in small adiabatic steps (dP/P = -gamma dV/V,
    # Simpson-free Euler with tiny steps) until the push reaches F.
    A = area * 1e-4
    L, P = rest * 1e-2, air
    dL = L / 2_000_000
    while P * A - air * A < grip:
        P += gamma * P * dL / L
        L -= dL
    return L * 100


PARAMS = {"rest": 30.0, "grip": 10.0, "area": 1.0, "gamma": 1.4, "air": 1.0e5}
VARIANTS = [{"grip": 25.0}, {"rest": 40.0, "area": 0.5}, {"grip": 5.0}]
ANSWER = 18.285204813067132
TOL = 1e-4
