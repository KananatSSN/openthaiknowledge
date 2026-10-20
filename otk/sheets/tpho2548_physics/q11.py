"""Theory 2.5: near the centre the force on the positron is -K x with K = 4 sqrt 2 ke^2/a^3 (the same in every direction), so omega = sqrt(4 sqrt 2 ke^2/(a^3 m_e)). Adapted: a in nm; rad/s with ke^2 = 2.307e-28 J m and m_e = 9.109e-31 kg."""

from math import sqrt


def solve(side=0.1, ke2=2.307e-28, mass=9.109e-31):
    a = side * 1e-9
    return sqrt(4 * sqrt(2) * ke2 / (a**3 * mass))


def check(side=0.1, ke2=2.307e-28, mass=9.109e-31):
    # Curvature of the exact 2D potential energy along a 45-degree direction,
    # by a second difference.
    a = side * 1e-9
    corners = [(sx * a / 2, sy * a / 2) for sx in (-1, 1) for sy in (-1, 1)]

    def energy(s):
        x = y = s / sqrt(2)
        return sum(ke2 / sqrt((x - cx) ** 2 + (y - cy) ** 2) for cx, cy in corners)

    h = 1e-3 * a
    k = (energy(h) - 2 * energy(0) + energy(-h)) / (h * h)
    return sqrt(k / mass)


PARAMS = {"side": 0.1, "ke2": 2.307e-28, "mass": 9.109e-31}
VARIANTS = [{"side": 0.05}, {"side": 1.0}, {"side": 0.3}]
ANSWER = 3.78508765034318e+16
TOL = 1e-5
