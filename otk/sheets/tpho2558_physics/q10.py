"""Theory 2.2 (c): the pellet leaves before the rod moves; integrating m v dv = [(F + P_a A)(L/(L + x))^gamma - P_a A - f] dx over the barrel length D gives v = sqrt((2/m)[((F + P_a A)/(gamma - 1))(L - L^gamma (L + D)^(1 - gamma)) - (f + P_a A) D]). Adapted: L0 and D (cm), F, f (N), A (cm^2) and m (g) vary with P_a = 1.0e5 Pa and gamma = 1.4; returns v in m/s."""

from math import sqrt


def solve(rest=30.0, grip=10.0, slide=0.5, area=1.0, barrel=5.0, mass=1.0, gamma=1.4, air=1.0e5):
    A, D, m = area * 1e-4, barrel * 1e-2, mass * 1e-3
    L = rest * 1e-2 * (air * A / (grip + air * A)) ** (1 / gamma)
    work = (grip + air * A) / (gamma - 1) * (L - L**gamma * (L + D) ** (1 - gamma)) - (slide + air * A) * D
    return sqrt(2 * work / m)


def check(rest=30.0, grip=10.0, slide=0.5, area=1.0, barrel=5.0, mass=1.0, gamma=1.4, air=1.0e5):
    from otk.sheets.tpho2558_physics._popgun import push, start_gap
    from otk.sheets.tpho2558_physics._shared import simpson

    A = area * 1e-4
    gap = start_gap(rest * 1e-2, grip, A, gamma, air)
    work = simpson(lambda x: push(x, gap, grip, A, slide, gamma, air), 0.0, barrel * 1e-2)
    return sqrt(2 * work / (mass * 1e-3))


PARAMS = {"rest": 30.0, "grip": 10.0, "slide": 0.5, "area": 1.0, "barrel": 5.0, "mass": 1.0, "gamma": 1.4, "air": 1.0e5}
VARIANTS = [{"barrel": 2.0}, {"grip": 20.0, "mass": 2.0}, {"slide": 1.0, "rest": 40.0}]
ANSWER = 25.203536810170906
TOL = 1e-8
