"""Written3 figure: cylinder onincline60deg held by horizontal rope RIGHT tangent at TOP, not center. Static friction uphill equals rope tension by torque balance. T/W=sin(theta)/(1+cos(theta))=1/sqrt3. Assume sufficient static friction."""

from math import radians, tan, sin, cos
import numpy as np


def solve(theta=60):
    return tan(radians(theta) / 2)


def check(theta=60):
    angle = radians(theta)
    # Solve horizontal, vertical, and torque equations for T,N,f with W=1.
    tension, normal, friction = np.linalg.solve(
        [[1, -sin(angle), cos(angle)], [0, cos(angle), sin(angle)], [-1, 0, 1]], [0, 1, 0]
    )
    assert normal > 0 and friction > 0
    return float(tension)


PARAMS = {"theta": 60}
VARIANTS = [{"theta": 30}, {"theta": 45}, {"theta": 75}]
ANSWER = 0.5773502691896257
