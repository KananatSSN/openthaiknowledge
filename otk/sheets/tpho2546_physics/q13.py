"""Theory 3.4: V = V1 + V2 = (rho/2 eps0)(R^2 - r^2/3) inside the uniformly charged ball. Adapted: returns V in units of rho/eps0 (lengths in m)."""

from math import pi


def solve(radius=1.0, point=0.4):
    return (radius**2 - point**2 / 3) / 2


def check(radius=1.0, point=0.4):
    # Integrate the Gauss's-law field inward from infinity: outside Q/(4 pi s^2),
    # inside s/3 (rho = eps0 = 1).
    charge = 4 / 3 * pi * radius**3
    n = 4000
    outside = sum(charge / (4 * pi * (radius / ((k + 0.5) / n)) ** 2) * radius / ((k + 0.5) / n) ** 2 / n for k in range(n))
    inside = sum((point + (radius - point) * (k + 0.5) / n) / 3 * (radius - point) / n for k in range(n))
    return outside + inside


PARAMS = {"radius": 1.0, "point": 0.4}
VARIANTS = [{"point": 0.0}, {"point": 1.0}, {"radius": 3.0, "point": 2.0}]
ANSWER = 0.47333333333333333
TOL = 1e-6
