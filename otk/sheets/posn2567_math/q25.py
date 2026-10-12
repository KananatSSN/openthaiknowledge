"""ข้อ 25 — ผลต่างของจำนวนสมาชิกของเซต A และเซต B

ให้ A เป็นเซตของสามสิ่งอันดับ (x, y, z) ของจำนวนเต็มบวกทั้งหมดที่สอดคล้องกับสมการ
x + 2y + 3z = 12 และ B เป็นเซตของสามสิ่งอันดับ (x, y, z) ของจำนวนเต็มที่ไม่เป็นลบ
ทั้งหมดที่สอดคล้องกับสมการเดียวกัน  จงหาว่าเซต A และเซต B มีจำนวนสมาชิกต่างกันเท่าใด

|B| counts non-negative solutions of x + 2y + 3z = 12: nineteen of them. |A|
counts the strictly positive ones, which is the same count for
x' + 2y' + 3z' = 12 - (1+2+3) = 6: seven. The answer is 19 - 7 = **12**.

``solve`` reads both counts off a generating function — the coefficient of t^N in
1/((1-t)(1-t²)(1-t³)), built by polynomial multiplication — and shifts the total
by a+b+c for the positive count. ``check`` loops over the triples themselves.
"""

from __future__ import annotations

#: coefficients of the equation and its right-hand side.
PARAMS = {"a": 1, "b": 2, "c": 3, "total": 12}
ANSWER = 12
VARIANTS = [
    {"total": 20},
    {"total": 6},
    {"a": 1, "b": 1, "c": 1, "total": 10},
    {"a": 2, "b": 3, "c": 5, "total": 30},
    {"a": 1, "b": 2, "c": 3, "total": 5},        # too small for any positive triple
    {"a": 0, "b": 2, "c": 3, "total": 12},       # degenerate coefficient
]


def _nonneg(a: int, b: int, c: int, total: int) -> int:
    """Coefficient of t^total in 1/((1-t^a)(1-t^b)(1-t^c))."""
    ways = [0] * (total + 1)
    ways[0] = 1
    for step in (a, b, c):
        for s in range(step, total + 1):
            ways[s] += ways[s - step]
    return ways[total]


def solve(a=1, b=2, c=3, total=12):
    """|B| - |A|, both counted by the same generating function."""
    if min(a, b, c) < 1 or total < 0:
        return None
    shifted = total - (a + b + c)
    positive = 0 if shifted < 0 else _nonneg(a, b, c, shifted)
    return _nonneg(a, b, c, total) - positive


def check(a=1, b=2, c=3, total=12):
    """Independent: enumerate the triples and count each set directly."""
    if min(a, b, c) < 1 or total < 0:
        return None
    big = small = 0
    for z in range(total // c + 1):
        for y in range((total - c * z) // b + 1):
            rest = total - c * z - b * y
            if rest % a:
                continue
            x = rest // a
            big += 1
            small += x > 0 and y > 0 and z > 0
    return big - small
