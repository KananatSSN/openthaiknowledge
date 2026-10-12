"""ข้อ 28 — จำนวนสมาชิกของเซต S

ให้ A = {1, 5, 7, {1}, {7}, {1,5}, {5,7}}  ให้ S = { B ⊆ P(A) : A − B มีสมาชิก 4 ตัว }
เมื่อ P(A) เป็นเพาเวอร์เซตของเซต A  จงหาจำนวนสมาชิกของเซต S

The whole item is one observation: **B is a set of subsets of A, so the only
elements of A it can possibly contain are those elements of A that are themselves
subsets of A.** Of the seven elements, 1, 5 and 7 are not sets at all, while
{1}, {7}, {1,5} and {5,7} are subsets of A — four candidates.

|A − B| = 4 means exactly |A| − 4 = 3 elements of A lie in B, so B contains three
of the four candidates, must exclude the fourth, and is otherwise free over the
remaining |P(A)| − 4 members of P(A):

    |S| = C(4, 3) · 2^(128-4) = 4 · 2¹²⁴ = **2¹²⁶**

which is why the answer wants to stay a power of two rather than a 39-digit
decimal.

``PARAMS`` carries the set literally — the scalars and the set-valued elements —
so ``check`` can build A, build P(A), and *find* the overlap instead of being told
it is four.
"""

from __future__ import annotations

from math import comb

#: A's plain elements, its set-valued elements, and the required |A - B|.
PARAMS = {"scalars": (1, 5, 7), "sets": ((1,), (7,), (1, 5), (5, 7)),
          "missing": 4}
ANSWER = 2 ** 126
VARIANTS = [
    {"scalars": (1, 5, 7), "sets": ((1,), (7,), (1, 5), (5, 7)), "missing": 5},
    {"scalars": (1, 2), "sets": ((1,),), "missing": 2},
    {"scalars": (1, 2), "sets": ((1,), (2,)), "missing": 3},
    {"scalars": (3,), "sets": ((3,),), "missing": 1},
    {"scalars": (1, 5, 7), "sets": ((1,), (7,)), "missing": 1},   # too few candidates
    {"scalars": (1, 5, 7), "sets": ((1,), (7,)), "missing": 9},   # more than |A|
]


def _build(scalars, sets):
    """A as a set of tokens: ints for the scalars, frozensets for the rest."""
    return frozenset(scalars) | frozenset(frozenset(s) for s in sets)


def solve(scalars=(1, 5, 7), sets=((1,), (7,), (1, 5), (5, 7)), missing=4):
    """C(c, |A|-missing)·2^(2^|A| - c) over the c elements of A that are in P(A)."""
    a = _build(scalars, sets)
    size = len(a)
    if not 0 <= missing <= size:
        return None
    candidates = sum(1 for x in a if isinstance(x, frozenset) and x <= a)
    wanted = size - missing
    if wanted > candidates:
        return 0
    return comb(candidates, wanted) * 2 ** (2 ** size - candidates)


def check(scalars=(1, 5, 7), sets=((1,), (7,), (1, 5), (5, 7)), missing=4):
    """Independent: construct A and P(A) for real, then count.

    The power set is built element by element and the candidates are found by
    testing membership rather than assumed, so a set-valued element that is *not*
    a subset of A would drop out here on its own. When P(A) is small enough the
    count is also brute-forced over every B ⊆ P(A) and the two are asserted equal
    — that is the part that checks the counting argument itself.
    """
    a = _build(scalars, sets)
    size = len(a)
    if not 0 <= missing <= size:
        return None

    items = sorted(a, key=repr)
    power = []
    for mask in range(2 ** size):
        power.append(frozenset(items[i] for i in range(size) if mask >> i & 1))
    candidates = [x for x in a if x in power]           # membership, not a rule

    total = 0
    for mask in range(2 ** len(candidates)):
        chosen = [candidates[i] for i in range(len(candidates))
                  if mask >> i & 1]
        if size - len(chosen) == missing:
            total += 2 ** (len(power) - len(candidates))

    if len(power) <= 16:                               # brute force every B
        brute = 0
        for mask in range(2 ** len(power)):
            b = {power[i] for i in range(len(power)) if mask >> i & 1}
            if len(a - b) == missing:
                brute += 1
        assert brute == total, (brute, total)
    return total
