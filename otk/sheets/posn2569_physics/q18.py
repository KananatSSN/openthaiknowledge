"""Part2 item 8 figure: equal smooth spheres, elastic, glancing; theta is the angle between M1's velocity and the line of centres. M2 leaves at u cos(theta), M1 at u sin(theta): speed ratio tan(theta). Input sin theta."""

from math import asin, cos, sin, sqrt


def solve(sine=0.6):
    return sine / sqrt(1 - sine * sine)


def check(sine=0.6):
    t = asin(sine)
    n = (cos(t), -sin(t))
    j = n[0]  # u = 1
    va = (1 - j * n[0], -j * n[1])
    vb = (j * n[0], j * n[1])
    return sqrt(va[0] ** 2 + va[1] ** 2) / sqrt(vb[0] ** 2 + vb[1] ** 2)


PARAMS = {"sine": 0.6}
VARIANTS = [{"sine": 0.8}, {"sine": 5 / 13}, {"sine": 0.5}]
ANSWER = 0.7499999999999999
