"""ข้อ 7 — จำนวนสามสิ่งอันดับ (a, b, c) ที่ ab + bc + ca = 11

มีสามสิ่งอันดับ (a, b, c) ของจำนวนเต็มบวกทั้งหมดกี่ชุดซึ่งสอดคล้องกับสมการ
ab + bc + ca = 11

Ordered triples, so a solution and its rearrangements all count. Sorting a ≤ b ≤ c
there are two of them,

    (1, 1, 5):  1 + 5 + 5 = 11      → 3 arrangements
    (1, 2, 3):  2 + 6 + 3 = 11      → 6 arrangements

for **9** in total.

The search is bounded: with a ≤ b ≤ c every term is at least a·b, so
3ab ≤ ab+bc+ca only helps the other way — the usable bound is ab ≤ n, since
ab + bc + ca ≥ ab + a + b > ab. ``solve`` walks a ≤ b and derives c from
c(a+b) = n - ab, counting each sorted triple with its multinomial multiplicity.
``check`` is the flat triple loop over 1..n, which needs no bound argument at all.
"""

from __future__ import annotations

#: ab + bc + ca = target, over positive integers.
PARAMS = {"target": 11}
ANSWER = 9
VARIANTS = [
    {"target": 3},          # only (1,1,1)
    {"target": 12},
    {"target": 27},
    {"target": 47},
    {"target": 2},          # impossible: the smallest value is 3
]


def solve(target=11):
    """Ordered triples, counted from the sorted ones with their multiplicities."""
    if target < 3:
        return 0
    total = 0
    a = 1
    while a * a * 3 <= target:
        b = a
        while a * b + b + a <= target:
            rest = target - a * b
            if rest % (a + b) == 0:
                c = rest // (a + b)
                if c >= b:
                    distinct = len({a, b, c})
                    total += (1, 3, 6)[distinct - 1]
            b += 1
        a += 1
    return total


def check(target=11):
    """Independent: enumerate every ordered triple up to the target and test it."""
    if target < 3:
        return 0
    top = target
    n = 0
    for a in range(1, top + 1):
        for b in range(1, top + 1):
            if a * b + a + b > target:
                break
            rest = target - a * b
            if rest % (a + b) == 0 and rest // (a + b) >= 1:
                n += 1
    return n
