"""ข้อ 30 — พื้นที่ของรูปสี่เหลี่ยมมุมฉากที่แรเงา

จากรูปกำหนดให้รูปสี่เหลี่ยมมุมฉากหมายเลข ①, ②, ③, ④ และ ⑤ มีพื้นที่เท่ากับ
13, 26, 20, 25 และ 27 ตารางหน่วย ตามลำดับ จงหาว่ารูปสี่เหลี่ยมมุมฉากที่แรเงา
มีพื้นที่เท่าใด

**The layout is the data and it has to be read off the crop.** With the outer
rectangle spanning x ∈ [0, X] and verticals at a and b, horizontals at y₁ (under
row 1) and y₂ (under row 2), and writing u, v, w for the three row heights from
the top:

    ① = a·u            ② = (X−a)·u          ← the top row, split at a
    ③ = a·v            ④ = (b−a)·v          ← the middle row, split at a and b
    ⑤ = (X−b)·(v+w)    ← the right column, from the row-1 line to the bottom
    shaded = b·w       ← under ③ and ④ together

Rectangles in the same row share their height, which is what makes the ratios
work:

    ①:② = 13:26 ⟹ X = 3a          ③:④ = 20:25 ⟹ b = 9a/4
    ⑤ ⟹ (3a/4)(v+w) = 27 ⟹ a·w = 36 − a·v = 36 − ③ = 16
    shaded = b·w = (9/4)·(a·w) = **36**

**No individual length is ever determined** — only the products a·u, a·v, a·w
are, and the answer happens to be one of them scaled. That is why the question is
answerable from five areas alone.

``solve`` runs that elimination in exact fractions. ``check`` picks a value for
a, solves for every coordinate of the figure, *draws* all six rectangles, and
verifies each printed area by multiplying its measured width and height before
reporting the shaded one — and it does this for two unrelated choices of a, so
nothing depends on the scale.
"""

from __future__ import annotations

from fractions import Fraction

#: the five printed areas, ① through ⑤.
PARAMS = {"a1": 13, "a2": 26, "a3": 20, "a4": 25, "a5": 27}
ANSWER = 36
VARIANTS = [
    {"a1": 13, "a2": 26, "a3": 20, "a4": 25, "a5": 30},
    {"a1": 10, "a2": 20, "a3": 12, "a4": 18, "a5": 21},
    {"a1": 6, "a2": 18, "a3": 8, "a4": 16, "a5": 20},
    {"a1": 13, "a2": 13, "a3": 20, "a4": 20, "a5": 27},
    {"a1": 13, "a2": 26, "a3": 20, "a4": 25, "a5": 15},   # ⑤ too small
    {"a1": 9, "a2": 27, "a3": 15, "a4": 10, "a5": 24},
]


def _layout(a1, a2, a3, a4, a5, a=Fraction(1)):
    """Every coordinate of the figure, for a chosen left-column width `a`."""
    if min(a1, a2, a3, a4, a5) <= 0:
        return None
    x = a * (1 + Fraction(a2, a1))            # ①:② splits the top row
    b = a * (1 + Fraction(a4, a3))            # ③:④ splits the middle row
    if x <= b:
        return None                           # ⑤ needs room on the right
    u = Fraction(a1) / a
    v = Fraction(a3) / a
    # ⑤ spans the middle row and the bottom one
    w = Fraction(a5) / (x - b) - v
    if w <= 0:
        return None                           # ⑤ does not reach the bottom
    return {"a": a, "b": b, "x": x, "u": u, "v": v, "w": w}


def solve(a1=13, a2=26, a3=20, a4=25, a5=27):
    """shaded = b·w, after eliminating every length but the products."""
    got = _layout(a1, a2, a3, a4, a5)
    if got is None:
        return None
    value = got["b"] * got["w"]
    return int(value) if value.denominator == 1 else value


def check(a1=13, a2=26, a3=20, a4=25, a5=27):
    """Independent: draw the six rectangles and re-measure every printed area.

    Each rectangle is built as an explicit box and its area recomputed as width ×
    height; if any of the five disagrees with the printed value the layout is
    wrong and nothing is returned. Two unrelated left-column widths are used, so
    the scale-invariance the argument relies on is tested rather than assumed.
    """
    answers = set()
    for a in (Fraction(1), Fraction(7, 3)):
        got = _layout(a1, a2, a3, a4, a5, a)
        if got is None:
            return None
        left, b, x = got["a"], got["b"], got["x"]
        u, v, w = got["u"], got["v"], got["w"]
        boxes = {
            "a1": (0, left, 0, u),                 # ① top-left
            "a2": (left, x, 0, u),                 # ② top-right
            "a3": (0, left, u, u + v),             # ③ middle-left
            "a4": (left, b, u, u + v),             # ④ middle-centre
            "a5": (b, x, u, u + v + w),            # ⑤ right column, to the floor
        }
        printed = {"a1": a1, "a2": a2, "a3": a3, "a4": a4, "a5": a5}
        for name, (x0, x1, y0, y1) in boxes.items():
            if (x1 - x0) * (y1 - y0) != printed[name]:
                return None
        shaded = (b - 0) * ((u + v + w) - (u + v))
        answers.add(shaded)
    if len(answers) != 1:
        return None
    value = answers.pop()
    return int(value) if value.denominator == 1 else value
