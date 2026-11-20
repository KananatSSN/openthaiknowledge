"""Short21: item 20 with g0 = 9.83, T = 23 h 56 min, R = 6370 km: g = 9.83 - (7.29e-5)^2 x 6.37e6 = 9.80 m/s^2 to three figures. Returns the unrounded value."""

from math import pi


def solve(polar=9.83, hours=23, minutes=56, radius_km=6370):
    period = 3600 * hours + 60 * minutes
    return polar - (2 * pi / period) ** 2 * radius_km * 1000


def check(polar=9.83, hours=23, minutes=56, radius_km=6370):
    # Speed of a point on the equator, then v^2 / R.
    period = 3600 * hours + 60 * minutes
    speed = 2 * pi * radius_km * 1000 / period
    return polar - speed * speed / (radius_km * 1000)


PARAMS = {"polar": 9.83, "hours": 23, "minutes": 56, "radius_km": 6370}
VARIANTS = [{"hours": 10, "minutes": 0}, {"radius_km": 3390, "polar": 3.73, "hours": 24, "minutes": 37}, {"hours": 5}]
ANSWER = 9.796124338194979
