"""Theory 1(a) figure: string of length 2H over a small pulley H above OX; end A moves along OX at v0 from O, the mass m starts at y = 0. Geometry (v0 t)^2 + H^2 = (H + y)^2 gives v = v0^2 t/(H + y) = v0^2 t/sqrt(v0^2 t^2 + H^2). Adapted: numbers for v0, H, t; m/s."""

from math import sqrt


def solve(speed=2, height=4, time=1.5):
    return speed**2 * time / sqrt(speed**2 * time**2 + height**2)


def check(speed=2, height=4, time=1.5):
    # Central difference of the height y(t): the slanted part of the 2H string
    # is the hypotenuse, the hanging part what is left of it.
    def y(t):
        hanging = 2 * height - sqrt((speed * t) ** 2 + height**2)
        return height - hanging

    h = 1e-6
    return (y(time + h) - y(time - h)) / (2 * h)


PARAMS = {"speed": 2, "height": 4, "time": 1.5}
VARIANTS = [{"time": 0}, {"speed": 5, "height": 12, "time": 1}, {"height": 0.5, "time": 3}]
ANSWER = 1.2
TOL = 1e-6
