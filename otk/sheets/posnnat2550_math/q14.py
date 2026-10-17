"""ข้อ 14 — Σₖ₌₈₄⁸⁰⁰⁰ C(k, 84)C(8084 − k, 84) ในรูป C(a, b)

Choose a + b + 1 numbers from {0, …, n}; the (a + 1)-th smallest is k, with
C(k, a) choices below and C(n − k, b) above: the sum is C(n + 1, a + b + 1),
recorded as the pair (8085, 169).

``check`` adds the whole sum as an integer and returns the pair only if the
total equals that binomial coefficient.
"""

from __future__ import annotations

from math import comb

PARAMS = {"n": 8084, "a": 84, "b": 84}
ANSWER = (8085, 169)
VARIANTS = [{"n": 60, "a": 3, "b": 7}, {"n": 1146, "a": 19, "b": 74}, {"n": 20, "a": 0, "b": 0}]


def solve(n=8084, a=84, b=84):
    return (n + 1, a + b + 1)


def check(n=8084, a=84, b=84):
    total = sum(comb(k, a) * comb(n - k, b) for k in range(a, n - b + 1))
    for top in range(a + b, n + 3):
        if comb(top, a + b + 1) == total:
            return (top, a + b + 1)
    return None
