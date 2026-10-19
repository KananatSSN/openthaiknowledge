"""MC15 figure: two smooth equal discs radiusR, incomingA moving alongx, initiallyrest Bcenter is offseta perpendicular toincomingpath. Atfirstcontact centerseparation2R; B moves along lineofcenters so theta=asin(a/(2R)), source answer2. Positiveoffset0<a<2R."""

from math import asin, atan2, sqrt, pi


def solve(offset=1, radius=1):
    return asin(offset / (2 * radius)) * 180 / pi


def check(offset=1, radius=1):
    # Locate collision by bisection of actual center distance as A approaches.
    lo, hi = -3.0 * radius, 0.0
    for _ in range(100):
        x = (lo + hi) / 2
        if sqrt(x * x + offset * offset) > 2 * radius:
            lo = x
        else:
            hi = x
    x = (lo + hi) / 2
    normal = (-x, offset)
    assert abs(sqrt(normal[0] ** 2 + normal[1] ** 2) - 2 * radius) < 1e-9
    return atan2(normal[1], normal[0]) * 180 / pi


PARAMS = {"offset": 1, "radius": 1}
VARIANTS = [{"offset": 0.5}, {"radius": 2}, {"offset": 1.5}]
ANSWER = 30.000000000000004
