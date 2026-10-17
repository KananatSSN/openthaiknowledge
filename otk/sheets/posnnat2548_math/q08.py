"""ข้อ 8 — ผลบวกผลลัพธ์สลับเครื่องหมายของทุกสับเซตของ {1, …, 7}

Pair each subset T without n with T ∪ {n}: their results add to n, and there are
2^(n − 1) pairs ({n} with ∅). Total n·2^(n − 1) = 448.

``check`` evaluates every non-empty subset.
"""

from __future__ import annotations

from itertools import combinations

PARAMS = {"n": 7}
ANSWER = 448
VARIANTS = [{"n": 1}, {"n": 3}, {"n": 10}, {"n": 12}]


def solve(n=7):
    return n * 2 ** (n - 1)


def check(n=7):
    total = 0
    for r in range(1, n + 1):
        for subset in combinations(range(n, 0, -1), r):
            total += sum(v if i % 2 == 0 else -v for i, v in enumerate(subset))
    return total
