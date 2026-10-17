"""MC1: E=h f implies h has dimensions M L² T^-1. Source non-equivalent unit is N s/m. Generalize E=k f^power; return(M,L,T) exponents, not a claim that photon energy changes its frequency law."""

from itertools import product


def solve(power=1):
    return (1, 2, power - 2)


def check(power=1):
    target = (1, 2, -2)
    for mass, length, time in product(range(-6, 7), repeat=3):
        if (mass, length, time - power) == target:
            return (mass, length, time)
    raise ValueError("outside independent dimension search")


PARAMS = {"power": 1}
VARIANTS = [{"power": 2}, {"power": 3}, {"power": 4}]
ANSWER = (1, 2, -1)
