"""Short12 figure: water of depth h jets from a small hole at height y and lands x away: x^2 = 4y(h - y) = h^2 - 4(h/2 - y)^2. Adapted quantity: x itself, in metres."""

from math import sqrt


def solve(depth=1.0, hole=0.2, g=10):
    return 2 * sqrt(hole * (depth - hole))


def check(depth=1.0, hole=0.2, g=10):
    # Torricelli speed, then time-step the flight to the floor.
    speed = sqrt(2 * g * (depth - hole))
    x, y, vy, dt = 0.0, hole, 0.0, 1e-6
    while y > 0:
        vy -= g * dt
        y += vy * dt
        x += speed * dt
    return x


PARAMS = {"depth": 1.0, "hole": 0.2, "g": 10}
VARIANTS = [{"hole": 0.5}, {"depth": 2.0, "hole": 0.4}, {"depth": 5, "hole": 1}]
TOL = 1e-4
ANSWER = 0.8
