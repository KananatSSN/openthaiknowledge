"""MC6: with three different resistors, used singly, in pairs or all three, series/parallel in every way: 3 + 6 + 8 = 17 values for generic values (answer 7). Adapted: given values; returns the number of distinct resistances."""

from fractions import Fraction
from itertools import combinations


def _par(*rs):
    return 1 / sum(Fraction(1) / r for r in rs)


def solve(values=(1, 3, 7)):
    a = [Fraction(v) for v in values]
    found = set(a)
    for x, y in combinations(a, 2):
        found |= {x + y, _par(x, y)}
    x, y, z = a
    found |= {x + y + z, _par(x, y, z)}
    for p, q, r in ((x, y, z), (y, x, z), (z, x, y)):
        found |= {p + _par(q, r), _par(p, q + r)}
    return len(found)


def check(values=(1, 3, 7)):
    # Recursive enumeration of every series-parallel network on each subset.
    def networks(items):
        if len(items) == 1:
            return {items[0]}
        out = set()
        n = len(items)
        for mask in range(1, (1 << n) - 1):
            left = tuple(items[i] for i in range(n) if mask >> i & 1)
            right = tuple(items[i] for i in range(n) if not mask >> i & 1)
            for a in networks(left):
                for b in networks(right):
                    out |= {a + b, a * b / (a + b)}
        return out

    a = tuple(Fraction(v) for v in values)
    found = set()
    for k in range(1, len(a) + 1):
        for subset in combinations(a, k):
            found |= networks(subset)
    return len(found)


PARAMS = {"values": (1, 3, 7)}
VARIANTS = [{"values": (1, 2, 3)}, {"values": (2, 3, 6)}, {"values": (4, 5, 11)}]
ANSWER = 17
