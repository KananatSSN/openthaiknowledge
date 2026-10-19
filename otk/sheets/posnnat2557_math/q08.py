"""ข้อ 8 — จำนวนบัตร m! น้อยที่สุดที่ได้ผลรวมทุก t ≤ n!

n! − 1 = Σ j·j! (j < n) is the factorial-base representation with the largest
digit sum, n(n − 1)/2, so that many cards below n! are needed; and those sum to
at most n! − 1 unless one more card is added. j copies of j! for j < n plus an
extra 1! reach everything: n(n − 1)/2 + 1.

``check`` searches multisets of the cards 1!, …, n! by size and returns the
smallest size whose subset sums cover 1..n!.
"""

from __future__ import annotations

from itertools import combinations_with_replacement
from math import factorial

PARAMS = {"n": 4}
ANSWER = 7
VARIANTS = [{"n": 2}, {"n": 3}, {"n": 5}]


def solve(n=4):
    return n * (n - 1) // 2 + 1


def check(n=4):
    target = factorial(n)
    values = [factorial(m) for m in range(1, n + 1)]
    full = (1 << (target + 1)) - 1
    size = 1
    while True:
        for cards in combinations_with_replacement(values, size):
            if sum(cards) < target:
                continue
            reach = 1
            for v in cards:
                reach |= reach << v
            if reach & full == full:
                return size
        size += 1
