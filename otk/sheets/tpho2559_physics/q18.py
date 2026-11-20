"""Theory 3.6: with constant spin-up and spin-down rates of equal size tau2/I = kMg/I, one cycle takes t = 4 sqrt(n pi I/(k M g)) and the user's work is F1 b, so the mean power is (F1 b/4) sqrt(k M g/(n pi I)). Adapted: F1 (N), b (cm), n, M (kg), k (mm) and I (kg cm^2) vary; returns the power in watts with g = 9.8."""

from math import pi, sqrt


def solve(force=10.0, reach=3.0, turns=5, mass=1.0, k=0.3, inertia=10.0, g=9.8):
    return force * reach * 1e-2 / 4 * sqrt(k * 1e-3 * mass * g / (turns * pi * inertia * 1e-4))


def check(force=10.0, reach=3.0, turns=5, mass=1.0, k=0.3, inertia=10.0, g=9.8):
    # Spin down at kMg/I through 2 n pi: the peak speed, then the time to
    # spin up and down at that same rate.
    moment = inertia * 1e-4
    rate = k * 1e-3 * mass * g / moment
    peak = sqrt(2 * rate * 2 * turns * pi)
    period = 2 * peak / rate
    return force * reach * 1e-2 / period


PARAMS = {"force": 10.0, "reach": 3.0, "turns": 5, "mass": 1.0, "k": 0.3, "inertia": 10.0, "g": 9.8}
VARIANTS = [{"force": 15.0}, {"turns": 3, "inertia": 20.0}, {"mass": 2.0}]
ANSWER = 0.03244703296994792
TOL = 1e-9
