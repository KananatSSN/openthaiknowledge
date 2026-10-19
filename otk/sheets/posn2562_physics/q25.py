"""Short25 figure: uniformpositive ringradiusR inYZplane, linechargedensitylambda. OnpositiveXaxis x, Ex=lambda R x/[2epsilon0(R^2+x^2)^(3/2)]. ReturncoefficientE/(lambda/epsilon0). Generator keepsx>0, asksmagnitude; sourcex isdistance."""

from math import pi, sin, cos, sqrt


def solve(radius=2, distance=3):
    return radius * abs(distance) / (2 * (radius * radius + distance * distance) ** 1.5)


def check(radius=2, distance=3):
    # Integrate all3 electricfieldcomponents of pointchargeelements.
    steps = 2000
    components = [0.0, 0.0, 0.0]
    dphi = 2 * pi / steps
    for i in range(steps):
        phi = (i + 0.5) * dphi
        vector = (distance, -radius * cos(phi), -radius * sin(phi))
        separation = sqrt(sum(v * v for v in vector))
        charge = radius * dphi
        for axis in range(3):
            components[axis] += charge * vector[axis] / (4 * pi * separation**3)
    assert abs(components[1]) < 1e-10 and abs(components[2]) < 1e-10
    return abs(components[0])


PARAMS = {"radius": 2, "distance": 3}
VARIANTS = [{"distance": 0}, {"distance": 2}, {"radius": 3, "distance": 1}]
ANSWER = 0.06400386879521874
