"""Theory 3.3: the charge inside radius r acts at its surface as a point charge (4/3) pi r^3 rho at the centre: V2 = rho r^2/(3 eps0). Adapted: returns V2 in units of rho/eps0 (lengths in m)."""

from math import pi


def solve(point=0.4):
    return point**2 / 3


def check(point=0.4):
    # Work to bring a unit charge from far away against the field of the
    # inner ball alone: integrate Q/(4 pi s^2) from r out, s = r/u.
    charge = 4 / 3 * pi * point**3  # rho = 1
    n = 4000
    total = 0.0
    for k in range(n):
        u = (k + 0.5) / n
        s = point / u
        total += charge / (4 * pi * s * s) * point / (u * u) / n
    return total


PARAMS = {"point": 0.4}
VARIANTS = [{"point": 1.0}, {"point": 0.15}, {"point": 2.5}]
ANSWER = 0.053333333333333344
TOL = 1e-6
