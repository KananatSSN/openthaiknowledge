"""ข้อ 2 — จำนวนสมาชิกของเซต A

ให้ A เป็นเซตของจำนวนเต็มบวก n ทั้งหมด โดยที่ n หาร 2024 เหลือเศษ 24
จำนวนสมาชิกของเซต A เท่ากับเท่าใด

"เหลือเศษ 24" carries two conditions, and the second is the one that is easy to
drop: 2024 = qn + 24 says n divides 2024 - 24 = 2000, and the remainder being a
*remainder* says n > 24. Without the second, every divisor of 2000 counts and
the answer comes out 20 instead of 12.

2000 = 2⁴·5³ has 20 divisors; the eight at or below 24 (1, 2, 4, 5, 8, 10, 16,
20) drop out. ``check`` ignores all of that and just runs the definition.
"""

from __future__ import annotations

PARAMS = {"total": 2024, "remainder": 24}
ANSWER = 12
VARIANTS = [
    {"total": 1000, "remainder": 10},
    {"total": 2024, "remainder": 8},
    {"total": 360, "remainder": 12},
    {"total": 5000, "remainder": 40},
    {"total": 99, "remainder": 3},
]


def _divisors(n: int) -> list[int]:
    out, d = [], 1
    while d * d <= n:
        if n % d == 0:
            out += [d, n // d]
        d += 1
    return sorted(set(out))


def solve(total=2024, remainder=24):
    """Count divisors of (total - remainder) that exceed the remainder."""
    if total <= remainder:
        return 0
    return sum(1 for d in _divisors(total - remainder) if d > remainder)


def check(total=2024, remainder=24):
    """Independent: run the definition of "divides with remainder" directly."""
    return sum(1 for n in range(1, total + 1) if total % n == remainder)
