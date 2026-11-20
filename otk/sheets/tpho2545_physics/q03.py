"""Theory I.2b: magnetic drag L^2 B^2 v / R slows the rod of mass M: v = v0 exp(-L^2 B^2 t/(M R)). Returns v at time t (m/s)."""

from math import exp


def solve(speed=4, separation=0.5, field=2, mass=0.5, resistance=1, time=1):
    return speed * exp(-(separation * field) ** 2 * time / (mass * resistance))


def check(speed=4, separation=0.5, field=2, mass=0.5, resistance=1, time=1):
    # Step M dv/dt = -L^2 B^2 v / R.
    v, dt = float(speed), 1e-6
    for _ in range(int(time / dt)):
        v -= (separation * field) ** 2 * v / (mass * resistance) * dt
    return v


PARAMS = {"speed": 4, "separation": 0.5, "field": 2, "mass": 0.5, "resistance": 1, "time": 1}
VARIANTS = [{"time": 2}, {"mass": 1, "field": 1}, {"resistance": 4, "time": 0.5}]
TOL = 1e-5
ANSWER = 0.5413411329464508
