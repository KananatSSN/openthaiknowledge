"""ข้อ 8 — จำนวนจุดบนวงกลมจากจำนวนเส้นเชื่อมที่เท่ากันสองครั้ง

มีจุดอยู่บนเส้นรอบวงของวงกลมจำนวน n จุด โดยที่ n ≥ 2 กำหนดสีจุดแต่ละจุดเป็นสีแดงหรือสีดำ
สีใดสีหนึ่งเพียงสีเดียว ลากเส้นเชื่อมต่อระหว่างจุดสองจุดใด ๆ บนเส้นรอบวงที่มีสีต่างกัน
ให้ N_k แทนจำนวนเส้นเชื่อม เมื่อมีจุดสีดำจำนวน k จุด  พบว่า N_m = N_{m+1} = 90
สำหรับบาง m ∈ {1, 2, …, n − 1}  จงหาค่าของ n

Every black point joins to every red point and nothing else, so

    N_k = k(n − k)

The two printed equalities are then one equation each, and subtracting them
removes the target entirely:

    m(n − m) = (m+1)(n − m − 1)   ⟹   n = 2m + 1

The count is symmetric about n/2, so N_m = N_{m+1} says m and m+1 are equidistant
from the middle — which pins n to an odd number with m just below the middle.
Feeding that back:

    m(n − m) = m(m + 1) = 90   ⟹   m = 9   ⟹   **n = 19**

``solve`` completes the square on ``m(m+1) = target``. ``check`` never forms
either equation: it tabulates ``k(n−k)`` for every (n, k) in range and looks for
a row with two equal consecutive entries hitting the target.
"""

from __future__ import annotations

from math import isqrt

#: N_m = N_{m+1} = target.
PARAMS = {"target": 90}
ANSWER = 19
VARIANTS = [
    {"target": 2},
    {"target": 6},
    {"target": 12},
    {"target": 20},
    {"target": 100},          # not of the form m(m+1): no such n
    {"target": 9900},
]


def solve(target=90):
    """n = 2m + 1 where m(m+1) = target."""
    if target < 1:
        return None
    # m² + m − target = 0
    disc = 1 + 4 * target
    root = isqrt(disc)
    if root * root != disc:
        return None
    m = (root - 1) // 2
    if m * (m + 1) != target or m < 1:
        return None
    return 2 * m + 1


def check(target=90):
    """Independent: tabulate k(n−k) and look for two equal consecutive entries."""
    if target < 1:
        return None
    limit = 4 * target + 8
    if limit > 4 * 10 ** 5:
        return None
    found = set()
    for n in range(2, limit):
        for m in range(1, n):
            if m * (n - m) == target and (m + 1) * (n - m - 1) == target:
                found.add(n)
    if len(found) != 1:
        return None
    return found.pop()
