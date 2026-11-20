"""Part2 item 4 figure: a heavy rope of mass M hangs between equal-height poles, making theta with the vertical at each top; tension at the lowest point (Mg/2) tan(theta). Input tan theta; newtons, g = 10."""

from math import asinh, sinh


def solve(mass=4, tangent=0.75, g=10):
    return mass * g / 2 * tangent


def check(mass=4, tangent=0.75, g=10):
    # Catenary y = c cosh(x/c) (weight per length 1 N/m, so H = c): slope at
    # the top cot(theta) = sinh(x_e/c), half arc length c sinh(x_e/c) = Mg/2.
    cot = 1 / tangent
    lo, hi = 1e-6, 1e7
    for _ in range(300):
        c = (lo + hi) / 2
        if c * sinh(asinh(cot)) < mass * g / 2:
            lo = c
        else:
            hi = c
    return (lo + hi) / 2


PARAMS = {"mass": 4, "tangent": 0.75, "g": 10}
VARIANTS = [{"tangent": 4 / 3}, {"mass": 10, "tangent": 5 / 12}, {"mass": 1, "tangent": 2}]
ANSWER = 15.0
