"""Theory 2.3: the second collision happens 0.485 s after the first at 0.90 m above the floor. The marking scheme prints 0.82 m, but its own equations (4) and (5) at t = 0.224 s give 0.90 m. Adapted: m/M, h and H vary; metres with g = 10."""

from math import sqrt


def solve(ratio=1 / 6, drop=5.0, ceiling=6.0, g=10.0):
    v0 = sqrt(2 * g * drop)
    v = (3 - ratio) / (1 + ratio) * v0
    big = (1 - ratio) * v0 - ratio * v
    top = sqrt(v * v - 2 * g * ceiling)
    t_top = (v - top) / g
    tau = (ceiling + top * t_top - g * t_top**2 / 2) / (big + top - g * t_top)
    return big * tau - g * tau * tau / 2


def check(ratio=1 / 6, drop=5.0, ceiling=6.0, g=10.0):
    from otk.sheets.tpho2552_physics._balls import second_collision

    return second_collision(ratio, drop, ceiling, g)[1]


PARAMS = {"ratio": 1 / 6, "drop": 5.0, "ceiling": 6.0, "g": 10.0}
VARIANTS = [{"ceiling": 8.0}, {"ratio": 0.2, "drop": 3.2, "ceiling": 4.0}, {"drop": 7.2, "ceiling": 10.0}]
ANSWER = 0.9025966955504932
TOL = 1e-4
