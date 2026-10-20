"""Theory 3.3: for small oscillations about the stretched equilibrium, m y'' = (V0^2 A eps0/(D - d)^3 - k) y, so omega^2 = (1/m)(k - V0^2 A eps0/(D - d)^3) = (k/m)(D - 3d)/(D - d). Adapted: k, m, D and d given; rad/s."""

from math import sqrt


def solve(spring=40.0, mass=0.05, gap=0.01, stretch=0.002):
    return sqrt(spring / mass * (gap - 3 * stretch) / (gap - stretch))


def check(spring=40.0, mass=0.05, gap=0.01, stretch=0.002):
    # Numerical stiffness: force at y on either side of equilibrium with the
    # electric force fixed by the equilibrium condition k d = F_e(d).
    coefficient = spring * stretch * (gap - stretch) ** 2   # = eps0 A V0^2/2

    def force(y):
        return coefficient / (gap - stretch - y) ** 2 - spring * (stretch + y)

    h = 1e-9
    stiffness = -(force(h) - force(-h)) / (2 * h)
    return sqrt(stiffness / mass)


PARAMS = {"spring": 40.0, "mass": 0.05, "gap": 0.01, "stretch": 0.002}
VARIANTS = [{"stretch": 0.001}, {"spring": 10.0, "mass": 0.2}, {"gap": 0.03, "stretch": 0.005}]
ANSWER = 20.0
TOL = 1e-5
