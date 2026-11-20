"""Theory II.e: with a pin (r -> 0) the hoop swings about a point on its rim: frequency (1/2 pi) sqrt(g/(2R)). Returns T/pi = 2 sqrt(2R/g)."""

from math import sqrt


def solve(hoop=0.5, g=10):
    return 2 * sqrt(2 * hoop / g)


def check(hoop=0.5, g=10):
    # Physical pendulum about a rim point: I = 2 M R^2, distance R:
    # T = 2 pi sqrt(I/(M g R)).
    return 2 * sqrt(2 * hoop * hoop / (g * hoop))


PARAMS = {"hoop": 0.5, "g": 10}
VARIANTS = [{"hoop": 2.0}, {"hoop": 0.2}, {"hoop": 1.25, "g": 9.8}]
ANSWER = 0.6324555320336759
