"""MC9 figure: ring of radius R with charge Q in the YZ plane; E(x) = kQx/(x^2 + R^2)^(3/2) is odd, with one positive and one negative peak (answer 7). Adapted quantity: E_x at x = -L (V/m), Q in nC, k = 9e9."""

from math import cos, pi, sin

K = 9e9


def solve(charge=5, radius=3, distance=4):
    return -K * charge * 1e-9 * distance / (radius**2 + distance**2) ** 1.5


def check(charge=5, radius=3, distance=4, n=4000):
    q = charge * 1e-9 / n
    ex = 0.0
    for k in range(n):
        p = 2 * pi * (k + 0.5) / n
        dx = -distance
        dy, dz = -radius * cos(p), -radius * sin(p)
        ex += K * q * dx / (dx * dx + dy * dy + dz * dz) ** 1.5
    return ex


PARAMS = {"charge": 5, "radius": 3, "distance": 4}
VARIANTS = [{"radius": 4, "distance": 3}, {"charge": 2, "radius": 12, "distance": 5}, {"distance": 8, "radius": 6}]
ANSWER = -1.44
