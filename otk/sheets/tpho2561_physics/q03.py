"""Theory 1.1 c): between impacts the beam turns 2 theta0 while the mass flies L cos(theta0) horizontally at v sin(theta0), so omega = 2 theta0 v sin(theta0)/(L cos theta0); with ML omega = 6mv this gives m/M = theta0 tan(theta0)/3 (theta0 in radians). Adapted: theta0 (degrees) varies; returns m/M."""

from math import radians, tan


def solve(angle=30.0):
    t = radians(angle)
    return t * tan(t) / 3


def check(angle=30.0, speed=3.0, g=9.8):
    # Build the motion: L from the projectile, flight time from the vertical
    # motion, omega = 2 theta0/T, then M from M L omega = 6 m v with m = 1.
    from math import cos, sin

    t = radians(angle)
    L = 2 * speed**2 * sin(t) / g
    flight = 2 * speed * cos(t) / g
    omega = 2 * t / flight
    beam = 6 * 1.0 * speed / (L * omega)
    return 1.0 / beam


PARAMS = {"angle": 30.0}
VARIANTS = [{"angle": 45.0}, {"angle": 20.0}, {"angle": 60.0}]
ANSWER = 0.10076663134634539
TOL = 1e-9
