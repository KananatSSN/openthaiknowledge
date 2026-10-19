"""Short8 figure: R1 in series with R2 || R; the total equals R when R^2 - R1 R - R1 R2 = 0, R = (R1 + sqrt(R1^2 + 4 R1 R2))/2. Ohms."""

from math import sqrt


def solve(first=1, second=6):
    return (first + sqrt(first * first + 4 * first * second)) / 2


def check(first=1, second=6):
    # Bisect on R for the fixed point of the network.
    def total(r):
        return first + second * r / (second + r)

    lo, hi = 1e-9, 1e6
    for _ in range(300):
        mid = (lo + hi) / 2
        if total(mid) > mid:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"first": 1, "second": 6}
VARIANTS = [{"first": 2, "second": 12}, {"first": 4, "second": 15}, {"first": 3, "second": 2}]
TOL = 1e-9
ANSWER = 3.0
