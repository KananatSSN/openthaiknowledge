"""ข้อ 11 — พื้นที่ของ △EBF ในรูปสี่เหลี่ยมผืนผ้าพื้นที่ 105

จากรูป รูปสี่เหลี่ยมผืนผ้า ABCD มีพื้นที่ 105 ตารางหน่วย จุด E และ F อยู่บนด้าน
AB และ BC ตามลำดับ ถ้า AE : EB = 4 : 3 และ BF : FC = 2 : 3
แล้วจงหาพื้นที่ของรูปสามเหลี่ยม EBF

The triangle is right-angled at B, so its area is half the product of the two
legs, and each leg is a printed fraction of a side:

    [EBF] = ½ · (3/7)·AB · (2/5)·BC = (3/35)·(AB·BC) = (3/35)·105 = **9**

**The rectangle's shape never enters** — only its area does, since AB·BC appears
as a single product. A 105 × 1 rectangle and a 15 × 7 one give the same answer,
which is why the question is answerable at all.

``solve`` evaluates that fraction of the area. ``check`` refuses the shortcut: it
builds four rectangles of genuinely different aspect ratios, each with the given
area, places E and F on them by the printed ratios, and takes the area of EBF
from the shoelace formula — then requires all four to agree.
"""

from __future__ import annotations

from fractions import Fraction

#: AE : EB = ae : eb along AB, and BF : FC = bf : fc along BC.
PARAMS = {"area": 105, "ae": 4, "eb": 3, "bf": 2, "fc": 3}
ANSWER = 9
VARIANTS = [
    {"area": 105, "ae": 1, "eb": 1, "bf": 1, "fc": 1},
    {"area": 120, "ae": 2, "eb": 1, "bf": 3, "fc": 5},
    {"area": 60, "ae": 4, "eb": 3, "bf": 2, "fc": 3},
    {"area": 210, "ae": 5, "eb": 2, "bf": 1, "fc": 4},
    {"area": 105, "ae": 3, "eb": 4, "bf": 3, "fc": 2},
    {"area": 96, "ae": 1, "eb": 3, "bf": 1, "fc": 2},
]


def solve(area=105, ae=4, eb=3, bf=2, fc=3):
    """½ · (eb/(ae+eb)) · (bf/(bf+fc)) · area."""
    if min(area, ae, eb, bf, fc) <= 0:
        return None
    value = (Fraction(area) * Fraction(eb, ae + eb) * Fraction(bf, bf + fc)) / 2
    return int(value) if value.denominator == 1 else value


def check(area=105, ae=4, eb=3, bf=2, fc=3):
    """Independent: measure EBF on four differently-shaped rectangles.

    Each rectangle has the printed area but a different width, so nothing can
    quietly depend on the shape; the triangle's area comes from the shoelace
    formula on the three actual corners. The four answers must agree exactly.
    """
    if min(area, ae, eb, bf, fc) <= 0:
        return None
    values = set()
    for width in (Fraction(1), Fraction(3), Fraction(7), Fraction(21, 2)):
        w = Fraction(width)
        h = Fraction(area) / w
        a = (Fraction(0), Fraction(0))
        b = (w, Fraction(0))
        c = (w, h)
        e = (w * Fraction(ae, ae + eb), Fraction(0))          # on AB
        f = (w, h * Fraction(bf, bf + fc))                    # on BC, from B
        del a, c
        shoelace = abs(e[0] * (b[1] - f[1]) + b[0] * (f[1] - e[1])
                       + f[0] * (e[1] - b[1])) / 2
        values.add(shoelace)
    if len(values) != 1:
        return None
    value = values.pop()
    return int(value) if value.denominator == 1 else value
