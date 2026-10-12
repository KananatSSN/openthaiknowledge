"""ข้อ 26 — จำนวนวิธีวางลูกบอลบนสี่ด้านของโต๊ะจัตุรัส

จงหาจำนวนวิธีที่แตกต่างกันทั้งหมดในการวางลูกบอลที่เหมือนกันทั้งหมด 8 ลูก ไว้บนด้านทั้งสี่
ของโต๊ะสี่เหลี่ยมจัตุรัสที่เหมือนกันทุกด้าน โดยแต่ละด้านต้องมีลูกบอลวางอย่างน้อย 1 ลูก
และลูกบอลแต่ละลูกจะถูกนับว่าวางอยู่บนด้านใดด้านหนึ่งของโต๊ะเท่านั้น

**"ที่เหมือนกันทุกด้าน" is the whole question.** If the sides were labelled the
answer would be the plain composition count C(7, 3) = 35; because they are not,
two placements that differ only by turning the table are the same placement, and
the count is over the orbits of the rotation group.

Burnside, on the four rotations of a square with 8 balls:

    identity   every composition             C(7,3) = 35
    90°, 270°  all four sides equal (2,2,2,2)          1 each
    180°       (a,b,a,b) with a + b = 4                3

    (35 + 1 + 3 + 1)/4 = **10**

In general the rotation by d has ``g = gcd(d, sides)`` free sides, each repeated
``sides/g`` times, so it fixes ``C(balls·g/sides − 1, g − 1)`` placements when
``sides/g`` divides balls and none otherwise.

Rotations only, not reflections: a table can be turned but not flipped over.
(Under the full dihedral group the answer would be 8 instead of 10 — the
generated question says out loud which one it means.)

``solve`` is that Burnside sum. ``check`` enumerates every composition, reduces
each to the smallest of its four rotations, and counts the distinct results —
no group theory anywhere.
"""

from __future__ import annotations

from math import comb, gcd

#: identical balls onto the sides of a regular table, at least one per side.
PARAMS = {"balls": 8, "sides": 4}
ANSWER = 10
VARIANTS = [
    {"balls": 8, "sides": 3},
    {"balls": 12, "sides": 4},
    {"balls": 6, "sides": 6},
    {"balls": 10, "sides": 5},
    {"balls": 3, "sides": 4},        # exactly one ball short: nothing works
    {"balls": 4, "sides": 4},
    {"balls": 15, "sides": 3},
]


def solve(balls=8, sides=4):
    """Burnside over the rotations of the table."""
    if sides < 1 or balls < sides:
        return None
    total = 0
    for turn in range(sides):
        free = gcd(turn, sides)
        block, remainder = divmod(balls * free, sides)
        if remainder or block < free:
            continue
        total += comb(block - 1, free - 1)
    quotient, remainder = divmod(total, sides)
    return quotient if remainder == 0 else None


def check(balls=8, sides=4):
    """Independent: list every composition and fold rotations together."""
    if sides < 1 or balls < sides:
        return None
    if comb(balls - 1, sides - 1) > 2 * 10 ** 5:
        return None

    def compositions(total: int, parts: int):
        if parts == 1:
            if total >= 1:
                yield (total,)
            return
        for first in range(1, total - parts + 2):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest

    seen = set()
    for arrangement in compositions(balls, sides):
        turns = [arrangement[i:] + arrangement[:i] for i in range(sides)]
        seen.add(min(turns))
    return len(seen)
