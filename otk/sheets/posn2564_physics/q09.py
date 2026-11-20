"""MC9 figure: semicircle ABC radius R in the YZ plane centred on O (A and C on the Z axis, B on the Y axis) carries total charge q; P on the X axis at distance x. Every element is sqrt(x^2 + R^2) from P, so V = (q/4 pi eps0)/sqrt(x^2 + R^2) (answer 1). Returns V / (k q) in m^-1."""

from math import cos, sin, pi, sqrt


def solve(radius=3, distance=4):
    return 1 / sqrt(distance**2 + radius**2)


def check(radius=3, distance=4):
    # Add the potential of 2000 equal elements along the half circle.
    n = 2000
    total = 0.0
    for k in range(n):
        phi = pi * (k + 0.5) / n
        y, z = radius * sin(phi), radius * cos(phi)
        total += 1 / sqrt(distance**2 + y * y + z * z) / n
    return total


PARAMS = {"radius": 3, "distance": 4}
VARIANTS = [{"radius": 5, "distance": 12}, {"radius": 12, "distance": 5}, {"radius": 2, "distance": 7}]
ANSWER = 0.2
