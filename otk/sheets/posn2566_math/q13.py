"""ข้อ 13 — จำนวนสามสิ่งอันดับของเซตที่ยูเนียนเต็มและอินเตอร์เซกชันว่าง

จงหาจำนวนของสามสิ่งอันดับของเซต (A, B, C) ทั้งหมดที่สอดคล้องกับเงื่อนไข
    1) A ∪ B ∪ C = {1, 2, 3, …, 15}
    2) A ∩ B ∩ C = ∅

The two conditions are both **per element**, and they do not interact: element i
sits in some sub-collection of {A, B, C}, condition 1 forbids the empty one and
condition 2 forbids all three. So each of the 15 elements independently picks one
of 2³ − 2 = 6 patterns:

    **6¹⁵ = 470 184 984 576**

The trap is treating the conditions as global and reaching for inclusion–exclusion
over subsets of the universe; that works too but is fifteen terms long.

``solve`` raises the per-element count. ``check`` does exactly that longer route
— inclusion–exclusion over how many elements are left uncovered, summing
``(−1)^j C(n,j)(2^k − 1)^{n−j}`` — and for a small enough universe it enumerates
every triple outright instead.
"""

from __future__ import annotations

from itertools import product
from math import comb

#: universe size and how many sets are in the tuple.
PARAMS = {"universe": 15, "sets": 3}
ANSWER = 470184984576
VARIANTS = [
    {"universe": 1},
    {"universe": 4},
    {"universe": 6, "sets": 2},
    {"universe": 5, "sets": 4},
    {"universe": 20},
    {"universe": 3, "sets": 3},
]


def solve(universe=15, sets=3):
    """Each element picks one of 2^k − 2 patterns, independently."""
    if universe < 0 or sets < 1:
        return None
    return (2 ** sets - 2) ** universe


def check(universe=15, sets=3):
    """Independent: enumerate for a small universe, else inclusion–exclusion.

    The sum ``Σ_j (−1)^j C(n,j) (2^k − 1)^{n−j}`` counts the triples whose triple
    intersection is empty and then removes, term by term, those that fail to
    cover — a completely different bookkeeping from the per-element product.
    """
    if universe < 0 or sets < 1:
        return None
    if sets <= 3 and universe <= 6:
        total = 0
        for assignment in product(range(2 ** sets), repeat=universe):
            if all(m not in (0, 2 ** sets - 1) for m in assignment):
                total += 1
        return total
    return sum((-1) ** j * comb(universe, j) * (2 ** sets - 1) ** (universe - j)
               for j in range(universe + 1))
