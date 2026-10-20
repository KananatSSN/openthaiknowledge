"""Theory 3.2: the shells from xi = r to xi = R give V1 = (rho/eps0) integral of xi d xi = rho (R^2 - r^2)/(2 eps0). Adapted: returns V1 in units of rho/eps0 (lengths in m)."""

from math import pi, sqrt


def solve(radius=1.0, point=0.4):
    return (radius**2 - point**2) / 2


def check(radius=1.0, point=0.4):
    # Direct volume sum of rho/(4 pi eps0 |x - p|) over the outer layer,
    # midpoint rule in xi and in u = cos(angle), rho = eps0 = 1.
    nx, nu = 300, 300
    total = 0.0
    for i in range(nx):
        xi = point + (radius - point) * (i + 0.5) / nx
        dxi = (radius - point) / nx
        for j in range(nu):
            u = -1 + 2 * (j + 0.5) / nu
            dist = sqrt(xi * xi + point * point - 2 * xi * point * u)
            total += 2 * pi * xi * xi * dxi * (2 / nu) / (4 * pi * dist)
    return total


PARAMS = {"radius": 1.0, "point": 0.4}
VARIANTS = [{"point": 0.0}, {"radius": 2.0, "point": 1.0}, {"radius": 0.5, "point": 0.1}]
ANSWER = 0.42
TOL = 1e-3
