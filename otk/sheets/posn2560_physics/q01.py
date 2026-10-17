"""Part1,1: dimensional analysis F=k v^p A. Source p2 gives dimensions of density. Return exponents (M,L,T)."""

from itertools import product


def solve(power=2):
    return (1, -1 - power, power - 2)


def check(power=2):
    for mass, length, time in product(range(-8, 9), repeat=3):
        if (mass, length + power + 2, time - power) == (1, 1, -2):
            return (mass, length, time)
    raise ValueError("outside search grid")


PARAMS = {"power": 2}
VARIANTS = [{"power": 1}, {"power": 3}, {"power": 4}]
ANSWER = (1, -3, 0)
