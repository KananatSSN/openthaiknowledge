"""ข้อ 20 — จำนวนสี่สิ่งอันดับ (a, b, c, d) ที่ a < b ≤ c < d

จงหาจำนวนของสี่สิ่งอันดับ (a, b, c, d) ทั้งหมดที่ a, b, c และ d เป็นเลขโดดซึ่ง
สอดคล้องกับ a < b ≤ c < d

Note the middle relation is ``≤`` while the outer two are ``<`` — that is what
makes the count a single binomial rather than a sum of two.

Over the digits 0..m the count is

    Σ_{b ≤ c} b·(m - c) = C(m + 2, 4),

which is C(11, 4) = **330** for m = 9. The clean way to see it: send
(a, b, c, d) ↦ (a, b, c+1, d+2); the four values become strictly increasing in
0..m+2, and every strictly increasing quadruple there comes back, so the count is
the number of 4-subsets of an (m+3)-element set.

``solve`` uses that binomial; ``check`` counts the quadruples one at a time.
"""

from __future__ import annotations

from math import comb

#: the digits run 0..top; the sheet's are the decimal digits, so top = 9.
PARAMS = {"top": 9}
ANSWER = 330
VARIANTS = [
    {"top": 3},
    {"top": 5},
    {"top": 11},
    {"top": 15},
    {"top": 2},          # the smallest range that admits any quadruple at all
    {"top": 1},          # too few values: none
]


def solve(top=9):
    """C(top+2, 4) — one strictly increasing quadruple in 0..top+2 per solution."""
    if top < 0:
        return None
    return comb(top + 2, 4)


def check(top=9):
    """Independent: enumerate the quadruples and test the chain as written."""
    if top < 0:
        return None
    n = 0
    for a in range(top + 1):
        for b in range(a + 1, top + 1):
            for c in range(b, top + 1):
                for d in range(c + 1, top + 1):
                    n += 1
    return n
