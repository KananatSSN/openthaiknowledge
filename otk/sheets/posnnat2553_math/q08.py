"""ข้อ 8 — สับเซต 70 ตัวต้องมี d(m, n) ≤ 36 (d = ระยะวนรอบมอดุโล 2553)  (พิสูจน์)

Sorted around the cycle of length L, the k gaps add to L, so one is at most
⌊L/k⌋ = ⌊2553/70⌋ = 36, and spacing the residues evenly attains it. The solver
returns ⌊L/k⌋.

``check`` finds the largest d for which k residues with all circular gaps ≥ d
fit (greedy placement), by trying d upward.
"""

from __future__ import annotations

PARAMS = {"length": 2553, "size": 70}
ANSWER = 36
VARIANTS = [{"length": 100, "size": 7}, {"length": 2553, "size": 71}, {"length": 50, "size": 50}]


def solve(length=2553, size=70):
    return length // size


def check(length=2553, size=70):
    best = 0
    for d in range(1, length + 1):
        points = [i * d for i in range(size)]
        if points[-1] < length and length - points[-1] >= d:
            best = d
        else:
            break
    return best
