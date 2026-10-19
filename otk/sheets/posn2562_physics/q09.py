"""MC9 figure: uniformly charged insulating semicircle radiusR, line densitylambda. Vcenter=lambda/(4epsilon0), source answer4. General arc anglephi; normalized potential V/(lambda/epsilon0)=phi/(4pi); positive radius cancels."""

from fractions import Fraction
from math import pi, sin, cos, hypot


def solve(angle=180, radius=1):
    return Fraction(angle, 720)


def check(angle=180, radius=1):
    # Integrate potentials of midpoint point-charges along the physical arc.
    steps = 1000
    dphi = angle * pi / 180 / steps
    potential = 0.0
    for i in range(steps):
        phi = (i + 0.5) * dphi
        position = (radius * cos(phi), radius * sin(phi))
        dq = radius * dphi
        potential += dq / (4 * pi * hypot(*position))
    return potential


PARAMS = {"angle": 180, "radius": 1}
VARIANTS = [{"angle": 90}, {"angle": 270}, {"radius": 3}]
ANSWER = Fraction(1, 4)
