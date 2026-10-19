"""MC23: equal electric and magnetic energy densities in an EM wave, (1/2) eps0 E^2 = B^2/(2 mu0), give E = c B (answer 1). Adapted: B in nT; returns E in V/m with c = 3e8."""

from math import sqrt

C = 3e8
MU0 = 4e-7 * 3.141592653589793
EPS0 = 1 / (MU0 * C * C)


def solve(field_nt=10):
    return C * field_nt * 1e-9


def check(field_nt=10):
    # Equate the two energy densities and solve for E directly.
    b = field_nt * 1e-9
    magnetic = b * b / (2 * MU0)
    return sqrt(2 * magnetic / EPS0)


PARAMS = {"field_nt": 10}
VARIANTS = [{"field_nt": 1}, {"field_nt": 50}, {"field_nt": 7}]
ANSWER = 3.0
