"""ข้อ 9 — ความน่าจะเป็นที่อัตราส่วนในทั้งสองกล่องเปลี่ยนไป

มีกล่องบรรจุลูกแก้ว 2 ใบ กล่องที่ 1 มีสีแดง 3 ลูก สีน้ำเงิน 2 ลูก กล่องที่ 2 มีสีแดง 2 ลูก
สีน้ำเงิน 3 ลูก  สุ่มหยิบลูกแก้ว 1 ลูกจากกล่องที่ 1 ใส่ลงในกล่องที่ 2 แล้วสุ่มหยิบลูกแก้ว
1 ลูกจากกล่องที่ 2 ใส่กลับลงในกล่องที่ 1  จงหาความน่าจะเป็นที่ในแต่ละกล่อง อัตราส่วนของ
จำนวนลูกแก้วสีแดงต่อจำนวนลูกแก้วสีน้ำเงินไม่เหมือนเดิม

**The two boxes rise and fall together.** Whatever leaves box 1 arrives in box 2
and vice versa, so after the round trip box 1 is back to its start exactly when
the ball that came back is the same colour as the one that left — and box 2 is
back at the same moment. So the event "both ratios changed" is simply

    the second ball is a different colour from the first

(a ratio r : b really does change when it becomes (r−1) : (b+1), since
(r−1)b = r(b+1) would need r = −b).

With 3 red and 2 blue in box 1, and 2 red and 3 blue in box 2:

    red then blue:  (3/5)·(3/6) = 3/10       blue then red:  (2/5)·(2/6) = 2/15

    total = 3/10 + 2/15 = **13/30**

The second factor is where the moved ball is already counted — box 2 holds six
marbles for the second draw, not five.

``solve`` adds those two disjoint paths in exact fractions. ``check`` labels
every marble individually and enumerates all ordered pairs of draws, comparing
the resulting counts against the starting ones rather than reasoning about
colours at all.
"""

from __future__ import annotations

from fractions import Fraction

#: (red, blue) in each box; one ball moves each way.
PARAMS = {"box1": (3, 2), "box2": (2, 3)}
ANSWER = Fraction(13, 30)
VARIANTS = [
    {"box1": (1, 1), "box2": (1, 1)},
    {"box1": (4, 1), "box2": (1, 4)},
    {"box1": (5, 5), "box2": (2, 8)},
    {"box1": (3, 0), "box2": (0, 3)},
    {"box1": (2, 7), "box2": (6, 1)},
    {"box1": (0, 0), "box2": (2, 2)},        # nothing to draw from box 1
]


def solve(box1=(3, 2), box2=(2, 3)):
    """Two disjoint paths: out red back blue, or out blue back red."""
    r1, b1 = box1
    r2, b2 = box2
    n1, n2 = r1 + b1, r2 + b2
    if n1 <= 0 or n2 < 0 or min(r1, b1, r2, b2) < 0:
        return None
    # after one arrives, box 2 holds n2 + 1
    red_out = Fraction(r1, n1) * Fraction(b2, n2 + 1)
    blue_out = Fraction(b1, n1) * Fraction(r2, n2 + 1)
    return red_out + blue_out


def check(box1=(3, 2), box2=(2, 3)):
    """Independent: label every marble and compare the final counts.

    Each individual marble is a distinct outcome, so the sample space is
    ``n₁ × (n₂ + 1)`` equally likely ordered pairs. A pair counts when *both*
    boxes end with a (red, blue) pair different from the one they started with —
    the colour argument is never used.
    """
    r1, b1 = box1
    r2, b2 = box2
    n1, n2 = r1 + b1, r2 + b2
    if n1 <= 0 or n2 < 0 or min(r1, b1, r2, b2) < 0:
        return None

    good = 0
    total = 0
    for first in ["R"] * r1 + ["B"] * b1:
        mid2 = (r2 + (first == "R"), b2 + (first == "B"))
        mid1 = (r1 - (first == "R"), b1 - (first == "B"))
        for second in ["R"] * mid2[0] + ["B"] * mid2[1]:
            total += 1
            end1 = (mid1[0] + (second == "R"), mid1[1] + (second == "B"))
            end2 = (mid2[0] - (second == "R"), mid2[1] - (second == "B"))
            if end1 != box1 and end2 != box2:
                good += 1
    if total == 0:
        return None
    return Fraction(good, total)
