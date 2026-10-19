"""MC7: constant-speed uphill motor, weight2000N, length20m,time80s,sin37=3/5,cos37=4/5,mu.20. Power380W includes work against gravity and kinetic friction."""

from math import sqrt


def solve(weight=2000, length=20, time=80, sine=0.6, mu=0.2):
    return weight * (sine + mu * sqrt(1 - sine * sine)) * length / time


def check(weight=2000, length=20, time=80, sine=0.6, mu=0.2):
    cosine = sqrt(1 - sine * sine)
    tangent = (cosine, sine)
    displacement = (length * cosine, length * sine)
    gravity = (0.0, -weight)
    normal = (-weight * cosine * sine, weight * cosine * cosine)
    friction = tuple(-mu * weight * cosine * x for x in tangent)
    motor = tuple(-a - b - c for a, b, c in zip(gravity, normal, friction))
    return sum(f * x for f, x in zip(motor, displacement)) / time


PARAMS = {"weight": 2000, "length": 20, "time": 80, "sine": 0.6, "mu": 0.2}
VARIANTS = [{"mu": 0}, {"time": 40}, {"weight": 1000}]
ANSWER = 380.0
