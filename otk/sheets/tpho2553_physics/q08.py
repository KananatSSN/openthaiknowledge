"""Theory 2.4: M y'' = -(P0 gamma (A - a)^2/V0) y, so T = 2 pi sqrt(3 M V0/(5 (Pa + Mg/(A - a)) (A - a)^2)) for helium. Adapted: numbers; seconds with g = 9.8."""

from math import pi, sqrt


def solve(outside=1.0e5, mass=20, big=0.05, small=0.01, volume=0.002, g=9.8):
    pressure = outside + mass * g / (big - small)
    return 2 * pi * sqrt(3 * mass * volume / (5 * pressure * (big - small) ** 2))


def check(outside=1.0e5, mass=20, big=0.05, small=0.01, volume=0.002, g=9.8):
    # Integrate the full adiabatic equation of motion from a small push and
    # time the period between upward zero crossings.
    pressure = outside + mass * g / (big - small)
    area = big - small

    def accel(y):
        p = pressure * (volume / (volume - y * area)) ** (5 / 3)
        return ((p - outside) * area - mass * g) / mass  # y measured downward, force upward

    y, v, t, dt = 1e-6, 0.0, 0.0, 1e-5
    crossings = []
    prev = y
    while len(crossings) < 3:
        v -= accel(y) * dt
        y += v * dt
        t += dt
        if (prev > 0 >= y) or (prev < 0 <= y):
            crossings.append(t)
        prev = y
    return crossings[2] - crossings[0]


PARAMS = {"outside": 1.0e5, "mass": 20, "big": 0.05, "small": 0.01, "volume": 0.002, "g": 9.8}
VARIANTS = [{"mass": 5}, {"volume": 0.005}, {"big": 0.03, "small": 0.02}]
ANSWER = 0.07513421508924445
TOL = 1e-3
