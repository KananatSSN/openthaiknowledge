"""วันที่สอง ข้อ 1 — ทุก x มี y ∈ {2, 5, 13} ที่ xy − 1 ไม่เป็นกำลังสอง  (พิสูจน์)

2x − 1 an odd square gives x ≡ 1 (mod 4), so 5x − 1 = 4u² and 13x − 1 = 4v², and
2x = (v − u)(v + u) would be divisible by 4 though x is odd. The solver counts
x ≤ L with all three of 2x − 1, 5x − 1, 13x − 1 squares, walking the squares of
2x − 1: none.

``check`` tests every x ≤ L directly.
"""

from __future__ import annotations

from math import isqrt

PARAMS = {"limit": 200000}
ANSWER = 0
VARIANTS = [{"limit": 10}, {"limit": 5000}, {"limit": 60000}]


def _square(v):
    return v >= 0 and isqrt(v) ** 2 == v


def solve(limit=200000):
    count, s = 0, 1
    while s * s + 1 <= 2 * limit:
        x = (s * s + 1) // 2
        if (s * s + 1) % 2 == 0 and _square(5 * x - 1) and _square(13 * x - 1):
            count += 1
        s += 2
    return count


def check(limit=200000):
    return sum(1 for x in range(1, limit + 1) if all(_square(y * x - 1) for y in (2, 5, 13)))
