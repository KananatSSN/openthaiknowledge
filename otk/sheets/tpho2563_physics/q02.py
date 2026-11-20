"""Theory 1.1 b): the apparent displacement at the n-th flash, u n dt + g (n dt)^2/2 with t = n(T0 + dt), is uniform acceleration a' = g (dt/(T0 + dt))^2. Adapted: the drop interval T0 (s) and the lag dt (ms) vary; returns mm/s^2 with g = 9.8."""


def solve(interval=0.05, lag=1.0):
    dt = lag * 1e-3
    return 9.8 * (dt / (interval + dt)) ** 2 * 1e3


def check(interval=0.05, lag=1.0, height=20.0):
    from math import sqrt

    dt = lag * 1e-3
    u = sqrt(2 * 9.8 * height * 1e-2)
    period = interval + dt
    s1 = u * dt + 0.5 * 9.8 * dt**2
    s2 = u * 2 * dt + 0.5 * 9.8 * (2 * dt) ** 2
    return (s2 - 2 * s1) / period**2 * 1e3


PARAMS = {"interval": 0.05, "lag": 1.0}
VARIANTS = [{"lag": 3.0}, {"lag": -2.0}, {"interval": 0.1}]
ANSWER = 3.767781622452903
TOL = 1e-9
