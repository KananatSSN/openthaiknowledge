"""Short23 figure: wheelrollsRIGHT withoutslip, clockwise angularspeedomega. Rimpoint angle theta measured CLOCKWISE fromUPWARDvertical radius. Speed relativefixedgroundO=2Romega|cos(theta/2)|, equivalentlyRomega sqrt(2+2cos theta), notspeedrelativecenter."""

from math import cos, sin, radians, hypot


def solve(radius=2, omega=3, theta=60):
    return 2 * radius * omega * abs(cos(radians(theta) / 2))


def check(radius=2, omega=3, theta=60):
    # Groundcoordinates of a cycloid; differentiate by symmetric differences.
    h = 1e-5
    phase = radians(theta)

    def position(time):
        angle = phase + omega * time
        return radius * omega * time + radius * sin(angle), radius + radius * cos(angle)

    before, after = position(-h), position(h)
    return hypot((after[0] - before[0]) / (2 * h), (after[1] - before[1]) / (2 * h))


TOL = 1e-8

PARAMS = {"radius": 2, "omega": 3, "theta": 60}
VARIANTS = [{"theta": 0}, {"theta": 180}, {"theta": 120}]
ANSWER = 10.392304845413264
