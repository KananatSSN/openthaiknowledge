"""ข้อ 17 — ค่าน้อยที่สุดที่เป็นไปได้ของ ab ที่ไม่เป็นลบ

กำหนดให้ a, b เป็นจำนวนเต็ม ที่สอดคล้องกับ (6a + b)² − (a + 6b)² = 4900
จงหาค่าน้อยที่สุดที่เป็นไปได้ของ ab ที่ ab ≥ 0

The left side expands to  35(a² − b²) = 4900, so  **a² − b² = 140**.

Factor as (a − b)(a + b) = 140.  Walk the divisor pairs (d, 140/d) with the
same parity (so a and b are integers): d·e = 140 with d ≡ e (mod 2).

    140 = 2·70  → a = 36, b = 34  → ab = 1224
    140 = 4·35  — different parity, skip
    140 = 10·14 → a = 12, b = 2   → ab = 24
    140 = 14·10 → a = 12, b = −2  → ab = −24 (skip, negative)
    140 = 2·70  → a = 36, b = −34 → ab = −1224 (skip)

Including negative factors and ab = 0 check: a² = 140 has no integer solution,
so ab = 0 is impossible. The least non-negative ab is **24**.

``solve`` walks divisor pairs.  ``check`` sweeps all (a, b) up to a bound.
"""

from __future__ import annotations

#: (6a + b)² − (a + 6b)² = rhs, find least non-negative ab.
PARAMS = {"rhs": 4900}
ANSWER = 24
VARIANTS = [
    {"rhs": 35},           # a² − b² = 1 → a = 1, b = 0, ab = 0
    {"rhs": 70},           # a² − b² = 2 → no solution (2 = 1·2, different parity)
    {"rhs": 140},          # a² − b² = 4 → (1,3) → a = 2, b = 1 → ab = 2
    {"rhs": 3500},         # a² − b² = 100
    {"rhs": 7000},         # a² − b² = 200
    {"rhs": 35 * 9},       # a² − b² = 9 → (1,9) → a = 5, b = 4 → ab = 20
]


def solve(rhs=4900):
    """Walk divisor pairs of rhs/35 to find the least non-negative ab."""
    if rhs % 35 != 0:
        return None
    diff = rhs // 35          # a² − b² = diff
    if diff < 0:
        return None

    best = None
    # (a − b)(a + b) = diff, so walk divisor pairs d | diff with d ≤ √diff
    # and d, diff/d same parity
    for d in range(1, abs(diff) + 1):
        if diff % d:
            continue
        e = diff // d         # d * e = diff, d = a − b, e = a + b
        if (d + e) % 2:
            continue
        a = (d + e) // 2
        b = (e - d) // 2
        ab = a * b
        if ab >= 0 and (best is None or ab < best):
            best = ab
        # also negative divisor pairs: d = -(a-b) → a-b = -d, a+b = -e
        if diff != 0:
            for d2, e2 in [(-d, -e)]:
                if (d2 + e2) % 2:
                    continue
                a2 = (d2 + e2) // 2
                b2 = (e2 - d2) // 2
                ab2 = a2 * b2
                if ab2 >= 0 and (best is None or ab2 < best):
                    best = ab2
    return best


def check(rhs=4900):
    """Independent: sweep all (a, b) and test the original equation."""
    if rhs % 35 != 0:
        return None
    diff = rhs // 35
    if diff < 0:
        return None

    bound = abs(diff) + 2
    if bound > 200_000:
        return None
    best = None
    for a in range(-bound, bound + 1):
        b_sq = a * a - diff
        if b_sq < 0:
            continue
        from math import isqrt
        b = isqrt(b_sq)
        if b * b != b_sq:
            continue
        for b_val in ([b, -b] if b != 0 else [0]):
            lhs = (6 * a + b_val) ** 2 - (a + 6 * b_val) ** 2
            if lhs != rhs:
                continue
            ab = a * b_val
            if ab >= 0 and (best is None or ab < best):
                best = ab
    return best
