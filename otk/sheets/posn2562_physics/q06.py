"""MC6 figure: mass in horizontal circular motion inside a smooth cone, vertical axis and apex on ground, orbit height h. v=sqrt(gh), source answer4; independent of cone half-angle beta. Normal verticalN sin(beta)=mg, inwardN cos(beta)=mv^2/r, r=h tan(beta)."""

from math import sqrt, sin, cos, tan, radians


def solve(height=5, g=10, beta=30):
    return sqrt(g * height)


def check(height=5, g=10, beta=30):
    angle = radians(beta)
    radius = height * tan(angle)
    mass = 2.3
    normal = mass * g / sin(angle)
    lo, hi = 0.0, 1000.0
    for _ in range(100):
        speed = (lo + hi) / 2
        if mass * speed**2 / radius < normal * cos(angle):
            lo = speed
        else:
            hi = speed
    return (lo + hi) / 2


PARAMS = {"height": 5, "g": 10, "beta": 30}
VARIANTS = [{"height": 10}, {"beta": 45}, {"beta": 60}]
ANSWER = 7.0710678118654755
