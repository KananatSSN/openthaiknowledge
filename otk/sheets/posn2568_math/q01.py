"""ข้อ 1 — ค่ามากที่สุดของ a+b+c จากสมการเชิงเส้นบนเลขโดด

ถ้า a, b, c ∈ {1,2,3,…,9} สอดคล้องกับสมการ  a + 32b + 48c = 504
แล้วค่ามากที่สุดของ a + b + c เท่ากับเท่าใด

Method: with the leading coefficient 1, ``a`` is pinned once b and c are chosen,
so the search is only over (b, c) — a is forced to ``total - cb*b - cc*c`` and
simply has to land in range. ``check`` is the naive triple loop.
"""

from __future__ import annotations

PARAMS = {"cb": 32, "cc": 48, "total": 504, "lo": 1, "hi": 9}
ANSWER = 21
VARIANTS = [
    {"total": 456},
    {"cb": 25, "cc": 37, "total": 400},
    {"cb": 11, "cc": 13, "total": 150},
    {"lo": 0, "hi": 9},
    {"cb": 32, "cc": 48, "total": 504, "hi": 12},
]


def solve(cb=32, cc=48, total=504, lo=1, hi=9):
    """Largest a+b+c over digits in [lo, hi] with a + cb*b + cc*c == total.

    Returns None when the equation has no solution in range.
    """
    best = None
    for b in range(lo, hi + 1):
        for c in range(lo, hi + 1):
            a = total - cb * b - cc * c
            if lo <= a <= hi:
                best = max(best or a + b + c, a + b + c)
    return best


def check(cb=32, cc=48, total=504, lo=1, hi=9):
    """Independent: enumerate every triple and filter."""
    sums = [a + b + c
            for a in range(lo, hi + 1)
            for b in range(lo, hi + 1)
            for c in range(lo, hi + 1)
            if a + cb * b + cc * c == total]
    return max(sums) if sums else None


def witness(cb=32, cc=48, total=504, lo=1, hi=9):
    """The (a, b, c) achieving the maximum — used for the generator's hint."""
    best = None
    for a in range(lo, hi + 1):
        for b in range(lo, hi + 1):
            for c in range(lo, hi + 1):
                if a + cb * b + cc * c == total:
                    if best is None or a + b + c > sum(best):
                        best = (a, b, c)
    return best
