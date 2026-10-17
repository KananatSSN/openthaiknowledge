"""Written2 figure: smooth wedge slopes down right bytheta; wedge and smooth vertical right wall accelerate LEFT bya. Ball stays fixed relative to wedge/wall. Wall forceR=m(a+g tan theta). Return forceN."""

from math import sin, cos, tan, radians
import numpy as np


def solve(mass=1, acceleration=2, theta=30, g=9.8):
    return mass * (acceleration + g * tan(radians(theta)))


def check(mass=1, acceleration=2, theta=30, g=9.8):
    angle = radians(theta)
    # Unknown ramp normal N, wall reaction R. x positive right.
    normal, wall = np.linalg.solve(
        [[sin(angle), -1], [cos(angle), 0]], [-mass * acceleration, mass * g]
    )
    assert normal > 0 and wall > 0
    return float(wall)


PARAMS = {"mass": 1, "acceleration": 2, "theta": 30, "g": 9.8}
VARIANTS = [{"mass": 2}, {"theta": 45}, {"acceleration": 5}]
ANSWER = 7.658032638058333
