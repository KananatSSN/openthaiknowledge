"""ข้อ 10 — มี f : ℕ → ℕ ที่ f(m + f(n)) = f(m) + f(n) + f(n + 1) หรือไม่ (ไม่มี)

For f(m + f(n)) = f(m) + a·f(n) + b·f(n + 1): comparing f(m + f(n)f(k)) two ways
makes f geometric, and linearity along progressions then forces a constant c
with c = c + (a + b)c, impossible once b ≥ 1. With b = 0, f(n) = an + c works.
The solver returns whether a solution exists (a = b = 1: no).

``check`` tests the candidate families (linear, constant, affine shifts,
powers) on a grid and reports whether any satisfies the equation on a range.
"""

from __future__ import annotations

PARAMS = {"a": 1, "b": 1}
ANSWER = False
VARIANTS = [{"a": 2, "b": 0}, {"a": 0, "b": 0}, {"a": 3, "b": 2}]


def solve(a=1, b=1):
    return b == 0


def check(a=1, b=1):
    def satisfies(f):
        return all(f(m + f(n)) == f(m) + a * f(n) + b * f(n + 1) for m in range(1, 7) for n in range(1, 7))

    candidates = []
    for p in range(0, 5):
        for q in range(0, 6):
            candidates.append(lambda n, p=p, q=q: p * n + q)
    for base in range(2, 4):
        candidates.append(lambda n, base=base: base**n)
    return any(satisfies(f) and all(f(n) >= 1 for n in range(1, 10)) for f in candidates)
