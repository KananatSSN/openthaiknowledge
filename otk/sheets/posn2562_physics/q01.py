"""MC1: resistivity has SI unit ohm m, from R=rho L/A. Source n=0 asks rho; adapted quantity rho/L^n has exponents(ohm,m)=(1,1-n). Rho is always ordinary resistivity, not a changed material law."""

from itertools import product


def solve(n=0):
    return 1, 1 - n


def check(n=0):
    # Find the unknown unit by dimensional balance R=(X L^n)L/A.
    for resistance, length in product(range(-5, 6), repeat=2):
        if (resistance, length + n + 1 - 2) == (1, 0):
            return resistance, length
    raise ValueError("outside dimension grid")


PARAMS = {"n": 0}
VARIANTS = [{"n": 1}, {"n": 2}, {"n": 3}]
ANSWER = (1, 1)
