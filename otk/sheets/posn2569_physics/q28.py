"""Part2 item 18 figure: m slides from rest down a smooth wedge M (height h) on a smooth floor and runs on along the floor. Momentum m v = M V and energy (1/2)(m v^2 + M V^2) = m g h give V/sqrt(2gh) = m/sqrt(M (M + m))."""

from math import sqrt


def solve(small=1, big=3):
    return small / sqrt(big * (big + small))


def check(small=1, big=3, height=1.0, g=10.0):
    # Bisect on the wedge speed using both conservation laws.
    lo, hi = 0.0, sqrt(2 * g * height)
    for _ in range(200):
        wedge = (lo + hi) / 2
        block = big * wedge / small
        if 0.5 * small * block**2 + 0.5 * big * wedge**2 < small * g * height:
            lo = wedge
        else:
            hi = wedge
    return (lo + hi) / 2 / sqrt(2 * g * height)


PARAMS = {"small": 1, "big": 3}
VARIANTS = [{"small": 2, "big": 2}, {"small": 1, "big": 8}, {"small": 5, "big": 4}]
ANSWER = 0.2886751345948129
