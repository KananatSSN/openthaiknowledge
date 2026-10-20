"""Theory 1.1 (b) design B: the throat (A2 = A1/2) carries 2 v1 and the exit (A3 = 2 A1) v1/2 at atmospheric pressure; water rises h when the throat's pressure is P_a - rho_w g h, so Bernoulli gives v1 = sqrt(8 rho_w g h/(15 rho_a)). Adapted: h (cm) and rho_a vary; returns v1 in m/s with g = 9.8."""

from math import sqrt


def solve(height=5.0, air=1.2, water=1000.0, g=9.8):
    return sqrt(8 * water * g * height / 100 / (15 * air))


def check(height=5.0, air=1.2, water=1000.0, g=9.8):
    # Bisect the inlet speed at which the throat's suction just lifts water h.
    from otk.sheets.tpho2559_physics._shared import bisect

    def lift(v1):
        throat, exit_ = 2 * v1, v1 / 2           # continuity with A2 = A1/2, A3 = 2 A1
        suction = 0.5 * air * (throat**2 - exit_**2)
        return suction - water * g * height / 100

    return bisect(lift, 0.0, 1e4)


PARAMS = {"height": 5.0, "air": 1.2, "water": 1000.0, "g": 9.8}
VARIANTS = [{"height": 2.0}, {"air": 1.29}, {"height": 10.0, "air": 1.1}]
ANSWER = 14.757295747452437
TOL = 1e-9
