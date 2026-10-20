"""Theory 2.2: inside the square of four protons the potential is lowest at the centre (0, 0), V = 4ke/(a/sqrt 2) = 4 sqrt 2 ke/a. Adapted: a in nm with ke = 1.44e-9 V m; volts."""

from math import sqrt


def solve(side=0.2, ke=1.44e-9):
    return 4 * sqrt(2) * ke / (side * 1e-9)


def check(side=0.2, ke=1.44e-9):
    # Minimise the potential over a grid inside the square and read it off.
    a = side * 1e-9
    corners = [(sx * a / 2, sy * a / 2) for sx in (-1, 1) for sy in (-1, 1)]
    best = None
    n = 40
    for i in range(1, n):
        for j in range(1, n):
            x, y = -a / 2 + a * i / n, -a / 2 + a * j / n
            v = sum(ke / sqrt((x - cx) ** 2 + (y - cy) ** 2) for cx, cy in corners)
            best = v if best is None or v < best else best
    return best


PARAMS = {"side": 0.2, "ke": 1.44e-9}
VARIANTS = [{"side": 1.0}, {"side": 0.05}, {"side": 2.0}]
ANSWER = 40.72935059634513
TOL = 1e-9
