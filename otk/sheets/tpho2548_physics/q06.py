"""Theory 1.4 figure: a light m bounces elastically between two resting masses M (m << M); treating each M as at rest, every collision leaves m the fraction ((M - m)/(M + m))^2 of its energy, so its energy is halved after n = ln 2/(-2 ln((M - m)/(M + m))) ~ (M/m) ln 2/4 collisions. The marking scheme's n ~ M/(8m) linearises (1 - 2m/M)^(2n) where 4nm/M = 1/2 is not small; its exact line gives the value used here. Returns the least whole number of collisions for which the energy is at most half."""

from math import ceil, log


def solve(ratio=100):
    keep = ((ratio - 1) / (ratio + 1)) ** 2
    return ceil(log(0.5) / log(keep) - 1e-12)


def check(ratio=100):
    # Collide m with a fresh resting M each time and count.
    big, small, v, count = float(ratio), 1.0, 1.0, 0
    start = v * v
    while v * v > start / 2:
        v = (small - big) * v / (small + big)
        count += 1
    return count


PARAMS = {"ratio": 100}
VARIANTS = [{"ratio": 800}, {"ratio": 40}, {"ratio": 1000}]
ANSWER = 18
