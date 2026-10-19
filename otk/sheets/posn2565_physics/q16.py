"""MC16 figure: tilt a rough incline slowly until m starts to slide (tan theta = mu_s), then hold it there. The block accelerates at g(sin theta - mu_k cos theta) = (mu_s - mu_k) g / sqrt(1 + mu_s^2) (answer 3). g = 10."""

from math import atan, cos, sin, sqrt


def solve(static=0.75, kinetic=0.5, g=10):
    return (static - kinetic) * g / sqrt(1 + static * static)


def check(static=0.75, kinetic=0.5, g=10):
    # Raise the angle in small steps until gravity along the slope exceeds the
    # largest static friction, then use kinetic friction at that angle.
    theta = 0.0
    while sin(theta) <= static * cos(theta):
        theta += 1e-6
    assert abs(theta - atan(static)) < 2e-6
    theta = atan(static)
    return g * (sin(theta) - kinetic * cos(theta))


PARAMS = {"static": 0.75, "kinetic": 0.5, "g": 10}
VARIANTS = [{"static": 4 / 3, "kinetic": 1}, {"static": 5 / 12, "kinetic": 0.25}, {"kinetic": 0.1}]
ANSWER = 2.0
