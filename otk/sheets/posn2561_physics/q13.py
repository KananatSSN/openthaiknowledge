"""MC13: use all three resistors R,R,2R in two-terminal series/parallel networks without shorts. Largest4R; smallest2R/5; ratio10. Generalize resistor tuple; independent checker enumerates every series-parallel composition."""

from fractions import Fraction
from functools import lru_cache


def solve(resistors=(1, 1, 2)):
    return sum(Fraction(r) for r in resistors) * sum(1 / Fraction(r) for r in resistors)


@lru_cache(maxsize=128)
def networks(resistors):
    if len(resistors) == 1:
        return frozenset((Fraction(resistors[0]),))
    values = set()
    for mask in range(1, 1 << len(resistors)):
        if not mask & 1 or mask == (1 << len(resistors)) - 1:
            continue
        left = tuple(r for j, r in enumerate(resistors) if mask & (1 << j))
        right = tuple(r for j, r in enumerate(resistors) if not mask & (1 << j))
        for a in networks(left):
            for b in networks(right):
                values.update((a + b, a * b / (a + b)))
    return frozenset(values)


def check(resistors=(1, 1, 2)):
    values = networks(tuple(resistors))
    return max(values) / min(values)


PARAMS = {"resistors": (1, 1, 2)}
VARIANTS = [{"resistors": (1, 2, 3)}, {"resistors": (2, 3, 4)}, {"resistors": (1, 3, 5)}]
ANSWER = Fraction(10, 1)
