"""Lab 2, part 2.2: with a cylindrical cavity and hanging (a), I1 = rho a^5/6 - pi rho a b^4/2 gives b^4 = 2(rho a^5/6 - I1)/(pi rho a). Adapted: synthetic a (cm), rho (g/cm^3) and I1 (g cm^2); returns b in cm."""

from math import pi


def solve(side=4, density=8.5, inertia=1397.26):
    return (2 * (density * side**5 / 6 - inertia) / (pi * density * side)) ** 0.25


def check(side=4, density=8.5, inertia=1397.26):
    # Bisect the cube-minus-cylinder moment of inertia, built from the solid
    # cube and a removed solid cylinder of mass rho pi b^2 a about its axis.
    def moment(b):
        cube = density * side**3 * (side**2 + side**2) / 12
        hole = density * pi * b * b * side * b * b / 2
        return cube - hole

    lo, hi = 0.0, side / 2
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if moment(mid) > inertia else (lo, mid)
    return lo


PARAMS = {"side": 4, "density": 8.5, "inertia": 1397.26}
VARIANTS = [{"inertia": 1300.0}, {"side": 5, "density": 7.8, "inertia": 3900.0}, {"inertia": 1450.0}]
ANSWER = 0.9999980880551393
TOL = 1e-6
