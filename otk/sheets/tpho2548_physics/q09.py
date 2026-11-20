"""Theory 2.3: a positron on the x axis through the centre of the proton square (corners at (+-a/2, +-a/2)) has E_p = 2ke^2/d1 + 2ke^2/d2 with d1,2 = sqrt((a/2 +- x)^2 + (a/2)^2); e.g. 4(1 + 1/sqrt 5) ke^2/a = 5.789 ke^2/a at x = -0.5a. Adapted: x as a fraction of a; returns E_p in units of ke^2/a."""

from math import sqrt


def solve(position=-0.5):
    near = sqrt((0.5 + position) ** 2 + 0.25)
    far = sqrt((0.5 - position) ** 2 + 0.25)
    return 2 / near + 2 / far


def check(position=-0.5):
    # Sum over the four protons from coordinates.
    corners = [(sx * 0.5, sy * 0.5) for sx in (-1, 1) for sy in (-1, 1)]
    return sum(1 / sqrt((position - cx) ** 2 + cy**2) for cx, cy in corners)


PARAMS = {"position": -0.5}
VARIANTS = [{"position": -2}, {"position": -0.25}, {"position": 0}]
ANSWER = 5.7888543819998315
TOL = 1e-12
