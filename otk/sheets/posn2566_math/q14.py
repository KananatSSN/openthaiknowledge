"""ข้อ 14 — จำนวนวิธีจัดที่นอนโดยมีคู่ติดกันและคู่ที่ต้องแยก

มีคน 4 คน คือ A, B, C และ D เข้าพักห้องพักห้องหนึ่งซึ่งมีเตียงเดี่ยว 10 เตียงเรียงกัน
เป็นแถวตรง โดยที่ 1) A กับ B อยากได้เตียงนอนติดกัน 2) C กับ D อยากได้เตียงนอนติดกัน
3) A กับ C ไม่ต้องการได้เตียงนอนติดกัน  จงหาจำนวนวิธีที่จะจัดที่นอนให้ 4 คนนี้

Conditions 1 and 2 turn the two pairs into **blocks of two adjacent beds**, so a
placement is a choice of two disjoint adjacent-bed slots plus the order inside
each block. With B beds there are B − 1 slots, and two of them are disjoint
unless they are equal or neighbours:

    (B−1)² − (B−1) − 2(B−2)  ordered disjoint slot pairs      = 56 at B = 10

and 2 × 2 internal orders gives 224 placements satisfying 1 and 2.

Condition 3 only bites when the two blocks **touch** — slots i and i+2, which
share a boundary. Then exactly one of the four internal orders puts A and C on
the two beds either side of that boundary, and there are B − 3 such i in each
direction:

    224 − 2(B − 3) = 224 − 14 = **210**

Blocks separated by even one empty bed can never make A and C adjacent, which is
why only the touching case has to be subtracted.

``solve`` evaluates that count. ``check`` places the four people one at a time
over every ordered choice of four distinct beds and applies the three printed
conditions literally.
"""

from __future__ import annotations

from itertools import permutations

#: a row of `beds` single beds.
PARAMS = {"beds": 10}
ANSWER = 210
VARIANTS = [
    {"beds": 4},
    {"beds": 5},
    {"beds": 6},
    {"beds": 8},
    {"beds": 12},
    {"beds": 3},
]


def solve(beds=10):
    """Two blocks of two, minus the draws where the blocks touch the wrong way."""
    if beds < 4:
        return 0 if beds >= 0 else None
    slots = beds - 1
    disjoint = slots * slots - slots - 2 * (beds - 2)
    return 4 * disjoint - 2 * (beds - 3)


def check(beds=10):
    """Independent: try every ordered placement of the four people."""
    if beds < 0:
        return None
    if beds > 13:
        return None
    good = 0
    for a, b, c, d in permutations(range(1, beds + 1), 4):
        if abs(a - b) == 1 and abs(c - d) == 1 and abs(a - c) != 1:
            good += 1
    return good
