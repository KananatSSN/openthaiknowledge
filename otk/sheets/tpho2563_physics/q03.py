"""Theory 1.1 c): drops at terminal speed u0 = d0/T0 lit with period T0 + tau sin(wt) drift by u0 tau sin(wt)/T0, so the apparent motion has amplitude A = d0 tau/(T0^2 w). Adapted: the drop spacing (cm), interval T0 (s), modulation tau (ms) and modulation period (s) vary; returns mm."""

from math import pi


def solve(spacing=10.0, interval=0.02, swing=0.1, period=10.0):
    w = 2 * pi / period
    return spacing * 1e-2 * swing * 1e-3 / (interval**2 * w) * 1e3


def check(spacing=10.0, interval=0.02, swing=0.1, period=10.0):
    from math import sin

    # the solution's direct route: add the extra flash delays for a quarter cycle
    w = 2 * pi / period
    u0 = spacing * 1e-2 / interval
    flashes = round(pi / (2 * w * interval))
    return u0 * sum(swing * 1e-3 * sin(n * w * interval) for n in range(1, flashes + 1)) * 1e3


PARAMS = {"spacing": 10.0, "interval": 0.02, "swing": 0.1, "period": 10.0}
VARIANTS = [{"spacing": 20.0}, {"period": 20.0}, {"swing": 0.05}]
ANSWER = 39.788735772973844
TOL = 1e-2
