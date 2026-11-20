"""MC19 figure: loop radius R carrying i, centre O; M on the axis at a on one side, N at b on the other. B_N / B_M = ((R^2 + a^2)/(R^2 + b^2))^(3/2) (answer 4)."""

from math import cos, sin, pi


def _axial_field(radius, z, n=4000):
    # Biot-Savart sum of the axial component, units mu0 i / (4 pi) = 1.
    total = 0.0
    for k in range(n):
        phi = 2 * pi * k / n
        dl = (-sin(phi) * 2 * pi * radius / n, cos(phi) * 2 * pi * radius / n, 0.0)
        r = (-radius * cos(phi), -radius * sin(phi), z)
        r3 = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** 1.5
        total += (dl[0] * r[1] - dl[1] * r[0]) / r3
    return total


def solve(radius=12, a=5, b=9):
    return ((radius**2 + a**2) / (radius**2 + b**2)) ** 1.5


def check(radius=12, a=5, b=9):
    return _axial_field(radius, -b) / _axial_field(radius, a)


PARAMS = {"radius": 12, "a": 5, "b": 9}
VARIANTS = [{"a": 16, "b": 5}, {"a": 9, "b": 16}, {"radius": 3, "a": 4, "b": 1}]
ANSWER = 0.6509629629629629
