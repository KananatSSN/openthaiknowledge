"""ข้อ 28 — คู่อันดับ (x,y) ของจำนวนเต็มบวกทั้งหมดที่สอดคล้องกับระบบสมการ

จงหาคู่อันดับ (x, y) ของจำนวนเต็มบวกทั้งหมดที่สอดคล้องกับระบบสมการ
(√x)^(x+y) = y¹²  และ  (√y)^(x+y) = x³

Clearing the square roots gives x^(x+y) = y²⁴ and y^(x+y) = x⁶. Taking logs, with
s = (x+y)/2,

    s·ln x = 12·ln y,   s·ln y = 3·ln x

and multiplying the two gives s²·ln x·ln y = 36·ln x·ln y. **Dividing by
ln x·ln y is exactly where the second solution hides**: for x, y > 1 it gives
s = 6, so x + y = 12 and x = y², hence y = 3, x = 9. But x = y = 1 makes both
logs zero and satisfies the original system trivially — 1 = 1 on both lines.

So the answer is **(1, 1) และ (9, 3)**, and an answer of just (9, 3) is the one
this item is set up to catch.

``solve`` handles the two cases separately: the trivial one by inspection, the
main one from s² = p·q and x = y^√(p/q). ``check`` runs an exact integer search
over a bounded box using ``pow`` on both cleared equations — no logarithms
anywhere, so the division that loses (1,1) cannot happen.
"""

from __future__ import annotations

import math

#: (√x)^(x+y) = y^p and (√y)^(x+y) = x^q.
PARAMS = {"p": 12, "q": 3}
ANSWER = ((1, 1), (9, 3))
VARIANTS = [
    {"p": 8, "q": 2},
    {"p": 27, "q": 3},
    {"p": 3, "q": 3},
    {"p": 12, "q": 12},
    {"p": 20, "q": 5},
    {"p": 5, "q": 2},          # s² = 10 is not a square: only the trivial pair
]


def solve(p=12, q=3):
    """(1,1) always, plus the branch with s = √(pq) and x = y^(p/s)."""
    if p <= 0 or q <= 0:
        return None
    found = {(1, 1)}                      # both sides are 1 regardless of p, q
    prod = p * q
    s = math.isqrt(prod)
    if s * s == prod and s > 0:
        # x + y = 2s and ln x / ln y = p/s, so x = y^(p/s) when that is integral
        if p % s == 0:
            power = p // s
            for y in range(2, 2 * s):
                x = y ** power
                if x + y == 2 * s:
                    found.add((x, y))
    return tuple(sorted(found))


def check(p=12, q=3):
    """Independent: exact integer search on the cleared equations.

    x^(x+y) = y^(2p) and y^(x+y) = x^(2q) are both integer identities, so every
    pair in a bounded box can simply be tested with ``pow``. No logarithm is
    taken and nothing is divided, which is what makes (1,1) impossible to lose.
    """
    if p <= 0 or q <= 0:
        return None
    limit = 4 * max(p, q, math.isqrt(p * q) + 1)
    if limit > 200:
        return None
    found = []
    for x in range(1, limit + 1):
        for y in range(1, limit + 1):
            s = x + y
            if s * max(math.log2(x) if x > 1 else 1,
                       math.log2(y) if y > 1 else 1) > 4000:
                continue                  # keep the exponentiation bounded
            if pow(x, s) == pow(y, 2 * p) and pow(y, s) == pow(x, 2 * q):
                found.append((x, y))
    return tuple(sorted(found))
