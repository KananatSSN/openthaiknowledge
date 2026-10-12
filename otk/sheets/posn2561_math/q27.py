"""ข้อ 27 — จำนวนที่ใช้เลขโดดครบชุดที่กำหนดพอดี

กำหนด A(n) แทนเซตของเลขโดดที่เขียนแทนจำนวนนับ n เช่น A(191) = {1, 9} และ
A(2018) = {0, 1, 2, 8} จงหา |P| เมื่อ P = { n ∈ ℕ | A(n) = {0, 4, 7} และ n ≤ 10000 }

``A(n)`` is a *set*, so a digit may repeat and the condition is "every digit is
one of 0, 4, 7 **and** all three actually occur". The bound rules out anything of
five digits except 10000 itself, whose digit set is {0, 1}, so only lengths 3 and
4 can qualify (two digits cannot hold three distinct values).

Three digits: the three digits must be a permutation of 0, 4, 7, and the leading
one cannot be 0 — 3! − 2! = **4**.

Four digits: strings over {0, 4, 7} with a nonzero lead number 2·3³ = 54, and
inclusion–exclusion removes those missing a value:

    54 − (16 + 8 + 8) + (1 + 1 + 0) = **24**

(16 strings avoid 0; 8 avoid 4; 8 avoid 7; 1 is all-7s, 1 all-4s, and an all-0
string has no legal lead.) Total |P| = 4 + 24 = **28**.

``solve`` runs a digit walk over the bound, carrying the set of values used so
far as a bitmask, so it handles a limit that is not a power of ten. ``check``
tests every n up to the limit with ``set(str(n))``.
"""

from __future__ import annotations

from functools import lru_cache

#: A(n) must equal exactly this set of digits, for n ≤ limit.
PARAMS = {"digits": (0, 4, 7), "limit": 10000}
ANSWER = 28
VARIANTS = [
    {"digits": (1, 2), "limit": 10000},
    {"digits": (0, 1), "limit": 5000},
    {"digits": (3, 5, 9), "limit": 100000},
    {"digits": (0, 4, 7), "limit": 7777},
    {"digits": (7,), "limit": 10000},
    {"digits": (0, 1, 2, 8), "limit": 10000},
]


def solve(digits=(0, 4, 7), limit=10000):
    """A digit walk over the bound, carrying which of the values have appeared."""
    allowed = tuple(sorted(set(digits)))
    if not allowed or any(d < 0 or d > 9 for d in allowed) or limit < 1:
        return None
    slot = {d: i for i, d in enumerate(allowed)}
    text = str(limit)
    width = len(text)
    complete = (1 << len(allowed)) - 1

    @lru_cache(maxsize=None)
    def walk(position: int, tight: bool, started: bool, used: int) -> int:
        if position == width:
            return 1 if started and used == complete else 0
        top = int(text[position]) if tight else 9
        total = 0
        for digit in range(top + 1):
            still_tight = tight and digit == top
            if not started and digit == 0:            # still in the leading zeros
                total += walk(position + 1, still_tight, False, 0)
                continue
            if digit not in slot:
                continue
            total += walk(position + 1, still_tight, True,
                          used | (1 << slot[digit]))
        return total

    result = walk(0, True, False, 0)
    walk.cache_clear()
    return result


def check(digits=(0, 4, 7), limit=10000):
    """Independent: read the digits of every n up to the limit."""
    allowed = set(digits)
    if not allowed or any(d < 0 or d > 9 for d in allowed) or limit < 1:
        return None
    if limit > 2 * 10 ** 6:
        return None
    wanted = {str(d) for d in allowed}
    return sum(1 for n in range(1, limit + 1) if set(str(n)) == wanted)
