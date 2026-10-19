"""ข้อ 2 — เวลาน้อยสุดในการส่งวัคซีน 63 หลัง

Elf Eᵢ to house d takes i·d minutes; the task time is the largest i·d. Pair the
slowest elves with the nearest houses: Eᵢ → house N + 1 − i, so every time is
i(N + 1 − i) ≤ ⌊(N + 1)²/4⌋. Conversely the elves i ≥ ⌈(N + 1)/2⌉ and the houses
d ≥ ⌈(N + 1)/2⌉ cannot all avoid each other, so some pair costs that much.
N = 63 gives 32·32 = 1024.

``check`` finds the least T with a complete assignment of i·d ≤ T. Each elf may
take any house up to ⌊T/i⌋, a prefix, so an assignment exists iff, with the
capacities sorted, the j-th smallest is at least j (Hall). For N ≤ 7 it also
tries every assignment.
"""

from __future__ import annotations

from itertools import permutations

PARAMS = {"houses": 63}
ANSWER = 1024
VARIANTS = [{"houses": 1}, {"houses": 6}, {"houses": 7}, {"houses": 100}]


def solve(houses=63):
    return (houses + 1) ** 2 // 4


def _feasible(n, t):
    caps = sorted(min(n, t // i) for i in range(1, n + 1))
    return all(c >= j for j, c in enumerate(caps, start=1))


def check(houses=63):
    n = houses
    t = 1
    while not _feasible(n, t):
        t += 1
    if n <= 7:
        brute = min(max(i * d for i, d in zip(range(1, n + 1), perm))
                    for perm in permutations(range(1, n + 1)))
        assert brute == t
    return t
