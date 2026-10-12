"""ข้อ 29 — จำนวนหลอดไฟที่เปิดอยู่ในตอนท้าย

ในห้องประชุมแห่งหนึ่งมีหลอดไฟ 2562 ดวง ซึ่งแต่ละดวงติดหมายเลข 1 ถึง 2562 และมี
นักเรียน 2562 คน เข้าไปเปลี่ยนสถานะของหลอดไฟ (ปิดหรือเปิด) ทีละคนตามลำดับ โดย
นักเรียนแต่ละคนจะเปลี่ยนสถานะของหลอดไฟทุกดวงที่ลำดับการเข้าของตนเองหารหมายเลข
ของหลอดไฟดวงนั้นลงตัว (เช่น นักเรียนลำดับที่ 2 จะเปลี่ยนสถานะของหลอดไฟทุกดวงที่
เป็นหมายเลขคู่) ถ้าในตอนเริ่มต้นหลอดไฟทุกดวงมีสถานะเป็นปิด จงหาจำนวนหลอดไฟที่
เปิดอยู่หลังจากนักเรียนคนที่ 2562 เข้าไปเปลี่ยนสถานะของหลอดไฟเสร็จแล้ว

Bulb n is flipped once by each student whose number divides n — so exactly
``d(n)`` times, and it ends up **on** precisely when d(n) is odd.

Divisors pair up as ``k ↔ n/k``, which is a perfect matching *unless* the two
coincide, i.e. unless n is a perfect square. So the bulbs left on are exactly the
squares, and

    ⌊√2562⌋ = **50**

(50² = 2500 ≤ 2562 < 2601 = 51²). The count is the integer square root of the
number of bulbs, and nothing else about 2562 matters.

``solve`` returns that square root. ``check`` runs the room: it keeps a list of
booleans and lets every student walk their multiples, exactly as the story
describes, then counts what is left on.
"""

from __future__ import annotations

from math import isqrt

#: how many bulbs (and, equally, how many students).
PARAMS = {"bulbs": 2562}
ANSWER = 50
VARIANTS = [
    {"bulbs": 100},
    {"bulbs": 1},
    {"bulbs": 2500},
    {"bulbs": 2601},          # one more bulb: 51 of them stay on
    {"bulbs": 9},
    {"bulbs": 0},
]


def solve(bulbs=2562):
    """The number of perfect squares up to ``bulbs`` — the odd-divisor bulbs."""
    if bulbs < 1:
        return None
    return isqrt(bulbs)


def check(bulbs=2562):
    """Independent: flip the switches for real and count what is left on.

    Every student from 1 to ``bulbs`` walks their own multiples and toggles each
    one, starting from all-off, and the bulbs still on are counted at the end.
    Nothing about divisor counts or square numbers appears.
    """
    if bulbs < 1:
        return None
    if bulbs > 2 * 10 ** 5:
        return None
    lit = [False] * (bulbs + 1)
    for student in range(1, bulbs + 1):
        for bulb in range(student, bulbs + 1, student):
            lit[bulb] = not lit[bulb]
    return sum(lit[1:])
