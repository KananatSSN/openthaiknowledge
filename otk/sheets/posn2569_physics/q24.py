"""Part2 item 14 figure: a uniform plate M, width a (hanging side) and length b (top edge), hung from the middle of its top edge, with m at a lower corner: tan(theta) = m b/(a(M + 2m)), so tan(theta) a/b = m/(M + 2m)."""

from math import cos, sin


def solve(plate=4, hung=1):
    return hung / (plate + 2 * hung)


def check(plate=4, hung=1, length=60.0, width=10.0):
    # Torque-balance bisection, then tan * width / length.
    def torque(t):
        return plate * (width / 2) * sin(t) + hung * (-(length / 2) * cos(t) + width * sin(t))

    lo, hi = 0.0, 1.5707
    for _ in range(200):
        mid = (lo + hi) / 2
        if torque(mid) < 0:
            lo = mid
        else:
            hi = mid
    t = (lo + hi) / 2
    return sin(t) / cos(t) * width / length


PARAMS = {"plate": 4, "hung": 1}
VARIANTS = [{"hung": 2}, {"plate": 1, "hung": 3}, {"plate": 10}]
TOL = 1e-9
ANSWER = 0.16666666666666666
