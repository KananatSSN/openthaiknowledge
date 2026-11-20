"""Lab 1 figure: a prism of apex angle A at minimum deviation D_m has n = sin((A + D_m)/2)/sin(A/2). Adapted: synthetic A and D_m in degrees."""

from math import radians, sin


def solve(apex=60, deviation=38):
    return sin(radians(apex + deviation) / 2) / sin(radians(apex) / 2)


def check(apex=60, deviation=38):
    # Trace rays: find the incidence that minimises the deviation for the
    # candidate n, and bisect on n until that minimum equals D_m.
    from math import asin, degrees

    def minimum(n):
        best = 1e9
        for k in range(1, 9000):
            i = radians(k / 100)
            if sin(i) / n > 1:
                continue
            r1 = asin(sin(i) / n)
            r2 = radians(apex) - r1
            if n * sin(r2) >= 1 or r2 < 0:
                continue
            e = asin(n * sin(r2))
            best = min(best, degrees(i + e) - apex)
        return best

    lo, hi = 1.0001, 3.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if minimum(mid) < deviation else (lo, mid)
    return lo


PARAMS = {"apex": 60, "deviation": 38}
VARIANTS = [{"deviation": 45}, {"apex": 45, "deviation": 25}, {"apex": 30, "deviation": 18}]
ANSWER = 1.5094191604455443
TOL = 2e-4
