"""ข้อ 16 — จำนวน (A, B, C) ที่ A ∪ B ∪ C = {1, …, 2549}

Each element picks a non-empty subset of the k sets to lie in: (2^k − 1)^n,
written "7^2549" because the number has 2154 digits.

``check`` counts by inclusion–exclusion on the elements left uncovered,
Σⱼ (−1)ʲ C(n, j)·2^(k(n−j)), as an integer, then recovers the base as the
integer n-th root and writes the same form.
"""

from __future__ import annotations

import math
from math import comb

PARAMS = {"k": 3, "n": 2549}
ANSWER = "7^2549"
VARIANTS = [{"k": 2, "n": 5}, {"k": 4, "n": 100}, {"k": 5, "n": 3000}, {"n": 1}]


def solve(k=3, n=2549):
    return f"{2**k - 1}^{n}"


def check(k=3, n=2549):
    value = sum((-1) ** j * comb(n, j) * 2 ** (k * (n - j)) for j in range(n + 1))
    base = round(math.exp(math.log(value) / n))
    assert base**n == value
    return f"{base}^{n}"
