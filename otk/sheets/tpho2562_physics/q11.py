"""Theory 3.1: the Sun's output sigma T^4 4 pi R^2 spreads over 4 pi d^2, so I = sigma T^4 R^2/d^2 and T = (I d^2/(sigma R^2))^(1/4) = 5.80e3 K for I = 1400 W/m^2, d = 1.5e11 m and R = 7.0e8 m. Adapted: the measured intensity and the distance (1e11 m) vary; returns kelvin."""


def solve(intensity=1400.0, distance=1.5, radius=7.0):
    d, r = distance * 1e11, radius * 1e8
    return (intensity * d**2 / (5.67e-8 * r**2)) ** 0.25


def check(intensity=1400.0, distance=1.5, radius=7.0):
    from math import pi

    from otk.sheets.tpho2562_physics._shared import bisect

    d, r = distance * 1e11, radius * 1e8
    output = 4 * pi * d**2 * intensity
    return bisect(lambda t: 5.67e-8 * t**4 * 4 * pi * r**2 - output, 1.0, 1e5)


PARAMS = {"intensity": 1400.0, "distance": 1.5, "radius": 7.0}
VARIANTS = [{"intensity": 1000.0}, {"distance": 2.0}, {"radius": 5.0}]
ANSWER = 5802.73655141035
TOL = 1e-9
