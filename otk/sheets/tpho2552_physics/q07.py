"""Theory 2.3: after the first collision the light ball hits the ceiling (H = 6.00 m) at 21.67 m/s after 0.261 s, falls back and meets the heavy ball 0.485 s after the first collision (the scheme: 0.48 s). Adapted: m/M, h and H vary; seconds with g = 10, solved in closed form."""

from math import sqrt


def solve(ratio=1 / 6, drop=5.0, ceiling=6.0, g=10.0):
    v0 = sqrt(2 * g * drop)
    v = (3 - ratio) / (1 + ratio) * v0
    big = (1 - ratio) * v0 - ratio * v
    top = sqrt(v * v - 2 * g * ceiling)
    t_top = (v - top) / g
    # Heavy ball: y = big tau - g tau^2/2; light ball after the ceiling:
    # y = H - top (tau - t_top) - g (tau - t_top)^2/2. The g tau^2 terms cancel
    # to a linear equation in tau.
    return (ceiling + top * t_top - g * t_top**2 / 2) / (big + top - g * t_top)


def check(ratio=1 / 6, drop=5.0, ceiling=6.0, g=10.0):
    from otk.sheets.tpho2552_physics._balls import second_collision

    return second_collision(ratio, drop, ceiling, g)[0]


PARAMS = {"ratio": 1 / 6, "drop": 5.0, "ceiling": 6.0, "g": 10.0}
VARIANTS = [{"ceiling": 8.0}, {"ratio": 0.2, "drop": 3.2, "ceiling": 4.0}, {"drop": 7.2, "ceiling": 10.0}]
ANSWER = 0.4847330727572656
TOL = 1e-4
