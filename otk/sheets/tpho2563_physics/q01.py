"""Theory 1.1 b): drops passing a height h at u = sqrt(2gh), lit every T0 + dt, appear displaced by u n dt + g (n dt)^2/2 at the n-th flash, so the apparent velocity is u' = sqrt(2gh) dt/(T0 + dt). Adapted: the height (cm), the drop interval T0 (s) and the lag dt (ms) vary; returns cm/s with g = 9.8."""

from math import sqrt


def solve(height=20.0, interval=0.05, lag=1.0):
    dt = lag * 1e-3
    return sqrt(2 * 9.8 * height * 1e-2) * dt / (interval + dt) * 1e2


def check(height=20.0, interval=0.05, lag=1.0):
    # the solution's second route: fit s = u't + a't^2/2 through two flashes
    dt = lag * 1e-3
    u = sqrt(2 * 9.8 * height * 1e-2)
    period = interval + dt
    s1 = u * dt + 0.5 * 9.8 * dt**2
    s2 = u * 2 * dt + 0.5 * 9.8 * (2 * dt) ** 2
    # s1 = v T + a T^2/2, s2 = 2 v T + 2 a T^2
    accel = (s2 - 2 * s1) / period**2
    return (s1 - 0.5 * accel * period**2) / period * 1e2


PARAMS = {"height": 20.0, "interval": 0.05, "lag": 1.0}
VARIANTS = [{"height": 50.0}, {"lag": -2.0}, {"interval": 0.1}]
ANSWER = 3.8821548771026135
TOL = 1e-9
