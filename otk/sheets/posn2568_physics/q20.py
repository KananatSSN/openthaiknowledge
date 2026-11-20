"""Short20: a uniform spherical Earth of radius R spinning with sidereal period T; at the pole g0, at the equator g = g0 - 4 pi^2 R / T^2. SI units."""

from math import pi


def solve(polar=9.83, period=86160, radius=6.37e6):
    return polar - 4 * pi**2 * radius / period**2


def check(polar=9.83, period=86160, radius=6.37e6):
    # Rotating frame: weight = gravity minus the centripetal requirement, with
    # the angular speed from one sidereal turn.
    omega = 2 * pi / period
    return polar - omega * omega * radius


PARAMS = {"polar": 9.83, "period": 86160, "radius": 6.37e6}
VARIANTS = [{"period": 3600 * 10}, {"radius": 3e6, "polar": 3.7}, {"period": 5000, "radius": 6.37e6}]
ANSWER = 9.796124338194979
