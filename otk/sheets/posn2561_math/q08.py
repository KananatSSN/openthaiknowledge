"""ข้อ 8 — จำนวนสับเซตที่ผลบวกของสมาชิกน้อยสุดกับมากสุดเท่ากับ 23

กำหนดให้ A = {1, 2, 3, 4, 5, …, 22} จงหาจำนวนสับเซต S ของ A ซึ่งผลบวกของสมาชิก
ที่มีค่าน้อยที่สุดของ S กับสมาชิกที่มีค่ามากที่สุดของ S เท่ากับ 23

Fix the two extremes and everything in between is free. The pairs (m, M) with
m < M and m + M = 23 are

    (1, 22), (2, 21), …, (11, 12)

— eleven of them — and for each, the ``M − m − 1`` elements strictly between them
may be included or not, in any combination. So the count is

    Σ 2^(M−m−1) = 2²⁰ + 2¹⁸ + … + 2⁰ = Σ_{j=0}^{10} 4^j = (4¹¹ − 1)/3
                = **1398101**

A singleton {m} has min = max = m, so it qualifies when ``2m`` hits the target —
impossible for an odd target like 23, which is why every subset counted here has
at least two elements. For an **even** target the singleton is real and has to be
added; ``check``'s brute-force sweep over small universes is what caught that
case being missed.

``solve`` sums that geometric series. ``check`` enumerates the pairs and counts
the free middles as a power of two per pair — and for small universes it also
walks every subset outright, so the "everything between is free" step is tested
rather than assumed.
"""

from __future__ import annotations

from itertools import combinations

#: A = {1..size}, and the required min + max.
PARAMS = {"size": 22, "target": 23}
ANSWER = 1398101
VARIANTS = [
    {"size": 22, "target": 24},
    {"size": 8, "target": 9},
    {"size": 10, "target": 11},
    {"size": 22, "target": 45},        # only (22, 23): out of range
    {"size": 15, "target": 16},
    {"size": 22, "target": 2},         # m = M = 1: no valid pair
]


def solve(size=22, target=23):
    """Σ over the (min, max) pairs of 2^(gap − 1)."""
    if size < 1 or target < 1:
        return None
    total = 0
    for low in range(1, size + 1):
        high = target - low
        if high <= low or high > size:
            continue
        total += 2 ** (high - low - 1)
    if target % 2 == 0 and 1 <= target // 2 <= size:
        total += 1                       # the singleton {target/2}
    return total


def check(size=22, target=23):
    """Independent: enumerate the pairs, and for small A every subset as well.

    The pair loop counts the free middles directly, and when the universe is
    small enough every subset of A is generated and tested on its own min and
    max — so the claim that the middle elements are unconstrained is verified on
    real subsets before being trusted at size 22.
    """
    if size < 1 or target < 1:
        return None
    total = 0
    for low in range(1, size + 1):
        for high in range(low + 1, size + 1):
            if low + high != target:
                continue
            total += 1 << (high - low - 1)
    for single in range(1, size + 1):
        if single + single == target:
            total += 1

    if size <= 16:
        brute = 0
        universe = range(1, size + 1)
        for count in range(1, size + 1):
            for subset in combinations(universe, count):
                if min(subset) + max(subset) == target:
                    brute += 1
        assert brute == total, f"pair count {total} but {brute} subsets"
    return total
