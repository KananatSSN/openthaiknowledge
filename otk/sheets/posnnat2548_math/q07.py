"""ข้อ 7 — เขียน 2548 เป็นผลบวกของจำนวนเต็มบวกสองจำนวนขึ้นไปโดยลำดับมีความสำคัญ

Bars in the N − 1 gaps between N ones: any non-empty set of bars, 2^(N−1) − 1.
The answer is kept in the form "2^(N−1)-1" because the number has 767 digits.

``check`` adds C(N − 1, k − 1) over k ≥ 2 parts as an integer, then writes it in
the same form (asserting it really is one less than a power of two).
"""

from __future__ import annotations

from math import comb

PARAMS = {"total": 2548}
ANSWER = "2^2547-1"
VARIANTS = [{"total": 2}, {"total": 10}, {"total": 570}, {"total": 3000}]


def solve(total=2548):
    return f"2^{total - 1}-1"


def check(total=2548):
    value = sum(comb(total - 1, k - 1) for k in range(2, total + 1))
    exponent = (value + 1).bit_length() - 1
    assert value + 1 == 1 << exponent
    return f"2^{exponent}-1"
