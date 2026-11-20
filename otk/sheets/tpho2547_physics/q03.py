"""Theory 1(e): at t = 0 the mass is at rest with acceleration v0^2/H upward, so T = m(g + v0^2/H). Adapted: numbers for m, v0, H; newtons with g = 10."""


def solve(mass=2, speed=2, height=4, g=10):
    return mass * (g + speed**2 / height)


def check(mass=2, speed=2, height=4, g=10):
    # Acceleration from a second difference of y(t) at t = 0, then Newton's law.
    from math import sqrt

    def y(t):
        return sqrt((speed * t) ** 2 + height**2) - height

    h = 1e-4
    a = (y(h) - 2 * y(0) + y(-h)) / (h * h)
    return mass * g + mass * a


PARAMS = {"mass": 2, "speed": 2, "height": 4, "g": 10}
VARIANTS = [{"speed": 0}, {"mass": 0.5, "speed": 3, "height": 1}, {"g": 9.8}]
ANSWER = 22.0
TOL = 1e-6
