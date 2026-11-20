"""MC17 figure: conical pendulum, string l, mass m moving in a horizontal circle of radius R. omega = (g / sqrt(l^2 - R^2))^(1/2) (answer 4)."""

from math import sqrt


def solve(length=5, radius=3, g=10):
    return sqrt(g / sqrt(length**2 - radius**2))


def check(length=5, radius=3, g=10):
    # Bisect on omega so the string's direction matches the force balance:
    # tan(alpha) = omega^2 R / g with sin(alpha) = R / l.
    sin_a = radius / length
    tan_a = sin_a / sqrt(1 - sin_a * sin_a)
    lo, hi = 0.0, 100.0
    for _ in range(200):
        w = (lo + hi) / 2
        if w * w * radius / g < tan_a:
            lo = w
        else:
            hi = w
    return (lo + hi) / 2


PARAMS = {"length": 5, "radius": 3, "g": 10}
VARIANTS = [{"length": 13, "radius": 5}, {"length": 10, "radius": 6}, {"length": 2, "radius": 1}]
ANSWER = 1.5811388300841898
