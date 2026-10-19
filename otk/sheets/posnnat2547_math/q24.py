"""วันที่สอง ข้อ 3 — แถว 18 คนที่ต้องสลับ 150 ครั้ง

Each swap of an adjacent out-of-order pair removes exactly one inversion, so the
number of swaps is the inversion count, at most C(18, 2) = 153. ``solve``
multiplies the generating polynomials Πᵢ(1 + x + ⋯ + x^(i−1)) and reads the
coefficient: 951.

``check`` uses the complement: reversing the line maps 150 inversions to 3, so it
enumerates the Lehmer codes (eᵢ ≤ i − 1) whose deficits sum to 153 − 150 = 3
directly.
"""

from __future__ import annotations

from itertools import combinations_with_replacement

PARAMS = {"n": 18, "swaps": 150}
ANSWER = 951
VARIANTS = [{"n": 9, "swaps": 34}, {"n": 12, "swaps": 61}, {"n": 6, "swaps": 15}, {"n": 20, "swaps": 186}]


def solve(n=18, swaps=150):
    counts = [1]
    for i in range(1, n + 1):
        new = [0] * (len(counts) + i - 1)
        for k, v in enumerate(counts):
            for j in range(i):
                new[k + j] += v
        counts = new
    return counts[swaps]


def check(n=18, swaps=150):
    deficit = n * (n - 1) // 2 - swaps
    count = 0
    # distribute the deficit as a multiset of positions i (2..n), each at most i − 1 times
    for positions in combinations_with_replacement(range(2, n + 1), deficit):
        if all(positions.count(i) <= i - 1 for i in set(positions)):
            count += 1
    return count
