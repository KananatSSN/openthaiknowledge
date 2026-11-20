"""Short23 figure: three equal masses M at the corners of an equilateral triangle of side D circle the centre: net pull sqrt3 G M^2/D^2 toward the centre at radius D/sqrt3, so T = 2 pi sqrt(D^3/(3 G M)). Returns T / pi for given D and GM."""

from math import cos, pi, sin, sqrt


def solve(side=3, gm=1):
    return 2 * sqrt(side**3 / (3 * gm))


def check(side=3, gm=1):
    # Vector-sum the two pulls on one star, then omega^2 r = |a|.
    r = side / sqrt(3)
    stars = [(r * cos(a), r * sin(a)) for a in (0, 2 * pi / 3, 4 * pi / 3)]
    ax = ay = 0.0
    for x, y in stars[1:]:
        dx, dy = x - stars[0][0], y - stars[0][1]
        d3 = (dx * dx + dy * dy) ** 1.5
        ax += gm * dx / d3
        ay += gm * dy / d3
    omega = sqrt(sqrt(ax * ax + ay * ay) / r)
    return 2 * pi / omega / pi


PARAMS = {"side": 3, "gm": 1}
VARIANTS = [{"side": 2, "gm": 6}, {"side": 6, "gm": 2}, {"side": 1, "gm": 3}]
ANSWER = 6.0
