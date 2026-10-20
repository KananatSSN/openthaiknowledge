"""Theory 1.4: continuity h1 v1 = h2 v2 and the momentum balance rho L (h2 v2^2 - h1 v1^2) = (1/2) rho g L (h1^2 - h2^2) give h2 = (h1/2)[sqrt(1 + 8 v1^2/(g h1)) - 1]. Adapted: the depth before (cm) and the speed (m/s) vary; returns the depth after the jump in cm with g = 9.8."""

from math import sqrt


def solve(depth=2.0, speed=3.0):
    h1 = depth * 1e-2
    return h1 / 2 * (sqrt(1 + 8 * speed**2 / (9.8 * h1)) - 1) * 1e2


def check(depth=2.0, speed=3.0):
    from otk.sheets.tpho2562_physics._shared import bisect

    h1 = depth * 1e-2
    q = h1 * speed  # flow per unit width

    def balance(h2):
        return (q * q / h2 - q * speed) - 0.5 * 9.8 * (h1**2 - h2**2)

    return bisect(balance, h1 * 1.000001, 100 * h1) * 1e2


PARAMS = {"depth": 2.0, "speed": 3.0}
VARIANTS = [{"depth": 1.0}, {"speed": 5.0}, {"depth": 4.0, "speed": 2.0}]
ANSWER = 18.192366679894125
TOL = 1e-9
