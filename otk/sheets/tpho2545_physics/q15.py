"""Experiment 1a: Newton cooling dT/dt = -(T - Ta)/beta gives T = Ta + (T0 - Ta) exp(-t/beta). Returns T at time t (deg C)."""

from math import exp


def solve(room=30, start=90, beta=600, time=600):
    return room + (start - room) * exp(-time / beta)


def check(room=30, start=90, beta=600, time=600):
    temp, dt = float(start), 0.01
    for _ in range(int(time / dt)):
        temp -= (temp - room) / beta * dt
    return temp


PARAMS = {"room": 30, "start": 90, "beta": 600, "time": 600}
VARIANTS = [{"time": 1200}, {"beta": 300, "time": 300}, {"room": 25, "start": 85, "time": 900}]
TOL = 1e-4
ANSWER = 52.07276647028654
