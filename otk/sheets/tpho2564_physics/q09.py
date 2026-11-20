"""Theory 2 a): one electron leaving the cathode at v0 in the uniform field V_d/d gains e x V_d/d of energy, v_x = sqrt(2 e x V_d/(m d) + v0^2). Adapted: V_d, the gap d and position x (mm) and v0 (km/s) vary; returns km/s."""

from math import sqrt


def solve(volts=100.0, gap=10.0, depth=5.0, launch=100.0):
    from otk.sheets.tpho2564_physics._shared import CHARGE, ELECTRON

    return sqrt(2 * CHARGE * depth * volts / (ELECTRON * gap) + (launch * 1e3) ** 2) / 1e3


def check(volts=100.0, gap=10.0, depth=5.0, launch=100.0):
    from otk.sheets.tpho2564_physics._shared import CHARGE, ELECTRON

    # integrate the motion in the uniform field step by step
    accel = CHARGE * volts / (gap * 1e-3) / ELECTRON
    x, v, target = 0.0, launch * 1e3, depth * 1e-3
    dt = target / v / 2000 if v else 1e-12
    while x + v * dt + 0.5 * accel * dt * dt < target:
        x += v * dt + 0.5 * accel * dt * dt
        v += accel * dt
    return sqrt(v * v + 2 * accel * (target - x)) / 1e3


PARAMS = {"volts": 100.0, "gap": 10.0, "depth": 5.0, "launch": 100.0}
VARIANTS = [{"volts": 250.0}, {"depth": 9.0}, {"launch": 500.0}]
ANSWER = 4194.8780514201
TOL = 1e-9
