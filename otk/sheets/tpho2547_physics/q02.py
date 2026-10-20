"""Theory 1(b): a = (v0^2 - v^2)/(H + y) = v0^2 H^2/(v0^2 t^2 + H^2)^(3/2). Adapted: numbers for v0, H, t; m/s^2."""

from math import sqrt


def solve(speed=2, height=4, time=1.5):
    return speed**2 * height**2 / (speed**2 * time**2 + height**2) ** 1.5


def check(speed=2, height=4, time=1.5):
    # Second difference of y(t) = sqrt(v0^2 t^2 + H^2) - H.
    def y(t):
        return sqrt((speed * t) ** 2 + height**2) - height

    h = 1e-4
    return (y(time + h) - 2 * y(time) + y(time - h)) / (h * h)


PARAMS = {"speed": 2, "height": 4, "time": 1.5}
VARIANTS = [{"time": 0}, {"speed": 5, "height": 12, "time": 1}, {"height": 0.5, "time": 3}]
ANSWER = 0.512
TOL = 1e-4
