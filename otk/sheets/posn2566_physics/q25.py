"""Short25 figure: pendulum bob M released from the height of its pivot (string horizontal) swings down, sticks to m at rest at the bottom, and the pair rises to 60 deg from the vertical. (M/(M+m))^2 = 1 - cos 60, so M/m = sqrt2 + 1. Adapted: any final angle, given by its cosine."""

from math import sqrt


def solve(cosine=0.5):
    s = sqrt(1 - cosine)
    return s / (1 - s)


def check(cosine=0.5, length=1.0, g=10):
    # Bisect on M/m: speed before sqrt(2 g L), sticking collision, rise height.
    def rise_cosine(ratio):
        v0 = sqrt(2 * g * length)
        v = ratio * v0 / (ratio + 1)
        return 1 - v * v / (2 * g * length)

    lo, hi = 1e-9, 1e6
    for _ in range(300):
        mid = (lo + hi) / 2
        if rise_cosine(mid) > cosine:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"cosine": 0.5}
VARIANTS = [{"cosine": 0.75}, {"cosine": 5 / 9}, {"cosine": 16 / 25}]
TOL = 1e-9
ANSWER = 2.414213562373096
