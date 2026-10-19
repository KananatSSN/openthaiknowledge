"""MC3 figure: +pQ at (0,0) and -sQ at (2a,0); the field at (a,a) makes theta with OX, tan theta = (p - s)/(p + s); for p = 2, s = 1 it is 1/3 (answer 4). Returns tan theta."""

from math import sqrt


def solve(positive=2, negative=1):
    return (positive - negative) / (positive + negative)


def check(positive=2, negative=1):
    # Add Coulomb vectors in coordinates (a = 1, k Q = 1).
    def field(q, x0, y0, x=1.0, y=1.0):
        dx, dy = x - x0, y - y0
        r3 = sqrt(dx * dx + dy * dy) ** 3
        return q * dx / r3, q * dy / r3

    e1, e2 = field(positive, 0, 0), field(-negative, 2, 0)
    ex, ey = e1[0] + e2[0], e1[1] + e2[1]
    return ey / ex


PARAMS = {"positive": 2, "negative": 1}
VARIANTS = [{"positive": 3}, {"positive": 5, "negative": 2}, {"positive": 4, "negative": 3}]
ANSWER = 0.3333333333333333
