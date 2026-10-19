"""MC15 graph: I=60A atV30V, wire length20cm, conductivity(2.5e6/pi)(ohm m)^-1. Conductance2S, radius.4mm. sigma_pi means coefficient in conductivity=sigma_pi/pi."""

from math import sqrt, pi


def solve(length_cm=20, current=60, voltage=30, sigma_pi=2500000):
    return 1000 * sqrt(length_cm / 100 * current / (voltage * sigma_pi))


def check(length_cm=20, current=60, voltage=30, sigma_pi=2500000):
    # Rebuild actual SI wire area and predict graph current from trial radius.
    lo, hi = 0.0, 100.0
    for _ in range(100):
        radius_mm = (lo + hi) / 2
        area = pi * (radius_mm / 1000) ** 2
        predicted = (sigma_pi / pi) * area / (length_cm / 100) * voltage
        if predicted < current:
            lo = radius_mm
        else:
            hi = radius_mm
    return (lo + hi) / 2


PARAMS = {"length_cm": 20, "current": 60, "voltage": 30, "sigma_pi": 2500000}
VARIANTS = [{"current": 15}, {"length_cm": 80}, {"sigma_pi": 10000000}]
ANSWER = 0.4
