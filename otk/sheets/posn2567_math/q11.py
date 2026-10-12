"""ข้อ 11 — พื้นที่ของรูปสามเหลี่ยม AEG ในรูปสี่เหลี่ยมจัตุรัส

จากรูป ABCD เป็นรูปสี่เหลี่ยมจัตุรัส โดยมี EG ขนานกับ AB และ BF ตั้งฉากกับ FC
ที่จุด F  ถ้า BF = 8 แล้วพื้นที่ของรูปสามเหลี่ยม AEG เท่ากับกี่ตารางหน่วย

รูปประกอบ (extract/figures/item11.png), read as follows:

* A top-left, B top-right, C bottom-right, D bottom-left.
* E on AD̅ and G on BC̅, so EG̅ is a full-width horizontal segment.
* F lies **on EG̅**, between E and G, and the right angle mark at F is ∠BFC.
* The triangle in question is AEG: base EG̅ (the whole width) and apex A.

Put D at the origin with side s: A=(0,s), B=(s,s), C=(s,0), E=(0,y), G=(s,y),
F=(f,y). ``BF ⊥ FC`` reads

    (s-f)² = y(s-y)

and then

    BF² = (s-f)² + (s-y)² = y(s-y) + (s-y)² = s(s-y).

The triangle AEG has base EG = s and height AE = s-y, so its area is

    s(s-y)/2 = BF²/2

— the side of the square never appears. That is the whole point of the item: it
gives BF and nothing else. ``PARAMS`` still carries a side so the variants can
push it around and ``check`` can rebuild the square each time; a ``solve`` that
had smuggled in a dependence on it would be caught at once.

The configuration exists only while BF < side (otherwise y ≤ 0 and E leaves the
square), which is what ``solve`` returns ``None`` for.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: BF, and the side of the square the figure is drawn at.
PARAMS = {"bf": 8, "side": 12}
ANSWER = Fraction(32)
VARIANTS = [
    {"bf": 8, "side": 20},          # same answer, a much bigger square
    {"bf": 6, "side": 7},           # F almost at G
    {"bf": 5, "side": 13},
    {"bf": 1, "side": 100},
    {"bf": 12, "side": 12},         # degenerate: y = 0, no triangle
]
TOL = 1e-9


def solve(bf=8, side=12):
    """Area of △AEG — half of BF², whatever the square's side."""
    if bf <= 0 or side <= 0 or bf >= side:
        return None
    return Fraction(bf) ** 2 / 2


def check(bf=8, side=12):
    """Independent: build the square in coordinates and shoelace the triangle.

    ``y`` and ``f`` are solved from the two conditions numerically, the right
    angle at F is asserted rather than assumed, and the area comes out of the
    shoelace formula — no algebra from ``solve`` is reused.
    """
    if bf <= 0 or side <= 0 or bf >= side:
        return None
    s = float(side)

    # Find y on (0, s) with BF(y) = bf, by bisection. BF² = (s-f)² + (s-y)²
    # where (s-f)² = y(s-y); BF falls as y rises, so bracket accordingly.
    def bf_at(y: float) -> float:
        f = s - math.sqrt(y * (s - y))
        return math.hypot(s - f, s - y)

    lo, hi = 1e-12, s - 1e-12
    if not bf_at(lo) >= bf >= bf_at(hi):
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if bf_at(mid) >= bf:
            lo = mid
        else:
            hi = mid
    y = (lo + hi) / 2
    f = s - math.sqrt(y * (s - y))

    a, b, c = (0.0, s), (s, s), (s, 0.0)
    e, g, fp = (0.0, y), (s, y), (f, y)
    # BF ⊥ FC, exactly as the figure marks it.
    assert abs((b[0] - fp[0]) * (c[0] - fp[0])
               + (b[1] - fp[1]) * (c[1] - fp[1])) < 1e-6 * s * s
    assert abs(math.dist(b, fp) - bf) < 1e-6 * s

    area = abs(a[0] * (e[1] - g[1]) + e[0] * (g[1] - a[1])
               + g[0] * (a[1] - e[1])) / 2
    return Fraction(area).limit_denominator(10 ** 6)
