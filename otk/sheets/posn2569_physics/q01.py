"""MC1 figure: equal masses, A at u hits B at rest head-on; afterwards both move on and the kinetic energy is 3/4 of before. v1 + v2 = u, v1^2 + v2^2 = (3/4) u^2, so v2/u = (1 + 1/sqrt2)/2 = (sqrt2 + 1)/sqrt8 (answer 2). Adapted: energy fraction f; v2/u = (1 + sqrt(2f - 1))/2."""

from math import sqrt


def solve(fraction=0.75):
    return (1 + sqrt(2 * fraction - 1)) / 2


def check(fraction=0.75):
    # Bisect on v2 (u = 1, v2 >= 1/2 so B leads) until the energy matches.
    lo, hi = 0.5, 1.0
    for _ in range(200):
        v2 = (lo + hi) / 2
        if (1 - v2) ** 2 + v2**2 < fraction:
            lo = v2
        else:
            hi = v2
    return (lo + hi) / 2


PARAMS = {"fraction": 0.75}
VARIANTS = [{"fraction": 5 / 9}, {"fraction": 0.625}, {"fraction": 13 / 18}]
ANSWER = 0.8535533905932737
