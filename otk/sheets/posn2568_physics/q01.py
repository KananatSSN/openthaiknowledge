"""Short1 figure: launched from O at u, 45 deg from the vertical; at A (still rising) the velocity is 60 deg from the vertical. Height of A = u^2 (sin^2 a - cos^2 a tan^2 b)/(2g) with a, b the elevations (45, 30): u^2/(6g). Inputs: elevations by (sin^2 a, tan^2 b); metres, g = 10."""

from math import asin, cos, sin, sqrt


def solve(speed=6, sin2=0.5, tan2=1 / 3, g=10):
    return speed**2 * (sin2 - (1 - sin2) * tan2) / (2 * g)


def check(speed=6, sin2=0.5, tan2=1 / 3, g=10):
    # Step the flight until the velocity's elevation drops to b.
    a = asin(sqrt(sin2))
    target = sqrt(tan2)
    vx, vy, y, dt = speed * cos(a), speed * sin(a), 0.0, 1e-6
    while vy / vx > target:
        y += vy * dt - g * dt * dt / 2
        vy -= g * dt
    return y


PARAMS = {"speed": 6, "sin2": 0.5, "tan2": 1 / 3, "g": 10}
VARIANTS = [{"speed": 10, "sin2": 0.75, "tan2": 1}, {"tan2": 0}, {"speed": 20, "sin2": 0.75, "tan2": 1 / 3}]
TOL = 1e-4
ANSWER = 0.6000000000000001
