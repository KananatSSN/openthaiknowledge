"""ข้อ 2 — ระบบสมการรากที่สอง

ถ้า a, b เป็นจำนวนจริงที่สอดคล้องกับ
    √(a+b) + √(a−b) = s        (สรุปในโจทย์: s = 5)
    a² − b² = p                (สรุปในโจทย์: p = 36)
ค่าของ a² + 3b² เท่ากับเท่าใด

Method: put u = √(a+b), v = √(a−b). Then u + v = s and (uv)² = (a+b)(a−b) = p,
so uv = √p and u, v are the roots of t² − s·t + √p. That gives
    a = (u²+v²)/2 = (s² − 2√p)/2 ,   b = (u²−v²)/2 = s·(u−v)/2
and b² = s²(s² − 4√p)/4 — which is symmetric in the two root orderings, so both
branches give the *same* a² + 3b². (The sheet's own numbers hit that: the two
solutions are b = ±5/2.)

``check`` never touches this algebra: it eliminates a via a = √(p + b²) and
bisects the remaining one-variable equation for b.
"""

from __future__ import annotations

import math
from fractions import Fraction

PARAMS = {"s": 5, "p": 36}
ANSWER = 61
VARIANTS = [
    {"s": 6, "p": 16},
    {"s": 7, "p": 81},
    {"s": 4, "p": 4},
    {"s": 10, "p": 144},
    {"s": 5, "p": 30},          # √p irrational — falls back to float
]


def _root(p):
    """√p exactly when p is a perfect square, else as a float."""
    if isinstance(p, int) and p >= 0 and math.isqrt(p) ** 2 == p:
        return Fraction(math.isqrt(p))
    return math.sqrt(p)


def solve(s=5, p=36):
    """a² + 3b² for the system above. Requires s² ≥ 4√p (real u, v)."""
    r = _root(p)
    if s * s < 4 * r:
        raise ValueError(f"no real solution: s²={s * s} < 4√p={4 * r}")
    exact = isinstance(r, Fraction)
    s2 = Fraction(s) ** 2 if exact else float(s) ** 2
    a = (s2 - 2 * r) / 2
    b2 = s2 * (s2 - 4 * r) / 4
    return a * a + 3 * b2


def check(s=5, p=36):
    """Independent: a = √(p+b²), then bisect √(a+b) + √(a−b) = s for b ≥ 0."""
    def f(b):
        a = math.sqrt(p + b * b)
        return math.sqrt(a + b) + math.sqrt(a - b) - s

    # f is increasing in b (u = √(a+b) grows faster than v = √(a−b) shrinks),
    # starting at f(0) = 2·p^¼ − s ≤ 0 whenever a solution exists.
    lo, hi = 0.0, 1.0
    while f(hi) < 0:
        hi *= 2
        if hi > 1e9:
            raise ValueError("no bracket for b")
    for _ in range(400):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2
    a = math.sqrt(p + b * b)
    return a * a + 3 * b * b
