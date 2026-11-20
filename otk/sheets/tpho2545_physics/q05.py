"""Theory I.4 figure: a solid sphere (radius r) rolls without slipping from rest at theta0 in a bowl of radius R; its largest spin rate (at the bottom) is sqrt(10 g (R - r)(1 - cos theta0)/(7 r^2)). rad/s; input cos theta0."""

from math import acos, sin, sqrt


def solve(bowl=1.0, ball=0.1, cosine=0.5, g=10):
    return sqrt(10 * g * (bowl - ball) * (1 - cosine) / (7 * ball * ball))


def check(bowl=1.0, ball=0.1, cosine=0.5, g=10):
    # Integrate theta'' = -(5/7) g sin(theta)/(R - r) from rest at theta0 to
    # the bottom; spin = (R/r - 1) theta'.
    theta, rate, dt = acos(cosine), 0.0, 1e-6
    while theta > 0:
        rate -= 5 / 7 * g * sin(theta) / (bowl - ball) * dt
        theta += rate * dt
    return abs(rate) * (bowl / ball - 1)


PARAMS = {"bowl": 1.0, "ball": 0.1, "cosine": 0.5, "g": 10}
VARIANTS = [{"cosine": 0.8}, {"bowl": 2.0, "ball": 0.5}, {"cosine": 0.0, "ball": 0.2}]
TOL = 1e-4
ANSWER = 25.354627641855497
