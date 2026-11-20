"""Theory 3.9: in a uniform sphere g(r) = (4/3) pi G rho r, and integrating dP/dr = -rho g from the surface gives P_c = (2/3) pi G rho^2 R^2 = (1/2) G M rho/R (alpha = 1/2); for the Sun it is 1.33e14 Pa. Adapted: the mass (1e30 kg) and radius (1e8 m) vary; returns pascals."""

from math import pi


def solve(mass=2.0, radius=7.0):
    from otk.sheets.tpho2562_physics._shared import G

    m, r = mass * 1e30, radius * 1e8
    rho = m / (4 / 3 * pi * r**3)
    return 0.5 * G * m * rho / r


def check(mass=2.0, radius=7.0, steps=20000):
    from otk.sheets.tpho2562_physics._shared import G

    m, r = mass * 1e30, radius * 1e8
    rho = 3 * m / (4 * pi * r**3)
    dr, p = r / steps, 0.0
    for i in range(steps):
        x = (i + 0.5) * dr
        p += rho * G * m * (x / r) ** 3 / x**2 * dr
    return p


PARAMS = {"mass": 2.0, "radius": 7.0}
VARIANTS = [{"mass": 1.0}, {"radius": 3.0}, {"mass": 4.0, "radius": 10.0}]
ANSWER = 132640167066590.0
TOL = 1e-6
