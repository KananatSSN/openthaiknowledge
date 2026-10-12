"""ข้อ 6 — สมชายกินช็อกโกแลตไปกี่ชิ้น

กล่องใบหนึ่งบรรจุช็อกโกแลตและลูกอมรวมกันจำนวน 110 ชิ้น โดยมีอัตราส่วนระหว่างจำนวน
ช็อกโกแลตกับลูกอมเป็น 4:7  สมชายกินลูกอมไป 10 ชิ้น และกินช็อกโกแลตไปจำนวนหนึ่ง
ทำให้อัตราส่วนระหว่างจำนวนช็อกโกแลตกับลูกอมเปลี่ยนเป็น 1:6  จงหาว่าสมชายกิน
ช็อกโกแลตไปกี่ชิ้น

The ratio 4:7 splits 110 into 40 chocolates and 70 sweets. Ten sweets go, leaving
60, and the new ratio 1:6 forces 10 chocolates to remain — so he ate

    40 - 10 = **30**.

In general, with a total T split a:b, ``eaten`` sweets and a new ratio c:d,

    choc₀ = T·a/(a+b),   sweet₁ = T·b/(a+b) - eaten,   choc₁ = sweet₁·c/d

and the answer is choc₀ - choc₁. ``solve`` returns ``None`` unless every one of
those is a non-negative whole number — most constants split 110 into fractions of
a sweet, and the generator's pool is exactly the ones that do not.
"""

from __future__ import annotations

from fractions import Fraction

#: total, the starting ratio a:b, the sweets eaten, and the ending ratio c:d.
PARAMS = {"total": 110, "a": 4, "b": 7, "eaten": 10, "c": 1, "d": 6}
ANSWER = 30
VARIANTS = [
    {"total": 60, "a": 1, "b": 2, "eaten": 5, "c": 1, "d": 3},
    {"total": 120, "a": 5, "b": 7, "eaten": 20, "c": 1, "d": 2},
    {"total": 110, "a": 4, "b": 7, "eaten": 0, "c": 4, "d": 7},   # nothing eaten
    {"total": 110, "a": 4, "b": 7, "eaten": 10, "c": 1, "d": 2},  # no whole answer
    {"total": 110, "a": 4, "b": 7, "eaten": 90, "c": 1, "d": 6},  # too many sweets
]


def solve(total=110, a=4, b=7, eaten=10, c=1, d=6):
    """Chocolates eaten, or None if the counts are not all whole and non-negative."""
    if min(total, a, b, c, d) <= 0 or eaten < 0:
        return None
    choc0 = Fraction(total * a, a + b)
    sweet0 = Fraction(total * b, a + b)
    if choc0.denominator != 1 or sweet0.denominator != 1:
        return None
    sweet1 = sweet0 - eaten
    if sweet1 < 0:
        return None
    choc1 = sweet1 * Fraction(c, d)
    if choc1.denominator != 1 or not 0 <= choc1 <= choc0:
        return None
    return int(choc0 - choc1)


def check(total=110, a=4, b=7, eaten=10, c=1, d=6):
    """Independent: try every number of chocolates he could have eaten.

    The two ratios are tested as equalities of whole counts, so nothing here
    relies on the algebra above — and a constant set with no answer, or with more
    than one, comes back as ``None`` on its own.
    """
    if min(total, a, b, c, d) <= 0 or eaten < 0:
        return None
    hits = []
    for choc0 in range(total + 1):
        sweet0 = total - choc0
        if choc0 * (a + b) != total * a or sweet0 * (a + b) != total * b:
            continue
        sweet1 = sweet0 - eaten
        if sweet1 < 0:
            continue
        for gone in range(choc0 + 1):
            choc1 = choc0 - gone
            if choc1 * d == sweet1 * c:
                hits.append(gone)
    if len(hits) != 1:
        return None
    return hits[0]
