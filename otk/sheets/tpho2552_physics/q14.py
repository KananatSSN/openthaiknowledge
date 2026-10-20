"""Lab 1: the Hall sensor's sensitivity is the change of V_out per gauss; with the coil's field B (gauss) at the sensor, sensitivity = dV/B. Adapted: synthetic dV (mV) at the coil field from q13's formula; mV/G."""

from math import pi, sqrt


def solve(change=5.0, side=10.0, distance=5.0, turns=130, current=4.8 / 5.2):
    a, x = side / 100, distance / 100
    b = 4e-7 * pi * a * a * current * turns / (2 * pi) / ((x * x + a * a / 4) * sqrt(x * x + a * a / 2)) * 1e4
    return change / b


def check(change=5.0, side=10.0, distance=5.0, turns=130, current=4.8 / 5.2):
    # The field from a Biot-Savart sum, as in q13's check.
    from otk.sheets.tpho2552_physics.q13 import check as field

    return change / field(side=side, distance=distance, turns=turns, current=current)


PARAMS = {"change": 5.0, "side": 10.0, "distance": 5.0, "turns": 130, "current": 4.8 / 5.2}
VARIANTS = [{"change": 2.0}, {"distance": 10.0, "change": 1.5}, {"side": 6.0, "change": 3.0}]
ANSWER = 0.9021097956087906
TOL = 1e-5
