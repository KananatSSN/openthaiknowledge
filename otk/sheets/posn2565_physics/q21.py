"""MC21 figure: a planet moves round the Sun; besides energy, angular momentum m v r sin(theta) is conserved, theta the angle between v and r (answer 3). Adapted: speed at a second point from v1 r1 sin1 = v2 r2 sin2 (km/s, AU)."""

from math import asin, cos, sin, sqrt


def solve(speed=30, distance=1, sine=0.8, other_distance=2, other_sine=0.6):
    return speed * distance * sine / (other_distance * other_sine)


def check(speed=30, distance=1, sine=0.8, other_distance=2, other_sine=0.6):
    # Areal velocity: area swept per unit time is (1/2)|r x v| at both points.
    r1 = (distance, 0.0)
    a1 = asin(sine)
    v1 = (speed * cos(a1), speed * sin(a1))
    rate = abs(r1[0] * v1[1] - r1[1] * v1[0]) / 2
    a2 = asin(other_sine)
    r2 = (0.0, other_distance)
    # v2 at angle a2 to r2: components along r2 and perpendicular.
    unit = (sin(a2), cos(a2))  # angle measured from r2's direction (y axis)
    speed2 = 2 * rate / abs(r2[0] * unit[1] - r2[1] * unit[0])
    assert sqrt(unit[0] ** 2 + unit[1] ** 2) - 1 < 1e-12
    return speed2


PARAMS = {"speed": 30, "distance": 1, "sine": 0.8, "other_distance": 2, "other_sine": 0.6}
VARIANTS = [{"sine": 1}, {"other_distance": 4, "other_sine": 1}, {"speed": 13, "sine": 12 / 13, "other_sine": 5 / 13}]
ANSWER = 20.0
